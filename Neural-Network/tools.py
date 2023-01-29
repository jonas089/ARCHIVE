import random
def randomize():
    return random.uniform(0,1)
def best_gen(data):
    best_gen = data[0]
    for i in range(0, len(data)):
        if data[i][1]['rounds'] > best_gen[1]['rounds']:
            best_gen = data[i]
    return best_gen
