from tkinter import *
import mysql.connector  
import csv
from tkinter import messagebox

root = Tk()
root.geometry('500x400')
root.title("Students database manager")
#connect to mysql
conn=mysql.connector.connect(
					host='localhost',
					user='root',
					passwd='password123',
					database='students'
						)



#create the cursor
c=conn.cursor()
# create db in mysql
#c.execute('CREATE DATABASE students')

# create a table
'''c.execute("""CREATE TABLE students(
		f_name VARCHAR(255),
		l_name VARCHAR(255),
		s_id INT AUTO_INCREMENT PRIMARY KEY,
		major VARCHAR(255),
		age INT(5)
	)

	""")'''

# Add student function
def add_student():
	query="INSERT INTO students(f_name,l_name,major,age) VALUES(%s,%s,%s,%s)"
	a=age_box.get()
	if a=="":
		a=None
	values=(fname_box.get(),lname_box.get(),major_box.get(),a)
	c.execute(query,values)
	#commit changes
	conn.commit()
	fname_box.delete(0, END)
	lname_box.delete(0, END)
	major_box.delete(0, END)
	age_box.delete(0, END)

# Show all students in db function
def show_students():
	show = Tk()
	show.geometry('650x600')
	show.title("Students")
	c.execute('SELECT * FROM students ')
	global records
	records=c.fetchall()
	#label=Label(show, text="ID" + "\t\tFirst name"+ "\t\t\tLast name" + "\t\tMajor"+ "\t\tAge").pack(anchor=W)
	label=Label(show, text="First name").grid(row=0,column=0, padx=40)
	label=Label(show, text="Last name").grid(row=0,column=1, padx=40)
	label=Label(show, text="ID").grid(row=0,column=2, padx=40)
	label=Label(show, text="Major").grid(row=0,column=3, padx=40)
	label=Label(show, text="Age").grid(row=0,column=4, padx=40)
	k=0
	for student in records:
		for col in student:
			label=Label(show, text=str(col)).grid(row=1+k, column=student.index(col), padx=40)
		k+=1


# Edit/search students function
def edit_student():
	edit = Tk()
	edit.geometry('960x600')
	edit.title("Search and Edit")

	# Search query function
	
	# frame for search results
	frame2=Frame(edit)
	frame2.grid(row=2, column=0,pady=20, columnspan=8)
	def search_query():
		l=[fname_box2.get(),lname_box2.get(),ID_student.get(),major_box2.get()]
		l2=[]
		columns=["f_name","l_name","s_id","major"]
		query= "SELECT * FROM students WHERE "
		j=1 #at least there's one entry
		for i,entry in enumerate(l):
			if entry!="":
				j=0
				l2.append(entry)
				query+= columns[i]+" = "+"%s"+" AND "
		query=query[:-4]
		values=tuple(l2)
		if j!=0:
			result=[]
		else:
			c.execute(query, values)
			result=c.fetchall()

		for w in frame2.winfo_children():
			w.destroy()

		if not result:
			label=Label(frame2, text="Result not found !").pack()
		else :
			label=Label(frame2, text="First name").grid(row=0,column=0, padx=40)
			label=Label(frame2, text="Last name").grid(row=0,column=1, padx=40)
			label=Label(frame2, text="ID").grid(row=0,column=2, padx=40)
			label=Label(frame2, text="Major").grid(row=0,column=3, padx=40)
			label=Label(frame2, text="Age").grid(row=0,column=4, padx=40)
			k=0
			
			for student in result:
				for col in student:
					label=Label(frame2, text=str(col)).grid(row=1+k, column=student.index(col), padx=40)
				k+=1
				# Add edit button to edit a record
				#print(student[2])
				#Button(frame2, text="edit",font=('Hesvineca', 10), command=lambda: edit_record(k+2)).grid(row=k, column=len(student))
			def export_search():
				with open("Research_result.csv", "w", newline="") as f:
					w=csv.writer(f, dialect='excel')
					for student in result:
						w.writerow(student)
				messagebox.showinfo("Info","Search results exported!")
			def delete_user():
				id=entry_edt.get()
				response= messagebox.askokcancel("Confirm", "Are you sure you want to delete this user? ")
				if response==True:
					c.execute("DELETE FROM students WHERE s_id="+id)
					conn.commit()



			entry_edt=Entry(frame2, width=20)
			entry_edt.grid(row=1+len(result[0]), column=0, pady =40, padx=(20,5), columnspan=2)
			Button(frame2, text="Edit by ID",font=('Hesvineca', 10), command=lambda: edit_record(entry_edt.get())).grid(row=1+len(result[0]), column=1, pady=40, columnspan=2)
			Button(frame2, text="Delete by ID",font=('Hesvineca', 10), command=delete_user).grid(row=1+len(result[0]), column=2, pady=40, columnspan=2)
			Button(frame2, text="Export result",font=('Hesvineca', 10), command=export_search).grid(row=1+len(result[0]), column=4, pady=40, columnspan=1, stick=W)



		def update_query():
			query= "UPDATE students SET f_name=%s ,l_name=%s ,major= %s, age=%s WHERE s_id= "+ID_student2
			t=(fname_box3.get(), lname_box3.get(),major_box3.get(),age_box3.get())
			c.execute(query,t)
			conn.commit()
			frame3.destroy()
				
		def edit_record(id):
			global ID_student2,fname_box3,lname_box3,major_box3,age_box3, frame3
			ID_student2=id
			c.execute("SELECT * FROM students WHERE s_id= "+ str(id))
			student=c.fetchall()
			# Labels and entry boxes to update
			# frame for search results
			frame3=Frame(edit)
			frame3.grid(row=3, column=0,pady=10, columnspan=8)
			ID_student=Label(frame3, text='ID student: ',font=('Hesvineca',10)).grid(row=0, column=0, pady=10)
			ID_student3=Label(frame3,text=student[0][2] , font=('Hesvineca',10), width=10)
			ID_student3.grid(row=0, column=1,padx=(5,10), pady=10)
			#ID_student3.insert(0,student[0][2])

			fname_label=Label(frame3, text='First name: ',font=('Hesvineca',10)).grid(row=0, column=2, pady=10)
			fname_box3=Entry(frame3,font=('Hesvineca',10))
			fname_box3.grid(row=0, column=3,padx=10, pady=10)
			fname_box3.insert(0,student[0][0])
	
			lname_label=Label(frame3, text='Last name: ',font=('Hesvineca',10)).grid(row=0, column=4, pady=10)
			lname_box3=Entry(frame3,font=('Hesvineca',10))
			lname_box3.grid(row=0, column=5, pady=10,padx=10, stick='W')
			lname_box3.insert(0,student[0][1])

			lname_label=Label(frame3, text='Major: ',font=('Hesvineca',10)).grid(row=0, column=6, pady=10)
			major_box3=Entry(frame3,font=('Hesvineca',10))
			major_box3.grid(row=0, column=7, pady=10,padx=10, stick='W')
			major_box3.insert(0,student[0][3])

			lname_label=Label(frame3, text='Age: ',font=('Hesvineca',10)).grid(row=0, column=8, pady=10)
			age_box3=Entry(frame3,font=('Hesvineca',10), width=5)
			age_box3.grid(row=0, column=9, pady=10,padx=10, stick='W')
			age_box3.insert(0,student[0][4])

			# Search button
			search_butt=Button(frame3, text="UPDATE",font=('Hesvineca',15), command= update_query).grid(row=1, column=0, columnspan=8, pady=20)



	

	# Labels and entry boxes
	ID_student=Label(edit, text='ID student: ',font=('Hesvineca',10)).grid(row=0, column=0, pady=20, padx=(10,5))
	ID_student=Entry(edit,font=('Hesvineca',10))
	ID_student.grid(row=0, column=1,padx=10, pady=20)

	fname_label=Label(edit, text='First name: ',font=('Hesvineca',10)).grid(row=0, column=2, pady=20)
	fname_box2=Entry(edit,font=('Hesvineca',10))
	fname_box2.grid(row=0, column=3,padx=10, pady=20)
	
	lname_label=Label(edit, text='Last name: ',font=('Hesvineca',10)).grid(row=0, column=4, pady=20)
	lname_box2=Entry(edit,font=('Hesvineca',10))
	lname_box2.grid(row=0, column=5, pady=20,padx=10, stick='W')

	lname_label=Label(edit, text='Major: ',font=('Hesvineca',10)).grid(row=0, column=6, pady=20)
	major_box2=Entry(edit,font=('Hesvineca',10))
	major_box2.grid(row=0, column=7, pady=20,padx=10, stick='W')
	# Search button
	search_butt=Button(edit, text="SEARCH",font=('Hesvineca',15), command= search_query).grid(row=1, column=0, columnspan=8, pady=20)

# Export db function
def export_db():
	with open("database.csv", "w", newline="") as f:
		w=csv.writer(f, dialect='excel')
		for student in records:
			w.writerow(student)
	messagebox.showinfo("Info", "Database exported!")

# Add input boxes and labels
fname_label=Label(root, text='First name: ',font=('Hesvineca',15)).grid(row=0, column=0, pady=10, padx=10, stick='W')
lname_label=Label(root, text='Last name: ',font=('Hesvineca',15)).grid(row=1, column=0, pady=10, padx=10, stick='W')
major_label=Label(root, text='Major: ',font=('Hesvineca',15)).grid(row=2, column=0, pady=10, padx=10, stick='W')
age_label=Label(root, text='Age: ',font=('Hesvineca',15)).grid(row=3, column=0, pady=10, padx=10, stick='W')


fname_box=Entry(root,font=('Hesvineca',15), width=30)
fname_box.grid(row=0, column=1,padx=10, pady=10)
lname_box=Entry(root,font=('Hesvineca',15), width=30)
lname_box.grid(row=1, column=1, pady=10,padx=10, stick='W')
major_box=Entry(root,font=('Hesvineca',15), width=30)
major_box.grid(row=2, column=1, pady=10,padx=10, stick='W')
age_box=Entry(root,font=('Hesvineca',15), width=30)
age_box.grid(row=3, column=1, pady=10,padx=10, stick='W')


# ADD record button
add_butt=Button(root, text='ADD STUDENT', font=('Hesvineca',15), command=add_student).grid(row=5, column=0,columnspan=2, pady=10)

frame=Frame(root)
frame.grid(row=6, column=0,pady=20, columnspan=2)
# Search/ edit button
edit_butt=Button(frame, text='SEARCH & EDIT', font=('Hesvineca',10), command=edit_student).grid(row=0, column=0,pady=10, padx=20)

# Display all database button
show_butt=Button(frame, text='SHOW ALL', font=('Hesvineca',10), command=show_students).grid(row=0, column=1, pady=10, padx=20)

# Export database
export_butt=Button(frame, text='EXPORT DATABASE', font=('Hesvineca',10), command=export_db).grid(row=0 ,column=2, pady=10, padx=20)


root.mainloop()