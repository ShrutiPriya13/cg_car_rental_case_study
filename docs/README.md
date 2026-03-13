# 🚗 Car Rental Data Engineering Pipeline

## 📌 Overview
This project implements a **complete end-to-end data engineering pipeline** for a **multi-city car rental company**.  
The system simulates real-world messy operational data and transforms it into **clean, validated, analytics-ready datasets**.

The pipeline performs the following major operations:

1. **Synthetic Data Generation** with real-world data issues
2. **Data Ingestion** from raw CSV files
3. **Data Cleaning & Normalization**
4. **Business Rule Validation**
5. **Deduplication & Fraud Detection**
6. **Advanced Data Transformations**
7. **KPI & Analytics Generation**
8. **SQL-based Analytical Queries**

The system processes **~2000+ rental reservations** and converts messy operational data into **reliable business intelligence metrics**.

---

# 🏗 System Architecture

```
car_rental_project/
│
├── main.py
│
├── data/
│   ├── raw/
│   │   └── car_rental_raw.csv
│   │
│   └── output/
│       ├── cleaned_reservations.csv
│       ├── rejected_reservations.csv
│       ├── metrics_report.csv
│       └── analytics_outputs/
│
├── src/
│
│   ├── ingestion/
│   │   ├── dataset_generator.py
│   │   └── reader.py
│
│   ├── cleaning/
│   │   └── cleaner.py
│
│   ├── validation/
│   │   └── validator.py
│
│   ├── processing/
│   │   └── deduplicator.py
│
│   ├── analytics/
│   │   ├── transformer.py
│   │   └── analytics_engine.py
│
│   └── pipeline/
│       └── pipeline_runner.py
│
├── sql/
│   ├── schema.sql
│   ├── inserts.sql
│   └── solutions.sql
│
└── docs/
    ├── README.md
    ├── architecture.md
    └── evaluation_questions.md
```

---

# ⚙️ How to Run the Project

```bash
cd car_rental_project
python main.py
```

The pipeline will automatically:

1. Generate the dataset  
2. Clean and validate data  
3. Remove duplicates  
4. Compute analytics metrics  
5. Save output files  

---

# 📊 Pipeline Stages

| Stage | Description |
|------|-------------|
| **1. Data Generation** | Generates ~2000 records with intentional data inconsistencies |
| **2. Data Ingestion** | Loads CSV data into memory |
| **3. Data Cleaning** | Standardizes formats across all columns |
| **4. Validation** | Applies business rules to detect invalid records |
| **5. Deduplication** | Removes duplicate reservations |
| **6. Fraud Detection** | Detects suspicious reservations and assigns risk scores |
| **7. Data Transformation** | Computes derived metrics like distance, duration, revenue |
| **8. Analytics Engine** | Generates advanced business insights |
| **9. Output Generation** | Writes cleaned, rejected, and metrics datasets |

---

# 🧹 Data Cleaning Capabilities

The pipeline handles multiple real-world data quality issues.

### Vehicle Data
- Extra spaces  
- Case inconsistencies  
- Incorrect ID formats  

### Timestamps
- Multiple datetime formats  
- Invalid timestamps (e.g., `10:75`)  
- Pickup/return order corrections  

### Odometer
- Text units (`45,000 km`)  
- Commas  
- Missing values  

### Fuel Levels
- Percent vs fraction (`50%` vs `0.5`)  
- Out-of-range values  

### Rate Fields
- Currency symbols (`₹1500/day`)  
- Mixed formats  

### City Names
- Abbreviations (`blr`, `hyd`)  
- Case normalization  

### Payment Methods
- Case inconsistencies  
- Invalid payment types  

---

# 🔍 Validation Rules

Business validation checks include:

- Pickup timestamp must be before return timestamp  
- Odometer end must be greater than start  
- Fuel levels must be between **0 and 100**  
- Payment method must be valid  
- Rate values must be positive  
- Reservation IDs must be unique  

Invalid records are saved in:

```
data/output/rejected_reservations.csv
```

---

# 🕵️ Fraud Detection

The system calculates **fraud risk scores** based on:

- Suspicious mileage patterns  
- Duplicate reservations  
- Unrealistic trip durations  
- Payment inconsistencies  
- Data anomalies  

Records are categorized as:

- **Low Risk**
- **Medium Risk**
- **High Risk**

---

# 📈 Analytics & KPI Metrics

The transformation layer computes business metrics such as:

| Metric | Description |
|------|-------------|
| Trip Distance | Odo_End − Odo_Start |
| Rental Duration | Total hours of rental |
| Revenue | Rental rate × duration |
| Cost per KM | Revenue ÷ distance |
| Fleet Utilization | Vehicle usage efficiency |
| City Performance | Revenue by location |
| Payment Distribution | Usage of payment methods |
| Vehicle Class Mix | Vehicle usage distribution |

These metrics are exported to:

```
data/output/metrics_report.csv
```

---


# 👨‍💻 Team Structure

This project was developed collaboratively by **7 developers**, each responsible for a specific module.

| Developer | Responsibility |
|---------|----------------|
| Developer 1 | Dataset generation & ingestion |
| Developer 2 & 3 | Data cleaning module |
| Developer 4 | Validation rules implementation |
| Developer 5 | Deduplication logic |
| Developer 6 & 7 | Data transformation & analytics|

---

# 📂 Output Files

| File | Description |
|-----|-------------|
| `cleaned_reservations.csv` | Valid, cleaned reservations |
| `rejected_reservations.csv` | Invalid records with rejection reason |
| `metrics_report.csv` | Computed analytics metrics |
| `analytics_outputs/` | Additional analytics outputs |

---

# 🎯 Project Objectives

This project demonstrates:

- Real-world **data engineering pipeline design**
- **Data cleaning and normalization**
- **Business rule validation**
- **Fraud detection techniques**
- **Analytics-ready data transformation**
- **SQL-based analytical querying**
- **Modular scalable architecture**

---

# 📌 Key Learning Outcomes

- Building **production-style ETL pipelines**
- Handling **messy real-world datasets**
- Implementing **data validation frameworks**
- Creating **analytics-ready datasets**
- Designing **scalable modular architectures**