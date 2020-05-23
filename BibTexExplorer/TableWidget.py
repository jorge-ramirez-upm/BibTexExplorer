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
    QShortcut,
    QSpinBox
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QCursor, QIcon, QKeySequence
from .BibTexExplorer_rc import *


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
        self.setWindowIcon(QIcon(":/Images/icons/Everaldo-Desktoon-Library.ico"))
        self.setWindowTitle("BibTex Explorer")

        tb = QToolBar()
        tb.setIconSize(QSize(24, 24))
        tmpfont = QFont()
        tmpfont.setBold(True)

        tmp = QLabel("<u>F</u>rom", self)
        tmp.setTextFormat(Qt.RichText);
        tmp.setToolTip("From this year")
        tmp.setFont(tmpfont)
        tb.addWidget(tmp)
        self.fromyear = QSpinBox(self)
        self.fromyear.setMinimum(1850)
        self.fromyear.setMaximum(2030)
        self.fromyear.setValue(1850)
        scfromyear = QShortcut(QKeySequence("Alt+F"), self)
        scfromyear.activated.connect(self.fromyear.setFocus)
        tb.addWidget(self.fromyear)
        tb.addSeparator()

        tmp = QLabel("T<u>o</u>", self)
        tmp.setTextFormat(Qt.RichText);
        tmp.setToolTip("To this year")
        tmp.setFont(tmpfont)
        tb.addWidget(tmp)
        self.toyear = QSpinBox(self)
        self.toyear.setMinimum(1850)
        self.toyear.setMaximum(2030)
        self.toyear.setValue(2030)
        sctoyear = QShortcut(QKeySequence("Alt+O"), self)
        sctoyear.activated.connect(self.toyear.setFocus)
        tb.addWidget(self.toyear)
        tb.addSeparator()

        tmp = QLabel("<u>A</u>uthor", self)
        tmp.setFont(tmpfont)
        tmp.setToolTip("Space separated author names (may be incomplete)")
        tb.addWidget(tmp)
        self.authorle = QLineEdit(self)
        scauthor = QShortcut(QKeySequence("Alt+A"), self)
        scauthor.activated.connect(self.authorle.setFocus)
        tb.addWidget(self.authorle)
        tb.addSeparator()
        tmp = QLabel("<u>J</u>ournal", self)
        tmp.setToolTip("Space separated journal name words (may be incomplete)")
        tmp.setFont(tmpfont)
        tb.addWidget(tmp)
        self.journalle = QLineEdit(self)
        scjournal = QShortcut(QKeySequence("Alt+J"), self)
        scjournal.activated.connect(self.journalle.setFocus)
        tb.addWidget(self.journalle)
        tb.addSeparator()
        tmp = QLabel("<u>T</u>itle", self)
        tmp.setToolTip("Space separated title words (may be incomplete)")
        tmp.setFont(tmpfont)
        tb.addWidget(tmp)
        self.titlele = QLineEdit(self)
        sctitle = QShortcut(QKeySequence("Alt+T"), self)
        sctitle.activated.connect(self.titlele.setFocus)
        tb.addWidget(self.titlele)
        self.actionreset = tb.addAction(
            QIcon(":/Images/icons/icons8-available-updates-96.png"), "Reset Filters"
        )
        self.actionreset.setShortcut(Qt.CTRL + Qt.Key_R)
        connectid = self.actionreset.triggered.connect(self.reset)
        self.actionhelp = tb.addAction(
            QIcon(":/Images/icons/icons8-help-96.png"), "BibTex Explorer Help"
        )
        self.actionhelp.setShortcut(Qt.Key_F1)
        connectid = self.actionhelp.triggered.connect(self.about)

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.table)
        vbox.insertWidget(0, tb)

        connectid = self.authorle.textChanged.connect(self.filter)
        connectid = self.journalle.textChanged.connect(self.filter)
        connectid = self.titlele.textChanged.connect(self.filter)
        connectid = self.fromyear.valueChanged.connect(self.filter)
        connectid = self.toyear.valueChanged.connect(self.filter)
        connectid = self.table.cellDoubleClicked.connect(self.itemDoubleClicked)

        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)

        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        connectid = self.table.customContextMenuRequested.connect(self.handleMenu)

    def about(self):
        text = """<b>Basic use</b><br>To filter the entries:"""
        text += """<ul><li>Input a year range (<i>i.e.</i>from <b>2004</b> to <b>2008</b>)</li>"""
        text += """<li>Input space-separated words (complete or incomplete) in the text boxes, <i>i.e.</i>:"""
        text += """<ul><li>Author: "<i>Smi Jo</i>"</li><li>Journal: "<i>Phy Re</i>"</li><li>Title: "<i>Phot Pol</i>"</li></ul></li>"""
        text += """<li>Ctrl-R to reset filters</li></ul>"""
        text += """Other commands:"""
        text += """<ul><li>Double-click on the key to open the corresponding PDF file (if available)</li>"""
        text += """<li>Right-click on an item to copy the bibtex entry</li></ul>"""
        text += """&copy; <a href="mailto: jorge.ramirez@upm.es">Jorge Ramírez</a> UPM 2020<br><a href="http://blogs.upm.es/compsoftmatter/">Author's personal page</a>"""
        QMessageBox.information(
            self, "BibTexExplorer information", text,
        )

    def reset(self):
        self.authorle.setText("")
        self.journalle.setText("")
        self.titlele.setText("")
        self.fromyear.setValue(1850)
        self.toyear.setValue(2030)


    def copyBtex(self):
        btex = self.entries[self.selecteditemkey]["bibtex"]
        QApplication.clipboard().setText(btex)

    def handleMenu(self, pos):
        self.selecteditemkey = self.table.item(self.table.itemAt(pos).row(), 0).text()
        menu = QMenu()
        btexcopyaction = menu.addAction("Copy BibTex entry to Clipboard")
        connectid = btexcopyaction.triggered.connect(self.copyBtex)
        menu.exec_(QCursor.pos())

    def itemDoubleClicked(self, row, column):
        if column > 0:
            return
        fpdf = self.path + os.sep + self.table.item(row, column).text() + ".pdf"
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
        yfrom = self.fromyear.value()
        yto = self.toyear.value()

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
            year = int(self.table.item(i, 1).text())
            if year<yfrom or year>yto:
                self.table.hideRow(i)

    def populate(self, entries):
        self.entries = entries
        items = ["key", "year", "citations", "author", "journal", "title"]
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

    def setbibtexpath(self, file):
        self.path = os.path.dirname(os.path.abspath(file))
