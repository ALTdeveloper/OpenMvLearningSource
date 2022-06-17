import sensor, image, time, pyb, math

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 1000)

img = sensor.snapshot()
print(img.width(),img.height(),img.format(),img.size())#获取图像信息

clock = time.clock()
ROI=(120,80,80,80)
red = (17, 39, 17, 45, -5, 54)#LAB颜色空间下的阈值

pyb.delay(1000)

while(True):
    clock.tick()
    img = sensor.snapshot()
    img.lens_corr(1.7)
    #img.draw_rectangle(ROI)
    targets = img.find_rects(threshold = 10000)#找矩形
    for target in targets:
        img.draw_rectangle(target.rect())
        ROI_color=(target.rect())#得到矩形
        blobs = img.find_blobs([red],roi=ROI_color,pixels_threshold=100, merge=True)#找色块
        for blob in blobs:
            img.draw_rectangle(blob.rect(), color = (0,255,0))
            img.draw_cross(blob.cx(),blob.cy())
            print("pos",blob.cx(),blob.cy())#返回色块坐标
