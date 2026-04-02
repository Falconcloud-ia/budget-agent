"""Tests for database operations."""

import sqlite3
import tempfile
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch


class TestDatabaseOperations(TestCase):
    """Test database CRUD operations."""

    def setUp(self):
        """Set up test database."""
        self.test_db = tempfile.NamedTemporaryFile(delete=False)
        self.test_db_path = self.test_db.name
        self.test_db.close()

    def tearDown(self):
        """Clean up test database."""
        Path(self.test_db_path).unlink(missing_ok=True)

    @patch('src.config.DATABASE_PATH')
    def test_create_expense(self, mock_db_path):
        """Test creating an expense."""
        mock_db_path.__str__ = lambda: self.test_db_path

        # Import here to use patched path
        from src.db import init_db, create_expense

        init_db()

        result = create_expense(
            nombre="Rent",
            monto=1200.00,
            frecuencia="mensual",
            descripcion="Monthly rent payment"
        )

        self.assertIsNotNone(result["id"])
        self.assertEqual(result["nombre"], "Rent")
        self.assertEqual(result["monto"], 1200.00)

    @patch('src.config.DATABASE_PATH')
    def test_create_income(self, mock_db_path):
        """Test creating an income."""
        mock_db_path.__str__ = lambda: self.test_db_path

        from src.db import init_db, create_income

        init_db()

        result = create_income(
            descripcion="Salary",
            monto=3000.00,
            frecuencia="mensual",
            fuente="Employment"
        )

        self.assertIsNotNone(result["id"])
        self.assertEqual(result["descripcion"], "Salary")
        self.assertEqual(result["monto"], 3000.00)

    @patch('src.config.DATABASE_PATH')
    def test_get_summary(self, mock_db_path):
        """Test getting budget summary."""
        mock_db_path.__str__ = lambda: self.test_db_path

        from src.db import init_db, create_expense, create_income, get_summary

        init_db()

        create_income(
            descripcion="Salary",
            monto=3000.00,
            frecuencia="mensual"
        )

        create_expense(
            nombre="Rent",
            monto=1200.00,
            frecuencia="mensual"
        )

        summary = get_summary()

        self.assertEqual(summary["monthly_income"], 3000.00)
        self.assertEqual(summary["monthly_expenses"], 1200.00)
        self.assertEqual(summary["balance"], 1800.00)
