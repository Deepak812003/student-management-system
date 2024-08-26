from tkinter import *
from PIL import ImageTk
#PIL-python image library
from tkinter import messagebox
#this module import the error msg in the frontend

def log():
    if userEntry.get()=='' or paswordEntry.get()=='':
        messagebox.showerror('error','field cannot be empty')
    elif userEntry.get()=='DEEPAK'.lower() and paswordEntry.get()=='1234':
        messagebox.showinfo('success','Welcome')
        root.destroy()
        import login

    else:
        messagebox.showerror('error','Please enter correct details')

root=Tk()
root.geometry("1290x700+0+0")
root.title("Login")
root.resizable(False,False)
login=Frame(root)
login.place(x=400,y=100)
logo=PhotoImage(file='graduate.png')
detail=Label(login,image=logo)
detail.grid(row=0,column=0 )
username=Label(login,text="Username",font=("Times new roman",20,"bold"))
username.grid(row=1,column=0,padx=30)
userEntry=Entry(login,font=("times new roman",20,"bold"),bd=5,fg="red")
userEntry.grid(row=1,column=1,padx=30)
password=Label(login,text="Password",font=("times new roman",20,"bold"))
password.grid(row=2,column=0,padx=30)
paswordEntry=Entry(login,font=("times new roman",20,"bold"),bd=5,fg="green")
paswordEntry.grid(row=2,column=1,padx=30,pady=20)
loginButton=Button(login,text="Login",font=("Times new roman",15,"bold"),width=15,bg="royalblue",fg="white",activebackground="royalblue",cursor="hand2",command=log)
loginButton.grid(row=4,column=1,pady=20)
root.mainloop()