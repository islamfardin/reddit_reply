"""Program to get reddit replies. Uses praw to web scrape reddit, tkinter for
gui, and pandas for csv/json export
"""
from tkinter import Tk, Label, StringVar, W, Entry, END, Button
import praw
import pandas as pd

#-----------------------------GUI PART-----------------------------#

# GUI customization
root = Tk() #initializing gui
root.title("Reddit Replies") # title
root.geometry("550x250") # size of textbox

# label customization
url_path = Label(root, text="URL", pady=20)#.place(x=5, y=3)
url_path.grid(row=0, column=0, sticky=W)
redditor_name = Label(root, text="Redditor")#.place(x=5, y=28)
redditor_name.grid(row=1, column=0, sticky=W)

# input box customization
path_text = StringVar()
url_entry = Entry(root, width=50, textvariable=path_text) # the two entry boxes
url_entry.grid(row=0, column=1)

name_text = StringVar()
name_entry = Entry(root, width=50, textvariable=name_text)
name_entry.grid(row=1, column=1)

GIVEN_URL=''
GIVEN_NAME=''

def func_1():
    """ declaring the user given url as global var,
    storing in separate functions"""
    global GIVEN_URL
    GIVEN_URL = url_entry.get()

def func_2():
    """ declaring the user given name as global var,
    storing in separate functions"""
    global GIVEN_NAME
    GIVEN_NAME = name_entry.get()

def get_info():
    """calling to the function that will use the given info to find reddit replies
    dsdsd"""
    func_1()
    func_2()
    get_text(GIVEN_URL,GIVEN_NAME)

def delete():
    """button to delete user input"""
    url_entry.delete(0, END)
    name_entry.delete(0, END)

but_1 = Button(root, text="Submit", height=2, width=10, fg='Green', font='14', command=get_info)
but_1.grid(row=2, column=1, pady=10)
but_2 = Button(root, text="Delete", height=2, width=10, fg='Red', font='14', command=delete)
but_2.grid(row=3, column=1)

#---------------------GETTING REDDIT REPLIES---------------------#

reply_dict = {"Redditor": [], "Reply": []} # dictionary to save redditor name and their reply

# id, secret, and agent can be found https://old.reddit.com/prefs/apps/
reddit = praw.Reddit(client_id=" ",
                               client_secret=" ",
                               user_agent=" ")

def get_text(get_url, get_redditor):
    """
    Takes in the user given url and name and checks if replies exist for that name.
    Loops over all of the replies in the post that matches the name and saves to a
    pandas df. Passes it to another function to display on gui
    """
    submission = reddit.submission(url=get_url)

    submission.comments.replace_more(limit=0) # replace_more loads more reply comments
    for comment in submission.comments:

        if len(comment.replies) > 0: # makes sure comment has replies

            for reply in comment.replies:

                if reply.author.name==get_redditor and reply.author.name is not None:

                    reply_dict["Redditor"].append(reply.author.name) # appending info to dictionary
                    reply_dict["Reply"].append(reply.body)

    df_text = pd.DataFrame(reply_dict) # saving text to a pandas df
    df_text = df_text.replace('\n', '', regex=True) # getting rid of \n lines
    df_text.index+=1 # start index at 1 instead of 0
    gui_result(df_text)

def gui_result(text):
    """
    displays redditor name and their replies to gui
    """
    but_1.grid_forget()
    but_2.grid_forget() # deleting the buttons and the insert boxes

    label_text = Label(root, text = str(text)) # prints directly to the GUI
    label_text.grid(row=3, column=1)

root.mainloop()
