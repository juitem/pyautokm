#!/usr/bin/python3

import pyautogui as pag
import sys
import time
import datetime
from PIL import Image, ImageChops
import numpy as np 
import copy

# Get Master info
def Info():
    sx,sy=pag.size()
    print('Size', sx, sy)
    x,y = pag.position()
    print('Pos', x, y)

def PosTest2():
    Info()
    _sx, _sy=pag.size()
    _sx = _sx* 0.97
    xd=_sx/23
    yd=_sy/12.5
    pauset=0.1

    shotx1=xd 
    shoty1=yd 
    shotx2=_sx/2-xd
    shoty2=_sy-yd 

    loop=1
    while loop>0:
        pag.moveTo(_sx/4,_sy/2,duration=.1)
        time.sleep(pauset)
        pag.moveTo(xd,yd,duration=.1)
        time.sleep(pauset)
        pag.moveTo(_sx/2-xd,yd,duration=.1)
        time.sleep(pauset)
        pag.moveTo(_sx/2 -xd,_sy-yd,duration=.1)
        time.sleep(pauset)
        pag.moveTo(xd, _sy-yd,duration=.1)
        time.sleep(pauset)
        loop=loop-1
    return int(shotx1),int(shoty1),int(shotx2),int(shoty2)


def focus(x1,y1,x2,y2):
    pag.moveTo(x2,(y1+y2)/2, duration=0.01)
    pag.moveRel(50,0, duration=0.1)

def diffImage(img1_path,img2_path):
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)
    diff = ImageChops.difference(img1, img2)
    if diff.getbbox():
        retv=30000
    else:
        retv=0
    return retv


def isSameArea(img1_path,img2_path):
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)

    width, height = img1.size

    box1 = (30,30,457,688)

    img1_crop = img1.crop(box1)
    img2_crop = img2.crop(box1)

    diff = np.array(img1_crop) - np.array(img2_crop)

    if np.count_nonzero(diff) == 0:
        retv=True
    else:
        retv=False
    return retv


# Adjust Size
x1,y1,x2,y2=PosTest2()
# Pages
Pages=1000
now=datetime.datetime.now()
prefix=now.strftime("../../Shots/temp/%Y%m%d_%H%M")
prevfilename="../../Shots/AI/Loading.png"

Numbering=1
ContSame= 0

print("calc XY: ", x1,y1,x2,y2)
print("cap XY: ",  x1,y1,x2-100,y2-100)


start_time = time.time()
dups=0
rtcnt=0
for i in range(1,Pages+1):
    filename=prefix +'_'+str(Numbering)+".png"
    focus(x1,y1,x2,y2)
    pag.screenshot(filename, region=(x1, y1, x2-100, y2-100))
    pag.click(button="left")
    print("Shot:",filename)

    difference=diffImage(prevfilename,filename)
    if difference == 0:
        print("Error: Duplicate Image Detected.")
        dups = dups +1
        ContSame = ContSame +1
        if ContSame==5:
            end_time = time.time()
            print("===================")
            print("Retries: ", rtcnt)
            print("Duplicates(+5): ", dups)
            print("Elapsed: ", int(end_time - start_time), "Seconds")
            exit(1)
    else:
        ContSame = 0
        prevfilename=copy.deepcopy(filename)
        Numbering=Numbering+1


    waitfirst=0.09
    time.sleep(waitfirst)
    if isSameArea("../../Shots/AI/Loading.png", filename):
        rtcnt=rtcnt+1
        # Wait for the Animation
        MaxWaitTime=10 # Max 10. Sec
        waitStep=0.2
        cnt=0;
        print("!!!! Loading..",waitfirst+waitStep*cnt)
        while ( waitStep*cnt < MaxWaitTime ) :
            rtcnt=rtcnt+1
            pag.screenshot(filename, region=(x1, y1, x2-100, y2-100))
            if isSameArea("../../Shots/AI/Loading.png", filename):
                print("Loading..",cnt,':', waitfirst+waitStep*cnt)
                time.sleep(waitStep)
            else:
                print('===> Success!')
                break
            cnt=cnt+1;

    #   Automatic Wait logic Applied sleep() not needed
    #   time.sleep(2)

