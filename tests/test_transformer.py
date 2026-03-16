from src.analytics.transformer import (
    compute_avg_rental_duration,
    compute_fleet_utilization,
    compute_record_metrics,
    compute_revenue_by_city,
    compute_vehicle_usage_frequency,
    detect_refueling,
    map_rate_plan,
    transform_all,
)


def make_record():
    return {
        "Reservation_ID": "RES001",
        "Vehicle_ID": "CAR101",
        "Pickup_TS": "2026-03-10 09:00",
        "Return_TS": "2026-03-10 13:30",
        "Odo_Start": 1000,
        "Odo_End": 1250,
        "Fuel_Level": 0.9,
        "Rate": 2000,
        "City": "Bengaluru",
        "Rate_Plan": "eco",
        "Fraud_Risk_Level": "Low",
    }


def test_map_rate_plan():
    record = {"Rate_Plan": "mystery"}

    mapped = map_rate_plan(record)

    assert mapped["Rate_Plan_Clean"] == "Standard"


def test_detect_refueling():
    record = {"Distance_km": 250, "Fuel_Level": 0.9}

    enriched = detect_refueling(record)

    assert enriched["Refuel_Event"] is True


def test_compute_record_metrics():
    metrics = compute_record_metrics(make_record())

    assert metrics["Distance_km"] == 250
    assert metrics["Rental_Hours"] == 4.5
    assert metrics["Revenue"] == 2000
    assert metrics["Cost_per_km"] == 8.0
    assert metrics["Rate_Plan_Clean"] == "Economy"
    assert metrics["Refuel_Event"] is True


def test_compute_fleet_utilization():
    records = [
        {"Vehicle_ID": "CAR101", "Rental_Hours": 4.5},
        {"Vehicle_ID": "CAR101", "Rental_Hours": 1.5},
        {"Vehicle_ID": "CAR102", "Rental_Hours": 2.0},
    ]

    utilization = compute_fleet_utilization(records)

    assert utilization == {"CAR101": 6.0, "CAR102": 2.0}


def test_compute_revenue_by_city():
    records = [
        {"City": "Bengaluru", "Revenue": 2000},
        {"City": "Bengaluru", "Revenue": 500},
        {"City": "Mumbai", "Revenue": 1000},
    ]

    revenue = compute_revenue_by_city(records)

    assert revenue == {"Bengaluru": 2500, "Mumbai": 1000}


def test_compute_avg_rental_duration():
    assert compute_avg_rental_duration([]) == 0


def test_compute_vehicle_usage_frequency():
    records = [
        {"Vehicle_ID": "CAR101"},
        {"Vehicle_ID": "CAR101"},
        {"Vehicle_ID": "CAR102"},
    ]

    freq = compute_vehicle_usage_frequency(records)

    assert freq == {"CAR101": 2, "CAR102": 1}


def test_transform_all():
    first = make_record()
    second = make_record()
    second["Reservation_ID"] = "RES002"
    second["Vehicle_ID"] = "CAR102"
    second["City"] = "Mumbai"
    second["Rate"] = 1500
    second["Odo_End"] = 1150
    second["Fuel_Level"] = 0.4
    second["Rate_Plan"] = "lux"
    second["Fraud_Risk_Level"] = "High"

    enriched, summary = transform_all([first, second])

    assert len(enriched) == 2
    assert enriched[0]["Distance_km"] == 250
    assert enriched[1]["Rate_Plan_Clean"] == "Luxury"
    assert enriched[1]["Refuel_Event"] is False
    assert summary["total_records"] == 2
    assert summary["total_distance_km"] == 400
    assert summary["total_revenue"] == 3500
    assert summary["avg_rental_hours"] == 4.5
    assert summary["avg_distance_km"] == 200.0
    assert summary["avg_cost_per_km"] == 9.0
    assert summary["revenue_by_city"] == {"Bengaluru": 2000, "Mumbai": 1500}
    assert summary["vehicle_usage_frequency"] == {"CAR101": 1, "CAR102": 1}
    assert summary["fraud_risk_distribution"] == {"Low": 1, "High": 1}

