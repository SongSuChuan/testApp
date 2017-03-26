#aa监测内存信息
# 1、adb shell top
#     vss(虚拟内存)、rss（实际使用物理内存）
# 2、adb shell top -d(指定刷新频率) 3（刷新频率具体数值）| grep com.wudaokou.*  >(重定向) meminfo.csv

#控制类
import csv
import os
import time


class Controller(object):

    def __init__(self):
        #self.counter = count
        #保存数据到列表 时间、虚拟内存、物理内存、名
        self.allData = [("timestamp", "VSS", "RSS", "name")]
        #self.second = ''
        self.totalTime = ''
        self.vss = ''


    #运行命令获取数据
    def getMemInfo(self):
        #读取几秒钟取一次数据
        second = input("请设置频率（s）: ")
        #设置持续时间
        # self.totalTime = input("持续时间（s）: ")
        # locTime = self.getCurrentTime()
        # while (self.totalTime + locTime) >
        #每10秒钟获取一次com.wudaokou.*的内存信息
        #result = os.popen("adb shell top -d " + second + " | findstr com.wudaokou.*")
        print(os.popen("adb shell top -d " + second + " | findstr com.wudaokou.*").readlines())
        for line in result.readlines():
            self.vss = line.split(" ")[5]
            rss = line.split(" ")[6]
            namme = line.split(" ")[9]

        currentTime = self.getCurrentTime()
        self.allData.append((currentTime, self.vss, rss, namme))
    #print(self.allData)


    #获取当前时间戳
    def getCurrentTime(self):
        currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return currentTime

    #保存数据
    def saveDataToFile(self):
        meminfo = open("C:\\Users\\wb-ssc204275\\Desktop\\meminfo.csv", 'w')
        writer = csv.writer(meminfo)
        writer.writerows(self.allData)
        meminfo.close()

if __name__ == '__main__':
    controller = Controller()
    controller.getMemInfo()
    controller.saveDataToFile()



