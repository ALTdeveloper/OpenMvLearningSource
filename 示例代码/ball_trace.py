# Untitled - By: Lazurit - 周三 7月 20 2022

import sensor, image, time
from pyb import Servo

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.set_vflip(True)#垂直镜像模式
#sensor.set_hmirror(True)#水平镜像模式
sensor.skip_frames(time = 2000)

clock = time.clock()

ball_color = (0, 55, -30, 8, -22, -2)

#参考中间坐标
x_mid = 80
y_mid = 60

#可移动范围上下0-2500左右0-2500
xmax = 2500
ymax = 2500
s1 = Servo(1) # P7旋转x
s2 = Servo(2) # P8上下y
s1.pulse_width(int(xmax/2))
s2.pulse_width(int(ymax/2))

class Mv_PID:
    #自定义的通用位置式pid类
    def __init__(self,p,i,d,imax):
        self.p = p
        self.i = i
        self.d = d
        self.imax = imax#积分限幅
        self.err_last = 0
        self.err_lastest = 0
        self.erri = 0#积分err

#PID参数声明
x_pid = Mv_PID(2.5,0,0.17,10)#2.5,0,0.17,10
y_pid = Mv_PID(2.5,0,0.17,10)#2.5,0,0.17,10

def color_judge(l,a,b,color):
    if (l > color[0] and l < color[1]):
        if (a > color[2] and a < color[3]):
            if (b > color[4] and b < color[5]):
                return True
    return False

#位置式pid
def pid(err,obj):
    pidout = obj.p * err + obj.i * obj.erri + obj.d * err - 2*obj.err_last + obj.err_lastest
    if (obj.erri+err < obj.imax and obj.erri+err > -obj.imax):
        obj.erri = obj.erri+err
    obj.err_lastest = obj.err_last
    obj.err_last = err
    return pidout

def servo_diffmove(x,y):
    pw1 = round(s1.pulse_width() + x)
    if (pw1 > 0 and pw1 < xmax):
        s1.pulse_width(pw1)
    pw2 = round(s2.pulse_width() + y)
    if (pw2 > 0 and pw2 < ymax):
        s2.pulse_width(pw2)

while(True):
    clock.tick()
    img = sensor.snapshot()
    balls = []
    targets = img.find_circles(threshold=2500,r_min=5)#x_margin=True,y_margin=True,r_margin=True)#找圆
    for target in targets:
        statistics = img.get_statistics(roi=(target.x(),target.y(),target.r(),target.r()))#从注意力区域返回该区域的统计结果，是一个元组
        color_l=statistics.l_mode()#分别得到lab颜色值
        color_a=statistics.a_mode()
        color_b=statistics.b_mode()
        if(color_judge(color_l,color_a,color_b,ball_color)):
            balls.append(target)

    if (len(balls) != 0):
        rb = []#存储球的半径大小
        for b in balls:
            rb.append(b.r())
        t_ball = balls[rb.index(max(rb))]
        xerr = t_ball.x() - x_mid
        yerr = t_ball.y() - y_mid
        img.draw_cross(t_ball.x(),t_ball.y(),color=(255,0,0))
        img.draw_line(t_ball.x(),t_ball.y(),x_mid,y_mid,color=(0,0,255))
        print(t_ball.x(),t_ball.y())
        servo_diffmove(pid(xerr,x_pid),pid(yerr,y_pid))

