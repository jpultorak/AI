from functools import cmp_to_key

agents = ['A', 'B', 'C', 'D']
results = [2.5, 1, 0, 3]

final =  [(agent, res) for agent, res in zip(agents, results)]

final.sort(key=cmp_to_key(lambda x1, x2 : x1[1] - x2[1]), reverse=True)
print(final)