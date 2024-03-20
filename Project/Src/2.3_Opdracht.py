
# %%

import warnings
warnings.simplefilter('ignore')
import pandas as pd
import sqlite3



# %%
Sales_connection= sqlite3.connect("go_sales.sqlite")
Sales_connection



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


# %%
product['PRODUCTION_COST'] = pd.to_numeric(product['PRODUCTION_COST'], errors='coerce')

selected_products = product[(product['PRODUCTION_COST'] > 50.00) & (product['PRODUCTION_COST'] < 100.00)]

selected_products[['PRODUCT_NAME','PRODUCTION_COST']]




# %%
product['MARGIN'] = pd.to_numeric(product['MARGIN'], errors='coerce')

selected_products = product[(product['MARGIN'] < .20) | (product['MARGIN'] > .60)]

selected_products[['PRODUCT_NAME','MARGIN']]


# %%
selected_country = country[(country['CURRENCY_NAME'] == 'francs') ]
selected_country.groupby('COUNTRY')

selected_country['COUNTRY']



# %%
high_margin_products = product[product['MARGIN'] > .50]
unique_intro_dates = high_margin_products['INTRODUCTION_DATE'].unique()
unique_intro_dates


# %%
selected_verkoopAfdeling= retailer_site[(retailer_site['ADDRESS2'].notnull())&(retailer_site['REGION'].notnull())]
selected_verkoopAfdeling[['ADDRESS1', 'CITY']]


# %%
selected_Landen= country[(country['CURRENCY_NAME']=='new dollar')|(country['CURRENCY_NAME']=='dollars')]
selected_Landen['COUNTRY']


# %%
selected_vestigingen = retailer_site[(retailer_site['POSTAL_ZONE'].str.startswith('D')) & (retailer_site['ADDRESS2'].notnull())]
selected_vestigingen[['ADDRESS1', 'ADDRESS2', 'CITY']]

# %%
total_returned_products = returned_item.shape[0]
total_returned_products

# %%
aantal_regios = sales_branch['REGION'].nunique()
aantal_regios


# %%
import numpy as np
laagste_marge = product['MARGIN'].min()

hoogste_marge = product['MARGIN'].max()

gemiddelde_marge = round(product['MARGIN'].mean(), 2)
data = {
    'Laagste marge': [laagste_marge],
    'Hoogste marge': [hoogste_marge],
    'Gemiddelde marge': [gemiddelde_marge]
}

marge_overzicht = pd.DataFrame(data)
marge_overzicht


# %%
aantal_ontbrekende_adressen = retailer_site['ADDRESS2'].isna().count()
aantal_ontbrekende_adressen
retailer_site




# %%
verkochte_producten_met_korting = order_details[order_details['UNIT_SALE_PRICE'] < order_details['UNIT_PRICE']]

verkochte_producten_met_korting['UNIT_PRICE'] = pd.to_numeric(verkochte_producten_met_korting['UNIT_PRICE'], errors='coerce')

gemiddelde_kostprijs_met_korting = verkochte_producten_met_korting['UNIT_PRICE'].mean()

gemiddelde_kostprijs_met_korting



# %%
grouped_by_position = sales_staff.groupby('POSITION_EN').size()
aantal_medewerkers_per_functie = grouped_by_position.reset_index(name='Aantal medewerkers')
aantal_medewerkers_per_functie



# %%
groupedBY_Telefoon= sales_staff.groupby('WORK_PHONE').size()
aantal = groupedBY_Telefoon.reset_index(name='Aantal_available')

meer_dan_vier = aantal[aantal['Aantal_available'] > 4]
meer_dan_vier


# %%
netherlands_customers = country[country['COUNTRY'] == 'Netherlands']

netherlands_locations = retailer_site.merge(netherlands_customers, how='inner', left_on='COUNTRY_CODE', right_on='COUNTRY_CODE')

netherlands_locations[['ADDRESS1', 'CITY']]


# %%
data_met_Eyewear = product_type[product_type['PRODUCT_TYPE_EN'] == 'Eyewear']['PRODUCT_TYPE_CODE']
eyewear_product_names = product[product['PRODUCT_TYPE_CODE'].isin(data_met_Eyewear)]['PRODUCT_NAME']
eyewear_product_names



# %%
branch_managers = sales_staff[sales_staff['POSITION_EN'] == 'Branch Manager']
sales_by_manager = pd.merge(branch_managers, order_header, how='inner', left_on='SALES_STAFF_CODE', right_on='SALES_STAFF_CODE')
sales_with_location = pd.merge(sales_by_manager, retailer_site, how='inner', left_on='RETAILER_SITE_CODE', right_on='RETAILER_SITE_CODE')
result = sales_with_location[['ADDRESS1', 'FIRST_NAME', 'LAST_NAME']].drop_duplicates()
result

# %%
managers = sales_staff[sales_staff['POSITION_EN'].str.contains('Manager')]
sales_by_manager = pd.merge(managers, order_header, how='inner', left_on='SALES_STAFF_CODE', right_on='SALES_STAFF_CODE')
result = sales_by_manager[['POSITION_EN', 'ORDER_DATE']].drop_duplicates()
result


# %%
product_merge = pd.merge(order_details,product,left_on='PRODUCT_NUMBER',how='left',right_on='PRODUCT_NUMBER')
product_type_merge = pd.merge(product_merge, product_type, left_on='PRODUCT_TYPE_CODE',how='left',right_on='PRODUCT_TYPE_CODE')
product_not_sold = product_type_merge['QUANTITY'] > 750
product_type_merge.loc[product_not_sold ,['PRODUCT_NAME','PRODUCT_TYPE_EN']].drop_duplicates()



# %%
product_merge_40_korting = ((product_merge['UNIT_PRICE'].astype(float) - product_merge['UNIT_SALE_PRICE'].astype(float))/product_merge['UNIT_PRICE'].astype(float)) > 0.4
product_merge.loc[product_merge_40_korting,['PRODUCT_NAME']].drop_duplicates()

# %%
returned_item_merge = pd.merge(returned_item,order_details,left_on='ORDER_DETAIL_CODE',how='left',right_on='ORDER_DETAIL_CODE')
returned_item_90 = (returned_item_merge['RETURN_QUANTITY'].astype(float)/returned_item_merge['QUANTITY'].astype(float)) < 0.9
returned_item_merge.loc[returned_item_90,['RETURN_QUANTITY','QUANTITY','RETURN_REASON_CODE']]



# %%
product.groupby('PRODUCT_TYPE_CODE',as_index=False)['PRODUCT_NUMBER'].count()


# %%
retailer_site.groupby('COUNTRY_CODE',as_index=False)['RETAILER_SITE_CODE'].count()

# %%
product_merge = pd.merge(order_details,product,left_on='PRODUCT_NUMBER',how='left',right_on='PRODUCT_NUMBER')
product_merge_cooking_is = product_merge['PRODUCT_TYPE_CODE'].astype(float) == 1
product_merge_cooking = product_merge.loc[product_merge_cooking_is, ['PRODUCT_TYPE_CODE','PRODUCT_NAME','QUANTITY','UNIT_SALE_PRICE']]

product_merge_cooking['QUANTITY'] = pd.to_numeric(product_merge_cooking['QUANTITY'], errors='coerce')
product_merge_cooking ['UNIT_SALE_PRICE'] = pd.to_numeric(product_merge_cooking['UNIT_SALE_PRICE'], errors='coerce')

ge_group = product_merge_cooking.groupby(['PRODUCT_NAME'], as_index=False).agg(
    Total_Quantity=('QUANTITY', 'sum'),
    Average_Price=('UNIT_SALE_PRICE', 'mean')
)
ge_group



# %%
amsterdam_sales_staff = sales_staff[sales_staff['SALES_BRANCH_CODE'] == 'Amsterdam']
targets_2006 = target[(target['SALES_YEAR'] == 2006) & (target['SALES_STAFF_CODE'].isin(amsterdam_sales_staff['SALES_STAFF_CODE']))]


# %%
retailer_country_merge = pd.merge(retailer_site,country,left_on='COUNTRY_CODE',how='left',right_on='COUNTRY_CODE')
retailer_country_branch_merge = pd.merge(sales_branch, retailer_country_merge,left_on='COUNTRY_CODE',how='left',right_on='COUNTRY_CODE')
retailer_country_branch_merge.groupby(['COUNTRY',], as_index=False)['RETAILER_SITE_CODE'].count()


# %%
no_sales_staff = sales_staff[~sales_staff['SALES_STAFF_CODE'].isin(order_header['SALES_STAFF_CODE'])]
result = no_sales_staff[['FIRST_NAME', 'LAST_NAME']]
result



# %%
gemiddelde_marge = product['MARGIN'].mean()
producten_met_lagere_marge = product[product['MARGIN'] < gemiddelde_marge]
aantal_producten_met_lagere_marge = producten_met_lagere_marge.shape[0]
gemiddelde_marge_lagere_producten = producten_met_lagere_marge['MARGIN'].mean()

overzicht = pd.DataFrame({
    'Aantal producten met lagere marge': [aantal_producten_met_lagere_marge],
    'Gemiddelde marge van deze producten': [gemiddelde_marge_lagere_producten]
})
overzicht

# %%
order_details['UNIT_PRICE'] = pd.to_numeric(order_details['UNIT_PRICE'], errors='coerce')

duur_verkochte_producten = order_details[order_details['UNIT_PRICE'] > 500]['PRODUCT_NUMBER']
niet_teruggebrachte_producten = returned_item['ORDER_DETAIL_CODE'].unique()
producten_voor_meer_dan_500_verkocht_niet_teruggebracht = duur_verkochte_producten[~duur_verkochte_producten.isin(niet_teruggebrachte_producten)]
namen_producten = product[product['PRODUCT_NUMBER'].isin(producten_voor_meer_dan_500_verkocht_niet_teruggebracht)]['PRODUCT_NAME']
overzicht = pd.DataFrame({'Producten': namen_producten})
overzicht


# %%
is_manager = []
for index, row in sales_staff.iterrows():
    if 'Manager' in row['POSITION_EN']:
        is_manager.append('Ja') 
    else:
        is_manager.append('Nee') 
sales_staff['Manager'] = is_manager

sales_staff.loc[:, ['LAST_NAME', 'Manager']]

# %%
from datetime import date
date.today().year


# %%
from datetime import datetime

date_str = '16-8-2013'
date_format = '%d-%m-%Y'
date_obj = datetime.strptime(date_str, date_format)

date_obj.year


# %%
current_year = date.today().year

def calculate_years_of_service(hire_date):
    hire_date_obj = datetime.strptime(hire_date, '%d-%m-%Y')
    years_of_service = current_year - hire_date_obj.year
    return years_of_service


dienstverband = []
for index, row in sales_staff.iterrows():
    years_of_service = calculate_years_of_service(row['DATE_HIRED'])
    if years_of_service < 25:
        dienstverband.append('Kort in dienst')
    elif years_of_service >= 12:
        dienstverband.append('Lang in dienst')
    else:
        dienstverband.append('')
        
sales_staff['Dienstverband'] = dienstverband
result = sales_staff[['LAST_NAME', 'Dienstverband']]
result



