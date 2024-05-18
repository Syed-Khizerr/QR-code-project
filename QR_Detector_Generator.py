import tkinter as tk
from ttkbootstrap import ttk
import qrcode
import os
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog
import base64
import re
from roboflow import 

def read_qr():
    print(file_variable.get())

def convert(file):
    # Define the regex patterns for text and image files
    text_file_pattern = re.compile(r'.*\.txt$', re.IGNORECASE)
    image_file_pattern = re.compile(r'.*\.png$', re.IGNORECASE)
   
    if text_file_pattern.match(file):
        return text_to_string(content1.get())
    elif image_file_pattern.match(file):
        return image_to_base64(content1.get())
    else:
        return file
    
def text_to_string(filename):
    try:
        # Open the file in read mode
        with open(filename, 'rb') as file:
            # Read the file contents and store in a string
            file_contents = file.read()
    except FileNotFoundError:
        messagebox.showerror('Error', 'File Not found')
    except IOError:
        messagebox.showerror('Error',"Error reading file.")
    return file_contents
    

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        base64_str = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_str

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
    if file_path:
        load_image(file_path)
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)


# Function to load the image and display it
def load_image(file_path):
    img = Image.open(file_path)
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk  # Keep a reference to avoid garbage collection


def generate_qr():
     # Ensure the save location directory exists
    if not os.path.exists(str(location_var1.get())):
        os.makedirs(str(location_var1.get()))
    
    
    # Full path for the QR code image
    qr_path = os.path.join(str(location_var1.get()), str(created_file.get())+".png")
    
    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    content  = convert(str(content1.get()))

    qr.add_data(content)
    qr.make(fit=True)
    
    img = qr.make_image(fill='black', back_color='white')
    
    # Save the image
    img.save(qr_path)
    messagebox.showinfo('Task Accomplished',f"QR code saved at {qr_path}")

window = tk.Tk()
# window.geometry('800x500')
window.title('Framework')

# Creating a notebook
notebook = ttk.Notebook(window)
notebook.pack()

tab1 = ttk.Frame(notebook,relief=tk.GROOVE)
label1 = ttk.Label(tab1, text = 'QR Code Generator', font = 'Calibri 28 bold')
label1.pack()
label2=ttk.Label(tab1, text = 'Enter the Image/Text file location or some text', font='Calibri 15 ')
content_var1 = tk.StringVar()
content1 = ttk.Entry(
    tab1,
    textvariable = content_var1,
    width=40
)

label3 = ttk.Label(tab1, text='Enter memory location', font='Calibri 15 ')
location_var1 = tk.StringVar()
location1 = ttk.Entry(
    tab1,
    textvariable = location_var1,
    width=40
    
)
label2.pack(pady=5)
content1.pack(pady=5)
label3.pack(pady=5)
location1.pack(pady=5)

label4 = ttk.Label(tab1, text='Enter a name for QR', font='Calibri 15')
label4.pack()
created_file = tk.StringVar(value="Enter File name")
file_name_creation = ttk.Entry(tab1, width = 40,textvariable=created_file)
file_name_creation.pack()

generate_button = ttk.Button(tab1,
                             text='Generate QR' , 
                             command= generate_qr
                             )
generate_button.pack(pady=5)




tab2 = ttk.Frame(notebook, relief=tk.GROOVE)
label2 = ttk.Label(tab2, text = 'QR Code Reader', font = 'Calibri 28 bold' )
label2.pack()
file_variable = tk.StringVar(value = 'Enter file path')

entry_frame = ttk.Frame(tab2)
file_entry = ttk.Entry(entry_frame, textvariable=file_variable , font = 'Calibri 15')
file_entry.pack(side = 'left')
select_button = ttk.Button(entry_frame, text='Select', command=open_image)
select_button.pack(side='left')
entry_frame.pack(pady=5)

image_label = ttk.Label(tab2)
image_label.pack()

file_entry.bind('<Return>', lambda event : load_image(file_variable.get()))

read_button = ttk.Button(tab2, text = 'Read', command = read_qr)
read_button.pack(pady =5)

notebook.add(tab1, text = 'Generate')
notebook.add(tab2, text = 'Read')


# run
window.mainloop()
