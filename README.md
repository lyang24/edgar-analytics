# My Solution to Edgar Analytics

### environment - python 3.6 & tested on ubuntu 17.10 and mac.
### packages - os, collections, logging, datetime, contextlib, csv (all come with python)
### assumptions - input data stream in timeline old once a second finished it will not appear again
1. create a class to hold and retrieve session values.
2. determine when should we remove sessions from the queue:
    1. criteria 1 - new session appeared after the timestamp gap
    2. criteria 2 - create a set to hold unique timestamps if uniques - 1 > then timeout dump all in dict with expired timestamp.
    3. criteria 3 - once reading from file is complete dump everything from queue.

### Instruction to run:
* git clone this repo
* ./run.sh

### Future improvements
* looking in to criteria 2's logic and come up with optimal algorithms.
* research into shell scripting to make ./run_test.sh work properly


# update
# now that i am looking back i should probably use a deque like data structure to solve this problem since the question constantly involves pollFirst and OfferLast Deque has these operations at the cost of o(1)
