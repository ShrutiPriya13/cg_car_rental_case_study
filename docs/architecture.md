# System Architecture

## High-Level Architecture

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   RAW DATA   │───▶│   CLEANING   │───▶│  VALIDATION  │
│  Generation  │    │   Module     │    │   Module     │
│ (Dev 1)      │    │ (Dev 2 & 3)  │    │ (Dev 4)      │
└──────────────┘    └──────────────┘    └──────┬───────┘
                                               │
                                    ┌──────────┴──────────┐
                                    ▼                     ▼
                              ┌───────────┐        ┌───────────┐
                              │  VALID    │        │ REJECTED  │
                              │  Records  │        │ Records   │
                              └─────┬─────┘        └───────────┘
                                    │                     │
                                    ▼                     ▼
                              ┌───────────┐        rejected_
                              │ DEDUP &   │        reservations.csv
                              │ FRAUD     │
                              │ (Dev 5)   │
                              └─────┬─────┘
                                    │
                                    ▼
                              ┌───────────┐
                              │ TRANSFORM │
                              │ & KPIs    │
                              │ (Dev 6 & 7)│
                              └─────┬─────┘
                                    │
                          ┌─────────┼─────────┐
                          ▼         ▼         ▼
                    cleaned_   metrics_    Terminal
                    reserv..   report.csv  Summary
```

---

# Module Responsibilities

## Developer 1: Ingestion (`src/ingestion/`)

### `dataset_generator.py`
Generates **~2000 realistic car rental records** with intentional data quality issues to simulate real-world datasets.

Data issues generated include:

- Vehicle IDs with extra spaces and mixed casing
- Mixed timestamp formats
- Odometer values containing commas and units (`45,000 km`)
- Fuel levels in both **percentage and fractional formats**
- Rental rates with **currency symbols and text**
- City abbreviations (`blr`, `hyd`, `mum`)
- Payment method case inconsistencies (`upi`, `Card`)
- Duplicate reservation IDs
- Negative mileage scenarios

Uses a **fixed random seed** to ensure reproducible dataset generation.

### `reader.py`

Handles CSV file input/output operations using Python's built-in `csv` module.

Responsibilities:

- Read raw dataset using `csv.DictReader`
- Write cleaned and processed datasets
- Handle directory creation for output folders
- Manage encoding and file safety

---

# Developer 2 & 3: Data Cleaning (`src/cleaning/`)

### `cleaner.py`

Performs **field-level data cleaning and normalization**.

Key cleaning functions include:

#### `clean_vehicle_id()`
- Removes extra whitespace
- Converts IDs to uppercase
- Ensures consistent vehicle ID formatting

#### `clean_timestamp()`
- Handles multiple timestamp formats
- Fixes invalid time values (e.g., `10:75`)
- Converts to standardized format:

```
YYYY-MM-DD HH:MM
```

#### `clean_odometer()`
- Removes units like `"km"`
- Removes commas from values
- Converts values to integers

Example:

```
"45,000 km" → 45000
```

#### `clean_fuel_level()`
- Converts percentages to fractions

Example:

```
50% → 0.50
```

#### `clean_rate()`
- Removes `₹`, `/day`, commas
- Converts to numeric value

Example:

```
₹1,500/day → 1500
```

#### `clean_city()`
Maps city abbreviations to standardized names using a lookup dictionary.

Example:

```
blr → Bengaluru
hyd → Hyderabad
mum → Mumbai
```

#### `clean_payment()`
- Converts to uppercase
- Ensures consistency across payment types

---

# Developer 4: Validation (`src/validation/`)

### `validator.py`

Implements **rule-based validation checks** to ensure business logic consistency.

Validation rules include:

- Pickup timestamp must be **before** return timestamp
- `Odo_End ≥ Odo_Start`
- Fuel level must be between **0 and 1**
- Payment method must be one of:

```
UPI, CARD, CASH, WALLET
```

- Required fields must not be null or missing

Invalid records are **flagged with rejection reasons** and separated into a rejected dataset.

---

# Developer 5: Deduplication & Fraud Detection (`src/processing/`)

### `deduplicator.py`

Handles **duplicate removal and fraud pattern detection**.

Key features include:

### Deduplication
- Removes duplicate records using **Reservation_ID**
- Keeps the **first valid occurrence**

### Fraud Detection
Detects suspicious patterns such as:

- **Overlapping bookings** for the same vehicle
- **Odometer rollback** between bookings
- **Unrealistic travel distance within short rentals**

### Fraud Risk Score

Risk scores are calculated between **0 and 8** based on:

| Condition | Score |
|--------|------|
| Short rental with large distance | +3 |
| Overlapping booking | +2 |
| Odometer rollback | +3 |

Risk categories:

- **None**
- **Low**
- **Medium**
- **High**

---

# Developer 6 & 7: Data Transformation & Analytics (`src/analytics/`)

### `transformer.py`

Computes **key business KPIs and analytics metrics**.

Per-record metrics:

| Metric | Description |
|------|-------------|
| Distance_km | `Odo_End − Odo_Start` |
| Rental_Hours | Total rental duration |
| Revenue | Rental rate × duration |
| Cost_per_km | Revenue ÷ distance |

Aggregate analytics:

- Fleet utilization by vehicle
- Revenue by city
- Average rental duration
- Vehicle usage frequency
- Fraud risk distribution

These transformations produce the **final analytics-ready dataset**.

---

# Developer 6: SQL Analytics (`sql/`)

### `schema.sql`

Defines the relational database schema including:

- `CUSTOMERS`
- `VEHICLES`
- `RESERVATIONS`
- `PAYMENTS`
- `MAINTENANCE`
- `LOCATIONS`

### `inserts.sql`

Contains **sample data entries** for testing the schema.

### `solutions.sql`

Includes **advanced analytical SQL queries** using:

- `JOIN`
- `GROUP BY`
- Window functions (`RANK`, `LAG`, `SUM OVER`)
- `CTE`
- `CASE` expressions

Example insights generated:

- Top performing cities
- Vehicle utilization ranking
- Revenue trends
- Fraud pattern identification

---

# Data Flow

1️⃣ **Raw Dataset Generation**

```
2080 messy records
```

⬇

2️⃣ **Cleaning Stage**

```
Standardized 2080 cleaned records
```

⬇

3️⃣ **Validation Stage**

```
Valid Records + Rejected Records
```

⬇

4️⃣ **Deduplication**

```
~1920 unique reservations
```

⬇

5️⃣ **Transformation & Analytics**

```
Enriched dataset with KPIs
```

⬇

6️⃣ **Output Files**

- `cleaned_reservations.csv`
- `rejected_reservations.csv`
- `metrics_report.csv`

---

# Design Decisions

### No External Dependencies

The system uses only **Python Standard Library** modules:

```
csv
datetime
re
os
sys
random
collections
```

This ensures **maximum portability and simplicity**.

---

### Dictionary-Based Data Processing

Records are processed using **Python dictionaries**, avoiding the need for external libraries such as:

- pandas
- numpy

This keeps the pipeline **lightweight and easy to understand**.

---

### Modular Architecture

Each stage of the pipeline is implemented as an **independent module**, enabling:

- Easier testing
- Code maintainability
- Independent development by multiple developers

---

### Deterministic Dataset Generation

A **fixed random seed** ensures:

- Reproducible datasets
- Consistent results across runs
- Reliable debugging and evaluation