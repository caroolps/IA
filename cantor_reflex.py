from inference_engine import Inference, Rule
import pymongo
# import main
# from main import rules

application_client = pymongo.MongoClient("mongodb://localhost:27017/")
application_db = application_client["apriori"]
application_collection = application_db["rule"]

#Insert rules

composite_rules = application_collection.find()
inferences = []
for composite_rule in composite_rules:

    rules = []
    rule = composite_rule['rules']
    r = Rule(rule['relation'], rule['percept_ref'], rule['percept_name'], rule['action'])
    rules.append(r)
    inferences.append(Inference(rules, composite_rule['operators'], rule['action']))

item = input("Qual foi o cantor(a) mais escutado(a)? \n")
percepts = [{"cantor": "'" + item + "'" }]

for inference in inferences:

    for percept in percepts:

        # print(percept.get('cantor'))

        inference_result = inference.infer(percept)
        if inference_result != 'False':
            print(f" Cantor(a) escutado(a): {percept.get('cantor')} \n Sugestão de Cantor(a) que você pode gostar : {inference_result}")
