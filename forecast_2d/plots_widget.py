from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import date2num
from datetime import datetime, time
from forecast_2d.data_components import temperature, pressure, humidity, clouds, wind, precipitation


class PlotsWidget(FigureCanvas):
    def __init__(self, parent=None, dpi=100):
        self.dpi = dpi
        self.parent = parent
        self.fig = Figure(figsize=(parent.size().width() / dpi, parent.size().height() / dpi), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.temperature_plot = self.figure.add_subplot(6, 1, 1)
        self.temperature_plot.set_title('Temperature [ºC]')
        plt.setp(self.temperature_plot.get_xticklabels(), visible=False)

        self.pressure_plot = self.figure.add_subplot(6, 1, 2, sharex=self.temperature_plot)
        self.pressure_plot.set_title('Pressure [hPa]')
        plt.setp(self.pressure_plot.get_xticklabels(), visible=False)

        self.humidity_plot = self.figure.add_subplot(6, 1, 3, sharex=self.temperature_plot)
        self.humidity_plot.set_title('Humidity [%]')
        plt.setp(self.humidity_plot.get_xticklabels(), visible=False)

        self.clouds_plot = self.figure.add_subplot(6, 1, 4, sharex=self.temperature_plot)
        self.clouds_plot.set_title('Clouds [%]')
        plt.setp(self.clouds_plot.get_xticklabels(), visible=False)

        self.wind_plot = self.figure.add_subplot(6, 1, 5, sharex=self.temperature_plot)
        self.wind_plot.set_title('Wind [km/h]')
        plt.setp(self.wind_plot.get_xticklabels(), visible=False)

        self.precipitation_plot = self.figure.add_subplot(6, 1, 6, sharex=self.temperature_plot)
        self.precipitation_plot.set_title('Precipitation [mm]')

        self.plots = [self.temperature_plot, self.pressure_plot, self.humidity_plot, self.clouds_plot, self.wind_plot, self.precipitation_plot]
        for plot in self.plots:
            plot.grid(which='major', axis='x')

        self.fig.tight_layout()

        self.plot_lines = []

    def update_size(self):
        self.fig.set_size_inches(self.parent.size().width() / self.dpi, self.parent.size().height() / self.dpi, forward=True)
        self.resize(self.parent.size())
        self.fig.tight_layout()
        self.draw()

    def draw_plots(self, forecast):
        for plot in self.plots:
            while len(plot.lines) > 0:
                plot.lines.pop()

        dates = self.get_list_of_dates(forecast)
        self.plot_lines.append(self.temperature_plot.plot(dates, temperature.get_y_values(forecast), color='tab:green', linewidth=2))
        self.plot_lines.append(self.pressure_plot.plot(dates, pressure.get_y_values(forecast), color='tab:purple', linewidth=2))
        self.plot_lines.append(self.humidity_plot.plot(dates, humidity.get_y_values(forecast), color='tab:gray', linewidth=2))
        self.plot_lines.append(self.clouds_plot.plot(dates, clouds.get_y_values(forecast), color='tab:blue', linewidth=2))
        self.plot_lines.append(self.wind_plot.plot(dates, wind.get_y_values(forecast), color='tab:orange', linewidth=2))
        rain, snow, total = precipitation.get_y_values(forecast)
        self.plot_lines.append(self.precipitation_plot.plot(dates, rain, color='tab:blue', linewidth=1.5))
        self.plot_lines.append(self.precipitation_plot.plot(dates, snow, color='tab:cyan', linewidth=1.5))
        self.plot_lines.append(self.precipitation_plot.plot(dates, total, color='k', linewidth=1.5))
        self.precipitation_plot.legend(['Rain', 'Snow', 'Total'])

        date_formatter = mdates.DateFormatter('%Y-%m-%d %H:%M')
        self.precipitation_plot.xaxis.set_major_formatter(date_formatter)

        # new day breaks on 00:00 UTC so on 01:00 CET
        days = [date for date in dates if date.time() == time(1, 0)]

        self.precipitation_plot.set_xticks(ticks=days)
        self.precipitation_plot.set_xticks(ticks=dates, minor=True)
        plt.setp(self.precipitation_plot.xaxis.get_majorticklabels(), rotation=30, ha="right", rotation_mode="anchor")
        self.fig.tight_layout()
        self.draw()

    @staticmethod
    def get_list_of_dates(forecast):
        dates = []
        for forecast_item in forecast:
            dates.append(datetime.fromtimestamp(forecast_item['dt']))
        return dates
