import multiprocessing
import array
import networkx as nx


def deal_one(a, l, s, e):
    #print(s, e)
    for i in range(s, e):
        l[i] = nx.DiGraph()

a = []
for i in range(100):
    a.append(i)
num_core = min(multiprocessing.cpu_count(),                        len(a))
step = int(len(a) / num_core)

if num_core * step < len(a):
    step += 1

jobs = []
print(a)

manager = multiprocessing.Manager()
l = manager.list() #range(100))
for i in range(len(a)):
    l.append(0)

for i in range(num_core):
    s = step * i
    if s > len(a) - 1:
        continue
    if i == num_core - 1:
        e = len(a)
    else:
        e = s + step
    e = min(e, len(a))
    p = multiprocessing.Process(target = deal_one, args = (a, l, s, e))
    jobs.append(p)
    p.start()

for p in jobs:
    p.join()

print(l)
