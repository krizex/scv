import os
import unittest

from scv.recognize.ocr import DataImageOCRer


class TestDataImageOCRer(unittest.TestCase):
    def test_recognize(self):
        images = []
        image_dir = '/home/dqian/dev/scv/src/scv/running/data/images/'
        for f in os.listdir(image_dir):
            if not f.endswith('.jpg'):
                continue
            real_f = os.path.join(image_dir, f)
            images.append(real_f)

        for f in images:
            self.binarization_0(f)
            # break


    def binarization(self, file_path):
        ocrer = DataImageOCRer(file_path)
        subscribe_box = (71, 64, 116, 78)
        image = ocrer.clip_image(subscribe_box)
        image = image.convert('1')
        pixdata = image.load()
        for y in xrange(image.size[1]):
            for x in xrange(image.size[0]):
                # print pixdata[x, y]
                if pixdata[x, y] == 255:
                    print '0',
                else:
                    print 1,

            print ''

    def binarization_0(self, file_path):
        ocrer = DataImageOCRer(file_path)
        ocrer.get_subscribe_num()



if __name__ == '__main__':
    unittest.main()
