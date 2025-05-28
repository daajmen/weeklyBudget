"""
This module provides utility functions for handling PostgreSQL databases and tables.
"""
import psycopg2
from psycopg2 import sql
from models.transaction import Transaction
from models.categories import CategoryList
from datetime import date

def create_database(db_name):
    """
    Creates a new PostgreSQL database with the specified name.
    Connects to the default "postgres" database as a superuser to perform the operation.

    Parameters:
        db_name (str): The name of the database to be created.

    Exceptions:
        Raises an exception if the database creation fails.

    Notes:
        - Ensure the PostgreSQL server is running.
        - Verify that the credentials provided are correct.
        - The user must have sufficient privileges to create databases.
    """
    try:
        # Anslut till PostgreSQL som superuser (postgres)
        conn = psycopg2.connect(
            dbname="postgres",  # Anslut till den befintliga "postgres"-databasen
            user="postgres",
            password="",  # Ändra till ditt lösenord
            host="192.168.50.16",
            port=5432

        )
        conn.autocommit = True  # Krävs för att skapa databaser
        cursor = conn.cursor()

        # SQL för att skapa databasen
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))

        print(f"Databasen {db_name} skapades!")
    except Exception as e:
        print(f"Ett fel uppstod vid skapandet av tabellen: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def get_connection(database):
    """
    Establishes a connection to a PostgreSQL database.
    Args:
        database (str): The name of the database to connect to.
    Returns:
        psycopg2.extensions.connection: A connection object to interact with the database.
    Raises:
        psycopg2.OperationalError: If the connection to the database fails.
    
    """
    return psycopg2.connect(
        host="192.168.50.16",
        database=database,
        user="postgres",
        password= '',
        port=5432
    )


def create_table(db_name):
    """
    Creates a table in the specified PostgreSQL database if it does not already exist.
    The table includes columns for id, date, category, description, and amount.

    Parameters:
        db_name (str): The name of the database where the table will be created.

    Exceptions:
        Raises an exception if the table creation fails.

    Notes:
        - Requires a valid connection to the specified database.
        - The table schema includes:
            - id: SERIAL PRIMARY KEY
            - date: DATE NOT NULL
            - category: TEXT NOT NULL
            - description: TEXT NOT NULL
            - amount: NUMERIC NOT NULL
    """
    try:
        with get_connection(db_name) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'''
                    CREATE TABLE IF NOT EXISTS {db_name} (
                        id SERIAL PRIMARY KEY,
                        date DATE NOT NULL,
                        category TEXT NOT NULL,
                        description TEXT NOT NULL,
                        amount NUMERIC NOT NULL
                    );
                ''')
                conn.commit()
                if cursor.rowcount == -1:  # rowcount is -1 for CREATE TABLE IF NOT EXISTS
                    print(f"Tabellen {db_name} existerar redan.")
                else:
                    print(f"Tabellen {db_name} skapades.")
    except Exception as e:
        print(f"Ett fel uppstod: {e}")

def create_budget_table(db_name, table_name):
    """
    Creates a table in the specified PostgreSQL database if it does not already exist.
    The table includes columns for id, date, category, and amount.
    Table name is predefined as budget_limit

    Parameters:
        table_name (str): The name of the database where the table will be created.

    Exceptions:
        Raises an exception if the table creation fails.

    Notes:
        - Requires a valid connection to the specified database.
        - The table schema includes:
            - id: SERIAL PRIMARY KEY
            - date: DATE NOT NULL
            - category: TEXT NOT NULL
            - amount: NUMERIC NOT NULL
    """   
    try:
        with get_connection(db_name) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'''
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        id SERIAL PRIMARY KEY,
                        date DATE NOT NULL,
                        category TEXT NOT NULL,
                        amount NUMERIC NOT NULL
                    );
                ''')
                conn.commit()
                if cursor.rowcount == -1:  # rowcount is -1 for CREATE TABLE IF NOT EXISTS
                    print(f"Tabellen {table_name} existerar redan.")
                else:
                    print(f"Tabellen {table_name} skapades.")
    except Exception as e:
        print(f"Ett fel uppstod: {e}")
        

def budget_entry(transaction_entry: Transaction, db_name: str):
    """
    Inserts a transaction entry into the database.

    Parameters:
        transaction_entry (Transaction): The transaction to be added.

    Raises:
        ValueError: If any field in the transaction is invalid.
    """
    try:
        with get_connection(db_name) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'''
                    INSERT INTO {db_name} (date, category, description, amount)
                    VALUES (%s, %s, %s, %s)
                ''', (transaction_entry.date, transaction_entry.category, transaction_entry.description, transaction_entry.amount))
                conn.commit()
                print("Transaktionen har lagts till.")
    except Exception as e:
        print(f"Ett fel uppstod: {e}, {transaction_entry}")    

def get_transactions(db_name):
    try:
        with get_connection(db_name) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT date, category, description, amount FROM {db_name};")
                return cursor.fetchall()
    except Exception as e:
        print(f"Ett fel uppstod vid hämtning av transaktioner: {e}")
        return []
    
def get_current_budget(db_name, table_name): 
    try:
        with get_connection(db_name) as conn: 
            with conn.cursor() as cursor: 
                cursor.execute(f"SELECT date, category, amount FROM {table_name};")
                return cursor.fetchall()
    except Exception as e: 
        print(f'Något gick fel {e}')
        return []
    
def budget_limit_entry(db_name: str, table_name: str, date_entry: date, catergory: str, amount: float):
    """
    Inserts a budget limit for the month 
    
    Parameters: 
        db_name: Database name
        table_name: Name of the table that keeps the budget limit
        date_entry: The date of the budget
        catergory_object: A category list that will be sent into the DB

    Raises

    """

    try:
        with get_connection(db_name) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'''
                    INSERT INTO {table_name} (date, category, amount)
                    VALUES (%s, %s, %s)
                ''', (date_entry, catergory, amount))
                conn.commit()
                print("Budgeten har uppdaterats.")
    except Exception as e:
        print(f"Ett fel uppstod: {e}, {catergory}")    
