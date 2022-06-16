# Untitled - By: Lazurit - 周三 6月 15 2022

import sensor, image, time, pyb

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

img = sensor.snapshot()
print(img.width(),img.height(),img.format(),img.size())#获取图像信息

clock = time.clock()
pyb.delay(2000)

while(True):
    clock.tick()
    img = sensor.snapshot()
    clock.tick()
    img_last = img
    img = sensor.snapshot()
    img.difference(img_last)#从这张图片减去另一个图片。比如，对于每个通道的每个像素点，取相减绝对值操作。这个函数，经常用来做移动检测。
