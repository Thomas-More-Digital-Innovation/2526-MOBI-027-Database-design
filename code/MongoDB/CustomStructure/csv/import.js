require("dotenv").config();
const fs = require("fs");
const path = require("path");
const csv = require("csv-parser");
const { MongoClient } = require("mongodb");

async function importAllCSVs() {
  const uri = process.env.MONGO_URI;
  const DB_NAME = process.env.DB_NAME;
  const client = new MongoClient(uri);

  try {
    await client.connect();
    const db = client.db(DB_NAME);
    const files = fs.readdirSync(".").filter(file => file.endsWith(".csv"));

    for (const file of files) {
      const collectionName = path.basename(file, ".csv");
      const isRelation = collectionName.includes("_");
      const records = await parseCSV(file, isRelation);

      if (records.length > 0) {
        const collection = db.collection(collectionName);
        await collection.insertMany(records);
        console.log(`✅ Inserted ${records.length} documents into "${collectionName}"`);
      } else {
        console.log(`⚠️ Skipped "${file}" (no records found)`);
      }
    }
  } catch (err) {
    console.error("❌ Error:", err);
  } finally {
    await client.close();
  }
}

function parseCSV(filePath, isRelation) {
  return new Promise((resolve, reject) => {
    const results = [];
    let firstColumnName = null;

    fs.createReadStream(filePath)
      .pipe(csv({ separator: ';' }))
      .on("data", (data) => {
        // Only replace _id for non-relation files
        if (!isRelation) {
          // Get the first column name from the first row
          if (!firstColumnName) {
            firstColumnName = Object.keys(data)[0];
          }

          // Use the first column as _id
          if (firstColumnName && data[firstColumnName]) {
            data._id = parseInt(data[firstColumnName]) || data[firstColumnName];
            delete data[firstColumnName];
          }
        }
        
        results.push(data);
      })
      .on("end", () => resolve(results))
      .on("error", (err) => reject(err));
  });
}

importAllCSVs();