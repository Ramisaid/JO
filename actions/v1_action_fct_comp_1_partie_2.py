
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fenetre de la partie 2.1
class AppFctCompP2(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_P2_1.ui", self)
        self.data = data
        self.refreshResult()

    # Fonction de mise à jour de l'affichage
    def refreshResult(self):
        display.refreshLabel(self.ui.label_fct_comp_1_P2, "")

        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT S.numEq, AVG(ageSp) as moyenne_age FROM LesEquipes S JOIN LesAgesSportifs A USING (numSp) JOIN LesResultats R on (R.gold == S.numEq) GROUP BY numEq;"

            )
        except Exception as e:
            self.ui.table_fct_comp_1_P2.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_comp_1_P2, "Impossible d'afficher les résultats : " + repr(e))
        else:
            i = display.refreshGenericData(self.ui.table_fct_comp_1_P2, result)
            if i == 0:
                display.refreshLabel(self.ui.label_fct_comp_1_P2, "Aucun résultat")