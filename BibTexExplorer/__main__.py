import sys
import os

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QIcon
from BibTexExplorer.bibfiletools import parse_bibfile
from BibTexExplorer.TableWidget import TableWidget

def main():
    app = QApplication(sys.argv)
    try:
        d = parse_bibfile(sys.argv[1])
    except IndexError:
        QMessageBox.warning(
                None, "Wrong number of arguments",
                "Missing 'bibtex' file argument\n"
                "Use: BibTexExplorer file.bib"
            )
        sys.exit(1)

    scriptDir = os.path.dirname(os.path.realpath(__file__))
    app.setWindowIcon(QIcon(scriptDir + os.path.sep + 'icons'+ os.path.sep+ 'Everaldo-Desktoon-Library.ico'))
    w = TableWidget()
    w.setWindowTitle("BibTex Explorer")
    
    w.populate(d)
    w.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()