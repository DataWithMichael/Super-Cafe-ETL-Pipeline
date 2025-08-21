# test_db_insert_functions.py
import pytest
from unittest.mock import MagicMock, patch
import datetime
import etl.db_utils
import etl.db_insert as db_insert
# --------------------------
# Branch tests
# --------------------------
@patch("db_insert.connect_db")
def test_insert_branch_new_branch(mock_connect):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = [1]
    mock_connect.return_value.__enter__.return_value = mock_cursor

    branch_id = db_insert.insert_branch("Test Branch")
    assert branch_id == 1
    mock_cursor.execute.assert_called_once()


@patch("db_insert.connect_db")
def test_get_branch_id_by_name(mock_connect):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = [5]
    mock_connect.return_value.__enter__.return_value = mock_cursor

    branch_id = db_insert.get_branch_id_by_name("Existing Branch")
    assert branch_id == 5
    mock_cursor.execute.assert_called_once()


# --------------------------
# Product tests
# --------------------------
@patch("db_insert.connect_db")
def test_insert_product(mock_connect):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = [10]
    mock_connect.return_value.__enter__.return_value = mock_cursor

    product_id = db_insert.insert_product("Test Product", 99.99, datetime.datetime.now())
    assert product_id == 10
    mock_cursor.execute.assert_called_once()


@patch("db_insert.connect_db")
def test_get_product_id(mock_connect):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = [20]
    mock_connect.return_value.__enter__.return_value = mock_cursor

    product_id = db_insert.get_product_id("Existing Product")
    assert product_id == 20
    mock_cursor.execute.assert_called_once()


# --------------------------
# Orders tests
# --------------------------
@patch("db_insert.connect_db")
def test_insert_order(mock_connect):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = [100]
    mock_connect.return_value.__enter__.return_value = mock_cursor

    order_id = db_insert.insert_order(1, datetime.datetime.now(), 150.0, "Cash")
    assert order_id == 100
    mock_cursor.execute.assert_called_once()


# --------------------------
# Order Items tests
# --------------------------
@patch("db_insert.connect_db")
def test_insert_order_item(mock_connect):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = [200]
    mock_connect.return_value.__enter__.return_value = mock_cursor

    order_item_id = db_insert.insert_order_item(100, 10, 2)
    assert order_item_id == 200
    mock_cursor.execute.assert_called_once()


# --------------------------
# Batch insert tests
# --------------------------
@patch("db_insert.run_batch_insert")
def test_insert_products_batch(mock_batch):
    products = [
        ("Product A", 10.0, datetime.datetime.now()),
        ("Product B", 20.0, datetime.datetime.now())
    ]
    db_insert.insert_products_batch(products)
    mock_batch.assert_called_once()
