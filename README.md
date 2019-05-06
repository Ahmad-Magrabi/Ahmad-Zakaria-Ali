Plant Detector 

Team members:

# Ahmad-Zakaria-Ali

# Tarek-Ibrahim



The project consists of two main parts :

1- Python code ( created and tested on pycharm ) : 
it divides the image to 3 main parts then detects the prescense of 
a plant in these three parts, then it compares it to a Threshold if
 it passes this threshold it will send a serial to the Arduino.


2- Arduino code : if it receives a serial from the python code it 
turns the Red Led ON.




Note :
     1- If will run the code without attaching the arduino, you Must delete the Arduino part in python code
    
	   2- The code build upon that the Arduino will be pulged in COM3 (USB).

	   3- Don't open multiple IDE for the same code as the PORT COM3 will be busy.
    
	   4- The Pin 13 in Arduino is where you should connect your Led in the arduino.
        
	   
