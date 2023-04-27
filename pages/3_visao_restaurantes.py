import pandas               as pd
import numpy                as np
import seaborn              as sns
import plotly.express       as px
import plotly.graph_objects as go
import re
import inflection
import folium
import streamlit as st

from haversine            import haversine
from IPython.core.display import HTML
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

def calc_dist(df2):
    cols = ['restaurant_latitude', 'restaurant_longitude', 'delivery_location_latitude', 'delivery_location_longitude']

    df2['distance'] = df2.loc[:, cols].apply(lambda x: haversine((x['restaurant_latitude'], x['restaurant_longitude']), (x['delivery_location_latitude'], x['delivery_location_longitude'])), axis=1)

    aux_dist = np.round(df2['distance'].mean())

    return aux_dist

def time_pcity(df2):
    aux = df2[['time_taken(min)', 'city']].groupby('city').agg({'time_taken(min)' :  ['mean', 'std']}).reset_index()
    aux.columns = ['city', 'time_mean', 'time_std']

    fig = go.Figure()
    fig.add_trace(go.Bar(name='Control', x=aux['city'], y=aux['time_std'], error_y=dict(type='data', array=aux['time_std'])))

    fig.update_layout(barmode='group')

    return fig

def time_pent(df2):
    aux3 = df2[['road_traffic_density', 'time_taken(min)', 'city']].groupby(['city', 'road_traffic_density']).agg({'time_taken(min)': ['mean', 'std']}).reset_index()
    aux3.columns = ['city', 'road_traffic_density', 'time_mean', 'time_std']
    
    fig2 = px.sunburst(aux3, path=['city', 'road_traffic_density'], values='time_mean', color='time_std', color_continuous_scale='RdBu', color_continuous_midpoint=np.average(aux3['time_std']))

    return fig2

df = pd.read_csv( 'datasets/train.csv' )

df1 = df.copy()

df2 = clean_code(df1)

# STREAMLIT

st.header('Visualização Perguntas de Negócio - Visão Restaurantes')

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

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '_', '_'])   

with tab1:
    with st.container():
        st.markdown('## Visualização Geral')
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.markdown('##### Entregadores únicos')
            qtd1 = df2['delivery_person_id'].unique()
            qtd2 = len(qtd1)
            col1.metric('Entregadores', qtd2)
        with col2:
            st.markdown('##### Distância média')
            aux_dist = calc_dist(df2)
            col2.metric('Distância Média', aux_dist)
        with col3:
            st.markdown('##### Tempo médio c/Festival')
            aux_fest = df2.loc[df2['festival'] == 'Yes ', ['time_taken(min)', 'festival']].groupby('festival').agg({'time_taken(min)' : ['mean', 'std']})
            aux_fest.columns = ['avg_time', 'std_time']
            aux_fest = aux_fest.reset_index()
            val = np.round(aux_fest.iloc[0,1])
            col3.metric('Tempo Médio', val)

        with col4:
            st.markdown('##### Desvio c/Festival')
            aux_fest = df2.loc[df2['festival'] == 'Yes ', ['time_taken(min)', 'festival']].groupby('festival').agg({'time_taken(min)' : ['mean', 'std']})
            aux_fest.columns = ['avg_time', 'std_time']
            aux_fest = aux_fest.reset_index()
            val = np.round(aux_fest.iloc[0,2])
            col4.metric('Tempo Médio', val)
        with col5:
            st.markdown('##### Tempo médio s/Festival')
            aux_fest = df2.loc[df2['festival'] == 'No ', ['time_taken(min)', 'festival']].groupby('festival').agg({'time_taken(min)' : ['mean', 'std']})
            aux_fest.columns = ['avg_time', 'std_time']
            aux_fest = aux_fest.reset_index()
            val = np.round(aux_fest.iloc[0,1])
            col5.metric('Tempo Médio', val)
        with col6: 
            st.markdown('##### Desvio s/Festival')
            aux_fest = df2.loc[df2['festival'] == 'No ', ['time_taken(min)', 'festival']].groupby('festival').agg({'time_taken(min)' : ['mean', 'std']})
            aux_fest.columns = ['avg_time', 'std_time']
            aux_fest = aux_fest.reset_index()
            val = np.round(aux_fest.iloc[0,2])
            col6.metric('Tempo Médio', val)
    with st.container():
        st.markdown("""___""")
        st.markdown('## Distribuição do Tempo por cidade')
        fig = time_pcity(df2)
        st.plotly_chart(fig)

    with st.container():
        st.markdown("""___""")
        st.markdown('## Distribuição do Tempo')
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('## Tempo Médio de entrega por cidade')
            aux = df2[['time_taken(min)', 'city']].groupby('city').agg({'time_taken(min)' :  ['mean', 'std']}).reset_index()
            aux.columns = ['city', 'time_mean', 'time_std']

            st.dataframe(aux)
        with col2:
            st.markdown('## Tempo Médio por entrega')
            fig2 = time_pent(df2)
            st.plotly_chart(fig2)

    with st.container():
        st.markdown("""___""")
        st.markdown('## Distribuição do Tempo por Cidade e Pedido')
        aux2 = df2[['type_of_order', 'time_taken(min)', 'city']].groupby(['city', 'type_of_order']).agg({'time_taken(min)' :  ['mean', 'std']}).reset_index()
        aux2.columns = ['city', 'type_of_order', 'time_mean', 'time_std']

        st.dataframe(aux2)