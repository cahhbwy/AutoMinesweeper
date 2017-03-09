# coding:gbk

import pyautogui
from PIL import ImageGrab
from GlobalData import MineData

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
    print size
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


def identify(panel, size):
    panelPic = ImageGrab.grab(panel)
    status = True
    for i in xrange(size[0]):
        for j in xrange(size[1]):
            if MineData.minefieldsType[i][j] is 9:
                kind = kindByPixel((i, j), panelPic)
                MineData.minefieldsType[i][j] = kind
                status = None
                if kind is -1:
                    MineData.status = False
                    return
    MineData.status = status


def showMinefields():
    for i in xrange(MineData.size[0]):
        for j in xrange(MineData.size[1]):
            print "%8s" % MineData.minefieldsType[j][i],
        print
    print


if __name__ == '__main__':
    panel, MineData.size, facePanel = findPanel()
    print facePanel
    MineData(MineData.size, 10)
    identify(panel)
    showMinefields()
