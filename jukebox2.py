
# =================
# jukebox2.py
# =================

# ========================
# Scrollable listboxes
# ========================

# Now that we have looked at *args and **kwargs and how we can pass arguments that we don't need to handle or know
# We will now create a listbox class that includes its own Scrollbar
# We cannot do this from scratch, because we would have to learn another language called TCL, which TKinter is written from.
# But we already have a working listbox class and we can inherit most of the behavior from there.

# We will create a scrollable listbox class and call it Scrollbox
# And then add Scrollbox class to LINE_1, LINE_2 and LINE_3

# When we run this code, we see we have our scrollbox although it runs to the bottom of the 2nd column
# We also have repeated code on LINE_4 and LINE_5 which we can put in the Scrollbox class.
# We will do this in jukebox3.py


import sqlite3
try:
    import tkinter
except ImportError:  # in case of python 2
    import Tkinter as tkinter

# connect to music.db

conn = sqlite3.connect('music.db', )

# ======= Scrollbox ==========

class Scrollbox(tkinter.Listbox):

    # tkinter.listbox.__init__(self, window, **kwargs)  # Syntax for python2
    def __init__(self, window, **kwargs):  # python3. We overwrite the init method to add scrollbar field
        super().__init__(window, **kwargs)  # Then we call the super method.

        self.scrollbar = tkinter.Scrollbar(window, orient=tkinter.VERTICAL, command=self.yview)

 # Now we have defined our listbox base class (Scrollbox), we need to change our listbox types to Scrollbox.
# See LINE_1, LINE_2 and LINE_3


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

# artistList = tkinter.Listbox(mainWindow)
artistList = Scrollbox(mainWindow,)  # LINE_1. NOTE we can add background color e.g. background='yellow'
artistList.grid(row=1, column=0, sticky='nsew', rowspan=2, padx=(30, 0))
artistList.config(border=2, relief='sunken')

# Add scrollbar next to artist listbox
# When you run this, you will see a scrollbar next to artists column

# LINE_4 - repeated code
artistScroll = tkinter.Scrollbar(mainWindow, orient=tkinter.VERTICAL, command=artistList.yview)  # yview can only scroll vertically
artistScroll.grid(row=1, column=0, sticky='nse', rowspan=2)
artistList['yscrollcommand'] = artistScroll.set

# ========= album Listbox ===========

# tkinter.Variables are tracked variables. This means that if they change, anything that uses them is notified of the change
# In this case, the Variable is assigned to albumLV which is linked to listvariable=albumLV to inform it of any changes
# We can test the change in main loop using line named TESTLINE

albumLV = tkinter.Variable(mainWindow)
albumLV.set(("Choose an Artist",) )

# albumList = tkinter.Listbox(mainWindow, listvariable=albumLV)  # albumList informed if albumLV changes.
albumList = Scrollbox(mainWindow, listvariable=albumLV)  # LINE_2
albumList.grid(row=1, column=1, sticky='nsew', padx=(30, 0))
albumList.config(border=2, relief='sunken')

# album Scroll

# LINE_5 - repeated code
albumScroll = tkinter.Scrollbar(mainWindow, orient=tkinter.VERTICAL, command=albumList.yview)  # yview can only scroll vertically
albumScroll.grid(row=1, column=1, sticky='nse', rowspan=2)
albumList['yscrollcommand'] = albumScroll.set


# ========= Songs Listbox ===========

songLV = tkinter.Variable(mainWindow)
songLV.set(("Choose an Album", ))

# songList = tkinter.Listbox(mainWindow, listvariable=songLV)
songList = Scrollbox(mainWindow, listvariable=songLV)  # LINE_3
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

