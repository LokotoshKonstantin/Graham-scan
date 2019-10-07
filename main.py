import sys
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QWidget
from PyQt5 import QtCore, uic
import numpy as np

qtCreatorFile = "design.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


def rotate(a, b, c):
    return (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])


class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.clear)
        self.pushButton_2.clicked.connect(self.apply_the_algorithm)
        self.lastPoint = QPoint()
        blank_image2 = 255 * np.ones(shape=[600, 800, 3], dtype=np.uint8)
        scene = QGraphicsScene()
        pixmap1 = QPixmap.fromImage(
            QImage(blank_image2, blank_image2.shape[1], blank_image2.shape[0], blank_image2.strides[0],
                   QImage.Format_RGB888))
        scene.addPixmap(pixmap1)
        self.graphicsView.setScene(scene)
        self.graphicsView.setSceneRect(0, 0, 800, 600)
        self.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setMouseTracking(True)
        self.setMouseMoveEventDelegate(self.graphicsView)
        self.listPoint = []

    def setMouseMoveEventDelegate(self, setQWidget):
        def subWidgetMouseMoveEvent(eventQMouseEvent):
            QWidget.mouseMoveEvent(setQWidget, eventQMouseEvent)

        setQWidget.setMouseTracking(True)
        setQWidget.mouseMoveEvent = subWidgetMouseMoveEvent

    def clear(self):
        clear_img = 255 * np.ones(shape=[600, 800, 3], dtype=np.uint8)
        scene = QGraphicsScene()
        pixmap1 = QPixmap.fromImage(
            QImage(clear_img, clear_img.shape[1], clear_img.shape[0], clear_img.strides[0],
                   QImage.Format_RGB888))
        scene.addPixmap(pixmap1)
        self.graphicsView.setScene(scene)
        self.graphicsView.viewport().update()
        self.lastPoint = QPoint()
        self.listPoint = []

    def grahamscan(self):
        n = len(self.listPoint)  # число точек
        P = list(range(n))  # список номеров точек
        for i in range(1, n):
            if self.listPoint[P[i]][0] < self.listPoint[P[0]][0]:  # если P[i]-ая точка лежит левее P[0]-ой точки
                P[i], P[0] = P[0], P[i]  # меняем местами номера этих точек
        for i in range(2, n):  # сортировка вставкой
            j = i
            while j > 1 and (rotate(self.listPoint[P[0]], self.listPoint[P[j - 1]], self.listPoint[P[j]]) < 0):
                P[j], P[j - 1] = P[j - 1], P[j]
                j -= 1
        S = [P[0], P[1]]  # создаем стек
        for i in range(2, n):
            while rotate(self.listPoint[S[-2]], self.listPoint[S[-1]], self.listPoint[P[i]]) < 0:
                del S[-1]  # pop(S)
            S.append(P[i])  # push(S,P[i])
        return S

    def apply_the_algorithm(self):
        s = self.grahamscan()
        for x in range(len(s) - 1):
            self.graphicsView.scene().addLine(self.listPoint[s[x]][0], self.listPoint[s[x]][1],
                                              self.listPoint[s[x + 1]][0], self.listPoint[s[x + 1]][1])
        self.graphicsView.scene().addLine(self.listPoint[s[0]][0], self.listPoint[s[0]][1],
                                          self.listPoint[s[len(s) - 1]][0], self.listPoint[s[len(s) - 1]][1])
        self.graphicsView.viewport().update()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.listPoint.append([event.x(), event.y()])
            self.graphicsView.scene().addRect(event.x(), event.y(), 1, 1)
            self.graphicsView.viewport().update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.setFixedSize(800, 689)
    window.show()
    sys.exit(app.exec_())
