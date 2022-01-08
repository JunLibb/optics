# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 15:54:26 2021

@author: APPO
"""
# TODO: 固定xy比例的encircle energy
# TODO: 连接API
import argparse
import numpy as np
import pandas as pd
import win32com.client as client
import clr
import System
import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser(description='Etendue of receiver')
    parser.add_argument("--r", "-r", "-Receiver",type=str, default="Receiver_DMD",
                        help="Receiver Name")

    args = parser.parse_args()
    receiver = args.r
    print("Receiver:",receiver)
    test = Receiver(src=receiver)

def main_clipboard():
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument("--method", type=str, default='encircled energy')
    parser.add_argument("--t", "--threshold", type=float, default=0.99,
                        help="percentage of encircled energy, default 0.99")

    args = parser.parse_args()
    energy_threshold = args.t

    print(energy_threshold)
    data = Meshdata()
    x, y, x0, y0 = data.encircled_energy(threshold=energy_threshold)
    print("FW x,y:", x, y)
    print("x0,y0:", x0, y0)


class Meshdata():
    def __init__(self, src="clipboard"):
        # 数据读取
        df = pd.read_clipboard(sep='\\t+')
        data = np.array(df, dtype='double')
        # 清理nan行
        data = np.delete(data, np.where(np.isnan(data))[0], axis=0)
        self.x = np.array(df.columns[1:], dtype='double')
        self.y = data[:, 0]
        self.data = data[:, 1:]

    def encircled_energy(self, threshold=0.99):
        def en_energy(x, energy):
            if (np.sum(energy[1:-1]) <= energy_threshold):
                return x
            else:
                energy = energy[1:-1]
                x = x[1:-1]
                return en_energy(x, energy)

        energy_total = np.sum(self.data[:])
        energy_x = np.sum(self.data, 0)
        energy_y = np.sum(self.data, 1)
        energy_threshold = np.sqrt(threshold)*energy_total

        x = en_energy(self.x, energy_x)
        y = en_energy(self.y, energy_y)
        x = abs(x[0])
        y = abs(y[0])
        x0 = np.dot(energy_x, self.x)/energy_total
        y0 = np.dot(energy_y, self.y)/energy_total
        return x, y, x0, y0


class Receiver():
    meshtype = {"illuminance": ".ILLUMINANCE_MESH[Illuminance_Mesh]",
                "cie": ".SPATIAL_CIE_MESH[CIE_Mesh]",
                "intensity": ".INTENSITY_MESH[Intensity_Mesh]"}

    def __init__(self, src="Receiver[1]"):
        self.receiver = src
        self.lt = client.Dispatch("LightTools.LTAPI4")
        x,y,a,b,eten = self.get_etendue()
        self.etendue_info = [x,y,a,b,eten]

    def get_mesh_data(self, meshtype="illuminance"):
        meshkey = self.receiver + self.meshtype[meshtype]

        XD = int(self.lt.DbGet(meshkey, "X_Dimension")[0])
        YD = int(self.lt.DbGet(meshkey, "Y_Dimension")[0])
        k = np.ones((XD, YD))
        # The CellFilter may not work for all options in COM mode
        [stat, myd, f] = self.lt.GetMeshData(meshkey, list(k), "CellValue")
        g = np.asarray(myd)
        g = np.rot90(g, axes=(0, 1))

        MinX = self.lt.DbGet(meshkey, "Min_X_Bound")[0]
        MaxX = self.lt.DbGet(meshkey, "Max_X_Bound")[0]
        MinY = self.lt.DbGet(meshkey, "Min_Y_Bound")[0]
        MaxY = self.lt.DbGet(meshkey, "Max_Y_Bound")[0]
        x = np.linspace(MinX, MaxX, XD)
        y = np.linspace(MaxY, MinY, YD)
        X, Y = np.meshgrid(x, y)
        return X, Y, g

    def encircled_energy(self, X, Y, data, threshold=0.99):
        def en_energy(x, energy):
            if (np.sum(energy[1:-1]) <= energy_threshold):
                return x
            else:
                energy = energy[1:-1]
                x = x[1:-1]
                return en_energy(x, energy)

        energy_total = np.sum(data[:])
        energy_x = np.sum(data, 0)
        energy_y = np.sum(data, 1)
        energy_threshold = np.sqrt(threshold)*energy_total

        x = en_energy(X, energy_x)
        y = en_energy(Y, energy_y)
        x = abs(x[0])
        y = abs(y[0])
        x0 = np.dot(energy_x, X)/energy_total
        y0 = np.dot(energy_y, Y)/energy_total
        return x, y, x0, y0

    def get_etendue(self, threshold=0.99):
        X1, Y1, D1 = self.get_mesh_data(meshtype="illuminance")
        X2, Y2, D2 = self.get_mesh_data(meshtype="intensity")
        dx1, dy1, x01, y01 = self.encircled_energy(X1[0,:], Y1[:,0], D1, threshold)
        dx2, dy2, x02, y02 = self.encircled_energy(X2[0,:], Y2[:,0], D2, threshold)
        Etendue = dx1 * dy1 * 4 * np.sin(np.radians(dx2)) * np.sin(np.radians(dy2))
        print("面x: ", dx1, " 面y:", dy1)
        print("角x: ", dx2, " 角y:", dy2)
        print("center point:",x01,y01,x02,y02)
        print("Etendue:", Etendue)
        return dx1,dy1,dx2,dy2,Etendue



if __name__ == "__main__":
    main()
