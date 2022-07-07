import cv2                  # importing libraries
import time
import serial
import pandas as pd
from tkinter import *
import pyzbar.pyzbar as pyzbar

print('---- Starting Process ----')

ard = serial.Serial('COM5', 9600, timeout=1)     #serial comms with arduino at 9600 baud rate
time.sleep(2)
print('Process Started')

'''
Function that reads the csv file with inventory details.
As done in price_entry script the code of items is stored as a text with a ' character as prefix.
This function removes that character and adds the entire csv into a new data frame named price_df.
'''

def edit_df():
    df1 = pd.read_csv('master_pindex.csv')
    global price_df
    price = []
    for i in range(0, len(df1)):
        temp = []
        d = (df1.loc[i][0])[1:]
        temp.append(d)
        temp.append(df1.loc[i][1])
        temp.append(df1.loc[i][2])
        temp.append(df1.loc[i][3])
        price.append(temp)
    price_df = pd.DataFrame(price, columns=[df1.columns[0], df1.columns[1], df1.columns[2], df1.columns[3]])

'''
This function is used to make the bill.
The data obtained from the camera after scanning all the products is looked up against the price_df data containing the product details.
If the code of the product matches with that in price_df then the details of this product is added to new list which also contains the
quantity of the product. If the product appears once the qty is 1 and more times them quantity is number of times it appeared in the data from camera.
This product data is then added to a list containing data of other such products and their quantity.
To ensure that the product appears only once in this bill list it is added to a list 'check' after comparing.
After the check list is prepared the function to display the bill - disp_bill is called with input as check.
'''

def make_bill():
    check = []
    uni = []
    bill = []
    for x in range(0, len(edata)):
        for i in range(0, len(price_df)):
            if edata[x][0] == price_df.loc[i][0]:
                if edata.count(edata[x]) > 1:
                    uni.append(price_df.loc[i][3])
                    uni.append(str(edata.count(edata[x])))
                    uni.append(price_df.loc[i][2])
                elif edata.count(edata[x]) == 1:
                    uni.append(price_df.loc[i][3])
                    uni.append("1")
                    uni.append(price_df.loc[i][2])
                bill.append(uni)
                uni = []

    for each in bill:
        if each not in check:
            check.append(each)

    '''for each in check:
        print(each)'''

    disp_bill(check)

'''
Function to display bill using tkinter.
Predefined format is followed and the calculations such as multiplying the quantity with unit price,
getting total items and total quantity, summing the total price and adding taxes is done.
'''

def disp_bill(my_list):
    root = Tk()
    root.title("Receipt")

    store = LabelFrame(root, height=2)
    store.grid(row=0, column=0, padx=10, pady=10, sticky=N)

    details = '''RS Mart
    -------------------------------------------------------------------------------
    Beaver Hills
    Avenue Supermarkets Ltd
    Route-54, VSKP-530002
    -------------------------------------------------------------------------------
    TAX INVOICE
    Bill No : 530107010-00581          Bill Dt: {}
    -------------------------------------------------------------------------------
    '''.format(time.ctime())

    text = Text(store, font='Helvetica 10 bold', height=9, width=30, bg='#F0F0F0')
    text.tag_configure("tag_name", justify='center')
    text.insert(INSERT, details)
    text.tag_add("tag_name", "1.0", "end")
    text.grid(row=0, column=0, sticky=W+N+E+S)

    info = Label(store, font='Helvetica 10')
    info.grid(row=1, column=0, sticky=W+N+E+S)

    head0 = Label(info, text="No", padx=20, font='Helvetica 9 bold')
    head1 = Label(info, text="Description", padx=20, font='Helvetica 9 bold')
    head2 = Label(info, text="Qty/Kg", padx=20, font='Helvetica 9 bold')
    head3 = Label(info, text="Rate", padx=20, font='Helvetica 9 bold')
    head4 = Label(info, text="Value", padx=20, font='Helvetica 9 bold')
    head0.grid(row=0, column=0)
    head1.grid(row=0, column=1)
    head2.grid(row=0, column=2)
    head3.grid(row=0, column=3)
    head4.grid(row=0, column=4)

    cost = 0
    for i in range(0, len(my_list)):
        Label(info, text="{})".format(i+1)).grid(row=i+1, column=0)
        Label(info, text=my_list[i][0]).grid(row=i+1, column=1)
        Label(info, text=my_list[i][1]).grid(row=i+1, column=2)
        Label(info, text=my_list[i][2]).grid(row=i+1, column=3)
        cost = cost + float(my_list[i][1])*float(my_list[i][2])                                 #sum of quantity * unit price for all items
        Label(info, text=str(round(float(my_list[i][1])*float(my_list[i][2]), 2))).grid(row=i+1, column=4)

    Label(info, text="---").grid(row=len(my_list)+1, column=0)
    Label(info, text="-------------------------------", padx=20).grid(row=len(my_list)+1, column=1)
    Label(info, text="-----", padx=20).grid(row=len(my_list)+1, column=2)
    Label(info, text="-------", padx=20).grid(row=len(my_list)+1, column=3)
    Label(info, text="-------", padx=20).grid(row=len(my_list)+1, column=4)

    summary = """------------------------------------------------------------------------------------------------------------------
    Items: {}                Qty : {}                Subtotal : {}                Taxes : {}
    ------------------------------------------------------------------------------------------------------------------
    """.format(len(my_list), sum([int(i) for i in [row[1] for row in my_list]]), round(cost, 2), '9%')      # items, quantity, cost of all items

    text = Text(store, font='Helvetica 10 bold', height=3, width=30, bg='#F0F0F0')
    text.tag_configure("tag_name", justify='center')
    text.insert(INSERT, summary)
    text.tag_add("tag_name", "1.0", "end")
    text.grid(row=2, column=0, sticky=W+N+E+S)

    tots = "Total: {}/-".format(round(float(cost*1.09), 2))
    text = Text(store, font='Helvetica 14 bold', height=1, width=10, bg='#F0F0F0')
    text.tag_configure("tag_name", justify='right')
    text.insert(INSERT, tots)
    text.tag_add("tag_name", "1.0", "end")
    text.grid(row=3, column=0, sticky=W+N+E+S)

    Label(store, text="Thank you for visting RS Mart", font='Helvetica 12').grid(row=4, column=0, sticky=W+N+E+S)

    def close_win():
        root.destroy()

    Button(root, text="Close Receipt", font='Poppins 12 bold', command=close_win, bg="#30D5C8").grid(row=1, column=0)

    root.mainloop()

###################################################

edit_df()                           #editing the saved csv file as written above

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

tx = 'r'
edata = []
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
        edata.append(temp)
        ard.write(tx.encode())                  #if code in frame then send 'r' to arduino and wait for 4 secs
        time.sleep(4)

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

make_bill()             # after scanning is completed make the bill and display the bill
