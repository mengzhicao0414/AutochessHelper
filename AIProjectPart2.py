import numpy as np
import heapq
import operator
import collections
import copy


# define a variable class to record the detailed information of each varable
class Variable:
    def __init__(self, name, varNameList, valListLen):
        # the name of each Variable
        self.name = name
        # the assign result of the Variable, defalut as -1 which won't be a
        # confilct with our assignments
        self.assign = -1
        # constraint matrix between other Variables
        self.conMatrix = {}
        for i in varNameList:
            if (i != name):
                self.conMatrix[i] = np.ones([valListLen, valListLen])

        # based on the constraint matrix bulid the neighbor of each variable
        self.neighbors = []
        # domain of the variable defalut are all values
        self.domain = [i for i in range(valListLen)]
        # sorted domain for recursion
        self.sDomain = []


# class to record distinct hero information


class HeroInfo:
    def __init__(self, name, level, price, race, classes, battlePoint):
        self.name = name
        self.level = level
        self.price = price
        self.race = race
        self.classes = classes
        self.battlePoint = battlePoint


# class to record prepared data and method to transform our data into csp
# problem format


class UnitInfo:
    def __init__(self, heroBase, heroPool, money, population):
        self.heroBase = heroBase
        self.heroPool = heroPool
        self.money = money
        self.population = population
        self.tHeroPool = []

    def tranLevel(self):
        counterHero = collections.Counter(self.heroPool).items()
        for unit, number in counterHero:
            if (number < 3):
                for i in range(number):
                    self.tHeroPool.append(unit)
            else:
                levelUp = int(number / 3)
                stayNumber = number % 3
                for i in range(levelUp):
                    if (self.heroBase[unit].price * 3 * (i + 1) <= self.money):
                        self.tHeroPool.append((unit[0], unit[1] + 1))
                for j in range(stayNumber):
                    self.tHeroPool.append(unit)
        if (len(self.tHeroPool) < self.population):
            self.population = len(self.tHeroPool)
        self.tHeroPool = sorted(
            self.tHeroPool,
            key=lambda x: heroBase[x].battlePoint,
            reverse=True)

    def countCombo(self):
        comboList = []
        tmpList = []
        for i in self.tHeroPool:
            tmpList.append((i[0], 1))
        noDuList = list(set(tmpList))

        for unit in noDuList:
            race = heroBase[unit].race
            classes = heroBase[unit].classes
            comboList.append(race)
            comboList.append(classes)
        comboCouter = collections.Counter(comboList)
        return comboCouter

    def buff_select(self, sheet1, sheet2):
        sque = []
        detail = []
        for key, value in sheet1.items():
            tem = []
            position = []
            battle = []
            combo = (value, 0.0)
            for buff in sheet2[key]:
                if value >= buff[0]:
                    combo = buff
                    break

            for index, hero in enumerate(self.tHeroPool):
                if (self.heroBase[hero].race ==
                        key or self.heroBase[hero].classes == key):
                    position.append(index)
                    battle.append(self.heroBase[hero].battlePoint)
            re = map(battle.index, heapq.nlargest(combo[0], battle))
            for i in list(re):
                tem.append(battle[i])
            average = (combo[1] + sum(tem)) / float(combo[0])
            sque.append(position)
            sque[-1].append(combo[0])
            sque[-1].append(average)

        sque.sort(key=operator.itemgetter(-1), reverse=True)

        for i in range(len(sque)):
            sque[i].pop()
            detail.append(sque[i].pop())
        return sque, detail


# build-in data base with hero information and combination battle point


def createData():
    heroBase = dict()
    Tusk = HeroInfo('Tusk', 1, 1, 'Beast', 'Warrior', 6.0)
    Tiny = HeroInfo('Tiny', 1, 1, 'Element', 'Warrior', 6.2)
    Tinker = HeroInfo('Tinker', 1, 1, 'Goblin', 'Mech', 4.0)
    ShadowShaman = HeroInfo('ShadowShaman', 1, 1, 'Troll', 'Shaman', 3.5)
    OgreMagi = HeroInfo('OrgeMagi', 1, 1, 'Ogre', 'Mage', 3.8)
    Enchantress = HeroInfo('Enchantress', 1, 1, 'Beast', 'Druid', 3.6)
    DrowRanger = HeroInfo('DrowRanger', 1, 1, 'Undead', 'Hunter', 3.5)
    Clockwerk = HeroInfo('Clockwerk', 1, 1, 'Goblin', 'Mech', 7.0)
    Batrider = HeroInfo('Batrider', 1, 1, 'Troll', 'Knight', 3.0)
    Axe = HeroInfo('Axe', 1, 1, 'Orc', 'Warrior', 5.0)
    Antimage = HeroInfo('Antimage', 1, 1, 'Elf', 'Demonhunter', 6.8)
    BountyHunter = HeroInfo('BountyHunter', 1, 1, 'Goblin', 'Assassin', 7.8)

    # level 2
    Tusk2 = HeroInfo('Tusk', 2, 3, 'Beast', 'Warrior', 6.0 * 1.8)
    Tiny2 = HeroInfo('Tiny', 2, 3, 'Element', 'Warrior', 6.2 * 1.8)
    Tinker2 = HeroInfo('Tinker', 2, 3, 'Goblin', 'Mech', 4.0 * 1.8)
    ShadowShaman2 = HeroInfo(
        'ShadowShaman',
        2,
        3,
        'Troll',
        'Shaman',
        3.5 * 1.8)
    OgreMagi2 = HeroInfo('OrgeMagi', 2, 3, 'Ogre', 'Mage', 3.8 * 1.8)
    Enchantress2 = HeroInfo('Enchantress', 2, 3, 'Beast', 'Druid', 3.6 * 1.8)
    DrowRanger2 = HeroInfo('DrowRanger', 2, 3, 'Undead', 'Hunter', 3.5 * 1.8)
    Clockwerk2 = HeroInfo('Clockwerk', 2, 3, 'Goblin', 'Mech', 7.0 * 1.8)
    Batrider2 = HeroInfo('Batrider', 2, 3, 'Troll', 'Knight', 3.0 * 1.8)
    Axe2 = HeroInfo('Axe', 2, 3, 'Orc', 'Warrior', 5.0 * 1.8)
    Antimage2 = HeroInfo('Antimage', 2, 3, 'Elf', 'Demonhunter', 7.5 * 1.8)
    BountyHunter2 = HeroInfo(
        'BountyHunter',
        2,
        3,
        'Goblin',
        'Assassin',
        7.8 * 1.8)

    heroBase[('Tusk', 1)] = Tusk
    heroBase[('Tusk', 2)] = Tusk2
    heroBase[('Tiny', 1)] = Tiny
    heroBase[('Tiny', 2)] = Tiny2
    heroBase[('Tinker', 1)] = Tinker
    heroBase[('Tinker', 2)] = Tinker2
    heroBase[('ShadowShaman', 1)] = ShadowShaman
    heroBase[('ShadowShaman', 2)] = ShadowShaman2
    heroBase[('OgreMagi', 1)] = OgreMagi
    heroBase[('OgreMagi', 2)] = OgreMagi2
    heroBase[('Enchantress', 1)] = Enchantress
    heroBase[('Enchantress', 2)] = Enchantress2
    heroBase[('DrowRanger', 1)] = DrowRanger
    heroBase[('DrowRanger', 2)] = DrowRanger2
    heroBase[('Clockwerk', 1)] = Clockwerk
    heroBase[('Clockwerk', 2)] = Clockwerk2
    heroBase[('Batrider', 1)] = Batrider
    heroBase[('Batrider', 2)] = Batrider2
    heroBase[('Axe', 1)] = Axe
    heroBase[('Axe', 2)] = Axe2
    heroBase[('Antimage', 1)] = Antimage
    heroBase[('Antimage', 2)] = Antimage2
    heroBase[('BountyHunter', 1)] = BountyHunter
    heroBase[('BountyHunter', 2)] = BountyHunter2

    comboHDict = dict()

    comboHDict['Assassin'] = [(9, 18.0), (6, 10.0), (3, 5.0)]
    comboHDict['Demonhunter'] = [(2, 6.0), (1, 1.0)]
    comboHDict['Druid'] = [(4, 4.0), (2, 2.0)]
    comboHDict['Hunter'] = [(6, 15.0), (3, 6.0)]
    comboHDict['Knight'] = [(6, 13.0), (4, 8.0), (2, 3.0)]
    comboHDict['Mage'] = [(6, 16.0), (3, 8.0)]
    comboHDict['Mech'] = [(4, 8.0), (2, 2.0)]
    comboHDict['Shaman'] = [(2, 5.0)]
    comboHDict['Warlock'] = [(6, 12.0), (3, 7.0)]
    comboHDict['Warrior'] = [(9, 17.0), (6, 10.0), (3, 3.0)]
    comboHDict['Beast'] = [(6, 13.0), (4, 6.0), (2, 3.0)]
    comboHDict['Demon'] = [(1, 2.0)]
    comboHDict['Dragon'] = [(3, 10.0)]
    comboHDict['Dwarf'] = [(1, 1.0)]
    comboHDict['Element'] = [(4, 8.0), (2, 4.0)]
    comboHDict['Elf'] = [(9, 15.0), (6, 8.0), (3, 4.0)]
    comboHDict['Goblin'] = [(6, 15.0), (3, 6.0)]
    comboHDict['Human'] = [(6, 10.0), (4, 5.0), (2, 3.0)]
    comboHDict['Naga'] = [(4, 8.0), (2, 4.0)]
    comboHDict['Ogre'] = [(1, 1.0)]
    comboHDict['Orc'] = [(4, 7.0), (2, 3.0)]
    comboHDict['Troll'] = [(4, 10.0), (2, 3.0)]
    comboHDict['Undead'] = [(4, 8.0), (2, 3.0)]

    return heroBase, comboHDict


# read sample file and initial our Variables


def initialVar(filepath, heroBase, comboHDict):
    fp = open(filepath, "r")
    lines = fp.readlines()
    heroPool = []

    varList = []
    unitNum = 0
    money = 0
    for line in lines:
        row = line.strip('\n').split()
        if row[0] == '#####':
            flag = row[2]
            continue

        if flag == "variables":
            unitNum = int(row[0])

        elif flag == "values":
            heroPool.append((row[0], int(row[1])))

        elif flag == "money":
            money = int(row[0])

    preData = UnitInfo(heroBase, heroPool, money, unitNum)
    preData.tranLevel()

    comboCounter = preData.countCombo()
    buffIndex, buffNum = preData.buff_select(comboCounter, comboHDict)

    varNameList = ["Unit%s" % i for i in range(preData.population)]
    valList = preData.tHeroPool
    for i in varNameList:
        varObj = Variable(i, varNameList, len(valList))
        varList.append(varObj)

    for unitIndex in range(buffNum[0]):
        varName = varNameList[unitIndex]
        unaryInclu(varList, varName, buffIndex[0])

    for i in varNameList:
        for j in varNameList:
            if (i != j):
                varOne = varList[varNameList.index(i)]
                varTwo = varList[varNameList.index(j)]
                biNotEquals(varOne, varTwo)

    return preData.money, valList, varList


# function to deal with the matrix of unary inclusive
def unaryInclu(varList, varName, valIndexList):
    # bulid the index of the value which is inclusinve for our Variable

    for i in varList:
        if (i.name == varName):
            for k in i.conMatrix.values():
                for j in range(k.shape[0]):
                    if (j not in valIndexList):
                        k[j] = 0
        else:
            for j in range(i.conMatrix[varName].shape[0]):
                if (j not in valIndexList):
                    i.conMatrix[varName][:, j] = 0


# function to deal with the matrix of the binary not equals
def biNotEquals(varOne, varTwo):
    # set the diag of variable as 0
    np.fill_diagonal(varOne.conMatrix[varTwo.name], 0)
    np.fill_diagonal(varTwo.conMatrix[varOne.name], 0)


# check the neighbor of each variable and  add them to a neighbor list
def checkNeighbor(varList):
    varDict = {}
    for i in varList:
        varDict[i.name] = i
    for i in varDict.values():
        for j in i.conMatrix.items():
            if (np.sum(j[1]) != j[1].shape[0] * j[1].shape[1]):
                i.neighbors.append(varDict[j[0]])


# Main BackTrackingSearch function
def BackTrackingSearch(varList, valList, deadLine, deadTable, sumTime):
    assignList = collections.deque()
    versionDe = collections.deque()

    if (not preAC3(varList, valList, versionDe)):
        return False
    return backTrack(
        assignList,
        varList,
        deadTable,
        deadLine,
        versionDe,
        valList,
        sumTime)


# AC3 before the backtracking phase which check the whole arc consistents
# of the variables
def preAC3(varList, valList, versionDe):
    queue = collections.deque()
    reviseDict = {}
    print("Domains Before Pre-processing of AC3: ")
    for i in varList:
        print("Variable: ", i.name, "Domain: ", [valList[j] for j in i.domain])
    for i in varList:
        for j in i.neighbors:
            queue.append((i, j))
    while queue:
        arc = queue.popleft()
        isRevised, reviseList = revise(arc[0], arc[1])
        if (not (arc[0] in reviseDict)):
            reviseDict[arc[0]] = []
        # reviseDict[arc[0]] = reviseDict[arc[0]].extend(reviseList)
        reviseDict[arc[0]].extend(reviseList)

        if (isRevised):
            if (len(arc[0].domain) == 0):
                versionDe.append(reviseDict)
                print("Domains After Pre-processing of AC3: ")
                for i in varList:
                    print(
                        "Variable: ", i.name, "Domain: ", [
                            valList[j] for j in i.domain])
                return False
            for i in arc[0].neighbors:
                if (i != arc[1]):
                    queue.append((arc[0], i))
    versionDe.append(reviseDict)
    print("Domains After Pre-processing of AC3: ")
    for i in varList:
        print("Variable: ", i.name, "Domain: ", [valList[j] for j in i.domain])

    return True


# recursive function in our BackTrackingSearch function
def backTrack(
        assignList,
        varList,
        deadTable,
        deadLine,
        versionDe,
        valList,
        sumTime):
    if len(assignList) == len(varList):
        return assignList
    nextVar = MRV(assignList, varList)

    leastConstraintValue(nextVar)
    print("\nSelected Variable:",
          nextVar.name,
          "Order of the values to try:",
          [valList[i] for i in nextVar.sDomain])
    for nextVal in nextVar.sDomain:
        print("Chosen Value", valList[nextVal])
        sumTime += deadTable[nextVal]
        if sumTime > deadLine:
            sumTime -= deadTable[nextVal]
            print("Fail because out of deadLine, choose the next value")
            continue
        else:
            nextVar.assign = nextVal
            assignList.append(nextVar)
            print("Assignment:")
            for i in assignList:
                print("Variable", i.name, "Value:", valList[i.assign])
            # record the abandoned domain after we set the value
            reviseDict = {}

            nextVar.domain.remove(nextVal)

            reviseDict[nextVar] = copy.deepcopy(nextVar.domain)
            nextVar.domain.clear()
            nextVar.domain.append(nextVal)

            if (not AC3(nextVar, versionDe, reviseDict, valList)):
                print("Fail because of failure in AC3, choose the next value")
                goBack(assignList, versionDe)

                continue
            result = backTrack(
                assignList,
                varList,
                deadTable,
                deadLine,
                versionDe,
                valList,
                sumTime)
            if result:
                return result
            else:
                print("BackTrack because no value available")
                goBack(assignList, versionDe)

    return False


# choose the value for the variable we have chosen
def leastConstraintValue(varible):
    sumCompare = []
    newSdomain = []
    for value in varible.domain:
        sumValue = 0
        for a, Matrix in varible.conMatrix.items():
            sumValue += np.sum(Matrix[value])
        sumCompare.append(sumValue)
    copyDomain = copy.deepcopy(varible.domain)
    varZipList = list(zip(sumCompare, copyDomain))
    sortedList = sorted(varZipList, key=lambda x: x[0], reverse=True)
    for i in sortedList:
        newSdomain.append(i[1])
    varible.sDomain = newSdomain


# if MRV can't find out which variable as the next one, then use
# degreeHeuristic funciton to break the tie
def degreeHeuristic(conflicts):
    sumCompare = []
    sum_matrix = 0
    for conflict in conflicts:
        for _, Matrix in conflict.conMatrix.items():
            sum_matrix += np.sum(np.reshape(Matrix, (Matrix.size,)))
        sumCompare.append(sum_matrix)
    # Find the index(s) of the minimum sum of all varibles' conMatrix
    identical = [i for i, x in enumerate(sumCompare) if x == min(sumCompare)]
    if len(identical) == 1:
        return (conflicts[identical[0]])
    else:
        return (conflicts[0])


# MRV function to decide which variable we should choose to assign
def MRV(assignment, varList):
    length = []  # Create a list to save the length of the varibles' domains
    desiredVar = []
    for var in varList:
        if var not in assignment:
            desiredVar.append(var)
    for object in desiredVar:
        # calculate the length of the varible's domain
        length.append(len(object.domain))
    # Find the index(s) of the minimum length of all varibles' domainx
    identical = [i for i, x in enumerate(length) if x == min(length)]
    if len(identical) == 1:
        # When here is only one minimum length of domain exists, don't need to
        # use degree heuristic method to solve the conflicts.
        return (desiredVar[identical[0]])
    else:
        conflicts = []
        for i in identical:
            conflicts.append(desiredVar[i])
            return (degreeHeuristic(conflicts))


# function for decide if we delete the domain or not
def revise(variable, varNeighbor):
    isRevised = False
    reviseList = []
    domainList = copy.deepcopy(variable.domain)
    neighDomain = copy.deepcopy(varNeighbor.domain)
    for i in domainList:
        sum = 0
        for j in neighDomain:
            sum += variable.conMatrix[varNeighbor.name][i, j]
        if (sum == 0):
            reviseList.append(i)
            variable.domain.remove(i)
            isRevised = True
    return isRevised, reviseList


# go back to the last version of domain and assignment


def goBack(assignList, versionDe):
    assignList.pop().assign = -1
    lastVersion = versionDe.pop()
    for i in lastVersion.keys():
        i.domain.extend(lastVersion[i])


# recursive add the neighbors of the variable
def neighborAdd(queue, variable):
    for i in variable.neighbors:
        if (not (variable, i) in queue):
            queue.append((variable, i))
            neighborAdd(queue, i)


# AC3 during the backtracking
def AC3(variable, versionDe, reviseDict, valList):
    queue = collections.deque()
    neighborAdd(queue, variable)
    print("Domains Before  AC3: ")
    for i in varList:
        print("Variable: ", i.name, "Domain: ", [valList[j] for j in i.domain])
    while queue:
        arc = queue.popleft()
        isRevised, reviseList = revise(arc[0], arc[1])
        if (not (arc[0] in reviseDict)):
            reviseDict[arc[0]] = []
        # reviseDict[arc[0]] = reviseDict[arc[0]].extend(reviseList)
        reviseDict[arc[0]].extend(reviseList)

        if (isRevised):
            if (len(arc[0].domain) == 0):
                versionDe.append(reviseDict)
                print("Domains After Pre-processing of AC3: ")
                for i in varList:
                    print(
                        "Variable: ", i.name, "Domain: ", [
                            valList[j] for j in i.domain])
                return False

            for i in arc[0].neighbors:
                if (i != arc[1]):
                    queue.append((arc[0], i))
    versionDe.append(reviseDict)
    print("Domains After AC3: ")
    for i in varList:
        print("Variable: ", i.name, "Domain: ", [valList[j] for j in i.domain])
    return True


if __name__ == "__main__":
    print("Please input the test file path like part2test1.txt ")
    filePath = input()

    heroBase, comboHDict = createData()

    deadLine, valList, varList = initialVar(filePath, heroBase, comboHDict)

    checkNeighbor(varList)
    deadTable = []
    for i in valList:
        deadTable.append(heroBase[i].price)
    sumTime = 0
    result = BackTrackingSearch(varList, valList, deadLine, deadTable, sumTime)
    if (result):
        print("Final Result:\n")
        sum = 0
        for i in result:
            print("Variable :", i.name, "Value :", valList[i.assign])
            sum += heroBase[valList[i.assign]].price

        print("\n")
        print("Total money: ", sum)

    else:
        print("No result")
