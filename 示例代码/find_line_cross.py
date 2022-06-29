# Find Lines
#通过这个程序，您可以识别空心的有明确边线的任何图形，只需要更改处理边线交角的方法即可
#design by La'3urit 22.06.29

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565) # grayscale is faster
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

min_degree = 0
max_degree = 179
line_anglex = []

def find_cross(line_f,line_b):
    import math
    t1 = line_f.theta()/180*math.pi#转弧度制
    t2 = line_b.theta()/180*math.pi
    c1 = line_f.rho()
    c2 = line_b.rho()
    a1 = math.cos(t1)
    b1 = math.sin(t1)
    a2 = math.cos(t2)
    b2 = math.sin(t2)

    if ((a1*b2-a2*b1) != 0 and (b1*a2-b2*a1) != 0):#两直线平行的时候没有交点
        x_cros = (c1*b2-c2*b1)/(a1*b2-a2*b1)#解二元一次直线相交方程
        y_cros = (c1*a2-c2*a1)/(b1*a2-b2*a1)
        if (x_cros > 0 and x_cros < 320 and y_cros > 0 and y_cros < 240):#保证交点在画面内
            #print(x_cros,y_cros)
            line_anglex.append(abs(line_f.theta()-line_b.theta()))#检测每条线的角度差（夹角）来判断多边形内角情况，返回值在（0，180）之间
            #print(line_anglex)#这可以让您看到程序是如何找到夹角的
            img.draw_cross(int(x_cros),int(y_cros))

while(True):
    clock.tick()
    img = sensor.snapshot()
    img.lens_corr(1.7)#矫正镜头畸变

    lines = img.find_lines(threshold = 820, theta_margin = 20, rho_margin = 25)#调整这个阈值可以减少误判的线
    lines_len = len(lines)#回报找到的线数量
    line_point = 1#提前声明变量
    print(lines_len)
    for l_f in lines:
        img.draw_line(l_f.line(), color = (255, 0, 0))#画线

    for l_f in lines:#遍历每根线，判断是否和其他线有交点
        #if (min_degree <= l_f.theta()) and (l_f.theta() <= max_degree):
        if (line_point < lines_len):
            for l_b in lines[line_point:]:#截取列表片段来遍历
                #if (min_degree <= l_b.theta()) and (l_b.theta() <= max_degree):
                find_cross(l_f,l_b)
            line_point = line_point + 1#将遍历开始的位置后移一位，因为l_f后移了一位
    line_point = 1#重置这个指针位置

    if (len(line_anglex) == 3):#三角形有三个角
        if (abs(180-(line_anglex[0]+line_anglex[1]+line_anglex[2]))<5):#验证三角形内角和等于180度，小于值是允许的误差
            print("三角形")
    elif (len(line_anglex) == 4):#四边形有四个角
        num_less90 = 0
        for angle in line_anglex:
            if (abs(angle - 90)>7):#统计不足九十度的夹角，大于值是分割阈值
                num_less90 = num_less90 + 1
        if (num_less90 >= 2):#两个不足九十度的角就认为不是矩形
            print("梯形或平行四边形")
        else:#可以加入验证变的长度以分类正方形长方形
            print("矩形")

    line_anglex = []#清空角度列表
