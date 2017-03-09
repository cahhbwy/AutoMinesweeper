# coding:gbk

from PIL import Image

minefieldKinds = {'none': 'none.PNG', '0': '0.PNG', '1': '1.PNG', '2': '2.PNG', '3': '3.PNG',
                  '4': '4.PNG', '5': '5.PNG', '6': '6.PNG', '7': '7.PNG', '8': '8.PNG',
                  'mine': 'mine.PNG', 'dead': 'mine_dead.PNG', 'flag': 'mine_flag.PNG',
                  'wrong': 'mine_wrong.PNG'}
# rgb2hex = lambda x: "%02x%02x%02x" % x
# rgb2hex = lambda x: "%x%x%x" % (x[0] / 16, x[1] / 16, x[2] / 16)
rgb2hex = lambda x: (x[0] >> 6 << 1) + (x[1] >> 5 << 1) + (x[2] >> 7)

for label, fileName in minefieldKinds.items():
    standPic = Image.open(fileName)
    # print label, standPic.getpixel((3, 9)), standPic.getpixel((9, 8)), standPic.getpixel((0, 0))
    print (rgb2hex(standPic.getpixel((9, 3))) << 1) + rgb2hex(standPic.getpixel((8, 9))) + rgb2hex(
        standPic.getpixel((0, 0))), label

'''
51:"mine",
25:"dead",
59:"flag",
78:"none",
57:"wrong",
16:"1",
70:"0",
44:"3",
37:"2",
40:"5",
34:"4",
13:"7",
50:"6",
58:"8"
'''
