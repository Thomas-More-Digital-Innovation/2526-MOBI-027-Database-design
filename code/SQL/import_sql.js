import fs from "fs";
import path from "path";
import csv from "csv-parser";
import mysql from "mysql2/promise";

const connectionConfig = {
  host: "localhost",
  user: "root",
  password: "",
  database: "Jobtakels",
};

const csvDir = path.resolve("./csv");

// Import order respecting foreign keys
const importOrder = [
  "Dof",
  "Exo",
  "ExoProperty",
  "StructureKinematicName",
  "Part",
  "HAS_PROPERTY",
  "HAS_AIM",
  "GIVES_POSTURAL_SUPPORT_IN",
  "TRANSFERS_FORCES_FROM",
  "TRANSFERS_FORCES_TO",
];

async function importAllCSV() {
  const connection = await mysql.createConnection(connectionConfig);
  console.log("✅ Connected to MySQL");

  for (const tableName of importOrder) {
    const filePath = path.join(csvDir, `${tableName}.csv`);
    if (!fs.existsSync(filePath)) {
      console.warn(`⚠️  Missing CSV for table ${tableName}`);
      continue;
    }

    console.log(`\n📥 Importing ${tableName}.csv → ${tableName}`);
    const rows = await readCSV(filePath);
    if (!rows.length) {
      console.warn(`⚠️  Skipping ${tableName} — empty file`);
      continue;
    }

    const columns = Object.keys(rows[0]);
    const placeholders = columns.map(() => "?").join(",");
    const sql = `INSERT INTO \`${tableName}\` (${columns.join(",")}) VALUES (${placeholders})`;

    let success = 0, failed = 0;

    for (const row of rows) {
      const values = columns.map(c => row[c] || null);
      try {
        await connection.execute(sql, values);
        success++;
      } catch (err) {
        failed++;
        console.error(`❌ Error in ${tableName}: ${err.message}`);
      }
    }

    console.log(`✅ Imported ${success} rows into ${tableName} (${failed} failed)`);
  }

  await connection.end();
  console.log("\n🎉 All imports finished!");
}

function readCSV(filePath) {
  return new Promise((resolve, reject) => {
    const results = [];
    fs.createReadStream(filePath)
      .pipe(csv({ separator: ";" }))
      .on("data", d => results.push(d))
      .on("end", () => resolve(results))
      .on("error", reject);
  });
}

importAllCSV().catch(err => console.error("💥 Fatal error:", err));
