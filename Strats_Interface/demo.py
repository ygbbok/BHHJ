import tkinter as tk
import math
import pyodbc

from tkinter import *
from tkinter import END
from xlrd import open_workbook

#from tkinter import tix

#from __future__ import print_function
#from os.path import join, dirname, abspath
#import xlrd
#import xlwt


#from tkinter.ttk import *

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        

    def create_widgets(self):
        #----------------------------------------
        # Poisson distribution
        #----------------------------------------
        label_Poisson = tk.Label(self, text = "Poisson Distribution:").grid(
            row = 0, column = 0)
        label_Poiss_lambda = tk.Label(self, text = '\u03bb:').grid(
            row = 1, column = 0)
        self.text_lambda = tk.Text(self, height = 2, width = 5)
        self.text_lambda.grid(row = 1, column = 1)
        label_Poiss_t = tk.Label(self, text = 't:').grid(row = 2, column = 0)
        self.text_Poiss_t = tk.Text(self, height = 1.5, width = 5)
        self.text_Poiss_t.grid(row = 2, column = 1)
        label_Poiss_n = tk.Label(self, text = 'N:').grid(row = 3, column = 0)
        self.text_Poiss_n = tk.Text(self, height = 1.5, width = 5)
        self.text_Poiss_n.grid(row = 3, column = 1)
        self.PoissCal = tk.Button(self, text = "Calculate",
                                command = self.Poiss_Cal).grid(row = 4)
        label_Poiss_P = tk.Label(self, text = 'P{N(t+s) - N(s) = n} =').grid(
            row = 5, column = 0)
        self.text_Poiss_P = tk.Text(self, height = 1.5, width = 20)
        self.text_Poiss_P.grid(row = 5,  column = 1)
        
        #----------------------------------------
        # Read Excel file
        #----------------------------------------        
        label_Excel = tk.Label(self, text = "Excel Reader:").grid(
            row = 7, column = 0)
        label_FileLoct = tk.Label(self, text
                                  = 'Please input the file path and file name:\n'
                                  + 'such as: \'D:/excel_file.xlsx\''
                                  ).grid(row = 8, column = 0)
        self.text_FilePath = tk.Text(self, height = 2, width = 50)
        self.text_FilePath.grid(row = 8, column = 1)
        self.ReadExcel = tk.Button(self, text = "Open File",
                                  command = self.OpenExcelFile).grid(row = 9)
        self.str4OpenFileResult = StringVar()
        #self.str4OpenFileResult.set("Open file result:")
        self.label_OpenFileResult = tk.Label(
            self, textvariable = self.str4OpenFileResult).grid(row = 10)

        #self.lst1 = ['Option1','Option2','Option3']
        self.Sheets_var = tk.StringVar()
        self.dropdownlist_Sheets = tk.OptionMenu(self,self.Sheets_var,'')
        self.dropdownlist_Sheets.grid(row = 11, column = 0)

        label_ExcelSheetData = tk.Label(
            self, text = "Show all the data on this sheet please click:").grid(
            row = 11, column = 1)
        self.ExcelSheetData = tk.Button(self, text = "Read all data",
                                  command = self.DataOnExcelSheet).grid(
                                      row = 12, column = 1)

        label_ExcelRow = tk.Label(self, text = 'Row:').grid(
            row = 13, column = 0)
        self.text_ExcelRow = tk.Text(self, height = 2, width = 5)
        self.text_ExcelRow.grid(row = 13, column = 1)
        label_ExcelCol = tk.Label(self, text = 'Column:').grid(
            row = 14, column = 0)
        self.text_ExcelCol = tk.Text(self, height = 1.5, width = 5)
        self.text_ExcelCol.grid(row = 14, column = 1)
        label_ExcelVal = tk.Label(self, text = 'Value:').grid(
            row = 15, column = 0)
        self.text_ExcelVal = tk.Text(self, height = 1.5, width = 20)
        self.text_ExcelVal.grid(row = 15, column = 1)
        self.ExcelGetValue = tk.Button(
            self, text = "GetValue", command = self.Excel_GetValue).grid(
                row = 16)

        #----------------------------------------
        # Connect SQL Server
        #----------------------------------------        
        label_SQL = tk.Label(self, text = "SQL Server:").grid(
            row = 17, column = 0)
        label_SQL_Server = tk.Label(self, text = 'Sever:').grid(
            row = 18, column = 0)
        self.text_SQL_Server = tk.Text(self, height = 2, width = 20)
        self.text_SQL_Server.grid(row = 18, column = 1)
        label_SQL_Database = tk.Label(self, text = 'Database:').grid(
            row = 19, column = 0)
        self.text_SQL_Database = tk.Text(self, height = 1.5, width = 20)
        self.text_SQL_Database.grid(row = 19, column = 1)

        self.CheckVar = IntVar()
        self.CB_TRST_CNNT = tk.Checkbutton(
            self, text = "Windows Authentication", variable = self.CheckVar,
            onvalue = 1, offvalue = 0, height=5, width = 20).grid(
            row = 20, column = 1)
        
        label_SQL_User = tk.Label(self, text = 'User:').grid(
            row = 21, column = 0)
        self.text_SQL_User = tk.Text(self, height = 1.5, width = 20)
        self.text_SQL_User.grid(row = 21, column = 1)
        label_SQL_PW = tk.Label(self, text = 'Password:').grid(
            row = 22, column = 0)
        self.text_SQL_PW = tk.Text(self, height = 1.5, width = 20)
        self.text_SQL_PW.grid(row = 22, column = 1)
        self.SQLConnect = tk.Button(self, text = "SQL Connect",
                                command = self.ConnectSQL).grid(row = 23)
        label_SQLQuery = tk.Label(self, text = 'SQL Query:').grid(
            row = 24, column = 0)
        self.text_SQLQuery = tk.Text(self, height = 1.5, width = 50)
        self.text_SQLQuery.grid(row = 24, column = 1)
        #self.SQLexecute = tk.Button(self, text = "Execute",
        #                        command = self.Execute).grid(row = 21)

        self.quit = tk.Button(self, text = "QUIT", fg = "red",
                              command = root.destroy).grid(row = 26)
        #self.quit.pack(side="bottom")

    def Poiss_Cal(self):
        if (self.text_lambda.get(1.0,END).strip() == '') or (
            self.text_Poiss_t.get(1.0,END).strip() == '') or (
                self.text_Poiss_n.get(1.0,END).strip() == ''):
            
            Poiss_window = tk.Toplevel()
            Poiss_window.title("Warning: Calculating Poisson Probability")
            Poiss_window.geometry("200x80")

            label_Poiss_Output = tk.Label(
                Poiss_window, text = "Please input \u03bb, t, and N.")
            label_Poiss_Output.pack(side = "top")
            
            Poiss_Okay = tk.Button(Poiss_window, text = "Okay",
                              command = Poiss_window.destroy)
            Poiss_Okay.pack(side = "bottom")
        else:
            bool_checker = True
            try:
                val_lambda = float(self.text_lambda.get(1.0,END).strip())
                val_t = float(self.text_Poiss_t.get(1.0,END).strip())
                val_n = float(self.text_Poiss_n.get(1.0,END).strip())
            except:
                bool_checker = False

            if bool_checker:
                val_P = math.exp(-1 * val_lambda * val_t) * math.pow(
                    val_lambda * val_t, val_n) / math.factorial(val_n)
                self.text_Poiss_P.delete(1.0,END)
                self.text_Poiss_P.insert(1.0, str(val_P))
                #print(str(val_P))
            else:
                Poiss_window = tk.Toplevel()
                Poiss_window.title("Warning: Calculating Poisson Probability")
                Poiss_window.geometry("250x80")

                label_Poiss_Output = tk.Label(
                    Poiss_window, text =
                    "Please make sure all the inputs are numeric.")
                label_Poiss_Output.pack(side = "top")
                #print(self.text_lambda.get(1.0,END).strip())
                #print(self.text_Poiss_t.get(1.0,END).strip())
                #print(self.text_Poiss_n.get(1.0,END).strip())
                Poiss_Okay = tk.Button(Poiss_window, text = "Okay",
                              command = Poiss_window.destroy)
                Poiss_Okay.pack(side = "bottom")
            
    def OpenExcelFile(self):
        if (self.text_FilePath.get(1.0,END).strip() == ''):
            self.str4OpenFileResult.set("File path is empty!")
        else:
            self.XLS_FILE = self.text_FilePath.get(1.0,END).strip()
            bool_checker = True
            try:
                temp_workbook = open_workbook(self.XLS_FILE)
            except:
                bool_checker = False
            if bool_checker:
                self.str4OpenFileResult.set("File is successfully found!")
                SheetsNames = temp_workbook.sheet_names()

                tempOptionMenu = self.dropdownlist_Sheets["menu"]
                tempOptionMenu.delete(0, "end")
                for tempSheetName in SheetsNames:
                    #print(tempSheetName)
                    tempOptionMenu.add_command(label = tempSheetName, 
                             command = lambda value = tempSheetName:
                                               self.Sheets_var.set(value))     
            else:
                self.str4OpenFileResult.set("File is Not found!")
        
    def DataOnExcelSheet(self):
        #print("This is the listbox!")
        SheetData_window = tk.Toplevel()
        SheetData_window.title("Data on sheet \'"
                               + self.Sheets_var.get() + "\'")
        #SheetData_window.geometry("300x250+30+30")

        tempWorkbook = open_workbook(self.XLS_FILE)
        tempExcelSheet = tempWorkbook.sheet_by_name(self.Sheets_var.get())
        #print(tempExcelSheet.nrows)
        #print(tempExcelSheet.ncols)
        max_row = 0
        for i in range(tempExcelSheet.nrows): #Rows
            for j in range(tempExcelSheet.ncols): #Columns
                ExcelData = tk.Label(SheetData_window,
                                  text = tempExcelSheet.cell(i,j).value )
                ExcelData.grid(row = i, column = j)
                max_row = i + 1

        CloseButton = tk.Button(SheetData_window, text = "CLOSE",
                              command = SheetData_window.destroy)
        CloseButton.grid(row = max_row)
        #topButton.pack(side="bottom")

    def Excel_GetValue(self):
        tempWorkbook = open_workbook(self.XLS_FILE)
        tempExcelSheet = tempWorkbook.sheet_by_name(self.Sheets_var.get())
        if (self.text_ExcelRow.get(1.0,END).strip() != '' and
                self.text_ExcelRow.get(1.0, END).strip() != ''
            and self.text_ExcelRow.get(1.0,END).strip().isdigit() and
                self.text_ExcelRow.get(1.0, END).strip().isdigit()):
            self.text_ExcelVal.delete(1.0,END)
            self.text_ExcelVal.insert(
                1.0, tempExcelSheet.cell(
                    int(self.text_ExcelRow.get(1.0, END).strip())-1,
                    int(self.text_ExcelCol.get(1.0, END).strip())-1).value)
        else:
            SQLWarning_window = tk.Toplevel()
            SQLWarning_window.title("Warning: Cannot retrieve data")
            SQLWarning_window.geometry("300x80")

            label_SQLWarning = tk.Label(
                SQLWarning_window, text =
                    "Make sure row and column numbers are entered.")
            label_SQLWarning.pack(side = "top")

            SQL_Okay = tk.Button(SQLWarning_window, text = "Okay",
                              command = SQLWarning_window.destroy)
            SQL_Okay.pack(side = "bottom")
        
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
            self.SQLexecute = tk.Button(self, text = "Execute",
                                command = self.Execute).grid(row = 25)
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
                DataList = tk.Label(SQLData, text = row)
                DataList.grid(row = i)
                i = i + 1
                #print(row)

            SQL_Okay = tk.Button(SQLData, text = "Okay",
                              command = SQLData.destroy)
            SQL_Okay.grid(row = i) 


def main():
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

if __name__ =="__main__":
    main()

