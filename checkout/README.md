# Automated checkout and invoice printing
Part 2 of automated conveyer belt checkout counter.
>Implementation video of checkout part [Video](https://drive.google.com/file/d/1ZIcJs7d93SwWbs8vTnuJpx11dEur0fVV/view?usp=sharing).

In this part the user or customer places all the items he want to purchase on the conveyer belt. The belt keeps moving forward and the scanner scans the items and decodes the code in the frame. This data is looked up against data in the _master file_ and when the match is found, all the details of the item are retreived. If the item is scanned more than once, the quantity is updated accordingly. An invoice is generated using the quantity, price and description of the items scanned.

The steps followed in this part are as follows:
* The conveyer belt (motor) moves forward by default. The master file is imported and converted into a dataframe. The python script scans the field of view of the camera for any codes in the frame.
* When a code is detected it is added to list which is sent for further processing. A databyte 'r' is sent to arduino via serial port. When this data is recieved and matched against a predefined value the motor (belt) stops for 1 second and buzzer makes a small ring indicating that the item got scanned.
* The motor starts moving and scanner resumes scanning. All the items are scanned and when scanning is terminated the function make_bill is called. In this function the list obtained from scanning is looked up against the master file and when a match is found all the data pertaining to the item are added to a list. If the item is scanned more than once then the quantity of item is increased accordingly. A list containing the code, price, decription, quantity of items that got scanned is made.
* This list is then passed to a predefined invoice of certain format with the inputs as description, quantity and price of items. The function displays the invoice in the tkinter window along with the calculations of total price etc.

>The _master file_ that was mentioned previously is from the part 1 of the automated checkout counter with more products added to the list. The updated file is [Master price index.csv](https://github.com/Ruthvik-1411/Automated_Conveyerbelt_Checkout/blob/main/checkout/master_pindex.csv). The arduino and python code for this part can be found above.

Due to low fps and ineffective positioning of the camera, the products couldn't be scanned in one go. As the belt keeps moving sometimes the code cannot be scanned. So sometimes the items are positioned below the camera with hand to get them scanned. It can be avoided with a slower belt or high fps camera and proper lighting. This can also be observed in the implementation video.
* The invoices generated are :
[Invoice 1](https://github.com/Ruthvik-1411/Automated_Conveyerbelt_Checkout/blob/main/checkout/rc2.jpg)
| [Invoice 2](https://github.com/Ruthvik-1411/Automated_Conveyerbelt_Checkout/blob/main/checkout/rc3.jpg)
| [Invoice 3](https://github.com/Ruthvik-1411/Automated_Conveyerbelt_Checkout/blob/main/checkout/rc4.jpg)
| [Invoice 4](https://github.com/Ruthvik-1411/Automated_Conveyerbelt_Checkout/blob/main/checkout/rc5.jpg)

The setup looks like this: &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; The invoice looks like this: <br>
<img src="https://github.com/Ruthvik-1411/Automated_Conveyerbelt_Checkout/blob/main/checkout/accb_ck_video_Moment.jpg" height=450 width=500 align=top>
<img src="https://github.com/Ruthvik-1411/Automated_Conveyerbelt_Checkout/blob/main/checkout/rc2.jpg" height=450 width=450>
