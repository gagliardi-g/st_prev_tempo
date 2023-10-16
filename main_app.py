import streamlit as st
import requests
import pandas as pd

API_KEY = ''

#Carga das cidades do brasil para o campo de select box
df_cidades = pd.read_csv('cidades_brasil.csv')

#Título do aplicativo
st.title('☁️ Aplicativo de Previsão do Tempo')

#Criação do select box
cidade = st.selectbox(
    "Qual cidade que você quer saber o clima?",
    df_cidades,
    index=None,
)

# Botão para buscar a previsão do tempo
if st.button('Obter Previsão do Tempo'):
    #Tratamento no csv para a leitura da API
    cidade = cidade.split(',')
    
    #Chamada da API dos dados de temperatura atual
    url = f'https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={cidade[0]},{cidade[1]}'
    response = requests.get(url)
    data = response.json()

    #Chamada da API dos dados de forecast
    url_fore = f'https://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={cidade}'
    response_fore = requests.get(url_fore)
    data_fore = response_fore.json()

    # Lógica para a exibição dos resultados
    if response.status_code==200:

        #Declarando as variáveis de clima
        temp = data['current']['temp_c'] 
        humidity = data['current']['humidity']
        wind_kph = data['current']['wind_kph']

        st.subheader(f"**Local:** {data['location']['name']}, {data['location']['region']}, {data['location']['country']}")
        st.write('Dados atuais da cidade:')

        #Exibindo os charts de forma horizontal
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(label="Temperature", value=str(temp)+' °C')
        with col2:
            st.metric(label="Humidade", value=str(humidity)+' %')
        with col3:
            st.metric(label="Vento", value=str(humidity)+' km/h')
        
        #Exibindo o gráfico do forecast
        st.write('Gráfico de forecast da cidade:')

        df_fore = pd.DataFrame(data_fore['forecast']['forecastday'][0]['hour'], columns=['time', 'temp_c'])
        df_fore['time'] = pd.to_datetime(df_fore['time'])
        df_fore['time'] = df_fore['time'].dt.hour
        st.line_chart(df_fore, x='time', y='temp_c')

        #Exibindo a tabela do forecast
        st.write('Tabela de forecast da cidade:')
        st.table(df_fore)

    elif response.status_code==400:
        st.write("Cidade não encontrada :(")
    elif response.status_code==500:
        st.write("Servidor fora do ar :(")
