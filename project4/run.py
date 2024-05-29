class Solution:
    def isPerfectSquare(self, num):
        l=1
        r=num
        while(l<=r):
            mid = l+int((r-l)/2)
            if(mid*mid==num):
                return True
            elif (mid*mid>num):
                r=mid-1
            else:
                l=mid+1
        
        return False
"""   
class Solution:
    def twoSum(self, nums, target):
        n = len(nums)
        for i in range(n-1):
            for j in range(i+1,n):
                if nums[i] + nums[j] == target:
                    return [i, j]
        
        return []
"""
class Solution:
    def twoSum(self, nums, target):
        numMap={}
        n=len(nums)
        for i in range(n):
            compliment = target-nums[i]
            if(compliment in numMap):
                return [i, numMap[compliment]]
            numMap[nums[i]]=i
        return []
    def longestCommonPrefix(self, strs: list[str]) -> str:
        pref = strs[0]
        pref_len = len(pref)
        for s in strs[1:]:
            while pref != s[0:pref_len]:
                pref_len = pref_len-1
                if pref_len == 0:
                    return ""
                pref = pref[0:pref_len]
            
        return pref


for i in range(10):
    print(i)

from typing import List, Dict

students: List[Dict[str, int]] = [
    {"name": 2},
    {"name": 1}
]
print(students)


class Solution:
    def removeDuplicates(self, nums) -> int:
        i = 0 
        while i < len(nums) - 1:  
            if nums[i] == nums[i + 1]:
                print(nums[i + 1])  
                nums.pop(i + 1)  #remove an element from the list based on the index 
            else:
                i += 1  

        return len(nums)  
    
    def lengthOfLastWord(self, s: str) -> int:
        words = s.strip().split()
        
        if not words:
            return 0
        
        return len(words[-1])

from typing import Optional

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        if root is None:
            return True
    

if __name__ == "__main__":
    s= Solution()

import heapq

# Example list
numbers = [4, 2, 9, 1, 5, 6]

# Transform the list into a heap
heapq.heapify(numbers)

print(numbers)  # Output: [1, 2, 6, 4, 5, 9] (elements are reordered to satisfy heap property)

heapq.heappush(numbers, 3)

print(numbers)  # Output: [1, 2, 6, 4, 5, 9, 3]

smallest = heapq.heappop(numbers)

print(smallest)  # Output: 1
print(numbers)  # Output: [2, 3, 6, 4, 5, 9]

import heapq

class MaxHeap:
    def __init__(self):
        self._heap = []

    def push(self, value):
        # Negate the value to simulate max-heap behavior
        heapq.heappush(self._heap, -value)

    def pop(self):
        # Negate the value again to get the original value
        return -heapq.heappop(self._heap)

    def peek(self):
        # Return the negated value of the smallest element
        return -self._heap[0]

    def __len__(self):
        # Return the number of elements in the heap
        return len(self._heap)

# Example usage
max_heap = MaxHeap()
max_heap.push(4)
max_heap.push(2)
max_heap.push(9)
max_heap.push(1)

print(max_heap.pop())  # Output: 9
print(max_heap.pop())  # Output: 4
print(max_heap.pop())  # Output: 2
print(max_heap.pop())  # Output: 1


# https://www.learnpython.org/en/Modules_and_Packages
import sys
sys.path.append("/lib1")
import numpy as np
arr = np.array([1,2,3])
arr_plus_10 = arr + 10
print("Array after adding 10: ", arr_plus_10)
x =1
if x==1:
    print("x is 1")
else:
    print("x is 2")
    
mylist =[]
mylist.append(1)
mylist.append(7.6)
mylist.append("string")
for x in mylist:
    print(x)
    
print(" is %s" % mylist[0])
print(mylist.count(1))
print(len(mylist))

class MyClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def display_info(self):
        print(f"Name: {self.name}")

person = MyClass("John",30)
person.display_info()

even_numbers = [2,4,6,8]
odd_numbers = [1,3,5,7]
all_numbers = odd_numbers + even_numbers
print(all_numbers)

print([1,2,3] * 3)

for i in range(5):  # Generates numbers from 0 to 4
    print(i)
    
    
# This prints out "John is 23 years old."
name = "John"
age = 23
print("%s is %d years old." % (name, age))


mylist = [1,2,3]
print("A list: %s" % mylist)


astring = "Hello world!"
print(astring.index("o"))


astring = "Hello world!"
print(astring.count("l"))

astring = "Hello world!"
print(astring[3:7])

# Python3 program to print DFS traversal
# from a given graph
from collections import defaultdict


# This class represents a directed graph using
# adjacency list representation
class Graph:

	# Constructor
	def __init__(self):

		# Default dictionary to store graph
		self.graph = defaultdict(list)

	
	# Function to add an edge to graph
	def addEdge(self, u, v):
		self.graph[u].append(v)

	
	# A function used by DFS
	def DFSUtil(self, v, visited):

		# Mark the current node as visited
		# and print it
		visited.add(v)
		print(v, end=' ')

		# Recur for all the vertices
		# adjacent to this vertex
		for neighbour in self.graph[v]:
			if neighbour not in visited:
				self.DFSUtil(neighbour, visited)

	
	# The function to do DFS traversal. It uses
	# recursive DFSUtil()
	def DFS(self, v):

		# Create a set to store visited vertices
		visited = set()

		# Call the recursive helper function
		# to print DFS traversal
		self.DFSUtil(v, visited)


# Driver's code
if __name__ == "__main__":
	g = Graph()
	g.addEdge(0, 1)
	g.addEdge(0, 2)
	g.addEdge(1, 2)
	g.addEdge(2, 0)
	g.addEdge(2, 3)
	g.addEdge(3, 3)

	print("Following is Depth First Traversal (starting from vertex 2)")
	
	# Function call
	g.DFS(2)

# This code is contributed by Neelam Yadav

# Python3 function to search a given key in a given BST

class Node:
	# Constructor to create a new node
	def __init__(self, key):
		self.key = key
		self.left = None
		self.right = None

# A utility function to insert
# a new node with the given key in BST
def insert(node, key):
	# If the tree is empty, return a new node
	if node is None:
		return Node(key)

	# Otherwise, recur down the tree
	if key < node.key:
		node.left = insert(node.left, key)
	elif key > node.key:
		node.right = insert(node.right, key)

	# Return the (unchanged) node pointer
	return node

# Utility function to search a key in a BST
def search(root, key):
	# Base Cases: root is null or key is present at root
	if root is None or root.key == key:
		return root

	# Key is greater than root's key
	if root.key < key:
		return search(root.right, key)

	# Key is smaller than root's key
	return search(root.left, key)

# Driver Code
if __name__ == '__main__':
	root = None
	root = insert(root, 50)
	insert(root, 30)
	insert(root, 20)
	insert(root, 40)
	insert(root, 70)
	insert(root, 60)
	insert(root, 80)

	# Key to be found
	key = 6

	# Searching in a BST
	if search(root, key) is None:
		print(key, "not found")
	else:
		print(key, "found")

	key = 60

	# Searching in a BST
	if search(root, key) is None:
		print(key, "not found")
	else:
		print(key, "found")




name = "John"
age = 23
if name == "John" and age == 23:
    print("Your name is John, and you are also 23 years old.")

if name == "John" or name == "Rick":
    print("Your name is either John or Rick.")
    

name = "John"
if name in ["John", "Rick"]:
    print("Your name is either John or Rick.")
    
    
statement = False
another_statement = True
if statement is True:
    # do something
    pass
elif another_statement is True: # else if
    # do something else
    pass
else:
    # do another thing
    pass


count = 0
while True:
    print(count)
    count += 1
    if count >= 5:
        break

# Prints out only odd numbers - 1,3,5,7,9
for x in range(10):
    # Check if x is even
    if x % 2 == 0:
        continue
    print(x)
    
    
class MyClass:
    variable = "blah"

    def function(self):
        print("This is a message inside the class.")
        
        


phonebook = {  
    "John" : 938477566,
    "Jack" : 938377264,
    "Jill" : 947662781
}  
# your code goes here
phonebook["Jake"] = 938273443
phonebook.pop("Jill")
# testing code
if "Jake" in phonebook:  
    print("Jake is listed in the phonebook.")
    
if "Jill" not in phonebook:      
    print("Jill is not listed in the phonebook.")
    
    

import re

# Your code goes here
find_members = []
for member in dir(re):
    if "find" in member:
        find_members.append(member)

print(sorted(find_members))


#Numpy and Pandas
height = [1.87,  1.87, 1.82, 1.91, 1.90, 1.85]
weight = [81.65, 97.52, 95.25, 92.98, 86.18, 88.45]

# Import the numpy package as np
import numpy as np

# Create 2 numpy arrays from height and weight
np_height = np.array(height)
np_weight = np.array(weight)

dict = {"country": ["Brazil", "Russia", "India", "China", "South Africa"],
       "capital": ["Brasilia", "Moscow", "New Dehli", "Beijing", "Pretoria"],
       "area": [8.516, 17.10, 3.286, 9.597, 1.221],
       "population": [200.4, 143.5, 1252, 1357, 52.98] }

import pandas as pd
brics = pd.DataFrame(dict)
print(brics)


# Advanced python

#Generator

import random

def lottery():
    # returns 6 numbers between 1 and 40
    for i in range(6):
        yield random.randint(1, 40)

    # returns a 7th number between 1 and 15
    yield random.randint(1, 15)

for random_number in lottery():
       print("And the next number is... %d!" %(random_number))
       
       
# try catch
def do_stuff_with_number(n):
    print(n)

def catch_this():
    the_list = (1, 2, 3, 4, 5)

    for i in range(20):
        try:
            do_stuff_with_number(the_list[i])
        except IndexError: # Raised when accessing a non-existing index of a list
            do_stuff_with_number(0)

catch_this()

#set

a = set(["Jake", "John", "Eric"])
b = set(["John", "Jill"])

print(a.intersection(b))
print(b.intersection(a))


print(set("my name is Eric and Eric is my name".split()))

#serialization with json
import json

# fix this function, so it adds the given name
# and salary pair to salaries_json, and return it
def add_employee(salaries_json, name, salary):
    salaries = json.loads(salaries_json)
    salaries[name] = salary

    return json.dumps(salaries)

# test code
salaries = '{"Alfred" : 300, "Jane" : 400 }'
new_salaries = add_employee(salaries, "Me", 800)
decoded_salaries = json.loads(new_salaries)
print(decoded_salaries["Alfred"])
print(decoded_salaries["Jane"])
print(decoded_salaries["Me"])


#Closure
# A closure occurs when:

# A nested (inner) function references variables from an enclosing scope.
# The enclosing function returns the nested function.
def transmit_to_space(message):
  "This is the enclosing function"
  def data_transmitter():
      "The nested function"
      print(message)
  return data_transmitter

fun2 = transmit_to_space("Burn the Sun!")
fun2()

# Decorator
def type_check(correct_type):
    def check(old_function):
        def new_function(arg):
            if (isinstance(arg, correct_type)):
                return old_function(arg)
            else:
                print("Bad Type")
        return new_function
    return check

@type_check(int)
def times2(num):
    return num*2

print(times2(2))
times2('Not A Number')

@type_check(str)
def first_letter(word):
    return word[0]

print(first_letter('Hello World'))
first_letter(['Not', 'A', 'String'])


#map
my_pets = ['alfred', 'tabitha', 'william', 'arla']

uppered_pets = list(map(str.upper, my_pets))

print(uppered_pets)



my_strings = ['a', 'b', 'c', 'd', 'e']
my_numbers = [1, 2, 3, 4, 5]

results = list(map(lambda x, y: (x, y), my_strings, my_numbers))


# filter
scores = [66, 90, 68, 59, 76, 60, 88, 74, 81, 65]

def is_A_student(score):
    return score > 75

over_75 = list(filter(is_A_student, scores))

print(over_75)
print(results)

# reduce
from functools import reduce

numbers = [3, 4, 6, 9, 34, 12]

def custom_sum(first, second):
    return first + second

result = reduce(custom_sum, numbers)
print(result)


#### Map
from functools import reduce 

my_floats = [4.35, 6.09, 3.25, 9.77, 2.16, 8.88, 4.59]
my_names = ["olumide", "akinremi", "josiah", "temidayo", "omoseun"]
my_numbers = [4, 6, 9, 23, 5]

map_result = list(map(lambda x: round(x ** 2, 3), my_floats))
filter_result = list(filter(lambda name: len(name) <= 7, my_names))
reduce_result = reduce(lambda num1, num2: num1 * num2, my_numbers)

print(map_result)
print(filter_result)
print(reduce_result)

# Example list of tuples
students = [("John", 22), ("Jane", 21), ("Dave", 25)]

# Sorting by the second element (age) of each tuple
students.sort(key=lambda student: student[1])

print(students)  # Output: [('Jane', 21), ('John', 22), ('Dave', 25)]

# Using sorted() with a custom key
students_sorted = sorted(students, key=lambda student: student[1], reverse=True)

print(students_sorted)  # Output: [('Dave', 25), ('John', 22), ('Jane', 21)]

for i in range(1,10):
    print(i)