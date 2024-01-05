import sqlite3
from CTkMessagebox import CTkMessagebox
from tkinter import messagebox

def success_added(master):
    ok=CTkMessagebox(master,title='Book added',message='Το βιβλίο προστέθηκε',icon='info')
    if ok.get():
        master.destroy()


def create_db():
    con=sqlite3.connect("book_library.db")
    create_table_books='''CREATE TABLE IF NOT EXISTS books(
    title TEXT,
    description TEXT,
    category TEXT,
    isbn TEXT PRIMARY KEY,
    author TEXT,
    book_owner TEXT,
    path TEXT
    )'''
    con.execute(create_table_books)
    con.close()
    
def show_error(error):
    CTkMessagebox(title="Error",message=f'{error} is required',icon="cancel")
    

