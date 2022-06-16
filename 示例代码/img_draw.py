# Untitled - By: Lazurit - 周三 6月 15 2022

import sensor, image, time, pyb

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

img = sensor.snapshot()
print(img.width(),img.height(),img.format(),img.size())#获取图像信息

clock = time.clock()
#pyb.delay(200)

while(True):
    clock.tick()
    img = sensor.snapshot()
    img.draw_line((0,0,320,240),color = (0,0,255))#在(0,0)和(320,240)之间画一条直线，颜色为rgb(0,0,255)
    img.draw_rectangle((0,0,160,120), color = (0,255,0))#以(0,0)为左上角画一个方框，长160宽120，颜色为rgb(0,255,0)
    img.draw_circle(160, 120, 80, color = (255,0,0))#以(160,120)为圆心画一个圆，半径为80，颜色为rgb(255,0,0)
    img.draw_string(160, 120, "draw_test", color = (255,255,255))#以(160.120)为左上角，放置8x10像素的字符
