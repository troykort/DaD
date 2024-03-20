
# %%

import warnings
warnings.simplefilter('ignore')
import pandas as pd
import sqlite3



# %%
Sales_connection= sqlite3.connect("go_sales.sqlite")
Sales_connection


# %%
sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
#Vul dit codeblok verder in
pd.read_sql(sql_query,Sales_connection)




# %%
query = "SELECT * FROM sales_staff"
df=pd.read_sql(query,Sales_connection)
df




# %%
dict= sales_staff.to_dict("Series")
pd.Series(dict)



# %%
sales_staff_code_series = df['SALES_STAFF_CODE']
work_phone_series = df['WORK_PHONE']
extension_series = df['EXTENSION']
fax_series = df['FAX']
email_series = df['EMAIL']

# Combineer de Series tot één DataFrame genaamd contact_details
contact_details = pd.concat([sales_staff_code_series, work_phone_series, extension_series, fax_series, email_series], axis=1)
contact_details 




# %%
contact_details_head = contact_details.head(5)
print (contact_details_head)


# %%
first_language_list = ['EN'] * 5

first_language_series = pd.Series(first_language_list, name='FIRST_LANGUAGE')

contact_details_with_language = pd.concat([contact_details_head, first_language_series], axis=1)

contact_details_with_language



# %%
second_language_dict = {0: 'FR', 1: 'FR', 2: 'FR', 3: 'DE', 4: 'DE'}

SECOND_LANGUAGE_SERIES=pd.Series(second_language_dict,name= "SECOND_LANGUAGE")

Contact_Details_Second_Language=pd.concat([contact_details_with_language,SECOND_LANGUAGE_SERIES],axis=1)
Contact_Details_Second_Language 


# %%
Third_Language_Dict={
    'Third_Language_Dict': ['NL', 'NL', 'JPN', 'JPN', 'KOR']
}
third_language_df = pd.DataFrame(Third_Language_Dict)

contact_details_with_third_language = pd.concat([Contact_Details_Second_Language, third_language_df], axis=1)

contact_details_with_third_language


# %%



new_row =pd.DataFrame( {'SALES_STAFF_CODE': ['SS06'], 
                        'FIRST_NAME': ['John'], 
                        'LAST_NAME': ['Doe'], 
                        'POSITION_EN': ['Sales Associate'], 
                        'WORK_PHONE': ['123-456-7890'], 
                        'EXTENSION': [''], 
                        'FAX': ['32'], 
                        'EMAIL': ['john.doe@example.com']})
df=pd.concat([df,new_row],axis=0,ignore_index=True)





# %%
df['FULL_NAME'] = df['FIRST_NAME'] + ' ' + df['LAST_NAME']
df

# %%
df.dtypes


# %%
sales_staff['EXTENSION'] = sales_staff['EXTENSION'].astype(int)
sales_staff.dtypes

# %%
sales_staff['EXTENSION'] = sales_staff['EXTENSION'].astype(float)
sales_staff.dtypes

# %%
sales_staff['EXTENSION'] = sales_staff['EXTENSION'] + 1
sales_staff


# %%


# %%
sales_staff['POSITION_EN'] = sales_staff['POSITION_EN'].replace('Branch Manager', 'General Manager')
sales_staff

# %%
sales_staff = sales_staff.rename(columns={'POSITION_EN': 'POSITION'})
sales_staff


# %%
sales_staff = sales_staff.drop(index=[99, 100, 101])
sales_staff


# %%
sales_staff = sales_staff.drop(columns=['FAX'])
sales_staff



