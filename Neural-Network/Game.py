from minesweeper import Neural_Network
from minesweeper import Player
from minesweeper import Field
from minesweeper import Mine

import tools
import time

def Play(n,p,f):
    rounds = 0
    while p.is_alive(f.minefield) == True:
        D = n.Decide(p.x,p.y,f.width,f.height)
        if D == 0: # Move left
            p.move(-1,0)
            n.track.append(len(n.track))
            n.track[len(n.track) - 1] = [-1,0]
            new_mine = Mine(p.x + 1, p.y)

        elif D == 1: # Move Right
            p.move(1,0)
            n.track.append(len(n.track))
            n.track[len(n.track) - 1] = [1,0]
            new_mine = Mine(p.x - 1, p.y)

        elif D == 2: # Move Up
            p.move(0,1)
            n.track.append(len(n.track))
            n.track[len(n.track) - 1] = [0,1]
            new_mine = Mine(p.x, p.y - 1)
        elif D == 3: # Move Down
            p.move(0,-1)
            n.track.append(len(n.track))
            n.track[len(n.track) - 1] = [0,-1]
            new_mine = Mine(p.x, p.y + 1)
        else:
            print("[Error]: Invalid D: " + str(D))
            return 0
        f.minefield.append(len(f.minefield))
        f.minefield[len(f.minefield) - 1] = new_mine
        rounds += 1
    return rounds



#@jit(target ="cuda")
def Train():
    res = [-1,None,None]
    nr_mines = 5
    f = Field(5,5,nr_mines)
    f.plant_mines()
    for mine in f.minefield:
        print("Mine:" + str(mine.x) + ':' + str(mine.y))
    wait = input("Enter... ")
    timestamp = time.time()
    simcount = 0
    while (time.time()-timestamp < 60*1):
        n = Neural_Network(tools.randomize(), tools.randomize(), tools.randomize(), tools.randomize(), tools.randomize(), tools.randomize(), tools.randomize(), tools.randomize(), tools.randomize(), tools.randomize(), tools.randomize(), tools.randomize(), tools.randomize(), tools.randomize(), tools.randomize(), tools.randomize())
        p = Player(1,1,f.width,f.height)
        r = Play(n,p,f)
        if r > res[0]:
            print("RES UPDATED.")
            print("TIME: " + str(time.time()-timestamp))
            res = [r, n, f.minefield]
        f.minefield = f.minefield[:nr_mines]
        simcount += 1
    best = 0
    best_index = 0
    print(res)
    for mine in res[2]:
        print("Mine: " + str(mine.x) + ' : ' + str(mine.y))
    print("Track: " + str(res[1].track))
    print("Number of simulations: " + str(simcount))
    print(res[0])

Train()
