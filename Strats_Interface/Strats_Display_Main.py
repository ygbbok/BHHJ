
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
sys.setdefaultencoding("gb2312")


def main(args):
	# Arguments:
	# 1. Dimensions Settings txt dir
	# 2. Measures Settings txt dir
	# 3. tape file dir
	# 4. strats_folder_dir
	# 5. temp_strats_folder_dir
	# 6. Sort By
	# 7. Display Top N

	args_list = args[0].split("|")
	dimensions_settings_file_dir = args_list[0]
	measures_settings_file_dir = args_list[1]
	strats_raw_tape_dir = args_list[2]
	source_strats_folder_dir = args_list[3]
	temp_strats_folder_dir = args_list[4]
	strats_sort_by = int(args_list[5])
	strats_display_topn = int(args_list[6])

	rawtape_df = IO_Util.read_csv(strats_raw_tape_dir, sep = ',')
	dimensions_settings = IO_Util.read_csv(dimensions_settings_file_dir, sep="|")
	measures_settings = IO_Util.read_csv(measures_settings_file_dir, sep="|")


	load_strats_analytics_instance = False
	for idx,row in dimensions_settings.iterrows():
		dimension_column = row['column']
		sl = row['strats_label']
		group_rule = row['group_rule']
		source_starts_txt_file_dir = source_strats_folder_dir + "\\" + sl + "_" + "strats" + ".txt"
		temp_starts_txt_file_dir = temp_strats_folder_dir + "\\" + sl + "_" + "strats" + ".txt"
		print source_starts_txt_file_dir
		res = pd.read_csv(source_starts_txt_file_dir, sep = "|",encoding = 'gb2312')

		if group_rule == group_rule: # with group rule
			pass
		else:
			if len(res)<=(strats_display_topn+1): # without group rule, but total bucket <= top N
				strats_total_line = res.loc[res.ix[:,0] == 'Total',:]
				strats_total_line =strats_total_line.loc[strats_total_line.index[0],:].values
				strats_wo_total_line = res.loc[res.ix[:,0] != 'Total',:]
				strats_wo_total_line = strats_wo_total_line.sort_values([strats_wo_total_line.columns.values[strats_sort_by]], ascending=[False])

				res = strats_wo_total_line
				res = res.reset_index(drop=True)
				res.loc[len(res)] = strats_total_line

			else:  # without group rule, and total bucket > top N
				if not load_strats_analytics_instance:
					Strats_Analytics_instance = Strats_Analytics(rawtape_df,dimensions_settings,measures_settings)
					load_strats_analytics_instance = True

				strats_total_line = res.loc[res.ix[:,0] == 'Total',:]
				strats_total_line =strats_total_line.loc[strats_total_line.index[0],:].values
				strats_wo_total_line = res.loc[res.ix[:,0] != 'Total',:]
				strats_wo_total_line = strats_wo_total_line.sort_values([strats_wo_total_line.columns.values[strats_sort_by]], ascending=[False])
				topn_bucket_list = strats_wo_total_line.head(strats_display_topn).ix[:,0].values

				the_target_other_dict = {"column":dimension_column,"topn_bucket_list":topn_bucket_list}
				Strats_Analytics_instance.update_target_other_dict(the_target_other_dict)
				Strats_Analytics_instance.run_tape_extension_procedure_target_other()
				others_line = Strats_Analytics_instance.analytics_procedure()

				strats_topn_line = strats_wo_total_line.head(strats_display_topn)
				res = strats_topn_line
				res = res.reset_index(drop=True)
				res.loc[len(res)] = others_line
				res.loc[len(res)] = strats_total_line
		
		res.to_csv(temp_starts_txt_file_dir, index = False, sep = "|",encoding = 'gb2312')



if __name__ == "__main__":

	# argstr = "F:\Work\Bohai Huijin Asset Management\Investment\Orcas_Killer\Strats_Analytics\Settings_Files\dimensions_settings.txt|F:\Work\Bohai Huijin Asset Management\Investment\Orcas_Killer\Strats_Analytics\Settings_Files\measures_settings.txt|F:\Work\Bohai Huijin Asset Management\Investment\ABS Investment\Opportunities\\5.RawTape\chinatopcredit.loantape.csv|F:\Work\Bohai Huijin Asset Management\Investment\ABS Investment\Opportunities\\4.Strats\\test_strats|F:\Work\Bohai Huijin Asset Management\Investment\Orcas_Killer\\txt_temp\\temp_strats|1|10"
	# main([argstr])

	main(sys.argv[1:])