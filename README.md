# Automated_Conveyerbelt_Checkout

This repository contains the files and implementation videos of an automated conveyer belt checkout counter. The checkout counter contains three main parts:
* Conveyer belt
* Scanner( Laser or Camera) (camera is used here)
* Processor

This project explores two possible use cases of this automated conveyer belt checkout counter. The scenario is that there is a need for checkout counter that scans the products placed on the conveyer belt. Each product has a unique code and each code has its unique properties such as price, description etc of the item similar to a supermarket's inventory.
* Each item should have its price and decription assigned to it and the data is usually stored in a _master file_ than can be accessed. This can be done manually using excel or other softwares. The other way is for the products to be placed on the belt and as the scanner scans the item, the manager can input the price and other details through a keypad and do this for all the items they have thus creating a master file with all the details.
This is step 1 of the process of making an automated counter.<br><br>
The files for implementing step 1 are above in [Price Entry](https://github.com/Ruthvik-1411/Automated_Conveyerbelt_Checkout/tree/main/price_entry)

* Then comes step 2 where the process is completely automated. The customer or user can place all the products to be purchased on the belt. As the products are scanned, their data is looked up from the _master file_ and processed. The cost, quantity, description are all processed and can be used to display an invoice incase of a retail purchase. An automated checkout counter that gives an invoice after placing all the desired products on the belt is implemented. <br><br>
The files for implementing step 2 are above in [Checkout](https://github.com/Ruthvik-1411/Automated_Conveyerbelt_Checkout/tree/main/checkout)

> The images for different views of the conveyer belt can be found above [Conveyer Belt](https://github.com/Ruthvik-1411/Automated_Conveyerbelt_Checkout/tree/main/conveyer%20belt).
The inclination of the conveyer belt is adjustable and it can observed after looking at all the images in the folder.
