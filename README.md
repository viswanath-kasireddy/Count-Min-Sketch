# Count-Min-Sketch

Count min sketches are probabilistic data structures that allow a user to count how many times an element has appeared in a time and space efficient manner. Count min sketches have a wide variety of applications such as Internet traffic analysis, database monitoring, and more. As it is a probabilistic data structure, count min sketches can occasionally return inflated/slightly inaccurate results in the form of false positives, something our code will explore. However, count min sketches will never return a false negative. If an element was not counted, a count min sketch will always be accurate in telling us so. 

Count min sketches can be viewed in terms of the number of hashes used to run our information through, as well as how many filters we are using to store this information. Every value in our filters will originally be set to 0, but as an element is counted, the value corresponding to our hashed result will increase by 1. At the end, we can simply check to see how many times a chosen element was counted. Each row or filter is associated with a different hash function.

Given a count min sketch of size w x d (where d is the number of filters and w is the size of each filter, and a total of N elements, our error rate has a lower bound of 1 - ((½)^d) and an upper bound of 2N/W

In our problem we are attempting to demonstrate the extent to which a count min sketch will display false positives. To do this we are first manually counting words in two text examples. Then, we will compare this to using our count min sketch to count words, and then visualize our results. 
