#获取cpu信息，并写入CSV文件

# 获取cpu信息：adb shell dumpsys cpuinfo | findstr com.wudaokou.flyingfish
import csv
import os
import time


#控制类
class Controller(object):

    #初始化
    def __init__(self, count):
        #计数器
        self.counter = count
        #存储要写入文件内数据的列表
        self.allData = [("timestamp", "cpustatus")]

        #self.cpuValue = 0

    #单次测试过程
    def testProcess(self):
        #执行命令获取结果
        result = os.popen("adb shell dumpsys cpuinfo | findstr com.wudaokou.flyingfish")
        monkey = os.popen("adb shell monkey -p com.wudaokou.flyingfish 100")
        for line in result.readlines():
            #print(line)
            #self.cpuValue = line.split("%")[0]
            cpuValue = line.split("%")[0]
            #print(cpuValue)
            currentTime = self.getCurrentTime()
            self.allData.append((currentTime, cpuValue))



    #多次测试过程
    def run(self):
        while self.counter > 0:
            self.testProcess()
            self.counter = self.counter - 1
            #print(self.counter)
            time.sleep(1)

    #获取当前时间戳
    def getCurrentTime(self):
        currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return currentTime

    #数据的存储
    def saveDataToCSV(self):
        cpuInfo = open('C:\\Users\\wb-ssc204275\\Desktop\\cpuInfo.csv', 'w')
        writer = csv.writer(cpuInfo)
        writer.writerows(self.allData)
        cpuInfo.close()

if  __name__ == '__main__':
    controller = Controller(5)
    controller.run()
    controller.saveDataToCSV()



