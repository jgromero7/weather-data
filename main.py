# import modules
from bs4 import BeautifulSoup

import pandas as pd
import requests

# URL GLOBAL
FORECAST_WEATHER = 'https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168#.Xlh1u3X0nZs'

def main():
    main_page = requests.get(FORECAST_WEATHER)
    if main_page.status_code == 200:
        html = BeautifulSoup(main_page.content, 'html.parser')
        seven_day = html.find('div', {'id': 'seven-day-forecast'})
        forecast_list = seven_day.find('ul', {'id': 'seven-day-forecast-list'})
        
        period_tags = forecast_list.select('div .tombstone-container .period-name')
        periods = [period.get_text() for period in period_tags]

        short_descs_tags = forecast_list.select("div .tombstone-container .short-desc")
        short_descs = [short_desc.get_text() for short_desc in short_descs_tags]

        temp_tags = forecast_list.select("div .temp")
        temps = [temp.get_text() for temp in temp_tags]

        descs_tags = forecast_list.select('div .tombstone-container img')
        descs = [desc.get('title') for desc in descs_tags]

        weather = pd.DataFrame({
            "period": periods,
            "short_desc": short_descs,
            "temp": temps,
            "desc":descs
        })
        temp_nums = weather["temp"].str.extract("(?P<temp_num>\d+)", expand=False)
        weather["temp_num"] = temp_nums.astype("int")

        print(weather)
    else:
        print("Ocurrio un error al consultar :: {}".format(FORECAST_WEATHER))

if __name__ == '__main__':
    main()