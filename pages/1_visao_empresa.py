import pandas         as pd
import numpy          as np
import seaborn        as sns
import plotly.express as px
import re
import inflection
import folium
import streamlit as st

from haversine            import haversine
from matplotlib           import pyplot as plt
from PIL                  import Image
from streamlit_folium            import folium_static

def clean_code(df1):
    old_cols = ['ID', 'Delivery_person_ID', 'Delivery_person_Age',
       'Delivery_person_Ratings', 'Restaurant_latitude',
       'Restaurant_longitude', 'Delivery_location_latitude',
       'Delivery_location_longitude', 'Order_Date', 'Time_Orderd',
       'Time_Order_picked', 'Weatherconditions', 'Road_traffic_density',
       'Vehicle_condition', 'Type_of_order', 'Type_of_vehicle',
       'multiple_deliveries', 'Festival', 'City', 'Time_taken(min)']

    snake_case = lambda x: inflection.underscore(x)

    new_cols = list( map(snake_case, old_cols))
    df1.columns = new_cols

    # Excluir as linhas com a idade dos entregadores vazia
    # ( Conceitos de seleção condicional )
    linhas_selecionadas = df1['delivery_person_age'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1['road_traffic_density'] != 'NaN ') 
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1['city'] != 'NaN ') 
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = (df1['festival'] != 'NaN ') 
    df1 = df1.loc[linhas_selecionadas, :].copy()

    # Conversao de texto/categoria/string para numeros inteiros
    df1['delivery_person_age'] = df1['delivery_person_age'].astype( int )

    # Conversao de texto/categoria/strings para numeros decimais
    df1['delivery_person_ratings'] = df1['delivery_person_ratings'].astype( float )

    # Conversao de texto para data
    df1['order_date'] = pd.to_datetime( df1['order_date'], format='%d-%m-%Y' )

    linhas_vazias = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )

    df1['time_taken(min)'] = df1['time_taken(min)'].apply(lambda x: x.split('(min) ')[1])
    df1['time_taken(min)'] = df1['time_taken(min)'].astype(int)

    df2 = df1.copy()

    return df2

def order_pday(df2):
    aux1 = df2[['id', 'order_date']].groupby('order_date').count().reset_index()
    aux1.columns = ['order_date', 'qtd_entregas']
    fig = px.bar(aux1, x='order_date', y='qtd_entregas')

    return fig

def order_ptraffic(df2):
    aux1 = df2.loc[:, ['id', 'road_traffic_density']].groupby( 'road_traffic_density' ).count().reset_index()
    aux1['traffic_perc'] = ( aux1['id'] / aux1['id'].sum() ) * 100

    fig2 = px.pie( aux1, values='traffic_perc', names='road_traffic_density' )

    return fig2

def order_pct_ptf(df2):
    aux2 = df2[['id', 'city','road_traffic_density']].groupby( ['city', 'road_traffic_density'] ).count().reset_index()
    fig3 = scatter_graph = px.scatter(aux2, x='city', y='road_traffic_density', size='id', color='city')
    return fig3

def order_pweek(df2):
    df2['week_of_year'] = df2['order_date'].dt.strftime('%U') 
    aux1 = df2[['id', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()
    fig4 = px.line(aux1, x='week_of_year', y='id')

    return fig4

def order_pet_pweek(df2):
    aux1 = df2[['id', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()
    aux2 = df2[['delivery_person_id', 'week_of_year']].groupby( 'week_of_year' ).nunique().reset_index()

    aux3 = pd.merge( aux1, aux2, how='inner' )
    aux3['order_by_delivery'] = aux3['id'] / aux3['delivery_person_id']
    fig5 = px.line(aux3, x='week_of_year', y='order_by_delivery')
    return fig5

def country_map(df2):
    data_plot = df2.loc[:, ['city', 'road_traffic_density', 'delivery_location_latitude', 'delivery_location_longitude']].groupby(['city', 'road_traffic_density']).median().reset_index()

    map_ = folium.Map(zoom_start=11)
    for index, location_info in data_plot.iterrows():
        folium.Marker([location_info['delivery_location_latitude'], location_info['delivery_location_longitude']]).add_to(map_)

    folium_static(map_, width=1024, height=600)

df = pd.read_csv( 'datasets/train.csv' )

df1 = df.copy()

df2 = clean_code(df1)

# STREAMLIT

st.header('Visualização Perguntas de Negócio - Visão Empresa')

image = Image.open('reports/images/logo.png') 
st.sidebar.image(image, width=120)

st.sidebar.markdown("# Made in Asia Restaurant")
st.sidebar.markdown('## Filtro')
st.sidebar.markdown("""---""")
st.sidebar.markdown('## Selecione uma data limite')

data_slider = st.sidebar.slider('Valores', value=pd.datetime(2022, 4, 13),min_value=pd.datetime(2022, 2, 11),max_value=pd.datetime(2022, 4, 6), format='DD-MM-YYYY')

st.sidebar.markdown("""---""")

st.sidebar.markdown('## Selecione uma ou mais condições')
traffic_options = st.sidebar.multiselect( 'Condições do trânsito', ['Low ', 'Medium ', 'High ', 'Jam '], default = ['Low ', 'Medium ', 'High ', 'Jam '])
st.sidebar.markdown("""---""")

linhas_selec = df2['order_date'] < data_slider
df2 = df2.loc[linhas_selec, :]

linhas_selec = df2['road_traffic_density'].isin(traffic_options) 
df2 = df2.loc[linhas_selec, :]

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Estratégica', 'Visão Geográfica'])   

with tab1:
    with st.container():
        st.markdown('## Quantidade de Pedidos por Dia') 
        fig = order_pday(df2)  
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('## Distribuição dos pedidos por tipo de tráfego - Porcentagem')
            fig2 = order_ptraffic(df2)
            st.plotly_chart(fig2, use_container_width=True)

        with col2:
            st.markdown('## Comparação do volume de pedidos por cidade e tipo de tráfego')
            
            fig3 = order_pct_ptf(df2)
            st.plotly_chart(fig3, use_container_width=True)

with tab2:
    with st.container():
        st.markdown('## Quantidade de pedidos por semana') 
        fig4 = order_pweek(df2)
        st.plotly_chart(fig4, use_container_width=True)

    with st.container():
        st.markdown('## Quantidade de pedidos por entregador por semana')
        fig5 = order_pet_pweek(df2)
        st.plotly_chart(fig5, use_container_width=True)

with tab3:
    st.markdown('## A localização central de cada cidade por tipo de tráfego')
    country_map(df2)