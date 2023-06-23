state = [0, 0, 6, 5, 4, 3, 2, 1, 7]
print(int(''.join([str(t) for t in state])))
s = set()
print(s, len(s))
s.add(int(''.join([str(t) for t in state])))
print(s, len(s))

s.discard(765432100)
print(s, len(s))