# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import matplotlib.pyplot as plt

OFF, ON = 0, 1

def dec2bin(n):
    """10進数を2進数の01リストに変換
    下位ビットから順番に並べる"""
    bit_list = np.zeros(8)
    for i in range(8):
        bit_list[i] = n%2
        n = int(n/2)
    return bit_list

def ca(width, height, rulenum):
    """1次元セルオートマトンの図を描画"""
    results = np.zeros((height, width))

    # 初期状態（中央のセルだけON）
    first_row = np.zeros(width)
    first_row[int(width/2)] = ON
    results[0] = first_row

    # ルールの番号から次の状態のビット列を得る
    rule = dec2bin(rulenum)

    for i in range(1, height):
        old_row = results[i-1]
        new_row = np.zeros(width)
        for j in range(width):
            # widthの剰余を取るのは、端同士がつながっているため
            n = 4 * old_row[(j-1)%width] + 2 * old_row[j] + old_row[(j+1)%width]
            new_row[j] = rule[int(n)]
        results[i] = new_row
    return results

def render(results, width, height, filename="ca.png"):
    """セルオートマトンを描画"""
    img = Image.new("RGB", (width, height), (255,255,255))
    draw = ImageDraw.Draw(img)
    for y in range(height):
        line = []
        for x in range(width):
            if results[y][x] == ON:
                character = "W"
            else:
                character = " "
            line.append(character)
        draw.text((0, y), "".join(line), fill="#000000")
        print("".join(line), end='\n')
            #draw.point((x, y), (0, 0, 0))
    out = np.array(img)
    #plt.imshow(out)
    #img.save(filename, "PNG")

if __name__ == "__main__":
    width, height = 300, 150
    rulenum = 210
    results = ca(width, height, rulenum)
    render(results, width, height)
    