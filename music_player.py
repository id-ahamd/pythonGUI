from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import pygame
from pygame.locals import *
from mutagen.mp3 import MP3
import time
from tkinter import ttk

root=Tk()
root.title("MP3 Player")
root.geometry('400x450')
root.resizable(0,0)

# Gets the requested values of the height and widht.
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
# Gets both half the screen width/height and window width/height
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/3 - windowHeight/2) 
# Positions the window in the center of the page.
root.geometry("+{}+{}".format(positionRight, positionDown))
# initialize pygame
pygame.init()

global songs_path
songs_path=[]
global stopped
stopped=False

def add_songs2():
	global songs_path

	songs_to_add=filedialog.askopenfilenames(initialdir='/c:', title='Select songs to add', filetypes=(('mp3 files', '*.mp3'),('wav files', '*.wav'),))
	for song in songs_to_add:
		song_name=song.split('/')[-1].split('.')[0]
		songs_list.insert(END,song_name)
		#songs_path.append(str(song_name[:-2]).replace(',',''))
		songs_path.append(song)

def add_songs():
	add_songs2()
	#Activate first song bar
	songs_list.activate(0)
	# Activate selection
	songs_list.selection_set(0, last=None)
	root.update()
	status_bar.config(text="New songs added...")
	root.update()
	status_bar.after(3000, status_bar.config(text=""))

global auto_play
auto_play=False
def autoplay_songs():
	global auto_play
	auto_play=True
	play_song()

global del_opt
del_opt=False
def select_to_delete_songs():
	global del_opt, myLabel
	selected=reversed(songs_list.curselection())
	#print (songs_list.curselection())
	if len(songs_list.curselection()): 
		songs_list.config(selectmode=MULTIPLE)
		del_opt=True
		myLabel = Label(root, text="Select and click button Delete ")
		myLabel.pack()

def delete_songs(event):
	stop_song()
	global del_opt, songs_path
	if del_opt:
		#myLabel = Label(root, text="You clicked this button: " + event.keysym)
		#myLabel.pack()
		selected=reversed(songs_list.curselection())
		for item in selected:
			songs_list.delete(item)
			del songs_path[item]
		del_opt=False
		songs_list.config(selectmode=SINGLE)
	myLabel.config(text='')
	status_bar.config(text="Songs deleted...")
	root.update()
	status_bar.after(3000, status_bar.config(text=""))


def delete_all():
	stop_song()
	global songs_path
	songs_list.delete(0,END)
	songs_path=[]
	status_bar.config(text="All songs deleted...")
	root.update()
	status_bar.after(3000, status_bar.config(text=""))


global running_state
running_state=False
# Play a song function
def play_song():
	global stopped, running_state
	stopped=False
	running_time_label.config(text="")
	slider.config(value=0)
	if running_state:
		stopped =True
	index=songs_list.curselection()
	if len(index)==0:
		status_bar.config(text="Play song")
		return
	pygame.mixer.music.load(songs_path[index[0]])
	pygame.mixer.music.play(loops=0)
	status_bar.config(text="Song playing...")
	running_time_fct()

global paused
paused=False
def pause_song():
	index=songs_list.curselection()
	if len(index)==0:
		status_bar.config(text="Pause playing")
		return
	pygame.mixer.music.pause()
	global paused
	if not paused:
		pygame.mixer.music.pause()
		paused=True
		status_bar.config(text="Song Paused...")
	else :
		pygame.mixer.music.unpause()
		paused=False
		status_bar.config(text="Song playing...")



def stop_song():
	index=songs_list.curselection()
	if len(index)==0:
		status_bar.config(text="Stop playing")
		return
	pygame.mixer.music.stop()
	songs_list.selection_clear(ACTIVE)
	status_bar.config(text="Song stopped")
	slider.config(value=0)
	running_time_label.config(text="")
	total_time_label.config(text="")
	global stopped
	stopped=True

def next_previous_song(d):
	global running_state, stopped
	index=songs_list.curselection()
	running_time_label.config(text="")
	slider.config(value=0)
	if d==1: # play next
		if len(index)==0:
			status_bar.config(text="Play next song")
			return
		i=(index[0]+1)%len(songs_path) 
		pygame.mixer.music.load(songs_path[i])
		pygame.mixer.music.play(loops=0)
		status_bar.config(text="Song playing...")
		# clear current selection
		songs_list.selection_clear(ACTIVE)
		#Activate next song bar
		songs_list.activate(i)
		# Activate selection
		songs_list.selection_set(i, last=None)
		if running_state:
		 stopped =True
		running_time_fct()
	if d==-1: #play previous
		if len(index)==0:
			status_bar.config(text="Play previous song")
			return
		i=index[0]%len(songs_path)-1
		if i==-1:
			i=len(songs_path)-1
		pygame.mixer.music.load(songs_path[i])
		pygame.mixer.music.play(loops=0)
		status_bar.config(text="Song playing...")
		#print(songs_path[i])
		# clear current selection
		songs_list.selection_clear(ACTIVE)
		#Activate next song bar
		songs_list.activate(i)
		# Activate selection
		songs_list.selection_set(i, last=None)
		if running_state:
			stopped =True
		running_time_fct()

global update_slider
update_slider=False
global is_end
is_end=False
global current_pos
def running_time_fct():
	global current_pos,formated_pos
	global update_slider
	global is_end
	global stopped
	global running_state
	if stopped:
		stopped=False
		running_state=False
		return
	index=songs_list.curselection()
	#load song with mutagen
	song_mut=MP3(songs_path[index[0]])
	#Get song length
	song_length = int(song_mut.info.length)
	#print(song_length)
	if song_length==int(slider.get()):	
		current_pos=song_length
		formated_pos=time.strftime("%M:%S", time.gmtime(current_pos))
		running_time_label.config(text= f"{formated_pos}")
		formated_song_length=time.strftime("%M:%S", time.gmtime(song_length))
		total_time_label.config(text= f"{formated_song_length}")
		running_time_label.config(text= f"{formated_pos}")
		total_time_label.config(text= f"{formated_song_length}")
		slider.config(to=song_length, value=current_pos)
		global is_end
		is_end =True
		running_state=False
		if auto_play:
			next_previous_song(1)
			running_state=True
			is_end=False
		return
	elif paused:
		pass
	elif update_slider:
		current_pos=int(slider.get())
		formated_pos=time.strftime("%M:%S", time.gmtime(current_pos))
		current_pos+=1
	else:
		current_pos=int(pygame.mixer.music.get_pos())//1000
		formated_pos=time.strftime("%M:%S", time.gmtime(current_pos))
	formated_song_length=time.strftime("%M:%S", time.gmtime(song_length))
	running_time_label.config(text= f"{formated_pos}")
	total_time_label.config(text= f"{formated_song_length}")
	slider.config(to=song_length, value=current_pos)
	running_state=True
	slider.after(1000,running_time_fct)
# Create slider function
def slider_fct(x):
	global update_slider
	global is_end
	update_slider=True
	index=songs_list.curselection()
	if len(index)==0:
		slider.config(value=0)
		running_time_label.config(text="00:00")
		return
	#load song with mutagen
	song_mut=MP3(songs_path[index[0]])
	#Get song length
	song_length = int(song_mut.info.length)
	#print(song_length)
	#print(int(slider.get()))
	slider.config(to=song_length)
	pygame.mixer.music.play(loops=0, start=int(slider.get()))
	if is_end:
		is_end=False
		running_time_fct()

global once, muted
muted=False
global volume_slider
once=False
def mute_volume():
	global muted
	if not muted:
		pygame.mixer.music.set_volume(0)
		muted=True
		volume_menu.entryconfigure(2, label="Unmute")

	else: 
		pygame.mixer.music.set_volume(1)
		muted=False
		volume_menu.entryconfigure(2, label="Mute")

global volume_value
volume_value=0.5
def volume_fct(x):
	global volume_meter,volume_slider,volume_value
	volume_value=volume_slider.get()
	pygame.mixer.music.set_volume(volume_slider.get())
	#current_volume = pygame.mixer.music.get_volume()
	#current_volume = int(current_volume * 100)
	volume_meter.config(text=f"{int(volume_value*100)}%")

def change_volume():
	global volume_slider,volume_meter, once
	once=True
	vol_window=Tk()
	vol_window.title("MP3 Player")
	vol_window.geometry('180x60')
	vol_window.resizable(0,0)
	# Gets the requested values of the height and widht.
	windowWidth = vol_window.winfo_reqwidth()
	windowHeight = vol_window.winfo_reqheight()	 
	# Gets both half the screen width/height and window width/height
	positionRight = int(vol_window.winfo_screenwidth()/2 - windowWidth/2)
	positionDown = int(vol_window.winfo_screenheight()/3 - windowHeight/2) 
	# Positions the window in the center of the page.
	vol_window.geometry("+{}+{}".format(positionRight, positionDown))
	volume_slider=ttk.Scale(vol_window, from_=0, to=1,orient=HORIZONTAL, value=volume_value, command=volume_fct, length=150)
	volume_slider.pack(pady=(10,0))
	volume_meter=Label(vol_window, text=f"{int(volume_value*100)}%")
	volume_meter.pack()
# Create menu
my_menu=Menu(root)
root.config(menu=my_menu)
# add menu items
options=Menu(my_menu)
options.config(tearoff=0)
my_menu.add_cascade(label='Options', menu= options)
options.add_command(label='Add songs', command= add_songs)
options.add_separator()
#options.add_command(label='Autoplay', command= autoplay_songs)
#options.add_separator()
options.add_command(label='Select songs and delete', command= select_to_delete_songs)
options.add_separator()
options.add_command(label='Delete all', command= delete_all)
options.add_separator()
options.add_command(label='Quit', command= root.quit)

autoplay_menu=Menu(my_menu)
autoplay_menu.config(tearoff=0)
my_menu.add_cascade(label='Autoplay', menu= autoplay_menu)
autoplay_menu.add_command(label='Autoplay', command= autoplay_songs )

volume_menu=Menu(my_menu)
volume_menu.config(tearoff=0)
my_menu.add_cascade(label='Volume', menu= volume_menu)
volume_menu.add_command(label='Change', command= change_volume)
volume_menu.add_separator()
volume_menu.add_command(label='Mute', command= mute_volume)

'''volume_menu.add_separator()
volume_menu.add_command(label='Unmute', command= mute_volume)'''

# Create playlist
frame3=Frame(root)
scroll_ver=Scrollbar(frame3, orient =VERTICAL)
scroll_hor=Scrollbar(frame3, orient =HORIZONTAL)
songs_list= Listbox(frame3, bg='white', fg='Black', width=55, selectbackground='green', \
					selectforeground='white', yscrollcommand=scroll_ver.set,xscrollcommand=scroll_hor.set)
scroll_ver.config(command=songs_list.yview)
scroll_hor.config(command=songs_list.xview)
scroll_ver.pack(side=RIGHT, fill=Y)
scroll_hor.pack(side=BOTTOM, fill=X)
songs_list.pack(pady=(20,0))
frame3.pack(padx=(12,0))
songs_list.bind('<Delete>', delete_songs) 

#Create frame for buttons
frame=Frame(root, bd=5, bg="gray")
frame.pack(fill='x', pady=25)
# Create buttons
img1=PhotoImage(file='img/play.png')
play=Button(frame, image=img1, command=play_song)
play.grid(row=0, column=0, padx=(17,10))

img2=PhotoImage(file='img/pause.png')
pause=Button(frame, image=img2, command= pause_song)
pause.grid(row=0, column=1 , padx=10)

img3=PhotoImage(file='img/stop.png')
stop=Button(frame, image=img3, command=stop_song)
stop.grid(row=0, column=2 , padx=10)

img4=PhotoImage(file='img/back.png')
forward=Button(frame, image=img4, command=lambda:next_previous_song(-1))
forward.grid(row=0, column=3 , padx=10)

img5=PhotoImage(file='img/forward.png')
back=Button(frame, image=img5, command=lambda:next_previous_song(1))
back.grid(row=0, column=4 , padx=10)

# Create status bar
status_bar=Label(root,text='', bd='1', relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side =BOTTOM, ipady=2)

# Create song position slider
frame2=Frame(root, bd=5, bg="white")
frame2.pack(pady=20)
slider=ttk.Scale(frame2, from_=0, to=100,orient=HORIZONTAL, value=0, command=slider_fct, length=300)
slider.grid(row=0, column=0, columnspan=100)
running_time_label=Label(frame2,text='00:00', bd='1', relief=GROOVE, anchor=W)
running_time_label.grid(row=1, column=0, padx=0)
total_time_label=Label(frame2,text='xx:xx', bd='1', relief=GROOVE, anchor=E)
total_time_label.grid(row=1, column=99)

root.mainloop()