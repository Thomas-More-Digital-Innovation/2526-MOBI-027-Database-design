require('dotenv').config();
const xlsx = require("xlsx");
const { MongoClient } = require("mongodb");

async function importExcelToMongo() {
  const uri = process.env.MONGO_URI;
  const DB_NAME = process.env.DB_NAME;
  const client = new MongoClient(uri);

  try {
    await client.connect();
    const db = client.db(DB_NAME);

    const filePath = "Exo_GIVES_SUPPORT_Dof.xlsx";
    const workbook = xlsx.readFile(filePath);

    for (const sheetName of workbook.SheetNames) {
      const sheet = workbook.Sheets[sheetName];
      const records = xlsx.utils.sheet_to_json(sheet);

      if (records.length > 0) {
        const collection = db.collection(sheetName);
        await collection.insertMany(records);
        console.log(`Inserted ${records.length} documents into collection: ${sheetName}`);
      }
    }
  } catch (err) {
    console.error("Error:", err);
  } finally {
    await client.close();
  }
}

importExcelToMongo();
