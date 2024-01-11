'''
Program Name: Advanced Commodity Data "Final Project"
Author: Sai Prudvi Raj Yerrapragada
Program Description: This program is a comprehensive tool for analyzing and visualizing commodity price trends over time. It is tailored to extract data from the 'produce_csv.csv' file, 
enabling detailed examination and comparison of commodity prices across multiple cities. 

Revisions:
00 - Initial setup for data processing, including the removal of currency symbols and conversion of price strings to floating-point numbers for precise calculations.

01 - Implementation of a user interface to select specific commodities, date ranges, and locations. This feature enhances user engagement and allows for tailored data analysis.

02 - Integration of Plotly for generating interactive and informative grouped bar graphs, providing a visual understanding of price trends.

03 - Extensive code documentation for clarity and ease of maintenance. Each function and segment is thoroughly commented for better comprehension and future reference.

04 - Update of graphical representation features in Plotly, including customization of axis titles, chart title, and currency formatting for a more polished and informative output.

'''
import csv
from datetime import datetime
import plotly.offline as plotly_offline
import plotly.graph_objs as plotly_graph

# Read and preprocess data
with open('C:\\Users\\saipr\\Downloads\\produce_csv.csv', 'r') as file:
    csv_reader = csv.reader(file)
    raw_data = [line for line in csv_reader]

processed_data = []
for line in raw_data:
    processed_line = []
    for element in line:
        if "$" in element:
            processed_line.append(float(element.replace("$", "")))
        elif "/" in element:
            processed_line.append(datetime.strptime(element, '%m/%d/%Y'))
        else:
            processed_line.append(element)
    processed_data.append(processed_line)

# Extract location of the data
location_headers = processed_data.pop(0)[2:]

# Create record for the entries
detailed_records = []
for line in processed_data:
    base_info = line[:2]
    for location, price in zip(location_headers, line[2:]):
        detailed_records.append(base_info + [location, price])

# Function to print the columns
def print_columns(items, index_width=2, column_width=20):
    line_output = ''
    for idx, item in enumerate(items):
        if len(line_output) < 3 * (column_width + index_width + 2):
            if index_width:
                line_output += f'[{idx:{index_width}}] '
            line_output += f'{item:<{column_width}}'
        else:
            print(line_output)
            line_output = ''
            if index_width:
                line_output += f'[{idx:>{index_width}}] '
            line_output += f'{item:<{column_width}}'
    if line_output:
        print(line_output)

# User interface for the data selection
print('='*30, "\nAnalysis of Commodity Data\n" + '='*30)
print('\nSELECT PRODUCTS BY NUMBER...')
unique_commodities = sorted(list(set([record[0] for record in detailed_records])))
print_columns(unique_commodities)

selected_product_indices = input('Enter product numbers separated by spaces: ').strip().split(' ')
selected_product_indices = [int(num) for num in selected_product_indices]
selected_products = [unique_commodities[idx] for idx in selected_product_indices]
print('Selected products:', *selected_products)

print('\nSELECT DATE RANGE BY NUMBER...')
unique_dates = sorted(list(set([record[1] for record in detailed_records])))
print_columns([datetime.strftime(date, "%Y-%m-%d") for date in unique_dates], column_width=10)

start_date, end_date = [int(x) for x in input('\nEnter start/end date numbers separated by a space: ').strip().split(' ')]
selected_date_range = unique_dates[start_date:end_date + 1]
print(f'Dates from {datetime.strftime(unique_dates[start_date], "%Y-%m-%d")} to {datetime.strftime(unique_dates[end_date], "%Y-%m-%d")}')

print('\nSELECT LOCATIONS BY NUMBER...')
unique_locations = sorted(list(set([record[2] for record in detailed_records])))
print_columns(unique_locations)

selected_location_indices = input('\nEnter location numbers separated by spaces: ').strip().split()
selected_locations = [unique_locations[int(loc)] for loc in selected_location_indices]
print('Selected locations:', *selected_locations)

filtered_records = [record for record in detailed_records if record[0] in selected_products
                                                           and record[1] in selected_date_range
                                                           and record[2] in selected_locations]
print(f'{len(filtered_records)} records have been selected')

# Calculating the average of prices
average_prices = {}
for location in selected_locations:  # Only iterate over selected locations
    average_prices[location] = {}
    for product in selected_products:
        product_records = [rec for rec in filtered_records if rec[0] == product and rec[2] == location]
        if product_records:
            average_prices[location][product] = sum(rec[3] for rec in product_records) / len(product_records)

# Plotting the data with Plotly
plot_bars = []
for location in selected_locations:  # Use selected_locations here
    product_prices = [average_prices[location].get(product, 0) for product in selected_products]
    plot_bars.append(plotly_graph.Bar(
        x=selected_products,
        y=product_prices,
        name=location
    ))

layout = plotly_graph.Layout(
    barmode='group',
    title=f'Produce Prices from {datetime.strftime(unique_dates[start_date], "%Y-%m-%d")} through {datetime.strftime(unique_dates[end_date], "%Y-%m-%d")}',
    xaxis=dict(
        categoryorder='array',
        categoryarray=selected_products
    ),
    yaxis=dict(
        title='Average Price',
        tickformat='$.2f'
    ),
    legend_title=dict(text='Locations')
)

figure = plotly_graph.Figure(data=plot_bars, layout=layout)
figure.update_xaxes(title_text="Product")

plotly_offline.plot(figure, filename='bar.html')


