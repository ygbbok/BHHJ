#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import Tkinter as Tkinter
import os
import shutil
import pandas as pd
import numpy as np
import math
import pyodbc
import ttk as ttk


from tkinter import Tk, StringVar, ttk
from Tkinter import *
from Tkinter import END
from xlrd import open_workbook


# import Config
from IO_Util import IO_Util
from RTD_Analytics import RTD_Analytics
from Strats_Analytics import Strats_Analytics
from IO_Utilities import SQL_Util

reload(sys)
sys.setdefaultencoding( "gb2312" )

#from tkinter import tix

#from __future__ import print_function
#from os.path import join, dirname, abspath
#import xlrd
#import xlwt

class TextBoxGroup_Mgmt(Tkinter.Frame):
    def __init__(self, master=None, num_of_text_box_IN = 3):
        Tkinter.Frame.__init__(self, master)
        self.pack()
        self.num_of_text_box = num_of_text_box_IN
        self.frame = Tkinter.Frame(self)
        self.frame.pack()

        self.nodes = {}
        for i in range(1,self.num_of_text_box+1):
            temp_node = Tkinter.Entry(self.frame, width=9)
            #Tkinter.Text(self.frame, width = 9)
            temp_node.grid(row = 0, column = i-1)
            self.nodes[i] = temp_node

    def get(self, node_num):
        return self.nodes[node_num].get()

#from tkinter.ttk import *
class Application(Tkinter.Frame):
    def __init__(self, master = None):
        #super().__init__(master)
        #Frame.__init__(self, master)
        Tkinter.Frame.__init__(self, master)
        self.pack()

        #----------------------------------------
        # Settings
        #----------------------------------------
        # self.frame_Settings = Tkinter.Frame(self)
        # self.frame_Settings.pack()
        # Settings(self.frame_Settings)
        # self.pack()

        #----------------------------------------
        # RTD Settings
        #----------------------------------------
        self.frame = Tkinter.Frame(self)
        self.frame.pack()
        RTD_settings(self.frame)
        self.pack()

        #----------------------------------------
        # Strats Settings
        #----------------------------------------
        self.frame2 = Tkinter.Frame(self)
        self.frame2.pack()
        Strats_settings(self.frame2)
        self.pack()

        #----------------------------------------
        # Strats Index and Name
        #----------------------------------------
        # self.frame_Strats_Idx_Name = Tkinter.Frame(self)
        # self.frame_Strats_Idx_Name.pack()
        # Strats_Idx_Name(self.frame_Strats_Idx_Name)
        # self.pack()

        #----------------------------------------
        # Dimensions
        #----------------------------------------
        self.frame3 = Tkinter.Frame(self)
        self.frame3.pack()

        self.title_list = ["column","group_rule","strats_label"]
        self.col_num = len(self.title_list)

        self.button_frame = Tkinter.Frame(self.frame3)
        self.button_frame.pack(expand = 1, fill="both")

        # self.add_condition_button = Tkinter.Button(self.button_frame, text = "Add Condition", command = self.add_condition)
        self.add_condition_button = Tkinter.Button(self.button_frame, text = u'添加 Dimensions',command = self.add_condition,width = 12)
        self.add_condition_button.pack(side = 'left')

        self.delete_condition_button = Tkinter.Button(self.button_frame, text = u"删除 Dimensions", command = self.delete_condition,width = 12)
        self.delete_condition_button.pack(side = 'left')

        self.title_frame = Tkinter.Frame(self.frame3)
        self.title_frame.pack(expand = 1, fill="both")

        self.labels_dict = {}
        for i in range(1,self.col_num + 1):
            self.labels_dict[i] = Tkinter.Label(self.title_frame,text = self.title_list[i-1], width = 9)
            self.labels_dict[i].grid(row = 0, column = i-1)

        self.condition_num = 1
        self.conditions_dict = {}
        self.conditions_dict[1] = [None, None]
        
        self.conditions_dict[1][0] = Tkinter.Frame(self.frame3)
        self.conditions_dict[1][0].pack(expand = 1, fill="both")
        self.conditions_dict[1][1] = TextBoxGroup_Mgmt(self.conditions_dict[1][0],num_of_text_box_IN = self.col_num)
        self.conditions_dict[1][1].pack()

        self.pack()

        #----------------------------------------
        # Measures
        #----------------------------------------
        self.frame4 = Tkinter.Frame(self)
        self.frame4.pack()

        self.measure_title_list = ["column","calc_method","calc_helper","col_name","format"]
        self.measure_col_num = len(self.measure_title_list)

        self.measure_button_frame = Tkinter.Frame(self.frame4)
        self.measure_button_frame.pack(expand = 1, fill="both")

        # self.add_condition_button = Tkinter.Button(self.button_frame, text = "Add Condition", command = self.add_condition)
        self.measure_add_condition_button = Tkinter.Button(self.measure_button_frame, text = u'添加 Measures',command = self.measure_add_condition,width = 12)
        self.measure_add_condition_button.pack(side = 'left')

        self.delete_condition_button = Tkinter.Button(self.measure_button_frame, text = u"删除 Measures", command = self.measure_delete_condition,width = 12)
        self.delete_condition_button.pack(side = 'left')

        self.measure_title_frame = Tkinter.Frame(self.frame4)
        self.measure_title_frame.pack(expand = 1, fill="both")

        self.measure_labels_dict = {}
        for i in range(1,self.measure_col_num + 1):
            self.measure_labels_dict[i] = Tkinter.Label(self.measure_title_frame,text = self.measure_title_list[i-1], width = 9)
            self.measure_labels_dict[i].grid(row = 0, column = i-1)

        self.measure_condition_num = 1
        self.measure_conditions_dict = {}
        self.measure_conditions_dict[1] = [None, None]
        
        self.measure_conditions_dict[1][0] = Tkinter.Frame(self.frame4)
        self.measure_conditions_dict[1][0].pack(expand = 1, fill="both")
        self.measure_conditions_dict[1][1] = TextBoxGroup_Mgmt(self.measure_conditions_dict[1][0],num_of_text_box_IN = self.measure_col_num)
        self.measure_conditions_dict[1][1].pack()

        

        self.frame5 = Tkinter.Frame(self)
        self.frame5.pack()
        SQL_settings(self.frame5)
        
        self.pack()

    


        # if not os.path.exists(temp_strats_folder_dir):      
        #     os.makedirs(temp_strats_folder_dir)
        # else:
        #     shutil.rmtree(temp_strats_folder_dir)
        #     os.makedirs(temp_strats_folder_dir)

        # for key,value in strats_res.items():
        #     txt_file_name = temp_strats_folder_dir + "\\" + key + "_" + "strats" + '.txt'
        #     value.to_csv(txt_file_name,index = False,sep = "|",encoding = 'gb2312')


        

    def add_condition(self):
        
        self.condition_num = self.condition_num + 1
        self.conditions_dict[self.condition_num] = [None, None]
        self.conditions_dict[self.condition_num][0] = Tkinter.Frame(self.frame)
        self.conditions_dict[self.condition_num][0].pack(expand = 1, fill="both")
        self.conditions_dict[self.condition_num][1] = TextBoxGroup_Mgmt(self.conditions_dict[1][0], num_of_text_box_IN = self.col_num)
        
        self.conditions_dict[self.condition_num][1].pack()


    def delete_condition(self):
        
        self.conditions_dict[self.condition_num][0].destroy()
        self.conditions_dict[self.condition_num][1].destroy()
        self.conditions_dict[self.condition_num] = [None, None]
        self.condition_num = self.condition_num - 1

    def measure_add_condition(self):
        
        self.measure_condition_num = self.measure_condition_num + 1
        self.measure_conditions_dict[self.measure_condition_num] = [None, None]
        self.measure_conditions_dict[self.measure_condition_num][0] = Tkinter.Frame(self.frame)
        self.measure_conditions_dict[self.measure_condition_num][0].pack(expand = 1, fill="both")
        self.measure_conditions_dict[self.measure_condition_num][1] = TextBoxGroup_Mgmt(self.measure_conditions_dict[1][0],num_of_text_box_IN = self.measure_col_num)
        
        self.conditions_dict[self.condition_num][1].pack()


    def measure_delete_condition(self):
        
        self.measure_conditions_dict[self.measure_condition_num][0].destroy()
        self.measure_conditions_dict[self.measure_condition_num][1].destroy()
        self.measure_conditions_dict[self.measure_condition_num] = [None, None]
        self.measure_condition_num = self.measure_condition_num - 1
    
    def get_all(self,dict_type = False):
        if dict_type:
            self.res = []
            for i in range(1,self.condition_num + 1):
                temp = {}
                for j in range(1,self.conditions_dict[i][1].num_of_text_box + 1):
                    temp[self.title_list[j-1]] = self.conditions_dict[i][1].get(j)
                self.res.append(temp)
        else:
            self.res = {}
            for i in range(1,self.condition_num + 1):
                temp = []
                for j in range(1,self.conditions_dict[i][1].num_of_text_box + 1):
                    temp.append(self.conditions_dict[i][1].get(j))
                self.res[i] = temp

    
        #ConditionGroup_Mgmt(self.frame3)
        # self.condition_num = 3
        # self.conditions_dict = {}
        # self.conditions_dict[1] = [None, None]

        # self.conditions_dict[1][0] = Tkinter.Frame(self.frame)
        # self.conditions_dict[1][0].pack(expand = 1, fill="both")
        # self.conditions_dict[1][1] = RTD_settings(self.conditions_dict[1][0])
        # self.conditions_dict[1][1].pack()
        # self.conditions_dict[2][0] = Tkinter.Frame(self.frame)
        # self.conditions_dict[2][0].pack(expand = 1, fill="both")
        # self.conditions_dict[2][1] = Strats_settings(self.conditions_dict[1][0])
        # self.conditions_dict[2][1].pack()
        #self.create_widgets()

        # self.frame = Tkinter.Frame(self)
        # self.frame.pack()


class Settings(Application):
    def __init__(self, master = None):
        Tkinter.Frame.__init__(self, master)
        self.pack()
        self.frame = Tkinter.Frame(self)
        self.frame.pack()
        #----------------------------------------
        # General Settings
        #----------------------------------------
        # Define General Settings Label
        self.label_General_Settings = Tkinter.Label(self.frame, text = "General Settings:")
        self.label_General_Settings.pack(side = TOP)
        # Define Dimensions_Settings_Input_File Label and Textbox
        self.label_Dime_Settings_Input_File = Tkinter.Label(self.frame, text = "Dimensions_Settings_Input_File:")
        self.label_Dime_Settings_Input_File.pack()
        self.text_Dime_Settings_Input_File = Tkinter.Text(self.frame, height = 1, width = 12)
        self.text_Dime_Settings_Input_File.pack()
        # Define Measures_Settings_Input_File Label and Textbox
        self.label_Meas_Settings_Input_File = Tkinter.Label(self.frame, text = 'Measures_Settings_Input_File:')
        self.label_Meas_Settings_Input_File.pack()
        self.text_Meas_Settings_Input_File = Tkinter.Text(self.frame, height = 1, width = 12)
        self.text_Meas_Settings_Input_File.pack()
        # Define rules_mapping_file Label and Textbox
        self.label_rules_mapping_file = Tkinter.Label(self.frame, text = 'rules_mapping_file:')
        self.label_rules_mapping_file.pack()
        self.text_rules_mapping_file = Tkinter.Text(self.frame, height = 1, width = 12)
        self.text_rules_mapping_file.pack()
        

        # #self.argstr = self.text_RT_Dir.get(1.0,END).strip()  + "|" + self.text_Temp_RTD_txt.get(1.0,END).strip()
        # self.argstr = "E:\BHHJ\Strats_Analytics\Data\chinatopcredit.CashLoan.20m.loantape.csv|E:\BHHJ\Strats_Analytics\\temp\\temp_rtd.txt"
        # #self.argstr = self.text_RT_Dir.get() + "|"
        # #print self.text_RT_Dir.get()
        # self.button_Run_RTD = Tkinter.Button(self.frame, text = u'Run RTD',
        #     # Run_RTD(["E:\BHHJ\Strats_Analytics\Data\chinatopcredit.CashLoan.20m.loantape.csv|E:\BHHJ\Strats_Analytics\\temp\\temp_rtd.txt"]
        #     #command = self.Run_RTD(["E:\BHHJ\Strats_Analytics\Data\chinatopcredit.CashLoan.20m.loantape.csv|E:\BHHJ\Strats_Analytics\\temp\\temp_rtd.txt"]),
        #     command = self.Run_RTD,
        #     width = 12)
        # #self.frame_Run_RTD.pack(expand = 1, fill="both")
        # self.button_Run_RTD.pack()

class RTD_settings(Application):
    def __init__(self, master=None):
        Tkinter.Frame.__init__(self, master)
        self.pack()
        self.frame = Tkinter.Frame(self)
        self.frame.pack()
        #----------------------------------------
        # RTD Settings
        #----------------------------------------
        # Define RTD Settings Label
        self.label_RTD_Settings = Tkinter.Label(self.frame, text = "RTD Procedures Parameters Settings:")
        #label_RTD_Settings.grid(row = 0, column = 0)
        self.label_RTD_Settings.pack(side = TOP)
        # Define RT_Dir Label and Textbox
        self.label_RT_Dir = Tkinter.Label(self.frame, text = 'RT Dir:')
        #label_RT_Dir.grid(row = 1, column = 0)
        self.label_RT_Dir.pack()
        self.text_RT_Dir = Tkinter.Text(self.frame, height = 1, width = 12)
        #self.text_RT_Dir = Tkinter.Entry(self.frame, width = 12)
        #self.text_RT_Dir.grid(row = 1, column = 1)
        self.text_RT_Dir.pack()
        # Define Temp RTD txt Label and Textbox
        self.label_Temp_RTD_txt = Tkinter.Label(self.frame, text = 'Temp RTD txt:')
        self.label_Temp_RTD_txt.pack()
        #label_Temp_RTD_txt.grid(row = 2, column = 0)
        self.text_Temp_RTD_txt = Tkinter.Text(self.frame, height = 1, width = 12)
        #self.text_Temp_RTD_txt.grid(row = 2, column = 1)
        self.text_Temp_RTD_txt.pack()
        # Define RTD txt Label and Textbox
        self.label_RTD_txt = Tkinter.Label(self.frame, text = 'RTD txt:')
        self.label_RTD_txt.pack()
        self.text_RTD_txt = Tkinter.Text(self.frame, height = 1, width = 12)
        self.text_RTD_txt.pack()
        #self.text_RTD_txt.grid(row = 3, column = 1)
        # Define Read from Existing? txt Label and Combobox
        self.label_RfE = Tkinter.Label(self.frame, text = 'Read from Existing?:')
        self.label_RfE.pack()
        self.combobox_RfE = ttk.Combobox(self.frame)
        self.combobox_RfE['values'] = ('Yes', 'No')
        #self.combobox_RfE.grid(row = 4, column = 1)
        self.combobox_RfE.pack()

        #self.argstr = self.text_RT_Dir.get(1.0,END).strip()  + "|" + self.text_Temp_RTD_txt.get(1.0,END).strip()
        self.argstr = "E:\BHHJ\Strats_Analytics\Data\chinatopcredit.CashLoan.20m.loantape.csv|E:\BHHJ\Strats_Analytics\\temp\\temp_rtd.txt"
        #self.argstr = self.text_RT_Dir.get() + "|"
        #print self.text_RT_Dir.get()
        self.button_Run_RTD = Tkinter.Button(self.frame, text = u'Run RTD',
            # Run_RTD(["E:\BHHJ\Strats_Analytics\Data\chinatopcredit.CashLoan.20m.loantape.csv|E:\BHHJ\Strats_Analytics\\temp\\temp_rtd.txt"]
            #command = self.Run_RTD(["E:\BHHJ\Strats_Analytics\Data\chinatopcredit.CashLoan.20m.loantape.csv|E:\BHHJ\Strats_Analytics\\temp\\temp_rtd.txt"]),
            command = self.Run_RTD,
            width = 12)
        #self.frame_Run_RTD.pack(expand = 1, fill="both")
        self.button_Run_RTD.pack()

    def Run_RTD(self):
        if (self.text_RT_Dir.get(1.0,END).strip() != ''
            and self.text_Temp_RTD_txt.get(1.0,END).strip() != ''):
            # print self.text_RT_Dir.get(1.0,END).strip()
            # print self.text_Temp_RTD_txt.get(1.0,END).strip()

            file_dir = self.text_RT_Dir.get(1.0,END).strip()
            rtd_txt_dir = self.text_Temp_RTD_txt.get(1.0,END).strip()

            df = pd.read_csv(file_dir, sep = ',')
            RTD_Analytics_instance = RTD_Analytics(df)
            rtd_res = RTD_Analytics_instance.analytics_procedure()
            IO_Util.output_to_txt(rtd_res, rtd_txt_dir)


        # if not os.path.exists(temp_strats_folder_dir):      
        #     os.makedirs(temp_strats_folder_dir)
        # else:
        #     shutil.rmtree(temp_strats_folder_dir)
        #     os.makedirs(temp_strats_folder_dir)

        # for key,value in strats_res.items():
        #     txt_file_name = temp_strats_folder_dir + "\\" + key + "_" + "strats" + '.txt'
        #     value.to_csv(txt_file_name,index = False,sep = "|",encoding = 'gb2312')


        df = pd.read_csv(file_dir, sep = ',')
        RTD_Analytics_instance = RTD_Analytics(df)
        rtd_res = RTD_Analytics_instance.analytics_procedure()
        IO_Util.output_to_txt(rtd_res, rtd_txt_dir)

class Strats_settings(Application):
    def __init__(self, master=None):
        Tkinter.Frame.__init__(self, master)
        self.pack()
        self.frame = Tkinter.Frame(self)
        self.frame.pack()

        self.label_General_Settings = Tkinter.Label(self.frame, text = "General Settings:")
        self.label_General_Settings.pack(side = TOP)
        # Define Dimensions_Settings_Input_File Label and Textbox
        self.label_Dime_Settings_Input_File = Tkinter.Label(self.frame, text = "Dimensions_Settings_Input_File:")
        self.label_Dime_Settings_Input_File.pack()
        self.text_Dime_Settings_Input_File = Tkinter.Text(self.frame, height = 1, width = 12)
        self.text_Dime_Settings_Input_File.pack()
        # Define Measures_Settings_Input_File Label and Textbox
        self.label_Meas_Settings_Input_File = Tkinter.Label(self.frame, text = 'Measures_Settings_Input_File:')
        self.label_Meas_Settings_Input_File.pack()
        self.text_Meas_Settings_Input_File = Tkinter.Text(self.frame, height = 1, width = 12)
        self.text_Meas_Settings_Input_File.pack()
        # Define rules_mapping_file Label and Textbox
        self.label_rules_mapping_file = Tkinter.Label(self.frame, text = 'rules_mapping_file:')
        self.label_rules_mapping_file.pack()
        self.text_rules_mapping_file = Tkinter.Text(self.frame, height = 1, width = 12)
        self.text_rules_mapping_file.pack()

        #----------------------------------------
        # Strats Procedures Parameters Settings
        #----------------------------------------
        # Define Strats Settings Label
        self.label_Strats_Settings = Tkinter.Label(self.frame, text = "Strats Procedures Parameters Settings:")
        #label_Strats_Settings.grid(row = 5, column = 0)
        self.label_Strats_Settings.pack(side = TOP)
        # Define Strats RT Dir Label and Textbox
        self.label_Strats_RT_Dir = Tkinter.Label(self.frame, text = 'RT Dir:')
        #label_Strats_RT_Dir.grid(row = 6, column = 0)
        self.label_Strats_RT_Dir.pack()
        self.text_Strats_RT_Dir = Tkinter.Text(self.frame, height = 1, width = 12)
        #self.text_Strats_RT_Dir.grid(row = 6, column = 1)
        self.text_Strats_RT_Dir.pack()
        # Define Temp Strats FolderLabel and Textbox
        self.label_Temp_Strats_Folder = Tkinter.Label(self.frame, text = 'Temp Strats Folder:')
        self.label_Temp_Strats_Folder.pack()
        #self.label_Temp_Strats_Folder.grid(row = 7, column = 0)
        self.text_Temp_Strats_Folder = Tkinter.Text(self.frame, height = 1, width = 12)
        self.text_Temp_Strats_Folder.pack()
        #self.text_Temp_Strats_Folder.grid(row = 7, column = 1)
        # Define Strats Folder Label and Textbox
        self.label_Strats_Folder = Tkinter.Label(self.frame, text = 'Strats Folder:')
        #.grid(row = 8, column = 0)
        self.label_Strats_Folder.pack()
        self.text_Strats_Folder = Tkinter.Text(self.frame, height = 1, width = 12)
        #self.text_Strats_Folder.grid(row = 8, column = 1)
        self.text_Strats_Folder.pack()
        # Define Strats Sort By Label and Textbox
        self.label_Sort_By = Tkinter.Label(self.frame, text = 'Sort By:')
        #.grid(row = 9, column = 0)
        self.label_Sort_By.pack()
        self.text_Sort_By = Tkinter.Text(self.frame, height = 1, width = 12)
        #self.text_Sort_By.grid(row = 9, column = 1)
        self.text_Sort_By.pack()
        # Define Display Top N Label and Textbox
        self.label_Display_Top_N = Tkinter.Label(self.frame, text = 'Display Top N:')
        #.grid(row = 10, column = 0)
        self.label_Display_Top_N.pack()
        self.text_Display_Top_N = Tkinter.Text(self.frame, height = 1, width = 12)
        #self.text_Display_Top_N.grid(row = 10, column = 1)
        self.text_Display_Top_N.pack()
        # Define Read from Existing? txt Label and Combobox
        self.label_Strats_RfE = Tkinter.Label(self.frame, text = 'Read from Existing?:')
        #.grid(row = 11, column = 0)
        self.label_Strats_RfE.pack()
        self.combobox_Strats_RfE = ttk.Combobox(self.frame)
        self.combobox_Strats_RfE['values'] = ('Yes', 'No')
        #self.combobox_Strats_RfE.grid(row = 11, column = 1)
        self.combobox_Strats_RfE.pack()

        #argstr = "E:\BHHJ\Strats_Analytics\Settings_Files\dimensions_settings.txt|E:\BHHJ\Strats_Analytics\Settings_Files\measures_settings.txt|E:\BHHJ\Strats_Analytics\Settings_Files\\rules_mapping.txt|E:\BHHJ\Strats_Analytics\Data\chinatopcredit.CashLoan.20m.loantape.csv|E:\BHHJ\Strats_Analytics\\temp\\temp_strats"
        self.button_Run_Strats = Tkinter.Button(self.frame, text = u'Run Strats',
            # Run_RTD(["E:\BHHJ\Strats_Analytics\Data\chinatopcredit.CashLoan.20m.loantape.csv|E:\BHHJ\Strats_Analytics\\temp\\temp_rtd.txt"]
            command = self.Run_Strats,
            width = 12)
        #self.frame_Run_RTD.pack(expand = 1, fill="both")
        self.button_Run_Strats.pack()


        self.frame_Strats_Idx = Tkinter.Frame(self)
        self.frame_Strats_Idx.pack()
        self.label_Strats_Idx = Tkinter.Label(self.frame_Strats_Idx, text = "Strats Index:")
        self.label_Strats_Idx.pack(side = LEFT)

        sql_query = "SELECT [Strats_Idx] FROM [Strats_Idx_Name]"
        res_list = SQL_Util.query_sql_procedure(sql_query, 1)
        strats_idx =  res_list[0]['Strats_Idx'].values
    
        self.Static_strVar = Tkinter.StringVar()
        strVar = ''
        for i in range(0, strats_idx.size):
            strVar = strVar + str(strats_idx[i]) + ' '

        self.combobox_Strats_Idx = ttk.Combobox(self.frame_Strats_Idx, textvariable = self.Static_strVar)
        self.combobox_Strats_Idx['values'] = strVar
        self.combobox_Strats_Idx.pack(side = RIGHT)
        
        # Define Strats Index Select Button
        self.SQLConnect = Tkinter.Button(self.frame_Strats_Idx, text = "Select",
                                command = self.strats_idx_select)
        self.SQLConnect.pack(side = BOTTOM)
        
        self.frame_Strats_Name = Tkinter.Frame(self)
        self.frame_Strats_Name.pack()
        self.label_Strats_Name = Tkinter.Label(self.frame_Strats_Name, text = "Strats Name:")
        self.label_Strats_Name.pack(side = LEFT)

        self.strats_name_strVar = StringVar()
        self.label_Strats_Name_text = Tkinter.Label(self.frame_Strats_Name, textvariable = self.strats_name_strVar)
        self.label_Strats_Name_text.pack(side = RIGHT)

    def Run_Strats(self):
        #args_list = args[0].split("|")
        
        # sett = Settings()
        # if (sett.text_Dime_Settings_Input_File.get(1.0,END).strip() != ''
        #     and sett.text_Meas_Settings_Input_File.get(1.0,END).strip() != ''
        #     and sett.text_rules_mapping_file.get(1.0,END).strip() != ''
        #     and self.text_Strats_RT_Dir.get(1.0,END).strip() != ''
        #     and self.text_Temp_Strats_Folder.get(1.0,END).strip() != ''):
        if (self.text_Dime_Settings_Input_File.get(1.0,END).strip() != ''
            and self.text_Meas_Settings_Input_File.get(1.0,END).strip() != ''
            and self.text_rules_mapping_file.get(1.0,END).strip() != ''
            and self.text_Strats_RT_Dir.get(1.0,END).strip() != ''
            and self.text_Temp_Strats_Folder.get(1.0,END).strip() != ''):
            #sett = Settings()
            dimensions_settings_file_dir = self.text_Dime_Settings_Input_File.get(1.0,END).strip() 
            measures_settings_file_dir = self.text_Meas_Settings_Input_File.get(1.0,END).strip()
            rules_mapping_file_dir = self.text_rules_mapping_file.get(1.0,END).strip()
            strats_raw_tape_dir = self.text_Strats_RT_Dir.get(1.0,END).strip()
            temp_strats_folder_dir = self.text_Temp_Strats_Folder.get(1.0,END).strip()
            
            df = IO_Util.read_csv(strats_raw_tape_dir, sep = ',')

            dimensions_settings = IO_Util.read_csv(dimensions_settings_file_dir, sep="|")
            measures_settings = IO_Util.read_csv(measures_settings_file_dir, sep="|")
            rules_mapping = IO_Util.read_csv(rules_mapping_file_dir, sep="|")
            Strats_Analytics_instance = Strats_Analytics(df,dimensions_settings,measures_settings,rules_mapping)

            Strats_Analytics_instance.run_tape_extension_procedure()
            
            strats_res = Strats_Analytics_instance.analytics_procedure()
            # sys.exit(0)

            if not os.path.exists(temp_strats_folder_dir):      
                os.makedirs(temp_strats_folder_dir)
            else:
                shutil.rmtree(temp_strats_folder_dir)
                os.makedirs(temp_strats_folder_dir)

            for key,value in strats_res.items():
                txt_file_name = temp_strats_folder_dir + "\\" + key + "_" + "strats" + '.txt'
                value.to_csv(txt_file_name,index = False,sep = "|",encoding = 'gb2312')

    def strats_idx_select(self):
        if (self.combobox_Strats_Idx.get() != ''):
            sql_query = "SELECT * FROM [Strats_Idx_Name] WHERE [Strats_Idx] = " + self.combobox_Strats_Idx.get()
            res_list = SQL_Util.query_sql_procedure(sql_query, 1)
            strats_name =  res_list[0]['Strats_Name'].values
            self.strats_name_strVar.set(strats_name[0])

            sql_query = "SELECT [Dime_Ori_Label] AS 'column', t_b.Rule_Name AS group_rule, [Dime_Std_Label] AS strats_label FROM [Dimensions] t_a LEFT JOIN (SELECT DISTINCT([Rule_Name]), Rule_Idx FROM [Strats_GroupRule_Mapping]) t_b ON t_a.[Rule_Idx] = t_b.[Rule_Idx] WHERE [Strats_Idx] = " + self.combobox_Strats_Idx.get()
            dimensions_list = SQL_Util.query_sql_procedure(sql_query, 1)

            Dimensions_Settings_Input_File = self.text_Dime_Settings_Input_File.get(1.0,END).strip() 
            for item in dimensions_list:
                item.to_csv(Dimensions_Settings_Input_File,index = False,sep = "|",encoding = 'gb2312')

            sql_query = "SELECT [Meas_Ori_Label] AS 'column', t_b.Calc_Method_Name AS calc_method, [calc_helper], [Meas_Std_Label] AS col_name, [format] FROM [Measures] t_a LEFT JOIN [Calc_Method] t_b ON t_a.Calc_Method_Idx = t_b.Calc_Method_Idx WHERE [Strats_Idx] = " + self.combobox_Strats_Idx.get()
            measures_list = SQL_Util.query_sql_procedure(sql_query, 1)

            Measures_Settings_Input_File = self.text_Meas_Settings_Input_File.get(1.0,END).strip() 
            for item in measures_list:
                item.to_csv(Measures_Settings_Input_File,index = False,sep = "|",encoding = 'gb2312')

            sql_query = "SELECT [Rule_Name], [Lower_Bound], [Upper_Bound], [Label] FROM [Strats_GroupRule_Mapping]"
            rules_list = SQL_Util.query_sql_procedure(sql_query, 1)

            rules_mapping_file = self.text_rules_mapping_file.get(1.0,END).strip() 
            for item in rules_list:
                item.to_csv(rules_mapping_file,index = False,sep = "|",encoding = 'gb2312')


class Strats_Idx_Name(Application):
    def __init__(self, master = None):
        Tkinter.Frame.__init__(self, master)
        self.pack()
        self.frame_Strats_Idx = Tkinter.Frame(self)
        self.frame_Strats_Idx.pack()
        self.label_Strats_Idx = Tkinter.Label(self.frame_Strats_Idx, text = "Strats Index:")
        self.label_Strats_Idx.pack(side = LEFT)

        sql_query = "SELECT [Strats_Idx] FROM [Strats_Idx_Name]"
        res_list = SQL_Util.query_sql_procedure(sql_query, 1)
        strats_idx =  res_list[0]['Strats_Idx'].values
    
        self.Static_strVar = Tkinter.StringVar()
        strVar = ''
        for i in range(0, strats_idx.size):
            strVar = strVar + str(strats_idx[i]) + ' '

        self.combobox_Strats_Idx = ttk.Combobox(self.frame_Strats_Idx, textvariable = self.Static_strVar)
        self.combobox_Strats_Idx['values'] = strVar
        self.combobox_Strats_Idx.pack(side = RIGHT)
        
        # Define Strats Index Select Button
        self.SQLConnect = Tkinter.Button(self.frame_Strats_Idx, text = "Select",
                                command = self.strats_idx_select)
        self.SQLConnect.pack(side = BOTTOM)
        
        self.frame_Strats_Name = Tkinter.Frame(self)
        self.frame_Strats_Name.pack()
        self.label_Strats_Name = Tkinter.Label(self.frame_Strats_Name, text = "Strats Name:")
        self.label_Strats_Name.pack(side = LEFT)

        self.strats_name_strVar = StringVar()
        self.label_Strats_Name_text = Tkinter.Label(self.frame_Strats_Name, textvariable = self.strats_name_strVar)
        self.label_Strats_Name_text.pack(side = RIGHT)

        

    def strats_idx_select(self):
        if (self.combobox_Strats_Idx.get() != ''):
            sql_query = "SELECT * FROM [Strats_Idx_Name] WHERE [Strats_Idx] = " + self.combobox_Strats_Idx.get()
            res_list = SQL_Util.query_sql_procedure(sql_query, 1)
            strats_name =  res_list[0]['Strats_Name'].values
            self.strats_name_strVar.set(strats_name[0])

            sql_query = "SELECT [Dime_Ori_Label], [Dime_Std_Label], [Rule_Idx], [Strats_Idx] FROM [Strats_Analytics].[dbo].[Dimensions] WHERE [Strats_Idx] = " + self.combobox_Strats_Idx.get()
            dimensions_list = SQL_Util.query_sql_procedure(sql_query, 1)
            print res_list

            Dimensions_Settings_Input_File = self.text_Dime_Settings_Input_File.get(1.0,END).strip() 
            for key,value in dimensions_list.items():
                value.to_csv(Dimensions_Settings_Input_File,index = False,sep = "|",encoding = 'gb2312')
        
        #print res_list

class SQL_settings(Application):
    def __init__(self, master=None):
        Tkinter.Frame.__init__(self, master)
        self.pack()
        self.frame = Tkinter.Frame(self)
        self.frame.pack()
        #----------------------------------------
        # Connect SQL Server
        #----------------------------------------
        # Define SQL Driver Label and Combobox
        self.frame_SQL_Driver = Tkinter.Frame(self)
        self.frame_SQL_Driver.pack()
        self.label_SQL_Driver = Tkinter.Label(self.frame_SQL_Driver, text = "SQL Driver:")
        self.label_SQL_Driver.pack(side = LEFT)
        self.combobox_SQL_Driver = ttk.Combobox(self.frame_SQL_Driver)
        self.combobox_SQL_Driver['values'] = ('{SQL Server Native Client 11.0}', 'SQLOLEDB', '{SQL Server}')
        self.combobox_SQL_Driver.pack(side = RIGHT)
        # Define Sever Label and Combobox
        self.label_SQL_Server = Tkinter.Label(self.frame, text = 'Sever:')
        self.label_SQL_Server.pack()
        self.combobox_SQL_Server = ttk.Combobox(self.frame)
        self.combobox_SQL_Server['values'] = ('(localdb)\MSSQLLocalDB', 'liuxiao-PC')
        self.combobox_SQL_Server.pack()
        # Define Database Label and Combobox
        self.label_SQL_Database = Tkinter.Label(self.frame, text = 'Database:')
        self.label_SQL_Database.pack()
        self.combobox_SQL_Database = ttk.Combobox(self.frame)
        self.combobox_SQL_Database['values'] = ('Strats_Analytics')
        self.combobox_SQL_Database.pack()


        # Define Windows Authentication checkbox
        self.CheckVar = IntVar()
        self.CB_TRST_CNNT = Tkinter.Checkbutton(
            self, text = "Windows Authentication", variable = self.CheckVar,
            onvalue = 1, offvalue = 0, height=5, width = 20)
        self.CB_TRST_CNNT.pack()

        # Define User Label and Textbox
        self.label_SQL_User = Tkinter.Label(self, text = 'User:')
        self.label_SQL_User.pack()

        self.text_SQL_User = Tkinter.Text(self, height = 1.5, width = 20)
        self.text_SQL_User.pack()
        # Define Password Label and Textbox
        self.label_SQL_PW = Tkinter.Label(self, text = 'Password:')
        self.label_SQL_PW.pack()      
        self.text_SQL_PW = Tkinter.Text(self, height = 1.5, width = 20)
        self.text_SQL_PW.pack()

        # Define SQL Connect Button
        self.SQLConnect = Tkinter.Button(self, text = "SQL Connect",
                                command = self.ConnectSQL)
        self.SQLConnect.pack()

        
        self.frame_Query_Execute = Tkinter.Frame(self)
        self.frame_Query_Execute.pack()
        self.label_SQLQuery = Tkinter.Label(self.frame_Query_Execute, text = 'SQL Query:')
        self.label_SQLQuery.pack(side = LEFT)
        self.text_SQLQuery = Tkinter.Text(self.frame_Query_Execute, height = 1.5, width = 50)
        self.text_SQLQuery.pack(side = RIGHT)
        self.SQLexecute = Tkinter.Button(self.frame_Query_Execute, text = "Execute",
                               command = self.Execute)
        self.SQLexecute.pack(side = BOTTOM)

        
        #self.quit.pack(side="bottom")



    def ConnectSQL(self):
        #print(self.CheckVar.get())
        #print(self.combobox_SQL_Server.get())
        #print(self.combobox_SQL_Database.get())

        bool_checker = False
        if self.CheckVar.get() == 1:
            if (self.combobox_SQL_Server.get() != '' and
                self.combobox_SQL_Database.get() != ''):
                bool_checker = True
                try:
                    self.connection = pyodbc.connect(
                        Driver = self.combobox_SQL_Driver.get(),
                        Server = self.combobox_SQL_Server.get(),
                        Database = self.combobox_SQL_Database.get(),
                        trusted_connection='yes')
                except:
                    bool_checker = False
        else:
            if (self.combobox_SQL_Driver.get() != '' and
                self.combobox_SQL_Server.get() != '' and
                self.combobox_SQL_Database.get() != '' and
                self.text_SQL_User.get(1.0,END).strip() != '' and
                self.text_SQL_PW.get(1.0, END).strip() != ''):
                bool_checker = True
                try:
                    self.connection = pyodbc.connect(
                        Driver = self.combobox_SQL_Driver.get(),
                        Server = self.combobox_SQL_Server.get(),
                        Database = self.combobox_SQL_Database.get(),
                        #trusted_connection='yes'
                        uid = self.text_SQL_User.get(1.0, END).strip(),
                        pwd = self.text_SQL_PW.get(1.0, END).strip())
                except:
                    bool_checker = False
        #print(str(bool_checker))
        if bool_checker:
            self.cursor = self.connection.cursor()
            # self.SQLexecute = Tkinter.Button(self, text = "Fetch Col Names",
            #                     command = self.Execute).grid(row = 26)
            SQLWarning_window = Tkinter.Toplevel()
            SQLWarning_window.title("Database connection status")
            SQLWarning_window.geometry("250x80")

            label_SQLWarning = Tkinter.Label(
                SQLWarning_window, text =
                    "The connection of the database is success!")
            label_SQLWarning.pack(side = "top")

            SQL_Okay = Tkinter.Button(SQLWarning_window, text = "Okay",
                              command = SQLWarning_window.destroy)
            SQL_Okay.pack(side = "bottom")
            
        else:
            SQLWarning_window = Tkinter.Toplevel()
            SQLWarning_window.title("Warning: database connection issue")
            SQLWarning_window.geometry("250x80")

            label_SQLWarning = Tkinter.Label(
                SQLWarning_window, text =
                    "There is an issue to connect the database.")
            label_SQLWarning.pack(side = "top")

            SQL_Okay = Tkinter.Button(SQLWarning_window, text = "Okay",
                              command = SQLWarning_window.destroy)
            SQL_Okay.pack(side = "bottom")
                
    def Execute(self):
        if (self.text_SQLQuery.get(1.0, END).strip() != ''):
            sql_script_IN = "set nocount on\n " + self.text_SQLQuery.get(1.0, END).strip()
            res_list = SQL_Util.query_sql_procedure(sql_script_IN, 2)
            print res_list
        # table_res_IN = 2
        # sql_script_IN = self.text_SQLQuery.get(1.0, END).strip()
        # if table_res_IN > 0:
        #     sql_script = "set nocount on\n"
        #     con = pyodbc.connect(
        #         Driver = self.combobox_SQL_Driver.get(),
        #         #Driver = '{SQL Server Native Client 11.0}',
        #         Host= self.combobox_SQL_Server.get(),
        #         Database = self.combobox_SQL_Database.get(),
        #         trusted_connection='yes')
        #     cursor = con.cursor()
        #     sql_script = sql_script + sql_script_IN

        #     cursor.execute(sql_script)
        #     # cursor.commit()

        #     res_list = []

        #     # cursor.commit()
        #     # cursor.nextset()
        #     # rows = cursor.fetchall()

        #     print "test_begin"
        #     print "test_end"
        #     for i in range(1,table_res_IN+1):
        #         if i > 1: cursor.nextset()
        #         cursor.commit()
        #         rows = cursor.fetchall()
        #         col = [item[0] for item in cursor.description]
        #         df = pd.DataFrame(data = [tuple(row_item) for row_item in rows],columns = col)

        #         res_list.append(df)

        #     con.close()
        #     print res_list

        # elif table_res_IN == 0:
        #     con = pyodbc.connect(
        #         #Driver = self.combobox_SQL_Driver.get(),
        #         Driver = '{SQL Server Native Client 11.0}',
        #         host = self.combobox_SQL_Server.get(),
        #         Database = self.combobox_SQL_Database.get(),
        #         trusted_connection='yes')
        #     cursor = con.cursor()
        #     sql_script = sql_script_IN
        #     cursor.execute(sql_script)
        #     cursor.commit()
        #     con.close()

        # if (self.text_SQLQuery.get(1.0, END).strip() != ''):
        #     self.cursor.execute(
        #         self.text_SQLQuery.get(1.0, END).strip())
        #     rows = self.cursor.fetchall()

        #     SQLData = Tkinter.Toplevel()
        #     SQLData.title("SQL Query Result")

        #     res_list = []
        #     i = 1
        #     for row in rows:
        #         col = [item[0] for item in self.cursor.description]
        #         df = pd.DataFrame(data = [tuple(row_item) for row_item in rows],columns = col)
        #         res_list.append(df)

        #         DataList = Tkinter.Label(SQLData, text = row)
        #         DataList.grid(row = i)
        #         i = i + 1
        #         #print(row)

        #     print df

        #     SQL_Okay = Tkinter.Button(SQLData, text = "Okay",
        #                       command = SQLData.destroy)
        #     SQL_Okay.grid(row = i) 


if True:
    root = Tkinter.Tk()
    root.title("Main") # Define title

    #----------------------------------------
    # Button
    #----------------------------------------
    # Broswer to show button
    # Create the application
    app = Application(master=root)

    # Start the program
    app.mainloop()

if False:
    sql_script_IN = "select " + " TOP 1*  FROM [Strats_Analytics].[dbo].[Calc_Method]"
    
    SQL_Util.query_sql_procedure(sql_script_IN)


