Stacks:
Undo/Redo Functionality: We use undo_stack for storing the previous state of expenses (before modifications). This allows us to undo and redo actions like adding or deleting an expense.
Queues:
The redo_stack is used to implement redo functionality. After performing an undo operation, the action is stored in the redo_stack so it can be re-applied later.
Hash Tables (Dictionaries):
The category_totals dictionary stores the sum of expenses for each category. This makes it easy to calculate and display the total expenses for each category in reports.
Linked Lists:
The ExpenseLinkedList class is used to track the history of expenses. Each expense is stored as a node in the linked list. This structure allows us to efficiently traverse and maintain the history of expenses.
Priority Queue:

The expense_queue (using Python's heapq module) stores expenses sorted by amount. This allows you to easily fetch the most expensive or least expensive expense.
