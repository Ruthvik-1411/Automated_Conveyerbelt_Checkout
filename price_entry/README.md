# Price entry of automated checkout counter
Part 1 of realising an automated checkout counter.
>Implementation Video of price entry part : [Video](https://drive.google.com/file/d/149Q3q940hoRtR1hcXWyi73tVxEw8p2N0/view?usp=sharing)

In this part, all the products to be added into the inventory are placed on the conveyer belt. As they pass through the scanner the belt is halted and the system waits for the user to enter the price of the corresponding product it scanned. After entering the price through the numpad the belt moves forward and the process repeats until user terminates this. All the product details like its code(barcode, qr code etc), price are added to a csv file at the end.
<br><br>
The steps in this process are as follows:<br>
* The conveyer belt moves forward by default. The motor is made to move in that direction using arduino. The webcam scans the part of belt in its field of view for any code (barcodes etc). When a product with this code enters this region the python script sends a data byte 'r' to the arduino via serial port.
* When the arduino recieves a data it reads it and if it is the predefined value then it stops the motor (conveyer belt) and indicates this using a blink of lights. Arduino then waits for the user to input something with the 4x4 numpad. When any key is pressed the lights blink and when a specific character is entered in the numpad then it breaks from receiving any input from numpad. For instance when the belt stops, the user types the keys 6,9,9,.,9,9,# in that order to give the input as 699.99.
* When the predefined character (# - here) is encounted the keys entered till then are combined and sent to python script. The python script then adds it into a list containing the code of the product. So we now have a list containing the type of code(EAN-13,CODE 128 etc), code of the product and its price.
* The scanner is paused for a certain duration so as to allow the user to enter price of the product. After the price is entered the belt starts moving, the scanner resumes scanning. When the next product is identified, its data is added to a list containing the list of all such products. A list of lists is created.
* All the unique elements in this list are seperated as details of same products entered more than once is not required. This new list is then made into a DataFrame making it easier to process. The Dataframe is converted into a csv file.
<br><br>
This csv file is what is referred to as _master file_ previously. The decription of the product can be added similarly. In this project only a small dataset is prepared. Due to lower fps of the camera and ineffective positioning of the camera only a few products could be scanned. This issue can be observed in the implementation video.
> The master file made in this project is [Price Index.csv](https://github.com/Ruthvik-1411/Automated_Conveyerbelt_Checkout/blob/main/price_entry/Price_index.csv).
The arduino code and python code can be found above with comments.

<b>Circuit:</b><br>
<img src="https://github.com/Ruthvik-1411/Automated_Conveyerbelt_Checkout/blob/main/price_entry/pe_ckt.jpg?raw=true" height=300 width=350>
