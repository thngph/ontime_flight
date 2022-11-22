import streamlit as st
import plotly.express as px
import pandas as pd
import datetime
import plost




# Setting the page title, layout, icon and initial sidebar state.

st.set_page_config(page_title="Airport Ontime Performance",layout='wide', 
page_icon=':airplane:', initial_sidebar_state='expanded')

padding = 0
reduce_header_height_style = """
    <style>
        div.block-container {padding-top : 1rem;}
    </style>
"""
st.markdown(reduce_header_height_style, unsafe_allow_html=True)

@st.cache
def get_data(path):
    return pd.read_csv(path, parse_dates=['FlightDate'])

df_cleaned = get_data('./data/cleaned/2022.csv')


# -----------Side bar------------

# The below code is creating a sidebar on the left side of the page. The sidebar is allowing the user
# to select the airline and the date range.

st.sidebar.header("Please Filter Here:")

airline = st.sidebar.multiselect(
    "Select the Airline:",
    options=df_cleaned["Reporting_Airline"].unique(),
    default=df_cleaned["Reporting_Airline"].unique()
)

d_start = st.sidebar.date_input(
    "Start date:",
    datetime.date(2022, 1, 1),
    min_value=datetime.date(2022, 1, 1),
    max_value=datetime.date(2022, 3, 15))
st.sidebar.write(d_start)

d_end = st.sidebar.date_input(
    "End date:",
    datetime.date(2022, 3, 15),
    min_value=datetime.date(2022, 1, 1),
    max_value=datetime.date(2022, 3, 15))
st.sidebar.write(d_end)

# year = st.sidebar.slider(
#      'Select a range of Year:',
#      2011, 2016, (2014, 2016))
# st.sidebar.write('Values:', year)


df_cleaned_selection = df_cleaned.query(
    "Reporting_Airline == @airline & @d_start <= FlightDate <= @d_end "
)



df_code = df_cleaned_selection[['CarrierDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay',
       'LateAircraftDelay']]

sum_delay = pd.DataFrame(df_code.sum(), columns=['minute']).reset_index()
df_code=df_code.fillna(0)

count = [[col, df_code[df_code[col]>0].count()[0]] for col in df_code.columns]
count_cause=pd.DataFrame(data=count, columns=['Cause', 'Count'])



#-----------Header-----------------------------------
st.markdown('# Reporting-Airline Ontime Performance')
st.write('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras interdum tristique quam id congue. Fusce consequat mi vitae risus euismod, eget sodales est viverra. Phasellus in ultricies libero, vel tristique est. Integer tincidunt sodales nulla et maximus. Vivamus in arcu nisl. Aenean a facilisis eros. Ut semper pretium nibh. Praesent felis leo, accumsan sit amet nisl vel, pretium tincidunt nisl. Ut ullamcorper diam sed metus dapibus varius. Integer sapien risus, congue id ullamcorper porttitor, mollis in odio. Quisque vitae suscipit orci, vitae maximus mauris. Vivamus lacinia in urna et imperdiet. Aenean arcu nibh, ornare ac condimentum eget, vulputate sed felis. Proin sem dolor, fringilla in lacus eu, rhoncus tincidunt sapien. Donec pretium quam sit amet vestibulum tristique.')


col0 = st.columns(1)

flight_count = df_cleaned_selection[['FlightDate','Avg_Delay']].groupby('FlightDate').count().reset_index()
fig = px.line(flight_count, x='FlightDate', y="Avg_Delay")
# fig.update_traces(line_color='black')

col0[0].plotly_chart(fig, use_container_width=True)







st.markdown('### Overview')
col1, col2, col3, col4, col5 = st.columns([1,1,2,2,3])
col1.metric("Number of flight", df_cleaned_selection.shape[0])
col2.metric("Number of Airline", df_cleaned_selection["Reporting_Airline"].nunique())
col3.metric("Total delay time", f"{round(df_cleaned_selection['Avg_Delay'].sum()/60/24, 2)} days")
col4.metric("Avg delay time per flight", f"{round(df_cleaned_selection['Avg_Delay'].mean(), 3)} mins")
col5.metric("Observed days", f"{d_start.strftime('%d/%m/%y')} - {d_end.strftime('%d/%m/%y')}", (d_end-d_start).days, 'off')


#-----------Row 1----------------------



col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('### Cause of Delay')
    st.write('total time (minute)')
    col1.plotly_chart(px.pie(
        sum_delay,
        values='minute',
        names='index',
        template='plotly_white',
    ),
    use_container_width=True)





airlines = pd.read_csv('.\\data\\L_UNIQUE_CARRIERS.csv',
                       names=['CODE', 'AIRLINE'])

c2airline = airlines.set_index('CODE')['AIRLINE'].to_dict()

stats = df_cleaned_selection['Avg_Delay'].groupby(df_cleaned_selection['Reporting_Airline']).describe()[
    ['count', 'mean', 'min', 'max']].sort_values(by='count', ascending=False).reset_index()
stats['Name'] = stats['Reporting_Airline'].replace(c2airline)




with col2:
    st.write('### No. flights per Airline')
    col2.plotly_chart(px.bar(
        stats,
        y='Name',
        x='count',
        color='Reporting_Airline',
        labels={"Name": "Airline", 
                "count": "Quantity"},
        orientation='h',
        template='plotly_white',
        color_discrete_sequence=px.colors.cyclical.IceFire
    ),
    use_container_width=True)

with col3:
    st.write('### Mean delay per Airline')
    
    col_2_bar=px.bar(
        stats,
        y='Name',
        x='mean',
        labels={"Name": "Airline",
                "mean": "Mean delay (minute)"},
        color='Reporting_Airline',
        orientation='h',
        template='plotly_white',
        color_discrete_sequence=px.colors.cyclical.IceFire
        )
    col_2_bar.update_layout(showlegend=False)
    col3.plotly_chart(col_2_bar,
        use_container_width=True)

with col1:
    st.write('### % of flight per company')
    col1.plotly_chart(
        px.pie(
            stats,
            values='count',
            # names='Name',
            color='Reporting_Airline',
            template='plotly_white',
        color_discrete_sequence=px.colors.cyclical.IceFire
        ),use_container_width=True
    )

with col2:
    st.write('### Delay level count per Airline')
    fig=px.histogram(
            df_cleaned_selection,
            y='Reporting_Airline',
            # names='Name',
            color='Delay_Level',
            template='plotly_white',
        )
    col2.plotly_chart(fig, use_container_width=False)

mean = df_cleaned_selection[['DepDelay', 'ArrDelay']].groupby(df_cleaned_selection['Reporting_Airline']).mean().reset_index()

with col3:
    st.write('### DepDelay - ArrDelay in comparison')

    fig=px.histogram(
            mean,
            x=['DepDelay', 'ArrDelay'],
            y='Reporting_Airline',
            # names='Name',
            template='plotly_white',barmode='group',
        )
    col3.plotly_chart(fig, use_container_width=False)