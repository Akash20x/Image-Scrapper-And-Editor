from tkinter import* # python library for GUI
from tkinter.colorchooser import* # get color window to choose color
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageChops,ImageTk # Get pillow library image functions
from tkinter import Tk, Label, Button, Canvas, Toplevel, simpledialog, messagebox #import main modules
from tkinter.filedialog import askopenfilename # To get image from the system
import basic_functions # Get some defined functions from basic_functions.py
import tkinter as tk 
import os # Library for interaction with operating system
import requests # To send HTTP request to specified URL and get response content
from bs4 import BeautifulSoup # To extract data from HTML and XML Files 
import time
from selenium import webdriver
import glob
import pyautogui

# Google image search url
google_image = \
'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

# Assign Folder where all scrapped images store 
SAVE_FOLDER = 'images'

data=None
img = None
img_copy = None
app_title = "Contents"
root = None
tk_im = None
color = (246,36,89,1) #Radical red color
filepath = ""
filepath2=""
content=None
img2=None
my_label=None
path=None
xi=0
yi=0
wi=0
hi=0
s=0
count=0
my_list=[]
tkfile=[]

x=0
y=0
rect = None
shape1=None
shape2=None
shape3=None
shape4=None
start_x = None
start_y = None
oval=None

topx, topy, botx, boty = 0, 0, 0, 0
rect_id = None

view_img=None
tk_im_view=None

def fetch(query: str, max_img: int, wd: webdriver):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    count = 0
    results = 0
    while count < max_img:
        scroll_to_end(wd)

        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)


        print(f"Found: {number_results} search results. Extracting links from {results}:{number_results}")

        for img in thumbnail_results[results:number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(1)
            except Exception:
                continue

            # extract image urls
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            count = len(image_urls)

            if len(image_urls) >= max_img:
                print(f"Found: {len(image_urls)} image links, done!")
                break
        else:
            print("Found:", len(image_urls), "image links, looking for more ...")
            time.sleep(30)
            return
            load_more_button = wd.find_element_by_css_selector(".mye4qd")
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")

        # move the result startpoint further down
        results = len(thumbnail_results)

    return image_urls


def persist_image(folder_path:str,url:str, counter):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        f = open(os.path.join(folder_path, 'jpg' + "_" + str(counter) + ".jpg"), 'wb')
        f.write(image_content)
        f.close()
        print(f"SUCCESS - saved {url} - as {folder_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")


def search_and_download(search_term: str, driver_path: str, target_path='./images', number_images=10):
    target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    with webdriver.Chrome(executable_path=driver_path) as wd:
        fetch_result = fetch(search_term, number_images, wd=wd) #Fetch urls for query

    counter = 0
    for url in fetch_result:
        persist_image(target_folder, url, counter) #Write images in the folder
        counter += 1

def download_images(data,toc):
    DRIVER_PATH = './chromedriver.exe'
    search_term = data
   
    number_images = toc

    search_and_download(search_term=search_term, driver_path=DRIVER_PATH, number_images = number_images)
    print('Searching Begin.....')  
    return data   

def forward(count):
    global button_forward
    global button_back
    global canvas
    global tkfile
    global img
    global tk_im

    try:
        img=my_list[count]
    except:
        if count!=5:
            messagebox.showinfo("Message", "Item Not Found: Defult Background Image")
            get_image("background")
        
    tk_im = ImageTk.PhotoImage(img) 
    display_image(img,canvas,tk_im)
     
    button_back = Button(canvas, text='<--', command=lambda: back(count-1))
    button_back.place(rely=1,relx=0,anchor=SW)

    if count == 5:
        button_forward = Button(canvas, text='-->', state=DISABLED)
    else:
        button_forward = Button(canvas, text='-->', command=lambda: forward(count+1))

    button_forward.place(rely=1,relx=1,anchor=SE)


def back(count):
    global button_forward
    global button_back
    global canvas
    global tkfile
    global img
    global tk_im

    img=my_list[count]
    tk_im = ImageTk.PhotoImage(img) 
    display_image(img,canvas,tk_im)
    
    button_forward = Button(canvas, text='-->', command=lambda: back(count+1))

    if count == 1:
        button_back = Button(canvas, text='<--', state=DISABLED)
    else:
        button_back = Button(canvas, text='<--', command=lambda: back(count-1))
    
    button_back.place(rely=1,relx=0,anchor=SW)
    button_forward.place(rely=1,relx=1,anchor=SE)


# Function to download the given image and return image in PIL and Tkinter format
def get_image(data):
    global my_list
    global tkfile
    global img
    global tk_im
    global path
    toc=5
    ans2=messagebox.askquestion("Mode","Are you online?")
    my_list.clear()
    tkfile.clear()
    if ans2=="yes":
        m=download_images(data,toc)
    else:
        m=data
    print(m)

    path="images/"+ m +"/"+"*.*"
    
    for file in glob.glob(path):
        try:
            img = Image.open(file)
            img = img.resize((500,500),resample=Image.NEAREST)
        except:
            pass  
        my_list.append(img)
        
        try:
            tk_im = ImageTk.PhotoImage(img) 
        except:
            pass
        tkfile.append(tk_im)
 
    print(img)
    if img==None:
        get_image("background")

    return img, tk_im

# Download and return second image in PIL format during merge function
def get_image2(data2):
    global tk_im
    global img2
    global canvas
    global color
    global c
    global filepath2
    toc=1
    c=download_images(data2,toc) 
    filepath2 = "./images/" + c + "/jpg_0"+".jpg"
    img2 = Image.open (filepath2) # im2 is image in PIL format
    img2 = img2.resize((500,500),resample=Image.NEAREST)
    return img2

# Function to get image from the system and return it in PIL and tkinter format
def getimg():
    global filepath
    global img2
    global filepath2
    Tk().withdraw()
    filepath = askopenfilename()
    img2 = Image.open(filepath)
    img2 = img2.resize((500,500),resample=Image.NEAREST)
    filepath2=filepath
    tk_im = ImageTk.PhotoImage(img2) 
    return img2,tk_im

 # Function to display image in canvas    
def display_image(im, canvas,tk_im):  # im is image in PIL format 
    image_window.geometry(str(im.size[0])+"x"+str(im.size[1])) #im.size is returning a tuple (width,height)
    canvas.pack(fill="both",expand="yes")
    canvas.create_image(im.size[0]/2, im.size[1]/2, image=tk_im) # coordinates of Pil image and display image

def draw_mode():
    global canvas
    canvas.bind("<Button 1>", draw_point)
    canvas.bind("<B1-Motion>", draw_curve)
  
 # check whether mouse pointer coordinates isless than or equal to image size coordinte
 # USE draw_paint again and again with mouse position to draw free hand
def draw_curve(event):
    global img
    if (event.x <= img.size[0] and event.y <= img.size[1]):
        draw_point(event)
             
# pick color from the main image in canvas             
def color_picker():
    global canvas
    canvas.bind("<Button 1>", pick_color)  

# Function to draw a point with respect to mouse position coordiantes
def draw_point(event):
    global tk_im
    global img
    global canvas
    global color
    x1,y1=(event.x-2),(event.y-2)
    x2,y2=(event.x+2),(event.y+2)   
    canvas.create_oval(x1,y1,x2,y2,outline="#f11",fill="green", width=2)


def on_button_press_rect(event):
    global start_x
    global start_y
    global canvas
    global rect
    global tk_im
    global img
    global color
    start_x = event.x
    start_y = event.y
    rect = canvas.create_rectangle(0, 0, 0, 0,outline="#fb0",fill="blue")



def on_button_press_oval(event):
    global start_x
    global start_y
    global canvas 
    global oval
    global tk_im
    global img
    global color
    start_x = event.x
    start_y = event.y
    oval=canvas.create_oval(0, 0, 0, 0, outline="#f11",fill="#1f1", width=2)
 

def on_button_press_triangle(event):
    global x
    global y
    global start_x
    global start_y
    global canvas
    global shape1
    global shape2
    global shape3
    global shape4
    global tk_im
    global img
    global color
    start_x = event.x
    start_y = event.y
    shape1=canvas.create_line(0,0,0,0, fill = "blue", width = 1)
    shape2=canvas.create_line(0,0,0,0, fill = "red", width = 1)
    shape3=canvas.create_line(0,0,0,0, fill = "green", width = 1)
    shape4=canvas.create_polygon([10, 10, 20,20, 30, 30, 10,10], fill='blue')


def on_move_press_rect(event):
    global rect
    global start_y
    global start_x
    global canvas
    global tk_im
    global img
    global color
    curX, curY = (event.x, event.y)
    canvas.coords(rect, start_x, start_y, curX, curY)



def on_move_press_oval(event):
    global start_y
    global start_x
    global canvas 
    global oval
    global tk_im
    global img
    global color
    curX, curY = (event.x, event.y)
    canvas.coords(oval, start_x, start_y, curX, curY)

   
def on_move_press_triangle(event):
    global start_y
    global start_x
    global canvas
    global shape1
    global shape2
    global shape3
    global shape4
    global tk_im
    global img
    global color
    curX, curY = (event.x, event.y)
    canvas.coords(shape1, start_x, start_y, curX, curY)
    a=start_x
    b=start_y
    c=curX
    d=curY
    e=c/2
    f=d/2
    canvas.coords(shape2, a, b, e, f)
    canvas.coords(shape3, c, d, e,f)
    canvas.coords(shape4,a,b,c,d,e,f,a,b)


def on_button_release(event):
    pass

def draw_rect():
    global canvas
    canvas.bind("<ButtonPress-1>", on_button_press_rect)
    canvas.bind("<B1-Motion>", on_move_press_rect)
    canvas.bind("<ButtonRelease-1>", on_button_release)

    
def draw_oval():
    global canvas
    canvas.bind("<ButtonPress-1>", on_button_press_oval)
    canvas.bind("<B1-Motion>", on_move_press_oval)
    canvas.bind("<ButtonRelease-1>", on_button_release)

    
def draw_triangle():
    global canvas
    canvas.bind("<ButtonPress-1>", on_button_press_triangle)
    canvas.bind("<B1-Motion>", on_move_press_triangle)
    canvas.bind("<ButtonRelease-1>", on_button_release)


def inc():
    global my_label2
    global s
    i=0
    while i<1:
        my_label2.configure(font=('Gotham Medium',s,"bold"))
        s+=1
        i+=1

def dec():
    global my_label2
    global s
    i=0
    while i<1:
        my_label2.configure(font=('Gotham Medium',s,"bold"))
        s-=1
        i+=1

# Function to add label text on the image on the canvas
def add_text():
    global tk_im
    global img
    global canvas
    global color
    global s
    global my_label2
    content1 = simpledialog.askstring(title=app_title, prompt="Enter text: ") # input text for Label text
    content2=get_definition2(content1)   # input text for label meaning
    colors=askcolor(title="choose color")
    colors=colors[1] # to get hex value from the tuple
    try:
        answ=messagebox.askquestion("Mode","Press yes for text and no for meaning")
        if answ =='yes':
            s=20
            my_label2=Label(canvas,text=content1,fg=colors,font=('Gotham Medium', s,"bold"))
            my_label2.place(x=10,y=40)

            inc_text=Button(canvas,text="I",command=inc)
            inc_text.place(x=30,y=10)

            dec_text=Button(canvas,text="D",command=dec)
            dec_text.place(x=50,y=10)
             
            my_label2.bind("<Button-1>",drag_start)
            my_label2.bind('<B1-Motion>',drag_motion)

            inc_text.bind("<Button-1>",drag_start)
            inc_text.bind('<B1-Motion>',drag_motion)

            dec_text.bind("<Button-1>",drag_start)
            dec_text.bind('<B1-Motion>',drag_motion)
        else:
            my_label2=Label(canvas,text=content2,fg=colors)
            my_label2.place(x=10,y=20)
         
            inc_text=Button(canvas,text="I",command=inc)
            inc_text.place(x=30,y=10)

            dec_text=Button(canvas,text="D",command=dec)
            dec_text.place(x=50,y=10)
             
            my_label2.bind("<Button-1>",drag_start)
            my_label2.bind('<B1-Motion>',drag_motion)

            inc_text.bind("<Button-1>",drag_start)
            inc_text.bind('<B1-Motion>',drag_motion)

            dec_text.bind("<Button-1>",drag_start)
            dec_text.bind('<B1-Motion>',drag_motion)

    except TypeError:
        pass

# Function to draw line using mouse coordinate position
def draw_line(event):
    global tk_im
    global img
    global canvas
    global color
    if str(event.type) == "ButtonPress":
       canvas.old_coords = event.x, event.y
    elif str(event.type) == "ButtonRelease":
        first_x, first_y = canvas.old_coords
        second_x = event.x 
        second_y = event.y
        img = basic_functions.draw_line(img, first_x, first_y, second_x, second_y, color)
    tk_im = ImageTk.PhotoImage(img)
    display_image(img, canvas,tk_im)

# Function to get RGB value of color from image 
def pick_color(event):
    global tk_im
    global img 
    global canvas
    global color
    color = basic_functions.pick_color(img, event.x, event.y)
    messagebox.showinfo(title=app_title, message=str("Selected RGB color is: "+str(color)))
    canvas.unbind("<Button-1>")

# Function to resize image in the canvas by input new size coordiantes for image
def resize():
    global tk_im
    global img
    global canvas
    x = simpledialog.askinteger(title=app_title, prompt="Enter new X size:")
    if x != None:
        y = simpledialog.askinteger(title=app_title, prompt="Enter new Y size:")
        try:
            img = basic_functions.resize(img, x, y)
        except TypeError:
            pass
    tk_im = ImageTk.PhotoImage(img)
    display_image(img, canvas,tk_im)



def get_mouse_posn(event):
    global topy, topx
    topx, topy = event.x, event.y

def update_sel_rect(event):
    global rect_id
    global topy, topx, botx, boty
    botx, boty = event.x, event.y
    canvas.coords(rect_id, topx, topy, botx, boty)  # Update selection rect.\


def crop():
    global canvas
    global topx
    global topy
    global tk_im
    global botx
    global boty
    global rect_id
    global img
    
    cropped=img.crop((topx,topy,botx,boty))
    print("Cropped",cropped)
    img=cropped
    tk_im= ImageTk.PhotoImage(img)
    display_image(img, canvas,tk_im)


def select():
    global canvas
    global topx
    global topy
    global tk_im
    global botx
    global boty
    global rect_id
    rect_id = canvas.create_rectangle(topx, topy, topx, topy,
                                  dash=(2,2), fill='', outline='green')
    canvas.bind('<Button-1>', get_mouse_posn)
    canvas.bind('<B1-Motion>', update_sel_rect)

# Get the defination by scraping and return it to the comtent2 to display it on image


def get_definition2(content1):
    url = 'https://www.dictionary.com/browse/'
    headers = requests.utils.default_headers()
    global name
    search = content1
    headers.update({
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        })
    print("->",search)
    try:
        req = requests.get(url+search, headers)
        soup = BeautifulSoup(req.content, 'html.parser')

        mydivs = soup.findAll("div", {"value": "1"})[0]

        for tags in mydivs:
            meaning = tags.text
        
        return meaning
    except:
        messagebox.showinfo("Definition", "Word not found")
      
# Get the defination by scraping and display it in messagebox
def get_definition():
    s= simpledialog.askstring(title=app_title, prompt="Enter word to search:")
    url = 'https://www.dictionary.com/browse/'
    headers = requests.utils.default_headers()
    global name
    search = s
    headers.update({
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        })
    print("->",search)
    try:
        req = requests.get(url+search, headers)
        soup = BeautifulSoup(req.content, 'html.parser')

        mydivs = soup.findAll("div", {"value": "1"})[0]

        for tags in mydivs:
            meaning = tags.text
        
        messagebox.showinfo("Definition", meaning)
    except:
        messagebox.showinfo("Definition", "Word not found")

# Function to assign the label coordinates with event coordinates
def drag_start(event):
    widget = event.widget
    widget.startX = event.x
    widget.startY = event.y

# Function to move the label according to canvas screen coordinates 
def drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() - widget.startX + event.x
    y = widget.winfo_y() - widget.startY + event.y
    widget.place(x=x,y=y)



def grow():
    global img2
    global my_label
    global xi
    global yi
    global wi 
    global hi 
    i=0
    while i<1:
        resized_img = img2.resize((xi, yi),resample=Image.NEAREST)
        tk_im=ImageTk.PhotoImage(resized_img)
        my_label.configure(width=wi,height=hi,image=tk_im)
        my_label.image=tk_im
        xi+=1
        yi+=1
        i+=1 
        wi+=1
        hi+=1
   

def shrink():
    global my_label
    global img2
    global xi
    global yi
    global wi 
    global hi 
    i=0
    while i<1:
        resized_img = img2.resize((xi, yi),resample=Image.NEAREST)
        tk_im=ImageTk.PhotoImage(resized_img)
        my_label.configure(width=wi,height=hi,image=tk_im)
        my_label.image=tk_im
        xi-=1
        yi-=1
        i+=1 
        wi-=1
        hi-=1


def save():
   
    b6= pyautogui.locateOnScreen('icon.png', confidence=0.9,region=(0,0, 500, 500))
    b7 = pyautogui.center(b6)
    x,y=b7
    myScreenshot = pyautogui.screenshot(region=(x-16,y+22, 500, 500))
    file_path = "save.jpg"
    myScreenshot.save(file_path)
    print("done")
    
def view():
    global canvas
    global view_img
    global tk_im_view
    global img
    global tk_im
    view_img = Image.open ("save.jpg") 
    tk_im_view= ImageTk.PhotoImage(view_img)
    img=view_img
    tk_im=tk_im_view
    display_image(view_img, canvas,tk_im_view)
    print("view-done")



# Function to merge 2 or more images by either scrapping or by choosing images from the system
def merge_image():
    global tk_im
    global img
    global canvas
    global img2
    global my_label
    global xi
    global yi
    global wi
    global hi
    ans2=messagebox.askquestion("Choose Mode","Do you want to scrape image ")
    if ans2 == 'yes':
        content5 = simpledialog.askstring(title=app_title, prompt="Enter text for second image: ")
        data2=content5   
        img2=get_image2(data2) # get the second image in PIL format
    else:
        img2=getimg() # get image form system in both PIL format
     
    try:
        img2 = Image.open (filepath2)
        xi=img2.size[0]
        yi=img2.size[1]
        xi = simpledialog.askinteger(title=f'current xsize {xi}', prompt="Enter second image X size:")
        yi = simpledialog.askinteger(title=f'current ysize {yi}', prompt="Enter second image Y size:")
        wi=xi
        hi=yi
        img2 = basic_functions.resize(img2, xi, yi)
        img_2=ImageTk.PhotoImage(img2) # HERE img2 becomes second image in tkinter format 
        my_label=Label(canvas,image=img_2)  # Place label image on the canvas
        my_label.image=img_2
        my_label.pack(expand=True)

        grow_button=Button(canvas,text="grow",command=grow)
        grow_button.pack()

        shrink_button=Button(canvas,text="shrink",command=shrink)
        shrink_button.pack()
        
        my_label.bind("<Button-1>",drag_start)
        my_label.bind('<B1-Motion>',drag_motion)

        grow_button.bind("<Button-1>",drag_start)
        grow_button.bind('<B1-Motion>',drag_motion)

        shrink_button.bind("<Button-1>",drag_start)
        shrink_button.bind('<B1-Motion>',drag_motion)

    except AttributeError:
        pass


# Main function to choose image either by scraping or get from the system
def choose():
    global tk_im
    global img
    global canvas
    global image_window 

    ans5=messagebox.askquestion("Choose Mode","Do you want to scrape image ")
    if ans5 == 'yes':
        content = simpledialog.askstring(title=app_title, prompt="Enter text: ")
        data=content
        img,tk_im = get_image(data)
        
        image_window = Toplevel(root) # Create a new tkinter window using Toplevel widget
        m="Scrapped Image"
        image_window.title(m)
        image_window.geometry(str(img.size[0])+"x"+str(img.size[1])+"+10+100") # geometry is completely based on image
        image_window.resizable(False, False)
        canvas = Canvas(master=image_window) # Create a canvas on the new tkinter window
        canvas.pack(side=LEFT)
        display_image(img, canvas,tk_im)


        button_back = Button(canvas, text='<--', state=DISABLED)
        button_forward = Button(canvas, text='-->', command=lambda:forward(2))

        button_back.place(rely=1,relx=0,anchor=SW)
        button_forward.place(rely=1,relx=1,anchor=SE)

    else:
        img,tk_im = getimg()
        image_window = Toplevel(root)
        m="Choosen Image"
        image_window.title(m)
        image_window.geometry(str(img.size[0])+"x"+str(img.size[1])+"+10+100")
        image_window.resizable(False, False)
        canvas = Canvas(master=image_window)
        canvas.pack(side=LEFT)
        display_image(img, canvas,tk_im)

    image_window.mainloop()


root = tk.Tk() # Create main tkinter window
root.title("Image Scrapper")
root.geometry('1200x700+550+100')
root.resizable(False,False)

background_image = tk.PhotoImage(file='./background.png') # To open and get image in Tkinter format
background_label = tk.Label(root, image=background_image) # To create label in tkinter form and assign png image
background_label.place(relwidth=1, relheight=1) # to place the image on the whole window


l_title=tk.Message(text="Image Scrapper & Editor",relief="raised",width=1500,padx=600,pady=5,fg="yellow",bg="blue",justify="center",anchor="center")
l_title.config(font=("TIMES New Roman","35","bold"))
l_title.pack(side="top")

canvas2=Canvas(width=320,height=280) # Another canvas on main window
canvas2.place(x=50,y=200)

photo=PhotoImage(file='./python.png')
canvas2.create_image(0,0,image=photo,anchor=NW)

button1 = tk.Button(root, command=choose, borderwidth=4,text="Choose image",font=('Gotham Medium', 14,"bold"),bg="blue",fg="yellow",padx=8,pady=8)
button1.place(x=440,y=150,width=180)

button2 = tk.Button(root, command=resize,borderwidth=4, text="Resize",font=('Gotham Medium', 14,"bold"),bg="blue",fg="yellow",padx=8,pady=8)
button2.place(x=640,y=150,width=180)

button3 = tk.Button(root, command=merge_image,borderwidth=4, text="Merge",font=('Gotham Medium', 14,"bold"),bg="blue",fg="yellow",padx=8,pady=8)
button3.place(x=440,y=250,width=180)

button4 = tk.Button(root, command= save, borderwidth=4,text="Save",font=('Gotham Medium', 14,"bold"),bg="blue",fg="yellow",padx=8,pady=8)
button4.place(x=640,y=250,width=180)

button5 = tk.Button(root, command=draw_mode,borderwidth=4, text="Draw",font=('Gotham Medium', 14,"bold"),bg="blue",fg="yellow",padx=8,pady=8)
button5.place(x=440,y=350,width=180)

button6 = tk.Button(root, command=add_text,borderwidth=4, text="Text",font=('Gotham Medium', 14,"bold"),bg="blue",fg="yellow",padx=8,pady=8)
button6.place(x=640,y=350,width=180)

button7 = tk.Button(root, command=color_picker,borderwidth=4, text="Color picker",font=('Gotham Medium', 14,"bold"),bg="blue",fg="yellow",padx=8,pady=8)
button7.place(x=440,y=450,width=180)

button8 = tk.Button(root, command=get_definition, borderwidth=4,text="Search Word",font=('Gotham Medium', 14,"bold"),bg="blue",fg="yellow",padx=8,pady=8)
button8.place(x=640,y=450,width=180)

button9 = tk.Button(root, command=draw_rect,borderwidth=4, text="Rectangle",font=('Gotham Medium', 14,"bold"),bg="blue",fg="yellow",padx=8,pady=8)
button9.place(x=440,y=550,width=180)

button10 = tk.Button(root, command=draw_oval,borderwidth=4, text="Circle",font=('Gotham Medium', 14,"bold"),bg="blue",fg="yellow",padx=8,pady=8)
button10.place(x=640,y=550,width=180)

button11 = tk.Button(root, command=draw_triangle,borderwidth=4, text="Triangle",font=('Gotham Medium', 14,"bold"),bg="blue",fg="yellow",padx=8,pady=8)
button11.place(x=840,y=150,width=180)

button12 = tk.Button(root, command=crop,borderwidth=4, text="Crop",font=('Gotham Medium', 14,"bold"),bg="blue",fg="yellow",padx=8,pady=8)
button12.place(x=840,y=250,width=180)

button13 = tk.Button(root, command=select,borderwidth=4, text="Select",font=('Gotham Medium', 14,"bold"),bg="blue",fg="yellow",padx=8,pady=8)
button13.place(x=840,y=350,width=180)

button14 = tk.Button(root, command=view,borderwidth=4, text="Saved Image",font=('Gotham Medium', 14,"bold"),bg="blue",fg="yellow",padx=8,pady=8)
button14.place(x=840,y=450,width=180)


ourMessage ='By Akash Jain'
messageVar = tk.Message(root, text = ourMessage) 
messageVar.config(bg='lightblue',font=('Gotham Medium', 18),width=200,padx=50)
messageVar.place(x=70,y=210)

root.mainloop() # End of the tkinter program  

