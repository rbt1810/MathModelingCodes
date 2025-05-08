##!/usr/bin/env python
'''
                      ::::::
                    :+:  :+:
                   +:+   +:+
                  +#++:++#++:::::::
                 +#+     +#+     :+:
                #+#      #+#     +:+
               ###       ###+:++#""
                         +#+
                         #+#
                         ###
'''
__author__ = "Alex Pujols"
__copyright__ = "Copyright 2020, Spacial and Temporal Analysis Project TIM-6110 wk1"
__credits__ = ["Alex Pujols"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Alex Pujols"
__email__ = "alex.pujols@gmail.com"
__status__ = "Prototype"

'''
Title	      :	{TBD}
Date		  :	{XX-XX-20XX}
Description   :	{TBD}
Options	      :	{TBD}
Notes	      :	{TBD}
'''

# Import modules declarations
from random import randint
from collections import Counter
from memory_profiler import memory_usage
from time import sleep
import heapq
import timeit

# Function declarations

# Function to test for valid input and convert to int for further processing
def input_validate():
    while True:
        try:
            validate = int(input(": "))
            break
        except:
            print ("Incorrect value! Please make a new selection")
    return validate
# Function to perform bubble sort
def bubble_sort(array):
    n = len(array)
    for i in range(n):
        # Is this already sorted? If so, move on
        already_sorted = True
        # Start the sort
        for j in range(n - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                already_sorted = False
        # If there are no more sorts we are done
        if already_sorted:
            break
    return array
# Function to perfom insertion sort
def insertion_sort(array):

    for i in range (1, len(array)):
        key_item = array[i]
        # Find the correct position
        j = i - 1
        # Run through the list and find correct position
        # referenced by key_item.  Only do this if key_item
        # is smaller than adjacent value
        while j >= 0 and array[j] > key_item:
            # Shift value one position to the left and
            # reposition j to point to the next element
            array[j + 1] = array[j]
            j -= 1
        # When finished shifting elements, position key_item
        # in its correct location
        array[j + 1] = key_item
    return array
# Function to perfom quicksort
def quicksort(array):
    n = len(array)
    # Should we continue
    if n < 2:
        return array
    # Establish current placement
    pivot = 0
    # Begin sorting values into temporary arrays
    for i in range(1, n):
        if array[i] <= array [0]:
            pivot += 1
            temp = array[i]
            array[i] = array[pivot]
            array[pivot] = temp
    # Reset where appropriate prior to recursive calls
    temp = array[0]
    array[0] = array[pivot]
    array[pivot] = temp
    # Make recursive calls to call left and right sorts
    left = quicksort(array[0:pivot])
    right = quicksort(array[pivot+1:n])
    # Assemble sorted array and return back to main function
    array = left + [array[pivot]] + right
    return array
# Function to determine entry frequency of an array or heap
def most_frequent(data):
    elements_count = Counter(data)
    # Return frequency counts
    return elements_count.most_common(10)
# Main code begins

# Set globals
samples = 5 # How many samples to take leveraging timeit

while True:
    print ("\n\n")
    print ("Hi, which type of analysis would you like to run?")
    print ("1 - Spacial analysis")
    print ("2 - Temporal analysis")
    print ("0 - EXIT")

    # Take user input and validate
    selection = input_validate()

    #If user selects spacial analysis
    if (selection == 1):
        print ("\n You selected spacial analysis \n")
        print ("What is the size of the array you wish to create?")
        size = input_validate()
        # Select sorting algorithm
        print ("\n What type of sorting algorithm would you like to apply?")
        print ("1 - Bubble sort")
        print ("2 - Quicksort")
        print ("3 - Insertion sort")
        algorithm = input_validate()
        # If user selects bubble sort
        if (algorithm == 1):
            spacArray = [randint(1, 10000) for i in range(size)]
            print ("\n AFTER \n", spacArray)
            times = timeit.repeat("bubble_sort(spacArray)", setup="from __main__ import bubble_sort, spacArray", number=samples)
            print ("\n AFTER \n", spacArray)
            print ("\n The minimum time to execute across ", samples, " samples was: ", min(times))
        # If user selects insertion sort
        if (algorithm == 2):
            spacArray = [randint(1, 10000) for i in range(size)]
            print ("\n AFTER \n", spacArray)
            times = timeit.repeat("insertion_sort(spacArray)", setup="from __main__ import insertion_sort, spacArray", number=samples)
            print ("\n AFTER \n", spacArray)
            print ("\n The minimum time to execute across ", samples, " samples was: ", min(times))
        # If user selects quicksort
        if (algorithm == 3):
            spacArray = [randint(1, 10000) for i in range(size)]
            print ("\n BEFORE \n", spacArray)
            times = timeit.repeat("quicksort(spacArray)", setup="from __main__ import quicksort, spacArray", number=samples)
            print ("\n AFTER \n", spacArray)
            print ("\n The minimum time to execute across ", samples, " samples was: ", min(times))
    #If user selects temporal analysis
    if (selection == 2):
        print ("\n You selected temporal analysis! \n")
        print ("What is the size of the array you wish to create?")
        size = input_validate()
        # Select action to Take
        print ("How would you like to count the frequency of occurances?")
        print ("1 - Via array structure")
        print ("2 - Via heap structure")
        structure = input_validate()
        # If user selects temporal array sort
        if (structure == 1):
            tempArray = [randint(1, 10000) for i in range(size)]
            # Use the collections module counter class to count elements of the arrazy
            print(most_frequent(tempArray))
            # To turn on memory analysis and check spacial usage
            mem_usage = memory_usage((most_frequent, (tempArray,)))
            print ("\nMAX memory usage in MB: ",max(mem_usage))
        # If user selects temporal heap
        if (structure == 2):
            tempArray = [randint(1, 10000) for i in range(size)]
            # Create heap
            heapq.heapify(tempArray)
            # Use the collections module counter class to count elements of the arrazy
            print (most_frequent(tempArray))
            # To turn on memory analysis and check spacial usage
            mem_usage = memory_usage((most_frequent, (tempArray,)))
            print ("\nMAX memory usage in MB: ",max(mem_usage))
    #If user selects exit
    if (selection == 0):
        print ("\n You have chosen to leave the program.  Goodbye! \n")
        break
