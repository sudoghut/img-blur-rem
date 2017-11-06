from PIL import Image, ImageTk, ImageFilter
import tkinter, math, os, random
from tkinter import PhotoImage,Label
import random
import copy

global_two_points, x_1, y_1, x_2, y_2, angle = [0, 0, 0, 0, 0, 0]
canvas, image_blur, image_clear = [0, "", ""]
file_path = "img/"
list_index_pointer = 0
file_list = []
width, height = [0, 0]

class img_blur_rem(tkinter.Frame):
    def __init__(self, root, file):
        tkinter.Frame.__init__(self, root)
        global canvas, image_blur, image_clear, file_list, file_path, list_index_pointer
        global width, height
        #open file
        print(file)
        image = Image.open(file)
        #blur the image
        image_blur = image.filter(ImageFilter.GaussianBlur(radius=10))
        image_clear = image.filter(ImageFilter.GaussianBlur(radius=0))
        

        #resize the width and height
        width = 800
        ratio = float(width)/image.size[0]
        height = int(image.size[1]*ratio)
        image_blur = image_blur.resize( (width, height), Image.BILINEAR )
        image_clear = image_clear.resize( (width, height), Image.BILINEAR )

        #setup scrollbar
        #self.canvas = tkinter.Canvas(self, width=image.size[0], height=image.size[1])
        self.canvas = tkinter.Canvas(self, width=width, height=height)
        self.xsb = tkinter.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.ysb = tkinter.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        #self.canvas.configure(scrollregion=(0,0,1000,1000))
        #self.canvas.configure(scrollregion=(0,0,image.size[0],image.size[1]))
        #self.canvas.configure(scrollregion=(0,0,image.size[0],image.size[1]))
        self.canvas.configure(scrollregion=(0,0,width,height))

        self.xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
        self.canvas.grid(row=0, column=0, sticky="nsew")       
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #load image file
        image_tk = ImageTk.PhotoImage(image_blur)
        self.canvas.create_image(0, 0, image=image_tk, anchor="nw")
        self.canvas.image = image_tk
        # self.canvas.create_text(10,10, anchor="nw", text="Click and drag to move the canvas\nScroll to zoom.")
        # for n in range(50):
        #     x0 = random.randint(0, 900)
        #     y0 = random.randint(50, 900)
        #     x1 = x0 + random.randint(50, 100)
        #     y1 = y0 + random.randint(50,100)
        #     color = ("red", "orange", "yellow", "green", "blue")[random.randint(0,4)]
        #     self.canvas.create_rectangle(x0,y0,x1,y1, outline="black", fill=color, activefill="black", tags=n)

        #bind keybroad
        self.canvas.bind("<ButtonRelease-1>", callback)
        self.canvas.bind("<ButtonPress-3>", self.move_start)
        self.canvas.bind("<B3-Motion>", self.move_move)
        #bind escape
        root.bind("<Escape>", esc_clear)
        root.bind("<c>", no_gaussianblur)
        #linux scroll
        #self.canvas.bind("<Button-4>", self.zoomerP)
        #self.canvas.bind("<Button-5>", self.zoomerM)
        #windows scroll
        #self.canvas.bind("<MouseWheel>",self.zoomer)
        root.bind("<Left>", to_before)
        root.bind("<Right>", to_next)
        canvas = self.canvas

    #move
    def move_start(self, event):
        self.canvas.scan_mark(event.x, event.y)
    def move_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    #windows zoom
    def zoomer(self,event):
        if (event.delta > 0):
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        elif (event.delta < 0):
            self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    #linux zoom
    def zoomerP(self,event):
        self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
    def zoomerM(self,event):
        self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

def to_before(event):
    print("left")
    global global_two_points, x_1, y_1, x_2, y_2, angle
    global canvas, image_blur, image_clear, file_list, file_path, list_index_pointer
    global width, height
    global_two_points, x_1, y_1, x_2, y_2, angle = [0, 0, 0, 0, 0, 0]
    list_index_pointer-=1
    if list_index_pointer < 0:
        list_index_pointer = 0
    if list_index_pointer>(len(file_list) - 1):
        list_index_pointer = len(file_list) - 1
    print(file_path+file_list[list_index_pointer])
    image = Image.open(file_path+file_list[list_index_pointer])
    ratio = float(width)/image.size[0]
    height = int(image.size[1]*ratio)
    canvas.config(width=width, height=height)
    image_blur = image.filter(ImageFilter.GaussianBlur(radius=10))
    image_clear = image.filter(ImageFilter.GaussianBlur(radius=0))
    image_blur = image_blur.resize( (width, height), Image.BILINEAR )
    image_clear = image_clear.resize( (width, height), Image.BILINEAR )
    image_tk = ImageTk.PhotoImage(image_blur)
    canvas.create_image(0, 0, image=image_tk, anchor="nw")
    canvas.image = image_tk

def to_next(event):
    print("right")
    global global_two_points, x_1, y_1, x_2, y_2, angle
    global canvas, image_blur, image_clear, file_list, file_path, list_index_pointer
    global width, height
    global_two_points, x_1, y_1, x_2, y_2, angle = [0, 0, 0, 0, 0, 0]
    list_index_pointer+=1
    if list_index_pointer < 0:
        list_index_pointer = 0
    if list_index_pointer>(len(file_list) - 1):
        list_index_pointer = len(file_list) - 1
    print(file_path+file_list[list_index_pointer])
    image = Image.open(file_path+file_list[list_index_pointer])
    ratio = float(width)/image.size[0]
    height = int(image.size[1]*ratio)
    canvas.config(width=width, height=height)
    image_blur = image.filter(ImageFilter.GaussianBlur(radius=10))
    image_clear = image.filter(ImageFilter.GaussianBlur(radius=0))
    image_blur = image_blur.resize( (width, height), Image.BILINEAR )
    image_clear = image_clear.resize( (width, height), Image.BILINEAR )
    image_tk = ImageTk.PhotoImage(image_blur)
    canvas.create_image(0, 0, image=image_tk, anchor="nw")
    canvas.image = image_tk

def callback(event):
    global global_two_points, x_1, y_1, x_2, y_2, angle
    global canvas, image_blur, image_clear
    
    global_two_points+=1
    if global_two_points == 1:
        x_1 = float(event.x)
        y_1 = float(event.y)       
    elif global_two_points>1:
        x_2 = event.x
        y_2 = event.y
        if (math.sqrt(pow(x_1-x_2, 2) + pow(y_1-y_2, 2))) != 0:
            angle = math.degrees(math.acos((x_2-x_1)/(math.sqrt(pow(x_1-x_2, 2) + pow(y_1-y_2, 2)))))
            if y_2 > y_1:
                angle = 360 - angle
            print(angle)
            width, height = image_blur.size
            bound = ()
            if (angle>315 and angle<=360) or (angle<=45 and angle >=0):
                bound = (int(x_1), 0, width, height)
            if angle>45 and angle<=135:
                bound = (0, 0, width, int(y_1))
            if angle>135 and angle<=225:
                bound = (0, 0, int(x_1), height)
            if angle>225 and angle<=315:
                bound = (0, int(y_1), width, height)
            image_blur_current = copy.deepcopy(image_blur)
            image_clear_temp = copy.deepcopy(image_clear)
            clips = image_clear_temp.crop(bound)
            image_blur_current.paste(clips, bound)
            image_tk = ImageTk.PhotoImage(image_blur_current)
            canvas.create_image(0, 0, image=image_tk, anchor="nw")
            canvas.image = image_tk
            print(bound)
        global_two_points, x_1, y_1, x_2, y_2 = [0, 0, 0, 0, 0]

    print("clicked at: ", event.x, event.y)

def esc_clear(event):
    global global_two_points, x_1, y_1, x_2, y_2, angle
    global canvas, image_blur, image_clear, file_list, file_path, list_index_pointer
    global width, height
    global_two_points, x_1, y_1, x_2, y_2, angle = [0, 0, 0, 0, 0, 0]
    # image_tk = ImageTk.PhotoImage(image_blur)
    # canvas.create_image(0, 0, image=image_tk, anchor="nw")
    # canvas.image = image_tk

    image = Image.open(file_path+file_list[list_index_pointer])
    print(list_index_pointer)
    ratio = float(width)/image.size[0]
    height = int(image.size[1]*ratio)
    canvas.config(width=width, height=height)
    image_blur = image.filter(ImageFilter.GaussianBlur(radius=10))
    image_clear = image.filter(ImageFilter.GaussianBlur(radius=0))
    image_blur = image_blur.resize( (width, height), Image.BILINEAR )
    image_clear = image_clear.resize( (width, height), Image.BILINEAR )
    image_tk = ImageTk.PhotoImage(image_blur)
    canvas.create_image(0, 0, image=image_tk, anchor="nw")
    canvas.image = image_tk

def no_gaussianblur(event):
    global canvas, image_blur, image_clear
    image_tk = ImageTk.PhotoImage(image_clear)
    canvas.create_image(0, 0, image=image_tk, anchor="nw")
    canvas.image = image_tk

if __name__ == "__main__":
    root = tkinter.Tk()
    file_list = os.listdir(file_path)
    random.shuffle(file_list)
    #print(file_list) 
    img_blur_rem(root, file_path+file_list[list_index_pointer]).pack(fill="both", expand=True)
    root.mainloop()
