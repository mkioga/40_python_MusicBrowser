# ===============================================
# GUI Database Viewer Setup
# ===============================================

# ===================
# Jukebox.py testing
# ===================

# First we will use database tab to configure data source correctly, so we don't get warning messages from intellij
# In our case, it looks like there is no database window, but we test using code below, we are able to connect to music.db and select stuff

# import sqlite3
#
# conn = sqlite3.connect('music.db', )
#
# for x in conn.execute("SELECT albums.name FROM albums WHERE albums.artist = ? ORDER BY albums.name", (196,)):
#     print(x)


# ===================
# Jukebox.py
# ===================

# We will combine what we have learned about databases and classes
# We will learn how "subclassing" and using existing classes can add extra functionality
# You need to know what the subclass does, but don't necesarrily need to know how it works.

# We will use our music.db database to produce a visual database browser
# It will show artists in a list, and when you select the artist, another list shows up with their albums.
# And when you click on an album, you will see all the songs in that album in a third list.

# The GUI we will build is similar to one named "Music Browser GUI we want to make.jpg"

# first we import sqlite3 and tkinter

import sqlite3
try:
    import tkinter
except ImportError:  # in case of python 2
    import Tkinter as tkinter

# connect to music.db

conn = sqlite3.connect('music.db', )

# ======= mainWindow =========

mainWindow = tkinter.Tk()
mainWindow.title('Music DB Browser')  # use single quotes
mainWindow.geometry('1024x768')

# ========= columns ===========

mainWindow.columnconfigure(0, weight=2)
mainWindow.columnconfigure(1, weight=2)
mainWindow.columnconfigure(2, weight=2)
mainWindow.columnconfigure(3, weight=1)  # spacer column on right

# ========= rows ===========

mainWindow.rowconfigure(0, weight=1)
mainWindow.rowconfigure(1, weight=5)  # We give more weight to these middle two rows because they contain the listboxes
mainWindow.rowconfigure(2, weight=5)
mainWindow.rowconfigure(3, weight=1)

# Configure labels for the columns

tkinter.Label(mainWindow, text="Artists").grid(row=0, column=0)
tkinter.Label(mainWindow, text="Albums").grid(row=0, column=1)
tkinter.Label(mainWindow, text="Songs").grid(row=0, column=2)


# ========= artist Listbox ===========

artistList = tkinter.Listbox(mainWindow)
artistList.grid(row=1, column=0, sticky='nsew', rowspan=2, padx=(30, 0))
artistList.config(border=2, relief='sunken')

# Add scrollbar next to artist listbox
# When you run this, you will see a scrollbar next to artists column

artistScroll = tkinter.Scrollbar(mainWindow, orient=tkinter.VERTICAL, command=artistList.yview)  # yview can only scroll vertically
artistScroll.grid(row=1, column=0, sticky='nse', rowspan=2)
artistList['yscrollcommand'] = artistScroll.set

# ========= album Listbox ===========

# tkinter.Variables are tracked variables. This means that if they change, anything that uses them is notified of the change
# In this case, the Variable is assigned to albumLV which is linked to listvariable=albumLV to inform it of any changes
# We can test the change in main loop using line named TESTLINE

albumLV = tkinter.Variable(mainWindow)
albumLV.set(("Choose an Artist",) )

albumList = tkinter.Listbox(mainWindow, listvariable=albumLV)  # albumList informed if albumLV changes.
albumList.grid(row=1, column=1, sticky='nsew', padx=(30, 0))
albumList.config(border=2, relief='sunken')

# album Scroll

albumScroll = tkinter.Scrollbar(mainWindow, orient=tkinter.VERTICAL, command=albumList.yview)  # yview can only scroll vertically
albumScroll.grid(row=1, column=1, sticky='nse', rowspan=2)
albumList['yscrollcommand'] = albumScroll.set


# ========= Songs Listbox ===========

songLV = tkinter.Variable(mainWindow)
songLV.set(("Choose an Album", ))

songList = tkinter.Listbox(mainWindow, listvariable=songLV)
songList.grid(row=1, column=2, sticky='nsew', padx=(30, 0))
songList.config(border=2, relief='sunken')


# ========= Main loop ===========

# TESTLINE: set albumLV with tuple shown. Enclose in two brackets because we are passing a tuple to a function
# when you run it, we see albums listbox is displaying items from the tuple because albums is bound to albumLV
# and if albumLV contents change, then albums contents change

# albumLV.set((1,2,3,4,5))  # TESTLINE: we comment it out for now

# We will add contents in album

testList = range(0, 100)
albumLV.set(tuple(testList))  # we pass a tuple with numbers from 0 to 100. similar to tuple in TESTLINE above

mainWindow.mainloop()
print("Closing database connection")
conn.close()


# ==========================================================
# Now go to star_args.py to learn about *args and **kwargs
#  =========================================================


