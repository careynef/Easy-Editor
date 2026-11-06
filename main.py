from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QRadioButton,
    QPushButton, QButtonGroup, QGroupBox,
    QVBoxLayout, QHBoxLayout, QFileDialog, QFormLayout, QListWidget, QLineEdit, QTextEdit, QInputDialog
)
from PIL import Image, ImageFilter

from PIL.ImageFilter import (
    BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE, EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN, GaussianBlur, UnsharpMask
)
import os
from PyQt5.QtGui import QPixmap
app = QApplication([])



editor_win = QWidget()
editor_win.setWindowTitle('Easy Editor')
editor_win.resize(900, 900)

lw_files = QListWidget()
button_folder = QPushButton('Folder')
button_left = QPushButton('Left')
button_right = QPushButton('Right')
button_mirror = QPushButton('Mirror')
button_sharp = QPushButton('Sharpness')
button_bw = QPushButton('B&W')
button_blur = QPushButton('Blur')

lb_image = QLabel('Image')

row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(button_folder)
col1.addWidget(lw_files)
col2.addWidget(lb_image, 95)

row_tools = QHBoxLayout()
row_tools.addWidget(button_left)
row_tools.addWidget(button_right)
row_tools.addWidget(button_mirror)
row_tools.addWidget(button_sharp)
row_tools.addWidget(button_bw)
row_tools.addWidget(button_blur)
col2.addLayout(row_tools)

row.addLayout(col1, 20)
row.addLayout(col2, 80)
editor_win.setLayout(row)
editor_win.show()

workdir = ''
def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def chooseworkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenameslist():
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    chooseworkdir()
    filenames = filter(os.listdir(workdir), extensions)
    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)

button_folder.clicked.connect(showFilenameslist)

class img_pro():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"
    def loadimage(self, dir, filename):
        '''When loading, remember the path and file name'''
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)
        
    def do_mir(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharp(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def saveImage(self):
        '"saves a copy of the file in a sub_folder"'
        path = os.path.join(self.dir, self.save_dir)
        if not os.path.exists(path):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def showImage(self, path):
        lb_image.hide()
        pixmapImage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapImage = pixmapImage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapImage)
        lb_image.show()

def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.loadimage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)

workimage = img_pro()
lw_files.currentRowChanged.connect(showChosenImage)

button_bw.clicked.connect(workimage.do_bw)
button_blur.clicked.connect(workimage.do_blur)
button_left.clicked.connect(workimage.do_left)
button_right.clicked.connect(workimage.do_right)
button_mirror.clicked.connect(workimage.do_mir)
button_sharp.clicked.connect(workimage.do_sharp)


    


app.exec()