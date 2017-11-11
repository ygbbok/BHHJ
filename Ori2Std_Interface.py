import Tkinter as tk
import math
import pyodbc

from Tkinter import *
from Tkinter import END
from xlrd import open_workbook

reload(sys)
sys.setdefaultencoding( "gb2312" )

#from tkinter import tix

#from __future__ import print_function
#from os.path import join, dirname, abspath
#import xlrd
#import xlwt


#from tkinter.ttk import *

class Application(tk.Frame):
    def __init__(self, master=None):
        #super().__init__(master)
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()
        
    def create_widgets(self):
        #----------------------------------------
        # Connect SQL Server
        #----------------------------------------
        # Define SQL Server Label
        label_SQL = tk.Label(self, text = "SQL Server:").grid(
            row = 0, column = 0)
        # Define Sever Label and Textbox
        label_SQL_Server = tk.Label(self, text = 'Sever:').grid(
            row = 1, column = 0)
        self.text_SQL_Server = tk.Text(self, height = 2, width = 20)
        self.text_SQL_Server.grid(row = 1, column = 1)
        # Define Database Label and Textbox
        label_SQL_Database = tk.Label(self, text = 'Database:').grid(
            row = 2, column = 0)
        self.text_SQL_Database = tk.Text(self, height = 1.5, width = 20)
        self.text_SQL_Database.grid(row = 2, column = 1)
        # Define Table Label and Textbox
        label_SQL_Table= tk.Label(self, text = 'Table:').grid(
            row = 3, column = 0)
        self.text_SQL_Table = tk.Text(self, height = 1.5, width = 20)
        self.text_SQL_Table.grid(row = 3, column = 1)

        # Define Windows Authentication checkbox
        self.CheckVar = IntVar()
        self.CB_TRST_CNNT = tk.Checkbutton(
            self, text = "Windows Authentication", variable = self.CheckVar,
            onvalue = 1, offvalue = 0, height=5, width = 20).grid(
            row = 4, column = 1)

        # Define User Label and Textbox
        label_SQL_User = tk.Label(self, text = 'User:').grid(
            row = 5, column = 0)
        self.text_SQL_User = tk.Text(self, height = 1.5, width = 20)
        self.text_SQL_User.grid(row = 5, column = 1)
        # Define Password Label and Textbox
        label_SQL_PW = tk.Label(self, text = 'Password:').grid(
            row = 6, column = 0)        
        self.text_SQL_PW = tk.Text(self, height = 1.5, width = 20)
        self.text_SQL_PW.grid(row = 6, column = 1)

        # Define SQL Connect Button
        self.SQLConnect = tk.Button(self, text = "SQL Connect",
                                command = self.ConnectSQL).grid(row = 7)

        
        label_SQLQuery = tk.Label(self, text = 'SQL Query:').grid(
            row = 25, column = 0)
        self.text_SQLQuery = tk.Text(self, height = 1.5, width = 50)
        self.text_SQLQuery.grid(row = 25, column = 1)
        #self.SQLexecute = tk.Button(self, text = "Execute",
        #                        command = self.Execute).grid(row = 21)

        self.quit = tk.Button(self, text = "QUIT", fg = "red",
                              command = root.destroy).grid(row = 27)
        #self.quit.pack(side="bottom")
        
    def ConnectSQL(self):
        #print(self.CheckVar.get())
        #print(self.text_SQL_Server.get(1.0, END).strip())
        #print(self.text_SQL_Database.get(1.0, END).strip())

        bool_checker = False
        if self.CheckVar.get() == 1:
            if (self.text_SQL_Server.get(1.0,END).strip() != '' and
                self.text_SQL_Database.get(1.0, END).strip() != ''):
                bool_checker = True
                try:
                    self.connection = pyodbc.connect(
                        Driver='{SQL Server}',
                        Server = self.text_SQL_Server.get(1.0, END).strip(),
                        Database = self.text_SQL_Database.get(1.0, END).strip(),
                        trusted_connection='yes')
                except:
                    bool_checker = False
        else:
            if (self.text_SQL_Server.get(1.0,END).strip() != '' and
                self.text_SQL_Database.get(1.0, END).strip() != '' and
                self.text_SQL_User.get(1.0,END).strip() != '' and
                self.text_SQL_PW.get(1.0, END).strip() != ''):
                bool_checker = True
                try:
                    self.connection = pyodbc.connect(
                        Driver='{SQL Server}',
                        Server = self.text_SQL_Server.get(1.0, END).strip(),
                        Database = self.text_SQL_Database.get(1.0, END).strip(),
                        #trusted_connection='yes'
                        uid = self.text_SQL_User.get(1.0, END).strip(),
                        pwd = self.text_SQL_PW.get(1.0, END).strip())
                except:
                    bool_checker = False
        #print(str(bool_checker))
        if bool_checker:
            self.cursor = self.connection.cursor()
            self.SQLexecute = tk.Button(self, text = "Fetch Col Names",
                                command = self.Execute).grid(row = 26)
            SQLWarning_window = tk.Toplevel()
            SQLWarning_window.title("Database connection status")
            SQLWarning_window.geometry("250x80")

            label_SQLWarning = tk.Label(
                SQLWarning_window, text =
                    "The connection of the database is success!")
            label_SQLWarning.pack(side = "top")

            SQL_Okay = tk.Button(SQLWarning_window, text = "Okay",
                              command = SQLWarning_window.destroy)
            SQL_Okay.pack(side = "bottom")
            
        else:
            SQLWarning_window = tk.Toplevel()
            SQLWarning_window.title("Warning: database connection issue")
            SQLWarning_window.geometry("250x80")

            label_SQLWarning = tk.Label(
                SQLWarning_window, text =
                    "There is an issue to connect the database.")
            label_SQLWarning.pack(side = "top")

            SQL_Okay = tk.Button(SQLWarning_window, text = "Okay",
                              command = SQLWarning_window.destroy)
            SQL_Okay.pack(side = "bottom")
                
    def Execute(self):
        if (self.text_SQLQuery.get(1.0, END).strip() != ''):
            self.cursor.execute(
                self.text_SQLQuery.get(1.0, END).strip())
            rows = self.cursor.fetchall()

            SQLData = tk.Toplevel()
            SQLData.title("SQL Query Result")

            i = 1
            for row in rows:
                DataList = tk.Label(SQLData, text = row, encoding = 'gb2312')
                DataList.grid(row = i)
                i = i + 1
                #print(row)

            SQL_Okay = tk.Button(SQLData, text = "Okay",
                              command = SQLData.destroy)
            SQL_Okay.grid(row = i) 

root = tk.Tk()
root.title("Main") # Define title

#----------------------------------------
# Button
#----------------------------------------
# Broswer to show button
# Create the application
app = Application(master=root)

# Start the program
app.mainloop()

