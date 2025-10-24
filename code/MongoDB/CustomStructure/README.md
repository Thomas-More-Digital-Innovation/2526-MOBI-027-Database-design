# Excel to MongoDB Import Script
This Node.js scrip timports data from an Excel file (`.xlsx`) and inserts each sheet inside that file into a MongoDB database. Each sheet becomes a separate MongoDB collection with the same name.

## ✅ Prerequisites
Make sure you have the following installed on your system:
- **Node.js** (v14+ recommended)
- **npm** (comes with Node.js)
- **MongoDB** instance (local or MongoDB Atlas cloud)

## 📦 Installation
1. Clone or download this project.
2. Open a terminal in the project folder.
3. install dependencies by running: `npm install dotenv xlsx mongodb`

## ⚙️ Configuration
Create a `.env` file in the project root with the following content:
```
MONGO_URI=mongodb+srv://<username>:<password>@<cluster-url>/  # or mongodb://localhost:27017
DB_NAME=your_database_name
```

Replace the values with your actual MongoDB connection string and disired database name.

## 📁 Excel File
Place your Excel file in the same folder as the script.
Make sure it is named:
```
Exo_GIVES_SUPPORT_Dof.xlsx
```

(Or change the filename in the script if needed.)

## ▶️ Run the Script
To execute the script, run:
```
node import.js
```

## ✅ What It Does
- Connects to MongoDB
- Reads every sheet from the Excel file.
- Converts each sheet to JSON.
- Inserts the records into MongoDB collections.
- Collection name = Sheet name from excel

## 🛑 Errors & Troubleshooting
If you see a connection error:
- Check your `MONGO_URI` in `.env`
- Allow your IP in MongoDB Atlas if using cloud
- Make sure MongoDB is running locally is using localhost
