import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
from settings import *
from controller import create_db, show_error, success_added
import sqlite3
import os
from PIL import Image, ImageTk


book_columns=("Title","Author","Category","isbn")

def select_record():
    global selected, cover
    selected=App.treeview.focus()
    App.selected_item=App.treeview.item(selected, 'values')
    isbn=App.selected_item[3]
    item=item_fetch(isbn)   #data της βάσης

    App.detail_title.set(item[0])   #title
    App.detail_description.set(item[1]) #Description
    App.detail_author.set(item[2])  #Author
    App.detail_category.set(item[3])  #Category
    App.detail_isbn.set(item[4])  #isbn

    path=os.path.dirname(__file__)
    image=os.path.join(path,'images',item[6])
    image1=Image.open(image)
    cover=ctk.CTkImage(image1)

def detail_cover(event):
    tree = event.widget
    selected=tree.focus()
    if selected:
        selection = tree.item(selected, 'values')
        isbn=selection[3]
        item=item_fetch(isbn)   #data της βάσης

        path=os.path.dirname(__file__)
        image=os.path.join(path,'images',item[6])
        image1=Image.open(image)

        ratio=image1.height/image1.width
        image_width=int(App.details_pic.winfo_width())-30
        image_height=int(ratio*App.details_pic.winfo_width())

        cover=ctk.CTkImage(image1, size=(image_width , image_height))

        App.d_cover=ctk.CTkLabel(App.details_pic,text='', image=cover)
        App.d_cover.grid(row=0,column=0,sticky="news")

def details_view(parent):
    #title
        parent.d_label_title=ctk.CTkLabel(parent,text="Title:", font=(FONT_FAMILY,FONT_SIZE, 'bold'))
        parent.d_label_title.pack(padx=10,pady=5,anchor="sw")
        App.detail_title=tk.StringVar()
        parent.d_title=ctk.CTkLabel(parent,text='',font=(FONT_FAMILY,FONT_SIZE,), textvariable=App.detail_title,anchor='w')
        parent.d_title.pack(padx=10,pady=10,anchor="sw")
        #description
        parent.d_label_description=ctk.CTkLabel(parent,text="Description:", font=(FONT_FAMILY,FONT_SIZE, 'bold'))
        parent.d_label_description.pack(padx=10,pady=5,anchor="sw")
        App.detail_description=tk.StringVar()
        parent.update_idletasks() # to update  window size atributes
  
        parent.d_label_description=ctk.CTkLabel(parent,text='test',font=(FONT_FAMILY,FONT_SIZE), textvariable=App.detail_description, wraplength=parent.winfo_width(),anchor='w', justify="left")
        parent.d_label_description.pack(padx=10,pady=10,fill='x',anchor="sw")
            #Αυτόματη αλλαγή του πλατους του description αναλογα με το πλάτος του παραθύρου, κόβει τις λέξεις
        parent.d_label_description.bind('<Configure>', lambda e: parent.d_label_description.configure(wraplength=parent.d_label_description.winfo_width()))
        #author
        parent.d_label_author=ctk.CTkLabel(parent,text="Author:", font=(FONT_FAMILY,FONT_SIZE, 'bold'))
        parent.d_label_author.pack(padx=10,pady=5,anchor="sw")
        App.detail_author=tk.StringVar()
        parent.d_author=ctk.CTkLabel(parent,text='',font=(FONT_FAMILY,FONT_SIZE,), textvariable=App.detail_author,anchor='w')
        parent.d_author.pack(padx=10,pady=10,anchor="sw")
        #Category
        parent.d_label_category=ctk.CTkLabel(parent,text="Category:", font=(FONT_FAMILY,FONT_SIZE, 'bold'))
        parent.d_label_category.pack(padx=10,pady=5,anchor="sw")
        App.detail_category=tk.StringVar()
        parent.d_category=ctk.CTkLabel(parent,text='',font=(FONT_FAMILY,FONT_SIZE,), textvariable=App.detail_category,anchor='w')
        parent.d_category.pack(padx=10,pady=10,anchor="sw")
        #ISBN
        parent.d_label_isbn=ctk.CTkLabel(parent,text="ISBN:", font=(FONT_FAMILY,FONT_SIZE, 'bold'))
        parent.d_label_isbn.pack(padx=10,pady=5,anchor="sw")
        App.detail_isbn=tk.StringVar()
        parent.d_isbn=ctk.CTkLabel(parent,text='',font=(FONT_FAMILY,FONT_SIZE,), textvariable=App.detail_isbn,anchor='w')
        parent.d_isbn.pack(padx=10,pady=10,anchor="sw")
        #Cover
        App.details_pic.rowconfigure(0,weight=1,uniform="a")
        App.details_pic.columnconfigure(0,weight=1,uniform="a")
        App.treeview.bind('<<TreeviewSelect>>', detail_cover)

def add_book(self,title, description,category,isbn,author,book_owner,image):
    con=sqlite3.connect("book_library.db")
    if title=="":show_error("title")
    if isbn=="":show_error("isbn")
    if title!="" and isbn!="":
        try:
            sql_book='''INSERT INTO books
            (title,description,category,isbn,author,book_owner,path)
            VALUES(?,?,?,?,?,?,?)'''
            cursor=con.cursor()
            cursor.execute(sql_book,(title, description,category,isbn,author,book_owner,image))
            con.commit()
            con.close()
            App.treeview.delete(*App.treeview.get_children())
            data=data_fetch_all()
            App.treeview=create_treeview(App.tree_frame, book_columns, data)
            App.treeview.bind("<ButtonRelease-1>", lambda e: select_record())
            App.treeview.bind('<<TreeviewSelect>>', detail_cover)
            success_added(self)
        
        except sqlite3.IntegrityError:
            messagebox.showwarning(title='Add Book', message='This ISBN exists',parent=self)
             
def delete_book():
    try:
        selected
        confirm=messagebox.askquestion(title="Delete Book",message="Are you sure?")
        if confirm=="yes":      
            item_to_delete=App.selected_item[3]
            App.treeview.delete(selected)  
            con=sqlite3.Connection('book_library.db')
            cur=con.cursor()
            sql_query="DELETE FROM books WHERE isbn = ?"
            cur.execute(sql_query,(item_to_delete,))
            con.commit()
            con.close()
    except:
        messagebox.showinfo(title="Edit Book",message="You must select a book first") 

def item_fetch(isbn):

    conn=sqlite3.connect('book_library.db')
    cur=conn.cursor()
    query="SELECT * FROM books WHERE isbn = ?"
    results=cur.execute(query,(isbn,))
    item=results.fetchone()
    conn.close()
    return item 

def data_fetch_all():
    conn=sqlite3.connect('book_library.db')
    cur=conn.cursor()
    data_query='''SELECT * FROM books'''
    results=cur.execute(data_query)
    data=results.fetchall()
    conn.close()
    return data 

def open_image(self,width):
    global filename
    list=self.grid_slaves()
    for l in list:
        l.destroy()

    self.rowconfigure(0,weight=1,uniform="a")
    self.columnconfigure(0,weight=1,uniform="a")
    file=filedialog.askopenfile(parent=self,filetypes=IMAGE_FORMATS).name
    filename=os.path.basename(file)
    image1=Image.open(file)
    ratio=image1.height/image1.width
    image_width=int(width)-10
    image_height=int(ratio*width)
    image2=ctk.CTkImage(image1, size=(image_width , image_height))
    #Add image in label
    image_label=ctk.CTkLabel(self,
                             text="",
                             image=image2,
                             )
    image_label.grid(row=0,column=0,sticky="ew")

def create_treeview(parent,book_columns,data):
    tree=Tree(parent,book_columns,data)
    tree.place(relx=0.01,rely=0.01,relheight=1,relwidth=0.78)
    vsb=ttk.Scrollbar(tree,orient='vertical',command=tree.yview)
    vsb.place(relx=1,rely=0,relheight=1,anchor='ne')
    tree.configure(yscrollcommand=vsb.set)
    ttk.Style().configure("Vertical.TScrollbar", background=BUTTON_COLOUR, bordercolor=BUTTON_COLOUR, arrowcolor=BUTTON_COLOUR, arrowsize=ARROWSIZE)
    
    return tree

def edit_book(parent):

    try:
        selected
        if App.oef==None or not App.oef.winfo_exists(): #αν δεν υπαρχει ανοιχτό παράθυρο ήδη
            App.oef=Edit_Book_form(parent, selected)
            
            App.treeview.delete(*App.treeview.get_children())
            data=data_fetch_all()
            App.treeview=create_treeview(App.tree_frame, book_columns, data)
         
    except NameError: 
        messagebox.showinfo(title="Edit Book",message="You must select a book first")

def edit_book_db(self,title, description,category,isbn,author,book_owner,image):
    con=sqlite3.connect("book_library.db")
    item_to_edit=App.selected_item[3]
    if title=="":show_error("title")
    if isbn=="":show_error("isbn")
    if title!="" and isbn!="":
        sql_book_update='''UPDATE books
        SET
            title=?,
            description=?,
            category=?,
            isbn=?,
            author=?,
            book_owner=?,
            path=?
        WHERE isbn=?'''
        cursor=con.cursor()
        cursor.execute(sql_book_update,(title, description,category,isbn,author,book_owner,image, item_to_edit))
        con.commit()
        con.close()
        
        App.treeview.delete(*App.treeview.get_children())
        data=data_fetch_all()
        App.treeview=create_treeview(App.tree_frame, book_columns, data)
        
        list=App.details_pic.grid_slaves()
        for l in list:
            l.destroy()

        path=os.path.dirname(__file__)
        image_1=os.path.join(path,'images',image)
        image1=Image.open(image_1)
        ratio=image1.height/image1.width
        image_width=int(App.details_pic.winfo_width())-30
        image_height=int(ratio*App.details_pic.winfo_width())

        cover=ctk.CTkImage(image1, size=(image_width , image_height))

        App.d_cover=ctk.CTkLabel(App.details_pic,text='', image=cover)
        App.d_cover.grid(row=0,column=0,sticky="news")

        App.treeview.bind("<ButtonRelease-1>", lambda e: select_record())
        App.treeview.bind('<<TreeviewSelect>>', detail_cover)

        success_added(self)

class Edit_Book_form(ctk.CTkToplevel):

    def __init__(self,my_parent, selected):
        super().__init__(master=my_parent)
        self._set_appearance_mode(APPEARANCE_MODE)
        self.title("Edit book")
        self.geometry(BOOK_FORM_GEO)
        self.resizable(False,False)

        self.selected=selected
        self.selected_item=App.treeview.item(self.selected, 'values')
        self.isbn=App.selected_item[3]
        self.item=item_fetch(self.isbn)   #data της βάσης

        #Labels_Frames
        self.left_lFrame=tk.LabelFrame(self,background=L_FRAME_COLOUR,foreground=TEXT_COLOUR,text="Book's Cover")
        self.left_lFrame.place(relx=0,rely=0,relwidth=0.30,relheight=1)
        self.right_lFrame=tk.LabelFrame(self,background=L_FRAME_COLOUR,foreground=TEXT_COLOUR,text="Book's Info")
        self.right_lFrame.place(relx=0.30,rely=0,relwidth=1,relheight=1)

        #Title/entry
        self.label1=ctk.CTkLabel(self.right_lFrame,text="Title")
        self.label1.pack(padx=10,pady=5,anchor="sw")
        self.title_entry=tk.StringVar()
        self.input_title=ctk.CTkEntry(self.right_lFrame ,width=500,height=2, textvariable=self.title_entry)
        self.input_title.pack(padx=10,pady=2,anchor="nw")
        
        #Description/Textbox
        self.label2=ctk.CTkLabel(self.right_lFrame,text="Description")
        self.label2.pack(padx=10,pady=5,anchor="sw")

        self.input_descr=ctk.CTkTextbox(self.right_lFrame,width=500, height=300)
        self.input_descr.pack(padx=10,pady=2, anchor="nw")
        
        #Category/Entry
        self.label3=ctk.CTkLabel(self.right_lFrame,text="Category")
        self.label3.pack(padx=10,pady=5,anchor="sw")
        self.category_entry=tk.StringVar()
        self.input_category=ctk.CTkEntry(self.right_lFrame ,width=500,height=2, textvariable=self.category_entry)
        self.input_category.pack(padx=10,pady=2,anchor="nw")

        #ISBN/Entry
        self.label4=ctk.CTkLabel(self.right_lFrame,text="ISBN")
        self.label4.pack(padx=10,pady=5,anchor="sw")
        self.isbn_entry=tk.StringVar()
        self.input_isbn=ctk.CTkEntry(self.right_lFrame ,width=300,height=2, textvariable=self.isbn_entry)
        self.input_isbn.pack(padx=10,pady=2,anchor="nw")

        #Author/Entry
        self.label5=ctk.CTkLabel(self.right_lFrame,text="Author")
        self.label5.pack(padx=10,pady=5,anchor="sw")
        self.author_entry=tk.StringVar()
        self.input_author=ctk.CTkEntry(self.right_lFrame ,width=300,height=2, textvariable=self.author_entry)
        self.input_author.pack(padx=10,pady=2,anchor="nw")

        #Book_Owner/Entry
        self.label5=ctk.CTkLabel(self.right_lFrame,text="Book Owner")
        self.label5.pack(padx=10,pady=5,anchor="sw")
        self.input_owner=ctk.CTkComboBox(self.right_lFrame ,width=300,values=["maria","giorgos","nikos"])
        self.input_owner.pack(padx=10,pady=2,anchor="nw")

        #StringVars
        self.title_entry.set(self.item[0])   #title      
        self.input_descr.insert("0.0", self.item[1]) #Description
        self.author_entry.set(self.item[2])  #Author
        self.category_entry.set(self.item[3])  #Category
        self.isbn_entry.set(self.item[4])  #isbn

        #cover
        self.left_lFrame.rowconfigure(0,weight=1,uniform="a")
        self.left_lFrame.columnconfigure(0,weight=1,uniform="a")
        
        path=os.path.dirname(__file__)
        image=os.path.join(path,'images',self.item[6])
        image1=Image.open(image)
        ratio=image1.height/image1.width
        image_width=int(self.left_lFrame.winfo_width())-10
        image_height=int(ratio*image_width)
        image2=ctk.CTkImage(image1, size=(image_width , image_height))

        #Add image in label
        self.image_label=ctk.CTkLabel(self.left_lFrame,
                             text="",
                             image=image2,
                             )
        self.image_label.grid(row=0,column=0,sticky="ew")

        #Buttons
        self.book_button=ctk.CTkButton(self.right_lFrame,text="Book's Image",command=lambda:open_image(self.left_lFrame,self.left_lFrame.winfo_width()))
        self.book_button.pack(padx=20,pady=5,anchor="nw")
        try:
            self.submit_button=ctk.CTkButton(self.right_lFrame,text="Submit", command=lambda:edit_book_db(self,self.input_title.get(),
                                                                                            self.input_descr.get("1.0","end-1c"),
                                                                                            self.input_category.get(),
                                                                                            self.input_isbn.get(),
                                                                                            self.input_author.get(),
                                                                                            self.input_owner.get(),
                                                                                            filename))
        
        
        
        except:

            self.submit_button=ctk.CTkButton(self.right_lFrame,text="Submit", command=lambda:edit_book_db(self,self.input_title.get(),
                                                                                            self.input_descr.get("1.0","end-1c"),
                                                                                            self.input_category.get(),
                                                                                            self.input_isbn.get(),
                                                                                            self.input_author.get(),
                                                                                            self.input_owner.get(),
                                                                                            self.item[6]))
        #todo

        
            
        self.submit_button.pack(pady=5,anchor="center")
        #App.detail_cover
               
class Tree(ttk.Treeview):
    def __init__(self,parent,book_columns,data):
        super().__init__(master=parent,columns=book_columns)
        s=ttk.Style()
        s.configure("Treeview",rowheight=150) #ύψος γραμμων treeview

        self.heading("#1", text="Title")
        self.heading("#2", text="Author")
        self.heading("#3", text="Category")
        self.heading("#4", text="ISBN")
        
        self.images={}
        if data:
            for each_row in data:
                path=os.path.dirname(__file__)
                fullname=os.path.join(path,'images',each_row[6])

                with Image.open(fullname) as img:
                    ratio=img.height/img.width
                    image_width=90
                    image_height=int(ratio*100)
                    image=img.resize((image_width,image_height),Image.ANTIALIAS)
                    photo=ImageTk.PhotoImage(image)
                    self.images[each_row[0]]=photo

                self.insert('','end',iid=data.index(each_row),values=(each_row[0],each_row[2],each_row[3],each_row[4]), image=photo)
              
class Book_form(ctk.CTkToplevel):
    def __init__(self,my_parent):
        super().__init__(master=my_parent)
        self._set_appearance_mode(APPEARANCE_MODE)
        self.title("Add book")
        self.geometry(BOOK_FORM_GEO)
        self.resizable(False,False)

        #Labels_Frames
        self.left_lFrame=tk.LabelFrame(self,background=L_FRAME_COLOUR,foreground=TEXT_COLOUR,text="Book's Cover")
        self.left_lFrame.place(relx=0,rely=0,relwidth=0.30,relheight=1)
        self.right_lFrame=tk.LabelFrame(self,background=L_FRAME_COLOUR,foreground=TEXT_COLOUR,text="Book's Info")
        self.right_lFrame.place(relx=0.30,rely=0,relwidth=1,relheight=1)

        #Title/entry
        self.label1=ctk.CTkLabel(self.right_lFrame,text="Title")
        self.label1.pack(padx=10,pady=5,anchor="sw")
        self.input_title=ctk.CTkEntry(self.right_lFrame ,width=500,height=2)
        self.input_title.pack(padx=10,pady=2,anchor="nw")

        #Description/Textbox
        self.label2=ctk.CTkLabel(self.right_lFrame,text="Description")
        self.label2.pack(padx=10,pady=5,anchor="sw")
        self.input_descr=ctk.CTkTextbox(self.right_lFrame,width=500, height=300)
        self.input_descr.pack(padx=10,pady=2, anchor="nw")
        
        #Category/Entry
        self.label3=ctk.CTkLabel(self.right_lFrame,text="Category")
        self.label3.pack(padx=10,pady=5,anchor="sw")
        self.input_category=ctk.CTkEntry(self.right_lFrame ,width=500,height=2)
        self.input_category.pack(padx=10,pady=2,anchor="nw")

        #ISBN/Entry
        self.label4=ctk.CTkLabel(self.right_lFrame,text="ISBN")
        self.label4.pack(padx=10,pady=5,anchor="sw")
        self.input_isbn=ctk.CTkEntry(self.right_lFrame ,width=300,height=2)
        self.input_isbn.pack(padx=10,pady=2,anchor="nw")

        #Author/Entry
        self.label5=ctk.CTkLabel(self.right_lFrame,text="Author")
        self.label5.pack(padx=10,pady=5,anchor="sw")
        self.input_author=ctk.CTkEntry(self.right_lFrame ,width=300,height=2)
        self.input_author.pack(padx=10,pady=2,anchor="nw")

        #Book_Owner/Entry
        self.label5=ctk.CTkLabel(self.right_lFrame,text="Book Owner")
        self.label5.pack(padx=10,pady=5,anchor="sw")
        self.input_owner=ctk.CTkComboBox(self.right_lFrame ,width=300,values=["maria","giorgos","nikos"])
        self.input_owner.pack(padx=10,pady=2,anchor="nw")

        #Buttons
        self.book_button=ctk.CTkButton(self.right_lFrame,text="Book's Image",command=lambda:open_image(self.left_lFrame,self.left_lFrame.winfo_width()))
        self.book_button.pack(padx=20,pady=5,anchor="nw")

        self.submit_button=ctk.CTkButton(self.right_lFrame,text="Submit", command=lambda:add_book(self,self.input_title.get(),
                                                                                              self.input_descr.get("1.0","end-1c"),
                                                                                              self.input_category.get(),
                                                                                              self.input_isbn.get(),
                                                                                              self.input_author.get(),
                                                                                              self.input_owner.get(),
                                                                                              filename))
        self.submit_button.pack(pady=5,anchor="center")

class App(ctk.CTk):
    
    def __init__(self,title):
        super().__init__()
        self._set_appearance_mode(APPEARANCE_MODE)
        self.title(title)
        self.geometry(INIT_GEOMETRY)
        self.minsize(MIN_WIDTH,MIN_HEIGHT)
        self.obf=None   #open book form
        App.oef=None #open edit form
        create_db() #CREATE_DB
#Frames
    #menu frame
        self.menu_frame=ctk.CTkFrame(self,fg_color=SIDE_FRAME_COLOUR)
        self.menu_frame.place(relx=0,rely=0,relwidth=0.20,relheight=1)
    #main frame
        self.main_frame=ctk.CTkFrame(self)
        self.main_frame.place(relx=0.20,rely=0,relwidth=1,relheight=1)
        #Tree frame
        self.tree_frame=ctk.CTkFrame(self.main_frame)
        self.tree_frame.place(relx=0,rely=0,relwidth=1,relheight=0.39)
        App.tree_frame=self.tree_frame
        #Details frame
        self.details_frame=ctk.CTkFrame(self.main_frame)
        self.details_frame.place(relx=0.01,rely=0.41,relwidth=0.55,relheight=0.57)
        App.details_frame=self.details_frame
        #details picture
        App.details_pic=ctk.CTkFrame(self.main_frame)
        App.details_pic.place(relx=0.51,rely=0.41,relwidth=0.28,relheight=0.57)
    #Buttons
        #Add_Book Button
        self.book_button=ctk.CTkButton(self.menu_frame,text="Add Book",corner_radius=10,fg_color=BUTTON_COLOUR, command=self.open_book_form)
        self.book_button.pack(padx=100, pady=20,fill="x",anchor="nw")
        #Edit_Book Button
        self.book_button=ctk.CTkButton(self.menu_frame,text="Edit Book",corner_radius=10,fg_color=BUTTON_COLOUR, command= lambda: edit_book(self))
        self.book_button.pack(padx=100, pady=20,fill="x",anchor="nw")
        #Delete_Book Button
        self.book_button=ctk.CTkButton(self.menu_frame,text="Delete Book",corner_radius=10,fg_color=BUTTON_COLOUR, command=lambda: delete_book())
        self.book_button.pack(padx=100, pady=20,fill="x",anchor="nw")

 #MAIN
    #treeView
        data=data_fetch_all()
        App.treeview=create_treeview(self.tree_frame,book_columns,data)
        
        default_selected_item=App.treeview.get_children()[0]    #default_selected_item
        App.treeview.selection_set(default_selected_item)       #set default_selected_item
        App.selected_item=App.treeview.item(default_selected_item)   
        App.treeview.bind("<ButtonRelease-1>", lambda e: select_record())
       
    #detailsView
        App.details_view=details_view(self.details_frame)
 
    def open_book_form(self):
        if self.obf==None or not self.obf.winfo_exists():
            self.obf=Book_form(self)
    
        
app=App("OUR BOOKS")
app.mainloop()
