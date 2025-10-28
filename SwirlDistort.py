from PIL import Image
import math

def apply_swirl_vignette(input_path, output_path, swirl_strength=10, vignette_strength=0.5):
    # spent way too long on this
    
    # load up the image 
    img = Image.open(input_path).convert("RGB")
    width, height = img.size
    
    out_img = Image.new("RGB", (width, height))
    pixels = img.load()
    out_pixels = out_img.load()
    
    # find the middle 
    center_x = width / 2
    center_y = height / 2
    
    # this is for the vignette 
    max_radius = math.sqrt(center_x**2 + center_y**2)
    
    for y in range(height):
        for x in range(width):
            # figure out how far we are from the center
            dx = x - center_x
            dy = y - center_y
            
            radius = math.sqrt(dx**2 + dy**2)
            theta = math.atan2(dy, dx)
            
            # this makes the swirl stronger in the middle
            swirl_factor = 1 - (radius / max_radius)
            new_theta = theta + swirl_strength * swirl_factor
            
            # convert back from polar coords 
            new_x = center_x + radius * math.cos(new_theta)
            new_y = center_y + radius * math.sin(new_theta)
            
            # make sure we don't go outside the image
            new_x = int(max(0, min(width - 1, new_x)))
            new_y = int(max(0, min(height - 1, new_y)))
            
            # grab the pixel from the swirled position
            r, g, b = pixels[new_x, new_y]
            
            # now add the vignette effect
            norm = radius / max_radius
            # make edges darker 
            factor = 1.0 - vignette_strength * (norm ** 4)
            factor = max(0.0, min(1.0, factor))
            
            # apply the darkness to our swirled pixel
            r = int(r * factor)
            g = int(g * factor)
            b = int(b * factor)
            
            out_pixels[x, y] = (r, g, b)
    
    out_img.save(output_path)

if __name__ == "__main__":
    apply_swirl_vignette("input.webp", "output_swirl_vignette.png", 
                        swirl_strength=15,  # more/less swirl
                        vignette_strength=1.2)  # max this at like 2