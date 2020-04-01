import PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtChart import QChart, QChartView, QValueAxis

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        chartView = QChartView(chart)
        self.setCentralWidget(chartView)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())