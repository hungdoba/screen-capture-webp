import os
import sys
import tinify
import tkinter as tk
from PIL import ImageGrab
from dotenv import load_dotenv
from PyQt5 import QtWidgets, QtCore, QtGui


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        print('Capture the screen...')
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), 3))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        load_dotenv(
            dotenv_path=r"C:\Users\hungba\Documents\Programming\Python\HyipAnalysis\.env")
        tinify.key = os.environ.get("TINIFY_KEY")
        self.close()
        url = r"C:\Users\hungba\OneDrive\Desktop\capture.png"

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        img.save(url)

        source = tinify.from_file(url)
        converted = source.convert(type=["image/webp"])
        converted.to_file(url.replace("png", "webp"))
        if os.path.exists(url):
            os.remove(url)


if __name__ == '__main__':
    url = r"C:\Users\hungba\OneDrive\Desktop\capture.png"
    if os.path.exists(url):
        os.remove(url)
    if os.path.exists(url.replace("png", "webp")):
        os.remove(url.replace("png", "webp"))
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())
