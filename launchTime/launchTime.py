#获取包名、activity名方法
# 1、adb shell dumpsys package [packagename]
# 2、adb logcat | grep START
# 3、adb shell monkey -p [packagename] -vvv
# 4、apk文件 使用aapt：aapt xmltree *.apk AndroidManifest.xml
# 5、已安装在手机或虚拟机上：adb logcat ActivityManager:I *:s
# 6、adb shell dumpsys window w | findstr \/ | findstr name=
# 启动APP：
#     adb shell am start -W -n packagename/MainActivity_Launcher
# 退到后台：
#     adb shell input keyevent 3

#获取启动时间，并写入CSV文件
import csv
import os
import time

#定义一个APP类
class App(object):

    #定义构造函数
    def __init__(self):
        self.startTime = 0
        self.content = ''

    #定义启动APP
    def launchApp(self):
        #运行命令
        cmd = 'adb shell am start -W -n com.wudaokou.flyingfish/.FFSplashActivity'
        #系统执行命令，将之后的内容保存在content中
        self.content = os.popen(cmd)

    #定义结束APP
    def stopApp(self):
        #冷启动
        cmd = 'adb shell am force-stop com.wudaokou.flyingfish'
        #keyevent 3 相当于back键  热启动
        #cmd = 'adb shell input keyevent 3'
        os.popen(cmd)

    #定义时间戳,获取启动时间
    def getLaunchTime(self):
        for line in self.content.readlines():
            if 'ThisTime' in line:
                self.startTime = line.split(':')[1]
                break
        return self.startTime




#定义一个Controller控制类
class Controller(object):

    #定义构造函数，一初始化就有循环次数
    def __init__(self, count):
        self.app = App()
        self.counter = count
        #收集数据存储在列表中的元组内  执行时间点和耗费时间
        self.allData = [('timeStamp', 'elapsedtime')]


    #定义单词测试过程
    def testProcess(self):
        self.app.launchApp()
        time.sleep(5)
        elpasedtime = self.app.getLaunchTime()
        self.app.stopApp()
        time.sleep(3)
        currentTime = self.getCurrentTime()
        self.allData.append((currentTime, elpasedtime))

    #定义多次测试过程
    def run(self):
        while self.counter > 0:
            self.testProcess()
            self.counter = self.counter - 1
            print(self.counter)

    #定义获取时间戳的方法
    def getCurrentTime(self):
        currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        return currentTime

    #d定义保存数据到CSV文件
    def saveDataToCSV(self):
        csvFile = open('C:\\Users\\wb-ssc204275\\Desktop\\startTime.csv', 'w')
        writer = csv.writer(csvFile)
        writer.writerows(self.allData)
        csvFile.close()

if __name__ == '__main__':
    controller = Controller(5)
    controller.run()
    controller.saveDataToCSV()
