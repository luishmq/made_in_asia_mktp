import pandas         as pd
import numpy          as np
import seaborn        as sns
import plotly.express as px
import re
import inflection
import folium
import streamlit as st

from haversine import haversine
from IPython.core.display import HTML
from matplotlib           import pyplot as plt

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
linhas_vazias = df1['delivery_person_age'] != 'NaN '
df1 = df1.loc[linhas_vazias, :]

# Conversao de texto/categoria/string para numeros inteiros
df1['delivery_person_age'] = df1['delivery_person_age'].astype( int )

# Conversao de texto/categoria/strings para numeros decimais
df1['delivery_person_ratings'] = df1['delivery_person_ratings'].astype( float )

# Conversao de texto para data
df1['order_date'] = pd.to_datetime( df1['order_date'], format='%d-%m-%Y' )
#
linhas_vazias = df1['multiple_deliveries'] != 'NaN '
df1 = df1.loc[linhas_vazias, :]
df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )

df1['time_taken(min)'] = df1['time_taken(min)'].apply(lambda x: x.split('(min) ')[1])
df1['time_taken(min)'] = df1['time_taken(min)'].astype(int)

df2 = df1.copy()

aux1 = df2[['id', 'order_date']].groupby( 'order_date' ).count().reset_index()
aux1.columns = ['order_date', 'qtd_entregas']
line_graph = sns.lineplot(x='order_date', y='qtd_entregas', data=aux1);
line_graph.set_title("Variação da quantidade de pedidos por dia")

# STREAMLIT

st.header('This is a header')

st.sidebar.markdown("# Cury Company")
st.sidebar.markdown('## Filtro')
st.sidebar.markdown("""---""")
st.sidebar.markdown('## Selecione uma data limite')

data_slider = st.sidebar.slider('Valores', value=pd.datetime(2022, 4, 13),min_value=pd.datetime(2022, 2, 11),max_value=pd.datetime(2022, 4, 6), format='DD-MM-YYYY')

st.header(data_slider)

st.markdown('# Visualização diária dos pedidos')
with st.container():
    st.markdown('### Quantidade de pedidos por dia')
    

print("Oi")