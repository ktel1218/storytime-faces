from PIL import Image, ImageOps
import random
import os


FULL_COLOR_RANGE = ((0, 256), (0, 256), (0, 256))

GRAY_HAIR_THRESHOLD = 215


class MyImage(object):

    def __init__(self):
        img = Image.open("images/base.png")
        self._img = Image.new('RGBA', (img.size[0], img.size[1]), (0, 255, 0, 255))
        self.pixdata = img.load()
        self.width = img.size[0]
        self.height = img.size[1]
        self.colorizers = [shift_color_factory(((0, 40), (210, 256), (0, 40)), get_random_color())]

    @property
    def img(self):
        return self._img

    @img.setter
    def img(self, img):
        self.pixdata = img.load()
        self._img = img

    # def tag_pixels(self, new_img, tag):
    #     new_img = new_img.load()
    #     for y in xrange(self.height):
    #         for x in xrange(self.width):
    #             r, g, b, a = new_img[x, y]
    #             if a > 8:
    #                 self.tagged_pixels[(x, y)] = tag

    # def merge(self):
    #     for y in range(self.height):
    #         for x in range(self.width):
    #             cumulative_alpha = 0
    #             for i in range(1, len(self.feature_stack) - 1):
    #                 r, g, b, alpha_channel = self.feature_stack[-i]
    #                 cumulative_alpha += alpha_channel

    def paste(self, new_img, tag=None, colorizers=[], x_offset=0, y_offset=0):
        self.colorizers.extend(colorizers)
        if x_offset or y_offset or self.width != new_img.size[0] or self.height != new_img.size[1]:
            backing = Image.new('RGBA', (self.width, self.height))
            backing.paste(new_img, (x_offset, y_offset))
            new_img = backing
        self.img = Image.alpha_composite(self.img, new_img)

    def colorize(self):
        for y in xrange(self.height):
            for x in xrange(self.width):
                r, g, b, a = self.pixdata[x, y]
                colors = []
                for func in self.colorizers:
                    mapping = func(r, g, b, a)
                    if mapping:
                        # r, g, b, a = mapping
                        colors.append(mapping)
                if colors:
                    self.pixdata[x, y] = average_rgbas(colors)


def average_rgbas(rgbas):
    length = len(rgbas)
    rs = [color[0] for color in rgbas]
    gs = [color[1] for color in rgbas]
    bs = [color[2] for color in rgbas]
    _as = [color[3] for color in rgbas]
    avg_r = sum(rs)/length
    avg_g = sum(gs)/length
    avg_b = sum(bs)/length
    avg_a = sum(_as)/length
    return (avg_r, avg_g, avg_b, avg_a)


class GraphicalEntity(object):

    asymmetry_factor = 3

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
        self.asymmetry = asymmetry
        img = MyImage()
        # img = apply_per_pixel(img, [shift_color_factory(FULL_COLOR_RANGE, background_color)])
        super(Face, self).__init__(img, Position(0, 0), Size(0, 0))
        random_skintone = get_random_skintone()
        random_hair_color = get_random_hair_color(skintone=random_skintone)
        pink_range = ((170, 256), (0, 30), (100, 160))
        purple_range = ((170, 256), (0, 30), (170, 256))
        self.hair_colorizer = shift_color_factory(pink_range, random_hair_color)
        darker_hair_color = [int(x/1.25) for x in random_hair_color]
        self.back_hair_colorizer = shift_color_factory(purple_range, darker_hair_color)
        self.eyebrow_colorizer = shift_color_factory(purple_range, darker_hair_color)
        base_yellow_range = ((90, 256), (90, 256), (0, 150))
        self.skin_colorizer = shift_color_factory(base_yellow_range, random_skintone)

        self.place_hair_back()
        self.place_shoulders()
        self.place_ears()
        self.place_neck()
        self.place_face()
        self.place_eyes_and_eyebrows()
        self.place_nose(get_random_from("noses"))
        self.place_mouth(get_random_from("mouths"))
        self.place_hair_front()
        self.img.colorize()

    def place_shoulders(self):
        shoulders = Image.open("images/shoulders.png")
        self.img.paste(shoulders)

    def place_neck(self):
        neck = get_random_from("necks")
        self.img.paste(neck, "neck", [self.skin_colorizer, shift_color_blue_to_black])

    def place_face(self):
        face = get_random_from("faces")
        self.img.paste(face, "face", [self.skin_colorizer, shift_color_blue_to_black])

    def place_ears(self):
        ear = get_random_from("ears")
        mirrored_ear = ImageOps.mirror(ear)
        ears = Image.alpha_composite(ear, mirrored_ear)
        self.img.paste(ears, "ears", [self.skin_colorizer, shift_color_blue_to_black])

    def place_hair_back(self):
        hair_back = get_random_from("hair_back", orNone=True)
        self.img.paste(hair_back, "hair_back", [self.back_hair_colorizer])

    def place_hair_front(self):
        hair_front = get_random_from("hair_front", orNone=True)
        self.img.paste(hair_front, "hair_front", [self.hair_colorizer])

    def place_eyes_and_eyebrows(self):
        off_x, off_y = self.place_eyes(get_random_from("eyes"))
        self.place_eyebrows(get_random_from("eyebrows"), off_x, off_y)

    def place_eyes(self, eye, offset_x=0, offset_y=0):
        angle = int(random.uniform(-1, 1) * 20)
        eye = eye.rotate(angle)
        x1, y1 = self.get_random_offset()
        mirrored_eye = ImageOps.mirror(eye)
        # x2, y2 = self.make_coords_asymmetrical(x1, y1)
        eyes = Image.alpha_composite(eye, mirrored_eye)
        self.img.paste(eyes, "eyes", [shift_color_blue_to_black], x1, y1)
        return (x1, y1)

    def place_eyebrows(self, eyebrow, offset_x=0, offset_y=0):
        angle = int(random.uniform(-1, 1) * 20)
        eyebrow = eyebrow.rotate(angle)
        mirrored_eyebrow = ImageOps.mirror(eyebrow)
        # x2, y2 = self.make_coords_asymmetrical(offset_x, offset_y)
        # eyebrows = paste(eyebrow, mirrored_eyebrow)
        eyebrows = Image.alpha_composite(eyebrow, mirrored_eyebrow)
        self.img.paste(eyebrows, "eyebrows", [self.eyebrow_colorizer], offset_x, offset_y - random.randint(20, 40))

    def place_nose(self, nose, offset_x=0, offset_y=0):
        # nose = apply_per_pixel(nose)
        y_shift = int(random.uniform(-self.asymmetry_factor, self.asymmetry_factor))
        self.img.paste(nose, "nose", [shift_color_blue_to_black], 0, y_shift)

    def place_mouth(self, mouth, offset_x=0, offset_y=0):
        # mouth = apply_per_pixel(mouth, [shift_color_blue_to_black])
        y_shift = int(random.uniform(-self.asymmetry_factor, self.asymmetry_factor))
        self.img.paste(mouth, "mouth", [shift_color_blue_to_black], 0, y_shift)

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


def paste(im1, im2, x=0, y=0):
    back_im = im1.copy()
    back_im.paste(im2, (x, y), mask=im2)
    return back_im


def apply_per_pixel(img, funcs):
    img = img.convert('RGBA')

    pixdata = img.load()
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            r, g, b, a = pixdata[x, y]
            for func in funcs:
                mapping = func(r, g, b, a)
                if mapping:
                    # r, g, b, a = mapping
                    pixdata[x, y] = mapping

    # print colors
    return img


def shift_color_blue_to_black(r, g, b, a):
    if (r < 80 and g < 50 and b > 40):
        return (0, 0, 0, a)


def min_max(value, low=0, high=256):
    return min(high, max(value, low))


def get_random_skintone():
    rr = min_max(random.randint(70, 256))
    rg = min_max(rr - random.randint(30, 50))
    rb = min_max(rg - random.randint(30, 50))
    return (rr, rg, rb)


def get_dark_skintone():
    rr = min_max(random.randint(70, 110))
    rg = min_max(rr - random.randint(30, 50))
    rb = min_max(rg - random.randint(30, 50))
    return (rr, rg, rb)


def get_random_hair_color(skintone=None):
    weighted_base_colors = []
    for i in range(0, 256):
        if skintone:
            if skintone[0] - 20 < i < skintone[0] + 20:
                pass
            else:
                single_color_with_weight = [i] * max(1, ((256 - i/2)/8))
                weighted_base_colors += single_color_with_weight
    rr = min_max(random.choice(weighted_base_colors))
    percentage_of_r = random.randint(70, 78) * .01
    rg = min_max(int(percentage_of_r * rr))
    percentage_of_g = random.randint(25, 65) * .01
    rb = min_max(int(percentage_of_g * rg))
    if rr > 215:
        rb = rg = rr
    return (rr, rg, rb)


def get_random_color():
    r = random.randint(0, 256)
    g = random.randint(0, 256)
    b = random.randint(0, 256)
    print(r, g, b)
    return (r, g, b)


def shift_color_factory(from_color_range, to_color):
    def shift_to_color(r, g, b, a):
        r1, g1, b1 = from_color_range
        r2, g2, b2 = to_color
        if (r1[0] <= r <= r1[1] and g1[0] <= g <= g1[1] and b1[0] <= b <= b1[1]):
            return (r2, g2, b2, a)
    return shift_to_color


def get_random_from(directory, orNone=False):
    choice = ""
    retries = 0
    directory = os.path.join("images", directory)
    choices = os.listdir(directory)
    while not choice.endswith(".png") and retries < 20:
        retries += 1
        choice = random.choice(choices)
    img = Image.open(os.path.join(directory, choice))
    if orNone:
        rand = random.randint(0, len(choices))
        if rand == 0:
            img = Image.new('RGBA', (img.size[0], img.size[1]))
    return img
