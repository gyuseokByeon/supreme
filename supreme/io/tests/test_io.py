import os.path
from glob import glob

from numpy.testing import *
import numpy as np

from supreme.io import *

class TestImage:
    def setUp(self):
        self.image = Image(np.arange(100).reshape((10,10)))
        self.image2 = Image(np.arange(10), filename='foo.jpg')
        assert_equal(self.image2.filename, 'foo.jpg')

    def test_pickle(self):
        self.image.filename = 'image.jpg'
        import pickle as P
        image = P.loads(P.dumps(self.image))
        assert_equal(image.filename, 'image.jpg')

    def test_image_of_image(self):
        x = Image(Image(np.arange(1), filename='stored.jpg'))
        assert_equal(x.filename, 'stored.jpg')

class TestImageCollection:
    data_path = os.path.dirname(__file__)
    data_glob = os.path.join(data_path, '*.png')
    images = [imread(os.path.join(data_path, 'data%d.png' % i))
              for i in range(3)]
    data_files = glob(data_glob)

    def setUp(self):
        self.c = ImageCollection(self.data_glob)

    def test_len(self):
        assert_equal(len(self.c), 3)

    def test_images(self):
        assert_array_equal(self.c[0], self.images[0])
        assert_equal(self.c[0].filename, 'data0.png')

        assert_array_equal(self.c[2], self.images[2])
        assert_array_equal(self.c[1], self.images[1])

    def test_iterate(self):
        for i, img in enumerate(self.c):
            assert_array_equal(img, self.c[i])
            assert_array_equal(img, self.images[i])

    def test_tags(self):
        ic = ImageCollection(os.path.join(self.data_path, 'exif_tagged.jpg'))
        img = ic[0]
        assert_equal(str(img.EXIF['EXIF ExposureTime']), '1/60')
        assert_equal(img.filename, 'exif_tagged.jpg')
        assert_almost_equal(img.exposure, 1/60.)

        img.info['x'] = 3
        img2 = (img + np.array([1,2,3]))
        assert_equal(img2.info['x'], 3)

    def test_grey(self):
        ic = ImageCollection(self.data_glob, grey=True)
        for img in ic:
            assert_equal(img.ndim, 2)

    def test_repr(self):
        im_path = os.path.join(self.data_path, 'exif_tagged.jpg')
        ic = ImageCollection(im_path)
        assert_equal(str([im_path]), str(ic))

    def test_files_list(self):
        c2 = ImageCollection(self.data_files)
        assert_equal(self.c.files, c2.files)

class TestImageCollection_do_not_conserve_memory(ImageCollection):
    def setUp(self):
        self.c = ImageCollection(self.data_glob, conserve_memory=False)

if __name__ == "__main__":
    run_module_suite()

