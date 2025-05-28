from flask import Flask, render_template, request, redirect
from models.transaction import Transaction
from models.categories import CategoryList
from utils.sql_handle import budget_entry, create_database, create_table, get_transactions, create_budget_table, get_current_budget, budget_limit_entry
from datetime import date
from collections import defaultdict

app = Flask(__name__)
DB_NAME = 'monthly_budget'
BUDGET_TABLE = 'budget_limit'

create_database(DB_NAME)
create_table(DB_NAME)
create_budget_table(DB_NAME, BUDGET_TABLE)

# debug
#budget_limit_entry(DB_NAME, BUDGET_TABLE, date.today(), 'Kläder', 1200)

category_list = CategoryList()


@app.route("/add_budget", methods=["POST"])
def add_budget():
    date_entry = request.form["budget_date"]
    category = request.form["budget_category"]
    amount = float(request.form["budget_amount"])
    budget_limit_entry(DB_NAME, BUDGET_TABLE, date_entry, category, amount)
    return redirect("/")

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
    budget_rows = get_current_budget(DB_NAME, BUDGET_TABLE)

    # Hämta aktuell månad och år
    today = date.today()
    current_month = today.month
    current_year = today.year

    # Bygg en lookup-dict för budget per kategori och månad
    budget_lookup = {}
    for row in budget_rows:
        date_obj = row[0]
        category = row[1]
        amount = float(row[2])
        if date_obj.month == current_month and date_obj.year == current_year:
            budget_lookup[category] = amount

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
        budget = budget_lookup.get(category, 0)  # Hämta från databasen, default 0
        remaining = round(budget - spent, 2)
        category_data[category] = {
            "spent": spent,
            "budget": budget,
            "remaining": remaining
        }

    budget_total = sum(category_totals.values())

    filtered_transactions.sort(key=lambda t: t[0], reverse=True)
    
    return render_template("index.html",
                        categories=category_list.get_all_categories(),
                        today=today.isoformat(),
                        category_data=category_data,
                        transactions=filtered_transactions,
                        budget_totals=budget_total)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)