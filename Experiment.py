import random
import copy
from timeit import default_timer as timer

from AQ import AQ
from CN2 import CN2
from DataSet import DataSet


class Experiment():
    def __init__(self, dataset, testSetSize, nExecutions, attributesScaling, examplesScaling):
        self.dataset = DataSet(dataset)
        self.testSetSize = testSetSize
        self.nExecutions = nExecutions
        self.attributesScaling = attributesScaling
        self.examplesScaling = examplesScaling
    
    def scaleSet(self):
        self.dataset.scaleAttributes(self.attributesScaling)
        self.dataset.scaleExamples(self.examplesScaling)

    def splitSet(self):
        temp_ds = copy.deepcopy(self.dataset)
        random.shuffle(temp_ds)
        length = len(temp_ds)
        length_train = round((1 - self.testSetSize) * length)

        self.train_dataset = temp_ds[:length_train]
        self.test_dataset = temp_ds[length_train:]

    def setAQ(self, nBestComplexes):
        self.algorithm = AQ(T = self.train_dataset, m = nBestComplexes)

    def conduct(self):
        nprecisions = 0
        accuracy = 0
        precision = 0
        specificity = 0
        sensitivity = 0
        time_start = timer()

        for _ in range(self.nExecutions):
            self.algorithm.getHighestQualityComplex()
            bestComplex, acc, prec, spec, sens = self.algorithm.get_best_complex_with_measures(dataset=self.test_dataset)
            accuracy += acc
            if prec:
                precision += prec
                nprecisions += 1
            specificity += spec
            sensitivity += sens

        return accuracy / self.nExecutions, \
               precision / nprecisions, \
               specificity / self.nExecutions, \
               sensitivity / self.nExecutions, \
               timer() - time_start
