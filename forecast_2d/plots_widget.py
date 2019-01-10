from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class PlotsWidget(FigureCanvas):
    def __init__(self, parent=None, dpi=100):
        fig = Figure(figsize=(parent.size().width() / dpi, parent.size().height() / dpi), dpi=dpi)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.temperature_plot = self.figure.add_subplot(6, 1, 1)
        self.pressure_plot = self.figure.add_subplot(6, 1, 2)
        self.humidity_plot = self.figure.add_subplot(6, 1, 3)
        self.clouds_plot = self.figure.add_subplot(6, 1, 4)
        self.wind_plot = self.figure.add_subplot(6, 1, 5)
        self.precipitation_plot = self.figure.add_subplot(6, 1, 6)

        fig.tight_layout()

    def draw_plots(self):
        self.temperature_plot.plot(range(10), range(10), linewidth=2)
        self.pressure_plot.plot(range(15), range(15), linewidth=2)
        self.humidity_plot.plot(range(10), range(10), linewidth=2)
        self.clouds_plot.plot(range(10), range(10), linewidth=2)
        self.wind_plot.plot(range(10), range(10), linewidth=2)
        self.precipitation_plot.plot(range(10), range(10), linewidth=2)
        self.draw()
