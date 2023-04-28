import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon="🍴"
    )


image = Image.open('reports/images/logo.png')
st.sidebar.image( image, width=120)

st.sidebar.markdown( '# Made in Asia Marketplace' )
st.sidebar.markdown( '## Greatest Marketplace in India' )
st.sidebar.markdown( """___""")

st.write( '# Made in Asia Marketplace Growth Dashboard' )

st.markdown(
    """
       Growth Dashboard foi construido para acompanhar as métricas de crescimento da empresa.
       ### Como utilizar esse Growth de comportamento?
         - Visão geral:
             - Métricas gerais dos restaurantes.
             - Insights de geolocalização.
         - Visão Empresa:
             - Visualização de dados e análise de gráficos interativos sobre a variação dos pedidos a partir de métricas selecionadas.
         - Visão Entregadores:
             - Visualização de dados e análise de datasets interativos sobre avaliações e características gerais dos entregadores a partir de métricas selecionadas.
         - Visão Restaurantes:
             - Acompanhamento de métricas como distância e tempo durante a entrega a partir de métricas selecionadas. 
        ### Ask for Help
        - Time de Data Science do Discord
            - @luis_hmq
    """
)