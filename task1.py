
def possible3(set3):
    if set3 == "ooo" or set3 == "o-o" or set3 == "---" or set3 == "--o" or set3 == "o--" or set3 == "-o-":
        return False
    elif set3 == "oo-":
        return "--o"
    elif set3 == "-oo":
        return "o--"


def computePossibleStates(boardStr):
    states = []
    for i in range(len(boardStr)-2):
        possibleState = possible3(boardStr[i:i+3])
        if(possibleState != False):
            lastBit = boardStr[i+3:] or ""
            states.append(boardStr[:i]+possibleState+lastBit)

    return states


def pegRemover(boardStr, level, maxScore):
    nextStates = computePossibleStates(boardStr)
    if len(nextStates) == 0:
        return level
    scores = []
    for state in nextStates:
        score = pegRemover(state, level+1, maxScore)
        if(score == maxScore):
            return score
        scores.append(score)
    return max(scores)


n = int(input())
results = []

for i in range(n):
    case = input()
    count = case.count("o")
    results.append(str(count - pegRemover(case, 0, str(count-1))))

print("\n".join(results))
