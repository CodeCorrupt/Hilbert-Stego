#!/usr/bin/env python
from PIL import Image
from hilbert import Hilbert
import sys
import math
import binascii

# Encoding
# R --> R%2 = bit value of this pixel
# G and B --> Together represent the direction of the next coordinate in the
# curve.
# 00 --> X+1,Y
# 01 --> X  ,Y+1
# 10 --> X-1, Y
# 11 --> X  , Y-1

# returns the new color of the pixel with the encoded data
def calculatePixelCode(x, y, bKey, hilbert):
    code = [0,0,0]

    # Get the distance along the curve a coordinate is in 2D space.
    dist = hilbert.distance_from_coordinates([x,y])
    # Set the key bit
    code[0] = int(bKey[dist%len(bKey)])

    print("dist=" + str(dist))
    print("code=" + str(code[0]))

    # Determine the coordinate of dist + 1
    currCoord = hilbert.coordinates_from_distance(dist)
    nextCoord = hilbert.coordinates_from_distance(dist+1)

    if(nextCoord[0] == x):
        code[2] = 1
        code[1] = (y - nextCoord[1] + 1)/2
    if(nextCoord[1] == y):
        code[2] = 0
        code[1] = (x - nextCoord[0] + 1)/2

    print("Code=" + str(code))
    print("(" + str(x) + "," + str(y) + ")")
    print("(" + str(nextCoord[0]) + "," + str(nextCoord[1]) + ")")

    return code

# returns the new color value
def changeColors(code, pixel):
    for i in range(3):
        if((pixel[i] % 2) != code[i]):
            if(pixel[i] > 265/2):
                pixel[i] -= 1
            else:
                pixel[i] += 1
    print(pixel)


def main():
    inputImage = sys.argv[1]
    userKey = "S-THIS IS THE KEY HAHAHAHAHAHA-E"
    maxKeyLength = 32


    # Convert key to binary
    if(len(userKey) > maxKeyLength):
        quit()
    binKey = bin(int(binascii.hexlify(userKey), 16))[2:]
    binKey = binKey.zfill(maxKeyLength * 8)


    # load the image
    img = Image.open(inputImage)
    # create the pixel map
    pixels = img.load()

    # Compute the number of hilbert curve itterations to construct a cube encompusing
    # the entire immage.
    hilbertItterations = int(math.ceil(math.sqrt(max(img.size[0], img.size[1]))))
    hilbert = Hilbert(hilbertItterations, 2)

    for j in range(img.size[0]):        # for every col:
        for i in range(img.size[1]):    # For every row
            print(pixels[i,j])
            lstPx = list(pixels[i,j])     # Convert tuple of color to list
            code = calculatePixelCode(i, j, binKey, hilbert)
            print("Pre= " + str(pixels[i,j]))
            changeColors(code, lstPx)
            pixels[i,j] = tuple(lstPx)
            print("Post= " + str(pixels[i,j]))
            print
    print(binKey)
    print(len(binKey))
    n = int('0b' + binKey, 2)
    key = binascii.unhexlify('%x' % n)
    print(key)


    img.save("out.png")

if __name__ == "__main__":
    main()
