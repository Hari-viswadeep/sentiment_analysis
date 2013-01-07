# CS 205 Final Project - Sentiment Analysis
## 

###Authors

* Tunde Agboola
* Omar Shammas
* Shashank Sunkavalli


###Description

A sentiment analysis tool that will output a rating between 1 (negative) and 5 (positive) for a given text. A random forest classifier is built using MPI and trained on the Yelp academic dataset, which was pre-processed using MapReduce. The dataset consisted of ~300,000 annotated reviews and was split into a training corpus and testing corpus (in a 4:1 ratio). All the data is in the folder 'data'.

## Code

### Phase 1: Preprocessing Using MapReduce

The code can be found in the mapreduce folder. MapReduce was used to extract the desired features from the training and testing data. The feature set consists of :
	
* One-Gram scores 
* One-Gram count
* Bi-Gram score
* Bi-Gram count
* Positive Word count
* Negative Word count
* Character count
* Count of Uppercase letters
* Count of Lowercase letters
* Count of punctuation characters
* Count of alphabets
* Count of numbers
* Ratio of Uppercase to Lowercase characters
* Ratio of Alphabets to Total Character count

The One-gram and Bi-gram scores for the text are calculated based on an index of one-gram and bi-gram scores created using the entire training corpus.

### Phase 2: Training Random Forest Classifier

Code for this section can be found in train.py. Using the training data, a random forest classifier (group of decision trees) is created. First the training data given as input is sampled with replacement to create a random sample to train each decision tree. The number of decision trees, the threshold for purity of the feature, and the number of features used for splitting at each node of each decision tree is configurable. Once the random forest classifier is trained, it is saved in a serialized format for making predictions.

### Phase 3: Prediction

Code for this section can be found in accuracy.py. The test data is given as input for prediction to determine the accuracy of the classifier. The ouput contains the overall accuracy of predictions, and the number of instances for each time the difference between the predicted rating and the actual rating is 1, 2, 3 and 4.
