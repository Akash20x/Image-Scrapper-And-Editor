from tkinter import* # python library for GUI
from tkinter.colorchooser import* # get color window to choose color
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageChops,ImageTk # Get pillow library image functions
from tkinter import Tk, Label, Button, Canvas, Toplevel, simpledialog, messagebox #import main modules
from tkinter.filedialog import askopenfilename # To get image from the system
import basic_functions # Get some defined functions from basic_functions.py
from export import export # Get export function from export.py
import tkinter as tk 
import os # Library for interaction with operating system
import requests # To send HTTP request to specified URL and get response content
from bs4 import BeautifulSoup # To extract data from HTML and XML Files 
import time
from selenium import webdriver
import cv2
import glob


# Google image search url
google_image = \
'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

# To get control as an agent over the response of the HTTP request 
usr_agent = {
    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

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


def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 1):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)

        # build the google query

    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q=dog&oq=dog&gs_l=img
    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)


        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

        for img in thumbnail_results[results_start:number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch:
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
        results_start = len(thumbnail_results)

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
        res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.2)

    counter = 0
    for elem in res:
        persist_image(target_folder, elem, counter)
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
            if(img.size[1]>600):
                img = img.resize((img.size[0],600),resample=Image.NEAREST)
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
    return img2

# Function to get image from the system and return it in PIL and tkinter format
def getimg():
    global filepath
    global img2
    global filepath2
    Tk().withdraw()
    filepath = askopenfilename()
    img2 = Image.open(filepath)
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
    canvas.bind("<ButtonRelease-3>", draw_line)
    canvas.bind("<ButtonPress-3>", draw_line)

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
    img = basic_functions.draw_point(img, event.x, event.y, color)
    tk_im = ImageTk.PhotoImage(img)
    display_image(img, canvas,tk_im)

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
        image_window.geometry(str(img.size[0])+"x"+str(img.size[1])) # geometry is completely based on image
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
        image_window.geometry(str(img.size[0])+"x"+str(img.size[1]))
        image_window.resizable(False, False)
        canvas = Canvas(master=image_window)
        canvas.pack(side=LEFT)
        display_image(img, canvas,tk_im)

    image_window.mainloop()


root = tk.Tk() # Create main tkinter window
root.title("Image Scrapper")
root.geometry('1000x600+500+100')
root.resizable(False,False)

background_image = tk.PhotoImage(file='./background.png') # To open and get image in Tkinter format
background_label = tk.Label(root, image=background_image) # To create label in tkinter form and assign png image
background_label.place(relwidth=1, relheight=1) # to place the image on the whole window


l_title=tk.Message(text="Image Scrapper & Editor",relief="raised",width=1500,padx=600,pady=5,fg="yellow",bg="blue",justify="center",anchor="center")
l_title.config(font=("TIMES New Roman","35","bold"))
l_title.pack(side="top")

canvas2=Canvas(width=320,height=280) # Another canvas on main window
canvas2.place(x=50,y=150)

photo=PhotoImage(file='./python.png')
canvas2.create_image(0,0,image=photo,anchor=NW)

button1 = tk.Button(root, command=choose, borderwidth=4,text="Choose image",font=('Gotham Medium', 12,"bold"),bg="blue",fg="yellow",padx=5,pady=5)
button1.place(x=440,y=100,width=150)

button2 = tk.Button(root, command=resize,borderwidth=4, text="Resize",font=('Gotham Medium', 12,"bold"),bg="blue",fg="yellow",padx=5,pady=5)
button2.place(x=610,y=100,width=150)

button3 = tk.Button(root, command=merge_image,borderwidth=4, text="Merge",font=('Gotham Medium', 12,"bold"),bg="blue",fg="yellow",padx=5,pady=5)
button3.place(x=440,y=200,width=150)

button4 = tk.Button(root, command= lambda: export(img), borderwidth=4,text="Save",font=('Gotham Medium', 12,"bold"),bg="blue",fg="yellow",padx=5,pady=5)
button4.place(x=610,y=200,width=150)

button5 = tk.Button(root, command=draw_mode,borderwidth=4, text="Draw",font=('Gotham Medium', 12,"bold"),bg="blue",fg="yellow",padx=5,pady=5)
button5.place(x=440,y=300,width=150)

button6 = tk.Button(root, command=add_text,borderwidth=4, text="Text",font=('Gotham Medium', 12,"bold"),bg="blue",fg="yellow",padx=5,pady=5)
button6.place(x=610,y=300,width=150)

button7 = tk.Button(root, command=color_picker,borderwidth=4, text="Color picker",font=('Gotham Medium', 12,"bold"),bg="blue",fg="yellow",padx=5,pady=5)
button7.place(x=440,y=400,width=150)

button8 = tk.Button(root, command=get_definition, borderwidth=4,text="Search Word",font=('Gotham Medium', 12,"bold"),bg="blue",fg="yellow",padx=5,pady=5)
button8.place(x=610,y=400,width=150)

ourMessage ='By Akash Jain'
messageVar = tk.Message(root, text = ourMessage) 
messageVar.config(bg='lightblue',font=('Gotham Medium', 18),width=200,padx=50)
messageVar.place(x=100,y=160)

root.mainloop() # End of the tkinter program  

