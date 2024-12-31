from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import addbook,addmember,givebook

con=sqlite3.connect("Library.db")
cur=con.cursor()

class Myclass(object):
    def __init__(self,master):
        self.master=master 

        def displayStatistics(evt):
            count_books=cur.execute("SELECT count(book_id) FROM books").fetchall()
            count_members = cur.execute("SELECT count(member_id) FROM members").fetchall()
            taken_books = cur.execute("SELECT count(book_status) FROM books WHERE book_status=1").fetchall()
            print(count_books)
            self.lbl_book_count.config(text='Total :'+ str(count_books[0][0])+' books in library')
            self.lbl_member_count.config(text="Total member : "+str(count_members[0][0]))
            self.lbl_taken_count.config(text="Taken books :"+str(taken_books[0][0]))
            displayBooks(self)


        def displayBooks(self):
            books=cur.execute("SELECT * FROM books").fetchall()
            count=0

            self.list_books.delete(0,END)
            for book in books:
                print(book)
                self.list_books.insert(count,str(book[0])+ "-" +book[1])
                count +=1

            def bookInfo(evt):
                value=str(self.list_books.get(self.list_books.curselection()))
                id=value.split('-')[0]
                book =cur.execute("SELECT * FROM books WHERE book_id=?",(id,))
                book_info=book.fetchall()
                print(book_info)
                self.list_details.delete(0,'end')
                self.list_details.insert(0,"Book Name : "+book_info[0][1])
                self.list_details.insert(1,"Author : "+book_info[0][2])
                self.list_details.insert(2,"Page : "+book_info[0][3])
                self.list_details.insert(3,"Language : "+book_info[0][4])
                if book_info[0][5] == 0:
                    self.list_details.insert(4,"Status : Avaiable")
                else:
                    self.list_details.insert(4,"Status : Not Avaiable")


            def doubleClick(evt):
                global given_id
                value=str(self.list_books.get(self.list_books.curselection()))
                given_id=value.split('-')[0]
                give_book=GiveBook()


            self.list_books.bind('<<ListboxSelect>>',bookInfo)
            self.tabs.bind('<<NotebookTabChanged>>',displayStatistics)
            # self.tabs.bind('<ButtonRelease-1>',displayBooks)
            self.list_books.bind('<Double-Button-1>',doubleClick)
            
           

        #### Master Frame ####
        masterframe=Frame(self.master,cursor="arrow")
        masterframe.pack()
        #### TopFrame ####
        topframe=Frame(masterframe,bg="#CBBFBD",width=1300,height=70,relief=SUNKEN,borderwidth=2)
        topframe.pack(fill=X,side=TOP)
        #### Center Frmae ####
        centerframe=Frame(masterframe,width=1300,height=620,bg="lightblue")
        centerframe.pack(fill=X,side=TOP)
        #### Center Left Frame ####
        centerleft=Frame(centerframe,bg="lightblue",relief=SUNKEN,borderwidth=2,width=900,height=620)
        centerleft.pack(side=LEFT)
        #### Center Right Frame ####
        centerright=Frame(centerframe,bg="lightblue",relief=SUNKEN,borderwidth=2,width=480,height=620)
        centerright.pack()
        #### Search Bar ####
        searchbar=LabelFrame(centerright,width=320,height=70,bg="#F2C043",text="SearchBox")
        searchbar.pack(fill=BOTH)
        #### ListBar ####
        listbar=LabelFrame(centerright,bg="#87F445",width=440,height=185,text="ListBox")
        listbar.pack(fill=BOTH)

        labellist=Label(listbar,text="Sort By ?",font="Times 15",fg="#01080A",bg="#87F445")
        labellist.grid(row=0,column=2)

        #### ListButtons ####
        style = ttk.Style()

        # style for the Radiobutton
        style.configure("Custom.TRadiobutton", background="#87F445", foreground="black", padding=10)

        self.choose=IntVar()
        r1=ttk.Radiobutton(listbar,text="All Books",variable=self.choose,value=1,style="Custom.TRadiobutton")
        r2=ttk.Radiobutton(listbar,text="In Library",variable=self.choose,value=2,style="Custom.TRadiobutton")
        r3=ttk.Radiobutton(listbar,text="Borrowed Books",variable=self.choose,value=3,style="Custom.TRadiobutton")

        r1.grid(row=1,column=0)
        r2.grid(row=1,column=1)
        r3.grid(row=1,column=2)

        #### Sort button to sort books ####
        self.sortbtn=Button(listbar,text="Sort !",font="Times 15 bold",width=6,bg="#72D6F3",relief=RAISED,command=self.listBooks)
        self.sortbtn.grid(row=1,column=3,padx=40,pady=5)
        


        #### Add Book button ####
        self.iconadd=PhotoImage(file="icons/add_book.png")
        self.btnadd=Button(topframe,image=self.iconadd,compound=LEFT,font="Arial 12",text="Add Book",command=self.addBook)
        self.btnadd.pack(padx=10,side=LEFT)
        #### Add Member button ####
        self.iconmem=PhotoImage(file="icons/users.png")
        self.btnmember=Button(topframe,text="Add Member",font="Arial 12",image=self.iconmem,compound=LEFT,command=self.addMember)
        self.btnmember.pack(side=LEFT,padx=10)
        #### Give Book button ####
        self.icongive=PhotoImage(file="icons/givebook.png")
        self.btngive=Button(topframe,text="Give book",font="Arial 12",image=self.icongive,compound=LEFT,command=self.giveBook)
        self.btngive.pack(side=LEFT,pady=10)

        #### Search Box ####
        self.lbl=Label(searchbar,text="Search",font="Arial 12 bold",fg="#185905",bg="#F2C043")
        self.lbl.grid(row=0,column=0,padx=10,pady=20)
        #### EntryBox ####
        self.entrysearch=Entry(searchbar,width=30,bd=5,font="Times 12")
        self.entrysearch.grid(row=0,column=1,columnspan=3)
        #### Search Button ####
        self.searchbtn=Button(searchbar,text="Search !",font="Arial 12 bold",relief=RAISED,command=self.searchBooks)
        self.searchbtn.grid(row=0,column=4,padx=10)

        libframe = Frame(centerright, width=440, height=380, relief=GROOVE, bd=10, bg="#F7FAFB")
        libframe.pack(fill=BOTH)

        # Library label
        libimage = Label(libframe, text="Welcome to our Library !!", font="Times 16 bold", bg="#F7FAFB")
        libimage.pack(pady=10)

        # Library image
        self.image_lib = PhotoImage(file="icons/library image.png")
        self.image_bar = Label(libframe, image=self.image_lib, bg="#F7FAFB")
        self.image_bar.pack(pady=20)

        # self.image_lib1=PhotoImage(file="icons/books1.png")
        # self.imagebar1=Label(libframe,image=self.image_lib1)
        # self.imagebar1.grid(row=2,sticky=W)
        # self.image_lib2=PhotoImage(file="icons/books3.png")
        # self.imagebar2=Label(libframe,image=self.image_lib2)
        # self.imagebar2.grid(row=2,sticky=E)
        # self.image_lib3=PhotoImage(file="icons/lib1.png")
        # self.imagebar3=Label(libframe,image=self.image_lib3)
        # self.imagebar3.grid(row=2,sticky=N)
        # self.image_lib4=PhotoImage(file="icons/icon1.png")
        # self.imagebar4=Label(libframe,image=self.image_lib4)
        # self.imagebar4.grid(row=1,padx=10,sticky=W)

        ####Tabs FRAME ####
        self.tabs= ttk.Notebook(centerleft,width=900,height=660)
        self.tabs.pack()
        self.tab1_icon=PhotoImage(file='icons/books.png')
        self.tab2_icon=PhotoImage(file='icons/members.png')
        self.tab1=ttk.Frame(self.tabs)
        self.tab2=ttk.Frame(self.tabs)
        self.tabs.add(self.tab1,text='Library Management',image=self.tab1_icon,compound=LEFT)
        self.tabs.add(self.tab2,text='Statistics',image=self.tab2_icon,compound=LEFT)

        self.list_books= Listbox(self.tab1,width=40,height=30,bd=5,font='times 12 bold')
        self.sb=Scrollbar(self.tab1,orient=VERTICAL)
        self.list_books.grid(row=0,column=0,padx=(10,0),pady=10,sticky=N)
        self.sb.config(command=self.list_books.yview)
        self.list_books.config(yscrollcommand=self.sb.set)
        self.sb.grid(row=0,column=0,sticky=N+S+E)
        #list details
        self.list_details=Listbox(self.tab1,width=80,height=30,bd=5,font='times 12 bold')
        self.list_details.grid(row=0,column=1,padx=(10,0),pady=10,sticky=N)
        ##########################tab2####################################
        #statistics
        self.lbl_book_count= Label(self.tab2,text="Yash",pady=20,font='verdana 14 bold')
        self.lbl_book_count.grid(row=0)
        self.lbl_member_count=Label(self.tab2,text="Bhai",pady=20,font='verdana 14 bold')
        self.lbl_member_count.grid(row=1,sticky=W)
        self.lbl_taken_count=Label(self.tab2,text="OP",pady=20,font='verdana 14 bold')
        self.lbl_taken_count.grid(row=2,sticky=W)
        
        #functions
        displayBooks(self)
    


    def addBook(self):
        add=addbook.AddBook()
    def addMember(self):
        member=addmember.AddMember()
    def searchBooks(self):
        value = self.entrysearch.get()
        search= cur.execute("SELECT * FROM Books WHERE Book_name LIKE ?",('%'+value+'%',)).fetchall()
        print(search)
        self.list_books.delete(0,END)
        count=0
        for book in search:
            self.list_books.insert(count,str(book[0])+ "-"+book[1])
            count +=1
    def listBooks(self):
        value = self.choose.get()
        if value == 1:
            allbooks= cur.execute("SELECT * FROM books").fetchall()
            self.list_books.delete(0,END)

            count=0
            for book in allbooks:
                self.list_books.insert(count,str(book[0]) + "-"+book[1])
                count +=1

        elif value == 2:
            books_in_library = cur.execute("SELECT * FROM books WHERE book_status =?",(0,)).fetchall()
            self.list_books.delete(0, END)

            count = 0
            for book in books_in_library:
                self.list_books.insert(count, str(book[0]) + "-" + book[1])
                count += 1
        else:
            taken_books= cur.execute("SELECT * FROM books WHERE book_status =?",(1,)).fetchall()
            self.list_books.delete(0, END)

            count = 0
            for book in taken_books:
                self.list_books.insert(count, str(book[0]) + "-" + book[1])

                count += 1
    def giveBook(self):
        give_book = givebook.GiveBook()
    

class GiveBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x650")
        self.title("Lend Book")
        self.resizable(False,False)
        self.resizable(False,False)
        global given_id
        self.book_id=int(given_id)
        query="SELECT * FROM books"
        books =cur.execute(query).fetchall()
        book_list=[]
        for book in books:
            book_list.append(str(book[0])+"-"+book[1])

        query2="SELECT * FROM members"
        members = cur.execute(query2).fetchall()
        member_list=[]
        for member in members:
            member_list.append(str(member[0])+"-"+member[1])
        #######################Frames#######################

        # Top Frame
        self.topFrame = Frame(self, height=150, bg='white')
        self.topFrame.pack(fill=X)
        # Bottom Frame
        self.bottomFrame = Frame(self, height=600, bg='#A3F95B')
        self.bottomFrame.pack(fill=X)
        # heading, image
        self.top_image = PhotoImage(file='icons/addperson.png')
        top_image_lbl = Label(self.topFrame, image=self.top_image, bg='white')
        top_image_lbl.place(x=120, y=10)
        heading = Label(self.topFrame, text='  Lend Book ! ', font='arial 22 bold', fg='#003f8a', bg='white')
        heading.place(x=290, y=60)

        ###########################################Entries and Labels########################3

        # member name
        self.book_name = StringVar()
        self.lbl_name = Label(self.bottomFrame, text='Book: ', font='arial 15 bold', fg='black', bg='#A3F95B')
        self.lbl_name.place(x=40, y=40)
        self.combo_name = ttk.Combobox(self.bottomFrame,textvariable=self.book_name)
        self.combo_name['values']=book_list
        self.combo_name.current(self.book_id-1)
        self.combo_name.place(x=150,y=45)

        # phone
        self.member_name = StringVar()
        self.lbl_phone = Label(self.bottomFrame, text='Member: ', font='arial 15 bold', fg='black', bg='#A3F95B')
        self.lbl_phone.place(x=40, y=80)
        self.combo_member = ttk.Combobox(self.bottomFrame, textvariable=self.member_name)
        self.combo_member['values']=member_list
        self.combo_member.place(x=150, y=85)

        # Button
        button = Button(self.bottomFrame, text='Lend Book',command=self.lendBook)
        button.place(x=220, y=130)

    def lendBook(self):
        book_name=self.book_name.get()
        member_name=self.member_name.get()

        if(book_name and member_name !=""):
            try:
                query="INSERT INTO 'Borrows' (bbook_id,bmember_id) VALUES(?,?)"
                cur.execute(query,(book_name,member_name))
                con.commit()
                messagebox.showinfo("Success","Successfully added to database!",icon='info')
                cur.execute("UPDATE books SET Book_status =? WHERE book_id=?",(1,self.book_id))
                con.commit()
            except:
                messagebox.showerror("Error", "Cant add to database", icon='warning')

        else:
            messagebox.showerror("Error","Fields cant be empty",icon='warning')


def main():
    root=Tk()
    app=Myclass(root)
    root.title("Library Management System")
    root.geometry("1300x750")
    root.iconbitmap("icons/icon.ico")
    root.mainloop()

if __name__== "__main__":
    main()
