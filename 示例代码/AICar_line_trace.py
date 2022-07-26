import sensor, image, time, pyb, math
from pyb import UART

uart = UART(3, 115200)

sensor.reset()
sensor.set_vflip(True)#垂直镜像模式
sensor.set_hmirror(True)#水平镜像模式
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)#160x120
sensor.skip_frames(time = 1000)

THRESHOLD = (20, 84, -34, 20, -18, 40) #LAB阈值
ROI = (40,20,80,80)

img = sensor.snapshot()
print(img.width(),img.height(),img.format(),img.size())#获取图像信息

clock = time.clock()

pyb.delay(1000)

while(True):
    clock.tick()
    img = sensor.snapshot().binary([THRESHOLD],invert=True)#获得图像并进行二值化
    img.dilate(2) #膨胀（去除噪点）
    line = img.get_regression([(100,100)],roi=ROI, robust = True)#这一步是对图像进行最小二乘法拟合，当像素点过多时将会消耗大量的性能
    if (line):
        img.draw_line(line.line(), color = (0,255,0))
        line_err = int((line[0]+line[2])/2-80)
        line_err = int(line_err/2 + 50)
        #line_err = str(line_err)
        #uart.write(bytearray([0x2C,0x56,int(line_err*10),line.theta(),]))
        #uart.write(',&'+line_err+' '+str(line.theta())+'[')
        #print(line_err)
        uart.write(chr(line_err))
        print(chr(line_err))
        #uart.write(',&'+line_err+' '+str(line.theta())+'[')

        '''if (line_err > 0):
            line_err = str(line_err)
            if (line_err.len() == 2):
                line_err = '0' + line_err
            elif (line_err.len() == 1):
                line_err = '00' + line_err

            print(',&'+line_err+' '+str(line.theta()))#返回一个直线元组(x1, y1, x2, y2)
            uart.write(',&'+line_err+' '+str(line.theta())+'[')
        else:
            line_err = str(line_err)
            print(',&'+line_err+' '+str(line.theta()))
            uart.write(',&'+line_err+' '+str(line.theta())+'[')'''
