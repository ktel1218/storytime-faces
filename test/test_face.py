import unittest
from face import Face, Position


class TestFace(unittest.TestCase):

    def test_init(self):
        self.assertIsNotNone(Face())

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
        for i in range(25):
            face = Face(asymmetry=1.2)
            face.place_eyes(face.get_random_eye())
            face.place_nose(face.get_random_nose())
            face.place_mouth(face.get_random_mouth())
            face.img.save("images/results/%s.png" % i)
            # face.img.show()

class TestPosition(unittest.TestCase):
    
    def test_init(self):
        self.assertIsNotNone(Position(2, 3))

    def test_iter(self):
        pos = Position(2, 3)
        x, y = pos
        self.assertEqual(x, 2)
        self.assertEqual(y, 3)

if __name__ == '__main__':
    unittest.main()