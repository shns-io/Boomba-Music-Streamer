import tkinter as tk
import pygame
from tkinter import filedialog
import tkinter.ttk as ttk
root = tk.Tk()

root.title("Boomba Music Streamer")
root.geometry("500x450")

# The title card
title_label = tk.Label(root, text="~♕𝓜𝔂 𝓑𝓸𝓸𝓶𝓫𝓪 𝓟𝓵𝓪𝔂𝓵𝓲𝓼𝓽 ♕~", font=("Forte", 40, "bold"), fg="#000000")
title_label.pack(pady=10)

pygame.mixer.init()

# Search bar 
search_var = tk.StringVar()

search_frame = tk.Frame(root)
search_frame.pack(pady=10)

tk.Label(
    search_frame,
    text="Search Artist/Genre:",
    font=("Forte", 12),
    fg="#628A63",
    bg="#e0e0e0"
).pack(side=tk.LEFT)

search_entry = tk.Entry(
    search_frame,
    textvariable=search_var,
    width=30,
    font=("Forte", 12),
    fg="#333333",
    bg="#A3199A",
    relief=tk.GROOVE,
    bd=2
)
search_entry.pack(side=tk.LEFT, padx=5)

#styling the search and show all button
search_btn_style = {

    "bg": "#537353",   
    "fg": "white",      
    "font": ("Forte", 12),
    "width": 10,          
    "height": 2,         
    "relief": tk.RAISED,  
    "bd": 3               
}
show_all_btn_style = {
    "bg": "#537353",   
    "fg": "white",      
    "font": ("Forte", 12),
    "width": 10,          
    "height": 2,         
    "relief": tk.RAISED,  
        "bd": 3  }

#define the search and show all function
def search():
    query = search_var.get().lower()
    songlist_box.delete(0, tk.END )
 
    for song in all_songs:
        if query in song.lower():
            songlist_box.insert(tk.END, song)

def show_all():
    songlist_box.delete(0, tk.END)
    for song in all_songs:
        songlist_box.insert(tk.END, song)

tk.Button(search_frame, text="Search", command=search,  **search_btn_style).pack(side=tk.LEFT)
tk.Button(search_frame, text="Show All", command=show_all , **show_all_btn_style).pack(side=tk.LEFT, padx=5)

# Store all songs added for searching
all_songs = []

#using file dialog do play songs
def add_song():
    song = filedialog.askopenfilename(initialdir="songs/", title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
    song = song.replace("C:/Users/smmba/OneDrive/Documents/Visual Studio Code/Boomba Music Player/Python/songs/", "")
    song = song.replace(".mp3", "")

    songlist_box.insert(tk.END, song)
    all_songs.append(song)  # Add to all_songs list


#define the add many songs function
def add_many_songs():   
    songs = filedialog.askopenfilenames(initialdir="songs/", title="Choose Many Songs", filetypes=(("mp3 Files", "*.mp3"), ))
    for song in songs:
        song = song.replace("C:/Users/smmba/OneDrive/Documents/Visual Studio Code/Boomba Music Player/Python/songs/", "")#preventing the long song path from being displayed
        song = song.replace(".mp3", "")#removing the mp3 part as well
        songlist_box.insert(tk.END, song)
        all_songs.append(song)  # Add to all_songs list

#song length
current_song_length = 0

#Defining the play function
def play():
    song = songlist_box.get(tk.ACTIVE)
    song_path = f"C:/Users/smmba/OneDrive/Documents/Visual Studio Code/Boomba Music Player/Python/songs/{song}.mp3"
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play(loops=0)
    global current_song_length
    try:            
        current_song_length = pygame.mixer.Sound(song_path).get_length()
    except Exception as e:
        current_song_length = 100
       
    music_slider.config(to=int(current_song_length))
    update_slider()  # Start updating the slider

#the songtime conversion function
def convert_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins}:{secs:02}"

#defining update slider function
def update_slider():
    if pygame.mixer.music.get_busy():
        pos = pygame.mixer.music.get_pos() / 1000
        music_slider.set(pos)
        slider_label.config(text=f"{convert_time(pos)} / {convert_time(current_song_length)}")
        root.after(500, update_slider)
    else:
        slider_label.config(text=f"0:00 / {convert_time(current_song_length)}")    

#Defining the stop function
def stop():
    pygame.mixer.music.stop()
    songlist_box.selection_clear(tk.ACTIVE)

#Defining the pause function(pauses and unpauses the song)
global paused
paused = False

def pause(is_paused):
    global paused
    paused = is_paused
    
    if paused:  #Unpausing
        #1
        pygame.mixer.music.unpause()
        paused = False
    else:        #Pausing
    #2  
        pygame.mixer.music.pause()
        paused = True
   
 #Defining the next song function
def next_song(): 
    #get the current song number
    next_one = songlist_box.curselection()

    next_one = next_one[0] + 1

    song = songlist_box.get(next_one) #whatever number the song is, get it from the playlist
    song = f"C:/Users/smmba/OneDrive/Documents/Visual Studio Code/Boomba Music Player/Python/songs/{song}.mp3" #the full song path
    #load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #moving the active bar in the playlist
    songlist_box.selection_clear(0, tk.END) #clears the bar when you click next song
    songlist_box.activate(next_one) #activates the bar for the next song, the underline only
    songlist_box.selection_set(next_one, last=None) #highlights it

#Defining the previous song function
def previous_song():
      #get the current song number
    next_one = songlist_box.curselection()

    next_one = next_one[0] -1

    song = songlist_box.get(next_one) #wtv number the song is, get it from the playlist
    song = f"C:/Users/smmba/OneDrive/Documents/Visual Studio Code/Boomba Music Player/Python/songs/{song}.mp3" #the song path
    #load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #moving the active bar in the playlist
    songlist_box.selection_clear(0, tk.END) #clears the bar when you click next song
    songlist_box.activate(next_one) #activates the bar for the next song, the underline only
    songlist_box.selection_set(next_one, last=None) #highlights it

#Defining the a delete song function
def delete_song():
    selected = songlist_box.curselection()
    if selected:
        song = songlist_box.get(selected)
        if song in all_songs:
            all_songs.remove(song)

    songlist_box.delete(tk.ACTIVE)#deleting the selected song
    pygame.mixer.music.stop()

#Defining the delete all songs function
def delete_all_songs():
    
    songlist_box.delete(0, tk.END)
    all_songs.clear()  # Clear the all_songs list if theyre deleted
    #stop the music if it was playing
    pygame.mixer.music.stop()

#Defining the slide function
def slide(x):
    pygame.mixer.music.set_pos(float(x))
    slider_label.config(text=f"{convert_time(float(x))} / {convert_time(current_song_length)}")


#Creating the playlist box
songlist_box = tk.Listbox(root, bg="black", fg="white", width=300, selectbackground="gray", selectforeground="black")
songlist_box.pack(pady=20)

contol_frame = tk.Frame(root)
contol_frame.pack()

#STYLING THE BUTTONs
button_style = {
    "bg": "#768676",   
    "fg": "white",      
    "font": ("Forte", 12),
    "width": 10,          
    "height": 2,         
    "relief": tk.RAISED,  
    "bd": 3               
}

#Making the buttons work with the functions and styling
back_btn = tk.Button(contol_frame, text="<< Replay", command=previous_song, **button_style)
pause_btn = tk.Button(contol_frame, text=" Pause", command=lambda: pause(paused), **button_style)
play_btn = tk.Button(contol_frame, text="Play", command=play, **button_style)
stop_btn = tk.Button(contol_frame, text="Stop", command=stop, **button_style)
forward_btn = tk.Button(contol_frame, text="Next >>", command=next_song, **button_style)



#button positioning
back_btn.grid(row=0, column=0, padx=10)	
pause_btn.grid(row=0, column=3, padx=10)
play_btn.grid(row=0, column=2, padx=10) 
stop_btn.grid(row=0, column=4, padx=10)
forward_btn.grid(row=0, column=1, padx=10)

#menubar
a_menu = tk.Menu(root, fg="#768676")
root.config(menu=a_menu)

add_song_menu = tk.Menu(a_menu)
a_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add A Song To The Playlist", command= add_song)
#adding several songs
add_song_menu.add_command(label="Add Many Songs To The Playlist", command= add_many_songs)
#delete a song
remove_song_menu = tk.Menu(a_menu)
a_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="🗑 Song ", command= delete_song)
remove_song_menu.add_command(label="🗑 All Songs", command= delete_all_songs)

#music slider
music_slider = ttk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, length=400, value=0, command=slide)
music_slider.pack(pady=40)

#slider label
slider_label = tk.Label(root, text="0") 
slider_label.pack(pady=20)

root.mainloop()



