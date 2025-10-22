// import.js (CommonJS / supports .env configuration)
require("dotenv").config(); // Load environment variables
const fs = require("fs");
const { MongoClient } = require("mongodb");

// Load configuration from environment variables or use defaults
const MONGO_URI = process.env.MONGO_URI || "mongodb://localhost:27017";
const DB_NAME = process.env.DB_NAME || "neo4j_import_test_relations_split";
const JSON_FILE = process.env.JSON_FILE || "./neo4j_query_table_data_2025-10-13.json";

async function run() {
  // 1) load file
  const raw = JSON.parse(fs.readFileSync(JSON_FILE, "utf8"));
  console.log(`📥 totaal records in JSON: ${raw.length}`);

  // 2) collect unique nodes per label
  const collections = {}; // label -> Map(identity -> doc)
  const relatiesByType = {}; // type -> array of relations

  function saveNode(node) {
    if (!node) return;
    const label = (node.labels && node.labels[0]) || "Unknown";
    if (!collections[label]) collections[label] = new Map();
    if (!collections[label].has(node.identity)) {
      // prepare doc; use identity as _id so upserts are easy
      const doc = Object.assign(
        { _id: node.identity, _neo4jElementId: node.elementId, _label: label },
        node.properties || {}
      );
      collections[label].set(node.identity, doc);
    }
  }

  for (const rec of raw) {
    const { n, r, m } = rec;
    saveNode(n);
    saveNode(m);

    if (r) {
      // Group relationships by type
      const relationType = r.type || "UNKNOWN";
      if (!relatiesByType[relationType]) {
        relatiesByType[relationType] = [];
      }

      const rela = {
        neo4jId: r.identity,
        elementId: r.elementId,
        type: r.type,
        start: r.start,
        end: r.end,
        startElementId: r.startNodeElementId,
        endElementId: r.endNodeElementId,
        properties: r.properties || {},
      };
      relatiesByType[relationType].push(rela);
    }
  }

  // Counts pre-insert
  const nodeCounts = {};
  let totalNodes = 0;
  for (const [label, map] of Object.entries(collections)) {
    nodeCounts[label] = map.size;
    totalNodes += map.size;
  }
  console.log(`🧾 unieke nodes per collectie (voor import):`, nodeCounts);

  console.log(`\n🔗 relaties per type:`);
  let totalRelations = 0;
  for (const [type, relations] of Object.entries(relatiesByType)) {
    console.log(`   - ${type}: ${relations.length}`);
    totalRelations += relations.length;
  }
  console.log(`🔗 totaal relaties: ${totalRelations}`);

  // 3) Insert/upsert into MongoDB
  const client = new MongoClient(MONGO_URI, { useUnifiedTopology: true });
  try {
    await client.connect();
    const db = client.db(DB_NAME);
    console.log(`\n🗄️ Verbonden met DB '${DB_NAME}'`);

    // Import nodes
    for (const [label, map] of Object.entries(collections)) {
      const coll = db.collection(label);

      const ops = [];
      for (const doc of map.values()) {
        ops.push({
          replaceOne: {
            filter: { _id: doc._id },
            replacement: doc,
            upsert: true,
          },
        });
      }

      if (ops.length > 0) {
        const res = await coll.bulkWrite(ops, { ordered: false });
        console.log(
          `✅ '${label}': upserted ${res.upsertedCount + res.modifiedCount} docs (ops: ${ops.length})`
        );
      } else {
        console.log(`ℹ️ '${label}': geen documenten om te importeren`);
      }
    }

    // Import relationships - each type in its own collection
    console.log(`\n📦 Importeren van relatie collecties...`);
    for (const [relationType, relations] of Object.entries(relatiesByType)) {
      const relColl = db.collection(relationType);

      // Clear old relations first for clean import
      await relColl.deleteMany({});

      if (relations.length > 0) {
        // Create indexes for query performance
        try {
          await relColl.createIndex({ neo4jId: 1 }, { background: false });
          await relColl.createIndex({ start: 1 }, { background: false });
          await relColl.createIndex({ end: 1 }, { background: false });
          await relColl.createIndex({ start: 1, end: 1 }, { background: false });
        } catch (e) {
          // ignore index-creation errors
        }

        // Insert all relationships of this type
        try {
          const res = await relColl.insertMany(relations, { ordered: false });
          console.log(
            `✅ '${relationType}': inserted ${res.insertedCount} van ${relations.length}`
          );
        } catch (err) {
          if (err && err.result && err.result.result) {
            const inserted = err.result.result.nInserted || 0;
            console.log(
              `⚠️ '${relationType}' bulk insert fouten: ${
                err.writeErrors ? err.writeErrors.length : "unknown"
              }, succesvol: ${inserted}`
            );
          } else {
            console.log(
              `⚠️ '${relationType}' fout tijdens insert:`,
              err.message || err
            );
          }
        }

        // Verify count
        const finalCount = await relColl.countDocuments({});
        console.log(`   📊 '${relationType}' totaal in database: ${finalCount}`);
      } else {
        console.log(`ℹ️ '${relationType}': geen relaties om te importeren`);
      }
    }

    console.log("\n🚀 Import voltooid.");
  } finally {
    await client.close();
  }
}

run().catch((err) => {
  console.error("FATALE FOUT:", err);
  process.exit(1);
});
