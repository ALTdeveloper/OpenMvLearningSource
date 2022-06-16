# Untitled - By: Lazurit - 周三 6月 15 2022

import sensor, image, time, pyb, math

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 1000)

img = sensor.snapshot()
print(img.width(),img.height(),img.format(),img.size())#获取图像信息

red = (17, 39, 17, 45, -5, 54)#LAB颜色空间下的阈值(minL, maxL, minA, maxA, minB, maxB)，可以用工具取得
blue = (17, 27, -42, 9, -38, -8)
#yellow = (0)


clock = time.clock()
pyb.delay(2000)

while(True):
    clock.tick()
    img = sensor.snapshot()
    img.lens_corr(1.7)
    #完整函数image.find_blobs(thresholds, roi=Auto, x_stride=2, y_stride=1, invert=False, area_threshold=10, pixels_threshold=10, merge=False, margin=0, threshold_cb=None, merge_cb=None)

    red_blobs = img.find_blobs([red], pixels_threshold=700, merge=True)#从img里面捕获所有在阈值内的区域，存储到red_blobs
    #color_blobs = img.find_blobs([red,blue,yellow])这样可以获得多个不同阈值的区域
    for red_blob in red_blobs:#遍历每一个区域
        img.draw_rectangle(red_blob.rect(), color = (0,255,0))#为区域打上边框
        print(red_blob.rotation() / math.pi * 180)#返回检测目标的旋转角度
        #此处可以对遍历到的区域进行操作
