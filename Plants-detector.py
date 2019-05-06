'''
"Plant detection"  project

Team Members :
                - Ahmad Zakaria Ali Mohamed
                - Tarek Ibrahim Hammad



'''
import cv2
import numpy as np
import serial


# creating class to handle plant detection
class plantDetection:
    def __init__(self,img):
        self.height = img.shape[0]
        self.width = img.shape[1]
        self.part_width = img.shape[1]//3

    #creating Method to blurs the image and converts to HSV color scale
    def preprocess(self, img):

        kernel = 15
        #step 1:blur image
        img_blur = cv2.medianBlur(img,kernel)
        #step 2:convert to HSV color scale
        img_hsv = cv2.cvtColor(img_blur,cv2.COLOR_BGR2HSV)
    
        return img_hsv


    # Create a mask containing with green colored pixels included
    def createMask(self, img_hsv):

        sensitivity = 20
        lower_bound = np.array([50 - sensitivity, 100, 60])
        upper_bound = np.array([50 + sensitivity, 255, 255])

        #create mask
        msk = cv2.inRange(img_hsv, lower_bound, upper_bound)

        return msk

    #apply morphology transformation
    def transform(self, msk):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))

        #erosion and dilation
        res_msk = cv2.morphologyEx(msk, cv2.MORPH_OPEN, kernel)
        res_msk = cv2.morphologyEx(res_msk, cv2.MORPH_CLOSE, kernel)

        return res_msk
    #returns the percentage of white in a binary image

    def calcPercentage(self, msk):
        height, width = msk.shape[:2]
        num_pixels = height * width
        count_white = cv2.countNonZero(msk)
        percent_white = (count_white/num_pixels) * 100
        percent_white = round(percent_white,2)

        return percent_white
    #Divide the mask into 3 parts and calculate the percentage of plants in each part
    #This will be used to find the direction in which the bot has to move
    def plantPercentage(self, msk):

        left_part = msk[:,:self.part_width]
        mid_part = msk[:,self.part_width:2*self.part_width]
        right_part = msk[:,2*self.part_width:]

        #percentage of plant
        left_percent = self.calcPercentage(left_part)
        mid_percent = self.calcPercentage(mid_part)
        right_percent = self.calcPercentage(right_part)

        return [left_percent, mid_percent, right_percent]
    #takes a 3-element list containing the left, middle and right percentages and writes them to an image

    def markPercentage(self, img, percentage):
        part_width = self.width//3

        font = cv2.FONT_HERSHEY_SIMPLEX
        idx = 0
        #write text in each partition
        for i in range(3):
            idx  += 1
            cv2.putText(img, str(percentage[i]) + "%", (int(part_width*(i + 0.34)), self.height//2), font, 1.0, (0,0,255),3, cv2.LINE_AA)
        return img

def main():
    #interfacing with User

    print("Welcome to plant detect program!")
    print("The python part will detect the plant in an image")
    print("Then the 'arduino' will turn on a Led in case if it finds a plant.")

    img = cv2.imread("Target.jpg")
    print(img.shape)
    img_resize = cv2.resize(img, (800,500))

    plant = plantDetection(img)

    img_hsv = plant.preprocess(img)

    msk = plant.createMask(img_hsv)

    msk = plant.transform(msk)

    percentage = plant.plantPercentage(msk)

    #To Arduino if it passes the threshold

    threshold = [15, 15, 15]
    if (percentage[0] > threshold[0] or percentage[1] > threshold[1] or percentage[2] > threshold[2]):
        ser1 = serial.Serial('COM3', 9600)
        ser1.write('s'.encode())
        print("A plant has been detected!")
    else:
        print("No plant in the image!")
    res =plant. markPercentage(img_resize, percentage)
    res_msk = cv2.bitwise_and(img,img,mask = msk)
    cv2.imshow('Res',res)
    cv2.imshow('Mask', res_msk)
    cv2.imshow('Frame',img)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()