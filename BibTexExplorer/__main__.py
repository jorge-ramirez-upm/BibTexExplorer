import sys

from PyQt5.QtWidgets import QApplication, QMessageBox
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

    w = TableWidget()
    
    w.populate(d)
    w.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()