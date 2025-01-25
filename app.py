from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import heapq

app = Flask(__name__)

# In-memory storage for expenses (could be a database in a real-world scenario)
expenses = []  # List to store expenses
undo_stack = []  # Stack for undo functionality
redo_stack = []  # Stack for redo functionality

# Min-heap for sorting expenses (priority queue)
expense_queue = []  # This can be used to store expenses sorted by amount

# Hash Table (Dictionary) to categorize expenses
category_totals = {}  # This will store totals by category for reports

# Linked List Node Class for Expense History
class ExpenseNode:
    def __init__(self, amount, category, description, date):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date
        self.next = None

class ExpenseLinkedList:
    def __init__(self):
        self.head = None

    def add_expense(self, amount, category, description, date):
        new_node = ExpenseNode(amount, category, description, date)
        new_node.next = self.head
        self.head = new_node

    def get_all_expenses(self):
        expenses = []
        current = self.head
        while current:
            expenses.append({
                'amount': current.amount,
                'category': current.category,
                'description': current.description,
                'date': current.date
            })
            current = current.next
        return expenses

expense_history = ExpenseLinkedList()  # Linked list for tracking expense history

# API to add an expense
@app.route('/add_expense', methods=['POST'])
def add_expense():
    data = request.get_json()
    amount = data['amount']
    category = data['category']
    description = data['description']
    date = data['date']
    
    expense = {
        'amount': amount,
        'category': category,
        'description': description,
        'date': date
    }

    # Push to undo stack before modifying
    undo_stack.append(expense)
    
    # Add expense to the list and to the linked list
    expenses.append(expense)
    expense_history.add_expense(amount, category, description, date)
    
    # Store category totals in hash table
    if category not in category_totals:
        category_totals[category] = 0
    category_totals[category] += float(amount)
    
    # Add to priority queue (min-heap) for sorting by amount
    heapq.heappush(expense_queue, (amount, category, description, date))
    
    # Clear redo stack after new action
    redo_stack.clear()

    return jsonify({'message': 'Expense added successfully'}), 201


# API to get all expenses
@app.route('/get_expenses', methods=['GET'])
def get_expenses():
    return jsonify(expenses)


# API to delete an expense
@app.route('/delete_expense/<int:index>', methods=['DELETE'])
def delete_expense(index):
    if index < len(expenses):
        expense = expenses.pop(index)  # Remove from list
        undo_stack.append({'action': 'delete', 'expense': expense})  # Add to undo stack
        redo_stack.clear()  # Clear redo stack after a delete action
        
        # Update category totals in hash table
        category_totals[expense['category']] -= float(expense['amount'])
        if category_totals[expense['category']] == 0:
            del category_totals[expense['category']]
        
        # Remove from linked list (expense history)
        current = expense_history.head
        prev = None
        while current:
            if current.amount == expense['amount'] and current.category == expense['category']:
                if prev:
                    prev.next = current.next
                else:
                    expense_history.head = current.next
                break
            prev = current
            current = current.next
        
        return jsonify({'message': 'Expense deleted successfully'}), 200
    else:
        return jsonify({'message': 'Expense not found'}), 404


# API to undo last action
@app.route('/undo', methods=['POST'])
def undo():
    if undo_stack:
        last_expense = undo_stack.pop()
        if last_expense.get('action') == 'add':
            expenses.remove(last_expense)
        elif last_expense.get('action') == 'delete':
            expenses.append(last_expense['expense'])
        
        # Add to redo stack
        redo_stack.append(last_expense)
        
        return jsonify({'message': 'Undo successful'}), 200
    else:
        return jsonify({'message': 'Nothing to undo'}), 400


# API to redo last undone action
@app.route('/redo', methods=['POST'])
def redo():
    if redo_stack:
        last_expense = redo_stack.pop()
        if last_expense.get('action') == 'add':
            expenses.append(last_expense)
        elif last_expense.get('action') == 'delete':
            expenses.remove(last_expense['expense'])
        
        # Add to undo stack
        undo_stack.append(last_expense)
        
        return jsonify({'message': 'Redo successful'}), 200
    else:
        return jsonify({'message': 'Nothing to redo'}), 400


# API to generate weekly report
@app.route('/weekly_report', methods=['GET'])
def weekly_report():
    now = datetime.now()
    start_of_week = now - timedelta(days=now.weekday())  # Start of the week (Monday)
    end_of_week = start_of_week + timedelta(days=6)  # End of the week (Sunday)

    weekly_expenses = [expense for expense in expenses if start_of_week <= datetime.strptime(expense['date'], "%Y-%m-%d") <= end_of_week]
    
    total_weekly_expenses = sum(float(expense['amount']) for expense in weekly_expenses)

    return jsonify({
        'weekly_expenses': weekly_expenses,
        'total_weekly_expenses': total_weekly_expenses
    })


# API to generate monthly report
@app.route('/monthly_report', methods=['GET'])
def monthly_report():
    now = datetime.now()
    start_of_month = datetime(now.year, now.month, 1)  # First day of the current month
    end_of_month = datetime(now.year, now.month + 1, 1) - timedelta(days=1)  # Last day of the current month

    monthly_expenses = [expense for expense in expenses if start_of_month <= datetime.strptime(expense['date'], "%Y-%m-%d") <= end_of_month]

    total_monthly_expenses = sum(float(expense['amount']) for expense in monthly_expenses)

    return jsonify({
        'monthly_expenses': monthly_expenses,
        'total_monthly_expenses': total_monthly_expenses
    })


if __name__ == '__main__':
    app.run(debug=True)
