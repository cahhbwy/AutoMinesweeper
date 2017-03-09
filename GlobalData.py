# coding:gbk
import numpy


class MineData:
    '''
    类型说明：
        size: 雷区大小
        mineSum: 雷的总数
        minefieldsType: 雷区状态
            none: 未知/未点开
            mine: 失败时未踩中的雷
            mine_dead: 失败时踩中的雷
            mine_wrong: 失败时标记错误的假雷
            flag: 对雷的标记
            '012345678': 表示周围的雷数量
        minefieldsStatus: 游戏中雷区状态，Flase表示为已标记的内部，True表示已标记的边缘和未标记区域
    '''
    size = (8, 8)
    mineSum = 10
    minefieldsType = []
    minefieldsStatus = []
    probability = None
    status = None

    def __init__(self, size=(8, 8), mineSum=10):
        MineData.size = size
        MineData.mineSum = mineSum
        MineData.minefieldsType = [['none'] * size[1] for i in xrange(size[0])]
        MineData.minefieldsStatus = [[True] * size[1] for i in xrange(size[0])]
        MineData.probability = numpy.zeros(size)
