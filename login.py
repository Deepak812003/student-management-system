from tkinter import *
import time
from tkinter import ttk, messagebox
import ttkthemes
from ttkthemes import ThemedTk
import pymysql
import datetime


def clock():
    date = time.strftime('%d/%m/%Y')
    current_time = time.strftime('%H:%M:%S')
    datelabel.config(text=f'    Date: {date}\n Time: {current_time}')
    datelabel.after(1000, clock)


text = ""
count = 0
s = "Student Management System"


def slider():
    global text, count
    if count == len(s):
        text = ""
        count = 0
    text = text + s[count]
    sliderlabel.config(text=text)
    count += 1
    sliderlabel.after(300, slider)


def connect_database():
    def connect():
        global mycursor, con
        try:
            con = pymysql.connect(host=hostEntry.get(), user=userEntry.get(), password=passwordEntry.get())
            mycursor = con.cursor()

        except:
            messagebox.showerror('Error', 'Invalid data', parent=window)
            return

        try:
            query = 'CREATE DATABASE IF NOT EXISTS studentdetails'
            mycursor.execute(query)
            query = 'USE studentdetails'
            mycursor.execute(query)
            create_table = '''
                            CREATE TABLE IF NOT EXISTS student (
                                id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                                name VARCHAR(30),
                                email VARCHAR(30),
                                mobile BIGINT(10),
                                gender VARCHAR(30),
                                address VARCHAR(100),
                                dob VARCHAR(30),
                                join_date VARCHAR(30)
                            )
                        '''
            mycursor.execute(create_table)
        except:
            query = 'USE studentdetails'
            mycursor.execute(query)

        messagebox.showinfo('Success', 'Database Connection is connected successfully', parent=window)
        window.destroy()
        addstudent.config(state=NORMAL)
        searchstudent.config(state=NORMAL)
        updatestudent.config(state=NORMAL)
        deletestudent.config(state=NORMAL)
        showstudent.config(state=NORMAL)

    window = Toplevel()
    window.geometry("470x270+730+230")
    window.grab_set()
    window.title("Database")
    window.resizable(False, False)
    host = Label(window, text="Host Name:", font=("Times New Roman", 15, "bold"))
    host.grid(row=0, column=0)
    hostEntry = Entry(window, font=("Times new Roman", 15, "bold"))
    hostEntry.grid(row=0, column=1, padx=20, pady=10)
    user = Label(window, text="User Name:", font=("Times New Roman", 15, "bold"))
    user.grid(row=1, column=0)
    userEntry = Entry(window, font=("Times new Roman", 15, "bold"))
    userEntry.grid(row=1, column=1, padx=20, pady=10)
    password = Label(window, text="Password:", font=("Times New Roman", 15, "bold"))
    password.grid(row=2, column=0)
    passwordEntry = Entry(window, font=("Times new Roman", 15, "bold"), show="*")
    passwordEntry.grid(row=2, column=1, padx=20, pady=10)
    connect = ttk.Button(window, text="Connect", command=connect)
    connect.grid(row=3, columnspan=2, pady=10)


def Add():
    def adddata():
        if idEntry.get() == '' or nameEntry.get() == '' or emailEntry.get() == '' or mobileEntry.get() == '' or addressEntry.get() == '' or genderEntry.get() == '' or dobEntry.get() == '' or joinEntry.get() == '':
            messagebox.showerror('Error', 'All details are must required', parent=addwindow)
        else:
            try:

                dob = datetime.datetime.strptime(dobEntry.get(), '%d/%m/%Y').strftime('%Y-%m-%d')
                join_date = datetime.datetime.strptime(joinEntry.get(), '%d/%m/%Y').strftime('%Y-%m-%d')

                query = 'INSERT INTO student (id, name, email, mobile, gender, address, dob, join_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
                values = (idEntry.get(), nameEntry.get(), emailEntry.get(), mobileEntry.get(), genderEntry.get(),
                          addressEntry.get(), dob, join_date)
                mycursor.execute(query, values)
                con.commit()
                result = messagebox.askyesno('confirm',
                                             'Add student details into the database. Do you want to clean the form?',
                                             parent=addwindow)
                if result:
                    idEntry.delete(0, END)
                    nameEntry.delete(0, END)
                    emailEntry.delete(0, END)
                    mobileEntry.delete(0, END)
                    genderEntry.delete(0, END)
                    addressEntry.delete(0, END)
                    dobEntry.delete(0, END)
                    joinEntry.delete(0, END)
                query = 'SELECT * FROM student'
                mycursor.execute(query)
                fetch = mycursor.fetchall()
                student.delete(*student.get_children())
                for data in fetch:
                    dataList = list(data)
                    student.insert('', END, values=dataList)
            except ValueError:
                messagebox.showerror('Error', 'Please enter the date in DD/MM/YYYY format', parent=addwindow)
            except:
                messagebox.showerror('Error','Id cannot be duplicate')

    addwindow = Toplevel()
    addwindow.geometry("470x550")
    addwindow.resizable(False, False)
    addwindow.grab_set()
    id = Label(addwindow, font=("times new roman", 20, "bold"), text="ID:")
    id.grid(row=0, column=0, padx=20, pady=10)
    idEntry = Entry(addwindow, font=("times new roman", 15, "bold"), width=20)
    idEntry.grid(row=0, column=1, pady=10)
    name = Label(addwindow, text="NAME:", font=("times new roman", 20, "bold"))
    name.grid(row=1, column=0, padx=20, pady=10)
    nameEntry = Entry(addwindow, font=("times new roman", 15, "bold"), width=20)
    nameEntry.grid(row=1, column=1, pady=10)
    email = Label(addwindow, text="EMAIL:", font=("times new roman", 20, "bold"))
    email.grid(row=2, column=0, padx=20, pady=10)
    emailEntry = Entry(addwindow, font=("times new roman", 15, "bold"), width=20)
    emailEntry.grid(row=2, column=1, pady=10)
    mobile = Label(addwindow, text="MOBILE:", font=("times new roman", 20, "bold"))
    mobile.grid(row=3, column=0, padx=20, pady=10)
    mobileEntry = Entry(addwindow, font=("times new roman", 15, "bold"), width=20)
    mobileEntry.grid(row=3, column=1, pady=10)
    gender = Label(addwindow, text="GENDER:", font=("times new roman", 20, "bold"))
    gender.grid(row=4, column=0, padx=20, pady=10)
    genderEntry = Entry(addwindow, font=("times new roman", 15, "bold"), width=20)
    genderEntry.grid(row=4, column=1, pady=10)
    address = Label(addwindow, text="ADDRESS:", font=("times new roman", 20, "bold"))
    address.grid(row=5, column=0, padx=20, pady=10)
    addressEntry = Entry(addwindow, font=("times new roman", 15, "bold"), width=20)
    addressEntry.grid(row=5, column=1, pady=10)
    dob = Label(addwindow, text="DOB:", font=("times new roman", 20, "bold"))
    dob.grid(row=6, column=0, padx=20, pady=10)
    dobEntry = Entry(addwindow, font=("times new roman", 15, "bold"), width=20)
    dobEntry.grid(row=6, column=1, pady=10)
    join = Label(addwindow, text="JOIN DATE:", font=("times new roman", 20, "bold"))
    join.grid(row=7, column=0, padx=20, pady=10)
    joinEntry = Entry(addwindow, font=("times new roman", 15, "bold"), width=20)
    joinEntry.grid(row=7, column=1, pady=10)
    submit = ttk.Button(addwindow, text="ADD", command=adddata)
    submit.grid(row=8, columnspan=2)
def search():
    def searchdata():
        query = ""
        params = ()

        if idEntry.get():
            query = 'SELECT * FROM student WHERE id=%s'
            params = (idEntry.get(),)
        elif nameEntry.get():
            query = 'SELECT * FROM student WHERE name=%s'
            params = (nameEntry.get(),)
        elif mobileEntry.get():
            query = 'SELECT * FROM student WHERE mobile=%s'
            params = (mobileEntry.get(),)
        elif emailEntry.get():
            query = 'SELECT * FROM student WHERE email=%s'
            params = (emailEntry.get(),)
        elif genderEntry.get():
            query = 'SELECT * FROM student WHERE gender=%s'
            params = (genderEntry.get(),)
        elif addressEntry.get():
            query = 'SELECT * FROM student WHERE address LIKE %s'
            params = (f"%{addressEntry.get()}%",)
        elif dobEntry.get():
            query = 'SELECT * FROM student WHERE dob=%s'
            params = (dobEntry.get(),)
        elif joinEntry.get():
            query = 'SELECT * FROM student WHERE join=%s'
            params = (joinEntry.get(),)
        else:
            return

        mycursor.execute(query, params)

        student.delete(*student.get_children())
        fetch_data = mycursor.fetchall()
        for data in fetch_data:
            student.insert('', END, values=data)

    searchwindow = Toplevel()
    searchwindow.geometry("470x550")
    searchwindow.resizable(False, False)
    searchwindow.grab_set()
    id = Label(searchwindow, font=("times new roman", 20, "bold"), text="ID:")
    id.grid(row=0, column=0, padx=20, pady=10)
    idEntry = Entry(searchwindow, font=("times new roman", 15, "bold"), width=20)
    idEntry.grid(row=0, column=1, pady=10)
    name = Label(searchwindow, text="NAME:", font=("times new roman", 20, "bold"))
    name.grid(row=1, column=0, padx=20, pady=10)
    nameEntry = Entry(searchwindow, font=("times new roman", 15, "bold"), width=20)
    nameEntry.grid(row=1, column=1, pady=10)
    email = Label(searchwindow, text="EMAIL:", font=("times new roman", 20, "bold"))
    email.grid(row=2, column=0, padx=20, pady=10)
    emailEntry = Entry(searchwindow, font=("times new roman", 15, "bold"), width=20)
    emailEntry.grid(row=2, column=1, pady=10)
    mobile = Label(searchwindow, text="MOBILE:", font=("times new roman", 20, "bold"))
    mobile.grid(row=3, column=0, padx=20, pady=10)
    mobileEntry = Entry(searchwindow, font=("times new roman", 15, "bold"), width=20)
    mobileEntry.grid(row=3, column=1, pady=10)
    gender = Label(searchwindow, text="GENDER:", font=("times new roman", 20, "bold"))
    gender.grid(row=4, column=0, padx=20, pady=10)
    genderEntry = Entry(searchwindow, font=("times new roman", 15, "bold"), width=20)
    genderEntry.grid(row=4, column=1, pady=10)
    address = Label(searchwindow, text="ADDRESS:", font=("times new roman", 20, "bold"))
    address.grid(row=5, column=0, padx=20, pady=10)
    addressEntry = Entry(searchwindow, font=("times new roman", 15, "bold"), width=20)
    addressEntry.grid(row=5, column=1, pady=10)
    dob = Label(searchwindow, text="DOB:", font=("times new roman", 20, "bold"))
    dob.grid(row=6, column=0, padx=20, pady=10)
    dobEntry = Entry(searchwindow, font=("times new roman", 15, "bold"), width=20)
    dobEntry.grid(row=6, column=1, pady=10)
    join = Label(searchwindow, text="JOIN DATE:", font=("times new roman", 20, "bold"))
    join.grid(row=7, column=0, padx=20, pady=10)
    joinEntry = Entry(searchwindow, font=("times new roman", 15, "bold"), width=20)
    joinEntry.grid(row=7, column=1, pady=10)
    submit = ttk.Button(searchwindow, text="SEARCH",command=searchdata)
    submit.grid(row=8, columnspan=2)
def delete():
    index=student.focus()
    content=student.item(index)
    content_id=content['values'][0]
    query='delete from student where id=%s'
    mycursor.execute(query,content_id)
    con.commit()
    messagebox.showinfo('Deleted..',f'this {content_id} is deleted successfully')
    query='select * from student'
    mycursor.execute(query)
    fetch_data=mycursor.fetchall()
    student.delete(*student.get_children())
    for data in fetch_data:
        student.insert('',END,values=data)
def show():
    query = 'select * from student'
    mycursor.execute(query)
    fetch_data = mycursor.fetchall()
    student.delete(*student.get_children())
    for data in fetch_data:
        student.insert('', END, values=data)
def update():
    def updatedata():
        try:
            original_dob = data[6]
            original_join_date = data[7]
            if dobEntry.get() != original_dob:
                dob = datetime.datetime.strptime(dobEntry.get(), '%d/%m/%Y').strftime('%Y-%m-%d')
            else:
                dob = original_dob
            if joinEntry.get() != original_join_date:
                join_date = datetime.datetime.strptime(joinEntry.get(), '%d/%m/%Y').strftime('%Y-%m-%d')
            else:
                join_date = original_join_date
            query = '''UPDATE student 
                          SET name=%s, email=%s, mobile=%s, gender=%s, address=%s, dob=%s, join_date=%s 
                          WHERE id=%s'''
            mycursor.execute(query, (
                nameEntry.get(), emailEntry.get(), mobileEntry.get(), genderEntry.get(), addressEntry.get(), dob,
                join_date, idEntry.get()))
            con.commit()
            messagebox.showinfo('Success', f'ID {idEntry.get()} has been updated successfully')
            updatewindow.destroy()
            show()

        except ValueError:
            messagebox.showerror('Error', 'Please enter the date in DD/MM/YYYY format', parent=updatewindow)
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred: {str(e)}', parent=updatewindow)
    updatewindow = Toplevel()
    updatewindow.geometry("470x550")
    updatewindow.resizable(False, False)
    updatewindow.grab_set()
    id = Label(updatewindow, font=("times new roman", 20, "bold"), text="ID:")
    id.grid(row=0, column=0, padx=20, pady=10)
    idEntry = Entry(updatewindow, font=("times new roman", 15, "bold"), width=20)
    idEntry.grid(row=0, column=1, pady=10)
    name = Label(updatewindow, text="NAME:", font=("times new roman", 20, "bold"))
    name.grid(row=1, column=0, padx=20, pady=10)
    nameEntry = Entry(updatewindow, font=("times new roman", 15, "bold"), width=20)
    nameEntry.grid(row=1, column=1, pady=10)
    email = Label(updatewindow, text="EMAIL:", font=("times new roman", 20, "bold"))
    email.grid(row=2, column=0, padx=20, pady=10)
    emailEntry = Entry(updatewindow, font=("times new roman", 15, "bold"), width=20)
    emailEntry.grid(row=2, column=1, pady=10)
    mobile = Label(updatewindow, text="MOBILE:", font=("times new roman", 20, "bold"))
    mobile.grid(row=3, column=0, padx=20, pady=10)
    mobileEntry = Entry(updatewindow, font=("times new roman", 15, "bold"), width=20)
    mobileEntry.grid(row=3, column=1, pady=10)
    gender = Label(updatewindow, text="GENDER:", font=("times new roman", 20, "bold"))
    gender.grid(row=4, column=0, padx=20, pady=10)
    genderEntry = Entry(updatewindow, font=("times new roman", 15, "bold"), width=20)
    genderEntry.grid(row=4, column=1, pady=10)
    address = Label(updatewindow, text="ADDRESS:", font=("times new roman", 20, "bold"))
    address.grid(row=5, column=0, padx=20, pady=10)
    addressEntry = Entry(updatewindow, font=("times new roman", 15, "bold"), width=20)
    addressEntry.grid(row=5, column=1, pady=10)
    dob = Label(updatewindow, text="DOB:", font=("times new roman", 20, "bold"))
    dob.grid(row=6, column=0, padx=20, pady=10)
    dobEntry = Entry(updatewindow, font=("times new roman", 15, "bold"), width=20)
    dobEntry.grid(row=6, column=1, pady=10)
    join = Label(updatewindow, text="JOIN DATE:", font=("times new roman", 20, "bold"))
    join.grid(row=7, column=0, padx=20, pady=10)
    joinEntry = Entry(updatewindow, font=("times new roman", 15, "bold"), width=20)
    joinEntry.grid(row=7, column=1, pady=10)
    submit = ttk.Button(updatewindow, text="UPDATE",command=updatedata)
    submit.grid(row=8, columnspan=2)
    index=student.focus()
    content=student.item(index)
    data=content['values']
    idEntry.insert(0,data[0])
    nameEntry.insert(0,data[1])
    emailEntry.insert(0,data[2])
    mobileEntry.insert(0,data[3])
    genderEntry.insert(0,data[4])
    addressEntry.insert(0,data[5])
    dobEntry.insert(0,data[6])
    joinEntry.insert(0,data[7])
def exit():
    result=messagebox.askyesno('confirm','Do you want to exit this window')
    if result:
        root.destroy()
    else:
        pass



root = ThemedTk(theme="Scidgreen")
root.geometry("1290x700+0+0")
root.resizable(False, False)
root.title("Student Management System")
datelabel = Label(root, font=("Times new roman", 18))
datelabel.place(x=5, y=5)
clock()
s = "Student Management System"
sliderlabel = Label(root, font=("Times new Roman", 30, "italic bold"), fg="red", width=20)
sliderlabel.place(x=400, y=0)
slider()

connectButton = ttk.Button(root, text="Connect Database", cursor="hand2", command=connect_database)
connectButton.place(x=1000, y=0, )

leftframe = Frame(root)
leftframe.place(x=40, y=80, width=300, height=600)
student_image = PhotoImage(file="students.png")
login_image = Label(leftframe, image=student_image)
login_image.grid(row=0, column=0)
addstudent = ttk.Button(leftframe, text="ADD STUDENT", width=25, state=DISABLED, command=Add)
addstudent.grid(row=1, column=0, pady=20)
searchstudent = ttk.Button(leftframe, text="SEARCH STUDENT", width=25, state=DISABLED,command=search)
searchstudent.grid(row=2, column=0, pady=20)
updatestudent = ttk.Button(leftframe, text="UPDATE STUDENT", width=25, state=DISABLED,command=update)
updatestudent.grid(row=3, column=0, pady=20)
deletestudent = ttk.Button(leftframe, text="DELETE STUDENT", width=25, state=DISABLED,command=delete)
deletestudent.grid(row=4, column=0, pady=20)
showstudent = ttk.Button(leftframe, text="SHOW STUDENTS", width=25, state=DISABLED,command=show)
showstudent.grid(row=5, column=0, pady=20)
exitstudent = ttk.Button(leftframe, text="EXIT", width=25,command=exit)
exitstudent.grid(row=6, column=0, pady=20)

rightframe = Frame(root)
rightframe.place(x=350, y=80, width=900, height=600)
scroll_x = Scrollbar(rightframe, orient=HORIZONTAL)
scroll_x.pack(side=BOTTOM, fill=X)
scroll_y = Scrollbar(rightframe, orient=VERTICAL)
scroll_y.pack(side=RIGHT, fill=Y)
student = ttk.Treeview(rightframe, columns=('ID', 'NAME', 'EMAIL', 'MOBILE', 'GENDER', 'ADDRESS', 'DOB', 'JOIN DATE'),
                       xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
student.pack(fill=BOTH, expand=1)
scroll_x.config(command=student.xview)
scroll_y.config(command=student.yview)
student.heading('ID', text='ID')
student.heading('NAME', text='NAME')
student.heading('EMAIL', text='E-MAIL')
student.heading('MOBILE', text='MOBILE-NO')
student.heading('GENDER', text='GENDER')
student.heading('ADDRESS', text='ADDRESS')
student.heading('DOB', text='DOB')
student.heading('JOIN DATE', text='JOIN DATE')
student.config(show="headings")
style=ttk.Style()
style.configure('Treeview',rowheight=40,background='white',fieldbackground='red',font=('arial',12,'bold'))
style.configure('Treeview.heading',font=('arial',12,'bold'))
root.mainloop()
