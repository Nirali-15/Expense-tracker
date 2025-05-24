// Sample data structure to store the expenses
let expenses = [];

// Initialize the chart with empty data
let expenseChart = new Chart(document.getElementById("expenseChart").getContext('2d'), {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            label: 'Expenses',
            data: [],
            backgroundColor: '#7dcfb6',
            borderColor: '#388E3C',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Add expense to the list and update the chart
document.getElementById("expenseForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const amount = document.getElementById("amount").value;
    const category = document.getElementById("category").value;
    const description = document.getElementById("description").value;
    const date = document.getElementById("date").value;

    // Create an expense object
    const expense = {
        amount: parseFloat(amount),
        category: category,
        description: description,
        date: date
    };

    // Add to expenses array
    expenses.push(expense);

    // Add to expense list on UI
    const expenseList = document.getElementById("expenseList");
    const li = document.createElement("li");
    li.textContent = `${category} - $${amount} on ${date}`;
    expenseList.appendChild(li);

    // Update the chart data
    updateChart();

    // Reset the form fields
    document.getElementById("expenseForm").reset();
});
// Sort expenses based on the selected criterion
document.getElementById("sortButton").addEventListener("click", function() {
    const sortBy = document.getElementById("sortBy").value;

    // Sorting logic
    if (sortBy === "category") {
        expenses.sort((a, b) => a.category.localeCompare(b.category));
    } else if (sortBy === "amount") {
        expenses.sort((a, b) => a.amount - b.amount);
    } else if (sortBy === "date") {
        expenses.sort((a, b) => new Date(a.date) - new Date(b.date));
    }

    // Re-render the sorted expense list
    renderExpenseList();
});

// Function to update the chart
function updateChart() {
    // Update the labels and data for the chart
    const labels = expenses.map(exp => exp.category);
    const data = expenses.map(exp => exp.amount);

    // Update the chart with new data
    expenseChart.data.labels = labels;
    expenseChart.data.datasets[0].data = data;
    expenseChart.update();
}

// Undo and Redo functionality (optional)
let undoStack = [];
let redoStack = [];

function undoExpense() {
    if (expenses.length > 0) {
        const lastExpense = expenses.pop();
        undoStack.push(lastExpense);
        updateChart();
        renderExpenseList();
    }
}

function redoExpense() {
    if (undoStack.length > 0) {
        const lastUndo = undoStack.pop();
        expenses.push(lastUndo);
        updateChart();
        renderExpenseList();
    }
}

function renderExpenseList() {
    const expenseList = document.getElementById("expenseList");
    expenseList.innerHTML = "";
    expenses.forEach(exp => {
        const li = document.createElement("li");
        li.textContent = `${exp.category} - $${exp.amount} on ${exp.date}`;
        expenseList.appendChild(li);
    });
}
