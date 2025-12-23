import sqlite3

con =sqlite3.connect("Contact.db")
print("Database created successfully")
crur=con.cursor()
crur.execute('drop table Contact_List;')
sql_command='''create table Contact_List(
                    Id integer primary key autoincrement,
                    Name text not null,
                    Email text unique not null,
                    Phone_no int unique,
                    Address text);'''
crur.execute(sql_command)
con.commit()
con.close()
print("Table created successfully")
