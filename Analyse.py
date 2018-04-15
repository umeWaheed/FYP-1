import Global
from Global import Points
import os
import time
from tinydb import TinyDB, Query

# global area


def load_settings():
    # global area
    # load settings from the database.
    # check if db exists.
    if os.path.exists(Global.path+'.json'):
        Points.x, Points.y, Points.w, Points.h, Points.range, Points.usage = Global.database.get_settings()
    else:
        print('unable to read settings')
    '''
    try:
        file = open(dir_path,'r')
        for line in file:
            print (line)
            arr = line.split()
            Points.x = int(arr[0])
            Points.y = int(arr[1])
            Points.w = int(arr[2])
            Points.h = int(arr[3])
            Points.range = int(arr[4])
            Points.usage = int(arr[5])
            # print("area=", (Points.w*Points.h))
            # area = Points.w*Points.h
        file.close()
    except:
        print('unable to read settings')
    '''

def check_movement(newX, newY, newW, newH):
    left, right, bottom, close, far = 0,0,0,0,0
    # new_area = newW*newH

    if newX < Points.x-Points.range:
        left = Points.x-newX
        #print('too left')
    if newX > Points.x+Points.w+Points.range:
        right = newX-(Points.x+Points.w)
        #print('too right')
    if newY > Points.y+Points.range:
        bottom = newY-Points.y
        #print ('sit straight')
    if newW > Points.w+Points.range:
        close = newW-Points.w
    if newW < Points.w-Points.range:
        far = Points.w-newW

    largest = 0
    print(left, " ", right, " ", bottom, " ", close, " ", far)
    index = ['too left', 'too right', 'too down', 'too close', 'too far', 'all set']
    arr = [left, right, bottom, close, far]

    if left == right == close==far==bottom: # all are zero
        print ('all set')
        present = 5
    else:
        i=0
        while i < len(arr):
            if arr[i]>arr[largest]:
                largest = i
            i += 1
        print(index[largest])
        present = largest

    write_posture(index[present])
    Global.engine.say(index[present])
    Global.engine.setProperty('rate', 120)
    Global.engine.runAndWait()

    if present != Points.prev:
        Points.prev = present   # change the previous state
        '''Global.engine.say(index[present])
        Global.engine.setProperty('rate', 120)
        Global.engine.runAndWait()'''


def write_settings(x, y, w, h, sensit, usage):
    # Global.path = 'user_info/'+name+'_'+str(label)
    Global.database.write_settings(x, y, w, h, sensit, int(usage)*60)
    '''if not os.path.exists(Global.path):
        os.mkdir(Global.path)
    dir_path = Global.path+'/settings.txt'
    # Global.path = 'user_info/'+name+'_'+str(total)
    fout = open(dir_path, 'w')   # open file in write mode, for new user
    # covert usage into seconds by *60
    line = str(x)+" "+str(y)+" "+str(w)+" "+str(h)+" "+str(sensit)+" "+str(int(usage)*60)   # input to file has to be string
    fout.write(line)
    fout.close()'''
    load_settings()     # load the newly written settings


def write_blinks(time, total):
    Global.database.add_blinks(time,total)
    # file = open(Global.path+'/blinks.txt','a')
    # file.write(str(time)+" "+str(total)+"\n")


def write_usage(time, type, duration):
    Global.database.add_usage(time, type, duration)
    # file = open(Global.path+'/usage.txt','a')
    # file.write(usage+'\n')


def write_posture(pose):
    Global.database.add_posture(time.strftime("%X"),pose)
    # file = open(Global.path+'/posture.txt', 'a')
    # file.write(pose+" "+str(time.asctime(time.localtime(time.time())))+"\n")