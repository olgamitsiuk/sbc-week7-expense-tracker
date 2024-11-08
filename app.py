from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load expenses data from file
with open('expenses_data.json', 'r') as file:
    expenses = json.load(file)

@app.route('/expenses', methods=['GET'])
def get_expenses():
    """Retrieve the list of expenses."""
    return jsonify({'expenses': expenses})

@app.route('/expenses', methods=['POST'])
def add_expense():
    """Add a new expense with description, amount, and date fields."""
    data = request.json  # Get JSON payload

    # Validate required fields
    required_fields = ['description', 'amount', 'date']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing one or more required fields: description, amount, date'}), 400

    # Create new expense entry
    expense = {
        'id': len(expenses) + 1,
        'description': data['description'],
        'amount': float(data['amount']),  # Convert amount to float
        'date': data['date']
    }

    # Append and save the new expense
    expenses.append(expense)
    with open('expenses_data.json', 'w') as f:
        json.dump(expenses, f)

    return jsonify(expense), 201

@app.route('/expenses/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    """Update an existing expense."""
    expense = next((exp for exp in expenses if exp['id'] == expense_id), None)
    if expense:
        expense.update(request.json)
        
        # Save updated expenses to file
        with open('expenses_data.json', 'w') as f:
            json.dump(expenses, f)
        
        return jsonify(expense)
    return jsonify({'error': 'Expense not found'}), 404

@app.route('/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    """Delete an expense."""
    global expenses
    expenses = [exp for exp in expenses if exp['id'] != expense_id]
    
    # Save updated expenses to file
    with open('expenses_data.json', 'w') as f:
        json.dump(expenses, f)
    
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)