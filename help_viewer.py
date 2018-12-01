import sys
from PyQt5.QtWidgets import QApplication, QWebView
from PyQt5.QtCore import QUrl
# from PyQt5.QtWebKit import QWebView


class Browser(QWebView):

    def __init__(self):
        QWebView.__init__(self)
        self.loadFinished.connect(self._result_available)

    def _result_available(self, ok):
        frame = self.page().mainFrame()
        # print(unicode(frame.toHtml()).encode('utf-8'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = Browser()
    view.load(QUrl('http://www.google.com'))
    app.exec_()