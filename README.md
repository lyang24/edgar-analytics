# My Solution to Edgar Analytics
### assumptions - input data stream in timeline old once a second finished it will not appear again
1. create a class to hold and retrive session values.
2. determine when should we remove sessions from the queue:
    1. criteria 1 - new session appeared after the timestamp gap
    2. criteria 2 - create a set to hold unique timestamps if uniques - 1 > then timeout dump all in dict with expired timestamp.
    3. criteria 3 - once reading from file is complete dump everything from queue.