# Untitled - By: Lazurit - 周一 7月 18 2022

import sensor, image, time
from pyb import Servo

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
#sensor.set_framesize(sensor.QVGA)
sensor.set_framesize(sensor.B128X128)   # 将图像大小设置为64x64…… (64x32)……
sensor.skip_frames(time = 2000)

# 从主帧缓冲区的RAM中取出以分配第二帧缓冲区。
# 帧缓冲区中的RAM比MicroPython堆中的RAM多得多。
# 但是，在执行此操作后，您的某些算法的RAM会少得多......
# 所以，请注意现在摆脱RAM问题要容易得多。
extra_fb = sensor.alloc_extra_fb(sensor.width(), sensor.height(), sensor.RGB565)
extra_fb.replace(sensor.snapshot())

clock = time.clock()

#可移动范围上下0-2500左右0-2500
xmax = 2500
ymax = 2500
s1 = Servo(1) # P7上下
s2 = Servo(2) # P8旋转
s1.pulse_width(int(ymax/2))
s2.pulse_width(int(xmax/2))
time.sleep_ms(10)

#PID参数声明
err_last = 0
err_lastest = 0
pid_p = 4#
pid_i = 12#15
pid_d = 0#3

#滤波参数声明
x_last = 0
y_last = 0
alpha = 0.8

def servo_diffmove(x,y):
    pw1 = round(s1.pulse_width() + y)
    if (pw1 > 0 and pw1 < ymax):
        s1.pulse_width(pw1)
    pw2 = round(s2.pulse_width() + x)
    if (pw2 > 0 and pw2 < xmax):
        s2.pulse_width(pw2)

#增量式pid
def pid(err):
    global err_last, err_lastest
    pidc = pid_p * err - pid_i * err_last + pid_d *err_lastest
    err_lastest = err_last
    err_last = err
    return pidc

#一阶滞后滤波
def filter(x,y):
    global x_last, y_last
    filt = [alpha*x+(1-alpha)*x_last, alpha*y+(1-alpha)*y_last]
    #filt = [x,y]#关闭了滤波
    x_last = x
    y_last = y
    return filt

while(True):
    clock.tick()
    img = sensor.snapshot()
    displacement = extra_fb.find_displacement(img)
    extra_fb.replace(img)

    if(displacement.response() > 0.1): # 低于0.1左右（YMMV），结果只是噪音。
        sub_pixel_x = displacement.x_translation()
        sub_pixel_y = displacement.y_translation()
        flit_result = filter(sub_pixel_x, sub_pixel_y)

        servo_diffmove((xmax/2),pid(flit_result[1]))

        print(flit_result[1], s1.pulse_width())
        #servo_diffmove(sub_pixel_x,sub_pixel_y)
