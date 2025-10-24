require('dotenv').config();
const xlsx = require("xlsx");
const { MongoClient } = require("mongodb");

async function importExcelToMongo() {
  const uri = process.env.MONGO_URI; 
  const client = new MongoClient(uri);

  try {
    await client.connect();
    const db = client.db("relationsTogether");

    const filePath = "TestNewStructure.xlsx";
    const workbook = xlsx.readFile(filePath);

    for (const sheetName of workbook.SheetNames) {
      const sheet = workbook.Sheets[sheetName];
      let records = xlsx.utils.sheet_to_json(sheet);

      if (records.length > 0) {
        let collectionName = sheetName;

        if (sheetName === "GIVES_POSTURAL_SUPPORT_IN" || sheetName === "TRANSFERS_FORCES_FROM" || sheetName === "TRANSFERS_FORCES_TO" || sheetName === "HAS_AIM" || sheetName === "HAS_PROPERTY") {
          collectionName = "Relations";

          records = records.map(record => ({
            ...record,
            type: sheetName
          }));
        }

        const collection = db.collection(collectionName);
        await collection.insertMany(records);
        console.log(
          `Inserted ${records.length} documents into collection: ${collectionName} (from ${sheetName})`
        );
      }
    }
  } catch (err) {
    console.error("Error:", err);
  } finally {
    await client.close();
  }
}

importExcelToMongo();
