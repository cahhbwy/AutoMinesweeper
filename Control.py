# coding:gbk

import pyautogui
from GlobalData import MineData


def click(panel, position, kind):
    x = panel[0] + position[0] * 16 + 8
    y = panel[1] + position[1] * 16 + 8
    pyautogui.click(x, y, button=kind)


def clickWhole(panel, size, type='r'):
    hasAct = False
    for i in xrange(size[0]):
        for j in xrange(size[1]):
            if 'r' in type and MineData.probability[i][j] >= 1.0:
                click(panel,(i,j),'right')
                MineData.mineSum-=1
                hasAct=True
            if 'l' in type and MineData.probability[i][j]<=0.0:
                click(panel,(i,j),'left')
                hasAct=True
    return hasAct


