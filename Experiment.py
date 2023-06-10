import random
import copy
from timeit import default_timer as timer

from AQ import AQ
from CN2 import CN2
from DataSet import DataSet


class Experiment():
    def __init__(self, dataset, test_set_size, n_executions, attributes_scaling, examples_scaling):
        self.dataset = DataSet(dataset)
        self.test_set_size = test_set_size
        self.n_executions = n_executions
        self.attributes_scaling = attributes_scaling
        self.examples_scaling = examples_scaling
    
    def scale_set(self):
        self.dataset.scale_attributes(self.attributes_scaling)
        self.dataset.scale_examples(self.examples_scaling)

    def split_set(self):
        temp_ds = copy.deepcopy(self.dataset)
        random.shuffle(temp_ds)
        length = len(temp_ds)
        length_train = round((1 - self.test_set_size) * length)

        self.train_dataset = temp_ds[:length_train]
        self.test_dataset = temp_ds[length_train:]

    def set_AQ(self, n_best_complexes):
        self.algorithm = AQ(T = self.train_dataset, m = n_best_complexes)

    def set_CN2(self):
        self.algorithm = CN2(dataset = self.train_dataset)

    def conduct(self):
        nprecisions = 0
        accuracy = 0
        precision = 0
        specificity = 0
        sensitivity = 0
        time_start = timer()

        for _ in range(self.n_executions):
            self.algorithm.process()
            acc, prec, spec, sens = self.algorithm.evaluate(self.test_dataset)
            accuracy += acc
            if prec:
                precision += prec
                nprecisions += 1
            specificity += spec
            sensitivity += sens

        accuracy /= self.n_executions
        precision /= nprecisions
        specificity /= self.n_executions
        sensitivity /= self.n_executions
        f1 = 2 * (precision * sensitivity) / (precision + sensitivity)

        return accuracy, \
               precision, \
               specificity, \
               sensitivity, \
               f1, \
               timer() - time_start
