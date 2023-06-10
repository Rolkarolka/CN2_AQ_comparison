from Experiment import Experiment

class UserInterface():
    datasets = [
        "./datasets/balloons/adult-stretch.data",
        "./datasets/balloons/adult+stretch.data",
        "./datasets/balloons/yellow-small.data",
        "./datasets/balloons/yellow-small+adult-stretch.data",
        "./datasets/breast-cancer/breast-cancer.data",
        "./datasets/car-evaluation/car.data",
        "./datasets/mushroom/agaricus-lepiota.data"
    ]
    dataset = "./datasets/car-evaluation/car.data"

    models = [
        "AQ",
        "CN2"
    ]
    model = "AQ"

    test_set_size = 0.15
    n_executions = 1
    n_best_complexes = 10

    attributes_scaling = 1
    examples_scaling = 1

    def __init__(self):
        self._print_intro()
        self._input_dataset()
        self._input_model()
        self._input_test_set_size()
        self._input_n_executions()
        self._input_attributes_scaling()
        self._input_examples_scaling()
        if(self.model == "AQ"):
            self._input_n_best_complexes()
        
        experiment = Experiment(self.dataset, self.test_set_size, self.n_executions, self.attributes_scaling, self.examples_scaling)
        experiment.split_set()
        if(self.model == 'AQ'):
            experiment.set_AQ(self.n_best_complexes)
        elif(self.model == 'CN2'):
            experiment.set_CN2()
        accuracy, precision, specificity, sensitivity, f1, delta_time = experiment.conduct()

        self._print_results(accuracy, precision, specificity, sensitivity, f1, delta_time)

    def _print_intro(self):
        print()
        print("******************************")
        print("AQ & CN2 comparison")
        print("******************************")

    def _input_dataset(self):
        print()
        print(f'Datasets:')
        for idx, set in enumerate(self.datasets):
            print(f'{idx + 1}. {set}')
        datasetIdx = self.datasets.index(self.dataset)
        try:
            datasetIdx = int(input(f'Dataset [{datasetIdx + 1}]: ')) - 1
        except(ValueError):
            pass
        self.dataset = self.datasets[datasetIdx] if datasetIdx >= 0 and datasetIdx < len(self.datasets) else self.dataset
        print(f'Dataset: {self.dataset}')

    def _input_model(self):
        print()
        print(f'Models:')
        for idx, model in enumerate(self.models):
            print(f'{idx + 1}. {model}')
        modelIdx = self.models.index(self.model)
        try:
            modelIdx = int(input(f'Model [{modelIdx + 1}]: ')) - 1
        except(ValueError):
            pass
        self.model = self.models[modelIdx] if modelIdx >= 0 and modelIdx < len(self.models) else self.model
        print(f'Model: {self.model}')

    def _input_test_set_size(self):
        print()
        value = self.test_set_size
        try:
            value = float(input(f'Test set size [{self.test_set_size}]: '))
        except(ValueError):
            pass
        self.test_set_size = value if value > 0 and value < 1 else self.test_set_size
        print(f'Test set size: {self.test_set_size}')

    def _input_n_executions(self):
        print()
        value = self.n_executions
        try:
            value = int(input(f'Number of executions: [{self.n_executions}]: '))
        except(ValueError):
            pass
        self.n_executions = value if value > 0 else self.n_executions
        print(f'Number of executions: {self.n_executions}')

    def _input_n_best_complexes(self):
        print()
        value = self.n_best_complexes
        try:
            value = int(input(f'Number of best complexes: [{self.n_best_complexes}]: '))
        except(ValueError):
            pass
        self.n_best_complexes = value if value > 0 else self.n_best_complexes
        print(f'Number of best complexes: {self.n_best_complexes}')

    def _print_results(self, accuracy, precision, specificity, sensitivity, f1, delta_time):
        print(f'Accuracy: {accuracy}')
        print(f'Precision: {precision}')
        print(f'Specificity: {specificity}')
        print(f'Sensivity: {sensitivity}')
        print(f'F1: {f1}')
        print(f'Time: {delta_time}')

    def _input_attributes_scaling(self):
        print()
        value = self.attributes_scaling
        try:
            value = int(input(f'Attributes scaling: [{self.attributes_scaling}]: '))
        except(ValueError):
            pass
        self.attributes_scaling = value if value > 0 else self.attributes_scaling
        print(f'Attributes scaling: {self.attributes_scaling}')
    
    def _input_examples_scaling(self):
        print()
        value = self.examples_scaling
        try:
            value = int(input(f'Examples scaling: [{self.examples_scaling}]: '))
        except(ValueError):
            pass
        self.examples_scaling = value if value > 0 else self.examples_scaling
        print(f'Examples scaling: {self.examples_scaling}')
