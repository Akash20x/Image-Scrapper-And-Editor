from PIL import ImageFilter, Image, ImageDraw, ImageFont
# Basic features of the editor



def resize(im, x, y):
    im = im.resize((x,y))
    return im

def draw_point(im, x, y, color):

    for x_coord in range(x-3, x+3):
        for y_coord in range(y-3, y+3):
            im.putpixel((x_coord,y_coord), color)
    
    return im

def add_text(im, x, y, content, color):
    im = im.convert("RGBA")
    d = ImageDraw.Draw(im)
    font = ImageFont.truetype("comic.ttf", 20)

    d.text((x,y), content, fill=color, font=font)

    return im

def pick_color(im, x, y):

    color = im.getpixel((x,y))
    return color

def draw_line(im, x1, y1, x2, y2, color):

    d = ImageDraw.Draw(im)
    d.line([(x1, y1), (x2, y2)], fill=color, width=3)

    return im