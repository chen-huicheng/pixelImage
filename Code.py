# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 12:18:04 2019

@author: icheng
"""

"""
PIL numpy 需要安装的包
"""

from PIL import Image
import numpy as np
import random
import time

"""
path :资源图片路径   savepath:输出图片保存路径
"""
def setSize(path,savepath,x,y): #重新设置图片大小  最终输出为保存图片为x*y像素
    image = Image.open(path)
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
    image.save(savepath)


"""

"""    
def getColor(path): #获取图片的大致色彩 保存为RGB
    image = Image.open(path)
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
#    im = Image.new('RGB',(100,100))
#    im1 = Image.new('RGB',(100,100))
#    for i in range(100):
#        for j in range(100):
#            im.putpixel((i,j),b)
#            im1.putpixel((i,j),c)
#    img = Image.new('RGB',(300,100))
#    img.paste(im,(0,0))
#    img.paste(image,(100,0))
#    img.paste(im1,(200,0))
#    img.save('pic.jpg')
#    img.show()

def write(data):
    path = 'colorlist.txt'
    f = open(path,'w')
    for i in data:
        f.write(str(i)+'\n')
    f.close()
    
def read():
    path = 'colorlist.txt'
    data = []
    f = open(path,'r')
    for line in f:
        temp = line[1:-2].split(',')
        temp = [int(i.strip()) for i in temp]
        data.append(temp)
    f.close()
    return data

def imageToColor(num):  #将批量图片转化为颜色 
    data = []
    for i in range(num):
        path = 'source\image_' + str(i) + '.jpg'
        color = getColor(path)
        data.append(color)
    write(data)

def findSimilerImage(data,pixel,similer):
    index = []
    for i in range(len(data)):
        temp = abs(data[i][0]-pixel[0]) + abs(data[i][1]-pixel[1]) + abs(data[i][2]-pixel[2])
        if(temp < similer):
            index.append(i)
    if(len(index) == 0):
        index = findSimilerImage(data,pixel,2*similer)
    return index
    
def dealImage(path,edge):  #处理图片  输出 像素填充图
    data = read()
    inImage = Image.open(path)
    x = inImage.size[0]
    y = inImage.size[1]
    outImage = Image.new('RGB',(x*edge,y*edge))
    for i in range(x):
        for j in range(y):
            pixel = inImage.getpixel((i,j))
            indexlist = findSimilerImage(data,pixel,100)
            index = random.randint(0,len(indexlist)-1)
            sourcePath = 'source\image_' + str(indexlist[index]) + '.jpg'
            sourceImage = Image.open(sourcePath)
            outImage.paste(sourceImage,(i*edge,j*edge))
#            print(i,j)
    outImage.save('ouput.jpg')
    
def run1(num,x):
    for i in range(num):
        path = 'image\image(' + str(i) +').jpg'
        savepath = 'source\image_' + str(i) +'.jpg'
        setSize(path,savepath,x,x)   
        
        
def main():
    path = 'config.txt'
    f = open(path,'r')
    data = []
    for line in f:
        temp = line.split(':')[-1]
        data.append(int(temp.strip()))
    f.close()
#    print(data)
    print('one step runing....')
    run1(data[0],data[1])
    print('two step runing....')
    imageToColor(data[0])
    path = 'input.jpg'
    print('three step runing....')
    setSize(path,path,data[2],data[2])
    dealImage(path,data[1])
    print('successfully')
    
if __name__ == '__main__':
    main()
    print('Exit after 10 seconds')
    time.sleep(10)
    
