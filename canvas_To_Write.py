import numpy as np

import keras

from tensorflow.keras.models import load_model
'''IMPORTING THE DEPENDENCIES HERE AM USING TKINKER 
  FOR CALCULATION NUMPY AND MATH TO READ WRITING IMPORTING IMAGE'''

from numpy import argmax
from tkinter import *
import tkinter as tk
import math
from PIL import Image, ImageDraw


model = load_model("model_to_find_handWritten_numbers.h5")

'''CREATING A CANVAS '''
white = (200, 25, 255)
black = (255, 0, 0)
window = Tk()
 
window.title("Handwriting Predector")
 
window.geometry('700x700')
# heading 
lbl = Label(window, text="Write number with your mouse in the Blue square",font=('Arial Bold',18))
 
lbl.grid(column=3, row=0)

lbl1 = Label(window, text="PREDICTION",font=('Arial Bold',12))
 
lbl1.grid(column=5, row=1)

# canvas to write numbers and creating to add the written value of coordinates into lists with
# respect to their coordinate axis
canvas_width = 400
canvas_height = 400
image1 = Image.new("RGB", (canvas_width, canvas_height),white)
draw = ImageDraw.Draw(image1)
counter=0
xpoints=[]
ypoints=[]
x2points=[]
y2points=[]
global predictions
predictions = []
number1 = []
digits=0

# function to read the mouse drawing
def paint( event ):
    x1, y1 = ( event.x - 4 ), ( event.y - 5 )
    x2, y2 = ( event.x + 5 ), ( event.y + 5 )
    w.create_oval( x1, y1, x2, y2, fill = 'red' )
    xpoints.append(x1)
    ypoints.append(y1)
    x2points.append(x2) 
    y2points.append(y2)    

# function to generate image with respect to writing
def imagen ():
    global counter
    global xpoints
    global ypoints    
    global x2points
    global y2points
    counter=counter+1

    image1 = Image.new("RGB", (canvas_width, canvas_height),black)
    draw = ImageDraw.Draw(image1) 

    elementos=len(xpoints)
    
    

    for p in range (elementos):
        x=xpoints[p]
        y=ypoints[p]
        x2=x2points[p]
        y2=y2points[p] 
        draw.ellipse((x,y,x2,y2),'white')
        w.create_oval( x-5, y-5, x2+5, y2+5,outline='yellow', fill = 'yellow' )
    
    # lets predict the written number using our model b4 that try to reshape the 
    #   the image so that model can predict so i did the same x point operation 
    size=(28,28)
    image1 = image1.resize(size)

    
    image1 = image1.convert('L')
    image1 = np.array(image1)
    image1 = image1.reshape(-1, 28, 28, 1)
    image1 = image1.astype('float32')
    image1 /= 255.0

    
    predictions.append(argmax(model.predict(image1)))
    lbl2 = Label(window, text=predictions[counter-1],font=('Arial Bold',30))
    lbl2.grid(column=5, row=2)
    

    xpoints=[]
    ypoints=[]
    x2points=[]
    y2points=[] 

## window to get input
w = Canvas(window, 
           width=canvas_width, 
           height=canvas_height,bg='yellow')
w.grid(column=3,row=2)

def delete ():
    global counter
    counter = counter-1
    del predictions[counter]
    w1 = Canvas(window, 
           width=27, 
           height=35,bg='yellow')
    w1.grid(column=5,row=2)
    
def reset():
    global predictions
    global counter
    predictions=[]
    counter=0
    w1 = Canvas(window, 
           width=27, 
           height=35,bg='yellow')
    w1.grid(column=5,row=2)
    
w1 = Canvas(window, width=27, height=35,bg='yellow')
w1.grid(column=5,row=2)

# w1 = Canvas(window, width=27, height=35,bg='royal blue')
# w1.grid(column=8,row=2)

w.bind( "<B1-Motion>", paint )
button = tk.Button(window, text='Predict image', width=35, command=imagen)
button.grid(column=3,row=3)

# button1 = tk.Button(window, text='delete', width=35, command=delete)
# button1.grid(column=3,row=4)

button3 = tk.Button(window, text='Reset', width=35, command=reset)
button3.grid(column=3,row=5)


window.mainloop()