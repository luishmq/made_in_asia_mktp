import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon="🍴"
    )


image = Image.open('reports/images/logo.png')
st.sidebar.image( image, width=120)

st.sidebar.markdown( '# Made in Asia Restaurant' )
st.sidebar.markdown( '## Fastest Restaurant in India' )
st.sidebar.markdown( """___""")

st.write( '# Made in Asia Restaurant Growth Dashboard' )

st.markdown(
    """
       Growth Dashboard foi construido para acompanhar as métricas de crescimento da empresa.
       ### Como utilizar esse Growth de comportamento?
         - Visão geral:
             - Métricas gerais dos restaurantes.
             - Insights de geolocalização.
         - Visão Cidades:
             - Acompanhamento dos indicadores de crescimento dos restaurantes e média de avaliação.
         - Visão Países:
             - Acompanhamento dos indicadores de crescimento dos restaurantes e média de avaliação.
         - Visão Restaurantes:
             - Ranking de avaliações dos melhores restaurantes e tipos culinários.  
        ### Ask for Help
        - Time de Data Science do Discord
            - @luis_hmq
    """
)