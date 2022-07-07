import cv2
import time
import serial
import pandas as pd
import pyzbar.pyzbar as pyzbar

print('---- Starting Process ----')

ard = serial.Serial('COM5', 9600, timeout=1)
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

    detected = pyzbar.decode(frame)
    temp = []
    for info in detected:
        Encoded_Data = info.data.decode('utf-8')
        Encoding_Type = info.type
        temp.append(Encoded_Data)
        temp.append(Encoding_Type)

        ard.write(tx.encode())
        time.sleep(8)
        rx = ard.readline().decode('utf-8').rstrip()
        temp.append(rx)
        print("Price Entered:", rx)
        data.append(temp)

        (x, y, w, h) = info.rect
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
