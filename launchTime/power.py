#监测电量用到的adb
# 1、展示电量：adb shell dumpsys battery
# 2、切换到非充电状态：adb shell dumpsys battery set status 1(1是非充电状态，2是充电状态)

#控制类controller
import os
import time
import csv


class Controller(object):
    def __init__(self, count):
        self.counter = count
        self.allData = [("timestamp", "level")]

    #单次测试过程
    def testProcess(self):
        #执行获取电量的命令
        result = os.popen("adb shell dumpsys battery")
        #获取电量的level
        for line in result.readlines():
            if "level" in line:
                level = line.split(":")[1]

        #获取当前时间
        currentTime = self.getCurrentTime()
        #将数据追加到allData中
        self.allData.append((currentTime, level))



    #多次测试过程，运行测试
    def run(self):
        #测试次数
        while self.counter > 0:
            #多次测试，必须将电池置为非充电状态
            os.popen("adb shell dumpsys battery set status 1")
            #执行单次测试
            self.testProcess()
            self.counter = self.counter - 1
            print(self.counter)
            time.sleep(10)

    #获取当前时间戳
    def getCurrentTime(self):
        currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return currentTime


    #保存数据
    def saveDataToCSV(self):
        power = open("C:\\Users\\wb-ssc204275\\Desktop\\power.csv", 'w')
        writer = csv.writer(power)
        writer.writerows(self.allData)
        power.close()



if __name__ == '__main__':
    controller = Controller(180)
    controller.run()
    controller.saveDataToCSV()
