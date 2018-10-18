from functools import reduce
import math


class Pluger:
    def __init__(self, outlets, laptops, adapters):
        self.G = {}
        self.source = "s"
        self.sink = "t"
        self.visited = []

        outlets = reduce(self.occurrencesReducer, outlets, {})
        laptops = reduce(self.occurrencesReducer, laptops, {})

        self.G = {**{self.source: {laptop: count for laptop, count in laptops.items()}},
                  **{outlet: {self.sink: count} for outlet, count in outlets.items()}}
        for laptop in laptops.keys():
            matches = [laptop[2:]]
            memory = [laptop[2:]]
            while memory:
                chosen = memory.pop()
                foundMatches = [x[1] for x in (
                    y for y in adapters if y[0] == chosen) if x[1] not in matches]
                matches.extend(foundMatches)
                memory.extend(foundMatches)

            self.G = {**self.G, **{laptop: {match: outlets[match]
                                            for match in matches if match in outlets}}}

    def DFS(self, v):
        self.visited.append(v)
        if v == self.sink:
            return [v]
        elif v not in self.G:
            return False
        else:
            for vertice in self.G[v].keys():
                if vertice not in self.visited:
                    temp = self.DFS(vertice)

                    if temp != False:
                        temp.insert(0, v)
                        return temp
            return False

    def ford(self):
        self.visited = []
        path = self.DFS(self.source)

        if not path:
            return False

        minResCap = min(self.G[path[pos]][path[pos+1]]
                        for pos in range(len(path)-1))

        for i in range(len(path)-1):
            source = path[i]
            dest = path[i+1]
            send = self.G[source][dest] - minResCap

            if send == 0:
                del self.G[source][dest]
            else:
                self.G[source][dest] = send

            if dest in self.G:
                if source not in self.G[dest]:
                    self.G[dest][source] = minResCap
                else:
                    self.G[dest][source] += minResCap
            else:
                self.G[dest] = {source: minResCap}

        return minResCap

    def occurrencesReducer(self, acc, curr):
        return {**acc, curr: acc[curr]+1 if curr in acc else 1}

    def computeMaxHappyPeople(self):
        maxCap = 0
        while True:
            minResCap = self.ford()
            if not minResCap:
                break
            maxCap += minResCap

        return maxCap


caseNum = int(input())
results = []

for _ in range(caseNum):
    outlets = []
    laptops = []
    adapters = []

    outletsNum = int(input())
    for _ in range(outletsNum):
        outlets.append(input())

    laptopsNum = int(input())
    for _ in range(laptopsNum):
        laptops.append("l-"+input())

    adaptersNum = int(input())
    for _ in range(adaptersNum):
        key, value = input().split()
        adapters.append((key, value))

    instance = Pluger(outlets, laptops, adapters)
    results.append(laptopsNum - instance.computeMaxHappyPeople())

print("\n".join(str(x) for x in results))
