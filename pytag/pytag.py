
import os 

from os import listdir
from os.path import isfile, join

import PIL
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

import datetime

supported_formats = ['.jpeg','.jpg','.bmp','.png']
mainpath = os.path.dirname(os.path.realpath(__file__))
importpath= join(mainpath,"import")
exportpath= join(mainpath,"export")
exportednames = join(exportpath,"exportednames.txt")

# Algorithm https://newbedev.com/pil-how-to-scale-text-size-in-relation-to-the-size-of-the-image
def find_optimal_fontsize(img_fraction, fontpath, text, width):
    breakpoint = img_fraction * width
    jumpsize = 2
    fontsize = 16
    tw = 0
    th = 0
    
    font = ImageFont.truetype(fontpath, fontsize)
    while True:
        tw, th = font.getsize(text)
        if tw < breakpoint:
            fontsize += jumpsize
        else:
            jumpsize = jumpsize // 2
            fontsize -= jumpsize
        font = ImageFont.truetype(fontpath, fontsize)
        if jumpsize <= 1:
            break
    
    return (fontsize, tw, th)

def add_text(pil_img, text, color):
    width, height = pil_img.size
    
    fontpath = "arial.ttf"
    fontsize, tw, th = find_optimal_fontsize(1, fontpath, text, width)
    font = ImageFont.truetype(fontpath, fontsize)
    
    # Calculate margin
    new_width = max(width,tw)
    new_height = height + th
    
    # Create margin and paste the image top left
    result = Image.new('RGB', (new_width, new_height), color)
    result.paste(pil_img, (0, 0))
    
    # add text on top
    # x0, y0 = (0, height-h)
    # x1, y1 = (max(width, w), height)
    #draw.rectangle((x0, y0, x1, y1), fill='white')
    #draw.text((x0, y0), text, fill=(0, 0, 0), font=font)
    draw = ImageDraw.Draw(result)
    draw.text((0, height), text, fill=(0, 0, 0), font=font)

    return result



if __name__ == "__main__":

    onlyfiles = [f for f in listdir(importpath) if isfile(join(importpath, f)) and os.path.splitext(f)[1].lower() in supported_formats]
    onlyfiles.sort()
    
    with open(exportednames,'w') as f:
        # Draw Image with a tag
        for filename in onlyfiles:
            img = Image.open(join(importpath,filename))


            # Tag
            datenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            tag = "[%s]"%(os.path.splitext(filename)[0])
            text = "%s %s"%(tag,datenow)
            
            f.write(tag+"\n")
            
            # Draw
            img = add_text(img,text,"white")
            
            # Save file
            img.save(join(exportpath, filename))
