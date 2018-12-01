from PyQt5.QtWidgets import QApplication
import sys

from source.interface import GOTLInterface


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GOTLInterface()
    sys.exit(app.exec_())
