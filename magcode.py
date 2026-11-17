from machine import Pin, SoftI2C, PWM,I2C
import time
from vl53l0x import VL53L0X

import math

# 离线拟合得到的一阶环形谐波系数
A0 = 0.01269085
A1 = 0.90327202
B1 = -0.06871016

C0 = -0.10671818
C1 = 0.07423876
D1 = 1.07606905

AS5600_ADDR = 0x36
REG_STATUS   = 0x0B
REG_RAW_ANGLE= 0x0C  # RAW ANGLE高字节，连续读2字节到0x0D

# I2C 引脚，ESP32：SCL=5 SDA=4
#i2c = SoftI2C(scl=Pin(5), sda=Pin(4), freq=100000)
i2c = I2C(0,scl=Pin(3), sda=Pin(4), freq=400000)
tof = VL53L0X(i2c, 0x29, b'\x29')# 初始化 VL53L0X 传感器
servo = PWM(Pin(2), freq=50)


tof.start()

def set_servo_pulse(us):
    """设置舵机PWM脉宽，单位us，范围500~2500"""
    us = max(500, min(2500, us))
    duty = int(us * 1023 / 20000)
    servo.duty(duty)

def read_reg(reg_addr, nbytes):
    i2c.writeto(AS5600_ADDR, bytes([reg_addr]))
    time.sleep_us(150)   # 拉长等待，减少I2C读失败
    return i2c.readfrom(AS5600_ADDR, nbytes)

def measure_to_real(x):
    # 零点实测分段，可以输出0~5°
    if x <= 10.107422:
        return 0.0
    elif 10.107422 < x <= 10.546875:
        t = (x - 10.107422) / (10.546875 - 10.107422)
        return 0.0 + t * 15.0
    # 大于10.546875使用4阶多项式拟合
    y = ((((2.1583e-08 * x - 1.47294e-05) * x + 2.91177e-03) * x + 0.860326) * x + 6.12506)
    return max(0.0, min(355.0, y))

def as5600_x2real(x):
    """
    输入：传感器测量值 x (0~360)
    输出：校正后的真实角度 0~360°
    """
    theta = math.radians(x)
    cx = math.cos(theta)
    sx = math.sin(theta)

    c_hat = A0 + A1 * cx + B1 * sx
    s_hat = C0 + C1 * cx + D1 * sx

    ang_rad = math.atan2(s_hat, c_hat)
    ang_deg = math.degrees(ang_rad)
    if ang_deg < 0:
        ang_deg += 360
    return ang_deg


# 舵机先回中
set_servo_pulse(1500)
time.sleep(1)
set_servo_pulse(1460)
deg_tar = 20

with open('data.txt','w') as f:
    f.write('')

while True:
    try:
        st_buf = read_reg(REG_STATUS, 1)
        status = st_buf[0]
        md  = (status >> 3) & 1
        ml  = (status >> 4) & 1
        mh  = (status >> 5) & 1

        ang_buf = read_reg(REG_RAW_ANGLE, 2)
        b_h = ang_buf[0]
        b_l = ang_buf[1]
        raw_val = (b_h << 8) | b_l
        raw_val = raw_val & 0x0FFF  # 保留12bit
        deg = 360-raw_val * 360.0 / 4096.0
        #print(deg)
        yp = as5600_x2real(deg)
        #t = time.ticks_ms()
        #with open('data.txt','a') as f:
        #    f.write(str(yp)+','+str(t)+'\n')
        #print(t)
        #print(yp)
        dis = min(tof.read(),1000)
        #print(deg,yp)
        print(int(yp),int(dis))

        #if (yp>deg_tar)&(yp<deg_tar+1):
            #set_servo_pulse(1500)
            #time.sleep(1)
            #break
        #time.sleep_ms(1)
    except Exception as e:
        print("I2C read err", e)
    
    


