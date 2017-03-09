# coding:gbk

from PIL import Image

minefieldKinds = {'none': 'none.PNG', '0': '0.PNG', '1': '1.PNG', '2': '2.PNG', '3': '3.PNG',
                  '4': '4.PNG', '5': '5.PNG', '6': '6.PNG', '7': '7.PNG', '8': '8.PNG',
                  'mine': 'mine.PNG', 'dead': 'mine_dead.PNG', 'flag': 'mine_flag.PNG',
                  'wrong': 'mine_wrong.PNG'}
rgb2hex = lambda x: "%02x%02x%02x" % x

for label, fileName in minefieldKinds.items():
    standPic = Image.open(fileName)
    # print label, standPic.getpixel((3, 9)), standPic.getpixel((9, 8)), standPic.getpixel((0, 0))
    print rgb2hex(standPic.getpixel((9, 3))) + rgb2hex(standPic.getpixel((8, 9))) + rgb2hex(
        standPic.getpixel((0, 0))), label

'''
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
'''

gameStatus = {'running': 'running.PNG', 'win': 'win.PNG', 'dead': 'dead.PNG'}

for label, fileName in gameStatus.items():
    pic = Image.open(fileName)
    print rgb2hex(pic.getpixel((8, 8))) + rgb2hex(pic.getpixel((8, 14))),label
    print pic.getpixel((8, 8)),pic.getpixel((8, 14)),label

'''
"ffff00000000": "running",
"ffff00ffff00": "win",
"000000ffff00": "dead"
'''