# This is a sample Python script.
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QGraphicsView, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

class MonteCarloApp(QMainWindow):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        run_button = QPushButton("Run sim")
        run_button.clicked.connect(self.run_simulation)
        layout.addWidget(run_button)

        self.graph_widget = QGraphicsView()
        layout.addWidget(self.graph_widget)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        def run_simulation(self):
            from portfolio_fun import MonteCarloPortFolio as Portfolio
            portfolio = Portfolio()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MonteCarloApp()
    window.show()
    sys.exit(app.exec_())
