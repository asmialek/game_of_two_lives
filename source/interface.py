import sys
import os

from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QGridLayout, QApplication,
                             QFileDialog, QPushButton,
                             QSlider, QMessageBox,
                             )
from PyQt5.QtCore import Qt

from source.gameplay import GameOfLife


class GOTLInterface(QWidget):

    def __init__(self):
        super().__init__()

        self.first = QLabel('Red')
        self.second = QLabel('Blue')
        self.turns = QLabel('Turns')
        self.speed = QLabel('Speed')

        self.firstEdit = QLineEdit()
        self.secondEdit = QLineEdit()
        self.turnsEdit = QLineEdit()
        self.turnsEdit.setAlignment(Qt.AlignHCenter)

        self.firstEdit.setText(os.path.abspath('./seeds/first.txt'))
        self.secondEdit.setText(os.path.abspath('./seeds/second.txt'))
        self.turnsEdit.setText('32')

        self.load_first = QPushButton('Load')
        self.load_first.clicked.connect(lambda:
                                        self.load_file(self.firstEdit))

        self.load_second = QPushButton('Load')
        self.load_second.clicked.connect(lambda:
                                         self.load_file(self.secondEdit))

        self.play = QPushButton('Play')
        self.play.clicked.connect(lambda:
                                  self.play_game())

        self.rules = QPushButton('Rules')
        self.rules.clicked.connect(lambda:
                                  self.show_rules())

        self.speedSlider = QSlider(Qt.Horizontal)
        self.speedSlider.setMinimum(1)
        self.speedSlider.setMaximum(9)
        self.speedSlider.setValue(5)
        self.speedSlider.setTickPosition(QSlider.TicksBelow)
        self.speedSlider.setTickInterval(1)

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.grid.addWidget(self.first, 0, 0)
        self.grid.addWidget(self.firstEdit, 0, 1, 1, 4)
        self.grid.addWidget(self.load_first, 0, 5)

        self.grid.addWidget(self.second, 1, 0)
        self.grid.addWidget(self.secondEdit, 1, 1, 1, 4)
        self.grid.addWidget(self.load_second, 1, 5)

        self.grid.addWidget(self.speed, 2, 0)
        self.grid.addWidget(self.speedSlider, 2, 1)
        self.grid.addWidget(self.turns, 2, 3)
        self.grid.addWidget(self.turnsEdit, 2, 4, 1, 2)

        self.grid.addWidget(self.play, 3, 0, 1, 5)
        self.grid.addWidget(self.rules, 3, 5)

        self.grid.setColumnStretch(1, 3)
        self.grid.setColumnStretch(2, 0.5)
        self.grid.setColumnStretch(4, 0.1)

        self.setLayout(self.grid)

        self.setGeometry(300, 300, 550, 100)
        self.setWindowTitle('Game of Life and Death')
        self.show()

    def load_file(self, textbox):
        filename = QFileDialog.getOpenFileName()
        textbox.setText(filename[0])

    def play_game(self):
        first_file = self.firstEdit.text()
        second_file = self.secondEdit.text()
        turns = int(self.turnsEdit.text())
        game = GameOfLife(turns,
                          first_seed=first_file,
                          second_seed=second_file,
                          show_plot=True,
                          speed=self.speedSlider.value())
        game.play()

    def show_rules(self):
        os.system("start README.md")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GOTLInterface()
    sys.exit(app.exec_())
