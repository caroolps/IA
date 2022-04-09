import pandas as pd
from apriori_2_algorithm import *
import pymongo

application_client = pymongo.MongoClient("mongodb://localhost:27017/")
application_db = application_client["apriori"]
application_collection = application_db["rule"]

#Reading CSV data archive
basket_data = pd.read_csv('cantores.csv')

#Item grouping by transaction id and conversion to set data type.
items_by_transaction = basket_data.groupby('escutado')['cantor'].apply(set)
itemset = basket_data['cantor'].unique()


rules = apriori_2(itemset, items_by_transaction, 0.05, 0.10)

composite_rule = []

for rule in rules[1]: 

    percept = rule['rule'].split('==>')[0].replace(" ", "")
    action = rule['rule'].split('==>')[1].replace(" ", "")

    newRule = {'relation':"==", 'percept_ref': "'" + percept + "'", 'percept_name': "cantor", 'action': "'" + action + "'"}
    application_collection.insert_one({
        'rules': newRule,
        'operators': []
    })
