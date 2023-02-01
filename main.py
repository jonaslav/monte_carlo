# This is a sample Python script.
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


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
class Canvas(FigureCanvas):
    def __init__(self, parent):
        fig, self.ax = plt.subplots(figsize=(10, 7), dpi=100)
        ## Inputs
        super().__init__(fig)
        self.setParent(parent)
        plt.style.use('_mpl-gallery')

    def initui(self):
        self.setWindowTitle('Monte Carlo simulering')

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

        self.calculate_button = QPushButton('Calculate', self)
        self.calculate_button.move(150, 150)
        self.calculate_button.clicked.connect(self.run_monte_carlo)

    def run_monte_carlo(self):

        stock_return = float(self.stock_return_input.text())

        stock_volatility = float(self.stock_volatility_input.text())
        weight_stock = float(self.weight_stock_input.text())

        bond_return = float(self.bond_return_input.text())
        bond_volatility = float(self.bond_volatility_input.text())
        weight_bond = float(self.weight_bond_input.text())

        correlation = float(self.correlation_input.text())

        percentage_cost = float(self.percentage_cost_input.text())  # Årlig forvaltningskostnad
        time_horizon = int(self.time_horizon_input.text())  # Tidsramme

        initial_value = float(self.initial_value_input.text())  # Startverdi
        yearly_deposit = float(self.yearly_deposit_input.text())  # Årlig innskudd

        iterations = int(self.iterations_input.text())  # Antall simuleringer

        ############################################################################################################
        # Key values
        covariance = stock_volatility * bond_volatility
        portfolio_var = (weight_stock ** 2 * stock_volatility ** 2) + (weight_bond ** 2 * bond_volatility ** 2) + (
                2 * weight_stock * weight_bond * covariance)
        portfolio_std = np.sqrt(portfolio_var)
        portfolio_expected_return = weight_stock * stock_return + weight_bond * bond_return

        # Simulation
        sim = DataFrame()
        sim2 = DataFrame()
        sim3 = DataFrame()

        streams = []
        streams2 = []

        for x in range(iterations):
            expected_return = portfolio_expected_return
            volatility = portfolio_std
            time_horizon1 = time_horizon
            pv = initial_value
            pv2 = initial_value
            annual_investment = yearly_deposit
            stream = []
            stream2 = []
            stream3 = []
            for i in range(time_horizon):
                end = round(pv * (1 + np.random.normal(expected_return, volatility)) + annual_investment, 2)
                acost = round(
                    pv * (1 + np.random.normal(expected_return - percentage_cost, volatility)) + annual_investment, 2)
                stream.append(end)
                stream2.append(acost)

                pv = end
                pv2 = acost

            streams.append(stream)
            streams2.append(stream2)

        sim = pd.concat([pd.Series(s) for s in streams], axis=1)
        sim_netto = pd.concat([pd.Series(s) for s in streams2], axis=1)

        # Create a new dataframe with the initial value as the first row in every column
        new_df = pd.DataFrame(initial_value, columns=sim.columns, index=[0])

        # Concatenate the new dataframe with the existing dataframe
        sim = pd.concat([new_df, sim])
        sim_netto = pd.concat([new_df, sim_netto])

        sim.reset_index(inplace=True, drop=True)
        sim_netto.reset_index(inplace=True, drop=True)
        cost = sim * percentage_cost

        def var(returns, alpha):
            return np.percentile(returns, alpha)

        def cvar(returns, alpha):
            returns = np.array(returns)
            belowVaR = returns <= var(returns, alpha=alpha)
            return returns[belowVaR].mean()

        def varsimiloc():
            var_95 = []
            var_5 = []
            for i in range(time_horizon + 1):
                var_95.append(var(sim.iloc[i], 5))
                var_5.append(var(sim.iloc[i], 95))

            # Calculate the mean of each row in the sim DataFrame
            means = sim.mean(axis=1)

            plt.plot(var_5, label='Sterk', color='green')
            plt.plot(var_95, label='Svak', color='orange')
            plt.plot(means, label='Forventet', color='blue')
            plt.fill_between(range(time_horizon + 1), var_95, var_5, color='#d3d3d3')

            plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.2f} NOK'))
            # Use the ',' as the decimal separator and '.' as the thousand separator
            plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(x, ',.0f').replace(',', '.')))

            plt.xlabel('År')
            plt.ylabel('Porteføljens verdi')
            plt.legend(loc='best')
            plt.show()

        varsimiloc()


class ShowGraph(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1000, 700)
        chart = Canvas(self)
        chart.initui()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = ShowGraph()
    demo.show()
    sys.exit(app.exec_())
