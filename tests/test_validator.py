from src.validation.validator import (
    validate_all,
    validate_driver_license,
    validate_fuel_level,
    validate_gst,
    validate_odometer,
    validate_payment,
    validate_promo_code,
    validate_record,
    validate_required_fields,
    validate_timestamps,
)


def make_valid_record():
    return {
        "Reservation_ID": "RES001",
        "Vehicle_ID": "CAR101",
        "Pickup_TS": "2026-03-10 09:00",
        "Return_TS": "2026-03-10 12:00",
        "Odo_Start": 1000,
        "Odo_End": 1100,
        "Fuel_Level": 0.5,
        "Rate": 2000,
        "City": "Bangalore",
        "Payment": "CARD",
        "Driver_License": "KA01AB1234",
        "Promo_Code": "SAVE10",
        "GST_Amount": 100.0,
    }


def test_validate_required_fields():
    is_valid, reason = validate_required_fields(make_valid_record())

    assert is_valid is True
    assert reason == ""


def test_validate_timestamps():
    record = make_valid_record()
    record["Return_TS"] = "2026-03-10 08:00"

    is_valid, reason = validate_timestamps(record)

    assert is_valid is False
    assert "not after" in reason


def test_validate_odometer():
    record = make_valid_record()
    record["Odo_End"] = 900

    is_valid, reason = validate_odometer(record)

    assert is_valid is False
    assert "Odo_End" in reason


def test_validate_fuel_level():
    record = make_valid_record()
    record["Fuel_Level"] = 1.5

    is_valid, reason = validate_fuel_level(record)

    assert is_valid is False
    assert "out of range" in reason


def test_validate_payment():
    record = make_valid_record()
    record["Payment"] = "upi"

    is_valid, reason = validate_payment(record)

    assert is_valid is True
    assert reason == ""


def test_validate_driver_license_empty():
    record = make_valid_record()
    record["Driver_License"] = ""

    is_valid, reason = validate_driver_license(record)

    assert is_valid is True
    assert reason == ""


def test_validate_driver_license_invalid():
    record = make_valid_record()
    record["Driver_License"] = "123-invalid"

    is_valid, reason = validate_driver_license(record)

    assert is_valid is False
    assert "Invalid driver license format" in reason


def test_validate_promo_code():
    record = make_valid_record()
    record["Promo_Code"] = "expired20"

    is_valid, reason = validate_promo_code(record)

    assert is_valid is False
    assert "Expired promo code" in reason


def test_validate_gst():
    record = make_valid_record()
    record["GST_Amount"] = 200.0

    is_valid, reason = validate_gst(record)

    assert is_valid is False
    assert "Incorrect GST amount" in reason


def test_validate_record():
    record = make_valid_record()
    record["Return_TS"] = "2026-03-10 08:00"
    record["Odo_End"] = 900
    record["Fuel_Level"] = 2

    is_valid, reasons = validate_record(record)

    assert is_valid is False
    assert len(reasons) == 3
    assert any("not after" in reason for reason in reasons)
    assert any("Odo_End" in reason for reason in reasons)
    assert any("out of range" in reason for reason in reasons)


def test_validate_all():
    valid_record = make_valid_record()
    rejected_record = make_valid_record()
    rejected_record["Reservation_ID"] = "RES002"
    rejected_record["Payment"] = "CHEQUE"

    valid, rejected = validate_all([valid_record, rejected_record])

    assert len(valid) == 1
    assert len(rejected) == 1
    assert rejected[0]["Reservation_ID"] == "RES002"
    assert "Invalid payment method" in rejected[0]["Rejection_Reasons"]

