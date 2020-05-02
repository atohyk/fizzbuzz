# fizzbuzz
An exploration of potential solutions and optimizations to the popular fizzbuzz problem in Python.

# Introduction
The fizzbuzz problem is a simple one - given a number **n**, return a list from **1 to n** where any number that is divisible by **3** is changd to **fizz** and any number that is divisible by **5** is changed to **buzz**. Any number that is divisible by **both 3 and 5** is changed to **fizzbuzz**.

The goal is to write a function that takes in 1 argument, **n**, and returns a list of numbers and/or strings that correspond to the above rules.

An example would be:
>fizzbuzz(15) = [1, 2, 'fizz', 4, 'buzz', 'fizz', 7, 8, 'fizz', 'buzz', 11, 'fizz', 13, 14, 'fizzbuzz']

# Running
Execute ```fizzbuzz.py``` with python3:
```sh
python3 fizzbuzz.py
```
Example output:
```sh
basic(50): [1, 2, 'fizz', 4, 'buzz', 'fizz', 7, 8, 'fizz', 'buzz', 11, 'fizz', 13, 14, 'fizzbuzz', 16, 17, 'fizz', 19, 'buzz', 'fizz', 22, 23, 'fizz', 'buzz', 26, 'fizz', 28, 29, 'fizzbuzz', 31, 32, 'fizz', 34, 'buzz', 'fizz', 37, 38, 'fizz', 'buzz', 41, 'fizz', 43, 44, 'fizzbuzz', 46, 47, 'fizz', 49, 'buzz']
Opt1 correct.
Opt2 correct.
Opt3 correct.
Opt4 correct.
Time taken for basic(10000):  0.1860354050004389
Time taken for opt1(10000):  0.19396261300425977
Time taken for Opt2(10000):  0.1783163729996886
Time taken for opt3(10000):  0.1424795780039858
Time taken for opt4(10000):  0.09713343801558949
```

# Basic Algorithm
There are numerous articles on the basic fizzbuzz algorithm implemented in python:
 - https://medium.com/@GalarnykMichael/python-basics-8-fizzbuzz-441e97c6c767
 - https://www.w3resource.com/python-exercises/python-conditional-exercise-10.php
 - https://www.blog.pythonlibrary.org/2019/09/18/python-code-kata-fizzbuzz/

The basic concept is to first test if the number is divisible by both 3 and 5, and then subsequently if it is divisible by 3 only and 5 only:
```sh
def basic(n):
    retval=[]
    for i in range(1,n+1):
        if (i % 3 == 0 and i % 5 == 0):
            retval += ['fizzbuzz']
        elif (i % 3 == 0):
            retval += ['fizz']
        elif (i % 5 == 0):
            retval += ['buzz']
        else:
            retval += [i]
    return retval
```
```Score: 0.1860354050004389``` (lower is better)

# Optimization
The two main objectives of optimization in our case are purely time and memory, while keeping the code relatively readable and pythonic.
### Optimization 1
Building on the basic solution, this function takes advantage of the fact that the fizzbuzz pattern is repeated every 15 elements, only the numbers change.
- Get the first 15 elements
- Store first 15 into output list
- Construct next 15 elements by replacing only numbers with a new (larger) number
- Add newly constructed list to output list
- Keep adding n/15 times
- Finally add on the remainder of the list
```sh
def opt1(n):
    rep = basic(15)
    retval = list(rep)
    for i in range(1,int(n/15)):
        retval += list(map(lambda x:x+i*15 if isinstance(x,int) else x,rep))
    retval += list(map(lambda x:x+(i+1)*15 if isinstance(x,int) else x,rep[:n%15]))
    return retval
```
for example:
>[1, 2, 'fizz', 4, 'buzz', 'fizz', 7, 8, 'fizz', 'buzz', 11, 'fizz', 13, 14, 'fizzbuzz'] +
>[16, 17, 'fizz', 19, 'buzz', 'fizz', 22, 23, 'fizz', 'buzz', 26, 'fizz', 28, 29, 'fizzbuzz'] + ...

```Score: 0.19396261300425977``` (lower is better)

Interestingly, we see from the results that this optimization actually makes things worse - it is entirely possible that it is expensive to create/join lists in python, and this could be the cause of the delay.
### Optimization 2
Building on the previous solution, this function constructs the list upfront, and loops through the list checking for "fizzbuzz", which is the "marker" for every 15 elements.
- Get the first 15 elements
- Construct output list based on repeating the basic list
- Iterate through the output list and add to the numerical elements accordingly by a multiple of 15
- Everytime a "fizzbuzz" is encountered, incremement the 15-multiplier by 1
```sh
def opt2(n):
    rep = basic(15)
    retval = list(rep*(int(n/15))+rep[:n%15])
    loopcount = 0
    for i in range(len(retval)):
        if isinstance(retval[i],int):
            retval[i] += loopcount*15
        elif retval[i] == 'fizzbuzz':
            loopcount+=1
    return retval
```
Here we start to see better times, but only marginally so.
```Score: 0.1783163729996886``` (lower is better)
### Optimization 3
Building on the previous idea, why do we not instead assign the loop variable to anything that is a number as we go through the list? In this way, we do not have to check for any "fizzbuzz"s, nor do any multiplication/addition etc.
- Get the first 15 elements
- Construct output list based on repeating the basic list
- Iterate through the output list using an index, if an element is a number, assign the current index + 1 to it
```sh
def opt3(n):
    rep = basic(15)
    retval = list(rep*(int(n/15))+rep[:n%15])
    for i in range(len(retval)):
        if isinstance(retval[i],int):
            retval[i] = i+1
    return retval
```
By not checking for "fizzbuzz"s and not doing addition/multiplication, we save even more time!
```Score: 0.1424795780039858``` (lower is better)
### Optimization 4
Actually, we don't even have to use the original basic list - 15 elements is trivial for us to write out and generate by hand. Instead of testing if a value is an integer and using a for loop to iterate, we could use list comprehension instead, which is generally faster in python.
- Create original list with placeholders for numbers to be replaced (in the code, this is a **1**)
- Generate output list of correct length with repeating fizzbuzz pattern
- Use list comprehension to replace anything that is a **1** with the index **i**
```sh
def opt4(n):
    rep = [1, 1, 'fizz', 1, 'buzz', 'fizz', 1, 1, 'fizz', 'buzz', 1, 'fizz', 1, 1, 'fizzbuzz']
    retval = list(rep*(int(n/15))+rep[:n%15])
    retval = [i+1 if retval[i] == 1 else retval[i] for i in range(n) ]
    return retval
```
By using list comprehension, we save even more time!
```Score: 0.09713343801558949``` (lower is better)

# Summary
As can be seen from the first iteration, an optimization in theory may not lead to a saving in reality, and there is a significant amount of overhead especially when working with an interpreted language such as Python. Overall, we managed to reduce the amount of time needed from ```0.186035``` to ```0.097133```, by taking advantage of the structure of the problem and improving the implementation.
