'''
Python code for entering price of scanned items.
Written 1 jul 2022
by Ruthvik Kotapati
'''

import cv2                                      # importing libraries
import time
import serial
import pandas as pd
import pyzbar.pyzbar as pyzbar

print('---- Starting Process ----')

ard = serial.Serial('COM5', 9600, timeout=1)    # Starting serial comms
time.sleep(2)
print('Process Started')

cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)

data = []
tx = 'r'
print("Process Running...")
while True:
    ret, frame = cap.read()

    detected = pyzbar.decode(frame)                         # decodes the codes in frame
    temp = []
    for info in detected:
        Encoded_Data = info.data.decode('utf-8')
        Encoding_Type = info.type
        temp.append(Encoded_Data)
        temp.append(Encoding_Type)

        ard.write(tx.encode())                          # sends a byte 'r' to arduino via serial comm
        time.sleep(8)                                   # arduino receives 'r' and sends back the entered price from numpad
        rx = ard.readline().decode('utf-8').rstrip()
        temp.append(rx)                                 # recieved price is added to list containing item code and type
        print("Price Entered:", rx)
        data.append(temp)                               # the data of this item is then added to a list containg such data of other items

        (x, y, w, h) = info.rect                        # to draw a bounding box for the decoded barcode
        if w < 20 or h < 20:
            cv2.putText(frame, str(temp), (200, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

        else:
            cv2.rectangle(frame, (x-2, y-2), (x+w+2, y+h+2), (0, 255, 0), 2)
            cv2.putText(frame, str(temp), (200, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

    cv2.imshow('QR_Detector', frame)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

'''
Large numbers stored in csv loose their integrity as csv identifies them as number and
denotes them in exponential form loosing the last terms.
So to make them store as text each item's code id prefixed with a ' character.
a same item can be read multiple time because of the fps of camera, so only unique items
entered in the data are transferred to the list edata.
This edata is then made into a dataframe which makes it easy to convert into a .csv file.
'''

for each in data:
    each[0] = "'"+each[0]

edata = []
for x in data:
    if x not in edata:
        edata.append(x)
print("############################################################")
print("Data Entered:")
for each in edata:
    print(each)
print("############################################################")
df = pd.DataFrame(edata, columns=['ID', 'Type', 'Price'])
df.to_csv('Price_index.csv', index=None)
print("Saved data as a csv!")
print("Terminating Process...")
time.sleep(1)
print("---- Process Terminated ----")
