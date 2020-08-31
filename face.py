from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import random
import os

class GraphicalEntity(object):

    asymmetry_factor = 15
    def __init__(self, img, pos, size=None):
        self.img = img
        self.pos = pos
        self.size = size

    def move(self, new_pos):
        self.pos = new_pos

    def resize(self, new_size):
        self.size = new_size


class Face(GraphicalEntity):
    def __init__(self, asymmetry=0.0):
        img = Image.open("images/Layer 002.png")
        hair = Image.open("images/Layer 026.png")
        img = paste(img, hair, 0, 0)
        self.asymmetry = asymmetry
        super(Face, self).__init__(img, Position(0, 0), Size(0, 0))

    def get_random_eye(self):
        return get_random_from("images/eyes")

    def get_random_nose(self):
        return get_random_from("images/noses")

    def get_random_mouth(self):
        return get_random_from("images/mouths")

    def place_eyes(self, eye_path, offset_x=0, offset_y=0):
        eye = Image.open(eye_path)
        angle = int(random.uniform(-1, 1) * 20)
        print(angle)
        eye = eye.rotate(angle)
        x1, y1 = self.get_random_offset()
        self.img = paste(self.img, eye, x1, y1)
        mirrored_eye = ImageOps.mirror(eye)
        x2, y2 = self.make_coords_asymmetrical(x1, y1)
        self.img = paste(self.img, mirrored_eye, x2, y2)

    def place_nose(self, path, offset_x=0, offset_y=0):
        nose = Image.open(path)
        y_shift = int(random.uniform(-self.asymmetry_factor, self.asymmetry_factor))
        self.img = paste(self.img, nose, 0, y_shift)

    def place_mouth(self, path, offset_x=0, offset_y=0):
        mouth = Image.open(path)
        y_shift = int(random.uniform(-self.asymmetry_factor, self.asymmetry_factor))
        self.img = paste(self.img, mouth, 0, y_shift)

    def get_random_offset(self):
        x = int(random.uniform(-1, 1) * self.asymmetry_factor)
        y = int(random.uniform(-1, 1) * self.asymmetry_factor)
        return x, y

    def make_coords_asymmetrical(self, x, y):
        x += int(random.uniform(-self.asymmetry, self.asymmetry) * self.asymmetry_factor)
        y += int(random.uniform(-self.asymmetry, self.asymmetry) * self.asymmetry_factor)
        return -x, y



class Eye(GraphicalEntity):
    def __init__(self):
        pass

class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iter__(self):
        return iter([self.x, self.y])

class Size(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __iter__(self):
        return iter([self.x, self.y])

def paste(im1, im2, x, y):
    back_im = im1.copy()
    back_im.paste(im2, (x, y), mask=im2)
    return back_im


def get_random_from(directory):
    choice = ""
    retries = 0
    while not choice.endswith(".png") and retries < 20:
        retries += 1
        choice = random.choice(os.listdir(directory))
    return os.path.join(directory, choice)
