import pandas         as pd
import numpy          as np
import seaborn        as sns
import plotly.express as px
import re
import inflection
import folium
import streamlit as st

from haversine            import haversine
from IPython.core.display import HTML
from matplotlib           import pyplot as plt
from PIL                  import Image
from streamlit_folium            import folium_static

df = pd.read_csv( 'datasets/train.csv' )

df1 = df.copy()

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
#
linhas_vazias = df1['multiple_deliveries'] != 'NaN '
df1 = df1.loc[linhas_vazias, :].copy()
df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )

df1['time_taken(min)'] = df1['time_taken(min)'].apply(lambda x: x.split('(min) ')[1])
df1['time_taken(min)'] = df1['time_taken(min)'].astype(int)

df2 = df1.copy()

# STREAMLIT

st.header('Visualização Perguntas de Negócio - Visão Entregadores')

image_path = 'reports/images/logo.png'
image = Image.open(image_path) 
st.sidebar.image(image, width=120)

st.sidebar.markdown("# Asian's Restaurant")
st.sidebar.markdown('## Filtro')
st.sidebar.markdown("""---""")
st.sidebar.markdown('## Selecione uma data limite')

data_slider = st.sidebar.slider('Valores', value=pd.datetime(2022, 4, 13),min_value=pd.datetime(2022, 2, 11),max_value=pd.datetime(2022, 4, 6), format='DD-MM-YYYY')

st.sidebar.markdown("""---""")

traffic_options = st.sidebar.multiselect( 'Quais as condições do trânsito', ['Low ', 'Medium ', 'High ', 'Jam '], default = ['Low ', 'Medium ', 'High ', 'Jam '])
st.sidebar.markdown("""---""")

linhas_selec = df2['order_date'] < data_slider
df2 = df2.loc[linhas_selec, :]

linhas_selec = df2['road_traffic_density'].isin(traffic_options) 
df2 = df2.loc[linhas_selec, :]

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '_', '_'])   

with tab1:
    with st.container():
        st.markdown('## Visualização Geral')
        col1, col2, col3, col4 = st.columns(4, gap='large')
        with col1:
            max_age = df2['delivery_person_age'].max()
            col1.metric('Maior idade', max_age)
        with col2:
            min_age = df2['delivery_person_age'].min()
            col2.metric('Menor idade', min_age)
        with col3:
            min_cond = df2['vehicle_condition'].min()
            col3.metric('Pior Condição', min_cond)
        with col4:
            max_cond = df2['vehicle_condition'].max()
            col4.metric('Melhor Condição', max_cond)

    with st.container():
        st.markdown("""___""")
        st.markdown('## Avaliações')
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('### Avaliações médias por Entregador')
            mean_rate = df2[['delivery_person_ratings', 'delivery_person_id']].groupby( 'delivery_person_id' ).mean().reset_index()
            mean_rate.columns = ['delivery_person_id', 'delivery_mean_id']
            st.dataframe(mean_rate)
        with col2:
            st.markdown('### Avaliações médias por Trânsito')
            aux_rate = df2[['delivery_person_ratings', 'road_traffic_density']].groupby( 'road_traffic_density' ).agg({'delivery_person_ratings' : ['mean', 'std' ]})
            aux_rate.columns = ['delivery_mean', 'delivery_std']
            aux_rate.reset_index()
            st.dataframe(aux_rate)
            st.markdown('### Avaliações médias por Clima')
            aux_cond = df2[['delivery_person_ratings', 'weatherconditions']].groupby( 'weatherconditions' ).agg({'delivery_person_ratings' : ['mean', 'std' ]})
            aux_cond.columns = ['delivery_mean', 'delivery_std']
            aux_cond.reset_index()
            st.dataframe(aux_cond)
 
    with st.container():
        st.markdown("""___""")
        st.markdown('## Velocidade de Entrega')
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('### Entregadores mais rápidos')
            aux = df2[['city', 'delivery_person_id', 'time_taken(min)']].groupby(['city', 'delivery_person_id']).min().sort_values(['time_taken(min)', 'city'], ascending=True).reset_index()

            aux1 = aux.loc[aux['city'] == 'Metropolitian ', :].head(10)
            aux2 = aux.loc[aux['city'] == 'Urban ', :].head(10)
            aux3 = aux.loc[aux['city'] == 'Semi-Urban ', :].head(10)
            aux4 = aux.loc[aux['city'] == 'NaN ', :].head(10)

            top_10_fast = pd.concat([aux1, aux2, aux3, aux4]).reset_index(drop=True)
            st.dataframe(top_10_fast)
        with col2:
            st.markdown('### Entregadores mais lentos')
            aux = df2[['city', 'delivery_person_id', 'time_taken(min)']].groupby(['city', 'delivery_person_id']).max().sort_values(['time_taken(min)', 'city'], ascending=False).reset_index()

            aux1 = aux.loc[aux['city'] == 'Metropolitian ', :].head(10)
            aux2 = aux.loc[aux['city'] == 'Urban ', :].head(10)
            aux3 = aux.loc[aux['city'] == 'Semi-Urban ', :].head(10)
            aux4 = aux.loc[aux['city'] == 'NaN ', :].head(10)

            top_10_slow = pd.concat([aux1, aux2, aux3, aux4]).reset_index(drop=True)
            st.dataframe(top_10_slow)
