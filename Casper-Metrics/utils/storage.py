import os
import pickle
class File:
    def __init__(self, path, name, type):
        self.filename = name
        self.name =  '{path}{name}.{type}'.format(path=path, name=name, type=type)
    def create(self):
        open(self.name, 'x')
    def read(self):
        with open(self.name, 'rb') as f:
            return pickle.load(f)
    def write(self, data):
        with open(self.name, 'wb') as f:
            pickle.dump(data, f)
            f.close()
    def add(self, data):
        x = self.read()
        x.append(data)
        self.write(x)


'''
def tests():
    data = [{'block':'something'}, {'block':'something'}]
    file = File('test', 'xml')
    file.create()
    file.write(data)
    print('01: ', file.read())
    for i in range(0, 100):
        file.add({'block':'something'})
    print('02: ', file.read())
tests()
'''
