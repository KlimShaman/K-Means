from asyncio.constants import LOG_THRESHOLD_FOR_CONNLOST_WRITES
from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi
from mplwidget import MplWidget
from mplwidget2 import MplWidget2
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import numpy as np
import math
import matplotlib.pyplot as plt
import random
import matplotlib.animation as animation
from PyQt5.QtWidgets import*
import copy
import os

from matplotlib.backends.backend_qt5agg import FigureCanvas

from matplotlib.figure import Figure



def center_cluster(xlim, ylim, lengthside, n_clusters):
    centers = []
    while (len(centers) < n_clusters):
        boole = True
        xcenter = random.randint(-xlim + lengthside, xlim - lengthside)
        ycenter = random.randint(-ylim + lengthside, ylim - lengthside)
        if (len(centers) == 0):
            centers.append([xcenter, ycenter])
        else:
            rx, ry = 0, 0
            for i in centers:
                if (i[0] < xcenter):
                    rx = xcenter - i[0]
                else:
                    rx = i[0] - xcenter

                if (i[1] < ycenter):
                    ry = ycenter - i[1]
                else:
                    ry = i[1] - ycenter
                if ((rx <= (lengthside * 1.3)) or (ry <= (lengthside * 1.3))):
                    boole = False
                    break
            if (boole):
                centers.append([xcenter, ycenter])
    return centers       
                    

def pointGeneration(lengthside, n_clusters, centers, n_points):
    xpoints, ypoints, xpoints1, ypoints1, points = [], [], [], [], []
    for i in centers:
        std = round((lengthside), 2)
        xpoints = np.random.normal(i[0], std, size=(1, n_points))
        ypoints = np.random.normal(i[1], std, size=(1, n_points))
        for i in range(n_points):
            xpoints1.append(xpoints)
            ypoints1.append(ypoints)
            points.append([round(xpoints[0][i], 2), round(ypoints[0][i], 2)])
    return points, xpoints1, ypoints1

klim = 0
centers = []
centers2 = []
points, xpoints1, ypoints1 = 0, 0, 0
xlim, ylim = 0, 0
newclusters = []
newcentersxy = [[], []]
newclusters2 = []
newcentersxy2 = [[], []]
jilist = []
ji = 0
lst = -1
listik = []
newcentersxy = [[], []]
 
class MplWidget(QWidget):
    
    def __init__(self, parent = None):

        QWidget.__init__(self, parent)
        
        self.canvas = FigureCanvas(Figure())
        
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)
class MplWidget2(QWidget):
    
    def __init__(self, parent = None):

        QWidget.__init__(self, parent)
        
        self.canvas = FigureCanvas(Figure())
        
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)       

class MatplotlibWidget(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi(os.path.join(os.path.dirname(__file__), "des6new.ui") ,self)
        self.label_20 = QLabel("", self)
        self.label_20.move(360, 650)


        self.add_functions()
        self.setWindowTitle("PyQt5 & Matplotlib Example GUI")
        self.pushButton_2.clicked.connect(self.update_animation)
        self.pushButton_3.clicked.connect(self.update_graph)
        self.addToolBar(NavigationToolbar(self.MplWidget2.canvas, self))
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))
        
    def set_key(self):
        global xlim, ylim, lengthside, n_clusters, n_points, sleep1, iterat, eps, centers, points, xpoints1, ypoints1
        xlim = int(self.lineEdit_6.text())
        ylim = int(self.lineEdit_4.text())
        lengthside = int(self.lineEdit_2.text())
        sleep1 = float(self.lineEdit_3.text())
        n_points = int(self.lineEdit_5.text())
        n_clusters = int(self.lineEdit_7.text())
        iterat = int(self.lineEdit_8.text())
        eps = float(self.lineEdit_9.text())

    def add_functions(self):
        self.pushButton.clicked.connect(lambda: self.set_key())

    def update_animation(self):
        self.ani = animation.FuncAnimation(self.MplWidget, self.update_axes, self.update_graph2, interval=sleep1*1000, repeat=False)
        self.MplWidget.canvas.draw()

    def update_graph2(self):
        global xlim, ylim, lengthside, n_clusters, n_points, sleep1, iterat, eps, ji, jilist, listik, klim
        self.label_20.setText("")
        newclusters = []
        newcentersxy = [[], []]
        centers = center_cluster(xlim, ylim, lengthside, n_clusters)
        points, xpoints1, ypoints1 = pointGeneration(lengthside, n_clusters, centers, n_points)
        newcenters = random.sample(points, k = n_clusters)
        for i in range(len(newcenters)):
            newcentersxy[0].append(newcenters[i][0])
            newcentersxy[1].append(newcenters[i][1])
        jilist = []
        listik = []
        for klim in range(iterat):
            newclusters = []
            for i in range(n_clusters * 2):
                newclusters.append([])
            for i in points:
                mmin = xlim * ylim
                clusterNum = -1
                for j in range(n_clusters):
                    clusterNum += 1
                    a = math.sqrt((i[0] - newcentersxy[0][j])**2 + (i[1] - newcentersxy[1][j])**2)
                    if (a < mmin):
                        mmin = a
                        k = clusterNum
                newclusters[k].append(i[0])
                newclusters[k + n_clusters].append(i[1])
            summa = 0
            temp = ji
            for i in range(n_clusters):
                for j in range(len(newclusters[i])):
                    summa += ((newclusters[i][j] - newcentersxy[0][i])**2 + (newclusters[i + n_clusters][j] - newcentersxy[1][i])**2)
            ji = summa / (n_points * n_clusters)
            jilist.append(ji)
            if (klim != 0):
                if(abs(temp - ji) < eps):
                    listik.append(klim + 1)
                    self.label_20.setText("Завершено")
                    break
            newcentersxy = [[], []]
            for i in range(n_clusters):
                newcentersxy[0].append(np.mean(newclusters[i]))
                newcentersxy[1].append(np.mean(newclusters[i + n_clusters]))
            listik.append(klim)
            if (klim == iterat - 1):
                self.label_20.setText("Завершено")
            yield newclusters, newcentersxy

    def update_axes(self, update):
        newclusters, newcentersxy = update[0], update[1]
        self.MplWidget.canvas.axes.clear()
        for i in range(n_clusters):
            self.MplWidget.canvas.axes.scatter(newclusters[i], newclusters[i + n_clusters])
        self.MplWidget.canvas.axes.scatter(newcentersxy[0], newcentersxy[1], color = "black")

    def update_graph(self):
        self.MplWidget2.canvas.axes.clear()
        self.MplWidget2.canvas.axes.plot(listik, jilist)
        self.MplWidget2.canvas.draw()

app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()