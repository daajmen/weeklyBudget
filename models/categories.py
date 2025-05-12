class CategoryList: 
    def __init__(self):
        self.food = 'Mat'
        self.animal = 'Djur'
        self.clothes = 'Kläder'
        self.entertainment = 'Nöjen'
        self.house_expenses = 'Grejer till hemmet'
        self.saving = 'Sparande'
        self.pharmacy = 'Apoteket'
        self.categories = [self.food, self.animal, self.clothes, self.entertainment, self.house_expenses, self.saving, self.pharmacy]

    def get_all_categories(self):
        return self.categories