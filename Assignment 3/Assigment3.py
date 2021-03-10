import pandas as pd

dataset = pd.read_csv('Market_Basket_Optimisation.csv', header = None)

trans = []

for i in range(0, 7501):
    trans.append([str(dataset.values[i,j]) for j in range(0, 20) if str(dataset.values[i,j])!='nan'])

from apyori import apriori    

rules = apriori(trans,min_support = 0.004,min_confidence = 0.3,min_lift = 3)

results = list(rules)

print("Number of rules mined = ",len(results))

for item in results:
    pair = item[2]
    items = [x for x in pair]
    for i in range(0,len(items)):
        print("Rule: " ,list(items[i][0]), " -> " , list(items[i][1]))
        print("Confidence: " + str(items[i][2]))
        print("Lift: " + str(items[i][3]))
    print("Support: " + str(item[1]))
    print("=====================================")