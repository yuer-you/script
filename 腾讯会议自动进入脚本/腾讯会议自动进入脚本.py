import os
import pandas as pd
import numpy as np
import pyautogui
import cv2
import time
from datetime import datetime

def imgAutoCick(tempFile, whatDo, debug=False):
    '''
    函数作用：自动点击匹配按钮
    '''
    pyautogui.screenshot('big.png')
    gray = cv2.imread("big.png",0)
    img_template = cv2.imread(tempFile,0)
    w, h = img_template.shape[::-1]
    res = cv2.matchTemplate(gray,img_template,cv2.TM_SQDIFF)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top = min_loc[0]
    left = min_loc[1]
    x = [top, left, w, h]
    top_left = min_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    pyautogui.moveTo(top+h/2, left+w/2)

    whatDo(x)

    if debug:
        img = cv2.imread("big.png",1)
        cv2.rectangle(img,top_left, bottom_right, (0,0,255), 2)
        img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
        cv2.imshow("processed",img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    os.remove("big.png")

def imgAutoCheck(tempFile, debug=False):
    '''
    本函数功能：自动检测图片是否匹配
    '''
    pyautogui.screenshot('check.png')
    gray = cv2.imread("check.png",0)
    img_template = cv2.imread(tempFile,0)
    w, h = img_template.shape[::-1]
    res = cv2.matchTemplate(gray,img_template,cv2.TM_SQDIFF)

    template_size= img_template.shape[:2]
    threshold = 0.99
    loc = np.where(res >= threshold)
    point = ()
    for pt in zip(*loc[::-1]):
        cv2.rectangle(gray, pt, (pt[0] + template_size[1], pt[1] + + template_size[0]), (7, 249, 151), 2)
        point = pt

    os.remove("check.png")

    if point==():
        return 0

def check():
    '''
    本函数功能：检测老师是否结束会议
    '''
    a = imgAutoCheck("check1.png", False)
    if a == 0:  # 会议结束
        time.sleep(1)
    else:    # 会议未结束
        imgAutoCick("goout.png", pyautogui.click, False)
        time.sleep(1)
        imgAutoCick("goout2.png", pyautogui.click, False)
        time.sleep(7)

# openApp函数有要自行修改的地方
def openApp():
    '''
    本函数功能：根据绝对路径打开腾讯会议
    '''
    os.startfile("D:\\txmeet\\WeMeet\\wemeetapp.exe")   # 此处输入自己电脑上腾讯会议exe文件的绝对路径（！！！非快捷方式！！！）
    time.sleep(7)

def signIn(meeting_id, password):
    '''
    本函数功能：写入腾讯会议号，写入密码（如有），进入会议之中
    '''
    imgAutoCick("joinbtn.png", pyautogui.click, False)
    time.sleep(1)
    imgAutoCick("meeting_id.png", pyautogui.click, False)
    pyautogui.write(meeting_id)
    time.sleep(2)
    imgAutoCick("final.png", pyautogui.click, False)
    time.sleep(1)

    pw = imgAutoCheck("check_pw.png", False)    # 确认是否有入会密码
    if pw != 0:
        pyautogui.write(password)
        time.sleep(2)
        imgAutoCick("final_pw.png", pyautogui.click, False)
        time.sleep(1)


# 下面的代码有需要修改的地方
# 如若想DIY仅需修改下面的代码（读懂函数作用后）

while True: # 上午第一节课
    now = datetime.now().strftime("%m-%d-%H:%M")
    if now == "04-27-07:55":    # 此处填写想要进入会议的时间（建议提前5min）
        meeting_id = '94378900148'    # 此处填入会议号
        password = '1324'     # 此处填写入会密码，请在''内填写，格式：'1324'；如无密码请忽略
        time.sleep(5)
        openApp()
        signIn(meeting_id, password)
        print('signed in')
        break

while True: # 上午第二节课
    now = datetime.now().strftime("%m-%d-%H:%M")
    if now == "04-27-10:05":    # 此处填写想要进入会议的时间（建议提前5min）
        meeting_id = '53230150751'    # 此处填入会议号
        password = '1324'     # 此处填写入会密码，请在''内填写，格式：'1324'；如无密码请忽略
        time.sleep(5)
        check()
        signIn(meeting_id, password)
        print('signed in')
        break