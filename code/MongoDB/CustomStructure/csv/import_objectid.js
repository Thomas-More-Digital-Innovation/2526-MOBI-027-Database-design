require("dotenv").config();
const fs = require("fs");
const path = require("path");
const csv = require("csv-parser");
const { MongoClient, ObjectId } = require("mongodb");

const uri = process.env.MONGO_URI;
const DB_NAME = process.env.DB_NAME;

async function importCSVsWithObjectId() {
  const client = new MongoClient(uri);
  try {
    await client.connect();
    const db = client.db(DB_NAME);

    // --- Stap 1: Exo en Part importeren ---
    const exoMapping = await importCollection(db, "Exo.csv", "exos", "exoId");
    const partMapping = await importCollection(db, "Part.csv", "parts", "partId");

    // --- Stap 2: TRANSFERS_FORCES_FROM importeren ---
    const transfersFile = "TRANSFERS_FORCES_FROM.csv";
    const transfers = await parseCSV(transfersFile);

    // Vervang CSV-ID door MongoDB ObjectId
    const transfersWithObjectId = transfers.map(t => {
      const exoIdNum = Number(t.exoId.trim());
      const partIdNum = Number(t.partId.trim());

      const exoMongoId = exoMapping[exoIdNum];
      const partMongoId = partMapping[partIdNum];

      if (!exoMongoId || !partMongoId) {
        console.warn(`⚠️ Mapping missing for transfer row: exoId=${t.exoId}, partId=${t.partId}`);
      }

      return {
        exoId: exoMongoId,
        partId: partMongoId
      };
    });

    const transfersCollection = db.collection("transfers_forces_from");
    await transfersCollection.insertMany(transfersWithObjectId);
    console.log(`✅ Imported ${transfersWithObjectId.length} transfers with ObjectId references.`);

  } catch (err) {
    console.error(err);
  } finally {
    await client.close();
  }
}

// Functie om een collectie te importeren en een mapping terug te geven
async function importCollection(db, filePath, collectionName, csvIdField) {
  const records = await parseCSV(filePath);

  // Zorg dat alle ID's getrimd en genummerd zijn
  records.forEach(record => {
    record[csvIdField] = Number(record[csvIdField].trim());
  });

  const collection = db.collection(collectionName);
  const result = await collection.insertMany(records);

  // Maak een mapping: CSV-ID -> MongoDB _id
  const mapping = {};
  records.forEach((record, index) => {
    mapping[record[csvIdField]] = result.insertedIds[index];
  });

  console.log(`✅ Imported ${records.length} documents into ${collectionName}`);
  return mapping;
}

// CSV parser
function parseCSV(filePath) {
  return new Promise((resolve, reject) => {
    const results = [];
    fs.createReadStream(filePath)
      .pipe(csv({ separator: ';' }))
      .on("data", (data) => results.push(data))
      .on("end", () => resolve(results))
      .on("error", (err) => reject(err));
  });
}

importCSVsWithObjectId();
