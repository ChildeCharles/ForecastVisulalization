from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
from window import Ui_MainWindow
import sys
import json
from pprint import pprint
import datetime
import requests
from urllib.parse import urlencode
from map_widget import MapWidget


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, api_key, cities, bounds, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.api_key = api_key
        self.bounds = bounds
        self.weather_data, self.forecast_data = self.download_data(cities)
        self.initialize_combo_boxes(cities, self.forecast_data)
        self.map_widget = MapWidget(parent=self.widget_3d, geographic_bounds=self.bounds, cities=cities)
        self.render_data_on_map()
        self.precipitation_checkbox.stateChanged.connect(self.map_widget.toggle_precipitation)
        self.clouds_checkbox.stateChanged.connect(self.map_widget.toggle_clouds)
        self.wind_checkbox.stateChanged.connect(self.map_widget.toggle_wind)
        self.temperature_checkbox.stateChanged.connect(self.map_widget.toggle_temperature)
        self.pressure_checkbox.stateChanged.connect(self.map_widget.toggle_pressure)

    def download_data(self, cities):
        weather_for_city = {}
        forecast_for_city = {}
        for city in cities:
            parameters = {"id": city['id'], "appid": self.api_key}

            url = 'http://api.openweathermap.org/data/2.5/weather?%s&units=metric' % urlencode(parameters)
            response = requests.get(url)
            weather = json.loads(response.text)

            if int(weather['cod']) != 200:
                raise Exception(weather['message'])

            weather_for_city[city['id']] = weather

            url = 'http://api.openweathermap.org/data/2.5/forecast?%s&units=metric' % urlencode(parameters)
            response = requests.get(url)
            forecast = json.loads(response.text)

            if int(forecast['cod']) != 200:
                raise Exception(forecast['message'])

            forecast_for_city[city['id']] = forecast

        return weather_for_city, forecast_for_city

    def initialize_combo_boxes(self, cities, forecast_data):
        for city in cities:
            self.city_combo_box.addItem(city['name'], city)

        self.city_combo_box.currentIndexChanged.connect(self.print_selected_city)

        for city_id, forecast in forecast_data.items():
            for forecast_item in forecast['list']:
                self.date_combo_box.addItem(forecast_item['dt_txt'], forecast_item['dt'])
            # only one forecast needed to setup available times
            break

        self.date_combo_box.currentIndexChanged.connect(self.select_date)

    def render_data_on_map(self):
        timestamp = self.date_combo_box.currentData()
        forecasts_for_cities = {}
        for city_id, forecast in self.forecast_data.items():
            for forecast_item in forecast['list']:
                if forecast_item['dt'] == timestamp:
                    forecasts_for_cities[city_id] = forecast_item
                    break

        visibilities = {
            'precipitation': self.precipitation_checkbox.isChecked(),
            'wind': self.wind_checkbox.isChecked(),
            'temperature': self.temperature_checkbox.isChecked(),
            'pressure': self.pressure_checkbox.isChecked(),
            'clouds': self.clouds_checkbox.isChecked()
        }

        self.map_widget.render_data(forecasts_for_cities, visibilities)

    def print_selected_city(self, index):
        pprint(self.city_combo_box.itemData(index))

    def select_date(self, index):
        self.render_data_on_map()


def main():
    app = QApplication([])

    if len(sys.argv) < 2:
        raise Exception("You must provide a config file")

    with open(sys.argv[1], encoding='utf-8') as config_file:
        json_config = json.load(config_file)
    api_key = json_config['api_key']
    cities = json_config['cities']
    bounds = json_config['bounds']

    main_window = MainWindow(api_key, cities, bounds)
    main_window.show()
    app.exec_()


if __name__ == '__main__':
    main()
