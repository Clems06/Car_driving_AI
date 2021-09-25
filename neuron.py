import random
import math
import copy
"""
def sigmoid(x):
    return .5 * (math.tanh(.5 * x) + 1)"""
def sigmoid(x):
    if x<-100:
        return 0
    if x>100:
        return 1
    return 1 / (1 + math.exp(-4.9*x))

class Neuron:
    def __init__(self,num_outputs, neuronindex,weights=[]):
        self.outputWeights=[]
        self.neuronIndex= neuronindex

        for i in range(num_outputs):
            if i<len(weights):
                self.outputWeights.append(weights[i])
            else:
                self.outputWeights.append(random.uniform(-1,1))
    def getOutputWeight(self,i):
        return self.outputWeights[i]
    def getOutputFromInputs(self,inputs,inputWeights):
        output=0
        for i in range(len(inputWeights)):
            output+=inputs[i]*inputWeights[i]
        if output<-200:
            print(inputs,inputWeights)
        return sigmoid(output)
class Net:
    def __init__(self,topology=[],model=False):
        self.topolgy = topology
        if model!=False:
            self.layers=model.layers.copy()
        else:
            self.layers=[]
            for i in range(len(topology)-1):
                layer=[]
                numOutputs=topology[i+1]
                for neuronNum in range(topology[i]):
                    layer.append(Neuron(numOutputs,neuronNum))
                self.layers.append(layer)
            layer = []
            for i in range(topology[-1]):
                layer.append(Neuron(0,i))
            self.layers.append(layer)
    def feedLayer(self,inputs,layerNum):
        layer=self.layers[layerNum]
        outputs=[]
        for i in range(len(layer)):
            neuronWeights=[]
            for a in self.layers[layerNum-1]:
                neuronWeights.append(a.getOutputWeight(i))
            outputs.append(layer[i].getOutputFromInputs(inputs,neuronWeights))
        return outputs
    def feedAll(self,inputs):
        prevOutputs=inputs.copy()
        for i in range(1,len(self.layers)):
            prevOutputs=self.feedLayer(prevOutputs,i)
        return prevOutputs
class Population:
    def __init__(self,PopNumber,topology=[],bestResults=[]):
        self.topology=topology
        if len(bestResults)>=1:
            self.population=[]
            for i,score in bestResults:
                self.population.append(copy.deepcopy(i))
            prev_brains=[item[0] for item in bestResults]
            prev_results=[item[1] for item in bestResults]
            num_mutate=PopNumber-len(bestResults)
            random_chosen=random.choices(population=prev_brains, weights=prev_results, k=num_mutate)
            for addNet in random_chosen:
                mutation = self.mutate(addNet)
                self.population.append(mutation)
            for i in range(PopNumber-num_mutate-len(bestResults)):
                combination=self.combine(random.sample(bestResults, 2))
                self.population.append(combination)


        else:
            self.population=[]
            for i in range(PopNumber):
                self.population.append(Net(self.topology))

    def choose(self,options):
        output=[]
        numChosen=random.randint(1,len(options))
        for i in range(numChosen):
            output.append(options[random.randint(0,len(options)-1)])
        return output

    def combine(self,chosen):
        output= copy.deepcopy(chosen[0])
        for layer in range(len(output.layers)-1):
            for neuron in range(len(output.layers[layer])):
                for weight in range(self.topology[layer+1]):
                    if random.randint(0,10)>=5:
                        output.layers[layer][neuron].outputWeights[weight]=copy.copy(chosen[1].layers[layer][neuron].outputWeights[weight])
        return output
    def mutate(self,chosen):
        output=copy.deepcopy(chosen)
        for layer in output.layers[:-1]:
            for neuron in layer:
                for weight in range(len(neuron.outputWeights)):
                    rand=random.randint(1,10)
                    if rand==1:
                        neuron.outputWeights[weight]=random.uniform(-1,1)
                    else:
                        neuron.outputWeights[weight] += random.gauss(0,1)/50
                        if neuron.outputWeights[weight]>1:
                            neuron.outputWeights[weight]=1
                        elif neuron.outputWeights[weight]<-1:
                            neuron.outputWeights[weight]=1
        return output
