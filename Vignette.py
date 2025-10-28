from PIL import Image
import math

# apply a vignette effect to an image using PIL only
def apply_vignette(input_path, output_path, strength=0.5):
    # open the image and convert to RGB
    img = Image.open(input_path).convert("RGB")
    width, height = img.size
    pixels = img.load()

    # calculate the center of the image
    cx = width / 2.0
    cy = height / 2.0
    max_dist = math.sqrt(cx ** 2 + cy ** 2)

    # create a new image for output
    out_img = Image.new("RGB", (width, height))
    out_pixels = out_img.load()

    for x in range(width):
        for y in range(height):
            # calculate distance from center
            dx = x - cx
            dy = y - cy
            dist = math.sqrt(dx ** 2 + dy ** 2)
            # normalize distance
            norm = dist / max_dist
            # make vignette effect even stronger by increasing the exponent and strength
            factor = 1.0 - strength * (norm ** 4)
            # clamp factor to [0, 1]
            factor = max(0.0, min(1.0, factor))
            # get original pixel
            r, g, b = pixels[x, y]
            # apply vignette factor
            r = int(r * factor)
            g = int(g * factor)
            b = int(b * factor)
            # set pixel in output image
            out_pixels[x, y] = (r, g, b)

    # save the output image
    out_img.save(output_path)

if __name__ == "__main__":
    # example usage: apply vignette to input.webp and save as ship_vignette.png
    apply_vignette("input.webp", "ship_vignette.png", strength=1.2)
