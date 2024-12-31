from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

con=sqlite3.connect("Library.db")
cur=con.cursor()

class AddMember(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x650")
        self.title("Add Member")
        self.resizable(False,False)

        ####Frames####

        #Top Frame
        self.topFrame= Frame(self,height=150,bg='white')
        self.topFrame.pack(fill=X)
        #Bottom Frame
        self.bottomFrame= Frame(self,height=600,bg='#F98151')
        self.bottomFrame.pack(fill=X)
        #heading, image
        self.top_image= PhotoImage(file='icons/addperson.png')
        top_image_lbl=Label(self.topFrame,image=self.top_image,bg='white')
        top_image_lbl.place(x=120,y=10)
        heading=Label(self.topFrame, text=' Add Person ',font='arial 22 bold',fg='#003f8a',bg='white')
        heading.place(x=290,y=60)

        ####Entries and Labels####

        #member name
        self.lbl_name=Label(self.bottomFrame,text='Name :',font='arial 15 bold',fg='black',bg='#F98151')
        self.lbl_name.place(x=40,y=85)
        self.ent_name=Entry(self.bottomFrame,width=30,bd=4)
        self.ent_name.insert(0,'Please enter your name')
        self.ent_name.place(x=150,y=85)

        # phone
        self.lbl_phone = Label(self.bottomFrame, text='Phone :', font='arial 15 bold', fg='Black', bg='#F98151')
        self.lbl_phone.place(x=40, y=125)
        self.ent_phone = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_phone.insert(0, 'Please enter Phone Number')
        self.ent_phone.place(x=150, y=130)

        #Button
        button=Button(self.bottomFrame,text='Add Member',command=self.addMember)
        button.place(x=270,y=180)

    def addMember(self):
        name = self.ent_name.get()
        phone=self.ent_phone.get()


        if (name and phone !=""):
            try:
                query="INSERT INTO 'Members' (Member_name,Member_phone) VALUES(?,?)"
                cur.execute(query,(name,phone))
                con.commit()
                messagebox.showinfo("Success","Successfully added to database",icon='info')

            except:
                messagebox.showerror("Error","Cant add to database",icon='warning')
        else:
            messagebox.showerror("Error", "Fields cant be empty", icon='warning')