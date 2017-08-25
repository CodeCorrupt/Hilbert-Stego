#!/usr/bin/env python
from __future__ import print_function
from PIL import Image
import binascii

keyLength = 256

def _find_full_string(x, y, xSize, ySize, pixels):
    bitString = ''
    cX = x
    cY = y
    while(cX < xSize and cX >= 0 and cY < ySize and cY >= 0 and len(bitString) < keyLength):
        bitString += str(pixels[cX,cY][0] % 2)
        a = pixels[cX,cY][1]%2
        b = pixels[cX,cY][2]%2
        dX = 0
        dY = 0
        if(a == 0 and b == 0):
            dX = 1
            dY = 0
        if(a == 0 and b == 1):
            dX = 0
            dY = 1
        if(a == 1 and b == 0):
            dX = -1
            dY = 0
        if(a == 1 and b == 1):
            dX = 0
            dY = -1
        cX += dX
        cY += dY
    return bitString



inputImage = "out.png"

img = Image.open(inputImage)
pixels = img.load() # create the pixel map


for i in range(img.size[0]):        # for every col:
    for j in range(img.size[1]):    # For every row
        ans = _find_full_string(i, j, img.size[0], img.size[1], pixels)
        if(len(ans) == keyLength):
            if(ans.startswith("0101001100101101") and ans.endswith("0010110101000101")):
                n = int('0b' + ans, 2)
                key = binascii.unhexlify('%x' % n)
                print(key)
                quit()
        else:
            print(len(ans))
