import requests
import json
from datetime import datetime

class ExpenseTracker:
    def __init__(self, base_url='http://127.0.0.1:5000'):
        self.base_url = base_url

    def add_expense(self):
        """Collects expense data from the user and sends it to the API."""
        try:
            description = input("Enter expense description: ")
            amount = float(input("Enter expense amount: "))
            date = input("Enter expense date (YYYY-MM-DD): ")
            
            # Validate date format
            datetime.strptime(date, '%Y-%m-%d')
            
            expense_data = {
                'description': description,
                'amount': amount,
                'date': date
            }
            
            response = requests.post(f'{self.base_url}/expenses', json=expense_data)
            if response.status_code == 201:
                print(f"Expense added successfully: {response.json()}")
            else:
                print(f"Error adding expense: {response.text}")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except requests.RequestException as e:
            print(f"Error connecting to server: {e}")

    def view_expenses(self):
        """Retrieves and displays all expenses."""
        try:
            response = requests.get(f'{self.base_url}/expenses')
            if response.status_code == 200:
                expenses = response.json().get('expenses', [])
                if expenses:
                    print("\nExpenses:")
                    print("ID  | Description        | Amount    | Date")
                    print("-" * 45)
                    for expense in expenses:
                        print(f"{expense['id']:<4}| {expense['description']:<17}| ${expense['amount']:<8}| {expense['date']}")
                else:
                    print("No expenses found.")
            else:
                print(f"Error retrieving expenses: {response.text}")
        except requests.RequestException as e:
            print(f"Error connecting to server: {e}")

    def update_expense(self):
        """Updates an existing expense."""
        try:
            expense_id = int(input("Enter expense ID to update: "))
            description = input("Enter new expense description: ")
            amount = float(input("Enter new expense amount: "))
            date = input("Enter new expense date (YYYY-MM-DD): ")
            
            # Validate date format
            datetime.strptime(date, '%Y-%m-%d')
            
            expense_data = {
                'description': description,
                'amount': amount,
                'date': date
            }
            
            response = requests.put(f'{self.base_url}/expenses/{expense_id}', json=expense_data)
            if response.status_code == 200:
                print(f"Expense updated successfully: {response.json()}")
            else:
                print(f"Error updating expense: {response.text}")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except requests.RequestException as e:
            print(f"Error connecting to server: {e}")

    def delete_expense(self):
        """Deletes an expense."""
        try:
            expense_id = int(input("Enter expense ID to delete: "))
            response = requests.delete(f'{self.base_url}/expenses/{expense_id}')
            if response.status_code == 204:
                print(f"Expense {expense_id} deleted successfully.")
            else:
                print(f"Error deleting expense: {response.text}")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except requests.RequestException as e:
            print(f"Error connecting to server: {e}")

def main():
    tracker = ExpenseTracker()
    
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Update Expense")
        print("4. Delete Expense")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            tracker.add_expense()
        elif choice == "2":
            tracker.view_expenses()
        elif choice == "3":
            tracker.update_expense()
        elif choice == "4":
            tracker.delete_expense()
        elif choice == "5":
            print("Exiting Expense Tracker...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()