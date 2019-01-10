import json
import sys
import argparse
from pprint import pprint
from urllib.parse import urlencode
from datetime import datetime
import requests
from PyQt5.QtWidgets import *
from forecast_3d.map_widget import MapWidget
from forecast_2d.plots_widget import PlotsWidget
from window import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, api_key, cities, bounds, forecast_file_path, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.api_key = api_key
        self.bounds = bounds
        self.forecast_data = self.download_data(cities, forecast_file_path)
        self.initialize_combo_boxes(cities, self.forecast_data)
        self.map_widget = MapWidget(parent=self.widget_3d, geographic_bounds=self.bounds, cities=cities)
        self.plots_widget = PlotsWidget(parent=self.widget_2d)
        self.render_data_on_map(self.date_combo_box.currentData())
        self.draw_plots(self.city_combo_box.currentData())
        self.precipitation_checkbox.stateChanged.connect(lambda checked: self.map_widget.toggle_data(checked, 'precipitation'))
        self.clouds_checkbox.stateChanged.connect(lambda checked: self.map_widget.toggle_data(checked, 'clouds'))
        self.wind_checkbox.stateChanged.connect(lambda checked: self.map_widget.toggle_data(checked, 'wind'))
        self.temperature_checkbox.stateChanged.connect(lambda checked: self.map_widget.toggle_data(checked, 'temperature'))
        self.pressure_checkbox.stateChanged.connect(lambda checked: self.map_widget.toggle_data(checked, 'pressure'))
        self.reset_camera_button.clicked.connect(self.map_widget.reset_camera)

    def resizeEvent(self, event):
        self.map_widget.update_size()
        self.plots_widget.update_size()

    def download_data(self, cities, forecast_file_path):
        forecast_for_city = {}
        if forecast_file_path is not None:
            print("Loading forecast from: " + forecast_file_path)
            with open(forecast_file_path, encoding='utf-8') as forecast_file:
                json_forecasts = json.load(forecast_file)
                for key, forecast in json_forecasts.items():
                    forecast_for_city[int(key)] = forecast
        else:
            for city in cities:
                parameters = {"id": city['id'], "appid": self.api_key}

                url = 'http://api.openweathermap.org/data/2.5/forecast?%s&units=metric' % urlencode(parameters)
                response = requests.get(url)
                forecast = json.loads(response.text)

                if int(forecast['cod']) != 200:
                    if int(forecast['cod']) == 401 or int(forecast['cod']) == 403:
                        self.display_api_key_dialog()
                    else:
                        self.display_fail_dialog()
                    raise Exception(forecast['message'])

                forecast_for_city[city['id']] = forecast

        return forecast_for_city

    def display_api_key_dialog(self):
        title = 'Invalid API key'
        message = "The API key provided in the config file is invalid.\n\n" \
                  "Valid keys can be obtained from openweathermap.org"
        QMessageBox.critical(self, title, message, QMessageBox.Close)

    def display_fail_dialog(self):
        title = "Download error"
        message = "Weather server is not responding at the moment, try again later.\n\n"\
                  "Seriously, it will work eventually.\n\n"\
                  "You can also try loading data from json file."
        QMessageBox.critical(self, title, message, QMessageBox.Close)

    def initialize_combo_boxes(self, cities, forecast_data):
        for city in cities:
            self.city_combo_box.addItem(city['name'], city)

        self.city_combo_box.currentIndexChanged.connect(self.select_city)

        for city_id, forecast in forecast_data.items():
            for forecast_item in forecast['list']:
                self.date_combo_box.addItem(datetime.fromtimestamp(forecast_item['dt']).strftime('%Y-%m-%d %H:%M'), forecast_item['dt'])
            # only one forecast needed to setup available times
            break

        self.date_combo_box.currentIndexChanged.connect(self.select_date)

    def render_data_on_map(self, timestamp):
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

    def draw_plots(self, chosen_city):
        self.plots_widget.draw_plots(self.forecast_data[chosen_city['id']]['list'])

    def select_city(self, index):
        self.draw_plots(self.city_combo_box.itemData(index))

    def select_date(self, index):
        self.render_data_on_map(self.date_combo_box.itemData(index))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file", type=str,
                        help="Path to config file containing api key, cities and geographic bounds of Poland")
    parser.add_argument("-f", "--forecast_file", type=str,
                        help="Path to json file containing forecast (this will be read instead of http request)")
    args = parser.parse_args()

    with open(args.config_file, encoding='utf-8') as config_file:
        json_config = json.load(config_file)
    api_key = json_config['api_key']
    cities = json_config['cities']
    bounds = json_config['bounds']

    app = QApplication([])
    main_window = MainWindow(api_key, cities, bounds, args.forecast_file)
    main_window.show()
    app.exec_()


if __name__ == '__main__':
    main()
