class CategoryList: 
    def __init__(self):
        self.food = 'Mat'
        self.animal = 'Djur'
        self.clothes = 'Kläder'
        self.entertainment = 'Nöjen'
        self.house_expenses = 'Grejer till hemmet'
        self.saving = 'Sparande'
        self.pharmacy = 'Apoteket'
        self.other = 'Övrigt'
        self.parking = 'Parkering'
        self.categories = [self.food, self.animal, self.clothes, self.entertainment, self.house_expenses, self.saving, self.pharmacy, self.other, self.parking]

        self.budgets = {
            'Mat': 13000,
            'Djur': 250,
            'Kläder': 2000,
            'Nöjen': 1000,
            'Grejer till hemmet': 1500,
            'Sparande': 2000,
            'Apoteket': 300,
            'Övrigt': 1500,
            'Parkering': 400
        }

    def get_all_categories(self):
        return self.categories

    def get_budget_for(self, category):
        return self.budgets.get(category, 0)