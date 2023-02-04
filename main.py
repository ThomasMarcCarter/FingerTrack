import socket
import tkinter
import customtkinter
import feedparser
from functools import partial
import webbrowser
from tkHyperlinkManager import *

import folium
from folium.plugins import MarkerCluster
import pandas as pd


def connect():
    # Define the server address and port
    host = '192.168.0.157'
    port = 12345
    
    # Create a socket object
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    try:
        client_socket.connect((host, port))
        print("Connected to {}:{}".format(host, port))
        connect_button.configure(state='disabled')
        send_button.configure(state='normal')
        disconnect_button.configure(state='normal')
        label_status.configure(text_color="green")
        label_status.configure(text="Connected")
    except:
        print("Failed to connect to {}:{}".format(host, port))
        label_status.configure(text_color="red")
        label_status.configure(text="Failed to Connect...")

def send_numbers():
    num1 = x_entry.get()
    num2 = y_entry.get()
    print(num1, num2)

    
    numbers = "{} {}".format(num1, num2)
    
    client_socket.sendall(numbers.encode())
    
    response = client_socket.recv(1024)
    
    decresponse = response.decode()

    value_response.configure(text_color="red")
    value_response.configure(text=decresponse)

def disconnect():
    client_socket.close()
    connect_button.configure(state='normal')
    send_button.configure(state='disabled')
    disconnect_button.configure(state='disabled')
    label_status.configure(text_color="red")
    label_status.configure(text="Disconnected")
    print("Disconnected")

#RENDER GUI
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()
app.geometry("1200x600")

# configure grid layout (4x4)
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure((2, 3), weight=0)
app.grid_rowconfigure((0, 1, 2), weight=1)

app.sidebar_frame = customtkinter.CTkFrame(app, width=140, corner_radius=0)
app.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
app.sidebar_frame.grid_rowconfigure(4, weight=1)
app.logo_label = customtkinter.CTkLabel(app.sidebar_frame, text="FingerTracker ALPHA 1.0", font=customtkinter.CTkFont(size=20, weight="bold"))
app.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

connect_button = customtkinter.CTkButton(app.sidebar_frame, text="Connect", command=connect)
connect_button.grid(row=9, column=0, padx=20, pady=2)

send_button = customtkinter.CTkButton(app.sidebar_frame, text="Send", command=send_numbers, state='disabled')
send_button.grid(row=3, column=0, padx=20, pady=2)

disconnect_button = customtkinter.CTkButton(app.sidebar_frame, text="Disconnect", command=disconnect, state='disabled')
disconnect_button.grid(row=10, column=0, padx=20, pady=2)

label_status = customtkinter.CTkLabel(app.sidebar_frame, text="Connect to Server...", text_color="grey")
label_status.grid(row=8, column=0, padx=20)

x_status = customtkinter.CTkLabel(app, text="x:", text_color="white")
x_status.place(relx=0.3, rely=0.1, anchor=tkinter.CENTER)

x_entry = customtkinter.CTkEntry(app, placeholder_text="Enter a number")
x_entry.place(relx=0.4, rely=0.1, anchor=tkinter.CENTER)

y_status = customtkinter.CTkLabel(app, text="y:", text_color="white")
y_status.place(relx=0.3, rely=0.2, anchor=tkinter.CENTER)

y_entry = customtkinter.CTkEntry(app, placeholder_text="Enter a number")
y_entry.place(relx=0.4, rely=0.2, anchor=tkinter.CENTER)

label_response = customtkinter.CTkLabel(app, text="Response:", text_color="white")
label_response.place(relx=0.3, rely=0.3, anchor=tkinter.CENTER)

value_response = customtkinter.CTkLabel(app, text="", text_color="white")
value_response.place(relx=0.4, rely=0.3, anchor=tkinter.CENTER)

feed = feedparser.parse("https://github.com/ThomasMarcCarter/FingerTrack/commits/main.atom")

print('Number of RSS posts :', len(feed.entries))
entry = feed.entries[0]
print(entry.keys())
print(entry.updated)
print(entry.title)
print(entry.link)

app.textbox = customtkinter.CTkTextbox(app, width=200, height=20)
app.textbox.grid(row=0, column=1, padx=(0, 2), pady=(0, 2), sticky="nsew")
for i in range(0, len(feed.entries)):
    app.textbox.insert("0.0","\n" + feed.entries[i].title +"\n" + feed.entries[i].link + "\n" + feed.entries[i].updated + "\n" + "----------------------------------------------------" )
app.textbox.configure(state="disabled")


# Start the GUI event loop
app.mainloop()