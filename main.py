from CN2 import CN2
from DataSet import DataSet
from AQ import AQ
import random
import copy


# def format_rules(rules):
#     for rule, common_class in rules:
#         rule_str = str(list(rule))
#         print(f"Rule: {rule_str:50} Class: {common_class[0]:10} Covered: {common_class[1]}")
#

if __name__ == "__main__":
    dataset = "./datasets/car.data"
    model = "CN2"

    valSplit = 0.15
    trainSplit = 0.8
    nexecutions = 1
    m = 10

    # podział zbioru na treningowy/walidacyjny i testowy
    ds = DataSet(dataset)
    ds.get_set_with_known_attributes()
    temp_ds = copy.deepcopy(ds)
    random.shuffle(temp_ds)
    length = len(temp_ds)
    length_train = round(trainSplit * length)
    train_dataset = temp_ds[:length_train]
    test_dataset = temp_ds[length_train:]

    accuracy = 0
    precision = 0
    recall = 0
    f1_score = 0

    for _ in range(nexecutions):
        if model == "AQ":
            algorithm = AQ(T=train_dataset, m=m)
            # rules = algorithm.process()
        else:
            algorithm = CN2(dataset=train_dataset)
        acc, prec, rec, f1 = algorithm.evaluate(test_dataset)
        accuracy += acc
        precision += prec
        recall += rec
        f1_score += f1

    print("Model: ", model)
    print("Zbiór danych: ", dataset[11:])
    if model == "modifiedAQ":
        print("Część jaką stanowi zbior walidacyjny: ", valSplit)
    print("Srednie miary z ", nexecutions, " wykonań algorytmu.")
    print("Dokładność: ", accuracy / nexecutions)
    print("Precyzja: ", precision / nexecutions)
    print("Czułość: ", recall / nexecutions)
    print("F1: ", f1_score / nexecutions)
