# pip install dash
# to run: python dashDemo3Data.py
# View on your browser at http://127.0.0.1:8050/
#
# TO RUN, open anaconda and open the terminal from the base:root environment
# Then change directory to where this progra is on the computer
# Maybe: "cd C:\Users\gilma_acc68ku\OneDrive\Documents\TechCareers\CPRG008_003\CPRG100-PythonData\code>"
# Then, run the command: python dashDemo3Data.py
# After, go to a browser and load the graph on port:8050 (localhost:8050)
#
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash_html_components import Br
from numpy import append
import plotly.express as px
import dash_table
import pandas as pd
from readDB import ReadMongoData as db
import plotly.graph_objects as pgo

# To run locally
# app = dash.Dash("app")
# app = dash_app.Dash("app")

# To run as service in Azure or similar
dash_app = dash.Dash(__name__)
app = dash_app.server

df = db.getBookingDetails()
df1 = db.booking_sales_by_supplier_by_region
df2 = db.booking_sales_by_region_by_agent

# Convert the Decimal128 columns to float to work for the dash_table.DataTable
df[["BasePrice",
    "AgencyCommission"]] = df[["BasePrice",
                               "AgencyCommission"]].astype(str).astype(float)

df1[["BasePrice",
     "AgencyCommission"]] = df1[["BasePrice",
                                 "AgencyCommission"]].astype(str).astype(float)

df2[["BasePrice",
     "AgencyCommission"]] = df2[["BasePrice",
                                 "AgencyCommission"]].astype(str).astype(float)

# Create a sunburst graph to show total sales by supplier by region
fig1 = px.sunburst(df1, path=['RegionName', 'SupName'], values='BasePrice')

# Base Price by Region and agent
fig4 = px.sunburst(df2, path=['AgtEmail', 'RegionName'], values='BasePrice')

# Commission by Region and agent
fig5 = px.sunburst(df2,
                   path=['AgtEmail', 'RegionName'],
                   values='AgencyCommission')

# Create a histogram to show quaterly base price average
fig2 = px.histogram(df1,
                    x="BookingDate",
                    y="BasePrice",
                    histfunc="avg",
                    title="Quaterly Average Base Price")
fig2.update_traces(xbins_size="M3")
fig2.update_xaxes(showgrid=True,
                  ticklabelmode="period",
                  dtick="M3",
                  tickformat="%b\n%Y")
fig2.update_layout(bargap=0.1)
fig2.add_trace(
    pgo.Scatter(mode="markers",
                x=df1["BookingDate"],
                y=df["BasePrice"],
                name="Quarterly"))

# Summary for destinations
df_group_destination = df.groupby(["Destination"
                                   ]).sum()[["BasePrice", "AgencyCommission"]]
fig = px.bar(df_group_destination, x=df_group_destination.index, y="BasePrice")

# Selecting and renaming of columns for data frame table
new_column_names = [
    'Region', 'Supplier', 'Booking Description', 'Destination', 'Base Price'
]
df_column_names = [
    'RegionName', 'SupName', 'Description', 'Destination', 'BasePrice'
]

app.layout = html.Div(children=[
    html.A(href='/', children='Home'),
    html.H1(children='Travel Experts data'),
    html.Div(children=['Base price totals per region per supplier']),
    html.Br(),
    dash_table.DataTable(
        id='mytable',
        columns=[{
            'name': col,
            'id': df_column_names[idx]
        } for (idx, col) in enumerate(new_column_names)],
        data=df1.to_dict('records'),
        page_size=20

        # dash_table.DataTable(
        #     id='mytable',
        #     columns=[{"name": i, "id": i} for i in df1.columns],
        #     data=df1.to_dict('records'),
        #     page_size=30
    ),
    html.Div(children=["Base Price by suppliers and regionn ..."]),
    html.Br(),
    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig4),
    dcc.Graph(figure=fig5),
    dcc.Graph(figure=fig2)
])

if __name__ == '__main__':
    dash_app.run_server(debug=True)

# To run locally comment out the if statement above
# and then the following line should be: app.run_server(debug=True)
