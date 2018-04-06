import Global
from Global import Points

# global area


def load_settings(dir_path):
    # global area
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
            # print("area=", (Points.w*Points.h))
            # area = Points.w*Points.h
        file.close()
    except:
        print('unable to read settings')


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

    if present != Points.prev:
        Points.prev = present   # change the previous state
        '''Global.engine.say(index[present])
        Global.engine.setProperty('rate', 120)
        Global.engine.runAndWait()'''


def write_blinks(time, total):
    file = open(Global.path+'_blink.txt','a')
    file.write(str(time)+" "+str(total))

