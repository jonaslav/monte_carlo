import matplotlib.ticker as ticker
import pandas as pd
import locale
import sys

import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QGraphicsView, QWidget, QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from pandas import DataFrame

locale.setlocale(locale.LC_ALL, 'no_NO')


class MonteCarlo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1000, 700)
        self.setMinimumSize(1000, 700)

        layout = QVBoxLayout()
        self.setLayout(layout)

        plt.style.use('_mpl-gallery')
        self.setWindowTitle('Monte Carlo simulering')

        self.canvas = FigureCanvas(plt.figure(figsize=(10, 7), dpi=100))

        layout.addWidget(self.canvas)
        self.init_inputs()

    def init_inputs(self):
        self.stock_return_input = QLineEdit(self)
        self.stock_return_input.move(50, 50)
        self.stock_return_input.setPlaceholderText("Enter stock return")

        self.stock_volatility_input = QLineEdit(self)
        self.stock_volatility_input.move(50, 100)
        self.stock_volatility_input.setPlaceholderText("Enter stock volatility")

        self.weight_stock_input = QLineEdit(self)
        self.weight_stock_input.move(50, 150)
        self.weight_stock_input.setPlaceholderText("Enter stock weight")

        self.bond_return_input = QLineEdit(self)
        self.bond_return_input.move(50, 200)
        self.bond_return_input.setPlaceholderText("Enter bond return")

        self.bond_volatility_input = QLineEdit(self)
        self.bond_volatility_input.move(50, 250)
        self.bond_volatility_input.setPlaceholderText("Enter bond volatility")

        self.weight_bond_input = QLineEdit(self)
        self.weight_bond_input.move(50, 300)
        self.weight_bond_input.setPlaceholderText("Enter bond weight")

        self.correlation_input = QLineEdit(self)
        self.correlation_input.move(50, 350)
        self.correlation_input.setPlaceholderText("Enter correlation")

        self.percentage_cost_input = QLineEdit(self)
        self.percentage_cost_input.move(50, 400)
        self.percentage_cost_input.setPlaceholderText("Enter percentage cost")

        self.time_horizon_input = QLineEdit(self)
        self.time_horizon_input.move(50, 450)
        self.time_horizon_input.setPlaceholderText("Enter time horizon")

        self.initial_value_input = QLineEdit(self)
        self.initial_value_input.move(50, 500)
        self.initial_value_input.setPlaceholderText("Enter initial value")

        self.yearly_deposit_input = QLineEdit(self)
        self.yearly_deposit_input.move(50, 550)
        self.yearly_deposit_input.setPlaceholderText("Enter yearly deposit")

        self.iterations_input = QLineEdit(self)
        self.iterations_input.move(50, 600)
        self.iterations_input.setPlaceholderText("Enter iterations")

        self.button = QPushButton('Simulate', self)
        self.button.move(150, 50)
        # self.button.clicked.connect(self.simulate)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    mc = MonteCarlo()
    mc.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
