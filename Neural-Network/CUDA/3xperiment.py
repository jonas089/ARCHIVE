from numba import jit
from numba.experimental import jitclass
from numba import boolean, int32, float64, uint8
import time
from hashlib import sha256
spec=[
    ('a', int32),
    ('b', int32)
]

@jitclass(spec)
class a_CUDA_class():
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def addition(self):
        return self.a + self.b
'''
@jit
def a_CUDA_func(instance, c, list):
    r = instance.addition()
    for i in range(0, 1000000000000000000):
        r += c
        #print(instance.addition() + c)
    print(r)

def a_CPU_func(instance, c):
    r = instance.addition()
    for i in range(0,1000):
        r += c
        #print(instance.addition() + c)
    print(r)

list = [1,2]

start = time.time()
instance = a_CUDA_class(5, 1)
a_CUDA_func(instance, 1, list)
print("CUDA: " + str(time.time()-start))

start = time.time()
a_CPU_func(instance, 1)
print("CPU: " + str(time.time()-start))
'''

# Comparing hashing power of CPU and GPU

@jit
def GPU(data):
    s = sha256()
    s.update(data.encode('utf-8'))
    return s.hexdigest()
def CPU(data):
    s = sha256()
    s.update(data.encode('utf-8'))
    return s.hexdigest()

def Compute_x_hashes(x, device):
    hashes = []
    for i in range(0, x):
        data = str(x) + str(time.time())
        if device == "GPU":
            hash = GPU(data)
        elif device == "CPU":
            hash = CPU(data)
        else: return
        hashes.append(len(hashes))
        hashes[len(hashes) - 1] = hash
    print(hashes)

def Evaluate_Devices(devices):
    hash_counter = 1
    while devices['GPU'] > devices['CPU'] or str(devices['GPU']) == '0.0' or str(devices['CPU']) == '0.0':
        start = time.time()
        G = Compute_x_hashes(hash_counter, "GPU")
        elapsed_time = time.time() - start
        devices['GPU'] = elapsed_time
        #print('GPU: ' + str(devices['GPU']))
        start = time.time()
        C = Compute_x_hashes(hash_counter, "CPU")
        elapsed_time = time.time() - start
        devices['CPU'] = elapsed_time
        #print('CPU: ' + str(devices['CPU']))
        hash_counter += 1
    print('GPU is now more efficient: ' + str(hash_counter))
Evaluate_Devices({"GPU":1, "CPU":-1})
