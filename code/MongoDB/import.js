// import.js (CommonJS / werkt zonder "type":"module")
const fs = require("fs");
const { MongoClient } = require("mongodb");

const MONGO_URI = "mongodb://localhost:27017";
const DB_NAME = "neo4j_import_test";
const JSON_FILE = "./neo4j_query_table_data_2025-10-13.json";

async function run() {
  // 1) load file
  const raw = JSON.parse(fs.readFileSync(JSON_FILE, "utf8"));
  console.log(`📥 totaal records in JSON: ${raw.length}`);

  // 2) collect unique nodes per label
  const collections = {}; // label -> Map(identity -> doc)
  const relatiesList = []; // CHANGED: Use array instead of Map to keep ALL relations

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
      // CHANGED: Push ALL relationships to array (no deduplication)
      const rela = {
        neo4jId: r.identity,
        elementId: r.elementId, // Added for completeness
        type: r.type,
        start: r.start,
        end: r.end,
        startElementId: r.startNodeElementId,
        endElementId: r.endNodeElementId,
        properties: r.properties || {}
      };
      relatiesList.push(rela);
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
  console.log(`🔗 totaal relaties (inclusief eventuele duplicaten): ${relatiesList.length}`);

  // Count unique neo4jId values to see if there are actual duplicates
  const uniqueNeo4jIds = new Set(relatiesList.map(r => r.neo4jId));
  console.log(`🔗 unieke neo4jId waarden: ${uniqueNeo4jIds.size}`);
  if (uniqueNeo4jIds.size < relatiesList.length) {
    console.log(`⚠️  Er zijn ${relatiesList.length - uniqueNeo4jIds.size} duplicate neo4jId waarden`);
  }

  // 3) Insert/upsert into MongoDB
  const client = new MongoClient(MONGO_URI, { useUnifiedTopology: true });
  try {
    await client.connect();
    const db = client.db(DB_NAME);
    console.log(`🗄️ Verbonden met DB '${DB_NAME}'`);

    // nodes: use bulkWrite replaceOne upsert:true so duplicates don't fail
    for (const [label, map] of Object.entries(collections)) {
      const coll = db.collection(label);

      // optional: clear collection first if you want a clean import
      // await coll.deleteMany({});

      const ops = [];
      for (const doc of map.values()) {
        ops.push({
          replaceOne: {
            filter: { _id: doc._id },
            replacement: doc,
            upsert: true
          }
        });
      }

      if (ops.length > 0) {
        const res = await coll.bulkWrite(ops, { ordered: false });
        console.log(`✅ '${label}': upserted ${res.upsertedCount + res.modifiedCount} docs (ops: ${ops.length})`);
      } else {
        console.log(`ℹ️ '${label}': geen documenten om te importeren`);
      }
    }

    // relaties: write ALL relationships
    const relColl = db.collection("relaties");
    
    // OPTION 1: Clear old relations first for clean import (recommended)
    await relColl.deleteMany({});
    console.log("🗑️  Oude relaties verwijderd voor fresh import");

    if (relatiesList.length > 0) {
      // CHANGED: Remove unique index constraint to allow all inserts
      // Instead create a non-unique index for query performance
      try {
        await relColl.createIndex({ neo4jId: 1 }, { background: false });
        await relColl.createIndex({ type: 1 }, { background: false });
        await relColl.createIndex({ start: 1, end: 1 }, { background: false });
      } catch (e) {
        // ignore index-creation errors about existing indexes
      }

      // Insert all relationships
      try {
        const res = await relColl.insertMany(relatiesList, { ordered: false });
        console.log(`✅ 'relaties' inserted: ${res.insertedCount} van ${relatiesList.length}`);
      } catch (err) {
        if (err && err.result && err.result.result) {
          const inserted = err.result.result.nInserted || 0;
          console.log(`⚠️ Bulk insert fouten: ${err.writeErrors ? err.writeErrors.length : "unknown"}, succesvol ingevoegd: ${inserted}`);
        } else {
          console.log("⚠️ Fout tijdens relatie insert:", err.message || err);
        }
      }
    } else {
      console.log("ℹ️ Geen relaties om te importeren.");
    }

    // Verify final counts
    const finalRelatieCount = await relColl.countDocuments({});
    console.log(`📊 Totaal relaties in database: ${finalRelatieCount}`);

    console.log("🚀 Import voltooid.");
  } finally {
    await client.close();
  }
}

run().catch(err => {
  console.error("FATALE FOUT:", err);
  process.exit(1);
});