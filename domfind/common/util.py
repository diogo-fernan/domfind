import random as rand


def shuffle(n):
    for i in range(len(n)):
        if rand.random() > .5:
            j = int(rand.random() * len(n))
            n[i], n[j] = n[j], n[i]
    return n
