from customtkinter import *
from tkinter import messagebox, filedialog
import requests
import os

pinstaller = CTk()

pinstaller.geometry("600x450")
pinstaller.configure(fg_color="#151515")
pinstaller.title("Chess1990 Installer")
pinstaller.iconbitmap("wN.ico")
pinstaller.resizable(False, False)

WelcomeLabel = None
DescLabel = None
FolderLabel = None
nextButton = None
FolderLabel = None
browseButton = None
FolderEntry = None
url = "https://github.com/MysteryCattics/Chess1190/releases/download/Legacy/Chess1990.exe"
folder_selected = None

def download_github_release_file(url, folder_selected):
    try:
        fileName = os.path.join(folder_selected, "Chess1990.exe")


        os.makedirs(folder_selected, exist_ok=True)

        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(fileName, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)

        return 1
    except requests.exceptions.RequestException:
        return 0


def browse_folder(FolderEntry):
            global folder_selected
            folder_selected = filedialog.askdirectory()
            FolderEntry.delete(0, 'end')
            FolderEntry.insert(0, folder_selected)

def next(step):
    global WelcomeLabel, DescLabel, FolderLabel, nextButton, browseButton, FolderEntry, url, folder_selected
    if step == 1:
        WelcomeLabel = CTkLabel(pinstaller, text="Welcome to Chess1990 installer!", font=("Segoe UI Black",  24))
        WelcomeLabel.place(x=10, y=0)

        DescLabel = CTkLabel(pinstaller, text="This game is the best game for \noffline chess! Play it When you want anywhere you want!", justify="left", anchor="w", font=("Segoe UI",  16))
        DescLabel.place(x=10, y=50)
        
        nextButton = CTkButton(pinstaller, text="Next >", width=100, height=40, command=lambda: next(2))
        nextButton.place(x=480, y=390)
    elif step == 2:
        nextButton.configure(command=lambda: next(3))
        WelcomeLabel.configure(text="Choose installation folder")
        DescLabel.place_forget()


        FolderLabel = CTkLabel(pinstaller, text="Select the folder where Chess1990 will be installed:", font=("Segoe UI",  16))
        FolderLabel.place(x=10, y=50)
        
        FolderEntry = CTkEntry(pinstaller, width=450, fg_color="#2A2A2A", text_color="#FFFFFF", font=("Segoe UI",  14))
        FolderEntry.place(x=10, y=200)
        folder_selected = os.path.expanduser("~\\Downloads\\Chess1990")
        FolderEntry.insert(0, folder_selected)
        
        browseButton = CTkButton(pinstaller, text="Browse", width=80, height=30, command=lambda: browse_folder(FolderEntry))        
        browseButton.place(x=480, y=200)
        
        nextButton.configure(text="Install")
    elif step == 3:
        FolderEntry.configure(state="disabled")
        nextButton.configure(state="disabled")

        WelcomeLabel.configure(text="Ready to install")
        FolderLabel.place_forget()
        FolderEntry.place_forget()
        browseButton.place_forget()
        nextButton.configure(text="Finish")

        WelcomeLabel = CTkLabel(pinstaller, text="Chess1990 installed successfully!", font=("Segoe UI Black",  24))
        WelcomeLabel.place(x=10, y=0)

        print("starting download...")
        status = download_github_release_file(url, os.path.join(folder_selected))
        
        nextButton.configure(command=lambda: pinstaller.destroy(), state="normal")

        if status == 0:
            messagebox.showerror("Error", "An error occurred during the installation. Please try again.")
            
next(1)



pinstaller.mainloop()