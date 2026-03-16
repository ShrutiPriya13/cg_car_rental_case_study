from src.cleaning.cleaner import (
    clean_all,
    clean_city,
    clean_fuel_level,
    clean_odometer,
    clean_payment,
    clean_rate,
    clean_record,
    clean_timestamp,
    clean_vehicle_id,
    detect_damage,
    mask_driver_license,
    normalize_speed,
    redact_pii,
    smooth_gps,
)


def make_raw_record():
    return {
        "Reservation_ID": "RES001",
        "Vehicle_ID": " ab 123 ",
        "Pickup_TS": "2026/03/10 09:00",
        "Return_TS": "10-03-2026 12:00",
        "Odo_Start": "1,000 km",
        "Odo_End": "1,125 km",
        "Fuel_Level": "75%",
        "Rate": "Rs. 2,500/day",
        "City": "blr",
        "Payment": "credit card",
        "Driver_License": "KA01AB1234",
        "GPS_Lat": "12.9715987",
        "GPS_Lon": "77.594566",
        "Max_Speed_kmh": "88 km/h",
        "Notes": "Customer called from 9876543210 and reported scratch damage",
        "Customer_Feedback": "Mail me at user@example.com",
    }


def test_clean_vehicle_id():
    assert clean_vehicle_id(" ab 123 ") == "AB-123"


def test_clean_timestamp():
    assert clean_timestamp("2026-03-10T09:00") == "2026-03-10 09:00"
    assert clean_timestamp("2026-03-10 10:75") == "2026-03-10 11:15"


def test_clean_odometer():
    assert clean_odometer("45,000 km") == 45000


def test_clean_fuel_level():
    assert clean_fuel_level("75%") == 0.75


def test_clean_rate():
    assert clean_rate("Rs. 2,500/day") == 2500


def test_clean_city():
    assert clean_city("blr") == "Bengaluru"


def test_clean_payment():
    assert clean_payment("credit card") == "CARD"


def test_mask_driver_license():
    assert mask_driver_license("KA01AB1234") == "KA01XXXXXXX"


def test_smooth_gps():
    assert smooth_gps("12.9715987") == 12.9716


def test_normalize_speed():
    assert normalize_speed("88 km/h") == 88


def test_redact_pii():
    redacted = redact_pii("Call 9876543210 or email user@example.com")

    assert "[PHONE]" in redacted
    assert "[EMAIL]" in redacted


def test_detect_damage():
    assert detect_damage("Minor scratch on rear door") is True
    assert detect_damage("Vehicle returned clean") is False


def test_clean_record():
    cleaned = clean_record(make_raw_record())

    assert cleaned["Vehicle_ID"] == "AB-123"
    assert cleaned["Pickup_TS"] == "2026-03-10 09:00"
    assert cleaned["Return_TS"] == "2026-03-10 12:00"
    assert cleaned["Odo_Start"] == 1000
    assert cleaned["Odo_End"] == 1125
    assert cleaned["Fuel_Level"] == 0.75
    assert cleaned["Rate"] == 2500
    assert cleaned["City"] == "Bengaluru"
    assert cleaned["Payment"] == "CARD"
    assert cleaned["Driver_License"] == "KA01XXXXXXX"
    assert cleaned["GPS_Lat"] == 12.9716
    assert cleaned["GPS_Lon"] == 77.5946
    assert cleaned["Max_Speed_kmh"] == 88
    assert "[PHONE]" in cleaned["Notes"]
    assert "[EMAIL]" in cleaned["Customer_Feedback"]
    assert cleaned["Damage_Reported"] is True


def test_clean_all():
    cleaned_records = clean_all([make_raw_record(), make_raw_record()])

    assert len(cleaned_records) == 2
    assert all(record["City"] == "Bengaluru" for record in cleaned_records)

