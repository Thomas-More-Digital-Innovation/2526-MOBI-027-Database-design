# JSON → MongoDB Import Scripts

This repository contains two Node.js scripts for importing a Neo4j-style JSON export into MongoDB.  
Both organize nodes into separate collections (based on their labels), but differ in how relationships are stored:

- **`import.js`** → imports all relationships into a single `relaties` collection.  
- **`import_relations_collections.js`** → imports relationships *split by type*, creating one MongoDB collection per relationship type.

--- 

## 📦 Requirements
- [Node.js](https://nodejs.org/) (version 16 or newer)
- A running [MongoDB](https://www.mongodb.com/) instance (local or remote)
- A JSON file exported from Neo4j (expected structure: objects with `{ n, r, m }` keys)
- A `.env` configuration file (see below)

---

## ⚙️ Setup

1. **Install dependencies**
```
npm install dotenv mongodb
```
2. Create a `.env` file in the same folder as `import.js` with the following variables:
```
MONGO_URI=mongodb://localhost:27017
DB_NAME=my_database
JSON_FILE=./data.json
```
- `MONGO_URI`: Connection string for your MongoDB instance
- `DB_NAME`: Name fo the target MnogoDB database
- `JSON_FILE`: Path to your JSON input file

---

## ▶️ Running the Import

1. **Import all relationships into a single collection**

Use this if you want **all realtionships** stored together in one collection named `relaties`.
```
node import.js
```

The script will:
1. Load and parse the JSON file
2. Deduplicate nodes buy their Neo4j `identity`
3. Create MnogDB collections per node label
4. Upsert nodes into MongoDB
5. Delete and reinsert all relationship data into the realties collection

---

2. **Import relationships split by type**

Use this if you prefer **each realtionship type** to be stored in its own MongoDB collection.
```
node import_relations_collections.js
```

This version preforms the same steps for nodes, but:
- Groups relationships by their `type`
- Deletes existing data in each relationship collection before importing
- Creates indexes(`neo4jId`, `start`, `end`) for faster queries
- Logs import progress for each realtionship type separately

## 🧾 Output Example (Single collection version)
```
🗄️ Verbonden met DB 'neo4j_import_test_env'
✅ 'JointT': upserted 10 docs (ops: 10)
✅ 'Dof': upserted 19 docs (ops: 19)
✅ 'Part': upserted 11 docs (ops: 11)
✅ 'Exo': upserted 38 docs (ops: 38)
✅ 'Aim': upserted 13 docs (ops: 13)
✅ 'ExoProperty': upserted 5 docs (ops: 5)
✅ 'StructureKinematicName': upserted 39 docs (ops: 39)
✅ 'AimType': upserted 2 docs (ops: 2)
✅ 'StructureKinematicNameType': upserted 8 docs (ops: 8)
🗑️  Oude relaties verwijderd voor fresh import
✅ 'relaties' inserted: 477 van 477
📊 Totaal relaties in database: 477
🚀 Import voltooid.
```

---

## 🧾 Output Example (Multiple collection version)
```
🗄️ Verbonden met DB 'neo4j_import_test_env_2'
✅ 'JointT': upserted 10 docs (ops: 10)
✅ 'Dof': upserted 19 docs (ops: 19)
✅ 'Part': upserted 11 docs (ops: 11)
✅ 'Exo': upserted 38 docs (ops: 38)
✅ 'Aim': upserted 13 docs (ops: 13)
✅ 'ExoProperty': upserted 5 docs (ops: 5)
✅ 'StructureKinematicName': upserted 39 docs (ops: 39)
✅ 'AimType': upserted 2 docs (ops: 2)
✅ 'StructureKinematicNameType': upserted 8 docs (ops: 8)

📦 Importeren van relatie collecties...
✅ 'HAS_DOF': inserted 19 van 19
   📊 'HAS_DOF' totaal in database: 19
✅ 'IS_CONNECTED_WITH': inserted 20 van 20
   📊 'IS_CONNECTED_WITH' totaal in database: 20
✅ 'HAS_AS_MAIN_DOF': inserted 17 van 17
   📊 'HAS_AS_MAIN_DOF' totaal in database: 17
✅ 'GIVES_POSTURAL_SUPPORT_IN': inserted 26 van 26
   📊 'GIVES_POSTURAL_SUPPORT_IN' totaal in database: 26
✅ 'LIMITS_IN': inserted 8 van 8
   📊 'LIMITS_IN' totaal in database: 8
✅ 'TRANSFERS_FORCES_FROM': inserted 35 van 35
   📊 'TRANSFERS_FORCES_FROM' totaal in database: 35
✅ 'TRANSFERS_FORCES_TO': inserted 35 van 35
   📊 'TRANSFERS_FORCES_TO' totaal in database: 35
✅ 'HAS_AIM': inserted 186 van 186
   📊 'HAS_AIM' totaal in database: 186
✅ 'HAS_PROPERTY': inserted 45 van 45
   📊 'HAS_PROPERTY' totaal in database: 45
✅ 'ASSISTS_IN': inserted 14 van 14
   📊 'ASSISTS_IN' totaal in database: 14
✅ 'GIVES_RESISTANCE_IN': inserted 14 van 14
   📊 'GIVES_RESISTANCE_IN' totaal in database: 14
✅ 'DOESNT_GO_WITH': inserted 6 van 6
   📊 'DOESNT_GO_WITH' totaal in database: 6
✅ 'HAS_AIMTYPE': inserted 13 van 13
   📊 'HAS_AIMTYPE' totaal in database: 13
✅ 'HAS_SKNTYPE': inserted 39 van 39
   📊 'HAS_SKNTYPE' totaal in database: 39

🚀 Import voltooid.
```

## ⚠️ Notes
- Existing `relaties` collection data is **deleted** before each import.
- Node collections are upserted (updated or inserted if missing).
- If duplicate `neo4jId` values are detected, a warning will be shown.
- The script uses `bulkWrite()` for performance on large datasets.

---

## 🧹 Troubleshooting
- **"FATALE FOUT:...** → Check your `.env` varaibles or MongoDB connection string.
- **JSON parsing errors** → Ensure the `JSON_FILE` path and syntax are correct.
- **Index creation warnings** → These can be safely ignored if indexes already exist.
- **Deprecation warnings** → You can safely remove the `useUnifiedTopology` option in newer MongoDB driver versions.