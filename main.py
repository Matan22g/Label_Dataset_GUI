__author__ = "Matan Achiel"
__credits__ = ["Matan Achiel"]
__email__ = "matan22g@gmail.com"

import glob
import os
import pickle
import sys
from os.path import basename
from pathlib import Path

import cv2
from PyQt5.QtCore import QRect, Qt, QPoint
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QApplication, QGridLayout

"""
    Interactive select rectangle ROIs and store list of bounding rect.
    
    Parameters
    ----------
    IM_DIR_PATH :
        Image dir path - str.

    Can be input in two different ways:
    Via cmd like in the following way: "python main.py YOUR_DATA_SET_PATH"
    Via modifying the constant 'IM_DIR_PATH' below.
"""
IM_DIR_PATH = r"dataset"


class ImageLabel(QLabel):
    # Custom Label for displaying image, and for drawing rectangles"

    begin = QPoint()
    end = QPoint()

    rectangles = []

    # Mouse click event
    def mousePressEvent(self, event):
        self.begin = self.end = event.pos()
        self.update()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        r = QRect(self.begin, self.end).normalized()
        self.rectangles.append(r)
        self.begin = self.end = QPoint()
        self.update()
        super().mouseReleaseEvent(event)

    # Draw events
    def paintEvent(self, event):
        super().paintEvent(event)

        qp = QPainter(self)
        qp.setPen(QPen(Qt.blue, 2, Qt.SolidLine))

        for rectangle in self.rectangles:
            qp.drawRect(rectangle)

        if not self.begin.isNull() and not self.end.isNull():
            qp.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            qp.drawRect(QRect(self.begin, self.end).normalized())


class AnnotationGUI(QMainWindow):

    def __init__(self, im_dir_path):
        super().__init__()
        self.ext = ['png', 'jpg', 'jpeg']  # Add image formats here
        self.setWindowTitle("Annotation Tool")

        # images paths - for loading
        self.images = []
        self.index = 0  # for swiping between the images

        # keys = image name,
        # value = list of rectangles (i.e. [[c1, r1, w1, h1],[c2, r2, w2, h2],...])
        self.images_labels = {}

        self.im_dir = im_dir_path
        pickle_name = "results.pkl"
        self.pickle_file = str(Path(self.im_dir) / pickle_name)

        # Loading the images and the saved pickle
        self.load_data()

        # Create a main widget for the window
        mainWidget = QWidget(self)
        self.setCentralWidget(mainWidget)
        self.layout = QGridLayout(mainWidget)

        if self.images:  # Managed to load images
            self.imgLabel = ImageLabel()
            self.layout.addWidget(self.imgLabel)
            self.show_img(self.images[self.index])
        else:  # Empty dir or Invalid path
            self.label = QLabel("Invalid Path", self)

        self.show()

    def keyPressEvent(self, event):

        # Swiping Images
        if event.key() == Qt.Key_Left:
            self.index -= 1
        elif event.key() == Qt.Key_Right:
            self.index += 1

        # Deleting last rect
        elif event.key() == Qt.Key_D:
            im_name = basename(Path(self.images[self.index])).split('.')[0]
            if self.images_labels[im_name]:
                self.images_labels[im_name].pop(-1)

        # Saving keys
        elif event.key() == Qt.Key_S:
            self.save_data()
        elif event.key() == Qt.Key_Q:
            self.save_data()
            sys.exit(app.exec_())

        # Rotational swiping using modulo
        self.index = self.index % len(self.images)
        self.show_img(self.images[self.index])

    def show_img(self, im_path):
        # Loading the image and setting the corresponding rectangles

        im_name = basename(Path(im_path)).split('.')[0]
        rgb_array = cv2.imread(im_path)
        rgb_array = cv2.cvtColor(rgb_array, cv2.COLOR_BGR2RGB)

        h, w, ch = rgb_array.shape
        bytesPerLine = ch * w
        qImg = QImage(rgb_array.data, w, h, bytesPerLine, QImage.Format_RGB888)
        self.imgLabel.setPixmap(QPixmap.fromImage(qImg))
        self.imgLabel.rectangles = self.images_labels[im_name]

        self.setFixedSize(self.layout.sizeHint())  # adjust the window size to the image

    def save_data(self):
        # Saving in the desired format
        to_save_dict = {im_name: [] for im_name in self.images_labels}
        for im_name in self.images_labels:
            for rect in self.images_labels[im_name]:
                to_save_dict[im_name].append([rect.topLeft().x(), rect.topLeft().y(), rect.width(), rect.height()])
        with open(self.pickle_file, 'wb') as handle:
            pickle.dump(to_save_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print(f"Successfully saved in {self.pickle_file}")

    def load_data(self):
        # Loading the images data set
        files = []
        [files.extend(glob.glob(self.im_dir + '*.' + e)) for e in self.ext]
        if not files:
            [files.extend(glob.glob(self.im_dir + '//*.' + e)) for e in self.ext]
        self.images = files

        # Initializing the labels dict.
        im_names = [basename(Path(file)).split('.')[0] for file in files]
        self.images_labels = {im_name: [] for im_name in im_names}

        # loading saved rectangle data if exist
        if os.path.isfile(self.pickle_file):
            with open(self.pickle_file, 'rb') as handle:
                loaded_dict = pickle.load(handle)
            for im_name in loaded_dict:
                for rect in loaded_dict[im_name]:
                    self.images_labels[im_name].append(QRect(rect[0], rect[1], rect[2], rect[3]))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    try:  # optional cmd run
        im_dir_path = sys.argv[1]
    except IndexError:
        im_dir_path = IM_DIR_PATH

    app_window = AnnotationGUI(im_dir_path)
    sys.exit(app.exec_())
