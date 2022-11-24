import streamlit as st
import pandas as pd
import datetime

import folium
import airportsdata
from streamlit_folium import st_folium
from folium.features import DivIcon


st.set_page_config(page_title="Reporting-Airline Ontime Performance", layout='centered',
                   page_icon=':airplane:')

st.markdown('# Reporting-Airline Ontime Performance')
st.markdown('## Connection maps')

st.write('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras interdum tristique quam id congue. Fusce consequat mi vitae risus euismod, eget sodales est viverra. Phasellus in ultricies libero, vel tristique est. Integer tincidunt sodales nulla et maximus. Vivamus in arcu nisl. Aenean a facilisis eros. Ut semper pretium nibh. Praesent felis leo, accumsan sit amet nisl vel, pretium tincidunt nisl. Ut ullamcorper diam sed metus dapibus varius. Integer sapien risus, congue id ullamcorper porttitor, mollis in odio. Quisque vitae suscipit orci, vitae maximus mauris. Vivamus lacinia in urna et imperdiet. Aenean arcu nibh, ornare ac condimentum eget, vulputate sed felis. Proin sem dolor, fringilla in lacus eu, rhoncus tincidunt sapien. Donec pretium quam sit amet vestibulum tristique.')



#---------------------------- [ DATA PREPARATION ] ----------------------------


airports = airportsdata.load('IATA')




@st.cache
def get_data(path):
    return pd.read_csv(path, parse_dates=['FlightDate'])


df_cleaned = get_data('./data/cleaned/2022.csv')



#---------------------------- [ SELECT AIRPORT ] ----------------------------

airline = st.selectbox(
    "Select the Airline:",
    options=df_cleaned["Reporting_Airline"].unique(),
)


high_date = datetime.date(2022, 2, 28)
df = df_cleaned.query(
    "Reporting_Airline == @airline & FlightDate == @high_date "
)[['Origin', 'Dest']]








def draw_map():
    """ Return a folium.Map() object represents flights of selected airport.
    """

    df_count=df.groupby(['Origin', 'Dest']).size().reset_index(name='counts')

    m = folium.Map(location=[39.198744, -102.083682],  width=750, height=500)
    m.fit_bounds([[45, -125], [24, -60]])

    for i in range(df_count.shape[0]):
        
        
        try:
            lat1, lon1,lat2, lon2=airports[df_count.iloc[i][0]]['lat'], airports[df_count.iloc[i][0]]['lon'], airports[df_count.iloc[i][1]]['lat'],  airports[df_count.iloc[i][1]]['lon']
            folium.PolyLine([[lat1, lon1],  [lat2, lon2]],weight = 0.2).add_to(m)
        except:
            pass
    list_airport=[*list(df_count['Origin']), *list(df_count['Dest'])]
    airport=set(list_airport)
    for i in airport:
        try:
            folium.map.Marker(
                [airports[i]['lat'], airports[i]['lon']],
                icon=DivIcon(
                    icon_size=(250,36),
                    icon_anchor=(0,0),
                    html='<div style="font-size: 8pt">'+i+'</div>',
                    )
                ).add_to(m)
        except:
            pass

    return m


map = draw_map()

st_folium(map,width=750, height=500)
