# coding:gbk

import pyautogui
from PIL import ImageGrab
from GlobalData import MineData

minefieldKinds = {
    "c0c0c0000000ffffff": "flag",
    "c0c0c0c0c0c0ffffff": "none",
    "c0c0c0000000808080": "mine",
    "ff0000000000808080": "dead",
    "c0c0c0ff0000808080": "wrong",
    "c0c0c0c0c0c0808080": "0",
    "0000ff0000ff808080": "1",
    "008000008000808080": "2",
    "ff0000c0c0c0808080": "3",
    "000080c0c0c0808080": "4",
    "800000c0c0c0808080": "5",
    "008080c0c0c0808080": "6",
    "000000000000808080": "7",
    "808080c0c0c0808080": "8"
}

rgb2hex = lambda x: "%02x%02x%02x" % x


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


def identify(panel, size):
    def kindByPixel(position, panelPic):
        global minefieldKinds
        x = position[0] * 16
        y = position[1] * 16
        c = rgb2hex(panelPic.getpixel((x + 9, y + 3))) + rgb2hex(panelPic.getpixel((x + 8, y + 9))) + rgb2hex(
            panelPic.getpixel((x, y)))
        return minefieldKinds[c]

    panelPic = ImageGrab.grab(panel)
    status = True
    for i in xrange(size[0]):
        for j in xrange(size[1]):
            if MineData.minefieldsType[i][j] is 'none':
                kind = kindByPixel((i, j), panelPic)
                MineData.minefieldsType[i][j] = kind
                status = None
                if kind in ['mine', 'dead', 'wrong']:
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
