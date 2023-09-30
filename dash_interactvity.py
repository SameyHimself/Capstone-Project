import dash_core_components as dcc

# Assume you have a DataFrame called spacex_df with 'Launch Site' column
launch_sites = spacex_df['Launch Site'].unique()

# Create options for the dropdown
options = [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in launch_sites]

# Define the dropdown component
dcc.Dropdown(
    id='site-dropdown',  # Specify the component ID
    options=options,  # Provide the list of options
    value='ALL',  # Set the default value to 'ALL'
    placeholder="Select a Launch Site here",  # Set a placeholder text
    searchable=True  # Enable searching for launch sites
)

import plotly.express as px
from dash import Dash, Input, Output

# Assume spacex_df is your DataFrame

# Define the callback function
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(selected_site):
    if selected_site == 'ALL':
        # If 'ALL' is selected, use all rows in spacex_df
        fig = px.pie(
            spacex_df,
            names='class',
            title='Total Launch Success',
            labels={'class': 'Success'},
            color_discrete_map={0: 'red', 1: 'green'}  # Custom colors for failed and successful launches
        )
    else:
        # If a specific site is selected, filter the DataFrame for that site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Launch Success at {selected_site}',
            labels={'class': 'Success'},
            color_discrete_map={0: 'red', 1: 'green'}
        )

    return fig

dcc.RangeSlider(
    id='payload-slider',
    min=0,
    max=10000,
    step=1000,
    value=[min_payload, max_payload],  # Set initial range values
    marks={0: '0', 10000: '10000'}  # Define slider marks
)

# Define the callback function for the scatter chart
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, payload_range):
    min_payload, max_payload = payload_range
    
    if selected_site == 'ALL':
        filtered_df = spacex_df
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]

    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Payload vs. Launch Outcome',
        range_x=[min_payload, max_payload],  # Set x-axis range based on slider
        labels={'class': 'Launch Outcome'}
    )

    return fig


