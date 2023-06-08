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

    testSetSize = 0.15
    nExecutions = 1
    nBestComplexes = 10

    attributesScaling = 1
    examplesScaling = 1

    def __init__(self):
        self._printIntro()
        self._inputDataset()
        self._inputModel()
        self._inputTestSetSize()
        self._inputNExecutions()
        self._inputAttributesScaling()
        self._inputExamplesScaling()
        if(self.model == "AQ"):
            self._inputNBestComplexes()
        
        experiment = Experiment(self.dataset, self.testSetSize, self.nExecutions, self.attributesScaling, self.examplesScaling)
        experiment.splitSet()
        if(self.model == 'AQ'):
            experiment.setAQ(self.nBestComplexes)
        accuracy, precision, specificity, sensitivity, delta_time = experiment.conduct()

        self._printResults(accuracy, precision, specificity, sensitivity, delta_time)

    def _printIntro(self):
        print()
        print("******************************")
        print("AQ & CN2 comparison")
        print("******************************")

    def _inputDataset(self):
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

    def _inputModel(self):
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

    def _inputTestSetSize(self):
        print()
        value = self.testSetSize
        try:
            value = float(input(f'Test set size [{self.testSetSize}]: '))
        except(ValueError):
            pass
        self.testSetSize = value if value > 0 and value < 1 else self.testSetSize
        print(f'Test set size: {self.testSetSize}')

    def _inputNExecutions(self):
        print()
        value = self.nExecutions
        try:
            value = int(input(f'Number of executions: [{self.nExecutions}]: '))
        except(ValueError):
            pass
        self.nExecutions = value if value > 0 else self.nExecutions
        print(f'Number of executions: {self.nExecutions}')

    def _inputNBestComplexes(self):
        print()
        value = self.nBestComplexes
        try:
            value = int(input(f'Number of best complexes: [{self.nBestComplexes}]: '))
        except(ValueError):
            pass
        self.nBestComplexes = value if value > 0 else self.nBestComplexes
        print(f'Number of best complexes: {self.nBestComplexes}')

    def _printResults(self, accuracy, precision, specificity, sensitivity, delta_time):
        print(f'Accuracy: {accuracy}')
        print(f'Precision: {precision}')
        print(f'Specificity: {specificity}')
        print(f'Sensivity: {sensitivity}')
        print(f'Time: {delta_time}')

    def _inputAttributesScaling(self):
        print()
        value = self.attributesScaling
        try:
            value = int(input(f'Attributes scaling: [{self.attributesScaling}]: '))
        except(ValueError):
            pass
        self.attributesScaling = value if value > 0 else self.attributesScaling
        print(f'Attributes scaling: {self.attributesScaling}')
    
    def _inputExamplesScaling(self):
        print()
        value = self.examplesScaling
        try:
            value = int(input(f'Examples scaling: [{self.examplesScaling}]: '))
        except(ValueError):
            pass
        self.examplesScaling = value if value > 0 else self.examplesScaling
        print(f'Examples scaling: {self.examplesScaling}')
