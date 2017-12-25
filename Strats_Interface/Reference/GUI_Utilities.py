# -*- coding: utf-8 -*-
import pandas as pd
import Tkinter as Tkinter
import ttk as ttk
import os
import locale
import sys
#from Config import Config
import Config
import numpy as np
#import matplotlib
#import pylab
#import pygtk
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar
#from matplotlib.figure import Figure

# sys.path.append("F:\Work\Bohai Huijin Asset Management\Investment\Orcas\\")
sys.path.append("E:\BHHJ\Code\Strats_Interface\Reference\\")


#from IO_Utilities import IO_Utilities
#import IO_Utilities

Formatter_pct2 = lambda x: "{:.2%}".format(x)
Formatter_dec2 = lambda x: '{0:,.2f}'.format(x)
Formatter_dec0 = lambda x: '{0:,.0f}'.format(x)

class Treeview_Mgmt(Tkinter.Frame):
	def __init__(self, master=None, df_IN = pd.DataFrame()):
		Tkinter.Frame.__init__(self, master)
		self.pack()
		self.frame = Tkinter.Frame(self)
		self.frame.pack()
 
		f = ttk.Frame(self.frame)
		f.pack(side='top', fill='both', expand='y')

		self.tree = ttk.Treeview(columns=tuple(df_IN.columns))

		ysb = ttk.Scrollbar(orient='vertical', command= self.tree.yview)
		xsb = ttk.Scrollbar(orient='horizontal', command= self.tree.xview)
		self.tree['yscroll'] = ysb.set
		self.tree['xscroll'] = xsb.set

		for item in self.tree.get_children(): self.tree.delete(item)
		# self.tree.heading('#0',         text='Index',           anchor='e')
		self.tree.heading('#0',         text='索引',           anchor='e')
		self.tree.column('#0',         stretch=0, width=40 , anchor='e')

		for col in list(df_IN.columns):
			# be careful with chinese character
			# self.tree.heading(col,text=str(col))
			self.tree.heading(col,text=col)
			self.tree.column(col, stretch=0, width=70)

		#Populate data in the treeview
		for index,row in df_IN.iterrows(): self.tree.insert('', 'end',text=index, values = tuple(row[0:]))

		# add tree and scrollbars to frame
		self.tree.grid(in_=f, row=0, column=0, sticky='nsew')
		ysb.grid(in_=f, row=0, column=1, sticky='ns')
		xsb.grid(in_=f, row=1, column=0, sticky='ew')

		# set frame resizing priorities
		f.rowconfigure(0, weight=1)
		f.columnconfigure(0, weight=1)
	
	def update_dataframe(self,df_IN):
		for item in self.tree.get_children(): self.tree.delete(item)
		for index,row in df_IN.iterrows(): self.tree.insert('', 'end',text=index, values = tuple(row[0:]))

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
			temp_node.grid(row = 0, column = i-1)
			self.nodes[i] = temp_node

	def get(self, node_num):
		return self.nodes[node_num].get()

class ConditionGroup_Mgmt(Tkinter.Frame):
	def __init__(self, master=None, title_list_IN = ["Column1","Column2","Column3"]):
		Tkinter.Frame.__init__(self, master)
		self.pack()

		self.frame = Tkinter.Frame(self)
		self.frame.pack()

		self.title_list = title_list_IN
		self.col_num = len(self.title_list)

		self.button_frame = Tkinter.Frame(self.frame)
		self.button_frame.pack(expand = 1, fill="both")

		# self.add_condition_button = Tkinter.Button(self.button_frame, text = "Add Condition", command = self.add_condition)
		self.add_condition_button = Tkinter.Button(self.button_frame, text = u'添加条件',command = self.add_condition,width = 12)
		self.add_condition_button.pack(side = 'left')

		self.delete_condition_button = Tkinter.Button(self.button_frame, text = u"删除条件", command = self.delete_condition,width = 12)
		self.delete_condition_button.pack(side = 'left')

		self.title_frame = Tkinter.Frame(self.frame)
		self.title_frame.pack(expand = 1, fill="both")

		self.labels_dict = {}
		for i in range(1,self.col_num + 1):
			self.labels_dict[i] = Tkinter.Label(self.title_frame,text = self.title_list[i-1], width = 9)
			self.labels_dict[i].grid(row = 0, column = i-1)

		self.condition_num = 1
		self.conditions_dict = {}
		self.conditions_dict[1] = [None, None]
		
		self.conditions_dict[1][0] = Tkinter.Frame(self.frame)
		self.conditions_dict[1][0].pack(expand = 1, fill="both")
		self.conditions_dict[1][1] = TextBoxGroup_Mgmt(self.conditions_dict[1][0],num_of_text_box_IN = self.col_num)
		self.conditions_dict[1][1].pack()


	def add_condition(self):
		
		self.condition_num = self.condition_num + 1
		self.conditions_dict[self.condition_num] = [None, None]
		self.conditions_dict[self.condition_num][0] = Tkinter.Frame(self.frame)
		self.conditions_dict[self.condition_num][0].pack(expand = 1, fill="both")
		self.conditions_dict[self.condition_num][1] = TextBoxGroup_Mgmt(self.conditions_dict[1][0],num_of_text_box_IN = self.col_num)
		
		self.conditions_dict[self.condition_num][1].pack()

	def delete_condition(self):
		
		self.conditions_dict[self.condition_num][0].destroy()
		self.conditions_dict[self.condition_num][1].destroy()
		self.conditions_dict[self.condition_num] = [None, None]
		self.condition_num = self.condition_num - 1
	
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
			
class DisplayTable_Mgmt(Tkinter.Frame):
	def __init__(self, master=None, df_IN = pd.DataFrame(), formatting_mapper_IN = None):
		Tkinter.Frame.__init__(self, master)
		self.pack()

		self.frame = Tkinter.Frame(self)
		self.frame.pack()

		self.df = df_IN
		self.formatting_mapper = formatting_mapper_IN
		self.node_dict = {}
		self.setup()


	def setup(self):

		r0_c0_node = Tkinter.Label(self.frame, width=16, text="")
		r0_c0_node.grid(row = 0, column = 0)

		self.node_dict[(0,0)] = r0_c0_node
		row_switch = False
		j = 1
		for col_name in self.df.columns.values:
			new_node = Tkinter.Label(self.frame, width=(16 if j == 0 else 12), text = col_name,relief = 'ridge',background = Config.Orcas_blue)
			new_node.grid(row = 0, column = j,sticky="nsew", padx=1, pady=1)
			self.node_dict[(0,j)] = new_node
			j += 1

		i = 1	
		for idx,row in self.df.iterrows():
			bg_color = Config.Orcas_grey if row_switch else Config.Orcas_snow
			j = 0
			new_node = Tkinter.Label(self.frame, width=(16 if j == 0 else 12), text = idx,relief = 'ridge',background = bg_color)
			new_node.grid(row = i, column = j,sticky="nsew",padx=1, pady=1)
			self.node_dict[(i,j)] = new_node

			j += 1
			for item in row:
				new_node = Tkinter.Label(self.frame, width=(16 if j == 0 else 12), text = self.formatting_mapper[idx](row[j-1]),relief = 'ridge',background = bg_color)
				new_node.grid(row = i, column = j,sticky="nsew",padx=1, pady=1)
				self.node_dict[(i,j)] = new_node
				j += 1

			i += 1
			row_switch = not(row_switch)


class Display_Unlevered_Econ_Cashflow_Mgmt(Tkinter.Frame):
	def __init__(self, master, run_num_list_IN = [], cashflow_df_list_IN = [],open_in_html_bool_IN = True):
		Tkinter.Frame.__init__(self, master)
		self.pack()

		self.frame = Tkinter.Frame(self)
		self.frame.pack(side = 'top')

		self.notebook = ttk.Notebook(self.frame)
		self.notebook.pack()

		self.page_frame_holder = []
		self.treeview_gui_mgmt_holder = []

		self.run_num_list = run_num_list_IN
		self.cashflow_df_list = cashflow_df_list_IN

		self.open_in_html_bool = open_in_html_bool_IN

		self.length = len(self.run_num_list)

		self.setup()

	def setup(self):
		for idx,item in enumerate(self.run_num_list):
			self.page_frame_holder.append(Tkinter.Frame(self.frame))
			self.page_frame_holder[-1].pack(side = 'top')
			self.notebook.add(self.page_frame_holder[idx], text = "Run - " + str(item))
			temp = Treeview_Mgmt(master = self.page_frame_holder[-1], df_IN = self.cashflow_df_list[idx])
			self.treeview_gui_mgmt_holder.append(temp)

			if self.open_in_html_bool:
				IO_Utilities.IO_Util.open_in_html(self.cashflow_df_list[idx])


class Display_Charts_Mgmt_OrcasFormat(Tkinter.Frame):
	def __init__(self, master, datadict_IN, keys_IN):
		Tkinter.Frame.__init__(self, master)
		self.pack()

		self.frame = Tkinter.Frame(self)
		self.frame.pack(side = 'top')

		self.datadict = datadict_IN
		self.keys = keys_IN
		self.legends = []
		self.setup()

	def setup(self):
		self.legends = []
		self.smm_curves = []
		self.mdr_curves = []
		self.sev_curves = []
		self.loss_curves = []

		for key,value in self.datadict.items():

			self.legends.append(key)
			self.smm_curves.append(value['smm_curve'])
			self.mdr_curves.append(value['mdr_curve'])
			self.sev_curves.append(value['severity_curve'])
			self.loss_curves.append(value['cum_loss_curve'])

		smm_curve_x = []
		smm_curve_y = []
		for smm_curve in self.smm_curves:
			if len(smm_curve['period'])>len(smm_curve_x) : smm_curve_x = smm_curve['period']
			smm_curve_y.append(smm_curve['smm'])

		mdr_curve_x = []
		mdr_curve_y = []
		for mdr_curve in self.mdr_curves:
			if len(mdr_curve['period'])>len(mdr_curve_x) : mdr_curve_x = mdr_curve['period']		
			mdr_curve_y.append(mdr_curve['mdr'])

		sev_curve_x = []
		sev_curve_y = []
		for sev_curve in self.sev_curves:
			if len(sev_curve['period'])>len(sev_curve_x) : sev_curve_x = sev_curve['period']
			sev_curve_y.append(sev_curve['sev'])

		loss_curve_x = []
		loss_curve_y = []
		for loss_curve in self.loss_curves:
			if len(loss_curve['period'])>len(loss_curve_x) : loss_curve_x = loss_curve['period']
			loss_curve_y.append(loss_curve['loss'])




		fig = Figure(figsize = (7,4.5))

		rect = fig.patch
		rect.set_facecolor(Config.Orcas_grey)
		ax1 = fig.add_subplot(221)
		ax1.set_title('SMM Curve',fontsize = 8)
		for smm_curve_y_item in smm_curve_y:
			if len(smm_curve_x) > len(np.transpose(smm_curve_y_item)):
				smm_curve_y_item_ploted = np.transpose(smm_curve_y_item) * 100
				smm_curve_y_item_ploted = np.concatenate([smm_curve_y_item_ploted,np.array([np.nan] * (len(smm_curve_x) - len(np.transpose(smm_curve_y_item))))])
			else:
				smm_curve_y_item_ploted = np.transpose(smm_curve_y_item) * 100

			ax1.plot(smm_curve_x,smm_curve_y_item_ploted)
			ax1.grid(b=True, which='both', color='0.65',linestyle='-.')

		ax2= fig.add_subplot(222)
		ax2.set_title('MDR Curve',fontsize = 8)
		for mdr_curve_y_item in mdr_curve_y:
			if len(mdr_curve_x) > len(np.transpose(mdr_curve_y_item)):
				mdr_curve_y_item_ploted = np.transpose(mdr_curve_y_item) * 100
				mdr_curve_y_item_ploted = np.concatenate([mdr_curve_y_item_ploted,np.array([np.nan] * (len(mdr_curve_x) - len(np.transpose(mdr_curve_y_item))))])
			else:
				mdr_curve_y_item_ploted = np.transpose(mdr_curve_y_item) * 100

			ax2.plot(mdr_curve_x,mdr_curve_y_item_ploted)
			ax2.grid(b=True, which='both', color='0.65',linestyle='-.')

		ax3= fig.add_subplot(223)
		ax3.set_title('SEV Curve',fontsize = 8)
		cnt_i = 0
		for sev_curve_y_item in sev_curve_y:
			if len(sev_curve_x) > len(np.transpose(sev_curve_y_item)):
				sev_curve_y_item_ploted = np.transpose(sev_curve_y_item) * 100
				sev_curve_y_item_ploted = np.concatenate([sev_curve_y_item_ploted,np.array([np.nan] * (len(sev_curve_x) - len(np.transpose(sev_curve_y_item))))])
			else:
				sev_curve_y_item_ploted = np.transpose(sev_curve_y_item) * 100


			ax3.plot(mdr_curve_x,sev_curve_y_item_ploted, label = self.legends[cnt_i])
			legend = ax3.legend(loc='best', shadow=False,fontsize = 'xx-small',fancybox=True)
			ax3.grid(b=True, which='both', color='0.65',linestyle='-.')

			cnt_i += 1

		ax4= fig.add_subplot(224)
		ax4.set_title('Cum Loss Curve',fontsize = 8)
		for loss_curve_y_item in loss_curve_y:
			if len(loss_curve_x) > len(np.transpose(loss_curve_y_item)):
				loss_curve_y_item_ploted = np.transpose(loss_curve_y_item) * 100
				loss_curve_y_item_ploted = np.concatenate([loss_curve_y_item_ploted,np.array([np.nan] * (len(loss_curve_x) - len(np.transpose(loss_curve_y_item))))])
			else:
				loss_curve_y_item_ploted = np.transpose(loss_curve_y_item)  * 100

			ax4.plot(mdr_curve_x,loss_curve_y_item_ploted)
			ax4.grid(b=True, which='both', color='0.65',linestyle='-.')


		self.canvas = FigureCanvasTkAgg(fig,master=self.frame)

		# unsolved problem : how to make charts interactive

		# self.toolbar = NavigationToolbar(self.canvas, self.frame)
		# self.toolbar.update()
		# self.plot_widget = self.canvas.get_tk_widget()
		# self.plot_widget.pack(side='top', fill='both', expand=1)
		# self.toolbar.pack(side='top', fill='both', expand=1)

		self.canvas.show()
		self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

		# matplotlib.pyplot.plot([1,2,3,4])
		# matplotlib.pyplot.ylabel('some numbers')
		# matplotlib.pyplot.show()




class Labeled_Entry(Tkinter.Frame):
	def __init__(self, master, label_IN, default_IN = 0, width_IN = 10):
		Tkinter.Frame.__init__(self, master)
		self.pack()

		self.frame = Tkinter.Frame(self)
		self.frame.pack(side = 'top')

		self.label = Tkinter.Label(self.frame, text = label_IN)
		self.label.pack(side = 'left')
		self.entry = Tkinter.Entry(self.frame, width = width_IN)
		self.entry.pack(side = 'left')
		self.entry.insert(0,default_IN)
	
	def get(self):
		return self.entry.get()


root = Tkinter.Tk()
root.title("Main") # Define title

#----------------------------------------
# Button
#----------------------------------------
# Broswer to show button
# Create the application

# df = pd.DataFrame(columns = ['a','b'])
# df.loc[0] = [1,2]
# df.loc[1] = [2,3]
# df.loc[2] = [3,4]

# mappers = {}
# mappers['a'] = Formatter_dec2
# mappers['b'] = Formatter_dec2
# mappers['c'] = Formatter_dec2

# app = DisplayTable_Mgmt(master=root,df_IN = df,formatting_mapper_IN = mappers)
app = ConditionGroup_Mgmt(master=root)

# Start the program
app.mainloop()