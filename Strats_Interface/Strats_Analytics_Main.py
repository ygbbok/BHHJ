
# -*- coding: utf-8 -*-
import os
import shutil
import pandas as pd
import numpy as np
import sys
import webbrowser
import random
import string
from Strats_Analytics import Strats_Analytics
from IO_Util import IO_Util
reload(sys)
sys.setdefaultencoding( "gb2312" )


def main(args):
	# Arguments:
	# 1. Dimension Settings txt dir
	# 2. Measures Settings txt dir
	# 3. tape file dir
	# 4. strats_txt_dir

	args_list = args[0].split("|")
	dimensions_settings_file_dir = args_list[0]
	measures_settings_file_dir = args_list[1]
	rules_mapping_file_dir = args_list[2]
	strats_raw_tape_dir = args_list[3]
	temp_strats_folder_dir = args_list[4]
	

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
	
	# IO_Util.open_in_html(df)

if __name__ == "__main__":

	# file_dir = "F:\Work\Bohai Huijin Asset Management\Investment\ABS Investment\Opportunities\\5.RawTape\creditease.nongzubao.aug2017.selected.loantape.csv"
	# file_dir = "F:\Work\Bohai Huijin Asset Management\Investment\ABS Investment\Opportunities\\5.RawTape\chinatopcredit.CashLoan.5m.loantape.csv"
	# argstr = "F:\Work\Bohai Huijin Asset Management\Investment\Orcas_Killer\Strats_Analytics\Settings_Files\dimensions_settings.txt|F:\Work\Bohai Huijin Asset Management\Investment\Orcas_Killer\Strats_Analytics\Settings_Files\measures_settings.txt|F:\Work\Bohai Huijin Asset Management\Investment\Orcas_Killer\Strats_Analytics\Settings_Files\\rules_mapping.txt|F:\Work\Bohai Huijin Asset Management\Investment\ABS Investment\Opportunities\\5.RawTape\creditease.nongzubao.aug2017.selected.loantape.parsed.csv|F:\Work\Bohai Huijin Asset Management\Investment\Orcas_Killer\\txt_temp\\temp_strats"
	# file_dir = "E:\BHHJ\Strats_Analytics\Data\zhengda.CashLoan.loantape.csv"
	# argstr = "E:\BHHJ\Strats_Analytics\Settings_Files\dimensions_settings.txt|E:\BHHJ\Strats_Analytics\Settings_Files\measures_settings.txt|E:\BHHJ\Strats_Analytics\Settings_Files\\rules_mapping.txt|E:\BHHJ\Strats_Analytics\Data\zhengda.CashLoan.loantape.csv|E:\BHHJ\Strats_Analytics\\temp\\temp_strats"
	# main([argstr])

	 main(sys.argv[1:])