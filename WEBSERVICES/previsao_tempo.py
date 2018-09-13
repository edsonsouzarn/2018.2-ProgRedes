import datetime
import json
import urllib.request

#
# Retirado de https://codereview.stackexchange.com/questions/131371/script-to-print-weather-report-from-openweathermap-api
#

# -------------------------------------------------------------------------------------------------------
# Convertendo uma estrutura (tupla) que representa uma data/hora em uma string no formato especificado
def time_converter(time):
    converted_time = datetime.datetime.fromtimestamp(
        int(time)
    ).strftime('%I:%M %p')
    return converted_time


# -------------------------------------------------------------------------------------------------------
# Monta a URL completa do Webservice
def url_builder(city_id):
    # Obtain yours form: http://openweathermap.org/
    user_api = 'INSIRA_AQUI_SUA_CHAVE'
    # For Fahrenheit use imperial, for Celsius use metric, and the default is Kelvin.
    unit = 'metric'
    api = 'http://api.openweathermap.org/data/2.5/weather?id='
    full_api_url = api + str(city_id) + '&mode=json&units=' + unit + '&APPID=' + user_api
    return full_api_url


# -------------------------------------------------------------------------------------------------------
# Efetua uma busca de dados e retorna os dados na forma bruta (RAW)
def data_fetch(full_api_url):
    url = urllib.request.urlopen(full_api_url)
    output = url.read().decode('utf-8')
    raw_api_dict = json.loads(output)
    url.close()
    # Descomente a linha abaixo para mostrar os dados brutos
    #print(raw_api_dict)
    return raw_api_dict


# -------------------------------------------------------------------------------------------------------
# Pega os dados brutos (RAW) e monta um dicionario com os dados selecionados
def data_organizer(raw_api_dict):
    data = dict(
        city=raw_api_dict.get('name'),
        country=raw_api_dict.get('sys').get('country'),
        temp=raw_api_dict.get('main').get('temp'),
        temp_max=raw_api_dict.get('main').get('temp_max'),
        temp_min=raw_api_dict.get('main').get('temp_min'),
        humidity=raw_api_dict.get('main').get('humidity'),
        pressure=raw_api_dict.get('main').get('pressure'),
        sky=raw_api_dict['weather'][0]['main'],
        sunrise=time_converter(raw_api_dict.get('sys').get('sunrise')),
        sunset=time_converter(raw_api_dict.get('sys').get('sunset')),
        wind=raw_api_dict.get('wind').get('speed'),
        wind_deg=raw_api_dict.get('wind').get('deg'),
        dt=time_converter(raw_api_dict.get('dt')),
        cloudiness=raw_api_dict.get('clouds').get('all')
    )
    # Descomente a linha abaixo para mostrar os dados tratados
    #print(data)
    return data


# -------------------------------------------------------------------------------------------------------
# Monta um layout de exibicao dos dados
def data_output(data):
    m_symbol = '\xb0' + 'C'
    print(' ')
    print('---------------------------------------')
    print('Clima atual em: {0}, {1}: {2}{3} {4}'.format(data['city'], data['country'], data['temp'], m_symbol, data['sky']))
    #print('Max: {}, Min: {}'.format(data['temp_max'], data['temp_min']))
    print(' ')
    print('Velocidade do vento: {0}, Direção: {1}'.format(data['wind'], data['wind_deg']))
    print('Umidade Relativa do Ar: {0}%'.format(data['humidity']))
    print('Cobertura de Nuvens: {0}%'.format(data['cloudiness']))
    print('Pressão: {0}hPa'.format(data['pressure']))
    print('Nascer do sol: {0}'.format(data['sunrise']))
    print('Por do Sol: {0}'.format(data['sunset']))
    print(' ')
    print('Última Atualização: {0}'.format(data['dt']))
    print('---------------------------------------')
    print(' ')


# -------------------------------------------------------------------------------------------------------
# Bloco principal do programa
if __name__ == '__main__':
    try:
        # Search for your city ID here: http://bulk.openweathermap.org/sample/city.list.json.gz
        id_city = 3394023
        data_output(data_organizer(data_fetch(url_builder(id_city))))
    except IOError:
        print('no internet')
