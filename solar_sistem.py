import matplotlib.pyplot as plt
import numpy as np
import rijecnici as r
import math as m
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

class Planets:
    def __init__(self, x):
        self.v = (x["brzina"])
        self.m = (x["masa"])
        self.x = (x["polozaj"])
        self.s = (x["velicina"])
        self.label = (x["ime"])
        self.c = (x["boja"])
        self.x_y_z = [self.x]
        self.akceleracija = np.array([0,0,0])
        self.size = (x["size"])

class Comet:
    def __init__(self,m1,v1,cord1):
        self.m = m1
        self.v = v1
        self.x = cord1
        self.akceleracija = np.array([0,0,0])
        self.x_y_z = []  

class Universe:
    def __init__(self, x,y,z=0,j=0,k=0,n=0,m=0):
        tijela1 = [x,y,z,j,k,n,m]
        tijela2 = ["Sunce","Merkur","Venera","Zemlja","Mars","Jupiter","Saturn"]
        self.kometi = []
        self.planeti = []
        for i in range (7):
            x = tijela1[i]
            if x==tijela2[0]:
                p1 = Planets(r.sunce)
                self.planeti.append(p1)
            elif x==tijela2[1]:
                p1 = Planets(r.merkur)
                self.planeti.append(p1)
            elif x==tijela2[2]:
                p1 = Planets(r.venera)
                self.planeti.append(p1)
            elif x==tijela2[3]:
                p1 = Planets(r.zemlja)
                self.planeti.append(p1)
            elif x==tijela2[4]:
                p1 = Planets(r.mars)
                self.planeti.append(p1)
            elif x==tijela2[5]:
                p1 = Planets(r.jupiter)
                self.planeti.append(p1)
            elif x==tijela2[6]:
                p1 = Planets(r.saturn)
                self.planeti.append(p1)

    def reset(self):
        del self.planeti

    def komet(self,m,v,x):
        x = Comet(m,v,x)
        self.kometi.append(x)

    def calculate(self):
        G = 6.67408E-11
        t = 0
        T = 4 * 365 * 24 * 3600
        dt = 36000
        while t<T:
            for x in self.planeti:
                for y in self.planeti:
                    if x!=y:
                        udaljenost = np.linalg.norm(abs(np.subtract(x.x,y.x)))**3
                        akc1 = -G * (y.m * (np.subtract(x.x,y.x))/ udaljenost)
                        for i in range(3):
                            if m.isnan(akc1[i])==True:
                                akc1[i ]= 0
                        x.akceleracija = np.add(akc1,x.akceleracija)
            for x in self.planeti:
                x.v1 = np.add(x.v,x.akceleracija*dt)
                x.x = np.add(x.x , x.v1 * dt)
                x.x_y_z.append(x.x)

            for x in self.kometi:
                for y in self.planeti:
                    udaljenost = np.linalg.norm(abs(np.subtract(x.x,y.x)))**3
                    akc1 = -G * (y.m * (np.subtract(x.x,y.x))/ udaljenost)
                    for i in range(3):
                        if m.isnan(akc1[i])==True:
                            akc1[i ]= 0
                    x.akceleracija = np.add(akc1,x.akceleracija)
            for x in self.kometi:
                x.v1 = np.add(x.v,x.akceleracija*dt)
                x.x = np.add(x.x , x.v1 * dt)
                x.x_y_z.append(x.x)
            t = t + dt

    def anima(self):
        self.calculate()
        fig = plt.figure(figsize = (5,5))
        axes = fig.add_subplot(111)
        axes.set_facecolor("black")
        x_liste = []
        y_liste = []
        x_liste_kometi = []
        y_liste_kometi = []
        legenda = False
        for x in self.planeti:
            x_list = []
            y_list = []
            for i in range(len(x.x_y_z)):
                polozaj = x.x_y_z[i]
                x_list.append(polozaj[0])
                y_list.append(polozaj[1])
            axes.plot(x_list,y_list,c = x.c)
            for i in range(3):
                del x_list[::2]
                del y_list[::2]
            x_liste.append(x_list)
            y_liste.append(y_list)

        for x in self.kometi:
            x_list = []
            y_list = []
            for i in range(len(x.x_y_z)):
                polozaj = x.x_y_z[i]
                x_list.append(polozaj[0])
                y_list.append(polozaj[1])
            axes.plot(x_list,y_list,c = "w")
            for i in range(3):
                del x_list[::2]
                del y_list[::2]
            x_liste_kometi.append(x_list)
            y_liste_kometi.append(y_list)

        axes.scatter(0,0,s = 300, c = "y" , label = "Sunce")

        point, = axes.plot([x_liste[0][0]],[y_liste[0][0]], 'go',c = "y")
        def ani(coords):
            point.set_data([coords[0]],[coords[1]])
            if self.planeti[0].label != "Sunce":
                point.set_label(self.planeti[0].label)
            point.set_color(self.planeti[0].c)
            point.set_marker("o")
            point.set_markersize(self.planeti[0].size)
            legend = plt.legend() 
            if legenda == False:
                return point,legend
            else:
                return point
        def frames():
            for acc_11_pos, acc_12_pos in zip(x_liste[0], y_liste[0]):
                yield acc_11_pos, acc_12_pos
        if self.planeti[0].label != "Sunce":
            animation = FuncAnimation(fig, ani, frames=frames, interval=3)
            legenda = True


        try:
            point1, = axes.plot([x_liste[1][0]],[y_liste[1][0]], 'go',linewidth = 0.01)
            def ani1(coords):
                point1.set_data([coords[0]],[coords[1]])
                if self.planeti[1].label != "Sunce":
                    point1.set_label(self.planeti[1].label)
                point1.set_color(self.planeti[1].c)
                point1.set_marker("o")
                point1.set_markersize(self.planeti[1].size)
                legend = plt.legend() 
                if legenda == False:
                    return point1,legend
                else:
                    return point1
            def frames1():
                for acc_11_pos, acc_12_pos in zip(x_liste[1], y_liste[1]):
                    yield acc_11_pos, acc_12_pos
            if self.planeti[1].label != "Sunce":
                animation1 = FuncAnimation(fig, ani1, frames=frames1, interval=3)
                legenda = True
        except:
            pass

        try:
            point2, = axes.plot([x_liste[2][0]],[y_liste[2][0]], 'go')
            def ani2(coords):
                point2.set_data([coords[0]],[coords[1]])
                if self.planeti[2].label != "Sunce":
                    point2.set_label(self.planeti[2].label)
                point2.set_color(self.planeti[2].c)
                point2.set_marker("o")
                point2.set_markersize(self.planeti[2].size)
                return point2
            def frames2():
                for acc_11_pos, acc_12_pos in zip(x_liste[2], y_liste[2]):
                    yield acc_11_pos, acc_12_pos
            if self.planeti[2].label != "Sunce":
                animation2 = FuncAnimation(fig, ani2, frames=frames2, interval=3)
        except:
            pass

        try:
            point3, = axes.plot([x_liste[3][0]],[y_liste[3][0]], 'go')
            def ani3(coords):
                point3.set_data([coords[0]],[coords[1]])
                if self.planeti[3].label != "Sunce":
                    point3.set_label(self.planeti[3].label)
                point3.set_color(self.planeti[3].c)
                point3.set_marker("o")
                point3.set_markersize(self.planeti[3].size)  
                return point3
            def frames3():
                for acc_11_pos, acc_12_pos in zip(x_liste[3], y_liste[3]):
                    yield acc_11_pos, acc_12_pos
            if self.planeti[3].label != "Sunce":
                animation3 = FuncAnimation(fig, ani3, frames=frames3, interval=3)
        except:
            pass

        try:
            point4, = axes.plot([x_liste[4][0]],[y_liste[4][0]], 'go')
            def ani4(coords):
                point4.set_data([coords[0]],[coords[1]])
                if self.planeti[4].label != "Sunce":
                    point4.set_label(self.planeti[4].label)
                point4.set_color(self.planeti[4].c)
                point4.set_marker("o")
                point4.set_markersize(self.planeti[4].size)
                return point4
            def frames4():
                for acc_11_pos, acc_12_pos in zip(x_liste[4], y_liste[4]):
                    yield acc_11_pos, acc_12_pos
            if self.planeti[4].label != "Sunce":
                animation4 = FuncAnimation(fig, ani4, frames=frames4, interval=3)

        except:
            pass

        try:
            point6, = axes.plot([x_liste[5][0]],[y_liste[5][0]], 'go')
            def ani6(coords):
                point6.set_data([coords[0]],[coords[1]])
                if self.planeti[5].label != "Sunce":
                    point6.set_label(self.planeti[5].label)
                point6.set_color(self.planeti[5].c)
                point6.set_marker("o")
                point6.set_markersize(self.planeti[5].size)
                return point6
            def frames6():
                for acc_11_pos, acc_12_pos in zip(x_liste[5], y_liste[5]):
                    yield acc_11_pos, acc_12_pos
            if self.planeti[5].label != "Sunce":
                animation6 = FuncAnimation(fig, ani6, frames=frames6, interval=3)

        except:
            pass

        try:
            point7, = axes.plot([x_liste[6][0]],[y_liste[6][0]], 'go')
            def ani7(coords):
                point7.set_data([coords[0]],[coords[1]])
                if self.planeti[6].label != "Sunce":
                    point7.set_label(self.planeti[6].label)
                point7.set_color(self.planeti[6].c)
                point7.set_marker("o")
                point7.set_markersize(self.planeti[6].size)
                return point7
            def frames7():
                for acc_11_pos, acc_12_pos in zip(x_liste[6], y_liste[6]):
                    yield acc_11_pos, acc_12_pos
            if self.planeti[6].label != "Sunce":
                animation7 = FuncAnimation(fig, ani7, frames=frames7, interval=3)

        except:
            pass

        try:
            point5, = axes.plot([x_liste_kometi[0][0]],[y_liste_kometi[0][0]], 'go',linewidth = 1)
            def ani5(coords):
                point5.set_data([coords[0]],[coords[1]])
                point5.set_label("Komet")
                point5.set_marker("o")
                point5.set_color("w")
                point5.set_markersize(4)
                return point5
            def frames5():
                for acc_11_pos, acc_12_pos in zip(x_liste_kometi[0], y_liste_kometi[0]):
                    yield acc_11_pos, acc_12_pos
            animation5 = FuncAnimation(fig, ani5, frames=frames5, interval=3)
        except:
            pass

        maximum = plt.get_current_fig_manager()
        maximum.full_screen_toggle()       #za izlazak iz full screena stisnuti "ctrl + f" ,a za izlazak iz programa "ctrl + w"

        plt.show()