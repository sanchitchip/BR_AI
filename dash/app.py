import sys
import geopandas as gpd
from datetime import date
from datetime import datetime as dt
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash
import numpy as np
import xarray as xr
import plotly.express as px
from shapely import geometry
from xarray.core.indexing import is_fancy_indexer
sys.path.insert(1, "../functions/")
import io_pipe
import nd_index
import filter
import aggregate
import plot_utils

# import local function

munich = gpd.read_file('../geojson/munich.geojson')
interested_area = munich.geometry.unary_union
bbox_interested_area = interested_area.bounds

# eopatch = io_pipe.read_eopatch('../example_data/ld8_example')
# read simpale data
data = np.load("../data/image_dump.npz",allow_pickle =True)
time = np.load("../data/timestamp.npz",allow_pickle =True)

# create data frame for choropleth map 
tem_geometry = [geometry.box(*pixel_box) for pixel_box in data["bbox"]]

geo_df = gpd.GeoDataFrame({
    'value': data["Temp"].max(axis=1),
    'geometry': tem_geometry
})

island_aggregate_data = filter.get_island_submatrix(data["data"],data['blobs'],dim_error=True)
ndvi_df = aggregate.get_index_plot_data(island_aggregate_data=island_aggregate_data,timestamp=time["timestamp"],bbox=data['bbox'])
ndwi_df = aggregate.get_index_plot_data(island_aggregate_data=island_aggregate_data,timestamp=time["timestamp"],bbox=data['bbox'],index_name='ndwi') 
lst_df = aggregate.get_index_plot_data(island_aggregate_data=island_aggregate_data,timestamp=time["timestamp"],bbox=data['bbox'],index_name='temp') 

ndvi_line_df = aggregate.get_line_data(ndvi_df,type='max')
ndwi_line_df = aggregate.get_line_data(ndwi_df,type='max')
lst_line_df = aggregate.get_line_data(lst_df,type='max')


coord_data = aggregate.get_plot_coord(bbox=data['bbox'],island_aggregate_data=island_aggregate_data)
years_timestamp = [dt.date(i) for i in time['timestamp']]


mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"


bands=['B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B09','B10', 'B11', 'BQA']
# bands = ['B01', 'B02', 'B03', 'B04', 'B05', 'B06',
        #  'B07', 'B08', 'B8A', 'B09', 'B10', 'B11', 'B12']

YEARS = [2014, 2015, 2016, 2017, 2018]
         

MONTHs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

initial_fig = px.choropleth_mapbox(geo_df,
                                   geojson=geo_df.geometry,
                                   locations=geo_df.index,
                                   color="value",
                                   center={"lat": 48.286602, "lon": 11.58578},
                                   mapbox_style="open-street-map",
                                   opacity=0.5,
                                   zoom=8.5)
initial_fig.update_layout(
    mapbox=dict(
        accesstoken=mapbox_access_token,
    ),
    height=770,
    hovermode="closest",
    margin=dict(r=0, l=0, t=0, b=0),
    dragmode="lasso",
)




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# Build App
app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
# App layout

app.layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            children=[
                html.Img(id="logo", src=app.get_asset_url("dash-logo.png")),
                html.H4(children="BR_AI description"),
                html.P(
                    id="description",
                    children="Demo for Urban Heat Island ",
                ),
            ],
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[

                        html.Div(
                            id="heatisland-container",
                            children=[
                                html.P(
                                    "Heat island detection in year {0}".format(
                                        min(YEARS)
                                    ),
                                    id="heatisland-title",
                                ),
                                dcc.Graph(
                                    id="munich-choropleth",
                                    figure=initial_fig,
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    id="graph-container",
                    children=[
                        html.P(
                            id="slider-text",
                            children="Drag the slider to change the year:",
                        ),
                        
                        dcc.Slider(
                            id="years-slider",
                            min=min(YEARS),
                            max=max(YEARS),
                            value=min(YEARS),
                            marks={
                                str(year): {
                                    "label": str(year),
                                    "style": {"color": "#7fafdf"},
                                }
                                for year in YEARS
                            },
                        ),

                        # html.P(id="months-select-text", children="Select Months:"),
                        # dcc.RangeSlider(
                        #     id='month-range-slider',
                        #     min=1,
                        #     max=12,
                        #     step=1,
                        #     value=[7,9]
                        # ),
                        # html.Div(id='range-slider-text'),
                        
                        dcc.Tabs(id='tabs-index',
                                value='ndvi',
                                children=[
                                    dcc.Tab(label='NDVI', value='ndvi'),
                                    dcc.Tab(label='NDWI', value='ndwi'),
                                     dcc.Tab(label='TEMP', value='temp'),
                                ]
                        ),
                        html.Div(id='tabs-content'),
                        # dcc.Dropdown(
                        #     id="index-dropdown",
                        #     options=[
                        #         {'label': 'NDVI', 'value': 'ndvi'},
                        #         {'label': 'NDWI', 'value': 'ndwi'}
                        #     ],
                        #     value="ndvi",
                        # ),

                        dcc.Graph(
                            id="selected-data",
                            
                        ),
                        dcc.Graph(
                            id="index-line",
                        ),
                    ],
                ),
            ],
        ),
    ],
)


# callback for tabs content
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs-index', 'value'),Input('years-slider', 'value')])
def render_content(tab,year):
    if tab == 'ndvi':
        return html.Div([
            html.H3('We are looking NDVI in {}'.format(year),)
            
        ])
    if tab == 'ndwi':
        return html.Div([
            html.H3('We are looking NDWI in {}'.format(year),)
        ])
    if tab == 'temp':
        return html.Div([
            html.H3('We are looking TEMP in {}'.format(year),)
        ])



# Year callback
@app.callback(Output("heatisland-title", "children"), [Input("years-slider", "value")])
def update_map_title(year):
    return "Heat island detection in year {0}".format(
        year
    )


# add graphs in Tabs
@app.callback(
     Output("selected-data", "figure"),
    [Input("years-slider", "value")],
    [Input("tabs-index", "value")],
    [Input("munich-choropleth", "selectedData")],
)
def add_tab_graph(year_value, tabs_label,island_index):
    try:
        select_index = island_index['points'][0]["pointIndex"]
    except (TypeError, IndexError):
        select_index = 0
    
    if str(tabs_label) == "ndvi":
        xr_data = ndvi_df.loc[select_index,str(year_value)]
        xr_time = [sub_year for sub_year in years_timestamp if sub_year.year==year_value]
        space_lati = coord_data[select_index]['space_lati']
        space_long = coord_data[select_index]['space_long']
        xr_array = xr.DataArray(xr_data,coords=[xr_time,space_lati[::-1],space_long],dims=['time','lati','long'])
        fig=px.imshow(xr_array,animation_frame='time',zmin=-1,zmax=1,color_continuous_scale='Greens')
        fig.update_yaxes(autorange=True,automargin=True)
        fig.update_layout(
            height=300,
        margin=dict(r=0, l=0, t=0.5, b=0.1),)
        return fig

    if str(tabs_label) == "ndwi":
        xr_data = ndwi_df.loc[select_index,str(year_value)]
        xr_time = [sub_year for sub_year in years_timestamp if sub_year.year==year_value]
        space_lati = coord_data[select_index]['space_lati']
        space_long = coord_data[select_index]['space_long']
        xr_array = xr.DataArray(xr_data,coords=[xr_time,space_lati[::-1],space_long],dims=['time','lati','long'])
        fig=px.imshow(xr_array,animation_frame='time',zmin=-1,zmax=1,color_continuous_scale='Blues')
        fig.update_yaxes(autorange=True,automargin=True)
        fig.update_layout(
            height=300,
            margin=dict(r=0, l=0, t=0.5, b=0.3),)
        return fig
    
    if str(tabs_label) == "temp":
        xr_data = lst_df.loc[select_index,str(year_value)]
        xr_time = [sub_year for sub_year in years_timestamp if sub_year.year==year_value]
        space_lati = coord_data[select_index]['space_lati']
        space_long = coord_data[select_index]['space_long']
        xr_array = xr.DataArray(xr_data,coords=[xr_time,space_lati[::-1],space_long],dims=['time','lati','long'])
        fig=px.imshow(xr_array,animation_frame='time',zmin=20,zmax=45,color_continuous_scale='Reds')
        fig.update_yaxes(autorange=True,automargin=True)
        fig.update_layout(
            height=300,
            margin=dict(r=0, l=0, t=0.5, b=0.3),)
        return fig
    return

@app.callback(
     Output("index-line", "figure"),
    [Input("tabs-index", "value")],
    [Input("munich-choropleth", "selectedData")],
)
def add_tab_line(tabs_label,island_index):
    try:
        select_index = island_index['points'][0]["pointIndex"]
    except (TypeError, IndexError):
        select_index = 0
    
    if str(tabs_label) == "ndvi":
        fig = plot_utils.plot_dash_line(ndvi_line_df,select_index)
        return fig
    if str(tabs_label) == "ndwi":
        fig = plot_utils.plot_dash_line(ndwi_line_df,select_index)
        return fig
    if str(tabs_label) == "temp":
        fig = plot_utils.plot_dash_line(lst_line_df,select_index)
        return fig
    return



if __name__ == "__main__":
    app.run_server(debug=True, port=8200)
