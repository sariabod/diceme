import random
from collections import Counter




def roll_dice(n):
    results = []
    for x in range(n):
        results.append(random.randint(1,6))

    return Counter(results)





