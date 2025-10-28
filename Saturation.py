from PIL import Image

img = Image.open("input.webp").convert("RGB")
pixels = img.load()
width, height = img.size

# saturation
factor = 1.5  

for y in range(height):
    for x in range(width):
        r, g, b = pixels[x, y]

        # turn rgb to hsl values
        rf = r/255.0
        gf = g/255.0
        bf = b/255.0

        # from here on hue(h), saturation(s), lightness(l)
        maxForLightness = max(rf, gf, bf)
        minForLightness = min(rf, gf, bf)
        l = (maxForLightness + minForLightness) / 2.0

        if maxForLightness == minForLightness:
            # this means no color, so hue and sat are 0
            h = s = 0.0
        else:
            difLight = maxForLightness - minForLightness
            if l > 0.5:
                s = difLight / (2.0 - maxForLightness - minForLightness)
            else:
                s = difLight / (maxForLightness + minForLightness)

            # hue calc
            if maxForLightness == rf:
                h = (gf - bf) / difLight
                if gf < bf:
                    h += 6
            elif maxForLightness == gf:
                h = (bf - rf) / difLight + 2
            else:
                h = (rf - gf) / difLight + 4

            h /= 6.0

        # apply saturation factor and clamp
        s = max(0.0, min(1.0, s * factor))

        # convert HSL back to RGB
        c = (1 - abs(2 * l - 1)) * s
        h_prime = h * 6.0  # sector 0..6
        x_ch = c * (1 - abs((h_prime % 2) - 1))

        if 0 <= h_prime < 1:
            r1, g1, b1 = c, x_ch, 0
        elif 1 <= h_prime < 2:
            r1, g1, b1 = x_ch, c, 0
        elif 2 <= h_prime < 3:
            r1, g1, b1 = 0, c, x_ch
        elif 3 <= h_prime < 4:
            r1, g1, b1 = 0, x_ch, c
        elif 4 <= h_prime < 5:
            r1, g1, b1 = x_ch, 0, c
        else:
            r1, g1, b1 = c, 0, x_ch

        m = l - c / 2
        r_out = int(round((r1 + m) * 255))
        g_out = int(round((g1 + m) * 255))
        b_out = int(round((b1 + m) * 255))

        # clamp final values to [0,255]
        r_out = max(0, min(255, r_out))
        g_out = max(0, min(255, g_out))
        b_out = max(0, min(255, b_out))

        pixels[x, y] = (r_out, g_out, b_out)

img.save("./output.png")
