import tkinter as tk
from tkinter import font  as tkfont
import tkinter.messagebox
import sqlite3
'''database connection'''

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne ,display):
            page_name = F.__name__
            frame = F(container,self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

value_1 = ''
value_2 = ''
a_1 = ''
a_2 = ''	
class StartPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		self.label_1 = tk.Label(self,text="Name")
		self.label_1.grid(row=0,sticky="w",padx=10,pady=10)
		self.label_2 = tk.Label(self,text="whats your average cgpa?")
		self.label_2.grid(row=2,sticky="w",padx=10,pady=10)
		self.value_1 = tk.Entry(self)
		self.value_1.grid(row=0,column=1,padx=10,pady=10)
		self.value_2 = tk.Entry(self)
		self.value_2.grid(row=2,column=1,padx=10,pady=10)
		self.value_1.focus_set()	
		self.value_2.focus_set()
		self.q_1 = tk.Label(self,text="what is your favorite subject?")
		self.a_1 = tk.Entry(self)
		self.a_1.focus_set()
		self.q_2 = tk.Label(self,text="what is your favorite game?")
		self.a_2 = tk.Entry(self)
		self.a_2.focus_set()
		self.q_1.grid(row=4,sticky="w",padx=10,pady=10)
		self.a_1.grid(row=4,column=1,padx=10,pady=10)
		self.q_2.grid(row=6,sticky="w",padx=10,pady=10)
		self.a_2.grid(row=6,column=1,padx=10,pady=10)
		self.submit = tk.Button(self,text="submit",command =self.checkEntries,bg="blue",fg="white")
		self.submit.grid(row=10,column=0,padx=10,pady=10)
		self.display = tk.Button(self,text="Search",command=lambda: controller.show_frame("PageOne"),bg="blue",fg="white")
		self.display.grid(row=10,column=1,padx=10,pady=10)
	
	def checkEntries(self):
		if self.value_1.get() == '' or self.value_2.get() == '' or self.a_1.get() == '' or self.a_2.get() == '' :
			tkinter.messagebox.showinfo("invalid input","please fill all the answers")
		else:
			conn = sqlite3.connect('test.db')
			c = conn.cursor()
			c.execute("INSERT INTO survey VALUES(?,?,?,?)",(self.value_1.get(),self.value_2.get(),self.a_1.get(),self.a_2.get()))
			conn.commit()
			conn.close()
			self.value_1.delete(0,"end")
			self.value_2.delete(0,"end")
			self.a_2.delete(0,"end")
			self.a_1.delete(0,"end")
			
class PageOne(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
				
		self.search = tk.Entry(self)
		#self.search.insert(0,'hello')
		self.search.focus_set()		
		self.search.grid(row = 0,column = 0,sticky="e",padx=10,pady=10)
		
		self.searchbut = tk.Button(self, text="enter the name",command=self.searchName)
		self.searchbut.grid(row =0,column =1,padx=10,pady=10)
		
		self.lab1 = tk.Label(self,text="cgpa")
		self.lab2 = tk.Label(self,text="Subject")
		self.lab3 = tk.Label(self,text="hobby")
		
		self.ent1 = tk.Entry(self)
		self.ent2 = tk.Entry(self)
		self.ent3 = tk.Entry(self)
		
		self.lab1.grid(row=2,column=0,padx=10,pady=10)
		self.lab2.grid(row=3,column=0,padx=10,pady=10)
		self.lab3.grid(row=4,column=0,padx=10,pady=10)
		
		self.ent1.grid(row=2,column=1,padx=10,pady=10)
		self.ent2.grid(row=3,column=1,padx=10,pady=10)
		self.ent3.grid(row=4,column=1,padx=10,pady=10)
				
		button = tk.Button(self, text="Survey page",command=lambda: controller.show_frame("StartPage"))
		button.grid(row =7,column=0,padx=10,pady=10)
		button1 = tk.Button(self, text="Display",command=lambda: controller.show_frame("display"))
		button1.grid(row =7,column=1,padx=10,pady=10)
	
	data=('','')
	
	def searchName(self):
		self.ent1.delete(0,"end")
		self.ent2.delete(0,"end")
		self.ent3.delete(0,"end")
		conn = sqlite3.connect('test.db')
		c = conn.cursor()
		c.execute("select * from survey where name=?",(self.search.get(),))
		self.data = c.fetchone()
		#self.search.delete(0,"end")
		print (self.data)
		conn.commit()
		conn.close()
		self.a=self.data[1]
		self.b=self.data[2]
		self.c=self.data[3]
		print(self.a)
		
		self.ent1.insert(0,self.a)
		self.ent2.insert(0,self.b)
		self.ent3.insert(0,self.c)
		data=('','','')

class display(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		label = tk.Label(self, text="Display page", font=controller.title_font)
		label.grid(column=1,columnspan=2)
		
		self.l1 = tk.Label(self,text="Name")
		self.l2 = tk.Label(self,text="CGPA")
		self.l3 = tk.Label(self,text="Subject")
		self.l4 = tk.Label(self,text="hobby")
				
		self.l1.grid(row=2,column=0,padx=10,pady=10)
		self.l2.grid(row=2,column=1,padx=10,pady=10)
		self.l3.grid(row=2,column=2,padx=10,pady=10)
		self.l4.grid(row=2,column=3,padx=10,pady=10)
		
		conn = sqlite3.connect('test.db')
		c = conn.cursor()
		row = 0
		rows = c.execute("select * from survey")
		data = []
		data =list(c.fetchall())
		print (data[4][1])
		print (len(data))
		for d in range(len(data)):
			self.l1 = tk.Label(self,text=data[d][0])
			self.l2 = tk.Label(self,text=data[d][1])
			self.l3 = tk.Label(self,text=data[d][2])
			self.l4 = tk.Label(self,text=data[d][3])
					
			self.l1.grid(row=d+3,column=0,padx=10,pady=10)
			self.l2.grid(row=d+3,column=1,padx=10,pady=10)
			self.l3.grid(row=d+3,column=2,padx=10,pady=10)
			self.l4.grid(row=d+3,column=3,padx=10,pady=10)
		
		
		
		button = tk.Button(self, text="survey page",command=lambda: controller.show_frame("StartPage"))
		button.grid(column=1,columnspan=2)
		
if __name__ == "__main__":
	app = SampleApp()
	app.title("Survey")
	#app.geometry("400x300")
	app.mainloop()






