#IMPORTING LIBRARIES
import tkinter
from PIL import Image
from PIL import ImageTk
import numpy as np

from VidCap import MyVideoCapture

class App:
    def __init__(self, window, window_title, video_source=0):
        self.video_num=0
        self.is_recording=False
        self.record_check=True
        self.b_check=False
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a Background
        self.btn_snapshot=tkinter.Button(window, text="Background", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)
        # Button that lets the user to Reset the background
        self.btn_reset=tkinter.Button(window, text="Reset", width=50, command=self.reset)
        self.btn_reset.pack(anchor=tkinter.CENTER, expand=True)
        # Slider that lets the user to take threshold
        self.w1 = tkinter.Scale(window,from_=0,to=255)
        self.w1.set(50)
        self.w1.pack(side=tkinter.LEFT)
        self.w2 = tkinter.Scale(window,from_=0,to=255)
        self.w2.set(100)
        self.w2.pack(side=tkinter.LEFT)
        self.w3 = tkinter.Scale(window,from_=0,to=255)
        self.w3.set(50)
        self.w3.pack(side=tkinter.LEFT)
        self.w4 = tkinter.Scale(window,from_=0,to=255)
        self.w4.set(170)
        self.w4.pack(side=tkinter.LEFT)
        self.w5 = tkinter.Scale(window,from_=0,to=255)
        self.w5.set(255)
        self.w5.pack(side=tkinter.LEFT)
        self.w6 = tkinter.Scale(window,from_=0,to=255)
        self.w6.set(255)
        self.w6.pack(side=tkinter.LEFT)

        # Button that lets the user to RECORD a video
        self.btn_Record=tkinter.Button(window, text="Record", width=50, command=self.record,height=5,bg="white")
        self.btn_Record.pack(anchor=tkinter.CENTER, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()
        self.window.mainloop()
    def record(self):
        #IT WILL CREATE A NEW RECORDING OBJECT
        if self.record_check:
            self.btn_Record.configure(text="Recording")
            self.record_check=False
            self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
            name = "Output" + str(self.video_num)+"_.avi"
            self.out = cv2.VideoWriter(name,self.fourcc, 20.0, (640,480))
            self.is_recording=True
        else:
            self.btn_Record.configure(text="Record")
            self.record_check=True
            self.out.release()
            self.is_recording=False
            self.video_num+=1


    def reset(self):
        #TO RESET THE BACkGROUND
        self.b_check=False

    def snapshot(self):
        #TO TAKE A FIXED BACKGROUND
        ret, frame = self.vid.get_frame()
        self.background=frame
        self.b_check = True

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if self.b_check:
            #IF FIXED BACKGROUND IS AVAILABLE
            hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            lower_blue = np.array([self.w1.get(),self.w2.get(),self.w3.get()])
            upper_blue = np.array([self.w4.get(),self.w5.get(),self.w6.get()])
            mask = cv2.inRange(hsv,lower_blue,upper_blue)
            mask2 = cv2.bitwise_not(mask)

            #Segmenting the cloth out of the frame using bitwise and with the inverted mask
            res1 = cv2.bitwise_and(frame,frame,mask=mask2)

            res2 = cv2.bitwise_and(self.background, self.background, mask = mask)

            frame = cv2.addWeighted(res1,1,res2,1,0)

        if ret:
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        if self.is_recording:
            #IF RECORDING IS ON
            self.out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

        self.window.after(self.delay, self.update)
    def delete(self):
        self.vid.vid.release()
