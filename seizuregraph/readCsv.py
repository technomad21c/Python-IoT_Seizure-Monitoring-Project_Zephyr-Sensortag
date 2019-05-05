import time

class ReadCSV:
    def open(self, fileName):
        self.infile = open(fileName, "r")
    
    def readOne(self):
        data = self.infile.readline().split(',')
        data[0] = int(data[0])
        data[1] = int(data[1])
        data[2] = int(data[2])
        return data

    def close(self):
        self.infile.close()


if __name__ == "__main__":
    csv = ReadCSV()

    while(True):
        csv.open("zephyr.csv")
        print(csv.readOne())
        csv.close()

