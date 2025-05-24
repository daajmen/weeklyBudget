from flask import Flask, render_template, request, redirect
from models.transaction import Transaction
from models.categories import CategoryList
from utils.sql_handle import budget_entry, create_database, create_table, get_transactions, create_budget_table
from datetime import date
from collections import defaultdict

app = Flask(__name__)
DB_NAME = 'monthly_budget'

create_database(DB_NAME)
create_table(DB_NAME)
create_budget_table(DB_NAME)

category_list = CategoryList()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        t = Transaction()
        t.category = request.form["category"]
        t.description = request.form["description"]
        t.amount = float(request.form["amount"])
        t.date = request.form["date"]
        budget_entry(t, DB_NAME)
        return redirect("/")
    

    # Hämta alla transaktioner från databasen
    transactions = get_transactions(DB_NAME)

    # Hämta aktuell månad och år
    today = date.today()
    current_month = today.month
    current_year = today.year

    # Skapa en dictionary för att lagra kostnader per kategori
    category_totals = defaultdict(float)
    
    filtered_transactions = []
    category_data = {}

    for transaction in transactions:
        if transaction[0].month == current_month and transaction[0].year == current_year:
            category = transaction[1]
            amount = float(transaction[3])
            category_totals[category] += amount
            filtered_transactions.append(transaction)

    # Bygg upp dict med total, budget och kvar
    for category in category_totals:
        spent = round(category_totals[category], 2)
        budget = category_list.get_budget_for(category)
        remaining = round(budget - spent, 2)
        category_data[category] = {
            "spent": spent,
            "budget": budget,
            "remaining": remaining
        }

    budget_total = sum(category_totals.values())

    return render_template("index.html",
                        categories=category_list.get_all_categories(),
                        today=today.isoformat(),
                        category_data=category_data,
                        transactions=filtered_transactions,
                        budget_totals=budget_total)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)