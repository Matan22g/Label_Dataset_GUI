# Label_Dataset_GUI
Annotation tool is a GUI tool which allows the creating of a labelled image dataset.


# Intro
The aim of the specific tool is to specify locations of people's HEAD in images.
The tool receive as input, a path to a folder, containing images. It reads the
images and presents each image to the user. The user can specify the locations of
all the heads in each image. When all the images are annotated (or on a command,
specified below), the data is saved to a single file (in pickle format) in the specified folder.

Annotations of all the images are saved in a dictionary, with: 
keys = image name 
value = list of rectangles of all the heads in the image (i.e. [[c1, r1, w1, h1],[c2, r2,
w2, h2],...]), can be empty, if no heads were specified for the image.


# Interface
Keys:
- 'q', the program saves all the data and exits
- 's' - save current data
- 'left' - when left arrow key is pressed, go to the previous image
- 'right' - when right arrow key is pressed, go to the next image
- 'd' - when d is pressed - delete last specified rectangle in the current image (if no
rectangles specified - do nothing)
- left mouse button press - start drawing rectangle
- mouse move (while left button is pressed) - change rectangle according to mouse
coordinates
- left mouse button release - end drawing rectangle, save the rectangle to the
database
On each presented image all the existing rectangles should be shown in blue color
(only boundary, no fill). The rectangle in the process of drawing should be shown in
red.

# Requirements 
cv2, Pyqt5

# Example 

![alt text](https://i.ibb.co/q56PCR8/Screenshot-2021-07-29-011834.png)



