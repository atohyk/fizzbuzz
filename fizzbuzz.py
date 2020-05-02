import timeit

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

def opt1(n):
    rep = basic(15)
    retval = list(rep)
    for i in range(1,int(n/15)):
        retval += list(map(lambda x:x+i*15 if isinstance(x,int) else x,rep))
    retval += list(map(lambda x:x+(i+1)*15 if isinstance(x,int) else x,rep[:n%15]))

    return retval

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

def opt3(n):
    rep = basic(15)
    retval = list(rep*(int(n/15))+rep[:n%15])
    for i in range(len(retval)):
        if isinstance(retval[i],int):
            retval[i] = i+1
    return retval

def opt4(n):
    rep = [1, 1, 'fizz', 1, 'buzz', 'fizz', 1, 1, 'fizz', 'buzz', 1, 'fizz', 1, 1, 'fizzbuzz']
    retval = list(rep*(int(n/15))+rep[:n%15])
    retval = [i+1 if retval[i] == 1 else retval[i] for i in range(n) ]
    return retval

if __name__ == '__main__':
    print('Testing for Correctness')
    print('basic(50):',basic(50)) # for manual verification
    a=basic(1000) # we know this to be true
    if a==opt1(1000):
        print('Opt1 correct.')
    if a==opt2(1000):
        print('Opt2 correct.')
    if a==opt3(1000):
        print('Opt3 correct.')
    if a==opt4(1000):
        print('Opt4 correct.')

    print('Time taken for basic(10000): ', timeit.timeit(lambda: basic(10000), number=100))
    print('Time taken for opt1(10000): ', timeit.timeit(lambda: opt1(10000), number=100))
    print('Time taken for Opt2(10000): ', timeit.timeit(lambda: opt2(10000), number=100))
    print('Time taken for opt3(10000): ', timeit.timeit(lambda: opt3(10000), number=100))
    print('Time taken for opt4(10000): ', timeit.timeit(lambda: opt4(10000), number=100))
