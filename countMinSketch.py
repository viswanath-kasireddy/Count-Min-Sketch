# Python3 program Miller-Rabin randomized primality test
# Copied from geeksforgeeks: https://www.geeksforgeeks.org/primality-test-set-3-miller-rabin/
import random 

#Modular exponentiation
#Returns (x^y) % p
def power(x, y, p): 
	
    #Placeholder 
	res = 1; 
	

	x = x % p; 
	while (y > 0): 
		
        #If y is odd, multiply x with result 
		if (y & 1): 
			res = (res * x) % p; 

        #y is even now, divide by 2 with bit shifting, exponentiate x and modularize 
		y = y>>1; 
		x = (x * x) % p; 
	
	return res; 

#Miller-Rabin test to determine if n is prime
def miillerTest(d, n): 
	
    #Pick a random number in [2..n-2], making sure n > 4
	a = 2 + random.randint(1, n - 4); 

    #Calculate a^d % n 
	x = power(a, d, n); 

	if (x == 1 or x == n - 1): 
		return True; 

    # Keep squaring x while one of the following does not occur
    # (i) d does not reach n-1 
    # (ii) (x^2) % n is not 1 
    # (iii) (x^2) % n is not n-1 
	while (d != n - 1): 
		x = (x * x) % n; 
		d *= 2; 

		if (x == 1): 
			return False; 
		if (x == n - 1): 
			return True; 

    # Return overall 
	return False; 

#Probabalistic nature of the Miller-Rabin test means we call it for K trials to assess higher accuracy 
def isPrime( n, k): 
	
	# Corner cases 
	if (n <= 1 or n == 4): 
		return False; 
	if (n <= 3): 
		return True; 

    # Find r such that n = 2^d * r + 1 for some r >= 1 
	d = n - 1; 
	while (d % 2 == 0): 
		d //= 2; 

    #Run test k times
	for i in range(k): 
		if (miillerTest(d, n) == False): 
			return False; 

	return True; 

# Driver Code 
# Number of iterations 
k = 4; 

#Get a random triple (p, a, b) where p is prime and a and b are numbers betweeen 2 and p-1
def get_random_hash_function():
    n = random.getrandbits(64)
    if n < 0: 
        n = -n 
    if n % 2 == 0:
        n = n + 1
    while not isPrime(n, 20):
        n = n + 1
    a = random.randint(2, n-1)
    b = random.randint(2, n-1)
    return (n, a, b)

# hash function for a number
def hashfun(hfun_rep, num):
    (p, a, b) = hfun_rep
    return (a * num + b) % p

# hash function for a string.
def hash_string(hfun_rep, hstr):
    n = hash(hstr)
    return hashfun(hfun_rep, n)    

#Using the book "The Great Gatsby" and extracting all words that are 5 letters or longer
filename ='/Users/viswakasireddy/Downloads/great-gatsby-fitzgerald.txt'
file = open (filename,'r')
txt = file.read()
txt = txt.replace('\n',' ')
words= txt.split(' ')
longer_words_gg = list(filter(lambda s: len(s) >= 5, words))
print(len(longer_words_gg))
# Let us count the precise word frequencies
word_freq_gg = {}
for elt in longer_words_gg:
    if elt in word_freq_gg:
        word_freq_gg[elt] += 1
    else:
        word_freq_gg[elt] = 1
        #print(len(word_freq_gg))




#Using the book "War and Peace" and extracting all words that are 5 letters or longer
filename = '/Users/viswakasireddy/Downloads/war-and-peace-tolstoy.txt'
file = open (filename,'r')
txt = file.read()
txt = txt.replace('\n',' ')
words= txt.split(' ')
longer_words_wp = list(filter(lambda s: len(s) >= 5, words))
print(len(longer_words_wp))
word_freq_wp = {}
for elt in longer_words_wp:
    if elt in word_freq_wp:
        word_freq_wp[elt] += 1
    else:
        word_freq_wp[elt] = 1
        #print(len(word_freq_wp))

#Class for implementing a count min sketch "single bank" of counters
class CountMinSketch:
    # Initialize with `num_counters`
    def __init__ (self, num_counters):
        self.m = num_counters
        self.hash_fun_rep = get_random_hash_function()
        self.counters = [0]*self.m
    
        #self.wordlist = {}
        self.list1 = []
        self.list1 = get_random_hash_function()
    
    
    #Given a word, increment its count in the countmin sketch
    def increment(self, word):
        n = hash_string(self.list1,word)
        column = n % self.m
        if self.counters[column] == 0:
            self.counters[column] = 1
        else:
            self.counters[column] += 1
        
        
    #Given a word, get its approximate count
    def approximateCount(self, word):

        n = hash_string(self.list1,word)
        column = n % self.m
        return self.counters[column]


#Initialize k different counters
def initialize_k_counters(k, m): 
    return [CountMinSketch(m) for i in range(k)]

#Increment each of the individual counters with the word
def increment_counters(count_min_sketches, word):
    for i in range(len(count_min_sketches)):
        count_min_sketches[i].increment(word)
    
        
#Get the approximate count by querying each counter bank and taking the minimum
def approximate_count(count_min_sketches, word):
    return min([cms.approximateCount(word) for cms in count_min_sketches])


#%matplotlib inline
from matplotlib import pyplot as plt 

#Great Gatsby example
cms_list = initialize_k_counters(5, 1000)
for word in longer_words_gg:
    increment_counters(cms_list, word)

discrepancies = []
count, count1 = 0,0
for word in longer_words_gg:
    l = approximate_count(cms_list, word)
    r = word_freq_gg[word]
    assert ( l >= r)
    if l >= r:
        count +=1
    if l > r:
        count1 +=1

    discrepancies.append( l-r )
    
plt.hist(discrepancies)
plt.show()
print ('counts')
print (count)
print (count1)

assert(max(discrepancies) <= 200), 'The largest discrepancy will have a high probability of being less than 200.'

#War and Peace example
#Bigger dimensions
cms_list = initialize_k_counters(5, 5000)
for word in longer_words_wp:
    increment_counters(cms_list, word)

discrepancies = []
for word in longer_words_wp:
    l = approximate_count(cms_list, word)
    r = word_freq_wp[word]
    assert ( l >= r)
    discrepancies.append( l-r )

plt.hist(discrepancies)
plt.show()