import PySide6.QtWidgets
import cv2
import sys
from os import walk
import dlib
import PySide6
from PySide6 import QtCore, QtWidgets, QtGui
import math



class DetectionMethod1:
    # Starts the first detection method, takes image path and returns Boolean
    def PixelDetector(self,img):
        #Reads the image from the path into an image object
        Image = cv2.imread(img)
        #Retrieves the resolution of the image into multiple variables
        height, width, channels = Image.shape
        #Tests each of the pixels by passing the image object and the height of the image
        condition1 = self.YellowDetector(Image,height)
        condition2 = self.GreenDetector(Image,height)
        condition3 = self.RedDetector(Image,height)
        #Uses the results of all the tests to determine if the filter is present
        if (condition1 == True and condition2 == True and condition3 == True):
            return True
        return False
    # Looks at the yellow pixel, takes image object and image height and returns Boolean
    def YellowDetector(self,img,h):
        #If the image is 1080p
        if (h == 1080):
            Marker1R = img[808][448][2]
            Marker1G = img[808][448][1]
            Marker1B = img[808][448][0]
        #If the image is 720p
        if (h == 720):
            Marker1R = img[539][289][2]
            Marker1G = img[539][289][1]
            Marker1B = img[539][289][0]
        #Takes the markers and checks to see if they are the correct colour all together
        if (Marker1G >= 150 and Marker1B <= 60 and Marker1R >= 150):
            return True
        else:
            return False
    # Looks at the Green pixel, takes image object and image height and returns Boolean
    def GreenDetector(self,img,h):
        # If the image is 1080p
        if (h == 1080):
            Marker1R = img[938][444][2]
            Marker1G = img[938][444][1]
            Marker1B = img[938][444][0]
        # If the image is 720p
        if (h == 720):
            Marker1R = img[625][296][2]
            Marker1G = img[625][296][1]
            Marker1B = img[625][296][0]
        # Takes the markers and checks to see if they are the correct colour all together
        if (Marker1G >= 185 and Marker1B <= 80 and Marker1R <= 80):
            return True
        else:
            return False
    # Looks at the red pixel, takes image object and image height and returns Boolean
    def RedDetector(self,img,h):
        # If the image is 1080p
        if (h == 1080):
            Marker1R = img[764][444][2]
            Marker1G = img[764][444][1]
            Marker1B = img[764][444][0]
        # If the image is 720p
        if (h == 720):
            Marker1R = img[509][296][2]
            Marker1G = img[509][296][1]
            Marker1B = img[509][296][0]
        # Takes the markers and checks to see if they are the correct colour all together
        if (Marker1G <= 60 and Marker1B <= 60 and Marker1R >= 100):
            return True
        else:
            return False
class DetectionMethod2:
    # Starts the second detection method, takes image path and returns Boolean and Float
    def EyeDetection(self,Image):
        # Reads the image from the path into an image object
        img = cv2.imread(Image)
        # Loads the xml file which contains the eye detection patterns
        eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
        eyes = eye_cascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=4)
        #creates two variables, wh stores the amount of white pixels, n stores the total pixels
        wh = 0
        n = 0
        #looking at each and every pixel within the boxes defined around the eyes
        for (x,y,w,h) in eyes:
            i = x
            #looking at each row
            while (i < x+w):
                j = y
                #looking at each coloumn
                while (j < y+h):
                    # retrieves the values of the pixel and then compares it to deem if it is "harsh white"
                    Marker1R = img[j][i][2]
                    Marker1G = img[j][i][1]
                    Marker1B = img[j][i][0]
                    if (Marker1G >= 205 and Marker1B >= 205 and Marker1R >= 205):
                        wh+=1
                    n+=1
                    j+=1
                i+=1
        #calculates the percentage of white pixels within the eyes
        p = (wh/n)*100
        #returns Boolean and the percentage
        return True, p
class DetectionMethod3:
    # Starts the Third detection method, takes image path and returns Boolean
    def dlib_Detection(self,img):
        #takes the image path and retrieves the landmarks from the image
        landmarks = self.landmarkFinder(img)
        #saves the landamrks for the width of the face and then calculates the distance between them
        Landmark1 = landmarks[0]
        Landmark17 = landmarks[16]
        FaceWidth = int(round(math.dist(Landmark1,Landmark17)))
        #saves the landmarks for the inter ocular region and then calculates the distance between them
        Landmark40 = landmarks[39]
        Landmark43 = landmarks[42]
        TopMid = ((Landmark40[0]+Landmark43[0])/2,(Landmark40[1]+Landmark43[1])/2)
        #Uses the middle point between the eyes and the landmark of the chin to calculate the height of the face
        Landmark9 = landmarks[9]
        FaceHeight = int(round(math.dist(Landmark9,TopMid)))
        #uses the face height and width to calculate a ratio of the size of the face
        FaceRatio = round((FaceWidth / FaceHeight),2)

        #if FaceRatio is less than 1 then the face is thinner than it is taller, if its more than 1 then its wider then tall.
        if(FaceRatio >= 1.33 and FaceRatio <= 1.40):
            return True
        return False
    #Takes the image path and returns the landmarks
    def landmarkFinder(self,img):
        #loads the landmark predictor
        p = "shape_predictor_68_face_landmarks.dat"
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(p)
        #loads the image in colour
        img = dlib.load_rgb_image(img)
        face = detector(img, 1)
        #loads all 69 landmarks into an array and then returns it
        landmarks = []
        for k, d in enumerate(face):
            landmark = predictor(img, d)
            for n in range(0, 68):
                x = landmark.part(n).x
                y = landmark.part(n).y
                landmarks.append((x, y))
        return landmarks
#Graphical User Interface Class
class UI(PySide6.QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.UINew()
    #Takes the bar object and colour and sets the bar to that colour
    def change_color(self, bar,  color):
        template_css = """QProgressBar::chunk { background: %s; }"""
        css = template_css % color
        bar.setStyleSheet(css)
    #creates the UI at the start of the applications runtime
    def UINew(self):
        #variables for both the names of files within folder and then the path to the folder
        self.filenames = None
        self.folderpath = None
        #creates elements of the UI adding them to the overall layout
        self.selectFilesButton = PySide6.QtWidgets.QPushButton("Select input folder")
        self.DetectorStarter = PySide6.QtWidgets.QPushButton("Start Mass Detection")
        self.MassBar = PySide6.QtWidgets.QProgressBar(self)
        self.MassBar.setObjectName("MassBar")
        #creates a second layout to embed within the main one, this one will hold the scroll area and have it display in a different format.
        self.layout = QtWidgets.QVBoxLayout(self)
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        #adds the widgets to the layout
        self.layout.addWidget(self.selectFilesButton)
        self.layout.addWidget(self.DetectorStarter)
        self.layout.addWidget(self.MassBar)
        self.layout.addWidget(self.scrollArea)
        #connects the buttons to functions
        self.selectFilesButton.clicked.connect(self.FileSelect)
        self.DetectorStarter.clicked.connect(self.MassDetection)
    #Allows for the files to be selected and then updates the GUI accordingly
    def FileSelect(self):
        self.dictionary = {}
        self.checker = {}
        #opens a dialoge window to select the folder and then saves the path to the variable, aswell as the array of file names
        folderpath = PySide6.QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        filenames = next(walk(folderpath), (None, None, []))[2]
        self.filenames = filenames
        self.folderpath = folderpath
        counter = 1
        #iterates through each of the files
        for i in filenames:
            self.dictionary[i]=0
            file = self.folderpath + "/" + i
            #creates a unique name for each of the widgets of each of the images by using the file name.
            r1 = "Result1-" + i
            r2 = "Result2-" + i
            r3 = "Result3-" + i
            bar = "Bar-" + i
            #sets the checkers of each of the results to 0 meaning that the coresponding test has not been run yet. Should a checker hold the value of 1 then that test can be skipped as it has already been ran
            self.checker[r1]=0
            self.checker[r2] = 0
            self.checker[r3] = 0
            #Loads the image and sets it as a pixel map to be displayed within the GUI
            self.image = PySide6.QtWidgets.QLabel()
            self.image.setObjectName(i)
            #Scales the image so that all the images are the same height
            pixmap = PySide6.QtGui.QPixmap(file).scaledToHeight(100)
            self.image.setPixmap(pixmap)
            self.gridLayout.addWidget(self.image,counter,0,3,1)
            #creates the button to run the "Baby Rattle" test, setting a unique name so that the text can be edited later
            self.R1 = PySide6.QtWidgets.QPushButton()
            self.R1.setObjectName(r1)
            self.R1.setText("Baby Rattle")
            self.gridLayout.addWidget(self.R1,counter,1,1,1)
            # creates the button to run the "Eye whiteness" test, setting a unique name so that the text can be edited later
            self.R2 = PySide6.QtWidgets.QPushButton()
            self.R2.setObjectName(r2)
            self.R2.setText("Eye Whites")
            self.gridLayout.addWidget(self.R2,(counter+1),1,1,1)
            # creates the button to run the "Face Morph" test, setting a unique name so that the text can be edited later
            self.R3 = PySide6.QtWidgets.QPushButton()
            self.R3.setObjectName(r3)
            self.R3.setText("Face Morph")
            self.gridLayout.addWidget(self.R3,(counter+2),1,1,1)
            # creates the confidence bar for the image with a unique name so that it can be called later
            self.confidenceBar = PySide6.QtWidgets.QProgressBar(self)
            self.confidenceBar.setObjectName(bar)
            self.gridLayout.addWidget(self.confidenceBar,(counter+3),0,1,2)
            #connects each of the buttons to the singlular detection methods
            self.R1.clicked.connect(self.Detection1)
            self.R2.clicked.connect(self.Detection2)
            self.R3.clicked.connect(self.Detection3)
            #increments the counter by 4 so that the next buttons dont overlap the last ones
            counter+=4
    #Function to get the filname from the button that was pressed, takes a button object as an argument and returns with a string of the file name the button is associated with
    def GetFileName(self,Button):
        ObjectName = Button.objectName()
        file = ObjectName.split("-")[1]
        return file
    #Changes the confidence bars colour depending on its value
    def SingleBarColourChanger(self,Bar,file):
        if (self.dictionary[file] <= 34):
            self.change_color(Bar,  "green")
        elif (self.dictionary[file] <= 67):
            self.change_color(Bar,  "orange")
        elif (self.dictionary[file] > 68):
            self.change_color(Bar,  "red")
    #Method runs the third detection method on its own
    def Detection3(self):
        #retrieves the button object that was pressed to call the method
        QPushButton = self.sender()
        #Passes the button object and retrieves the file name
        file = self.GetFileName(QPushButton)
        r3 = "Result3-" + file
        #validates if the test has been ran already or not
        if (self.checker[r3] == 0):
            #sets up some variables for handling the GUI objects
            File = self.folderpath + "/" + file
            bar = "Bar-" + file
            Bar = self.findChild(QtWidgets.QProgressBar, bar)
            #creates a new detector object
            detector = DetectionMethod3()
            try:
                #runs the detection method by passing it the file path
                result3 = detector.dlib_Detection(File)
                #If the result was positive/true then sets the button to display the result and then increments the confidence bar
                if (result3 == True):
                    QPushButton.setText("Face Ratio: Detected")
                    var = self.dictionary[file]
                    var = var + 33.3
                    self.dictionary[file]=var
                    Bar.setValue(self.dictionary[file])
                    self.SingleBarColourChanger(Bar,file)
                #if the result was false then sets the button to indicate the result
                if (result3 == False):
                    QPushButton.setText("Face Ratio: Not Detected")
            except:
                #if there were any error running the detection then an error message is posted to the GUI
                QPushButton.setText("Error With image, unable to run detection. Please check image size")
            #Sets the checker to 1 to prevent the test being ran again
            self.checker[r3] = 1
    def Detection2(self):
        # retrieves the button object that was pressed to call the method
        QPushButton = self.sender()
        # Passes the button object and retrieves the file name
        file = self.GetFileName(QPushButton)
        r2 = "Result2-" + file
        # validates if the test has been ran already or not
        if (self.checker[r2] == 0):
            # sets up some variables for handling the GUI objects
            File = self.folderpath + "/" + file
            bar = "Bar-" + file
            Bar = self.findChild(QtWidgets.QProgressBar, bar)
            # creates a new detector object
            detector = DetectionMethod2()
            try:
                # runs the detection method by passing it the file path
                result2, p = detector.EyeDetection(File)
                if (result2 == True):
                    #If the result was positive/true then sets the button to display the result and then increments the confidence bar, also depending on the value of p (percentage) the output message will change
                    QPushButton.setText("Baby Rattle: Detected")
                    var = self.dictionary[file]
                    if (p <= 0):
                        var = var + 0
                        R3Statement = "Eye Whites: Not Detected"
                    elif (p <= 0.01):
                        var = var + 9
                        R3Statement = "Eye Whites: Detected, Low Confidence"
                    elif (p <= 0.1):
                        var = var + 17
                        R3Statement = "Eye Whites: Detected, Medium Confidence"
                    elif (p <= 0.5):
                        var = var + 24
                        R3Statement = "Eye Whites: Detected, High Confidence"
                    elif (p <= 1):
                        var = var + 33.3
                        R3Statement = "Eye Whites: Detected, Extreme Confidence"
                    QPushButton.setText(R3Statement)
                    self.dictionary[file] = var
                    Bar.setValue(self.dictionary[file])
                    self.SingleBarColourChanger(Bar, file)
                # if the result was false then sets the button to indicate the result
                if (result2 == False):
                    QPushButton.setText("Eye Whites: Not Detected")
            except:
                # if there were any error running the detection then an error message is posted to the GUI
                self.widget2.setText("Error With image, unable to run detection. Face possibly not detected")
            # Sets the checker to 1 to prevent the test being ran again
            self.checker[r2] = 1
    def Detection1(self):
        # retrieves the button object that was pressed to call the method
        QPushButton = self.sender()
        # Passes the button object and retrieves the file name
        file = self.GetFileName(QPushButton)
        r1 = "Result1-" + file
        # validates if the test has been ran already or not
        if(self.checker[r1]==0):
            # sets up some variables for handling the GUI objects
            File = self.folderpath + "/" + file
            bar = "Bar-" + file
            Bar = self.findChild(QtWidgets.QProgressBar, bar)
            # creates a new detector object
            detector = DetectionMethod1()
            try:
                # runs the detection method by passing it the file path
                result1 = detector.PixelDetector(File)
                # If the result was positive/true then sets the button to display the result and then increments the confidence bar
                if (result1 == True):
                    QPushButton.setText("Baby Rattle: Detected")
                    var = self.dictionary[file]
                    var = var + 33.3
                    self.dictionary[file]=var
                    Bar.setValue(self.dictionary[file])
                    self.SingleBarColourChanger(Bar, file)
                # if the result was false then sets the button to indicate the result
                if (result1 == False):
                    QPushButton.setText("Baby Rattle: Not Detected")
            except:
                # if there were any error running the detection then an error message is posted to the GUI
                QPushButton.setText("Error With image, unable to run detection. Please check image size")
            # Sets the checker to 1 to prevent the test being ran again
            self.checker[r1] = 1

    def MassDetection(self):
        #creates all the detector objects
        detector1 = DetectionMethod1()
        detector2 = DetectionMethod2()
        detector3 = DetectionMethod3()
        #gets the total amount of files to be processed
        totalfiles = len(self.filenames)
        counter = 1
        #loop through all the files
        for i in self.filenames:
            #define some variables for the GUI to perform actions on the correct widget
            img = self.folderpath + "/" + i
            r1 = "Result1-" + i
            self.widget1 = self.findChild(QtWidgets.QPushButton, r1)
            r2 = "Result2-" + i
            self.widget2 = self.findChild(QtWidgets.QPushButton, r2)
            r3 = "Result3-" + i
            self.widget3 = self.findChild(QtWidgets.QPushButton, r3)
            bar = "Bar-" + i
            Bar = self.findChild(QtWidgets.QProgressBar, bar)
            try:
                # runs the detection method by passing it the file path
                result1 = detector1.PixelDetector(img)
                # If the result was positive/true then sets the button to display the result and then increments the confidence bar
                if (result1 == True):
                    self.widget1.setText("Baby Rattle: Detected")
                    var = self.dictionary[i]
                    var = var + 33.3
                    self.dictionary[i]=var
                    Bar.setValue(self.dictionary[i])
                if (result1 == False):
                    # if the result was false then sets the button to indicate the result
                    self.widget1.setText("Baby Rattle: Not Detected")
            except:
                # if there were any error running the detection then an error message is posted to the GUI
                self.widget1.setText("Error With image, unable to run detection. Please check image size")
            # Sets the checker to 1 to prevent the test being ran again
            self.checker[r1] = 1
            try:
                # runs the detection method by passing it the file path
                result2, p = detector2.EyeDetection(img)
                # If the result was positive/true then sets the button to display the result and then increments the confidence bar, also depending on the value of p (percentage) the output message will change
                if (result2 == True):
                    self.widget2.setText("Baby Rattle: Detected")
                    var = self.dictionary[i]
                    if (p <= 0):
                        var = var + 0
                        R3Statement = "Eye Whites: Not Detected"
                    elif (p <= 0.01):
                        var = var + 9
                        R3Statement = "Eye Whites: Detected, Low Confidence"
                    elif (p <= 0.1):
                        var = var + 17
                        R3Statement = "Eye Whites: Detected, Medium Confidence"
                    elif (p <= 0.5):
                        var = var + 24
                        R3Statement = "Eye Whites: Detected, High Confidence"
                    elif (p <= 1):
                        var = var + 33.3
                        R3Statement = "Eye Whites: Detected, Extreme Confidence"
                    self.widget2.setText(R3Statement)
                    self.dictionary[i] = var
                    Bar.setValue(self.dictionary[i])
                if (result2 == False):
                    # if the result was false then sets the button to indicate the result
                    self.widget2.setText("Eye Whites: Not Detected")
            except:
                # if there were any error running the detection then an error message is posted to the GUI
                self.widget2.setText("Error With image, unable to run detection. Face possibly not detected")
            # Sets the checker to 1 to prevent the test being ran again
            self.checker[r2] = 1
            try:
                # runs the detection method by passing it the file path
                result3 = detector3.dlib_Detection(img)
                # If the result was positive/true then sets the button to display the result and then increments the confidence bar
                if (result3 == True):
                    self.widget3.setText("Face Ratio: Detected")
                    var = self.dictionary[i]
                    var = var + 33.3
                    self.dictionary[i] = var
                    Bar.setValue(self.dictionary[i])
                if (result3 == False):
                    # if the result was false then sets the button to indicate the result
                    self.widget3.setText("Face Ratio: Not Detected")
            except:
                # if there were any error running the detection then an error message is posted to the GUI
                self.widget3.setText("Error With image, unable to run detection. Please check image size")
            # Sets the checker to 1 to prevent the test being ran again
            self.checker[r3] = 1
            #sets the % value for the progress bar
            value=(counter/totalfiles)*100
            self.MassBar.setValue(value)
            #Updates the confidence bar of the image to the correct colour
            self.SingleBarColourChanger(Bar, i)
            counter+=1


#creates the window of the application
if __name__ == "__main__":
    app = PySide6.QtWidgets.QApplication([])
    #initiates the GUI with a size of 1000,1000
    widget = UI()
    widget.resize(1000, 1000)
    widget.show()

    sys.exit(app.exec())
