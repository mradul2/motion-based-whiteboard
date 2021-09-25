import cv2
import numpy as np

# Global variable ans that is initialised as a white image
ans = np.full((720,1280,3),255).astype("uint8")
# Capturing frames from WebCam
vid = cv2.VideoCapture(0)

# Values for font that will appear in the Board
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
color = (0,0,0)
thickness = 2

# Color ranges for the target shade of yellow pen
lower = np.array([29, 71, 67], dtype=np.uint8)
upper = np.array([63, 255, 255], dtype=np.uint8)

# Old x,y of Pen
oldx = 0
oldy = 0

# Old x,y of Eraser
olderx = 0
oldery = 0

# True when current mode is not changed
br = True
# True when writing
writing = True

while True:
    ret,frame = vid.read()
    # converting to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # creating binary mask according to the target color
    mask = cv2.inRange(hsv, lower, upper)
    # doing morphology to remove noise
    cv2.erode(mask,(5,5))
    cv2.dilate(mask,(5,5),None,None,3)
    # finding contour in that mask
    contours, heir = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    # Reset the board when pen is taken too near webCam
    if contours and cv2.contourArea(max(contours,key = cv2.contourArea)) > 250000:
        ans = np.full(frame.shape,255).astype("uint8")
        cv2.imshow("board",ans)
        oldx = 0
        oldy = 0
        cv2.waitKey(2000)
        br = False
    # Pen ( checking if writing is True ) 
    elif contours and cv2.contourArea(max(contours,key = cv2.contourArea)) > 60 and writing:
        c = max(contours, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        br = False
        # Start
        if oldx == 0 and oldy == 0:
            oldx = x
            oldy = y
        else:
            # Lines are drawn between the current x,y and just previous x,y
            cv2.line(ans,(1280 - oldx,oldy),(1280 - x,y),(255,0,0),3)
            oldx = x
            oldy = y
    # Eraser
    elif contours and cv2.contourArea(max(contours,key = cv2.contourArea)) > 100:
        c = max(contours, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        # Start
        if olderx == 0 and oldery == 0:
            olderx = x
            oldery = y
        else:
            # A white circle is created at just previous x,y
            cv2.circle(ans,(1280 - olderx,oldery),30,(255,255,255),-1)
            # A gray circle is created at current x,y
            cv2.circle(ans,(1280 - x,y),30,(211,211,211),-1)
            olderx = x
            oldery = y
        br = False
    # Nothing is infront of webCam
    else:
        # creating a white circle so that the last gray circle vanishes
        cv2.circle(ans,(1280 - olderx,oldery),30,(255,255,255),-1)
        oldx = 0
        oldy = 0
        # change mode (writing) if and only if br is False
        if not br:
            writing = not writing
        # ensuring that br is True always
        br = True

    # Code for showing text on the Board
    if writing:
        ans = cv2.putText(ans, 'ERASER', (20,600), font, fontScale, (255,255,255), thickness, cv2.LINE_AA)
        ans = cv2.putText(ans, 'PEN', (20,600), font, fontScale, color, thickness, cv2.LINE_AA)
    else:
        ans = cv2.putText(ans, 'PEN', (20,600), font, fontScale, (255,255,255), thickness, cv2.LINE_AA)
        ans = cv2.putText(ans, 'ERASER', (20,600), font, fontScale, color, thickness, cv2.LINE_AA)
        
    cv2.imshow("board",ans)

    k = cv2.waitKey(1)
    if k == 27:
        break