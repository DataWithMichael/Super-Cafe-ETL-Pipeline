from file_handling import extract_raw_data

def test_extract_raw_data():
    data = extract_raw_data()
    assert isinstance(data, list), "Extracted data should be a list"
    assert len(data) > 0, "No rows extracted from raw_data folder"

    # Raw CSV should have at least these columns
    expected_cols = ["date", "branch_name", "customer", "orders", "total_price", "payment_method", "card_number"]
    for col in expected_cols:
        assert col in data[0], f"CSV missing expected column '{col}'"
