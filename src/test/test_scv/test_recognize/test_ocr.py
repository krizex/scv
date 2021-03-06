import os
import unittest
import datetime
from scv.recognize.ocr import DataImageOCRer
from scv.runner.run import Runner


class TestDataImageOCRer(unittest.TestCase):
    def setUpClass(cls):
        runner = Runner()
        cls.recognizer = runner.recognizer

    def test_recognize(self):
        images = []
        image_dir = os.path.join(os.path.dirname(__file__), '../../../scv/running/data/images')
        for f in os.listdir(image_dir):
            if not f.endswith('.jpg'):
                continue
            real_f = os.path.join(image_dir, f)
            images.append(real_f)

        for f in images:
            print(f)
            self.binarization_0(f)
            # break

    def binarization_0(self, file_path):
        ocrer = DataImageOCRer(file_path, self.recognizer)
        ocrer.recognize_subscribe_num()
        ocrer.recognize_deal_num()

    # @unittest.skip('Do NOT call this method This function is only for data fixing')
    def test_fix_data(self):
        # TODO: This function is only for data fixing
        images = []
        image_dir = os.path.join(os.path.dirname(__file__), '../../../scv/running/data/images')
        for f in os.listdir(image_dir):
            if not f.endswith('.jpg'):
                continue

            real_f = os.path.join(image_dir, f)
            data_time = f.split('.jpg')[0]
            data_time = datetime.datetime.strptime(data_time, '%Y%m%d')
            data_time -= datetime.timedelta(days=1)

            images.append((real_f, data_time))

        for image in images:
            self.fix_data(image[0], image[1])

    def fix_data(self, img_path, data_time):
        ocr = DataImageOCRer(img_path, self.recognizer)
        subscribe_num = ocr.recognize_subscribe_num()
        deal_num = ocr.recognize_deal_num()
        from pymongo.errors import DuplicateKeyError
        try:
            from scv.db.db import DBManager
            DBManager.delete_record({'date': data_time.strftime("%Y%m%d")})
            DBManager.insert_record({
                'date': data_time.strftime("%Y%m%d"),
                'subscribe': subscribe_num,
                'deal_num': deal_num
            })
        except DuplicateKeyError:
            pass

    def test_split(self):
        images = []
        image_dir = os.path.join(os.path.dirname(__file__), '../../../scv/running/data/images')
        for f in os.listdir(image_dir):
            if not f.endswith('.jpg'):
                continue

            real_f = os.path.join(image_dir, f)
            data_time = f.split('.jpg')[0]
            data_time = datetime.datetime.strptime(data_time, '%Y%m%d')
            data_time -= datetime.timedelta(days=1)

            images.append((real_f, data_time))

        ret = []
        for image in images:
            print(os.path.basename(image[0]))
            a, b = self.split(image[0])
            ret.append(a)
            ret.append(b)

    def split(self, image):
        ocr = DataImageOCRer(image, self.recognizer)
        subscribe_split = ocr.get_subscribe_number_feature()

        deal_split = ocr.get_deal_number_feature()

        return subscribe_split, deal_split

if __name__ == '__main__':
    unittest.main()
