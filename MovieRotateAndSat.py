from PIL import Image
import math
import numpy as np


def rgb_to_hsl(r, g, b):
    rf = r / 255.0
    gf = g / 255.0
    bf = b / 255.0

    maxC = max(rf, gf, bf)
    minC = min(rf, gf, bf)
    l = (maxC + minC) / 2.0

    if maxC == minC:
        return 0.0, 0.0, l

    dif = maxC - minC
    if l > 0.5:
        s = dif / (2.0 - maxC - minC)
    else:
        s = dif / (maxC + minC)

    if maxC == rf:
        h = (gf - bf) / dif
        if gf < bf:
            h += 6
    elif maxC == gf:
        h = (bf - rf) / dif + 2
    else:
        h = (rf - gf) / dif + 4

    h /= 6.0
    return h, s, l


def hsl_to_rgb(h, s, l):
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


def set_saturation(rgb, satTarget):
    h, s, l = rgb_to_hsl(*rgb)
    s = max(0.0, min(1.0, satTarget))
    return hsl_to_rgb(h, s, l)


def rotate_point(x, y, cx, cy, angleRad):
    # translate to center
    tx = x - cx
    ty = y - cy

    cosA = math.cos(angleRad)
    sinA = math.sin(angleRad)

    rx = tx * cosA - ty * sinA
    ry = tx * sinA + ty * cosA

    # translate back
    return rx + cx, ry + cy


def create_rotate_and_saturate_animation(
    input_path,
    output_path,
    frames = 300,
    fps = 60,
    sMin = 0.0,
    sMax = 1.0,
):
    image = Image.open(input_path).convert("RGB")
    width, height = image.size
    raster = image.load()

    framesList = []

    cx = width / 2.0
    cy = height / 2.0

    for i in range(frames):
        # angle rotates one full turn over 314 frames
        angle = 2 * math.pi * (i / frames)

        t = i / frames
        satTarget = sMin + (sMax - sMin) * 0.5 * (1 + math.cos(2 * math.pi * t))

        newImg = Image.new("RGB", (width, height))
        newPixels = newImg.load()

        for x in range(width):
            for y in range(height):
                srcX, srcY = rotate_point(x, y, cx, cy, -angle)
                # nearest-neighbor sampling (fast and simple)
                ix = int(round(srcX))
                iy = int(round(srcY))

                if 0 <= ix < width and 0 <= iy < height:
                    orig = raster[ix, iy]
                else:
                    orig = (0, 0, 0)

                newPixels[x, y] = set_saturation(orig, satTarget)

        framesList.append(newImg)

    framesList[0].save(
        output_path,
        save_all = True,
        append_images = framesList[1:],
        duration = 1000.0 / fps,
        loop = 0,
    )


if __name__ == "__main__":
    # default usage: rotate and saturate ship.png -> movie_rotate_and_sat.png
    create_rotate_and_saturate_animation(
        "dog1.jpg",
        "movie_rotate_and_sat.png",
        frames = 314,
        fps = 60,
        sMin = 0.0,
        sMax = 1.0,
    )
