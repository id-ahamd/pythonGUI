from tkinter import *
import sqlite3 

root =Tk()
root.title("database")
root.geometry("400x600")


#Create or connect to database
#conn=sqlite3.connect('database.db')

#create cursor
#c=conn.cursor()

# execute
#c.execute(""" CREATE TABLE mytable(
#		f_name text,
#		s_name text,
#		age integer
#		)

#	""")

#commit changes
#conn.commit()

# close connection
#conn.close()

# add record function
def add():
	#Create or connect to database
	conn=sqlite3.connect('database.db')

	#create cursor
	c=conn.cursor()

	c.execute("INSERT INTO mytable VALUES (:fname, :lname, :age)",
			{
				'fname':f_name.get(),
				'lname':l_name.get(),
				'age':age.get()

			}
		)

	#commit changes
	conn.commit()

	# close connection
	conn.close()
	f_name.delete(0,END)
	l_name.delete(0,END)
	age.delete(0,END)


# Show records function
def show():

	#Create or connect to database
	conn=sqlite3.connect('database.db')

	#create cursor
	c=conn.cursor()
	c.execute("SELECT *, oid FROM mytable")
	global records
	records=c.fetchall()

	#commit changes
	conn.commit()

	# close connection
	conn.close()
	i=0
	global frame
	frame.grid_forget()
	frame=LabelFrame(root, text="All database records: ", padx=10)
	frame.grid(row=8, column=0,columnspan=2)
	for record in records:
		label_records=Label(frame, text="fname: " + record[0] + "\tlname: "+ record[1]+ "\tage: "+ str(record[2])+ "\tID : "+ str(record[3]))
		label_records.pack()
		i+=1


#Delete record by id function
def delete():
	global frame
	if id_entry.get()!="":
		#Create or connect to database
		conn=sqlite3.connect('database.db')

		#create cursor
		c=conn.cursor()
		c.execute("DELETE FROM mytable WHERE oid="+id_entry.get())
		#commit changes
		conn.commit()
		# close connection
		conn.close()
		id_entry.delete(0,END)
		frame.grid_forget()
		show()
	else: 
		frame.grid_forget()
		frame=LabelFrame(root, text="Error: ", padx=10)
		frame.grid(row=8, column=0,columnspan=2)
		label_error=Label(frame, text="Error: You have to specify an ID")
		label_error.pack()

# save record function
def save():
	#Create or connect to database
	conn=sqlite3.connect('database.db')
	#create cursor
	c=conn.cursor()
	c.execute(""" UPDATE mytable SET 
			f_name=:fname,
			s_name=:lname,
			age= :age  
			WHERE oid=:oid """,
			{
				'fname': f_name2.get(),
				'lname':l_name2.get(),
				'age':age2.get(),
				'oid': id_entry2.get()

			}
		
		)

	#commit changes
	conn.commit()
	# close connection
	conn.close()
	edit_wd.destroy()
# Edit record by id function
def edit():
	global frame
	if id_entry2.get()!="":
		#Create or connect to database
		conn=sqlite3.connect('database.db')
		#create cursor
		c=conn.cursor()
		c.execute("SELECT * FROM mytable WHERE oid="+id_entry2.get())
		reco=c.fetchall()
		if reco!=[]:
			global edit_wd
			edit_wd =Tk()
			edit_wd.title("Edit record")
			edit_wd.geometry("400x200")

			# create labels
			label_fname= Label(edit_wd, text='Fisrt name').grid(row=0, column=0, padx=30, pady=(10,0))
			label_lname= Label(edit_wd, text='Last name').grid(row=1, column=0)
			label_age= Label(edit_wd, text='Age').grid(row=2, column=0)

			# create entries
			global f_name2, l_name2, age2
			f_name2= Entry(edit_wd, width=40)
			l_name2=Entry(edit_wd, width=40)
			age2=Entry(edit_wd, width=40)
			f_name2.grid(row=0, column=1, pady=(10,0))
			l_name2.grid(row=1, column=1)
			age2.grid(row=2, column=1)

			# create save record button
			save_button=Button(edit_wd, text="SAVE RECORD", width=16, command=save)
			save_button.grid(row=3, column=0, columnspan=2, pady=10)

			record=reco[0]
			f_name2.insert(0,record[0])
			l_name2.insert(0,record[1])
			age2.insert(0,str(record[2]))
		else:
			frame.grid_forget()
			frame=LabelFrame(root, text="Error: ", padx=10)
			frame.grid(row=8, column=0,columnspan=2)
			label_error=Label(frame, text="Error: You have to specify a valid ID")
			label_error.pack()
			
			#commit changes
			conn.commit()
			# close connection
			conn.close()
			id_entry2.delete(0,END)



	else: 
		frame.grid_forget()
		frame=LabelFrame(root, text="Error: ", padx=10)
		frame.grid(row=8, column=0,columnspan=2)
		label_error=Label(frame, text="Error: You have to specify an ID")
		label_error.pack()

	
# create labels
label_fname= Label(root, text='Fisrt name').grid(row=0, column=0, padx=30, pady=(10,0))
label_lname= Label(root, text='Last name').grid(row=1, column=0)
label_age= Label(root, text='Age').grid(row=2, column=0)


# create entries
f_name= Entry(root, width=40)
l_name=Entry(root, width=40)
age=Entry(root, width=40)
f_name.grid(row=0, column=1, pady=(10,0))
l_name.grid(row=1, column=1)
age.grid(row=2, column=1)

#create add record
add_button=Button(root, text="ADD RECORD", width=16, command=add)
add_button.grid(row=3, column=0, columnspan=2, pady=10)
# create show records
add_button=Button(root, text="SHOW RECORDS", width=16, command=show)
add_button.grid(row=4, column=0, columnspan=2, pady=10)
#label_del= Label(root, text='All database records: ').grid(row=7, column=0, pady=20)
frame=LabelFrame(root, text="All database records: ", padx=10)
frame.grid(row=8, column=0,columnspan=2)


# Create delete record by id
label_del= Label(root, text='Delete record by id: ').grid(row=5, column=0)
id_entry=Entry(root, width=5)
id_entry.grid(row=6, column=0, pady=(10,20))
del_button=Button(root, text="Delete RECORD", width=35, command=delete)
del_button.grid(row=6, column=1, pady=(10,20))
# Create edit record by id
label_edit= Label(root, text='Edit record by id: ').grid(row=5, column=0)
id_entry2=Entry(root, width=5)
id_entry2.grid(row=7, column=0, pady=(10,20))
edit_button=Button(root, text="EDIT RECORD", width=35, command=edit)
edit_button.grid(row=7, column=1, pady=(10,20))

root.mainloop()

