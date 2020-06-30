#! /usr/bin/env python
from PIL import Image  # Python Image Library - Image Processing
import glob
import os, sys

for infile in glob.glob("*.png"):
    f, e = os.path.splitext(infile)
    outfile = f + ".jpg"
    print(outfile)
    if infile !=  outfile:
        try:
            image = Image.open(infile)

            #new image with white background
            new_image = Image.new("RGBA", image.size, "WHITE")

            #paste the image on the new background
            new_image.paste(image, (0, 0), image)

            #convert the image and save it in JPEG format
            new_image.convert('RGB').save(outfile, quality=100)

        except IOError:
            print("Can not conver", infile)