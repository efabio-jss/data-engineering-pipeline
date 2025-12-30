# ⚡ E-REDES Open Data → Data Engineering

## 📌 Summary
This project builds a **fully automated data platform** that ingests official **E-REDES Open Data (Portugal Power Distribution Operator)** via API into **Microsoft SQL Server**, refreshes the data automatically, and exposes it for analytics (Power BI, dashboards, data science, reporting, and strategic decision making).

It is designed as a **real-world data engineering project**, demonstrating:
- Reliable API ingestion
- Structured raw data warehousing
- Automation & scheduling
- Enterprise-ready database integration
- Business relevance for **renewable energy & power grid development**

---

## 🎯 Business Value
This platform is especially relevant for:
- Renewable energy developers  
- Utility analytics teams  
- Energy consultants  
- Data & BI teams  
- Infrastructure planning & strategy  

It enables organizations to:

✔ Understand **energy consumption patterns** across municipalities  
✔ Monitor **network capacity & substation load**  
✔ Evaluate viability of **renewable energy project connections**  
✔ Track growth of **self-consumption and energy communities**  
✔ Analyze **grid reliability & planned outages**  
✔ Build **Power BI dashboards** directly on live SQL data  

In short, it transforms **raw open energy data** into **strategic decision intelligence**.

---

## 🧠 Datasets Integrated
All data comes from the official **E-REDES Open Data Platform**.

The pipeline ingests and refreshes:

| Dataset | Purpose |
|--------|---------|
| Self-Consumption Units (UPAC) | Renewable installed capacity & adoption |
| National Consumption | Electricity usage across tension levels |
| Consumption by Municipality | Detailed regional demand & trends |
| Substation Load & Capacity | Critical for project grid connection |
| Low Voltage Supports | Infrastructure mapping |
| Energy Communities | Distributed renewable initiatives |
| Planned Outages | Reliability & risk assessment |

All datasets are pulled through the official JSON API and stored as **raw tables** in SQL Server.

---

## 🏗️ Architecture
E-REDES API  →  Python Pipeline  →  MS SQL Server  →  Power BI / Analytics

- **Python** handles API calls, pagination, and JSON normalization  
- Data stored in **raw SQL tables** (one per dataset)  
- Pipeline runs automatically on a schedule  
- Any BI or analytics tool can connect — example: Power BI  

---

## 🛠️ Tech Stack

| Component | Technology |
|----------|------------|
| Programming | Python 3.x |
| Database | MS SQL Server |
| Driver | ODBC 17 |
| ORM Layer | SQLAlchemy |
| Automation | Windows Task Scheduler |
| Visualization (optional) | Power BI |

---

## 🚀 Features
- Full refresh ingestion  
- Handles pagination automatically  
- Flattens API JSON structures  
- Creates SQL tables automatically  
- Fast insert with batching  
- Secured connection via environment variables  
- Production-style logging output  
- Works offline after setup  
- Zero-cost stack  

---

## 📥 Setup Guide

### 1️⃣ Requirements
- MS SQL Server  
- Python 3.x  
- Internet connection  
- ODBC SQL Server Driver  

---

### 2️⃣ Create Database & User
Run in SQL Server Management Studio:

```sql
CREATE DATABASE EnergiaEredes;
GO

CREATE LOGIN EredesUser WITH PASSWORD = 'PasswordStrong_123!';
GO

USE EnergiaEredes;
GO
CREATE USER EredesUser FOR LOGIN EredesUser;
GO

ALTER ROLE db_owner ADD MEMBER EredesUser;
GO
3️⃣ Environment Variables


Create a file named:

.env
Contents:

SQL_SERVER=localhost\SQLEXPRESS
SQL_DB=EnergiaEredes
SQL_USER=EredesUser
SQL_PASSWORD=PasswordStrong_123!
SQL_DRIVER=ODBC Driver 17 for SQL Server
4️⃣ Install Dependencies
pip install pandas requests sqlalchemy pyodbc python-dotenv
5️⃣ Run Pipeline
python eredes_ingest.py
⏰ Automation (Daily Refresh)


This platform is designed to run automatically.



Windows Task Scheduler


1️⃣ Open Task Scheduler

2️⃣ Click Create Basic Task

3️⃣ Name: E-REDES Data Refresh

4️⃣ Trigger: Daily → choose preferred time (example: 03:00)

5️⃣ Action:

Program: python

Arguments: C:\projects\eredes\eredes_ingest.py

Start in: C:\projects\eredes

6️⃣ Save



The database now refreshes automatically 🚀

📊 Power BI Integration


1️⃣ Open Power BI Desktop

2️⃣ Click:

Get Data → SQL Server
3️⃣ Enter:

Server: localhost\SQLEXPRESS
Database: EnergiaEredes
4️⃣ Select:

Import (performance)

DirectQuery (live data)



5️⃣ Authenticate using database credentials

6️⃣ Select tables such as:

raw_eredes_national_consumption
raw_eredes_municipal_consumption
raw_eredes_substation_load
7️⃣ Load → Build dashboards 🎯

✅ Current Status
✔ Fully functional ingestion pipeline

✔ Stable SQL data storage

✔ Ready for analytics

✔ Production-ready automation



📈 Future Roadmap
Dimensional modeling (FACT + DIM)

Incremental ingestion

Geospatial analytics

Cloud deployment (Azure / AWS)

👤 Author


Developed as a real-world data engineering project, showcasing modern energy analytics capabilities and strong applied data engineering design.

📜 License


Open for learning and development use. Attribution appreciated.

---
