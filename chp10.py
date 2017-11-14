def addall(l):
    i=0
    total = 0
    for i in range(len(l)):
        if type(l[i]) == list:
            for j in l[i]:
                total += j
        else:
            total += l[i]
    print(total)


addall([[1,2],[3,4],5])


# 10.4
def middle(list):
    new = []
    if len(list)>1:
        new = list[1:len(list)-1]
    return new


print(middle([1,2,3,4]))


# 10.6
def is_sorted(array):
    i=0
    for i in range(len(array)-1):
        if array[i] > array[i+1]:
            return False
    return True


print(is_sorted(['c','b']))


# 10.7
def anagrams(w1,w2):
    if len(w1) == len(w2):
        for char in w1:
            if char not in w2:
                return False
        return True

    else:
        return False


print(anagrams('mad','dam'))