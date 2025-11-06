require("dotenv").config();
const fs = require("fs");
const path = require("path");
const { MongoClient } = require("mongodb");

async function importAllJSONs() {
  const uri = process.env.MONGO_URI;
  const DB_NAME = process.env.DB_NAME;
  const client = new MongoClient(uri);

  try {
    await client.connect();
    const db = client.db(DB_NAME);

    const files = fs.readdirSync(".").filter(file => file.endsWith(".json"));

    for (const file of files) {
      const collectionName = path.basename(file, ".json");
      const isRelation = collectionName.includes("_");
      const filePath = path.join(".", file);

      const fileContent = fs.readFileSync(filePath, "utf8");
      let records;
      try {
        records = JSON.parse(fileContent);
      } catch (err) {
        console.error(`❌ Failed to parse ${file}: ${err.message}`);
        continue;
      }

      if (!Array.isArray(records)) {
        records = [records];
      }

      // Process records to use first property as _id for non-relation files
      if (!isRelation && records.length > 0) {
        records = records.map(record => {
          const firstKey = Object.keys(record)[0];
          if (firstKey && record[firstKey] !== undefined) {
            const newRecord = { ...record };
            newRecord._id = parseInt(record[firstKey]) || record[firstKey];
            delete newRecord[firstKey];
            return newRecord;
          }
          return record;
        });
      }

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

importAllJSONs();