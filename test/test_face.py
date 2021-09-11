import unittest
import portrait
from PIL import Image


def xtest_random_color():
    img = Image.open("images/base.png")
    img = Image.new('RGB', (img.size[0], img.size[1]))
    background_color = portrait.get_random_color()
    img = portrait.apply_per_pixel(img, [portrait.shift_color_factory(portrait.FULL_COLOR_RANGE, background_color)])
    img.show()
    assert False


class TestMyImage(unittest.TestCase):

    def xtest_init(self):
        self.assertIsNotNone(portrait.MyImage())


class TestFace(unittest.TestCase):

    def xtest_get_random_skintone(self):
        result = portrait.get_random_skintone()
        self.assertIsNotNone(result)
        assert len(result) == 3

    def xtest_colorize_face(self):
        face = portrait.Face(asymmetry=1.2)
        # img = portrait.get_random_from("faces")
        # base_skin_color = ((210, 256), (210, 256), (0, 70))
        # random_skin_tone = portrait.get_random_skintone()
        # shift_skintone = portrait.shift_color_factory(base_skin_color, random_skin_tone)
        # img = portrait.apply_per_pixel(img, [shift_skintone, portrait.shift_color_blue_to_black])
        face.img.show()
        # assert False

    def xtest_get_random_hair_color(self):
        for i in range(30):
            color = portrait.get_random_hair_color()
            print(color)
            img = Image.new('RGB', (50, 50))
            shift_visible_color = portrait.shift_color_factory(portrait.FULL_COLOR_RANGE, color)
            img = portrait.apply_per_pixel(img, [shift_visible_color])
            img.save("images/results/%s.png" % "_".join([str(n) for n in color]))
        assert False

    def xtest_init(self):
        self.assertIsNotNone(portrait.Face())

    # def xtest_show(self):
    #     face = Face()
    #     face.img.show()

    # def xtest_place_eyes(self):
    #     face = Face()
    #     face.place_eyes("test/resources/left_eye.png", -3, -4)
    #     face.img.show()

    # def xtest_place_eyes_asym(self):
    #     face = Face(asymmetry=1.2)
    #     face.place_eyes("images/eyes/Layer 015.png")
    #     face.img.show()

    def test_place_eyes_and_nose_and_mouth(self):
        for i in range(10):
            face = portrait.Face(asymmetry=1.2)
            face.img.img.save("images/results/%s.png" % i)
            # face.img.img.show()
        # assert False


class TestPosition(unittest.TestCase):

    def test_init(self):
        self.assertIsNotNone(portrait.Position(2, 3))

    def test_iter(self):
        pos = portrait.Position(2, 3)
        x, y = pos
        self.assertEqual(x, 2)
        self.assertEqual(y, 3)


if __name__ == '__main__':
    unittest.main()