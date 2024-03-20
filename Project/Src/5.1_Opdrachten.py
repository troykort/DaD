# %%

import pandas as pd 
import pyodbc
import warnings
warnings.simplefilter('ignore')
import sqlite3

# %%
DB = {'servername': 'LAPTOPTK\SQLEXPRESS',
'database': 'DAD'}

export_conn = pyodbc.connect('DRIVER={SQL Server}; SERVER=' + DB['servername'] +
                            ';DATABASE=' + DB['database'] + ';Trusted_Connection=yes')
export_cursor = export_conn.cursor()
export_cursor

# %%
# DB = {'servername': 'LAPTOP-3S422SS6\\SQLEXPRESS',
# 'database': 'DAD'}

# export_conn = pyodbc.connect('DRIVER={SQL Server}; SERVER=' + DB['servername'] +
#                               ';DATABASE=' + DB['database'] + ';Trusted_Connection=yes')
# export_cursor = export_conn.cursor()
# export_cursor

# %%
Sales_connection= sqlite3.connect("go_sales.sqlite")
Crm_connection= sqlite3.connect("go_crm.sqlite")
inventory_levels = pd.read_csv('GO_SALES_INVENTORY_LEVELSData.csv', index_col=False) 
product_forecast = pd.read_csv('GO_SALES_PRODUCT_FORECASTData.csv', index_col=False)

# %%
newQuery = "SELECT * FROM product"
product = pd.read_sql(newQuery,Sales_connection)
newQuery = "SELECT * FROM product_type"
product_type = pd.read_sql(newQuery,Sales_connection)
newQuery = "SELECT * FROM product_line"
product_line = pd.read_sql(newQuery,Sales_connection)
newQuery = "SELECT * FROM sales_staff"
sales_staff = pd.read_sql(newQuery,Sales_connection)
newQuery = "SELECT * FROM sales_branch"
sales_branch = pd.read_sql(newQuery,Sales_connection)
newQuery = "SELECT * FROM retailer_site"
retailer_site = pd.read_sql(newQuery,Sales_connection)
newQuery = "SELECT * FROM country"
country = pd.read_sql(newQuery,Sales_connection)
newQuery = "SELECT * FROM order_header"
order_header = pd.read_sql(newQuery,Sales_connection)
newQuery = "SELECT * FROM order_details"
order_details = pd.read_sql(newQuery,Sales_connection)
newQuery = "SELECT * FROM SALES_TARGETData"
target = pd.read_sql(newQuery,Sales_connection)
newQuery = "SELECT * FROM returned_item"
returned_item = pd.read_sql(newQuery,Sales_connection)
newQuery = "SELECT * FROM return_reason"
return_reason = pd.read_sql(newQuery,Sales_connection)

newQuery = "SELECT * FROM country"
country_crm = pd.read_sql(newQuery,Crm_connection)
newQuery = "SELECT * FROM retailer_type"
retailer_type = pd.read_sql(newQuery,Crm_connection)
newQuery = "SELECT * FROM retailer_segment"
retailer_segment = pd.read_sql(newQuery,Crm_connection)
newQuery = "SELECT * FROM retailer"
retailer = pd.read_sql(newQuery,Crm_connection)
newQuery = "SELECT * FROM sales_territory"
sales_territory = pd.read_sql(newQuery,Crm_connection)
newQuery = "SELECT * FROM retailer_headquarters"
retailer_headquarters = pd.read_sql(newQuery,Crm_connection)



# %%
Sales_staff_connection=sqlite3.connect('go_staff.sqlite')
Sales_staff_connection

# %%
newQuery= "SELECT * FROM course"
course= pd.read_sql(newQuery,Sales_staff_connection)
newQuery= "SELECT * FROM sales_branch"
sales_branch=pd.read_sql(newQuery,Sales_staff_connection)
newQuery= "SELECT * FROM sales_staff"
sales_staff=pd.read_sql(newQuery,Sales_staff_connection)
newQuery= "SELECT * FROM satisfaction"
satisfaction=pd.read_sql(newQuery,Sales_staff_connection)
newQuery= "SELECT * FROM satisfaction_type"
satisfaction_type=pd.read_sql(newQuery,Sales_staff_connection)
newQuery= "SELECT * FROM training" 
training=pd.read_sql(newQuery,Sales_staff_connection)


# %%
retailer_site_merge = pd.merge(retailer_site, country_crm, on='COUNTRY_CODE', how='left', suffixes=('', '_country'))
retailer_site_merge = pd.merge(retailer_site_merge, sales_territory, on='SALES_TERRITORY_CODE', how='left', suffixes=('', '_sales_territory'))
retailer_site_merge = pd.merge(retailer_site_merge, retailer, on='RETAILER_CODE', how='left', suffixes=('', '_retailer'))
retailer_site_merge = pd.merge(retailer_site_merge, retailer_type, on='RETAILER_TYPE_CODE', how='left', suffixes=('', '_retailer_type'))
retailer_site_merge = pd.merge(retailer_site_merge, retailer_headquarters, on='RETAILER_CODEMR', how='left', suffixes=('', '_retailer_headquarters'))
retailer_site_merge = pd.merge(retailer_site_merge, retailer_segment, on='SEGMENT_CODE', how='left', suffixes=('', '_retailer_segment'))

retailer_site_dimensie = retailer_site_merge[[
    'RETAILER_SITE_CODE', 'ADDRESS1', 'ADDRESS2', 'ACTIVE_INDICATOR', 'COMPANY_NAME', 
    'RETAILER_TYPE_EN', 'SEGMENT_NAME', 'CITY', 'REGION', 'COUNTRY_EN', 'TERRITORY_NAME_EN'
]].copy()

retailer_site_dimensie['ACTIVE_INDICATOR'] = pd.to_numeric(retailer_site_dimensie['ACTIVE_INDICATOR']).astype(int)


# %%
product_merge = product.merge(product_type, left_on='PRODUCT_TYPE_CODE', right_on='PRODUCT_TYPE_CODE', how='left')
product_merge = product_merge.merge(product_line, left_on='PRODUCT_LINE_CODE', right_on='PRODUCT_LINE_CODE', how='left')
product_dimensie = product_merge[['PRODUCT_NUMBER', 'PRODUCT_TYPE_CODE', 'PRODUCT_NAME', 'DESCRIPTION', 'PRODUCT_TYPE_EN', 'PRODUCT_LINE_EN', 'INTRODUCTION_DATE', 'PRODUCTION_COST', 'MARGIN']]

product_dimensie['INTRODUCTION_DATE'] = pd.to_datetime(product_dimensie['INTRODUCTION_DATE']).dt.date
product_dimensie['PRODUCTION_COST'] = pd.to_numeric(product_dimensie['PRODUCTION_COST']).astype('float').round(2)
product_dimensie['MARGIN'] = pd.to_numeric(product_dimensie['MARGIN']).astype('float').round(2)


# %%
date_dimensie = order_header['ORDER_DATE'].drop_duplicates()

product_forecast = product_forecast.rename(columns={'INTRODUCTION_DATE': 'date'})
product_forecast['date'] = pd.to_datetime(product_forecast['YEAR'].astype(str) + '-' + product_forecast['MONTH'].astype(str) + '-01').dt.date
product_forecast_date = product_forecast['date'] 

satisfaction = satisfaction.rename(columns={'YEAR': 'date'})
satisfaction['date'] = pd.to_datetime(satisfaction['date'].astype(str) + '-01-01').dt.date
satisfaction_date = satisfaction['date'].drop_duplicates()

inventory_levels = inventory_levels.rename(columns={'INVENTORY_YEAR': 'date'})
inventory_levels['date'] = pd.to_datetime( inventory_levels['date'].astype(str)+'-'+inventory_levels['INVENTORY_MONTH'].astype(str)+'-01').dt.date
inventory_levels_date =  inventory_levels['date'].drop_duplicates()

# %%
returned_item['RETURN_DATE'] = pd.to_datetime(returned_item['RETURN_DATE'], format='%d-%m-%Y %H:%M:%S')
returned_item_date = returned_item['RETURN_DATE'].dt.date

# %%
date_dimensie = pd.to_datetime(date_dimensie).dt.date
product_forecast_date = pd.to_datetime(product_forecast_date).dt.date
satisfaction_date = pd.to_datetime(satisfaction_date).dt.date
inventory_levels_date = pd.to_datetime(inventory_levels_date).dt.date
returned_item_date = pd.to_datetime(returned_item_date).dt.date

all_dates = pd.concat([
    date_dimensie,
    product_forecast_date,
    satisfaction_date,
    inventory_levels_date,
    returned_item_date
])

all_dates_unique = all_dates.drop_duplicates().sort_values()

all_dates_df = all_dates_unique.to_frame(name='date')

all_dates_df['date'] = pd.to_datetime(all_dates_df['date'])

all_dates_df['month'] = all_dates_df['date'].dt.month
all_dates_df['quarter'] = all_dates_df['date'].dt.quarter
all_dates_df['year'] = all_dates_df['date'].dt.year


# %%
order = pd.merge(order_details,order_header,left_on='ORDER_NUMBER',how='left',right_on='ORDER_NUMBER')
order_fact = order[['ORDER_NUMBER','ORDER_DETAIL_CODE','QUANTITY','UNIT_COST','UNIT_PRICE','UNIT_SALE_PRICE','PRODUCT_NUMBER','RETAILER_SITE_CODE','SALES_STAFF_CODE','ORDER_DATE']]

# %%
date_export_cursor = export_conn.cursor()

for index, row in all_dates_df.iterrows():
    try:
        query = f"""
        INSERT INTO DATE 
        (DATE_date, DATE_MONTH_nr, DATE_QUARTER_nr, DATE_YEAR_nr) 
        VALUES 
        ('{row['date']}', {row['month']}, {row['quarter']}, {row['year']});
        """
        date_export_cursor.execute(query)
    except pyodbc.Error as e:
        print("An error occurred:", e)
        print(query)

export_conn.commit()
date_export_cursor.close()

# %%
export_cursor = export_conn.cursor()  

for index, row in product_dimensie.iterrows():
    try:
        query = f"""
        INSERT INTO PRODUCT 
        (PRODUCT_id, PRODUCT_name, PRODUCT_description, PRODUCT_TYPE_name, PRODUCT_LINE_name, 
        PRODUCT_INTRODUCTION_DATE_date, PRODUCT_COST_nr, PRODUCT_MARGIN_nr) 
        VALUES 
        ({row['PRODUCT_NUMBER']}, '{row['PRODUCT_NAME'].replace("'", "''")}', 
        '{row['DESCRIPTION'].replace("'", "''")}', '{row['PRODUCT_TYPE_EN'].replace("'", "''")}', 
        '{row['PRODUCT_LINE_EN'].replace("'", "''")}', '{row['INTRODUCTION_DATE']}', 
        {row['PRODUCTION_COST']}, {row['MARGIN']});
        """
        export_cursor.execute(query)
    except pyodbc.Error as e:
        print("An error occurred:", e)
        print(query)

export_conn.commit()  
export_cursor.close()  

# %%
export_cursor = export_conn.cursor()  

for index, row in retailer_site_dimensie.iterrows():
    try:
        retailer_site_id = row['RETAILER_SITE_CODE']
        address1 = f"'{row['ADDRESS1'].replace("'", "''")}'" if pd.notna(row['ADDRESS1']) else 'NULL'
        address2 = f"'{row['ADDRESS2'].replace("'", "''")}'" if pd.notna(row['ADDRESS2']) else 'NULL'
        active_indicator = row['ACTIVE_INDICATOR']
        company_name = f"'{row['COMPANY_NAME'].replace("'", "''")}'" if pd.notna(row['COMPANY_NAME']) else 'NULL'
        retailer_type_en = f"'{row['RETAILER_TYPE_EN'].replace("'", "''")}'" if pd.notna(row['RETAILER_TYPE_EN']) else 'NULL'
        segment_name = f"'{row['SEGMENT_NAME'].replace("'", "''")}'" if pd.notna(row['SEGMENT_NAME']) else 'NULL'
        city = f"'{row['CITY'].replace("'", "''")}'" if pd.notna(row['CITY']) else 'NULL'
        region = f"'{row['REGION'].replace("'", "''")}'" if pd.notna(row['REGION']) else 'NULL'
        country_en = f"'{row['COUNTRY_EN'].replace("'", "''")}'" if pd.notna(row['COUNTRY_EN']) else 'NULL'
        territory_name_en = f"'{row['TERRITORY_NAME_EN'].replace("'", "''")}'" if pd.notna(row['TERRITORY_NAME_EN']) else 'NULL'

        query = f"""
        INSERT INTO RETALER_SITE (
            RETALER_SITE_id, RETALER_SITE_adress1, RETALER_SITE_adress2, 
            RETALER_SITE_ACTIVE_INDICATOR_nr, RETALER_SITE_RETAILER_name, 
            RETALER_SITE_RETAILER_TYPE_name, RETALER_SITE_SEGMENT_name, 
            RETALER_SITE_CITY_name, RETALER_SITE_REGION_name, RETALER_SITE_COUNTRYname, 
            RETALER_SITE_TERRITORY_name
        ) VALUES (
            {retailer_site_id}, {address1}, {address2}, 
            {active_indicator}, {company_name}, {retailer_type_en}, 
            {segment_name}, {city}, {region}, {country_en}, {territory_name_en}
        );
        """
        export_cursor.execute(query)
    except pyodbc.Error as e:
        print("An error occurred:", e)
        print(query)
        
export_conn.commit()
export_cursor.close()


merged_sales_staff = pd.merge(sales_staff, sales_staff, left_on='MANAGER_CODE', right_on='SALES_STAFF_CODE', suffixes=('_staff', '_manager'))

selected_columns = [
    'SALES_STAFF_CODE_staff',
    'FIRST_NAME_staff',
    'LAST_NAME_staff',
    'EXTENSION_staff',
    'EMAIL_staff',
    'WORK_PHONE_staff',
    'MANAGER_CODE_staff',
    'DATE_HIRED_staff',
    'SALES_BRANCH_CODE_staff',
    'FIRST_NAME_manager',
    'LAST_NAME_manager'
]

sales_staff_DIMENSION = merged_sales_staff[selected_columns].rename(columns={
    'FIRST_NAME_staff': 'FIRST_NAME',
    'LAST_NAME_staff': 'LAST_NAME',
    'FIRST_NAME_manager': 'MANAGER_FIRST_NAME',
    'LAST_NAME_manager': 'MANAGER_LAST_NAME'
})
sales_staff_DIMENSION['MANAGER_NAME'] = sales_staff_DIMENSION['MANAGER_FIRST_NAME'] + ' ' + sales_staff_DIMENSION['MANAGER_LAST_NAME']
sales_staff_DIMENSION.drop(columns=['MANAGER_FIRST_NAME', 'MANAGER_LAST_NAME'], inplace=True)
sales_staff_DIMENSION['NAME'] = sales_staff_DIMENSION['FIRST_NAME'] + ' ' + sales_staff_DIMENSION['LAST_NAME']


# %%
SELECTED_COLUMS=['ORDER_DETAIL_CODE','ORDER_NUMBER','PRODUCT_NUMBER','QUANTITY','UNIT_COST','UNIT_PRICE','UNIT_SALE_PRICE','RETAILER_SITE_CODE','SALES_STAFF_CODE','ORDER_DATE']
FINAL_ORDER_DETAILS= order_fact[SELECTED_COLUMS]

FINAL_ORDER_DETAILS['ORDER_DETAIL_CODE'] = pd.to_numeric(FINAL_ORDER_DETAILS['ORDER_DETAIL_CODE'])
FINAL_ORDER_DETAILS['QUANTITY'] = pd.to_numeric(FINAL_ORDER_DETAILS['QUANTITY'])
FINAL_ORDER_DETAILS['UNIT_COST'] = pd.to_numeric(FINAL_ORDER_DETAILS['UNIT_COST'])
FINAL_ORDER_DETAILS['UNIT_PRICE'] = pd.to_numeric(FINAL_ORDER_DETAILS['UNIT_PRICE'])
FINAL_ORDER_DETAILS['UNIT_SALE_PRICE'] = pd.to_numeric(FINAL_ORDER_DETAILS['UNIT_SALE_PRICE'])
FINAL_ORDER_DETAILS['Total_Revenue'] = FINAL_ORDER_DETAILS['QUANTITY'] * FINAL_ORDER_DETAILS['UNIT_SALE_PRICE']

FINAL_ORDER_DETAILS['Gross_Profit'] = FINAL_ORDER_DETAILS['Total_Revenue'] - (FINAL_ORDER_DETAILS['QUANTITY'] * FINAL_ORDER_DETAILS['UNIT_COST'])

FINAL_ORDER_DETAILS['Profit_Margin'] = (FINAL_ORDER_DETAILS['Gross_Profit'] / FINAL_ORDER_DETAILS['Total_Revenue']) * 100

FINAL_ORDER_DETAILS['Profit_per_Product'] = FINAL_ORDER_DETAILS['UNIT_SALE_PRICE'] - FINAL_ORDER_DETAILS['UNIT_COST']

FINAL_ORDER_DETAILS['Discount_Amount'] = (FINAL_ORDER_DETAILS['QUANTITY'] * FINAL_ORDER_DETAILS['UNIT_PRICE']) - FINAL_ORDER_DETAILS['Total_Revenue']


# %%
order_export_cursor = export_conn.cursor()

for index, row in FINAL_ORDER_DETAILS.iterrows():
    try:
        query = f"""
        INSERT INTO ORDERR
        (ORDER_number_id, ORDER_detail_id, PRODUCT_number, ORDER_Quantity, ORDER_unit_Cost, ORDER_Unit_price, ORDER_Unit_sale_price, 
        Totale_omzet, ORDER_gross_profit, ORDER_profit_margin, ORDER_profit_per_product, ORDER_discount_amount, 
        RETAILER_SITE_id, SALES_STAFF_id, DATE_Order_date) 
        VALUES
        ('{row['ORDER_DETAIL_CODE']}', '{row['ORDER_NUMBER']}', '{row['PRODUCT_NUMBER']}', 
        {row['QUANTITY']}, {row['UNIT_COST']}, {row['UNIT_PRICE']}, {row['UNIT_SALE_PRICE']}, 
        {row['Total_Revenue']}, {row['Gross_Profit']}, {row['Profit_Margin']}, 
        {row['Profit_per_Product']}, {row['Discount_Amount']}, 
        '{row['RETAILER_SITE_CODE']}', '{row['SALES_STAFF_CODE']}', '{row['ORDER_DATE']}');
        """
        order_export_cursor.execute(query)
    except pyodbc.Error as e:
        print("An error occurred:", e)
        print(query)

export_conn.commit()
order_export_cursor.close()


# %%

inventory_levels1 = pd.read_csv('GO_SALES_INVENTORY_LEVELSData.csv', index_col=False) 
product_forecast1 = pd.read_csv('GO_SALES_PRODUCT_FORECASTData.csv', index_col=False)
inventory_levels_dimension = inventory_levels
inventory_levels_dimension['INVENTORY_YEAR'] = inventory_levels1['INVENTORY_YEAR']



# %%
inventory_export_cursor = export_conn.cursor()

for index, row in inventory_levels_dimension.iterrows():
    try:
        query = f"""
        INSERT INTO INVENTORY_LEVELS 
        (PRODUCT_id, DATE_YEAR_nr, DATE_MONTH_nr, INVENTORY_LEVELS_count, date) 
        VALUES 
        ({row['PRODUCT_NUMBER']}, {row['INVENTORY_YEAR']}, {row['INVENTORY_MONTH']}, 
        {row['INVENTORY_COUNT']}, '{row['date']}');
        """
        inventory_export_cursor.execute(query)
    except pyodbc.Error as e:
        print("An error occurred:", e)
        print(query)

export_conn.commit()
inventory_export_cursor.close()

# %%
inventory_export_cursor = export_conn.cursor()
for index, row in product_forecast.iterrows():
    try:
        query = f"""
        INSERT INTO PRODUCT_FORECAST 
        (PRODUCT_id, DATE_YEAR_nr, DATE_MONTH_nr, PRODUCT_FORECAST_expected_volume, date) 
        VALUES 
        ({row['PRODUCT_NUMBER']}, {row['YEAR']}, {row['MONTH']}, 
        {row['EXPECTED_VOLUME']}, '{row['date']}');
        """
        inventory_export_cursor.execute(query)
    except pyodbc.Error as e:
        print("An error occurred:", e)
        print(query)

export_conn.commit()
inventory_export_cursor.close()

# %%
MergedReturnReason=pd.merge(returned_item,return_reason, left_on='RETURN_REASON_CODE', right_on='RETURN_REASON_CODE')
SELECTED_COLUMS=['RETURN_CODE','RETURN_QUANTITY','RETURN_DATE','ORDER_DETAIL_CODE','RETURN_DESCRIPTION_EN']
ReturnedItems = MergedReturnReason[SELECTED_COLUMS]
ReturnedItems['RETURN_DATE'] = ReturnedItems['RETURN_DATE'].dt.date
ReturnedItems

# %%
returned_items_export_cursor = export_conn.cursor()

for index, row in ReturnedItems.iterrows():
    try:
        formatted_date = row['RETURN_DATE'].strftime('%Y-%m-%d')

        query = f"""
        INSERT INTO RETURNED_ITEM
        (RETURNED_ITEM_id, RETURNED_ITEM_quantity, DATE_date, ORDER_detail_id, RETURN_ITEM_REASON_description)
        VALUES
        ({row['RETURN_CODE']}, {row['RETURN_QUANTITY']}, '{formatted_date}', {row['ORDER_DETAIL_CODE']}, '{row['RETURN_DESCRIPTION_EN']}');
        """
        returned_items_export_cursor.execute(query)
    except pyodbc.Error as e:
        print("An error occurred:", e)
        print(query)

export_conn.commit()
returned_items_export_cursor.close()

# %%
sales_staff_export_cursor = export_conn.cursor()

for index, row in sales_staff_DIMENSION.iterrows():
    try:
        # Corrected query without the trailing comma in the VALUES clause
        query = f"""
        INSERT INTO SALES_STAFF 
        (SALES_STAFF_id, SALES_STAFF_name, SALES_STAFF_extention, SALES_STAFF_email, SALES_STAFF_WORK_PHONE_nr, SALES_STAFF_MANAGER_id, SALES_STAFF_DATE_HIRED_date, SALES_STAFF_SALES_BRANCH_id) 
        VALUES 
        ({row['SALES_STAFF_CODE_staff']}, '{row['NAME']}', '{row['EXTENSION_staff']}', '{row['EMAIL_staff']}', 
        '{row['WORK_PHONE_staff']}', {row['MANAGER_CODE_staff']}, '{row['DATE_HIRED_staff']}', '{row['SALES_BRANCH_CODE_staff']}');
        """
        sales_staff_export_cursor.execute(query)
    except pyodbc.Error as e:
        print("An error occurred:", e)
        print(query)

export_conn.commit()
sales_staff_export_cursor.close()



# %%
newQuery= "SELECT * FROM satisfaction"
satisfaction1=pd.read_sql(newQuery,Sales_staff_connection)
satisfaction['YEAR'] = satisfaction1['YEAR']
satisfaction_merge=pd.merge(satisfaction,satisfaction_type, left_on='SATISFACTION_TYPE_CODE', right_on='SATISFACTION_TYPE_CODE')
satisfaction_merge

# %%
satisfaction_export_cursor = export_conn.cursor()

for index, row in satisfaction_merge.iterrows():
    try:
        query = f"""
        INSERT INTO SATISFACTION 
        (DATE_YEAR_nr, SALES_STAFF_id, SATISFACTION_id, date) 
        VALUES 
        ({row['YEAR']}, {row['SALES_STAFF_CODE']}, {row['SATISFACTION_TYPE_CODE']}, '{row['date']}');
        """
        satisfaction_export_cursor.execute(query)
    except pyodbc.Error as e:
        print("An error occurred:", e)
        print(query)

export_conn.commit()
satisfaction_export_cursor.close()



