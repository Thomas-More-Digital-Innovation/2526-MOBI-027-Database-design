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
      let records = xlsx.utils.sheet_to_json(sheet);

      console.log(`\n📄 Processing sheet: ${sheetName}`);
      
      if (records.length > 0) {
        console.log(`First record:`, records[0]);
        
        // Ensure _id is properly typed (convert to number if possible)
        records = records.map(record => {
          if (record._id !== undefined) {
            record._id = parseInt(record._id) || record._id;
          }
          return record;
        });

        const collection = db.collection(sheetName);
        await collection.deleteMany({});
        await collection.insertMany(records);
        console.log(`✅ Inserted ${records.length} documents into collection: ${sheetName}`);
      }
    }
  } catch (err) {
    console.error("❌ Error:", err);
  } finally {
    await client.close();
  }
}

importExcelToMongo();