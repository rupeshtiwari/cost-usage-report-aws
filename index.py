import pandas as pd

# Load the previous and current CUR CSV files
previous_csv = pd.read_csv('previous_cur.csv')
current_csv = pd.read_csv('current_cur.csv')

# Column name
service_name_col = 'WAF'

# Group the data by service name
previous_grouped = previous_csv.groupby(service_name_col).sum().reset_index()
current_grouped = current_csv.groupby(service_name_col).sum().reset_index()

# Compare aggregated data by service name
new_data = current_grouped[~current_grouped[service_name_col].isin(previous_grouped[service_name_col])]
modified_data = current_grouped.merge(previous_grouped, on=service_name_col, how='inner',
                                      suffixes=('_current', '_previous'))
modified_data = modified_data[(modified_data.drop(service_name_col, axis=1) !=
                               modified_data.drop(service_name_col, axis=1).shift()).any(axis=1)]

# Process and analyze the results
if not new_data.empty:
    print("New data found by service name:")
    print(new_data)

if not modified_data.empty:
    print("Modified data found by service name:")
    print(modified_data)
