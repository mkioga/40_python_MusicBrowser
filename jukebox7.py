
# =================
# jukebox7.py
# =================


# under CHANGE_31, we wrote get_albums function to link id of chosen artist to their albums.
# We will need to write get_songs function to do the same for linking album to songs
# To avoid repeating ourselves, we put above into a class and call that class whenever we want to link
# from Artist to Albums, and from Album to Songs
# We will do this under CHANGE_32
# Then add a link between one data listbox to another: CHANGE_33
# And method to link the listboxes: CHANGE_34
# Put binding under DatalistBox: CHANGE_35
# Then we link Artist to Album and Album to Song:  There are multiple changes named. CHANGE_36

# After all changes, this program funs fine and displays Album when you click artist and displays songs when you click album
# We have taken the basic TKinter listbox and have created our own  scrollable version of it.


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


# CHANGE_21
# NOTE it is advisable to add docstrings to this class if you intend to reuse it. Currently no docstrings are added.

class DataListBox(Scrollbox):

    def __init__(self, window, connection, table, field, sort_order=(), **kwargs):  # NOTE: sort_order returns a tuple
        # Scrollbox.__init__(self, window, **kwargs)  # Python 2
        super().__init__(window, **kwargs, exportselection=False)  # CORRECTION_1: exportselection=False was added to clear IndexError: tuple index out of range

        # CHANGE_33:
        # Adding a link between one data listbox to another
        # NOTE that not all listboxes will be linked e.g. Songs will not cause another listbox to be updated.
        # Therefore we may want to use a SQL data listbox to display a database table without linking into anything else.
        # Rather than insisting another DataListBox is provided in the class __init__ method, we will add a link method that
        # can be used if required.
        # We will use the link method while passing a widget that we want to link to and a database column that forms that link.
        # So we will need two more data attributes in our class DataListBox
        # We default to None so there is no link to start with.
        # if we need to link to listboxes, we will call link method in CHANGE_34 below

        self.linked_box = None
        self.link_field = None


        self.cursor = connection.cursor()  # self.cursor = connection to the cursor. hence ending with ()
        self.table = table
        self.field = field

        # CHANGE_35

        # We put the binding here and rename it

        self.bind('<<ListboxSelect>>', self.on_select)

        # This is SQL statement to retrieve required field and ID
        # NOTE that the table must have a column named _id to uniquely identify the table.

        self.sql_select = "SELECT " + self.field + ", _id" + " FROM " + self.table
        if sort_order:
            self.sql_sort = " ORDER BY " + ','.join(sort_order)  # specify SQL sort attribute with an order by clause
        else:
            self.sql_sort = " ORDER BY " + self.field  # otherwise order by field (default) if user does not specify order by argument

    # The class does not load any data, so we need to implement the requery method that it will need.
    # If we are going to allow the listboxes to be requeried so that they can show new data, we need some way to clear
    # the existing data out, hence we will also add a clear method.
    #
    def clear(self):
        self.delete(0, tkinter.END)

    # CHANGE_34

    # This is the method used to link to Listboxes
    # whenever we want to link two listboxes together, we can call this "link" method of the master Listbox.
    # We will pass it a reference to the datalistbox we want to link to, which is the name of the column in the DataListBox table.


    def link(self, widget, link_field):
        self.linked_box = widget
        widget.link_field = link_field  # Saving value passed in the argument.





    # CHANGE_30

    # We will modify requery and give it a single parameter which will be the ID to match and we will make that ID to None
    # So that we can populate a list without records as we did for the artist
    # LINE_30 Lisbox can populate itself with data for specific artist ID
    # You can test it by adding an artist ID e.g. 12 under "albumList.requery(12)" and it will pull the artist with artist id 12



    def requery(self, link_value=None):  # We add link_value=None
        if link_value and self.link_field:  # CHANGE_36: rest for link_value and link_field too.
            sql = self.sql_select + " WHERE " + self.link_field + "=?" + self.sql_sort # CHANGE_36: replace "artist" with self.link_field
            print(sql)   # TODO this is to print sql value here. Can delete
            self.cursor.execute(sql, (link_value,))
        else:  # Else if link_value is None, run this code
            print(self.sql_select + self.sql_sort)   # TODO This is for printing. Can delete after testing code
            self.cursor.execute(self.sql_select + self.sql_sort)  # We executing combination of sql_select and sql_sort

        # Clear the listbox Contents before reloading
        self.clear()
        for value in self.cursor:
            self.insert(tkinter.END, value[0])  # We add first item in the tuple list.

        # CHANGE_36
        # This is to clear the data in any linked data Listbox so when we select a new artist, the songs for old album are not displayed.

        if self.linked_box:
            self.linked_box.clear()

    # Now we will remove all the code to populate the list from the artists listbox and replace it with a call to this
    # requery method to see that it actually works. CHANGE_22



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


# CHANGE_31
# We will tell one listbox to tell another what ID to use by changing get_albums and get_songs.
# We will comment out the lines shown and add [0] to LINE_15
# Then we requery the albumList and pass it the artist_id that it should display the albums for.
# When you run code from here and choose different artists, it should be able to display the albums for those artists you chose.

# Now we can move this function (get_album) into a class so it can be reused and not repeated under get_songs.
# Then we can call that class whenever a new item is selected.
# We do that on jukebox7.py

    # CHANGE_32
    # We want this function to become a method under DataListBox class, hence we indent it to be under DataListBox class
    # Remember that all methods in a class have a "self" argument. So we add self in LINE_11
    # then instead of calling this method "get_albums", we can give it a more generic name like "on_select" that can be called for many functions

    # The "on_select" method below will only query a listbox if there is one. We need a way of linking two linkboxes together
    # first we need to check if there is a link to this box before trying to requery one.

    def on_select(self, event):  # LINE_11: Change method name to on_select and add self.
        if self.linked_box:  # Checks if there is a link before doing query
            print(self is event.widget)  # self should be same as event.widget. Checking here if its true
            # lb = event.widget   # LINE_12. since self is same as lb, we comment it out and modify below and replace lb with self.
            index = self.curselection()[0]  # LINE_13: replace lb with self.
            value = self.get(index),   # LINE_14: replace lb with self. and replace artist_name with value

            # Now get the artist ID from the database row
            # artist_id is returned as a tuple and we add [0] to return a first single value from that tuple.
            # We will change LINE_15 because we can now use function to pull Artist, or Album
            # And we will use position [1] because that is where the ID is located
            # NOTE this is related to LINE_30 above
            # NOTE: we are using global connection "conn" to connect to database, so if we try to reuse this code in another program
            # that calls has connection to database called something else other than "conn", then it will crash.
            # So when we move function (e.g. get_albums) into a class (e.g. Datalistbox class), we should make sure we are
            # not using global objects in the function.
            # So we need to change this method to use the classes cursor attribute i.e. from "conn.execute" to "self.cursor.execute"
            # NOTE we also change "artist_id" to "link_id" to be more generic

            link_id = self.cursor.execute(self.sql_select + " WHERE " + self.field + "=?", value).fetchone()[1]  # LINE_15


            # artist_id = conn.execute("SELECT artists._id FROM artists WHERE artists.name =?", artist_name).fetchone()[0]  # LINE_15
            self.linked_box.requery(link_id)  # change this to link_id too (from artist_id). and then replace "albumList" with "self.linked_box"


        # # Now get the artist ID from the database row
        # artist_id = conn.execute("SELECT artists._id FROM artists WHERE artists.name =?", artist_name).fetchone()  # LINE_15
        # alist = []
        # for row in conn.execute("SELECT albums.name FROM albums WHERE albums.artist = ? ORDER BY albums.name", artist_id):  # LINE_16
        #     alist.append(row[0])  # LINE_17
        # albumLV.set(tuple(alist))  # LINE_18
        # songLV.set(("Choose an Album",))  # CHANGE_7: This resets the song when you click on new album and tells you to choose an album.


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
# artistList = Scrollbox(mainWindow,)  # LINE_1. NOTE we can add background color e.g. background='yellow'
artistList = DataListBox(mainWindow, conn, "artists", "name")  # CHANGE_22. use class DataListBox instead of ScrollBox on LINE_1 and add connection, tablename and column you will display
artistList.grid(row=1, column=0, sticky='nsew', rowspan=2, padx=(30, 0))
artistList.config(border=2, relief='sunken')

# CHANGE_23
# We will comment out the sql code under CHANGE_2 below and then use artistList.requery

artistList.requery()

# CHANGE_2
# This code retrieves artists name from database and populates to Artists column.


# for artist in conn.execute("SELECT artists.name FROM artists ORDER BY artists.name"):
#     artistList.insert(tkinter.END, artist[0])


# CHANGE_3: bind the artist to album
# When you click an item under Artist, it populates Albums under that artist.
# We saw how to cause a function to be executed when a button is clicked when we looked at blackjack game in section 11
# Listboxes don't have an explicit command property, but they have a number of events that we can bind functions to.
# The event we will use here is a Virtual Event called "listboxSelect" which the listbox receives when an item is selected.
# We can bind our own function or method to that virtual event so our function is called when our event happens.
# NOTE that we need to define "get_albums". We will do that under CHANGE_4 above

# CHANGE_35.

# We remove this listboxSelect binding and put it under CHANGE_35 above
# artistList.bind('<<ListboxSelect>>', get_albums)  # Whenever an item is selected under ArtistList, get_albums method will be called


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
# albumList = Scrollbox(mainWindow, listvariable=albumLV)  # LINE_2
albumList = DataListBox(mainWindow, conn, "albums", "name", sort_order=("name",))  # CHANGE_24. replace LINE_2 with DataListBox and add parameters
albumList.requery()  # CHANGE_25. add this requery
albumList.grid(row=1, column=1, sticky='nsew', padx=(30, 0))
albumList.config(border=2, relief='sunken')

# CHANGE_6
# Wnen we run the code, it works by producing songs when we click on an album
# However when we click on another artist, the songs are not updated automatically until we click on the new album.
# We can correct this under CHANGE_7

# albumList.bind('<<ListboxSelect>>', get_songs)

# CHANGE_36

# We will comment out the "albumList.bind('<<ListboxSelect>>', get_songs)" above and replace it with:
# Then use below code to link Albumlist to Artistlist

artistList.link(albumList, "artist")


# album Scroll

# LINE_5 - we delete these 3 lines because we are implementing them in our class Scrollbox above
# albumScroll = tkinter.Scrollbar(mainWindow, orient=tkinter.VERTICAL, command=albumList.yview)  # yview can only scroll vertically
# albumScroll.grid(row=1, column=1, sticky='nse', rowspan=2)
# albumList['yscrollcommand'] = albumScroll.set


# ========= Songs Listbox ===========

songLV = tkinter.Variable(mainWindow)
songLV.set(("Choose an Album", ))

# songList = tkinter.Listbox(mainWindow, listvariable=songLV)
# songList = Scrollbox(mainWindow, listvariable=songLV)  # LINE_3
songList = DataListBox(mainWindow, conn, "songs", "title", ("track", "title"))  # CHANGE_26. Sort order may be in format: sort_order=("track", "title")
songList.requery()  # CHANGE_27
songList.grid(row=1, column=2, sticky='nsew', padx=(30, 0))
songList.config(border=2, relief='sunken')

# CHANGE_36

# Then we will link SongList to Albumlist

albumList.link(songList, "album")


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

