from flask import Flask, render_template, request, redirect
from models.transaction import Transaction
from models.categories import CategoryList
from utils.sql_handle import budget_entry, create_database, create_table, get_transactions
from datetime import date
from collections import defaultdict

app = Flask(__name__)
DB_NAME = 'monthly_budget'

create_database(DB_NAME)
create_table(DB_NAME)

category_list = CategoryList()

@app.route("/weekly_budget", methods=["GET", "POST"])
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
    
    # Filtrera och summera transaktioner för den aktuella månaden
    filtered_transactions = []
    for transaction in transactions:
        if transaction[0].month == current_month and transaction[0].year == current_year:
            category_totals[transaction[1]] += float(transaction[3])  # Omvandla Decimal till float
            filtered_transactions.append(transaction)  # Lägg till transaktionen för visning


    return render_template("index.html", 
                           categories=category_list.get_all_categories(), 
                           today=today.isoformat(),
                           category_totals=category_totals,
                           transactions=filtered_transactions) 

if __name__ == "__main__":
    app.run(debug=True)
