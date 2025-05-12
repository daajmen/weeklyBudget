from utils.sql_handle import create_database, create_table, budget_entry
from models.categories import CategoryList
from models.transaction import Transaction 


budget_data = Transaction()
category_list = CategoryList()

database = 'monthly_budget'

create_database(database)
create_table(database)
budget_entry(budget_data, database)