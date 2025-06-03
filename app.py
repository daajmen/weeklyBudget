from flask import Flask, render_template, request, redirect
from models.transaction import Transaction
from models.categories import CategoryList
from models.budget_logic import get_budget_period
from utils.sql_handle import budget_entry, create_database, create_table, get_transactions, create_budget_table, get_current_budget, budget_limit_entry
from datetime import date
from collections import defaultdict, OrderedDict

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
    today = date.today()


    # Hämta alla perioder som finns i budgettabellen
    periods = set()
    for row in budget_rows:
        date_obj = row[0]
        # Beräkna period_start för varje budgetpost
        p_start, p_end = get_budget_period(date_obj)
        periods.add((p_start, p_end))
    # Sortera perioderna nyast först
    periods = sorted(periods, reverse=True)

    # Läs in vald period från query-param, annars ta aktuell
    selected_period = request.args.get("period")
    if selected_period:
        # Format: "YYYY-MM-DD_YYYY-MM-DD"
        start_str, end_str = selected_period.split("_")
        period_start = date.fromisoformat(start_str)
        period_end = date.fromisoformat(end_str)
    else:
        period_start, period_end = get_budget_period(today)

    # Bygg en lookup-dict för budget per kategori och period
    budget_lookup = {}
    for row in budget_rows:
        date_obj = row[0]
        category = row[1]
        amount = float(row[2])
        if period_start <= date_obj <= period_end:
            budget_lookup[category] = amount

    # Skapa en dictionary för att lagra kostnader per kategori
    category_totals = defaultdict(float)
    filtered_transactions = []
    category_data = {}

    for transaction in transactions:
        t_date = transaction[0]
        if period_start <= t_date <= period_end:
            category = transaction[1]
            amount = float(transaction[3])
            category_totals[category] += amount
            filtered_transactions.append(transaction)


    # Bygg upp dict med total, budget och kvar
    for category in category_list.get_all_categories():
        spent = round(category_totals.get(category, 0), 2)
        budget = budget_lookup.get(category, 0)
        remaining = round(budget - spent, 2)
        category_data[category] = {
            "spent": spent,
            "budget": budget,
            "remaining": remaining
        }

    # Totalt spenderat
    total_spent = sum([inner_dict['spent'] for inner_dict in category_data.values()])
    # Total budget
    total_budget = sum([inner_dict['budget'] for inner_dict in category_data.values()])

    filtered_transactions.sort(key=lambda t: t[0], reverse=True)

    return render_template("index.html",
        categories=category_list.get_all_categories(),
        today=today.isoformat(),
        category_data=category_data,
        transactions=filtered_transactions,
        total_spent=round(total_spent, 2),
        total_budget=round(total_budget, 2),
        period_start=period_start,
        period_end=period_end,
        periods=periods
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)