import json
from pathlib import Path

class ProductRepository:
    _instance = None

    def __new__(cls, json_path='prods.json'):
        if not cls._instance:
            cls._instance = super(ProductRepository, cls).__new__(cls)
        return cls._instance

    def __init__(self, json_path='prods.json'):
        if not hasattr(self, 'initialized'): 
            self.initialized = True
            self.json_path = json_path
            self.products = self.load_products()

    def load_products(self):
        with open(self.json_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def get_product_by_id(self, product_id):
        for product in self.products:
            if product['id'] == product_id:
                return product
        return None


# Unittest
# product_repos = ProductRepository('prods.json')
# product = product_repos.get_product_by_id('6669d4248546532208394150')
# print(product)


