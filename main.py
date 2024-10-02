import re
import tkinter as tk
from tkinter import Menu, filedialog, Label, Button, Entry

def confirm_sender(chat_log):
        sender_name = sendervalue.get()
        display_chat(chat_log, sender_name)

# Function to handle file upload
def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        global chat_log
        chat_log = extract_messages(file_path)
        status_label.config(text="File uploaded successfully!", fg='green')

    return chat_log


# Function to Extract Messages
def extract_messages(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        chat_data = f.readlines()

    chat_log = []
    chat_pattern = r"(\d{2}/\d{2}/\d{2,4}), (\d{1,2}:\d{2}\s?[ap]m?) - (.*?): (.*)"
    message_buffer = None

    for line in chat_data:
        MATCH = re.match(chat_pattern, line)
        if MATCH:
            # If a previous message is being accumulated, store it
            if message_buffer:
                chat_log.append(message_buffer)

            # Start a new message buffer
            date, time, sender, message = MATCH.groups()
            message_buffer = {
                'DATE': date,
                'TIME': time,
                'SENDER': sender,
                'MESSAGE': message
            }
        else:
            # If this line doesn't match the pattern, it's a continuation of the previous message
            if message_buffer:
                message_buffer['MESSAGE'] += '\n' + line.strip()

    if message_buffer:
        chat_log.append(message_buffer)

    return chat_log

# Function to display chat in the GUI with proper scrolling
def display_chat(chat_log, sender_name):

    # Inital values
    global icon, name_bar_color, name_bar_Textcolor, background_color, receivers_messageBox_color, senders_messageBox_color, text_color
    icon = 'light_icon.png' 
    name_bar_color = 'white'
    name_bar_Textcolor = 'black'
    background_color = '#FCE3C3'                 
    receivers_messageBox_color = 'white'
    senders_messageBox_color = 'lightgreen'
    text_color = 'black'


    # Function to apply theme
    def theme(icon, name_bar_color, name_bar_Textcolor, background_color, receivers_messageBox_color, senders_messageBox_color, text_color):
        # Clear previous widgets before re-applying
        for widget in root.winfo_children():
            widget.destroy()

        # Frame for displaying sender & receiver names
        name_bar = tk.Frame(root, bg=name_bar_color, height=30)
        name_bar.pack_propagate(0)
        name_bar.pack(side='top', fill='x')

        
        # Icons
        global photo
        photo = tk.PhotoImage(file=icon)  

        # Receivers side icon
        icon_label = tk.Label(name_bar, borderwidth=0, image=photo)
        icon_label.pack(side='left')

        # Senders side icon
        icon_label = tk.Label(name_bar, borderwidth=0, image=photo )
        icon_label.pack(side='right')


        # sender & receiver names
        Senders = set()
        Receivers = set()
        for chat in chat_log:  
            sender = chat['SENDER']
            if sender == sender_name:
                Senders.add(sender)
            else:
                Receivers.add(sender)

        # Default Names
        receiver_display_name = ', '.join(Receivers) if Receivers else "Unknown Receiver"
        sender_display_name = sender_name if sender_name else "Unknown Sender"

        # Display sender & receiver names
        sender_label = tk.Label(name_bar, text=sender_display_name, font='comicsansns 13', fg=name_bar_Textcolor, bg=name_bar_color)
        sender_label.pack(side='right', padx=10)
        receiver_label = tk.Label(name_bar, text=receiver_display_name, font='comicsansns 13', fg=name_bar_Textcolor, bg=name_bar_color)
        receiver_label.pack(side='left', padx=10)


        # canvas_widget & scrollable frame for the chat
        canvas_widget = tk.Canvas(root, width=350, height=600, bg=background_color)
        canvas_widget.pack(side="left", fill="both", expand=True)

        scrollable_frame = tk.Frame(canvas_widget, bg=background_color)
        scrollable_frame.bind("<Configure>", lambda e: canvas_widget.configure(scrollregion=canvas_widget.bbox("all")))
        canvas_widget.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Display chat messages
        for chat in chat_log:
            message = chat['MESSAGE']
            if chat['SENDER'] != sender_name:
                message_label = tk.Label(scrollable_frame, text=f"{message}", anchor='w', justify='left', wraplength=250,
                                         bg=receivers_messageBox_color, fg=text_color, padx=10, pady=5)
                message_label.pack(anchor='w', padx=10, pady=2)
            else:
                message_label = tk.Label(scrollable_frame, text=f"{message}", anchor='e', justify='left', wraplength=250,
                                         bg=senders_messageBox_color, fg=text_color, padx=10, pady=5)
                message_label.pack(anchor='e', padx=70, pady=4)

        def _on_mouse_wheel(event):
            canvas_widget.yview_scroll(-1 * int((event.delta / 120)), "units")

        root.bind_all("<MouseWheel>", _on_mouse_wheel)

        # Recreate the main menu
        mainmenu()

    # Main Menu function
    def mainmenu():
        MenuBar = Menu(root)
        theme_menu = Menu(MenuBar, tearoff=0)
        theme_menu.add_radiobutton(label='Dark', command=dark)
        theme_menu.add_radiobutton(label='Light', command=light)
        MenuBar.add_cascade(label='Change Theme', menu=theme_menu)
        root.config(menu=MenuBar)

    # Dark theme function
    def dark():
        global icon, name_bar_color, name_bar_Textcolor, background_color, receivers_messageBox_color, senders_messageBox_color, text_color
        icon = 'dark_icon.png'
        name_bar_color = '#282828'
        name_bar_Textcolor = 'white'
        background_color = '#303030'
        receivers_messageBox_color = '#404040'
        senders_messageBox_color = 'darkgreen'
        text_color = 'white'
        theme(icon, name_bar_color, name_bar_Textcolor, background_color, receivers_messageBox_color, senders_messageBox_color, text_color)

    # Light theme function
    def light():
        global icon, name_bar_color, name_bar_Textcolor, background_color, receivers_messageBox_color, senders_messageBox_color, text_color
        icon = 'light_icon.png' 
        name_bar_color = 'white'
        name_bar_Textcolor = 'black'
        background_color = '#FAD6A5'
        receivers_messageBox_color = 'white'
        senders_messageBox_color = 'lightgreen'
        text_color = 'black'
        theme(icon, name_bar_color, name_bar_Textcolor, background_color, receivers_messageBox_color, senders_messageBox_color, text_color)

    # Initially apply light theme
    theme(icon, name_bar_color, name_bar_Textcolor, background_color, receivers_messageBox_color, senders_messageBox_color, text_color)

    # root.mainloop()


# Main part of the program
if __name__ == "__main__": 
    root = tk.Tk()
    root.configure(bg='#00A550')
    root.geometry("350x600")
    root.minsize(350, 600)
    root.maxsize(350, 600)
    root.title("Developer : Akarsh Prakash")
    root.wm_iconbitmap('logo_icon.ico')

    label_1 = Label(root, text="Upload the WhatsApp exported file \n & \n Provide Sender's Name.", bg='#00A550', fg='white', font='comicsansns 15 bold')
    label_1.pack(padx=10, pady=(50, 20))

    label_2 = Label(root, text="Choose WhatsApp File", bg='#00A550', fg='white', font='comicsansns 15')
    label_2.pack(anchor='center', pady=(40, 10))

    # File upload button
    upload_button = Button(root, text="Upload", command=upload_file,padx=5, pady=5, bg='#008C4A', fg='white', font='comicsansns 14 bold')
    upload_button.pack(anchor='center', pady=(0, 30))

    label_3 = Label(root, text="Enter Sender's Name.", bg='#00A550', fg='white', font='comicsansns 15')
    label_3.pack(anchor='center', pady=(10, 10))

    # Input Sender's name
    sendervalue = tk.StringVar()
    senderentry = Entry(root, textvariable = sendervalue, font=('Helvetica', 16), width=20, justify='center')
    senderentry.pack(anchor='center', pady=(0, 30))

    # Uploaded File Status label
    status_label = Label(root, text="", bg='#00A550', fg='white', font='comicsansns 12')
    status_label.pack(pady=(10, 20))  

    confirm_button = Button(root, text="Confirm", command= lambda: confirm_sender(chat_log), padx=15, pady=6, bg='#008C4A', fg='white', font='comicsansns 14 bold') 
    confirm_button.pack(pady=(20, 0))

    # Hover effect functionality
    def on_enter(e):
        e.widget['bg'] = '#005B3D'  # Dark green on hover

    def on_leave(e):
        e.widget['bg'] = '#008C4A'  # Original green color

    upload_button.bind("<Enter>", on_enter)
    upload_button.bind("<Leave>", on_leave)
    confirm_button.bind("<Enter>", on_enter)
    confirm_button.bind("<Leave>", on_leave)

    root.mainloop()
