# Made in Asia Marketplace 🍴
## Visualização e análise de dados da empresa Made in Asia na plataforma do Streamlit 
![](reports/images/india_rest.jpeg)

# 1.0 Problema de Negócio 

A Made in Asia é uma empresa de tecnologia que criou um aplicativo que conecta restaurantes, entregadores e pessoas. Através desse aplicativo, é possível realizar o pedido de uma refeição, em qualquer restaurante cadastrado, e recebê-lo no conforto da sua casa por um entregador também cadastrado no aplicativo da Made in Asia.

A empresa realiza negócios entre restaurantes, entregadores e pessoas, e gera muitos dados sobre entregas, tipos de pedidos, condições climáticas, avaliação dos entregadores e etc. Apesar da entrega estar crescento, em termos de entregas, o CEO não tem visibilidade completa dos KPIs de crescimento da empresa.

Dessa forma, é fundamental que alguém seja responsável por criar soluções de dados para entrega, mas antes de treinar algoritmos, a necessidade da empresa é ter um os principais KPIs estratégicos organizados em uma única ferramenta, para que o CEO possa consultar e conseguir tomar decisões simples, porém importantes.

A empresa possui um modelo de negócio chamado Marketplace, que busca fazer o intermédio do negócio entre três clientes principais: Restaurantes, entregadores e pessoas compradoras. Nesse sentido, o CEO gostaria de acompanhar as métricas de crescimento baseando-se em três visões distintas:

Do lado da empresa:
- 1. Quantidade de pedidos por dia.
- 2. Quantidade de pedidos por semana.
- 3. Distribuição dos pedidos por tipo de tráfego.
- 4. Comparação do volume de pedidos por cidade e tipo de tráfego.
- 4. A quantidade de pedidos por entregador por semana.
- 5. A localização central de cada cidade por tipo de tráfego.

Do lado do entregador:
- 1. A menor e maior idade dos entregadores.
- 2. A pior e a melhor condição de veículos.
- 3. A avaliação médida por entregador.
- 4. A avaliação média e o desvio padrão por tipo de tráfego.
- 5. A avaliação média e o desvio padrão por condições climáticas.
- 6. Os 10 entregadores mais rápidos por cidade.
- 7. Os 10 entregadores mais lentos por cidade.

Do lado do restaurantes:
- 1. A quantidade de entregadores únicos.
- 2. A distância média dos resturantes e dos locais de entrega.
- 3. O tempo médio e o desvio padrão de entrega por cidade.
- 4. O tempo médio e o desvio padrão de entrega por cidade e tipo de pedido.
- 5. O tempo médio e o desvio padrão de entrega por cidade e tipo de tráfego.
- 6. O tempo médio de entrega durantes os Festivais.

# 2.0 Premissas de Negócio

- A análise foi realizada a partir de dados entre 11/02/2022 e 06/04/2022
- O modelo adotado pela empresa é o Marketplace
- Um dashboard baseado em três visões diferentes (Empresa, Entregadores e Restaurantes)foi construído para acompanhar as métricas de crescimento da empresa 

## 2.1 Descrição dos dados

| Column            | Description                                                                                                                             |
| :---------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| `ID`       | Identificador único do cliente                                                                                                                                  |
| `Delivery_person_ID`      | Identificador único do Entregador                                                                                                                           |
| `Delivery_person_Age`         | Idade de cada Entregador                                                                                                                    |
| `Delivery_person_Ratings`     | Nota de cada Entregador                                                                                                            |
| `Restaurant_latitude`       | Valor da latitude de cada Restaurante                                                                                                        |
| `Restaurant_longitude`          | Valor da longitude de cada Restaurante                                                                                                                      |
| `Delivery_location_latitude`             | Valor da latitude da localização de cada Entregador                                                                                                                         |
| `Delivery_location_longitude`          | Valor da longitude da localização de cada Entregador                                                                             |
| `Order_Date`         | Data que cada pedido foi realizado                                                                                           |
| `Time_Orderd`   | Horário que cada pedido foi realizado                                                                     |
| `Time_Order_picked`       | Horário em que cada pedido foi entregue 
| `Weatherconditions`  | Condições do clima                                                     |
| `Road_traffic_density` | Tipo de tráfego                                                                                                         |
| `Vehicle_condition`          | Condição de cada veículo em uma escala de 0 a 3
| `Type_of_order`   | Tipo de cada pedido realizado                                                                      |
| `Type_of_vehicle`       | Tipo de cada veículo
| `multiple_deliveries`  | Se houve mais de um pedido ( 1 ) ou não ( 0 )                                                   |
| `Festival` | Se era período de festival ( Yes ) ou não ( No )                                                                                                         |
| `City`          | Tipo de cada cidade 
| `Time_taken(min)`          | Tempo para cada pedido ser entregue


# 3.0 Estratégia da Solução

O painel estratégico foi desenvolvido utilizando as métricas que refletem as 4 principais visões do modelo de negócio da empresa:

- Visão geral
- Visão cidades
- Visão países
- Visão restaurantes

Cada visão é representada pelo conjunto de métricas descrito no Problema de Negócio.

# 4.0 Insights

## 4.2 Top 3 Insights

### Notou-se que houve uma semana no mês de fevereiro em que não houve pedidos, o que sugere algumas hipóteses.
![](reports/images/bar_day.png)

### A variação dos pedidos por tipo de tráfego não sofreu grandes mudanças ao longo do tempo. Nesse sentido, os tipos "Low" e "Jam" predominam as vendas.
![](reports/images/pie_traffic.png)

### As cidades do tipo "Urban" apresentaram o menor tempo médio de entrega
![](reports/images/time_per_city.png)

# 5.0 O produto final do projeto

Com o dashboard criado, o CEO pode agora consultar o painel via Cloud, pela plataforma Streamlit e, portanto, uma maneira mais ágil e fácil para a tomada de decisão.

O painel pode ser acessado através desse link: https://luishmq-made-in-asia-mktp-home.streamlit.app/

# 6.0 Conclusões

O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas que exibam as métricas selecionadas da melhor forma possível para o CEO.

Da visão da Empresa, podemos concluir que o número de pedidos cresceu entre a semana 06 e a semana 13 de 2022.

# 7.0 Lições Aprendidas
- Visualização e análise de dados com bibliotecas como plotly, matplotlib e seaborn
- Cálculo de medidas como latitude e longitude por meio da biblioteca haversine
- Possibilidade de consulta ágil e profissional dos dados via Cloud Streamlit

# 8.0 Próximos Passos
- Responder a novas hipóteses de negócios para entender melhor os dados e as relações de recursos e criar novas visões para verificar novas relações entre os dados
- Criar novos filtros
- Reduzir o número de métricas
- Aplicar técnicas de programação para melhorar o desempenho da solução criada


