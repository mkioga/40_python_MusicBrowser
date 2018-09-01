
# =================
# jukebox9.py
# =================

# There is a bug in the code from jukebox8.py and we will fix it here

# THE BUG
# The bug itself is that if any Artist has an album with the same name as the other artist, it selects songs for the first artist's album
# For example, Artist "Billy Idol" has album "Greatest Hits" which has songs starting with "American Girl" and ends with "Something in the Air"
# Artist "Fleetwood Mac" also has album named "Greatest Hits". If you click his album, it generates same songs as from Billy Idol's Greatest hits album
# Same things for Artist "Tom Petty & the heartbreakers" have album "Greatest hits" pulling same songs.

# All these artists have album named "Greatest Hits", but the program is pulling only the songs for the
# first artists (Billy Idols) "greatest hits" album from the database.
# This is because we are looking at the "display value" in the database instead of using IDs

# We need to modify the DataListbox Class so that it retrieves the correct record from the linked table
# i.e. the Album (Greatest hits) for the correct artist.
# Remember we are keeping DataListbox class generic so that it can cope with any table that has a single column primary key.
# Before we do this, we need to query the database table from within Intellij ID or pycharm using DB Browser plugin

# FIND OUT HOW MANY DUPLICATE ALBUMS EXIST:

# Click on DB Browser icon on the right
# Then we need to point it to our SQLite database under Database files to database named "music.db"
# Note that this needs the full path.
# Click space next to "Database files" then click the ... to open browse window
# then navigate to the folder where your account is and select "accounts.sqlite"
# C:\Users\moe\Documents\Python\IdeaProjects\40_MusicBrowser\music.db
# Then click "Test Connection" and it should say its connected.
# NOTE: Full instructions under " DB Browser install "

# To execute the SQL commands to query database, Click the icon in "DB Browser" named "Open SQL Console"
# This opens a window where we can enter this SQL command
# Then type this SQL command. NOTE: you don't need to end it with ;

# SELECT albums.name, COUNT(albums.name) AS num_albums FROM albums GROUP BY albums.name HAVING num_albums >1

# Then click the green arrow (Execute Statement).

# It should run and give you below results which shows four duplicated album names in the database.
# Greatest hits appear 4 times and the rest appear 2 times each

# ========= Name ========== : num_albums
# Champion of Rock          : 2
# Greatest Hits             : 4
# Pictures at an exhibition : 2
# The very best of          : 2

# We need to know which artists are associated with these albums (with same names) so we can test our fix.
# We will run another SQL query to retrieve the artist names for above duplicate albums
# We will do this under the DB Browser "Open SQL Console" and use below SQL query:

# SELECT artists._id, artists.name, albums.name FROM artists
#   INNER JOIN albums ON albums.artist = artists._id
# WHERE albums.name IN
#   (SELECT albums.name FROM albums GROUP BY albums.name HAVING COUNT(albums.name) > 1)
# ORDER BY albums.name, artists.name

# Click the "Execute Statement" green arrow and it will give you results below.

# _id : === name ========= : ======== name ========
# 114 : Blue Ouster Cult   : Champion of Rock
# 13  : Nazareth           : Champion of Rock
# 176 : Billy Idol         : Greatest Hits
# 92  : Fleetwood Mac      : Greatest Hits

# Truncated. There are 10 records in total

# CHALLENGE

# Now the challenge is to fix the "DataListBox" class so that it displays the songs for the correct album
# when the same album name appears more than once in the database.
# Hint: you should work out what you need the query to be, then check the code to see at what point you actually
# have the information you will need.

# SOLUTION

# Check Explanation and changes starting at CHANGE_40



import sqlite3
try:
    import tkinter
except ImportError:  # in case of python 2
    import Tkinter as tkinter

# CHANGE_37
# This connection will be moved under "if __name__ == '__main__'. See CHANGE_37 below

# connect to music.db
# conn = sqlite3.connect('music.db',)

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

        # CHANGE_42

        # we add the data attribute to store link_value, which is artist_id when requeried from albums listbox)
        # Then we will save it in our requery method: go back to CHANGE_41
        self.link_value = None

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


    # CHANGE_41

    # We can see that artists_id was passed to requery method below as "link_value'
    # When requery is called on the albums listbox, we get the artist to filter on on the "link_value" argument
    # This is the only time we know the artist Id, so we need to store it in a "data attribute" so we can then use it later.
    # We will add a field to store the link_value (artist_id) and it will be updated every time the requery method is called.
    # We also need to cater for the fact that it can be None when the complete table is displayed.

    # We add code for "data attribute" under CHANGE_42 above

    # After adding the data attribute, we come back here to save it with data every time it is requeried by album listbox.
    # See line marked CHANGE_41 below

    # The final step is now to update the WHERE clause of our query in the on_select method.
    # Go back to CHANE_40 below

    def requery(self, link_value=None):  # We add link_value=None
        self.link_value = link_value   # CHANGE_41 : store the id so we know the "master" record we are populated from.
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


    # CHANGE_40

    # The code under "on_select" (see original under jukebox8.py) runs a SQL query to retrieve the ID for the selected album
    # but it does not consider which artist the album belongs to.
    # Effectively it runs this SQL code and then uses the fetchone method to retrieve the second row (id)
    # SELECT name, _id FROM albums WHERE name = "Greatest Hits"
    # If you test it in DB Browser, you will see it retrieves 4 records without regard for who the Artists are:

    # SOLUTION
    # So the SOLUTION is to change the Where clause so it includes the artists ID
    # We can test the SQL code to see how it works. Example code:
    # SELECT name, _id, artist FROM albums WHERE name = "Greatest Hits" AND artist = 176 (Billy Idol)

    # This gives results: Its considers the name of album and the artist it belongs to.

    # == name ===== : = _id =  : == artist ==
    # Greatest Hits : 399      : 176

    # Code to check which artist is 176 (Billy Idol)
    # SELECT * FROM artists WHERE _id = 176

    # Code to check which album has Id of 399
    # SELECT * FROM songs WHERE album = 399

    # So now we need to add artist_id to our query
    # Question is where are we going to get the artist_id from in our code ?
    # See CHANGE_41 above next to requery method

    # After doing CHANGE_41, and CHANGE_42, we come back here to update the WHERE clause of our query in the "on_select" method.
    # We will name this CHANGE_43


    def on_select(self, event):  # LINE_11: Change method name to on_select and add self.
        if self.linked_box:  # Checks if there is a link before doing query
            print(self is event.widget)  # self should be same as event.widget. Checking here if its true
            # lb = event.widget   # LINE_12. since self is same as lb, we comment it out and modify below and replace lb with self.
            index = self.curselection()[0]  # LINE_13: replace lb with self.
            value = self.get(index),   # LINE_14: replace lb with self. and replace artist_name with value

            # CHANGE_43

            # Get the ID from the database row.
            # Make sure we are getting the correct one, by including the link_value if appropriate

            # NOTE: in this line ==> ( value = value[0], self.link_value ), we are creating a new tuple (value) by combining
            # the first item on the existing value with the new link_value.

            # This is the FIX for the bug which was causing same "Greatest Hits" songs to be chosen even if the album is from different artists
            # Now we can test it by clicking these Artists> albums and we see they give different Songs:
            # Billy Idol > Greatest hits
            # Fleetwood Mac > Greatest hits
            # Troggs > Greatest Hits

            if self.link_value:  # Make sure we have a link_value
                value = value[0], self.link_value  # if link_value exist, we add a WHERE clause that includes the link_value
                sql_where = " WHERE " + self.field + "=? AND " + self.link_field + "=?"
            else:  # if link_value does not exist, we set the WHERE clause to self.field=?, which is what it was originally
                sql_where = " WHERE " + self.field + "=?"

            # Note this line is modified to have sql_where replace ( " WHERE " + self.field + "=?" ) which was there originally
            # This is because "sql_where" will include link_value if link_value exists.

            link_id = self.cursor.execute(self.sql_select + sql_where, value).fetchone()[1]  # LINE_15

            # link_id = self.cursor.execute(self.sql_select + " WHERE " + self.field + "=?", value).fetchone()[1]  # original LINE_15

            # artist_id = conn.execute("SELECT artists._id FROM artists WHERE artists.name =?", artist_name).fetchone()[0]  # LINE_15
            self.linked_box.requery(link_id)  # change this to link_id too (from artist_id). and then replace "albumList" with "self.linked_box"



# CHANGE_5

# CHANGE_37
# We don't need this get_songs function anymore because we are now using "on_select" which was modified from get_albums.
# We also don't need to connect to the database right at the start of the program
# we did that originally because our functions were using the global database connection.
# But now we are passing our connection to the DataListBox object, so this code is not needed anymore
# so we can delete or comment out the get_songs function

# def get_songs(event):
#     lb = event.widget
#     index = int(lb.curselection()[0])
#     print("Index = {}".format(index))
#     album_name = lb.get(index),
#
#     # Get the album ID from database row
#     album_id = conn.execute("SELECT albums._id FROM albums WHERE albums.name=?", album_name).fetchone()
#     alist = []
#     for x in conn.execute("SELECT songs.title FROM songs WHERE songs.album=? ORDER BY songs.track", album_id):
#         alist.append(x[0])
#     songLV.set(tuple(alist))


# We will now bind the get_songs function to album Listbox below and
# songs list will be updated when we click on an album:  CHANGE_6 below



# Now we have defined our listbox base class (Scrollbox), we need to change our listbox types to Scrollbox.
# See LINE_1, LINE_2 and LINE_3


# CHANGE_37

# We should also add a condition so that the main code is not executed with modules imported by another program
# That will let other modules to use the scrollbox and Datalistbox classes
# We put the if__name__ == '__main__', then add connection, then indent there rest of the code under if__name__


if __name__ == '__main__':
    conn = sqlite3.connect('music.db',)

    # Indent this code

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
    # albumList.requery()  # CHANGE_25. add this requery. Comment this out under CHANGE_37
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
    # songList.requery()  # CHANGE_27. comment this out under CHANGE_37
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

    # Comment these two lines out under CHANGE_37

    # testList = range(0, 100)
    # albumLV.set(tuple(testList))  # we pass a tuple with numbers from 0 to 100. similar to tuple in TESTLINE above

    mainWindow.mainloop()
    print("Closing database connection")
    conn.close()

