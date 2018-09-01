

# =================
# jukebox4.py
# =================

# ==================================
# Populating listbox from database:
# ==================================

# we now want to create a scollable listbox that can populate itself from the database.
# We will see how to populate the listboxes and how clicking on one item in the listbox will populate the other listbox.

# The Artist list is the simplest because it does not update when something else is clicked.
# So we just execute a query and insert the query result into the listbox. under CHANGE_2
# Then when we click an item under Artists, it responds by populating Albums under that artist. under CHANGE_3 & CHANGE_4

# Now we will write code to produce songs when album is selected. CHANGE_5
# And then we bind the code to album_list. CHANGE_6

# NOTE: After making CHANGE_5, program runs as expected but am getting "IndexError: tuple index out of range"
# NOTE: Correction was done on CORRECTION_1; where we added exportselection=False to clear "IndexError: tuple index out of range"


import sqlite3
try:
    import tkinter
except ImportError:  # in case of python 2
    import Tkinter as tkinter

# connect to music.db

conn = sqlite3.connect('music.db',)

# ======= Scrollbox ==========

class Scrollbox(tkinter.Listbox):

    # tkinter.listbox.__init__(self, window, **kwargs)  # Syntax for python2
    def __init__(self, window, **kwargs):  # python3. We overwrite the init method to add scrollbar field
        # CORRECTION_1; Added exportselection=False under super(). __init__ to clear "IndexError: tuple index out of range"
        super().__init__(window, **kwargs, exportselection=False)  # Then we call the super method.

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



# CHANGE_4
# When a bound function is called, it gets passed a single argument "event". LINE_11
# We use that event to retrieve our reference to the widget to trigger the effect. LINE_12
# A listbox (lb) has a curselection method that returns a tuple containing the positions of all the selected items in the list. LINE_13
# initially, we will only allow a single item to be selected in the GUI by hardcoding the first value [0] of returned tuple. LINE_13
# We will come back to allowing selection of multiple items later when we create the class
# Once we know the position of the selected item, we can use the "get" method to that from the listboxes list,
# so we know Artist name that was selected . LINE_14
# unfortunately, the TK in this box does not provide any way to associate an ID with the strings that it displays.
# So we have to query the database to retrieve the artists ID. LINE_15
# We are using a local database, so this is not a problem, but if we were getting data from a remote database, we may
# want to reduce the number of network calls that we may have to make to fetch data.
# In that case, we could add a list to our Listbox subclass and then store the database IDs
# in the list in the same position as the names in the Listbox
# We however need to be careful to keep the list in Sync if rows can be inserted and deleted from the database.
# A better option in that case would be to use new TTK Triveiw widget in order to store the IDs in a column alongside the names.

# In this case, we are using a local database, so we will run a query in LINE_15 to return the ID of the specified artist. i.e. artist_id

# We will use artist_name (LINE_14) as a parameter to the query, but we have to pass a tuple rather than a single value
# artist_name is a tuple and we don't have to worry about using it when executing the query.
# The fetchone method (LINE_15) returns a tuple so that variable artist_id will already be suitable for passing on to the next query.
# Now we use the artist_id to query the albums table on LINE_16 and from there we are getting a list of the albums.
# Then we append the names to a list on LINE_17
# Remember that the listbox wants a tuple in the list variable, so we convert "alist" from a list to a tuple before
# setting it as value of albumLV on LINE_18


def get_albums(event):  # LINE_11
    lb = event.widget   # LINE_12
    index = lb.curselection()[0]  # LINE_13
    artist_name = lb.get(index),   # LINE_14

    # Now get the artist ID from the database row
    artist_id = conn.execute("SELECT artists._id FROM artists WHERE artists.name =?", artist_name).fetchone()  # LINE_15
    alist = []
    for row in conn.execute("SELECT albums.name FROM albums WHERE albums.artist = ? ORDER BY albums.name", artist_id):  # LINE_16
        alist.append(row[0])  # LINE_17
    albumLV.set(tuple(alist))  # LINE_18
    songLV.set(("Choose an Album",))  # CHANGE_7: This resets the song when you click on new album and tells you to choose an album.


# CHANGE_5

def get_songs(event):
    lb = event.widget
    index = int(lb.curselection()[0])
    print("Index = {}".format(index))
    album_name = lb.get(index),

    # Get the album ID from database row
    album_id = conn.execute("SELECT albums._id FROM albums WHERE albums.name=?", album_name).fetchone()
    alist = []
    for x in conn.execute("SELECT songs.title FROM songs WHERE songs.album=? ORDER BY songs.track", album_id):
        alist.append(x[0])
    songLV.set(tuple(alist))

    # We will now bind the get_songs function to album Listbox below and
    # songs list will be updated when we click on an album:  CHANGE_6 below



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

# CHANGE_2
# This code retrieves artists name from database and populates to Artists column.

for artist in conn.execute("SELECT artists.name FROM artists ORDER BY artists.name"):
    artistList.insert(tkinter.END, artist[0])

# CHANGE_3: bind the artist to album
# When you click an item under Artist, it populates Albums under that artist.
# We saw how to cause a function to be executed when a button is clicked when we looked at blackjack game in section 11
# Listboxes don't have an explicit command property, but they have a number of events that we can bind functions to.
# The event we will use here is a Virtual Event called "listboxSelect" which the listbox receives when an item is selected.
# We can bind our own function or method to that virtual event so our function is called when our event happens.
# NOTE that we need to define "get_albums". We will do that under CHANGE_4 above

artistList.bind('<<ListboxSelect>>', get_albums)  # Whenever an item is selected under ArtistList, get_albums method will be called


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

# CHANGE_6
# Wnen we run the code, it works by producing songs when we click on an album
# However when we click on another artist, the songs are not updated automatically until we click on the new album.
# We can correct this under CHANGE_7

albumList.bind('<<ListboxSelect>>', get_songs)




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

