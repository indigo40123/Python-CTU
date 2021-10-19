# This won't work in jupyter notebook
import time
import json
import numpy
import threading
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from urllib.request import urlopen

### Empty array for location and plot
ISS_X, ISS_Y = [], []
hl, = plt.plot([],[], color='red', marker='o', markersize=3,markeredgecolor='black', label = []) #empty plot
### zero for first point
new_data= [0,0]

### axis limits
plt.ylim(-200, 200)
plt.xlim(-200, 200)

### Update the figure form the data
def update_line(hl, new_data):
    hl.set_xdata(numpy.append(hl.get_xdata(), new_data[0]))
    hl.set_ydata(numpy.append(hl.get_ydata(), new_data[1]))
    red_patch = mpatches.Patch(color='red', label= r'X : %.3f' %new_data[0] +'\n'+ r'Y : %.3f' %new_data[1])
    plt.legend(handles=[red_patch])
    plt.draw()  # draw new data
    plt.pause(0.1)  # update graph every 0.5 second

### Read the data every 1 second form the website
def Read():
    while True:
        start = time.time()
        time.sleep(1)
        response = urlopen("http://api.open-notify.org/iss-now.json")
        obj = json.loads(response.read())
        ISS_X.append(float(obj.get('iss_position').get('latitude')))
        ISS_Y.append(float(obj.get('iss_position').get('longitude')))
        end = time.time()
        print('Read: {} s'.format(round(end-start),2), time.time())
        if stop:
            break

### Write and save the data every 5 second I read
def Write(ISS_X,ISS_Y):
    while True:
        start = time.time()
        time.sleep(5)
        df2 = pd.DataFrame({"latitude" : ISS_X,
                            "longitude": ISS_Y})
        df2.to_csv("HW9.csv",index=False)
        end = time.time()
        print('Write: {} s'.format(round(end - start), 2), time.time())
        if stop:
            break
    #return 'Create a new file HW9 and save data to the file'


### Main function starts here
### Threading reading and writing function
stop = False
t1 = threading.Thread(target=Read)
t1.start()
t2 = threading.Thread(target=Write, args=[ISS_X, ISS_Y])
t2.start()

### Run the main function for the furture 50 seconds
ticks_end = time.time()+50
while True:
### Update the figure every 3 seconds
    if time.time()< ticks_end:
        start = time.time()
        time.sleep(3)
        new_data[0] = ISS_X[-1]   # x data
        new_data[1] = ISS_Y[-1]
        update_line(hl, new_data)
        end = time.time()
        print('Plot: {} s'.format(round(end - start), 2),time.time())
    else: break
stop = True