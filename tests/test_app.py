import unittest
from unittest.mock import patch, mock_open
import json
from app import app

class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        
        # Sample expense for testing
        self.sample_expense = {
            "description": "Lunch",
            "amount": 10.5,
            "date": "2023-11-01"
        }
        
        # Initial test data
        self.initial_expenses = [{
            "id": 1,
            "description": "Dinner",
            "amount": 15.0,
            "date": "2023-11-02"
        }]
        
        # Start file patch
        self.patcher = patch('app.expenses', self.initial_expenses.copy())
        self.mock_expenses = self.patcher.start()
        
        # Mock the file operations
        self.file_patcher = patch('builtins.open', mock_open(read_data=json.dumps(self.initial_expenses)))
        self.mock_file = self.file_patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.file_patcher.stop()
        self.app_context.pop()

    def test_get_expenses(self):
        response = self.app.get('/expenses')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['expenses'], self.initial_expenses)

    def test_add_expense(self):
        # First get the current expenses to determine next ID
        get_response = self.app.get('/expenses')
        current_expenses = get_response.get_json()['expenses']
        expected_next_id = max(exp['id'] for exp in current_expenses) + 1 if current_expenses else 1
        
        # Add new expense
        response = self.app.post('/expenses', json=self.sample_expense)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        
        # Check that all the fields from sample_expense are in the response
        for key, value in self.sample_expense.items():
            self.assertEqual(data[key], value)
        
        # Check that the ID is correct
        self.assertIn('id', data)
        self.assertEqual(data['id'], expected_next_id)
        
        # Verify expense was actually added
        get_response = self.app.get('/expenses')
        updated_expenses = get_response.get_json()['expenses']
        self.assertEqual(len(updated_expenses), len(current_expenses) + 1)
        self.assertTrue(any(exp['id'] == expected_next_id for exp in updated_expenses))

    def test_update_expense(self):
        updated_expense = {
            "description": "Updated Dinner",
            "amount": 20.0,
            "date": "2023-11-03"
        }
        
        response = self.app.put('/expenses/1', json=updated_expense)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        # Check that all fields were updated
        expected_response = {
            'id': 1,
            **updated_expense
        }
        self.assertEqual(data, expected_response)

    def test_update_nonexistent_expense(self):
        updated_expense = {
            "description": "Updated Dinner",
            "amount": 20.0,
            "date": "2023-11-03"
        }
        
        response = self.app.put('/expenses/999', json=updated_expense)
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data['error'], 'Expense not found')

    def test_delete_expense(self):
        # Add a test expense first
        self.app.post('/expenses', json=self.sample_expense)
        
        # Get current expenses to find the ID of the new expense
        get_response = self.app.get('/expenses')
        current_expenses = get_response.get_json()['expenses']
        test_expense_id = max(exp['id'] for exp in current_expenses)
        
        # Delete the expense
        response = self.app.delete(f'/expenses/{test_expense_id}')
        self.assertEqual(response.status_code, 204)
        
        # Verify the expense was deleted
        get_response = self.app.get('/expenses')
        updated_expenses = get_response.get_json()['expenses']
        self.assertFalse(any(exp['id'] == test_expense_id for exp in updated_expenses))

    def test_delete_nonexistent_expense(self):
        response = self.app.delete('/expenses/999')
        self.assertEqual(response.status_code, 204)

    def test_add_expense_missing_fields(self):
        incomplete_expense = {
            "description": "Lunch"  # Missing amount and date
        }
        response = self.app.post('/expenses', json=incomplete_expense)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)
        self.assertIn('Missing one or more required fields', data['error'])

if __name__ == '__main__':
    unittest.main()