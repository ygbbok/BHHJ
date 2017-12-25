# -*- coding: utf-8 -*-
################# edited ################

import pandas as pd
import locale

Mgmt_Static_Pool_File = "F:\Work\Bohai Huijin Asset Management\Investment\Orcas\Static_Pool\Mgmt_Static_Pool.pickle"
Static_Pool_Folder = "F:\Work\Bohai Huijin Asset Management\Investment\Orcas\Static_Pool\\"

Unlevered_Economics_Run_Folder = "F:\Work\Bohai Huijin Asset Management\Investment\Orcas\Unlevered_Economics_Run\\"
Mgmt_Unlevered_Economics_Run_File = "F:\Work\Bohai Huijin Asset Management\Investment\Orcas\Unlevered_Economics_Run\Mgmt_Unlevered_Economics_Run.pickle"

ORCAS_ICON = "F:\Work\Bohai Huijin Asset Management\Investment\Orcas\LOGO_TITLE\ORCAS_ICON.ico"

Formatter_pct2 = lambda x: "{:.2%}".format(x)

#
# ********************** Database **********************
sql_server = "liuxiao-PC"#"(localdb)\MSSQLLocalDB"
staging_tables_db = "markplace_lending_staging_tables"
cracked_tables_dev_db = "markplace_lending_cracked_dev_tables"
#cracked_tables_prod_db = "markplace_lending_cracked_prod_tables"
cracked_tables_prod_db = "Strats_Analytics"

production_table_list = ['Consumer']

BHHJ_static_temp_pool_txt = "F:\Work\Bohai Huijin Asset Management\Investment\Orcas\Static_Pool\\to_be_loaded_pool.txt"

BHHJ_Forecast_temp_txt = "F:\Work\Bohai Huijin Asset Management\Investment\Orcas\Unlevered_Economics_Run\\BHHJ_Forecast.txt"
# ********************** Database **********************


# ********************** Color **********************
Orcas_green = '#%02x%02x%02x' % (52, 204, 153)
Orcas_blue = '#%02x%02x%02x' % (64, 204, 208)
Orcas_grey = '#%02x%02x%02x' % (238,233,233)
Orcas_snow = '#%02x%02x%02x' % (255,250,250)
# ********************** Color **********************



# ********************** Credit Model **********************
creditmodel_list = ['CPR/CDR','SMM/MDR','CTC CASHLOAN(5m10m BASE)']
# ********************** Credit Model **********************

# ********************** Struct Model **********************
structmodel_list = [u'结构化信托','Securitization','Whole Loan Purchase','Empty']
# ********************** Struct Model **********************