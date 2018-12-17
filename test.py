#! coding=utf-8
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("TKAgg")
import matplotlib.pyplot as plt

data = pd.read_table("18125813.txt", sep="\t", header=None, names=['y1', 'y2', 'y3', 'y4'])

T = 1/333

x = np.arange(0.0, len(data) * T, T)

y1 = data['y1']
y2 = data['y2']
y3 = data['y3']
y4 = data['y4']

fig = plt.figure("曲线图")


plt.plot(x, y1, color="green", label="1")

# 图2

plt.plot(x, y2, color="red", label="2")

# 图3
plt.plot(x, y3, color="black", label="3")

# 图4
plt.plot(x, y4, color="blue", label='4')


x_global_min = 0
x_global_max = 10
def call_back(event):
    global x_global_min
    global y_global_max
    axtemp=event.inaxes
    x_min, x_max = axtemp.get_xlim()
    fanwei = (x_max - x_min) / 10
    if event.button == 'up':
        x_global_min = x_min + fanwei
        x_global_max = x_max - fanwei
        axtemp.set(xlim=(x_global_min, x_global_max))
    elif event.button == 'down':
        x_global_min = x_min - fanwei
        x_global_max = x_max + fanwei
        axtemp.set(xlim=(x_global_min, x_global_max))
    fig.canvas.draw_idle()


def key_press(event):
    global x_global_min
    global x_global_max
    axtemp = event.inaxes
    x_min, x_max = axtemp.get_xlim()
    fanwei = (x_max - x_min) / 10
    if event.key == "left":
        x_global_min = x_min - fanwei
        x_global_max = x_max - fanwei
        plt.xlim(x_global_min, x_global_max)
    if event.key == "right":
        x_global_min = x_min + fanwei
        x_global_max = x_max + fanwei
        plt.xlim(x_global_min, x_global_max)
    if event.key == "up":
        x_global_min = x_min + fanwei
        x_global_max = x_max - fanwei
        axtemp.set(xlim=(x_global_min, x_global_max))
    if event.key == "down":
        x_global_min = x_min - fanwei
        x_global_max = x_max + fanwei
        axtemp.set(xlim=(x_global_min, x_global_max))

    fig.canvas.draw_idle()

press = False
x_press = None
def on_press(event):
    global press
    global x_press
    press = True
    x_press = event.xdata;

def on_motion(event):
    global press
    global x_press
    global x_global_min
    global x_global_max
    if press:
        dx = event.xdata - x_press
        x_global_min = x_global_min - dx
        x_global_max = x_global_max - dx
        plt.xlim(x_global_min, x_global_max)
        fig.canvas.draw_idle()
    x_press = event.xdata


def on_release(event):
    global press
    global x_press
    press = False

fig.canvas.mpl_connect('scroll_event', call_back)
fig.canvas.mpl_connect("button_press_event", on_press)
fig.canvas.mpl_connect("key_press_event", key_press)

fig.canvas.mpl_connect("button_release_event", on_release)
fig.canvas.mpl_connect("motion_notify_event", on_motion)


def print_data(col_data):
    t_start = 0
    t_end = 0
    is_on_wave = False
    num = 0
    tmp_most = 0 # 波动最高点或者最低的决定值
    tmp_num = 0 # 波动的越界的个数
    for i in range(len(col_data)):

        if col_data[i] > 2050 or col_data[i] < 1990:

            tmp_num += 1

            if col_data[i] > 2050:
                tmp_most = max(tmp_most, col_data[i] - 2050)
            else:
                tmp_most = max(tmp_most, 1990 - col_data[i])
            # if i > 0:
            #     print(str(tmp_most) + " " + str(col_data[i]))

            if not is_on_wave:
                is_on_wave = True
                t_start = i + 1
                t_end = i + 1
            else:
                t_end = i + 1
        else:
            if is_on_wave and i - t_end > 30: # 30 点后认定结束了当前的波动
                if tmp_most > 100 and tmp_num > 30 and t_end - t_start > 30:
                    print("波动：" + str(t_start) + "-" + str(t_end) + " 点数: " + str(t_end - t_start) +
                          " 坐标：(" + str(t_start * T) + "," + str(t_end * T) + ")")
                    num += 1

                elif tmp_most > 400 and tmp_num > 20:
                    print("波动：" + str(t_start) + "-" + str(t_end) + " 点数: " + str(t_end - t_start) +
                          " 坐标：(" + str(t_start * T) + "," + str(t_end * T) + ")")
                    num += 1
                is_on_wave = False

                tmp_most = 0
                tmp_num = 0

    print("波动数 = " + str(num))


print("第一条数据：")
print_data(y1)
print("第二条数据：")
print_data(y2)
print("第三条数据：")
print_data(y3)
print("第四条数据：")
print_data(y4)


plt.legend()
plt.show()
