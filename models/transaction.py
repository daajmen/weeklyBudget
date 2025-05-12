from datetime import date

class Transaction: 
    def __init__(self):
        self.date = date.today()  # Default to today's date
        self.category = ''
        self.description = ''
        self.amount = float


    def __str__(self):
        return f'{self.date}, {self.category}, {self.description}, {self.amount}kr'
    