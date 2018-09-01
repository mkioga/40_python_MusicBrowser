
# =======================
# star_args.py
# =======================

# =======
# *args
# =======

# NOTE: Below command will not work if you are running python 2
# If running python 2, you can import print module from python 3 (future)
# from __future__ import print_function
# But in our case, we have python 3, so it runs fine.

# In this code, we are calling print function and passing two (or more) strings to it

# print("Hello", "Dear", "World")


# If we do CTRL + click print, we get the print built in below

#  def print(self, *args, sep=' ', end='\n', file=None):

# We can see the print function takes the *args parameter that lets it take a variable (many) number of arguments
# so since we have given print function two strings above, it uses the *args parameter to take the unpacked
# string values in that tuple i.e. Hello, Dear, World
# args itself is a tuple, so print function iterates through all the values of the tuple and prints them all
# the star (*) in front of "args" unpacks the passed tuple

# We will test *args below to see how it works in calculating averages
# NOTE: if using python 2, do: from __future__ import division

# NOTE that "def average(*args)" with (*args) tells the function "average" to expect an unpacked tuple e.g. average(1, 2, 3, 4)
# then the values will be packed into a parameter called args.

# print("="*30)
#
# def average(*args):  # *args represents the unpacked tuple which we will provide when calling it.
#     print(type(args))  # Checks what type args is. Should be a tuple
#     print("args is {}".format(args))  # prints the contents of args (without star). Prints tuple enclosed in ( )
#     print("*args is:", *args)  # prints contents of *args tuple (with star). prints the four values i.e. * unpacked the args tuple
#     mean = 0
#     for arg in args:
#         mean += arg
#     return mean / len(args)  # returns the average
#
# # Now we call the function average and give it parameters
#
# print("Average:")
# print(average(1, 2, 3, 4))  # we pass four arguments as unpacked tuple

# ================================================================
# in code below, we pass (args) without * to def average.
# This means that def average expects to be passed a tuple, which is enclosed in extra ( )


# print("="*20)
#
# def average(args):  # args (without *) represents the tuple which we will provide when calling it.
#     print(type(args))  # Checks what type args is. Should be a tuple
#     print("args is {}".format(args))  # prints the contents of args (without star). Prints tuple enclosed in ( )
#     print("*args is:", *args)  # prints contents of *args tuple (with star). prints the four values i.e. * unpacked the args tuple
#     mean = 0
#     for arg in args:
#         mean += arg
#     return mean / len(args)  # returns the average
#
# # Now we call the function average and give it parameters
#
# print("Average:")
# print(average((1, 2, 3, 4)))  # we pass four arguments as a tuple. NOTE: need to be enclosed in extra ( ) to be tuple




# =============================================
# *args challenge
# =============================================

# write a function called build_tuple that takes a variable number of arguments,
# and returns a tuple containing the values passed to it.

# print("="*20)
#
# def build_tuple(*args):  # takes unpacked tuple
#     return args  # returns the packed tuple
#
# message_tuple = build_tuple("hello", "planet", "earth", "take", "me", "to", "your", "leader")
# print(type(message_tuple))
# print(message_tuple)
#
# number_tuple = build_tuple(1, 2, 3, 4, 5, 6)
# print(type(number_tuple))
# print(number_tuple)


# for more documentation on *args, see link below
# https://docs.python.org/3/tutorial/controlflow.html#more-on-defining-functions



# ==============================================
# **kwargs (Keyword arguments)
# ===============================================

# **kwargs is another way of specifying parameters
# it works in the same way as packing a variable number of elements of arguments into a tuple
# but this time we need to pack a variable number of "named arguments" or "keyword arguments"


# print("Hello world")


# if you CTRL + click on print, we get
#  def print(self, *args, sep=' ', end='\n', file=None):

# we sometimes modify sep= '--' to separate with --, or end=' ' to end in space instead of newline,
# or file="filename" instead of None to print to a file
# These three (sep, end, file) are examples of keyword arguments.
# Until now, we have seen keyword arguments that have default values e.g. sep=' ' end='\n' and file=None

# Sometimes we don't want to use the default values of these keyword arguments
# e.g. in code below where we print backwards

# print("="*20)
# print("Printing backwards:")
#
# def print_backwards(*args):
#     for word in args[::-1]:  # NOTE that [::-1] is to read backwards
#         print(word[::-1], end=' ')  # we print backwards and modify end to be ' ' instead of '\n'
#
# # Then we call print_backwards and give it unpacked tuple comprising of strings
# # This commmand prints backwards and gives result: "redael ruoy ot em ekat htrae tenalp olleh "
#
# print_backwards("hello", "planet", "earth", "take", "me", "to", "your", "leader")

# Above is a modified version of the print function.
# We would like it to behave the same as the print function
# for example, we can write the results to a file named "backwards_file"


#
# print("="*20)
# print("Printing to file named backward_file:")
#
# def print_backwards(*args, file=None):  # we introduce file and give it default or None
#     for word in args[::-1]:  # NOTE that [::-1] is to read backwards
#         print(word[::-1], end=' ', file=file)  # we add file=file here to print to passed filename
#
# # this is the code to write to backwards_file.txt
#
# with open("backwards_file.txt", 'w') as backwards_file:
#     print_backwards("hello", "planet", "earth", "take", "me", "to", "your", "leader", file=backwards_file)  # we add file backward_file
#

# When you run above code, it creates a file named "backwards_file.txt and writes reverse results to it.
# That worked fine. But we know that print function only defines three parameters that we can use
# def print(self, *args, sep=' ', end='\n', file=None):

# In the case of listbox class for example, there are a lot of named arguments that we can provide when creating a new listbox
# Things like background, font, hightlight color, hightlight thickness etc
# There are about 22 named parameters that we would have to match in our init method if we want to provide all the same options

# Instead of worrying about all the parameters in classes, we can use **kwargs
# we know that the asterix (*) can be used to unpack a tuple or list
# Then Double Asterix (* * ) unpacks a dictionary.

# A dictionary is used because "keyword arguments" are specified as a "keyword" and a "value".
# And we know that a dictionary comprises a "keyword or key" and a "value"

# This means we can get all the keyword arguments and pass all of them to the print function
# Here is an example of using **kwargs in above code

# We will replace file=None with **kwargs
# And then under print, replace file=file with **kwargs

# When we run this code, we successfully create backwards_file2.txt with same output as above code

# ADVANTAGE of this is that in the calling code, we are free to add as many keywords as print will accept
# and we don't need to worry about what they are or what their default values are.
# So if print function changes in future and adds keyword values, our code will work just fine.

# NOTE that we can call the parameter anything, but the convention is to call it kwargs

# NOTE: when we do print(kwargs), it shows:
# "{'file': <_io.TextIOWrapper name='backwards_file2.txt' mode='w' encoding='cp1252'>}"

# we see that kwargs is a dictionary. It's keyword is: "file" and value is: <_io.TextIOWrapper name='backwards_file2.txt' mode='w' encoding='cp1252'>}


# print("="*20)
# print("Printing to file named backward_file using **kwargs:")
#
# def print_backwards(*args, **kwargs):  # replace file=None with **kwargs
#     print(kwargs)  # This print shows what is in the kwargs
#     for word in args[::-1]:  # NOTE that [::-1] is to read backwards
#         print(word[::-1], end=' ', **kwargs)  # Replace file=file with **kwargs
#
# # this is the code to write to backwards_file.txt
#
# with open("backwards_file2.txt", 'w') as backwards_file:
#     print_backwards("hello", "planet", "earth", "take", "me", "to", "your", "leader", file=backwards_file)  # we add file backward_file
#



# =============================================
# More on KWargs - Multiple keyword arguments
# =============================================

# In this code, LINE_1 - "print(word[::-1], end=' ', **kwargs)" has end=' '
# If on LINE_2 when calling the print_backwards function, we specify end='\n', which is a valid thing to do
# We get an error message: TypeError: print() got multiple values for keyword argument 'end'
# This is because LINE_1 has end=' ' and then on LINE_2, you provide end='\n', and it is not allowed to have multiple values for keyword argument

# We can fix the print_backwards function so that it correctly handles the case when the calling code also specifies the end keyword argument.

#
# print("="*20)
# print("Printing to file named backward_file using **kwargs:")
#
# def print_backwards(*args, **kwargs):  # replace file=None with **kwargs
#     print(kwargs)  # This print shows what is in the kwargs
#     for word in args[::-1]:  # NOTE that [::-1] is to read backwards
#         print(word[::-1], end=' ', **kwargs)  # Replace file=file with **kwargs:  LINE_1
#
# # this is the code to write to backwards_file.txt
#
# with open("backwards_file3.txt", 'w') as backwards_file:
#     print_backwards("hello", "planet", "earth", "take", "me", "to", "your", "leader", file=backwards_file, end='\n')  # LINE_2: we add end='\n'


# SOLUTION 1:
# ============
# Both of the solutions rely on making sure that we don't pass the end keyword argument in kwargs
# One approach is to include "end" in our parameter list, before the **kwargs: LINE_3
# NOTE that just like *args, **kwargs will check the remaining arguments that we don't specify in our function definition
# So in this case, **kwargs does not take end=' '  because it is already specified in the function definition before **kwargs

# NOTE: there is a slight difference between *args and **kwargs
# *args deals with positional arguments, they don't have names, so they just appear in order in the function call
# **kwargs uses parameter names, so it does not care what order we specify them in when calling the function
#  it just scoops up any that our function has not declared and puts them into kwargs

# NOTE: we will remove the "file=backwards_file" on LINE_2, so we can see the results on the screen and not on txt file
# We can see that this code now runs fine.


# print("="*20)
# print("Printing to file named backward_file using **kwargs:")
#
# def print_backwards(*args, end=' ', **kwargs):  # replace file=None with **kwargs. LINE_3: we include end=' ' in parameter list
#     print(kwargs)  # This print shows what is in the kwargs
#     for word in args[::-1]:  # NOTE that [::-1] is to read backwards
#         print(word[::-1], end=' ', **kwargs)  # Replace file=file with **kwargs:  LINE_1
#
# # this is the code to write to backwards_file.txt
#
# with open("backwards_file3.txt", 'w') as backwards_file:
#     print_backwards("hello", "planet", "earth", "take", "me", "to", "your", "leader", end='\n')  # LINE_2: we add end='\n'
#
#


# SOLUTION 2:
# ============
# The other approach is to remove any "end" keyword arguments from the kwargs dictionary before passing it on to the built-in print function
# On LINE_3, we remove the end=' '
# We know that kwargs is a dictionary, so we can manipulate its contents.
# In this case we will pop out "end" on LINE_4 and provide it with default or None
# we use the dictionary pop method. if you click the pop section, it shows

# When we run this code, we see that kwargs before pop = {'end': '\n'}: and kwargs after pop = {}:
# After end is popped out of kwargs, then you can call print_backwards function and give it end='\n'
# and there will be no error because there will be no multiple occurances of end keywords

# This code now works in resolving error if you pass end='\n'

#
# print("="*20)
# print("Printing to file named backward_file using **kwargs:")
#
# def print_backwards(*args, **kwargs):  # LINE_3: we remove the end=' ' from here
#     print("kwargs before pop = {}:".format(kwargs))  # This print shows what is in the kwargs before pop
#     kwargs.pop('end', None)  # LINE_4:
#     print("kwargs after pop  = {}:".format(kwargs))  # This print shows what is in the kwargs before pop
#     for word in args[::-1]:  # NOTE that [::-1] is to read backwards
#         print(word[::-1], end=' ', **kwargs)  # Replace file=file with **kwargs:  LINE_1
#
# # this is the code to write to backwards_file.txt
#
# with open("backwards_file3.txt", 'w') as backwards_file:
#     print_backwards("hello", "planet", "earth", "take", "me", "to", "your", "leader", end='\n')  # LINE_2: we add end='\n'
#


# Those two solutions above show how to manipulate kwargs by either
# (1) manipulating the keyword in your own definition
# (2) or explicitly removing it from the dictionary


# ========================================================================

# Our print_backwards function works but it does not really behave like the built in print function
# We can see that even if LINE_2 has end='\n', LINE_5 is not being printed on a new line.
# so we are effectively using end=' ' argument on LINE_1 as a separator because we are using multiple
# calls to the built in print function inside our loop, we have to use end=' ' to avoid having each word
# appearing on a new line
# If we specify "sep" (separator) when callng our print function, it will not do anything.
# in the built in print function, sep is used as separator, but in our print_backwards function, end=' ' is used as separator

#
# print("="*20)
# print("Printing to file named backward_file using **kwargs:")
#
# def print_backwards(*args, **kwargs):  # LINE_3: we remove the end=' ' from here
#     print("kwargs before pop = {}:".format(kwargs))  # This print shows what is in the kwargs before pop
#     kwargs.pop('end', None)  # LINE_4:
#     print("kwargs after pop  = {}:".format(kwargs))  # This print shows what is in the kwargs before pop
#     for word in args[::-1]:  # NOTE that [::-1] is to read backwards
#         print(word[::-1], end=' ', **kwargs)  # Replace file=file with **kwargs:  LINE_1
#
# # this is the code to write to backwards_file.txt
#
# with open("backwards_file3.txt", 'w') as backwards_file:
#     print_backwards("hello", "planet", "earth", "take", "me", "to", "your", "leader", end='\n')  # LINE_2: we add end='\n'
#     print("LINE_5 should be on a new line")  # LINE_5: should be on newline but it is not
#
# # We see that LINE_5 separates with sep='|' while LINE_6 separates with spaces (end=' ')
#
# print("="*15)
# print("adding sep to built in print:")
# print("hello", "planet", "earth", "take", "me", "to", "your", "leader", end='\n', sep='|')  # LINE_5
# print("adding sep to print_backwards:")
# print_backwards("hello", "planet", "earth", "take", "me", "to", "your", "leader", end='\n', sep='|')  # LINE_6


# from above demonstration, we see that kwargs is very useful but we need to be careful that we don't subvert the
# meaning of the arguments that we are passing on e.g. above where we want a separator of | and we end up getting space

# We could fix this by joining the reverse words up into a string using a single call to the built in print function.
# That is the recommended way because code would end up being cleaner and it would be obvious what is going on.

# But this course is about using *args and **kwargs, so we will manipulate the keyword arguments to resolve the issue.
# You may find yourself having to do this when subclassing another class so its useful to know how to do it.

# SOLUTION:
# We will use any "sep" argument that the calling code provides instead of hardcoding end=' '
# which it is currently doing on LINE_1.
# Then we will add a final print call using whatever "end" value has been provided.

# Changes we make are:
# LINE_7 & LINE_8 where we define end and sep characters. which pops them from kwargs
# LINE_1, where we make end to be sep_character instead of space.
# LINE_9, we print the end character.

# when we run this code, we see that print_backwards now uses | as separator
#
# print("="*20)
# print("Printing to file named backward_file using **kwargs:")
#
# def print_backwards(*args, **kwargs):  # LINE_3: we remove the end=' ' from here
#     print("kwargs before pop = {}".format(kwargs))  # default in kwargs before pop = end='\n' and sep='|'
#
#     end_character = kwargs.pop('end', '\n')  # LINE_7. end_character is newline. we pop it from kwargs
#     sep_character = kwargs.pop('sep', ' ')   # LINE_8. sep_character is | . we pop it from kwargs
#
#     print("end_character = {}".format(end_character))  # print shows end_character is newline
#     print("sep_character = {}".format(sep_character))  # print shows sep_character is |
#     print("="*5)
#     print("kwargs after pop  = {}".format(kwargs))  # print shows that empty since "end" and "sep" are popped.
#     print("="*5)
#     for word in args[::-1]:  # NOTE that [::-1] is to read backwards
#         print(word[::-1], end=sep_character, **kwargs)  # Replace file=file with **kwargs:  LINE_1. We make end=sep_character to make it separator
#     print('\n')
#     print(end=end_character)  # LINE_9; we print the end_character which is a newline
#
#
# # this is the code to write to backwards_file.txt
#
# with open("backwards_file3.txt", 'w') as backwards_file:
#     print_backwards("hello", "planet", "earth", "take", "me", "to", "your", "leader", end='\n')  # LINE_2: we add end='\n'
#     print("LINE_5 should be on a new line")  # LINE_5: should be on newline but it is not
#
# # We see that LINE_5 separates with sep='|' while LINE_6 separates with spaces (end=' ')
#
# print("="*15)
# print("Results of builtin print:")
# print("hello", "planet", "earth", "take", "me", "to", "your", "leader", end='\n', sep='|')  # LINE_5
# print("== dash after print ==")
# print("Results of print_backwards:")
# print_backwards("hello", "planet", "earth", "take", "me", "to", "your", "leader", end='\n', sep='|')  # LINE_6
# print("== dash after print_backwards ==")


# ===============================================

# Above code for print_backwards works almost exactly as the inbuilt print function
# It also works if we suppress the end of line character: end='\n' and make it end=''. # we will do this on LINE_5 and LINE_6
# We will also modify separator to be sep='\n**\n' on LINE_5 and LINE_6

# When your run the code, we see that the first word of "print_backwards" function starts on the same line as
# the last word on the "print" function i.e. leaderredael which is leader and and leader backwards
# but then the ==== line prints in a new line after the "print_backwards function.
# This means the end='' under print is suppressed but one under print_backwards is not.
# We can fix this to make print_backwards behave similar to print as shown in following section



# print("="*20)
# # print("Printing to file named backward_file using **kwargs:")
#
# def print_backwards(*args, **kwargs):  # LINE_3: we remove the end=' ' from here
#     # print("kwargs before pop = {}".format(kwargs))  # default in kwargs before pop = end='\n' and sep='|'
#
#     end_character = kwargs.pop('end', '\n')  # LINE_7. end_character is newline. we pop it from kwargs
#     sep_character = kwargs.pop('sep', ' ')   # LINE_8. sep_character is | . we pop it from kwargs
#
#     # print("end_character = {}".format(end_character))  # print shows end_character is newline
#     # print("sep_character = {}".format(sep_character))  # print shows sep_character is |
#     # print("="*5)
#     # print("kwargs after pop  = {}".format(kwargs))  # print shows that empty since "end" and "sep" are popped.
#    #  print("="*5)
#     for word in args[::-1]:  # NOTE that [::-1] is to read backwards
#         print(word[::-1], end=sep_character, **kwargs)  # Replace file=file with **kwargs:  LINE_1. We make end=sep_character to make it separator
#     print(end=end_character)  # LINE_9; we print the end_character which is a newline
#
#
# # this is the code to write to backwards_file.txt
#
# with open("backwards_file3.txt", 'w') as backwards_file:
#     print_backwards("hello", "planet", "earth", "take", "me", "to", "your", "leader", end='\n')  # LINE_2: we add end='\n'
#     print("another string")
#
# # We see that LINE_5 separates with sep='|' while LINE_6 separates with spaces (end=' ')
#
# print("="*15)
# # print("Results of builtin print:")
# print("hello", "planet", "earth", "take", "me", "to", "your", "leader", end='', sep='\n**\n')  # LINE_5
# # print("== dash after print ==")
# # print("Results of print_backwards:")
# print_backwards("hello", "planet", "earth", "take", "me", "to", "your", "leader", end='', sep='\n**\n')  # LINE_6
# print("====")


# ==========================================
# Making print_backwards behave like print:
# ==========================================

# One solution to this is to handle the last word differently so it goes to a new line.
# the last word should be printed using the specified end argument: end='', rather than the separator: sep='\n**\n'
# We do this by altering the range so that it reads the words backwards but stops before it reads the last one
# which in this case is "hello" (first one) because we are going backwards.
# then we print this first word in args (hello), separately using the end value that the calling code specified i.e. end=''

# So we change the range in LINE_10 and then print the first word separately in LINE_11
# When we run this code, we now see that end='' is also suppressed in print_backwards because last output is olleh====
# Which means there is no newline between olleh and ====, hence newline suppression is working.


#
# print("="*20)
# # print("Printing to file named backward_file using **kwargs:")
#
# def print_backwards(*args, **kwargs):  # LINE_3: we remove the end=' ' from here
#     # print("kwargs before pop = {}".format(kwargs))  # default in kwargs before pop = end='\n' and sep='|'
#
#     end_character = kwargs.pop('end', '\n')  # LINE_7. end_character is newline. we pop it from kwargs
#     sep_character = kwargs.pop('sep', ' ')   # LINE_8. sep_character is | . we pop it from kwargs
#
#     # print("end_character = {}".format(end_character))  # print shows end_character is newline
#     # print("sep_character = {}".format(sep_character))  # print shows sep_character is |
#     # print("="*5)
#     # print("kwargs after pop  = {}".format(kwargs))  # print shows that empty since "end" and "sep" are popped.
#     #  print("="*5)
#     # for word in args[::-1]:  # NOTE that [::-1] is to read backwards
#     for word in args[:0:-1]:  # LINE_10, We change range here. includes up to but not including the stop value.
#         print(word[::-1], end=sep_character, **kwargs)  # Replace file=file with **kwargs:  LINE_1. We make end=sep_character to make it separator
#     print(args[0][::-1], end=end_character, **kwargs)   # LINE_11, print first word separately
#     # print(end=end_character)  # LINE_9; we print the end_character which is a newline
#
#
# # this is the code to write to backwards_file.txt
#
# with open("backwards_file3.txt", 'w') as backwards_file:
#     print_backwards("hello", "planet", "earth", "take", "me", "to", "your", "leader", end='\n')  # LINE_2: we add end='\n'
#     print("another string")
#
# # We see that LINE_5 separates with sep='|' while LINE_6 separates with spaces (end=' ')
#
# print("="*15)
# # print("Results of builtin print:")
# print("hello", "planet", "earth", "take", "me", "to", "your", "leader", end='', sep='\n**\n')  # LINE_5
# # print("== dash after print ==")
# # print("Results of print_backwards:")
# print_backwards("hello", "planet", "earth", "take", "me", "to", "your", "leader", end='', sep='\n**\n')  # LINE_6
# print("====")




# All above examples showed how to manipulate kwargs functions and still retain the bahavior of the original function.

# ==================================================

# A simpler way you can use to print backwards is as follows
# NOTE that this uses "list comprehension" which we will study later in the course.


def backwards_print(*args, **kwargs):
    sep_character = kwargs.pop('sep', ' ')
    print(sep_character.join(word[::-1] for word in args[::-1]), **kwargs)


print("="*15)
# print("Results of builtin print:")
print("hello", "planet", "earth", "take", "me", "to", "your", "leader", end='', sep='\n**\n')  # LINE_5
# print("== dash after print ==")
# print("Results of print_backwards:")
backwards_print("hello", "planet", "earth", "take", "me", "to", "your", "leader", end='', sep='\n**\n')  # LINE_6
print("====")

# ===============================================================================
# Now that we understand kwargs, we will go to jukebox2.py and create scrollbox
# ===============================================================================