import sys
import random
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QListWidget, QPushButton, QInputDialog
from PyQt5.Qt import QGridLayout, QMimeData
from PyQt5.QtCore import pyqtSlot


class StringListDlg(QDialog):
    """docstring for Form"""

    def __init__(self, title="Title", items=[]):
        super(StringListDlg, self).__init__()
        self.initUi(title, items)

    def initUi(self, title, items):
        layout = QGridLayout()
        self.qlist = QListWidget()
        self.stringlist = items

        if len(self.stringlist) == 0:
            self.feedList()

        else:
            self.qlist.addItems(self.stringlist)
            layout.addWidget(self.qlist, 0, 0, 7, 3)

        butttonsList = ['&Add...', '&Edit...',
                        '&Remove...', '&Up', '&Down', '&Sort', '&Close']

        for idx, button in enumerate(butttonsList):
            qPushButton = QPushButton()
            method = str.lower((button.split('.')[0])[1:])
            qPushButton.clicked.connect(getattr(self, method))
            qPushButton.setText(button)
            layout.addWidget(qPushButton, idx, 3)

        self.setLayout(layout)
        self.setWindowTitle('List of %s' % title)
        self.show()

    def feedList(self):
        for x in range(10):
            self.stringlist.append("List item number %.3d" %
                                   (random.randrange(100)))

    @pyqtSlot()
    def add(self):
        print('add')
        text, okPressed = QInputDialog.getText(
            self, "Add Item", "New Item:", QLineEdit.Normal, "")
        if okPressed and text != '':
            self.stringlist.append(text)
            self.qlist.clear()
            self.qlist.addItems(self.stringlist)
            self.qlist.scrollToBottom()

    @pyqtSlot()
    def edit(self):
        print('edit')
        text, okPressed = QInputDialog.getText(
            self, "Add Item", "New Item:", QLineEdit.Normal, self.qlist.currentItem().text())
        if okPressed and text != '':
            self.qlist.currentItem().setText(text)

    @pyqtSlot()
    def remove(self):
        print('remove')
        self.qlist.takeItem(self.qlist.currentRow())

    @pyqtSlot()
    def up(self):
        print('up')
        if self.qlist.currentRow() > 0:
            item = self.qlist.takeItem(self.qlist.currentRow())
            self.qlist.insertItem((self.qlist.currentRow() - 1), item.text())
            self.qlist.setCurrentRow((self.qlist.currentRow() - 2))

    @pyqtSlot()
    def down(self):
        print('down')
        if self.qlist.currentRow() < self.qlist.count():
            item = self.qlist.takeItem(self.qlist.currentRow())
            self.qlist.insertItem((self.qlist.currentRow() + 1), item.text())
            self.qlist.setCurrentRow((self.qlist.currentRow() + 1))

    @pyqtSlot()
    def sort(self):
        print('sort')
        self.qlist.sortItems()
        self.qlist.scrollToTop()

    @pyqtSlot()
    def close(self):
        print('close')
        self.stringlist = []
        for i in range(0, self.qlist.count()):
            self.stringlist.append(self.qlist.item(i).text())
        self.accept()


if __name__ == "__main__":
    fruit = ["Banana", "Apple", "Elderberry", "Clementine", "Fig",
             "Guava", "Mango", "Honeydew Melon", "Date", "Watermelon",
             "Tangerine", "Ugli Fruit", "Juniperberry", "Kiwi",
             "Lemon", "Nectarine", "Plum", "Raspberry", "Strawberry",
             "Orange"]
    app = QApplication(sys.argv)
    form = StringListDlg("Fruit", fruit)
    form.exec_()
    print("\n".join([str(x) for x in form.stringlist]))
