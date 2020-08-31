from PIL import Image, ImageFilter, ImageEnhance, ImageOps
# import numpy as np
import random


def mirror_test(im):
    width, height = im.size
    bg = Image.new('RGBA', (width * 2, height), (0, 0, 0, 0))
    im_mirror = ImageOps.mirror(im)
    bg = paste(bg, im, 0, 0)
    bg = paste(bg, im_mirror, width, 0)
    return bg

def paste(im1, im2, x, y):
    back_im = im1.copy()
    back_im.paste(im2, (x, y), mask=im2)
    return back_im

def shift_color(im):
    im = im.convert('RGBA')
     
    pixdata = im.load()
    rr = random.randint(0, 256)
    rg = random.randint(0, 256)
    rb = random.randint(0, 256)
    for y in xrange(im.size[1]):
        for x in xrange(im.size[0]):
            r, g, b, a = pixdata[x, y]
            # if r > 20:
            # pixdata[x, y] = (b, r, g, 255)

            pixdata[x, y] = (rr, rg, rb, a)
    return im

def convert_to_grayscale(im):
    im = im.convert('RGBA')
     
    pixdata = im.load()
    for y in xrange(im.size[1]):
        for x in xrange(im.size[0]):
            r, g, b, a = pixdata[x, y]
            # if r > 20:
            # pixdata[x, y] = (b, r, g, 255)
            avg = sum([r, g, b])/3

            pixdata[x, y] = (avg, avg, avg, a)
    return im

def place_eye(face, eye, eyebrow):
    width, height = face.size
    resized_eye = eye.thumbnail((width/4, width/4), Image.ANTIALIAS)
    # eyebrow.show()
    resized_eyebrow = eyebrow.thumbnail((width/2, width/2), Image.ANTIALIAS)
    eyebrow = shift_color(eyebrow)

    with_eye = paste(face, eye, int(width/1.5), int(height/2.5))
    with_eyebrow = paste(with_eye, eyebrow, int(width/2.5), int(height/4))
    return with_eyebrow

# def transparency(im, value):
#     im = im.convert('RGBA')
     
#     pixdata = im.load()

#     for y in xrange(im.size[1]):
#         for x in xrange(im.size[0]):
#             r, g, b, a = pixdata[x, y]
#             pixdata[x, y] = (r, g, b, a * value)
#     return im


def avg(l):
    return sum(l)/len(l)

def colorize_grayscale(im, darks, lights, midpoint=256/2):
    print(darks)
    print(lights)
    im = im.convert('RGBA')
    # dr, dg, db = darks
    hsl_darks = rgb_to_hsl(darks)
    hsl_lights = rgb_to_hsl(lights)

    # lr, lg, lb = lights
    pixdata = im.load()
    for y in xrange(im.size[1]):
        for x in xrange(im.size[0]):
            is_dark = False
            r, g, b, a = pixdata[x, y]
            # decide if it's light or dark
            tone = avg([r, g, b]) # same as r or g or b
            if tone < midpoint:
                # hsl = rgb_to_hsl(darks)
                hsl = (hsl_darks[0], hsl_darks[1], avg([hsl_darks[2], tone])/float(255))
                r, g, b = hsl_to_rgb(hsl)
            else:
                hsl = (hsl_lights[0], hsl_lights[1], avg([hsl_lights[2], tone])/float(255))
                # hsl[3] = tone/float(255)
                r, g, b = hsl_to_rgb(hsl)
            pixdata[x, y] = (int(r), int(g), int(b), a)
    return im

def rgb_to_hsl(rgb):
    r, g, b = rgb

    R = r / float(255)
    G = g / float(255)
    B = b / float(255)

    high = max(R, G, B)
    low = min(R, G, B)
    print("high %s" % high)
    print("low %s" % low)

    luminance = avg([high, low])

    if luminance < 0.5:
        saturation = (high - low) / (high + low)
    else:
        saturation = (high - low)/ (2.0 - high - low)

    if R == high:
        hue = (G - B) / (high - low)
    if G == high:
        hue = (B - R) / (high - low)
    if B == high:
        hue = 4.0 + (R - G) / (high - low)

    hue = hue * 60

    return (hue, saturation, luminance)

def hsl_to_rgb(hsl):
    h, s, l = hsl
    if l < 0.5:
        temporary_1 = l * (1.0 + s)
    else:
        temporary_1 = l + s - l * s
    temporary_2 = 2 * l - temporary_1
    h = h/360

    R = normalize(h + 0.333, temporary_1, temporary_2)
    G = normalize(h, temporary_1, temporary_2)
    B = normalize(h - 0.333, temporary_1, temporary_2)
    return (R, G, B)


def normalize(color, val1, val2):
    if color < 0:
        color += 1
    if color > 1:
        color -= 1
    
    if 6 * color < 1:
        r = val2 + (val1 - val2) * 6 * color
    elif 2 * color < 1:
        r = val1
    elif 3 * color < 2:
        r = val2 + (val1 - val2) * (0.666 - color) * 6
    else:
        r = color
    return r * 255

def place_nose(face, nose):
    width, height = face.size
    w, h = nose.size
    # PIL.ImageChops.multiply(image1, image2)
    out = paste(face, nose, width/2 - w/2, int(height/1.8) - h/2)
    return out

def place_mouth(face, mouth):
    pass

def face():
    with Image.open("images/face.png") as im1:
        with Image.open("images/red_dot.png") as im2:
            im3 = Image.open("images/eyebrow.png")
            nose = Image.open("images/nose.png")
            # out = im.filter(ImageFilter.BLUR)
            # out = im.point(lambda i: i * 1.2)  # higher contrast
            # out = shift_color(im1)
            # out = paste(out, im2, 10, 10)
            width, height = im1.size
            im1 = im1.crop((0, 0, width/2, height))
            out = place_eye(im1, im2, im3)
            out = mirror_test(out)
            out = place_nose(out, nose)
            out.save("images/result.png")

def grayscale_test():
    with Image.open("images/face.png") as im1:
        im = convert_to_grayscale(im1)
        im.show()
        im = colorize_grayscale(im, (84, 0, 102), (255, 255, 10))
        im.show()

if __name__ == "__main__":
    grayscale_test()
