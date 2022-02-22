import csv
import numpy as np
from scipy import interpolate
from matplotlib import pyplot as plt

class Spectrometer():
    def __init__(self, url):
        wv = []
        t = []
        with open(url, newline='') as csvfile:
            specreader = csv.reader(csvfile, delimiter='\t')
            for i, row in enumerate(specreader):
                if i < 12:
                    continue
                wv.append(float(row[0]))
                t.append(float(row[7]))
            self.wavelength = np.array(wv)
            self.transmission = np.array(t)
            # print(self.wavelength)
            # print(wv)
    
    def resample(self, min_wavelength= 400, max_wavelength = 700, step = 1):
        if (min_wavelength<min(self.wavelength)) or (max_wavelength>max(self.wavelength)):
            print("重采样失败，原因为重采样区间超出所采集波段")
            return
        x = np.arange(min_wavelength, max_wavelength, step)
        tcp = interpolate.splrep(self.wavelength, self.transmission)
        y = interpolate.splev(x, tcp)
        self.wavelength = x
        self.transmission = y

    def plot(self):
        plt.plot(self.wavelength, self.transmission)

    





if __name__ == "__main__":
    folder = r'D'
    file = r'test.txt'
    filepath = folder + '\\' + file
    data = Spectrometer(filepath)

    plt.figure()
    data.plot()
    # plt.show()
    data.resample()
    # plt.figure()
    data.plot()
    plt.show()

