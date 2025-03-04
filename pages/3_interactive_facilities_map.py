# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import plotly.express as px
import pandas as pd


year = "2021"
year = st.selectbox(label="Year", options=('2011', '2012', '2013', '2014', '2015', \
                                    '2016', '2017', '2018', '2019', '2020', '2021'),
                    placeholder="2021")

num_facilities = "100"
num_facilities = st.slider(label="Number of Facilities", min_value=0, max_value=300, value=100,step=10)

df = pd.read_excel("ghgp_data_by_year.xlsx")
df.dropna(inplace=True) #in this dataset this removes all facilities that don't have data from every year(in the future make this just from 2016-2021 for Sentinel2)

#removes the text at the beginning and correctly assigns the collumns
df.columns = df.iloc[0]
df = df[1:int(num_facilities)]
df = df.reset_index(drop=True)

df = df.sort_values(by="2021 Total reported direct emissions", ascending=False)

size = df[year + ' Total reported direct emissions'].to_list()



print(year)

fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", hover_name='Facility Name', 
                        zoom=3, size=size, color=size, color_continuous_scale=px.colors.diverging.RdYlGn_r,
                        custom_data=['Facility Name', year + ' Total reported direct emissions','Latitude','Longitude','Facility Id'], 
                        opacity=1, title=year + " GHG Emissions by Facility")


fig.update_traces(
    hovertemplate="<br>".join([
        "<b>Facility Name: %{customdata[0]}",
        year + " Emissions: %{customdata[1]}</b>",
        "Latitude: %{customdata[2]}",
        "Longitude: %{customdata[3]}",
        "Facility Id: %{customdata[4]}",
    ])
)




fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# create our callback function
def update_point(trace, points, selector):
    c = list(scatter.marker.color)
    s = list(scatter.marker.size)
    for i in points.point_inds:
        c[i] = '#bae2be'
        s[i] = 20
        with fig.batch_update():
            scatter.marker.color = c
            scatter.marker.size = s

scatter = fig.data[0]

scatter.on_click(update_point)

st.plotly_chart(fig)