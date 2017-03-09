# coding:gbk

import pyautogui
from PIL import ImageGrab
import numpy

# 识别
minefieldKinds = {
    59: 10,  # flag,
    78: 9,  # none,
    51: -1,  # mine,
    25: -1,  # dead,
    57: -1,  # wrong,
    70: 0,
    16: 1,
    37: 2,
    44: 3,
    34: 4,
    40: 5,
    50: 6,
    13: 7,
    58: 8
}


def findPanel():
    corner = []
    corner.append(pyautogui.locateOnScreen('src/左上.PNG'))
    corner.append(pyautogui.locateOnScreen('src/右下.PNG'))
    if corner[0] is None or corner[1] is None:
        print u"查找窗口失败，请移动窗体重试"
        return None
    panel = (corner[0][0] + 9, corner[0][1] + 9, corner[1][0], corner[1][1])
    # pic = ImageGrab.grab(panel)
    # pic.show()
    size = ((panel[2] - panel[0]) / 16, (panel[3] - panel[1]) / 16)
    # print size
    # isRight = raw_input(u"雷区大小和图像抓取是否正确？[y/n]: ")
    isRight = 'y'
    if isRight == 'y':
        return panel, size
    else:
        print u"查找窗口失败，请移动窗体重试"
        return None


def rgb2key(c1, c2, c3):
    return (((c1[0] >> 6 << 1) + (c1[1] >> 5 << 1) + (c1[2] >> 7)) << 1) + \
           (c2[0] >> 6 << 1) + (c2[1] >> 5 << 1) + (c2[2] >> 7) + \
           (c3[0] >> 6 << 1) + (c3[1] >> 5 << 1) + (c3[2] >> 7)


def kindByPixel(position, panelPic):
    global minefieldKinds
    x = position[0] * 16
    y = position[1] * 16
    c = rgb2key(panelPic.getpixel((x + 9, y + 3)), panelPic.getpixel((x + 8, y + 9)), panelPic.getpixel((x, y)))
    return minefieldKinds[c]


def identify(panel, size, mineType):
    panelPic = ImageGrab.grab(panel)
    status = True
    for i in xrange(size[0]):
        for j in xrange(size[1]):
            if mineType[i][j] == 9:
                kind = kindByPixel((i, j), panelPic)
                mineType[i][j] = kind
                status = None
                if kind == -1:
                    return False
    return status


# 控制
def click(panel, position, kind):
    x = panel[0] + position[0] * 16 + 8
    y = panel[1] + position[1] * 16 + 8
    pyautogui.click(x, y, button=kind)


def clickWhole(panel, size, probability, type='r'):
    hasAct = False
    global mineSum
    for i in xrange(size[0]):
        for j in xrange(size[1]):
            if 'r' in type and probability[i][j] >= 1.0:
                click(panel, (i, j), 'right')
                mineSum -= 1
                hasAct = True
            if 'l' in type and probability[i][j] <= 0.0:
                click(panel, (i, j), 'left')
                hasAct = True
    return hasAct


# 分析
def neighborhood(position, size, step=1):
    return [(i, j) for i in xrange(position[0] - step, position[0] + step + 1) for j in
            xrange(position[1] - step, position[1] + step + 1) if
            0 <= i < size[0] and 0 <= j < size[1]]


def divideInOut(size, mineType, mineStatus):
    for i in xrange(size[0]):
        for j in xrange(size[1]):
            if mineStatus[i][j]:
                if mineType[i][j] == 0:
                    mineStatus[i][j] = False
                else:
                    neighbor = neighborhood((i, j), size)
                    for x, y in neighbor:
                        if mineType[x][y] == 9:
                            break
                    else:
                        mineStatus[i][j] = False


def findByOne(size, mineType, mineStatus, probability):
    probability[:] = 0.5
    for i in xrange(size[0]):
        for j in xrange(size[1]):
            if mineStatus[i][j] and 0 < mineType[i][j] < 9:
                neighbor = neighborhood((i, j), size)
                mineNum = int(mineType[i][j])
                blank = []
                for x, y in neighbor:
                    if mineType[x][y] == 10:
                        mineNum -= 1
                    elif mineType[x][y] == 9:
                        blank.append((x, y))
                if mineNum == 0:
                    for x, y in blank:
                        probability[x][y] = 0.0
                elif len(blank) == mineNum:
                    for x, y in blank:
                        probability[x][y] = 1.0


def findByTwo(size, mineType, mineStatus, probability):
    probability[:] = 0.5

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
            if mineStatus[i][j] and 0 < mineType[i][j] < 9:
                mineNum = int(mineType[i][j])
                neighbor = neighborhood((i, j), size)
                blank = []
                for x, y in neighbor:
                    if mineType[x][y] == 10:
                        mineNum -= 1
                    elif mineType[x][y] == 9:
                        blank.append((x, y))
                neighbor = neighborhood((i, j), size, step=2)
                digits = []
                for x, y in neighbor:
                    if mineStatus[x][y] and 0 < mineType[x][y] < 9:
                        digits.append((x, y))
                for x, y in digits:
                    neighborMineNum = int(mineType[x][y])
                    neighborNeighbor = neighborhood((x, y), size)
                    netghborBlank = []
                    for p, q in neighborNeighbor:
                        if mineType[p][q] == 9:
                            netghborBlank.append((p, q))
                        elif mineType[p][q] == 10:
                            neighborMineNum -= 1
                    intersection, unique = divide(blank, netghborBlank)
                    if mineNum - min(neighborMineNum, len(intersection)) == len(unique):
                        for p, q in unique:
                            probability[p][q] = 1.0
                    if len(netghborBlank) == neighborMineNum and mineNum == len(intersection):
                        for p, q in unique:
                            probability[p][q] = 0.0


def findByProbability(size, mineType, mineStatus, probability):
    count = 0
    for i in xrange(size[0]):
        for j in xrange(size[1]):
            if mineType[i][j] == 9:
                count += 1
    if count == 0:
        return 0, 0
    probability[:] = 1.0  # * MineData.mineSum / count
    for i in xrange(size[0]):
        for j in xrange(size[1]):
            if mineStatus[i][j]:
                if 0 < mineType[i][j] < 9:
                    probability[i][j] = 1.0
                    mineNum = int(mineType[i][j])
                    neighbor = neighborhood((i, j), size)
                    blank = []
                    for x, y in neighbor:
                        if mineType[x][y] == 9:
                            blank.append((x, y))
                        elif mineType[x][y] == 10:
                            mineNum -= 1
                    for x, y in blank:
                        probability[x][y] = min(probability[x][y], 1.0 * mineNum / len(blank))
                elif mineType[i][j] == 10:
                    probability[i][j] = 1.0
            else:
                probability[i][j] = 1.0
    minProbability = probability.min()
    selectSet = numpy.where(probability <= minProbability + 0.1)
    sel = numpy.random.randint(low=0, high=selectSet[0].size)
    return selectSet[0][sel], selectSet[1][sel]


# 主函数
if __name__ == '__main__':
    pyautogui.PAUSE = 0.005
    panel, size = findPanel()
    if size == (8, 8):
        mineSum = 10
    elif size == (16, 16):
        mineSum = 40
    elif size == (30, 16):
        mineSum = 99
    else:
        mineSum = input(u"请输入雷数量：")
    mineType = numpy.ones(shape=size, dtype='int8') * 9
    mineStatus = numpy.ones(shape=size, dtype='bool')
    probability = numpy.ones(shape=size)

    while True:
        if identify(panel, size, mineType) is not None:
            break
        divideInOut(size, mineType, mineStatus)
        findByOne(size, mineType, mineStatus, probability)
        if not clickWhole(panel, size, probability, 'lr'):
            findByTwo(size, mineType, mineStatus, probability)
            if not clickWhole(panel, size, probability, 'lr'):
                x, y = findByProbability(size, mineType, mineStatus, probability)
                click(panel, (x, y), 'left')
