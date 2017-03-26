#监测流量步骤
#1、获取进程ID：adb shell ps | grep packagename
#2、获取进程ID流量：adb shell cat /proc/pid/net/dev
#    只要关注receive（接收）+ transmit（发送）= 总流量  关注网卡eth0, eth1


#定义控制类
import csv
import os
import string
import time


class Controller(object):

    #定义构造函数，包含运行次数
    def __init__(self, count):
        #定义计数器
        self.counter = count
        #定义收集数据的数组
        self.allData = [("timestamp", "traffic")]


    #单次测试过程
    def testProcess(self):
        #执行获取进程的命令
        result = os.popen("adb shell ps | findstr com.wudaokou.flyingfish")
        #获取进程ID
        pid = result.readlines()[0].split(" ")[1]
        #print(result.readlines()[0])
        print(pid)

        #获取进程ID使用的流量
        traffic = os.popen("adb shell cat /proc/" + pid + "/net/dev")
        for line in traffic.readlines():
            if "wlan0" in line:
                #将所有空行换成‘#’
                line = '#'.join(line.split())
                #按#号拆分，获取接收到的和发送的流量
                receive = line.split("#")[1]
                transmit = line.split("#")[9]
            # elif "wlan1" in line:
            #     # 将所有空行换成‘#’
            #     line = '#'.join(line.split())
            #     # 按#号拆分，获取接收到的和发送的流量
            #     receive1 = line.split("#")[1]
            #     transmit1 = line.split("#")[9]

        #计算所有的流量之和
        allTraffic = int(receive) + int(transmit) #+ int(receive1) + int(transmit1)
        #按KB进行计算流量值
        allTraffic = allTraffic/1024
        #获取当前时间
        currentTime = self.getCurrentTime()
        #将获取到的数据保存在数据列表中
        self.allData.append((currentTime, allTraffic))


    #多次运行测试
    def run(self):
        while self.counter > 0:
            self.testProcess()
            self.counter = self.counter -1
            time.sleep(5)
            print(self.counter)

    #获取当前时间戳
    def getCurrentTime(self):
        currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return currentTime

    #数据的存储
    def saveDataToCSV(self):
        traffic = open("C:\\Users\\wb-ssc204275\\Desktop\\traffic5.csv", 'w')
        writer = csv.writer(traffic)
        writer.writerows(self.allData)
        traffic.close()

if __name__ == '__main__':
    controller = Controller(12)
    controller.run()
    controller.saveDataToCSV()