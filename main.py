# coding:gbk

from Analysis import *
from Identify import *
from Control import *

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
MineData(size, mineSum)

while True:
    identify(panel, size)
    if MineData.status is not None:
        break
    divideInOut(size)
    findByOne(size)
    if clickWhole(panel, size, 'lr'):
        pyautogui.moveTo((1, 1))
        print u"单数据判断"
    else:
        findByTwo(size)
        if clickWhole(panel, size, 'lr'):
            pyautogui.moveTo((1, 1))
            print u"两数据判断"
        else:
            x, y = findByProbability(size)
            print u"概率选择一次"
            click(panel, (x, y), 'left')
            pyautogui.moveTo((1, 1))
