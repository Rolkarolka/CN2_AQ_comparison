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
        self.algorithm = AQ(T=self.train_dataset, m=n_best_complexes)

    def set_CN2(self):
        self.algorithm = CN2(dataset=self.train_dataset)

    def conduct(self):
        accuracy = 0
        precision = 0
        recall = 0
        f1_score = 0
        times_avg = 0

        for _ in range(self.n_executions):
            time_start = timer()
            self.algorithm.process()
            acc, prec, rec, f1 = self.algorithm.evaluate(self.test_dataset)
            accuracy += acc
            precision += prec
            recall += rec
            f1_score += f1
            exec_time = timer() - time_start
            times_avg += exec_time

        accuracy /= self.n_executions
        precision /= self.n_executions
        recall /= self.n_executions
        f1_score /= self.n_executions
        times_avg /= self.n_executions

        return accuracy, \
               precision, \
               recall, \
               f1_score, \
               times_avg

    def get_output(self):
        return self.algorithm.get_output()
