# coding:gbk

from GlobalData import MineData
import numpy


def neighborhood(position, size, step=1):
    return [(i, j) for i in xrange(position[0] - step, position[0] + step + 1) for j in
            xrange(position[1] - step, position[1] + step + 1) if
            0 <= i < size[0] and 0 <= j < size[1]]


def divideInOut(size):
    for i in xrange(size[0]):
        for j in xrange(size[1]):
            if MineData.minefieldsStatus[i][j]:
                if MineData.minefieldsType[i][j] is 0:
                    MineData.minefieldsStatus[i][j] = False
                else:
                    neighbor = neighborhood((i, j), size)
                    for x, y in neighbor:
                        if MineData.minefieldsType[x][y] is 9:
                            break
                    else:
                        MineData.minefieldsStatus[i][j] = False


def findByOne(size):
    MineData.probability[:] = 0.5
    for i in xrange(size[0]):
        for j in xrange(size[1]):
            if MineData.minefieldsStatus[i][j] and 0 < MineData.minefieldsType[i][j] < 9:
                neighbor = neighborhood((i, j), size)
                mineNum = int(MineData.minefieldsType[i][j])
                blank = []
                for x, y in neighbor:
                    if MineData.minefieldsType[x][y] is 10:
                        mineNum -= 1
                    elif MineData.minefieldsType[x][y] is 9:
                        blank.append((x, y))
                if mineNum == 0:
                    for x, y in blank:
                        MineData.probability[x][y] = 0.0
                elif len(blank) == mineNum:
                    for x, y in blank:
                        MineData.probability[x][y] = 1.0


def findByTwo(size):
    MineData.probability[:] = 0.5

    def divide(set1, set2):
        x = numpy.array([i * size[0] + j for i, j in set1])
        y = numpy.array([i * size[0] + j for i, j in set2])
        common = numpy.intersect1d(x, y)
        sub1 = numpy.setdiff1d(x, y)
        c1 = [(i / size[0], i % size[0]) for i in common]
        s1 = [(i / size[0], i % size[0]) for i in sub1]
        return (c1, s1)

    for i in xrange(size[0]):
        for j in xrange(size[1]):
            if MineData.minefieldsStatus[i][j] and 0 < MineData.minefieldsType[i][j] < 9:
                mineNum = int(MineData.minefieldsType[i][j])
                neighbor = neighborhood((i, j), size)
                blank = []
                for x, y in neighbor:
                    if MineData.minefieldsType[x][y] is 10:
                        mineNum -= 1
                    elif MineData.minefieldsType[x][y] is 9:
                        blank.append((x, y))
                neighbor = neighborhood((i, j), size, step=2)
                digits = []
                for x, y in neighbor:
                    if MineData.minefieldsStatus[x][y] and 0 < MineData.minefieldsType[x][y] < 9:
                        digits.append((x, y))
                for x, y in digits:
                    neighborMineNum = int(MineData.minefieldsType[x][y])
                    neighborNeighbor = neighborhood((x, y), size)
                    netghborBlank = []
                    for p, q in neighborNeighbor:
                        if MineData.minefieldsType[p][q] is 9:
                            netghborBlank.append((p, q))
                        elif MineData.minefieldsType[p][q] is 10:
                            neighborMineNum -= 1
                    intersection, unique = divide(blank, netghborBlank)
                    if mineNum - min(neighborMineNum, len(intersection)) == len(unique):
                        for p, q in unique:
                            MineData.probability[p][q] = 1.0
                    if len(netghborBlank) == neighborMineNum and mineNum == len(intersection):
                        for p, q in unique:
                            MineData.probability[p][q] = 0.0


def findByProbability(size):
    count = 0
    for i in xrange(size[0]):
        for j in xrange(size[1]):
            if MineData.minefieldsType[i][j] is 9:
                count += 1
    if count == 0:
        return 0, 0
    MineData.probability[:] = 1.0  # * MineData.mineSum / count
    for i in xrange(size[0]):
        for j in xrange(size[1]):
            if MineData.minefieldsStatus[i][j]:
                if 0 < MineData.minefieldsType[i][j] < 9:
                    MineData.probability[i][j] = 1.0
                    mineNum = int(MineData.minefieldsType[i][j])
                    neighbor = neighborhood((i, j), size)
                    blank = []
                    for x, y in neighbor:
                        if MineData.minefieldsType[x][y] is 9:
                            blank.append((x, y))
                        elif MineData.minefieldsType[x][y] is 10:
                            mineNum -= 1
                    for x, y in blank:
                        MineData.probability[x][y] = min(MineData.probability[x][y], 1.0 * mineNum / len(blank))
                elif MineData.minefieldsType[i][j] is 10:
                    MineData.probability[i][j] = 1.0
            else:
                MineData.probability[i][j] = 1.0
    minProbability = MineData.probability.min()
    selectSet = numpy.where(MineData.probability == minProbability)
    sel = numpy.random.randint(low=0, high=selectSet[0].size)
    return selectSet[0][sel], selectSet[1][sel]


def showProbability(size):
    for i in xrange(size[0]):
        for j in xrange(size[1]):
            print '%.4f' % MineData.probability[j][i],
        print
    print
