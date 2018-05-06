# COMP307 - Assignment1 - part2
# 300434790 - Yalian

import copy
import os
import os.path
import argparse

class Feature:
    def __init__(self, column, data):
        self._name = data[0][column]
        self._values = set()
        self._weighted_impurity = 0
        for row in range(1, len(data)):
            self._values.add(FeatureValue(data[row][column]))
        for featureVal in self._values:
            counter = 0
            for row in range(1, len(data)):
                if featureVal.get_name() == data[row][column]:
                    counter += 1
                    featureVal.set_occurences(counter)
            featureVal.set_prob(float(featureVal.get_occurences()/(len(data) - 1)))
    def get_values(self): return self._values
    def get_name(self): return self._name
    def get_weighted_impurity(self): return self._weighted_impurity
    def set_weighted_impurity(self, weighted_impurity): self._weighted_impurity = weighted_impurity
    def __str__(self): return self._name

class FeatureValue:
    def __init__(self, name):
        self._name = name
        self._occurences = 0
        self._prob = 0
        self._impurity = 0
    def get_name(self): return self._name
    def get_occurences(self): return self._occurences
    def set_occurences(self, occurences): self._occurences = occurences 
    def get_prob(self): return self._prob
    def set_prob(self, prob): self._prob = prob
    def get_impurity(self): return self._impurity
    def set_impurity(self, impurity): self._impurity = impurity
    def __str__(self): return self._name
    def __eq__(self, o): return (isinstance(o, FeatureValue)) and (o._name == self._name)
    def __hash__(self): return hash(self._name)

class Node:
    def __init__(self, bestAttr, left, right):														
        self._bestAttr = bestAttr
        self._left = left
        self._right = right
    
    def get_bestAttr(self): return self._bestAttr
    def set_left(self, left): self._left = left
    def get_left(self): return self._left
    def set_right(self, right): self._right = right
    def get_right(self): return self._right

    def report(self, indent, f):
        print(indent + str(self._bestAttr) + ' = True: ')
        f.write(indent + str(self._bestAttr) + ' = True: \n')
        if isinstance(self._left, tuple) == True:
            print(indent + '\t', self._left)
            f.write(indent + '\t' + str(self._left))
            f.write('\n')
        else:
            self._left.report(indent + '\t', f)
        
        print(indent + str(self._bestAttr) + ' = False: ')
        f.write(indent + str(self._bestAttr) + ' = False: \n')
        if isinstance(self._right, tuple) == True:
            print(indent + '\t', self._right)  
            f.write(indent + '\t'+ str(self._right))  
            f.write('\n')
        else:
            self._right.report(indent + '\t', f)
       

def prepare_dataset(file):
    class_list, attr_list, dataset = ([] for i in range(3))
    with open(file, 'r') as f:
        data = f.read().split('\n')
        class_list = data[0].split()
        attr_list = data[1].split()
        attr_list.append('CATEGORY')
        
        dataset.append(attr_list)

        for i in range(2,len(data)):
            line = data[i].split()
            if line!='\n' and line!='\r' and len(line)!=0:
                first_val = line.pop(0)
                line.append(first_val)
                dataset.append(line)

    return dataset, class_list 

def get_baseline_class(dataset):
    feature_cat = Feature(len(dataset[0])-1,dataset)
    cat_list = {}
    for val in feature_cat.get_values(): 
        cat_list[val.get_name()] = val.get_occurences()
    return max(cat_list, key=cat_list.get)     

def prepare_sub_dataset(dataset, bestAttr, boolVal):
    subDS = []
    subDS.append(copy.deepcopy(dataset[0]))
    bestAttr_index = dataset[0].index(bestAttr.get_name())
    
    for row in range(1, len(dataset)):
        if dataset[row][bestAttr_index] == boolVal:
            subDS.append(copy.deepcopy(dataset[row]))

    for sub in subDS:
        sub.pop(bestAttr_index)    
    return subDS

def BuildTree(dataset, class_list):
    feature_cat = Feature(len(dataset[0])-1,dataset)
    if len(feature_cat.get_values()) == 1: #instances are pure  
        cat = list(feature_cat.get_values())[0]
        return cat.get_name(), cat.get_occurences()
    if len(dataset[0]) == 1: #attribute is empty
        feature_cat = Feature(len(dataset[0])-1,dataset)
        cat_list = {}
        for val in feature_cat.get_values(): 
            cat_list[val.get_name()] = val.get_occurences()
        return max(cat_list, key=cat_list.get), cat_list[max(cat_list)]
    else:
        CLASS1 = class_list[0]
        CLASS2 = class_list[1]

        BOOL_TRUE = 'true'
        BOOL_FALSE = 'false'

        featureImpurity = {}
        
        for column in range(0, len(dataset[0])-1): 
            count_true_class1, count_true_class2, count_false_class1, count_false_class2  = (0 for i in range(4))
            for row in range(1, len(dataset)):          
                feature_val = dataset[row][column]
                cat_val = dataset[row][len(dataset[0]) - 1]
                if feature_val == BOOL_TRUE:
                    if cat_val == CLASS1: count_true_class1 += 1
                    elif cat_val == CLASS2: count_true_class2 += 1
                elif feature_val == BOOL_FALSE:
                    if cat_val == CLASS1: count_false_class1 += 1
                    elif cat_val == CLASS2: count_false_class2 += 1
            feature = Feature(column,dataset)      

            for val in feature.get_values(): 
                if val.get_name() == BOOL_TRUE:
                    impurity = (count_true_class1 * count_true_class2) / (val.get_occurences()**2)
                elif val.get_name() == BOOL_FALSE:
                    impurity = (count_false_class1 * count_false_class2) / (val.get_occurences()**2)
                val.set_impurity(impurity)
            
            w_impurity = 0
            for val in feature.get_values():
                w_impurity +=  val.get_prob() * val.get_impurity()      
            feature.set_weighted_impurity(w_impurity)
            featureImpurity[feature] = feature.get_weighted_impurity()

        bestAttr = min(featureImpurity, key=featureImpurity.get)

        best_attr_true_set = prepare_sub_dataset(dataset, bestAttr, BOOL_TRUE)
        best_attr_false_set = prepare_sub_dataset(dataset, bestAttr, BOOL_FALSE)
        left = BuildTree(best_attr_true_set, class_list)
        right = BuildTree(best_attr_false_set, class_list)

    return Node(bestAttr, left, right)

def get_accuracy(dataset, node, f):
    correct = 0
    for row in range(1, len(dataset)):
        rootnode = node
        while not isinstance(rootnode, tuple):
            bestAttr_index = dataset[0].index(rootnode.get_bestAttr().get_name())
            if dataset[row][bestAttr_index] == 'true':
                rootnode = rootnode.get_left()
            elif dataset[row][bestAttr_index] == 'false':
                rootnode = rootnode.get_right()

        if rootnode[0] == dataset[row][len(dataset[0]) - 1]:
            correct += 1   
    f.write(str(correct) + ' correct out of ' + str(len(dataset) - 1) + '\n')
    accuracy = round(float(correct) / (len(dataset) - 1) * 100, 2)
    return accuracy

def get_baseline_accuracy(dataset, baseline_class):
    correct = 0
    for row in range(1, len(dataset)):
        if dataset[row][len(dataset[0])-1] == baseline_class:
            correct += 1
    accuracy = round(float(correct)/(len(dataset) - 1) * 100, 2)
    return accuracy
    

def Main():
    output_file = 'sampleoutput.txt'
    if os.path.exists(output_file):
        os.remove(output_file)

    parser = argparse.ArgumentParser()
    parser.add_argument('trainingset', help='Choose a training data set')
    parser.add_argument('testset', help='Choose a test data set')
    args = parser.parse_args()

    with open(output_file, 'a') as f:
        f.write('Reading training data from file ' + str(args.trainingset) + '\n')
        (dataset, class_list) = prepare_dataset(args.trainingset)
        f.write(str(len(class_list)) + ' categories \n')
        f.write(str(len(dataset[0])) + ' attributes \n')
        f.write('Read ' + str(len(dataset) - 1) + ' instances \n\n')

        node = BuildTree(dataset, class_list)

        f.write('Reading test data from file ' + str(args.testset) + '\n')
        test_dataset = prepare_dataset(args.testset)[0]
        f.write('Read ' + str(len(test_dataset) - 1) + ' instances \n')
        test_accuracy = get_accuracy(test_dataset, node, f)

        f.write('\n')
        f.write('Accuracy: \n')
        print('Decision Tree Accuracy: ' + str(test_accuracy) + '%.')
        f.write('Decision Tree Accuracy: ' + str(test_accuracy) + '%.\n')
        
        #baseline accuracy
        baseline_class = get_baseline_class(dataset)
        test_accuracy = get_baseline_accuracy(test_dataset, baseline_class)
        print('Baseline Accuracy (' + baseline_class + '): '  + str(test_accuracy) + '%.\n\n')
        f.write('Baseline Accuracy (' + baseline_class + '): '  + str(test_accuracy) + '%.\n\n')
        
        print('Apply decision tree classifier to 10 pairs of training/test files:')
        f.write('Apply decision tree classifier to 10 pairs of training/test files:\n')
        acc = 0
        for i in range(1,11):
            (dataset, class_list) = prepare_dataset('hepatitis-training-run' + str(i) + '.dat')
            node = BuildTree(dataset, class_list)
            test_dataset = prepare_dataset('hepatitis-test-run' + str(i) + '.dat')[0]
            test_accuracy = get_accuracy(test_dataset, node, f)
            acc += test_accuracy
            print('Accuracy of run ' + str(i) + ' is: ' + str(test_accuracy) + '%.')
            f.write('Accuracy of run ' + str(i) + ' is: ' + str(test_accuracy) + '%.\n\n')
        avg_acc = round(float(acc/10),2)
        print('The average accuracy of the classifiers over the 10 trials is: '+ str(avg_acc) + '%.')
        f.write('The average accuracy of the classifiers over the 10 trials is: '+ str(avg_acc) + '%.\n\n')

        f.write('Decision Tree constructed: \n')
        node.report('\t', f)
Main()
