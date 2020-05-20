import os
from PyQt5.QtWidgets import (
    QTableWidgetItem,
    QTableWidget,
    QApplication,
    QWidget,
    QVBoxLayout,
    QToolBar,
    QAction,
    QLabel,
    QMessageBox,
    QMenu,
    QCheckBox,
    QLineEdit,
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QCursor


class MyTableWidgetItem(QTableWidgetItem):
    def __init__(self, number):
        QTableWidgetItem.__init__(self, number, QTableWidgetItem.UserType)
        self.__number = number

    def __lt__(self, other):
        return int(self.__number) < int(other.__number)


class TableWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.table = QTableWidget()

        tb = QToolBar()
        tb.setIconSize(QSize(24, 24))
        tmp = QLabel("Author", self)
        tmpfont = QFont()
        tmpfont.setBold(True)
        tmp.setFont(tmpfont)
        tb.addWidget(tmp)
        self.authorle = QLineEdit(self)
        tb.addWidget(self.authorle)
        tb.addSeparator()
        tmp = QLabel("Journal", self)
        tmpfont = QFont()
        tmpfont.setBold(True)
        tmp.setFont(tmpfont)
        tb.addWidget(tmp)
        self.journalle = QLineEdit(self)
        tb.addWidget(self.journalle)
        tb.addSeparator()
        tmp = QLabel("Title", self)
        tmp.setFont(tmpfont)
        tb.addWidget(tmp)
        self.titlele = QLineEdit(self)
        tb.addWidget(self.titlele)
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.table)
        vbox.insertWidget(0, tb)

        connectid = self.authorle.textChanged.connect(self.filter)
        connectid = self.journalle.textChanged.connect(self.filter)
        connectid = self.titlele.textChanged.connect(self.filter)
        connectid = self.table.cellDoubleClicked.connect(self.itemDoubleClicked)

        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)

        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        connectid = self.table.customContextMenuRequested.connect(self.handleMenu)

    def copyBtex(self):
        btex = self.entries[self.selecteditemkey]["bibtex"]
        QApplication.clipboard().setText(btex)

    def handleMenu(self, pos):
        self.selecteditemkey = self.table.item(self.table.itemAt(pos).row(), 0).text()
        # self.table.itemAt(pos)
        # print('column(%d)' % self.table.horizontalHeader().logicalIndexAt(pos))
        menu = QMenu()
        btexcopyaction = menu.addAction("Copy BibTex entry to Clipboard")
        connectid = btexcopyaction.triggered.connect(self.copyBtex)
        menu.exec_(QCursor.pos())

    def itemDoubleClicked(self, row, column):
        if column > 0:
            return
        fpdf = self.table.item(row, column).text() + ".pdf"
        try:
            os.startfile(fpdf)  # Only works on Windows
        except FileNotFoundError:
            QMessageBox.warning(
                None, "Missing PDF file", "The file '%s' can't be found!" % fpdf,
            )

    def filter(self):
        wordsauthor = self.authorle.text().split() + [""]
        wordsjournal = self.journalle.text().split() + [""]
        wordstitle = self.titlele.text().split() + [""]

        for i in range(self.table.rowCount()):
            self.table.showRow(i)
            for word in wordsauthor:
                if word not in self.table.item(i, 3).text():
                    self.table.hideRow(i)
                    break
            for word in wordsjournal:
                if word not in self.table.item(i, 4).text():
                    self.table.hideRow(i)
                    break
            for word in wordstitle:
                if word not in self.table.item(i, 5).text():
                    self.table.hideRow(i)
                    break

    def populate(self, entries):
        self.entries = entries
        items = ["id", "year", "citations", "author", "journal", "title"]
        numericitems = ["year", "citations"]
        alignments = [
            Qt.AlignHCenter,
            Qt.AlignHCenter,
            Qt.AlignHCenter,
            Qt.AlignLeft,
            Qt.AlignLeft,
            Qt.AlignLeft,
        ]
        widths = [150, 80, 90, 250, 250, 500]
        self.resize(sum(widths) + 50, 800)
        self.table.setRowCount(len(entries))
        self.table.setColumnCount(len(items))
        self.table.horizontalHeader().setFont(QFont("Arial", 9, QFont.Bold))

        for col, key in enumerate(items):
            item = QTableWidgetItem(key)
            item.setTextAlignment(alignments[col])
            item.setFont(QFont("Times", 20, QFont.Bold))
            self.table.setHorizontalHeaderItem(col, QTableWidgetItem(key))
            self.table.setColumnWidth(col, widths[col])

        for row, item_key in enumerate(entries.keys()):
            item_list = entries[item_key]

            for col, key in enumerate(items):
                if key in numericitems:
                    try:
                        newitem = MyTableWidgetItem(str(int(item_list[key])))
                    except:
                        newitem = MyTableWidgetItem("0")
                else:
                    try:
                        newitem = QTableWidgetItem(item_list[key])
                    except:
                        newitem = QTableWidgetItem("-")
                newitem.setTextAlignment(alignments[col])
                newitem.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(row, col, newitem)
        self.table.sortItems(2, Qt.DescendingOrder)
        self.table.setStyleSheet(
            "alternate-background-color: lightgray; background-color: white;"
        )
