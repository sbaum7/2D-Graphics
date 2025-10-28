from PIL import Image
import math
import numpy as np

countFrames = 314
frames = []

image = Image.open("./ship.png")
raster = image.load()

def interpolate(one, two, factor):
    return [a*(1-factor)+b*factor for a, b in zip(one, two)]

def nearestNeighbor(px, py):
    return raster[int(px), int(py)]

def bilinearInterpolation(px, py):
    if not (0 <= int(px) < image.width-1 and 0 <= int(py) < image.height-1):
        return nearestNeighbor(px, py)
    ul = raster[int(px), int(py)]
    ur = raster[int(px)+1, int(py)]
    ll = raster[int(px), int(py)+1]
    lr = raster[int(px)+1, int(py)+1]

    x_factor = px - int(px)
    y_factor = py - int(py)

    top = interpolate(ul, ur, x_factor)
    bottom = interpolate(ll, lr, x_factor)
    middle = interpolate(top, bottom, y_factor)
    return tuple([int(c) for c in middle])

def rgbToHsl(r, g, b):
    rf = r / 255.0
    gf = g / 255.0
    bf = b / 255.0

    maxc = max(rf, gf, bf)
    minc = min(rf, gf, bf)
    l = (maxc + minc) / 2.0

    if maxc == minc:
        return 0.0, 0.0, l

    dif = maxc - minc
    if l > 0.5:
        s = dif / (2.0 - maxc - minc)
    else:
        s = dif / (maxc + minc)

    if maxc == rf:
        h = (gf - bf) / dif
        if gf < bf:
            h += 6
    elif maxc == gf:
        h = (bf - rf) / dif + 2
    else:
        h = (rf - gf) / dif + 4

    h /= 6.0
    return h, s, l

def hslToRgb(h, s, l):
    c = (1 - abs(2 * l - 1)) * s
    hPrime = h * 6.0
    xCh = c * (1 - abs((hPrime % 2) - 1))

    if 0 <= hPrime < 1:
        r1, g1, b1 = c, xCh, 0
    elif 1 <= hPrime < 2:
        r1, g1, b1 = xCh, c, 0
    elif 2 <= hPrime < 3:
        r1, g1, b1 = 0, c, xCh
    elif 3 <= hPrime < 4:
        r1, g1, b1 = 0, xCh, c
    elif 4 <= hPrime < 5:
        r1, g1, b1 = xCh, 0, c
    else:
        r1, g1, b1 = c, 0, xCh

    m = l - c / 2
    rOut = int(round((r1 + m) * 255))
    gOut = int(round((g1 + m) * 255))
    bOut = int(round((b1 + m) * 255))

    rOut = max(0, min(255, rOut))
    gOut = max(0, min(255, gOut))
    bOut = max(0, min(255, bOut))

    return (rOut, gOut, bOut)

# target saturation during loop
def adjustSaturation(rgb, satTarget):
    h, s, l = rgbToHsl(*rgb)
    s = max(0.0, min(1.0, satTarget))
    return hslToRgb(h, s, l)

sMin = 0.0
sMax = 1.0

for i in range(countFrames):
    newImage = Image.new("RGB", (image.width, image.height))
    newRaster = newImage.load()

    t = i / countFrames
    satFactor = sMin + (sMax - sMin) * (0.5 * (1 + math.cos(2 * math.pi * t)))

    for x in range(image.width):
        for y in range(image.height):
            color = raster[x, y]
            newRaster[x, y] = adjustSaturation(color, satFactor)

    frames.append(newImage)

frames[0].save(
    "movie_saturation.png",
    save_all=True,
    append_images=frames[1:],
    duration=1/60*1000,
    loop=0,
)
