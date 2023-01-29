import tools
data = []

class Neural_Network():
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
    def Decide(self, EA, EN):
        weight_EA = EA * self.a + EN * self.c
        weight_EN = EA * self.b + EN * self.d
        if weight_EA > weight_EN:
            return "Eat"
        elif weight_EN > weight_EA:
            return "Nest"
        else:
            return "DRAW"
class Simulation():
    def __init__(self, EA, EN, creatures, neural_network):
        self.EA = EA
        self.EN = EN
        self.creatures = creatures
        self.neural_network = neural_network
    def run_simulation(self):
        rounds = 0
        while self.creatures > 0:
            decision = self.neural_network.Decide(self.EA, self.EN)
            if decision == "Eat":
                self.EA -= 1
            elif decision == "Nest":
                self.EA -= 1
                self.EN += 1
                self.creatures -= 1
            else:
                self.EA -= 1
            if self.EA <= 0:
                self.creatures -= 1
            if self.EN <= 0:
                #print("Nest ran out of Energy.")
                break

            #print("[ROUNDS]: " + str(rounds))
            #print("[STATE]: ", str(self.EN), ' : ', str(self.creatures))
            rounds += 1
        #print("!!! [Generation Survived]: ", str(rounds))
        data.append(len(data))
        data[len(data) - 1] = [len(data) - 1, {'model_a':self.neural_network.a, 'model_b':self.neural_network.b, 'model_c':self.neural_network.c, 'model_d':self.neural_network.d, 'rounds':rounds}]
for u in range(0, 100):
    n = Neural_Network(tools.randomize(), tools.randomize(), tools.randomize(), tools.randomize())
    s = Simulation(100,100,10,n)
    s.run_simulation()
print(tools.best_gen(data))
