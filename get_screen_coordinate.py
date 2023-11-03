import cv2
# import matplotlib.pyplot as plt
import pyautogui
import numpy as np
import pyperclip

# Global variables
drawing = False  # True if mouse is pressed
start_x, start_y = -1, -1

# Return coordinate of text by location
# quardrant: The quadrant relative to the cursor
def text_quadrant(x, y, img_shape_x):
    rx, ry = x+4, y-7
    if y < 40:
        ry = y + 32
    if (img_shape_x - x) < 200:
        rx = x - 190
    return (rx, ry)

def brick_quadrant(x, y, img_shape_x, loc):
    # loc = 0: top left;  loc = 1: bottom right
    if loc == 0:
        rx, ry = x-37, y-32
    if loc == 1:
        rx, ry = x-10, y-5
    
    if y < 40:
        ry = ry + 40
    if (img_shape_x - x) < 200:
        rx = rx - 190
    if x < 40:
        rx = rx + 190
    return (rx,ry)

def color_inv(x,y):
    r = int(np.uint8(img[y,x,0]))
    g = int(np.uint8(img[y,x,1]))
    b = int(np.uint8(img[y,x,2]))
    r,g,b = 255-r,255-g,255-b
    return r, g, b

# Mouse callback function
def draw_rectangle(event, x, y, flags, param):
    global start_x, start_y, drawing

    # When moving cursor around, show the real-time cursor locationq
    if drawing == False:
        img_temp_clear = img.copy()
        cv2.putText(img_temp_clear, f"{x}, {y}", text_quadrant(x, y, img_temp_clear.shape[1]), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        cv2.rectangle(img_temp_clear, brick_quadrant(x,y,img_temp_clear.shape[1],0), brick_quadrant(x,y,img_temp_clear.shape[1],1), 
                      (int(img[y,x,0]), int(img[y,x,1]), int(img[y,x,2])), thickness=cv2.FILLED)
        cv2.rectangle(img_temp_clear, brick_quadrant(x,y,img_temp_clear.shape[1],0), brick_quadrant(x,y,img_temp_clear.shape[1],1), 
                      color_inv(x,y), thickness=1)
        cv2.imshow("Screenshot", img_temp_clear)
        # np.uint8(img[y,x,0]-255), np.uint8(img[y,x,1]-255), np.uint8(img[y,x,2]-255)
        # print(np.uint8(img[y,x,2]-255))
    
    # When press the button, start to draw the square
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_x, start_y = x, y

    # When drag the cursor, draw the square on the canvas
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_temp = img.copy()
            cv2.putText(img_temp, f"{start_x}, {start_y}", text_quadrant(start_x, start_y, img_temp.shape[1]),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(img_temp, f"{x}, {y}", text_quadrant(x, y, img_temp.shape[1]),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.rectangle(img_temp, brick_quadrant(x,y,img_temp.shape[1],0), brick_quadrant(x,y,img_temp.shape[1],1), 
                      (int(img[y,x,0]), int(img[y,x,1]), int(img[y,x,2])), thickness=cv2.FILLED)
            cv2.rectangle(img_temp, brick_quadrant(x,y,img_temp.shape[1],0), brick_quadrant(x,y,img_temp.shape[1],1), 
                       color_inv(x,y), thickness=1)
            cv2.rectangle(img_temp, (start_x, start_y), (x, y), (0, 255, 0), 2)
            cv2.imshow("Screenshot", img_temp)
    # When release the button, draw the final square and the coordinate
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.putText(img, f"{x}, {y}", text_quadrant(x, y, img.shape[1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(img, f"{start_x}, {start_y}", text_quadrant(start_x, start_y, img.shape[1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.rectangle(img, (start_x, start_y), (x, y), (0, 255, 0), 2)
        cv2.imshow("Screenshot", img)\
        # Return the coordinates:
        # print("Top-left corner:", start_x, start_y)
        # print("Top-right corner:", x, start_y)
        # print("Bottom-right corner:", x, y)
        # print("Bottom-left corner:", start_x, y)
        width = np.abs(x - start_x + 1); height = np.abs(y - start_y + 1)
        # return_text = f"{start_x}, {start_y}, {x}, {y}, {width}, {height}"
        return_text = f"{start_x}, {start_y}, {x}, {y}, {width}, {height}"
        pyperclip.copy(return_text)

# Load the image
img = np.array(pyautogui.screenshot())
img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
# img = cv2.imread("1691530840935.jpg")

# Create a window and set the mouse callbackq
cv2.namedWindow("Screenshot")
cv2.setMouseCallback("Screenshot", draw_rectangle)

# Display the image
cv2.imshow("Screenshot", img)

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):  # Press 'q' to quit
        break
    if cv2.getWindowProperty("Screenshot", cv2.WND_PROP_VISIBLE) < 1:
        break

cv2.destroyAllWindows()