from CN2 import CN2
from DataSet import DataSet
from AQ import AQ
import random
import copy

if __name__ == "__main__":
    dataset = "./datasets/car-evaluation/car.data"
    model = "AQ"

    valSplit = 0.15
    trainSplit = 0.8
    nexecutions = 1

    # podział zbioru na treningowy/walidacyjny i testowy
    ds = DataSet(dataset)
    temp_ds = copy.deepcopy(ds)
    random.shuffle(temp_ds)
    length = len(temp_ds)
    length_train = round(trainSplit * length)
    train_dataset = temp_ds[:length_train]
    test_dataset = temp_ds[length_train:]

    nprecisions = 0
    accuracy = 0
    precision = 0
    specificity = 0
    sensitivity = 0
    for _ in range(nexecutions):
        if model == "AQ":
            algorithm = AQ(T = train_dataset, m = 10)
        else:
            algorithm = CN2()
        print(algorithm.getHighestQualityComplex())
        bestComplex, acc, prec, spec, sens = algorithm.get_best_complex_with_measures(dataset=test_dataset)
        accuracy += acc
        if prec:
            precision += prec
            nprecisions += 1
        specificity += spec
        sensitivity += sens

    print("Model: ", model)
    print("Zbiór danych: ", dataset[11:])
    if model == "modifiedAQ":
        print("Część jaką stanowi zbior walidacyjny: ", valSplit)
    print("Srednie miary z ", nexecutions, " wykonań algorytmu.")
    print("Dokładność: ", accuracy / nexecutions)
    print("Precyzja: ", precision / nprecisions)
    print("Swoistość: ", specificity / nexecutions)
    print("Czułość: ", sensitivity / nexecutions)