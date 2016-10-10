import os
import unittest

import datetime

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
            print f
            self.binarization_0(f)
            # break

    def binarization_0(self, file_path):
        ocrer = DataImageOCRer(file_path)
        ocrer.get_subscribe_num()
        ocrer.get_deal_num()

    @unittest.skip('Do NOT call this method This function is only for data fixing')
    def test_fix_data(self):
        # TODO: This function is only for data fixing
        images = []
        image_dir = '/home/dqian/dev/scv/src/scv/running/data/images/'
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
        ocr = DataImageOCRer(img_path)
        subscribe_num = ocr.get_subscribe_num()
        deal_num = ocr.get_deal_num()
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


if __name__ == '__main__':
    unittest.main()
