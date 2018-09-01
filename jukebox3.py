
# =================
# jukebox3.py
# =================

# ======================================================================================
# Subclassing tkinter listbox to create our own Scrollbox with additional functionality
# ======================================================================================

# We will make CHANGE_1 to add the grid functionality to Scrollbox and avoid repeated code under LINE_4 and LINE_5

# When we run this code, we see we have our scrollbox is working and it scrolls within the box
# And we have successfully subclassed the tkinter listbox to create our own scrollbox and provided some additional functionality.
# This is great use of inheritance.

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

    # CHANGE_1
    # We have just created our subsclass in listbox that we can add extra functionality to.
    # In this case, we want to add a Scrollbar.
    # The time to add this is when the scrollbox is added to the layout manager.
    # we are only going to support the grid manager and to do this, we will overide the grid method.

    # tkinter.Listbox.grid(self, row=row, column=column, sticky=sticky, rowspan=rowspan, **kwargs)  # Python 2 code
    def grid(self, row, column, sticky='nsw', rowspan=1, columnspan=1, **kwargs):
        super().grid(row=row, column=column, sticky=sticky, rowspan=rowspan, columnspan=columnspan, **kwargs)  # call Super and pass options we don't want to use in kwargs
        self.scrollbar.grid(row=row, column=column, sticky='nse', rowspan=rowspan)  # Code used to display the scrollbar using scrollbar.grid method
        self['yscrollcommand'] = self.scrollbar.set

    # Since we use above two lines to display scrollbar, we will delete lines shown below after LINE_4 and LINE_5


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

# LINE_4 - we delete these 3 lines because we are implementing them in our class Scrollbox above
# artistScroll = tkinter.Scrollbar(mainWindow, orient=tkinter.VERTICAL, command=artistList.yview)  # yview can only scroll vertically
# artistScroll.grid(row=1, column=0, sticky='nse', rowspan=2)
# artistList['yscrollcommand'] = artistScroll.set

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

# LINE_5 - we delete these 3 lines because we are implementing them in our class Scrollbox above
# albumScroll = tkinter.Scrollbar(mainWindow, orient=tkinter.VERTICAL, command=albumList.yview)  # yview can only scroll vertically
# albumScroll.grid(row=1, column=1, sticky='nse', rowspan=2)
# albumList['yscrollcommand'] = albumScroll.set


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


# =========================================================
# Now go to jukebox4.py to populate listbox from database
# =========================================================
