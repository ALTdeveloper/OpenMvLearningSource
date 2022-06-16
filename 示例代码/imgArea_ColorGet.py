# Untitled - By: Lazurit - 周三 6月 15 2022

import sensor, image, time, pyb

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)

#img = sensor.snapshot()
#print(img.width(),img.height(),img.format(),img.size())#获取图像信息

clock = time.clock()
#pyb.delay(2000)

ROI = (0,0,10,20)#注意力区域

while(True):
    clock.tick()
    img = sensor.snapshot()
    statistics = img.get_statistics(roi=ROI)#从注意力区域返回该区域的统计结果，是一个元组
    color_l=statistics.l_mode()#分别得到lab颜色值
    color_a=statistics.a_mode()
    color_b=statistics.b_mode()
    print(color_l,color_a,color_b)
    img.draw_rectangle(ROI)#框住注意力区域
