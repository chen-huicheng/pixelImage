# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 12:18:04 2019

@author: icheng
"""

"""
PIL numpy 需要安装的包
"""
from tkinter import filedialog
from PIL import Image
import numpy as np
import tkinter
import random
import os


"""
path :资源图片路径   savepath:输出图片保存路径
"""
def setSize(path,x,y): #重新设置图片大小  最终输出为保存图片为x*y像素
    try:
        image = Image.open(path)
    except:
        print('open Error')
        return 'null'
    width, height = image.size
    if(width > height):
        left = (width - height) // 2
        box=(left,0,left + height,height)
        image = image.crop(box)
    elif(width < height):
        top = (height - width) // 2
        box=(0,top,width,top + width)
        image = image.crop(box)
    image = image.resize((x,y),Image.ANTIALIAS)  #此处可更改输出图片大小
    image = image.convert('RGB')
    return image

def reSize(path):
    try:
        image = Image.open(path)
    except:
        print('open Error')
        return
    width, height = image.size
    x = 100
    y = 100
    if(width > height):
        y  = int((x*1.0 / width) * height) 
    elif(width < height):
        x  = int((y*1.0 / height) * width)
    image = image.resize((x,y),Image.ANTIALIAS)  #此处可更改输出图片大小
    image = image.convert('RGB')
    return image
   
def getColor(image): #获取图片的大致色彩 保存为RGB
    data = list(image.getdata())
    b = np.array([0,0,0])
    for i in data:
        a = np.array(i)
        b = np.add(a,b)
    b = list(b)
    b = [i // 10000 for i in b]
    b = tuple(b)
    c = np.array([0,0,0])
    count = 0
    for i in data:
        a = np.array(i)
        temp = list(np.subtract(a,b))
        temp = abs(temp[0]) + abs(temp[1]) + abs(temp[2])
        if(temp > 200):
            continue
        count += 1
        c = np.add(a,c)
    c = list(c)
    c = [i // count for i in c]
    c = tuple(c)
    return c           #此处可选择  b  OR  c

def imageToColor(Imagelist):  #将批量图片转化为颜色 
    colorlist = []
    for image in Imagelist:
        color = getColor(image)
        colorlist.append(color)
    return colorlist

def findSimilerImage(colorlist,pixel,similer):
    index = []
    for i in range(len(colorlist)):
        temp = abs(colorlist[i][0]-pixel[0]) + abs(colorlist[i][1]-pixel[1]) + abs(colorlist[i][2]-pixel[2])
        if(temp < similer):
            index.append(i)
    if(len(index) == 0):
        index = findSimilerImage(colorlist,pixel,2*similer)
    return index
    
def dealImage(Imagelist,colorlist,inImage,Imagename,edge):  #处理图片  输出 像素填充图
    x = inImage.size[0]
    y = inImage.size[1]
    outImage = Image.new('RGB',(x*edge,y*edge))
    for i in range(x):
        for j in range(y):
            pixel = inImage.getpixel((i,j))
            indexlist = findSimilerImage(colorlist,pixel,100)
            index = random.randint(0,len(indexlist)-1)
            sourceImage = Imagelist[indexlist[index]]
            outImage.paste(sourceImage,(i*edge,j*edge))
#            print(i,j)
    i = Imagename.rfind('/')
    savepath = Imagename[:i+1] + 'output0.jpg'
    outImage.save(savepath)
    im = Image.open(Imagename)
    im = im.resize((x*edge,y*edge),Image.ANTIALIAS)
    out = Image.blend(im,outImage,0.5)
    savepath = Imagename[:i+1] + 'output1.jpg'
    out.save(savepath)
    
    
def oneStep(path,x):
    Image = []
    filenames = os.listdir(path)
    savepath = path+'/source'
    if(not os.path.exists(savepath)):
        os.mkdir(savepath)
    for filename in filenames:
        if((filename.split('.')[-1]).lower() in ['jpg','png']):
            img = setSize(path + '/' + filename,x,x)
            if(type(img) is str):
                continue
            Image.append(img)
    return Image

def opendir():
    path = filedialog.askdirectory(title='选择文件夹')
    label1['text'] = path

def openImage():
    Imagename = filedialog.askopenfilename(title='选择图片',filetypes=[('图片', '*')])
    label2['text'] = Imagename

def run():
    path = label1['text']
    Imagename = label2['text']
    print(1)
    Imagelist = oneStep(path,100)
    print(2)
    colorlist = imageToColor(Imagelist)
    print(3)
    inImage = reSize(Imagename)
    print(4)
    dealImage(Imagelist,colorlist,inImage,Imagename,100)


win = tkinter.Tk()
win.title("Icheng")
win.geometry("460x300+300+200")
win.resizable(0,0)
btn1 = tkinter.Button(win, text='选择文件夹',font =("楷体",15,'bold'),width=20,height=4, command=opendir)
btn2 = tkinter.Button(win, text='选择图片',font = ('楷体',15,'bold'),width=20,height=4, command=openImage)
btn3 = tkinter.Button(win, text='执行',font =("楷体",20,'bold'),width=18,height=2, command=run)
label1 = tkinter.Label(win,text='文件夹: 未选择',font = ('楷体',13),width=20,height=4)
label2 = tkinter.Label(win,text='图片: 未选择',font = ('楷体',13),width=20,height=4)
label = tkinter.Label(win,text='状态栏',font = ('楷体',13),width=40,height=1,anchor="w")
btn1.grid(row=0,column=0)
btn2.grid(row=0,column=1)
label1.grid(row=1,column=0)
label2.grid(row=1,column=1)
label.place(x=0,y=260)
btn3.place(x=100,y=170)
win.mainloop()
    
