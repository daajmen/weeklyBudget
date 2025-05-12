from flask import Flask, render_template, request, redirect
from models.transaction import Transaction
from models.categories import CategoryList
from utils.sql_handle import budget_entry, create_database, create_table
from datetime import date

app = Flask(__name__)
DB_NAME = 'monthly_budget'

create_database(DB_NAME)
create_table(DB_NAME)

category_list = CategoryList()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        t = Transaction()
        t.category = request.form["category"]
        t.description = request.form["description"]
        t.amount = float(request.form["amount"])
        budget_entry(t, DB_NAME)
        return redirect("/")
    
    return render_template("index.html", categories=category_list.get_all_categories(), today=date.today().isoformat())

if __name__ == "__main__":
    app.run(debug=True)
