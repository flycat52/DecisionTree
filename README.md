# DecisionTree

## Problem Description
The main data set for the DT program is in the files hepatitis.dat, hepatitis-training.dat, and hepatitis-testing.dat. It describes 137 cases of patients with hepatitis, along with the outcome. Each case is specified by 16 Boolean attributes describing the patient and the results of various tests. The goal is to be able to predict the outcome based on the attributes. The first file contains all the 137 cases; the training file contains 110 of the cases (chosen at random) and the testing file contains the remaining 27 cases. The data files are formatted as tab-separated text files, containing two header lines, followed by a line for each instance.
- The first line contains the names of the two classes.
- The second line contains the names of the attributes.
- Each instance line contains the class name followed by the values of the attributes (“true” or “false”).

This data set is taken from the UCI Machine Learning Repository http://mlearn.ics.uci.edu/MLRepository.html. It consists of data about the prognosis of patients with hepatitis. This version has been simplified by removing some of the numerical attributes, and converting others to booleans.

## Requirements
Your program should take two file names as command line arguments, construct a classifier from the training data in the first file, and then evaluate the classifier on the test data in the second file.

1. You should first apply your program to the hepatitis-training.dat and hepatitis-test.dat files and report the classification accuracy in terms of the fraction of the test instances that it classified correctly. Report the learned decision tree classifier printed by your program. Compare the accuracy of your Decision Tree program to the baseline classifier which always predicts the most frequent class in the dataset, and comment on any difference.
2. You should then construct 10 other pairs of training/test files, train and test your classifiers on each pair, and calculate the average accuracy of the classifiers over the 10 trials. There is a script split-datafile that takes the name of the full data set (eg, hepatitis), the number of training instances, and a suffix for the filenames, and will construct pairs of training and test files. For example `./split-datafile hepatitis.dat 100 run1` will construct the files hepatitis-training-run1.dat and hepatitis-test-run1.dat with 100 and 37 instances respectively. This process need to run 10 times.

## Prerequisite
- Python 3.6 or higher
- Please keep all the related data files in the same folder (i.e.part2).

## Running Steps
1. Open Terminal console
2. Go to the project part2 directory
3. Run command: python DT.py hepatitis-training.dat hepatitis-test.dat 
4. An output file (sampleoutput.txt) will be generated in the same project folder. Check it for the result.

