from customtkinter import *
from PIL import ImageTk, Image
from pytubefix import YouTube
from tkinter import messagebox
import threading

app = CTk()
app.geometry("500x700")
app.title("Universal video downloader")



image1 = CTkImage(light_image=Image.open("photos/youtube-logo-hd-8.png"), size=(200, 200))

label = CTkLabel(app, text=None, image=image1)
label.pack()
text = CTkLabel(app, text="DOWNLOAD VIDEO", font=("Arial", 32))
text.pack()

url_label = CTkLabel(app, text="Enter video URL", font=("Arial", 20))
url_label.pack(pady=20)

urlEntry = CTkEntry(app, width=400)
urlEntry.pack()
urlEntry.focus()

resolution_label = CTkLabel(app, text='Resolution:')
resolution_label.pack()

combobox = CTkComboBox(app, width=200)
combobox.pack()

resSearch = CTkButton(app, text="Search resolutions")
resSearch.pack(pady=20)

progressbar = CTkProgressBar(app, orientation="horizontal", mode="determinate")
#progressbar.pack(pady=40)
progressbar.set(0)

download = CTkButton(app, text="Download")
download.pack(pady=20)


def SearchRes():
    video_link = urlEntry.get().strip()
    if video_link == "":
        messagebox.showerror(title="Universal video downloader", message="Enter the link")
    else:
        try:
            video = YouTube(video_link)
            resolutions = []
            for stream in video.streams.filter(file_extension='mp4', progressive=True):
                if stream.resolution:
                    resolutions.append(stream.resolution)
            combobox.configure(values=resolutions)
            messagebox.showinfo(title='Search Complete', message='Check the Combobox for the available video resolutions')
        except Exception as e:
            messagebox.showerror(title='Error', message=f'An error occurred: {e}')


def searchThread():
    t1 = threading.Thread(target=SearchRes, daemon=True)
    t1.start()

resSearch.configure(command=searchThread)


def download_video():
    try:
        video_link = urlEntry.get().strip()
        resolution = combobox.get()
        if resolution == '' or video_link == '':
            messagebox.showerror(title='Error', message='Please enter both the video URL and resolution!')
            return
        if resolution == 'None':
            messagebox.showerror(title='Error', message='Invalid resolution selected!')
            return

        def on_progress(stream, chunk, bytes_remaining):
            total_size = stream.filesize
            bytes_downloaded = total_size - bytes_remaining
            progress = bytes_downloaded / total_size   # значення від 0.0 до 1.0
            progressbar.set(progress)
            app.update_idletasks()

        try:
            video = YouTube(video_link, on_progress_callback=on_progress)
            video.streams.filter(res=resolution).first().download()
            messagebox.showinfo(title='Download Complete', message='Video has been downloaded successfully.')
            progressbar.set(0)
        except Exception as e:
            messagebox.showerror(title='Download Error', message=f'Failed to download video: {e}')
            progressbar.set(0)
    except Exception as e:
        messagebox.showerror(title='Download Error', message=f'An error occurred: {e}')
        progressbar.set(0)


def downloadThread():
    t2 = threading.Thread(target=download_video, daemon=True)
    t2.start()

download.configure(command=downloadThread)

app.mainloop()
