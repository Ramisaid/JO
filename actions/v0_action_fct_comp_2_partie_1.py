
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction à compléter 4
class AppFctComp2Partie1(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_2_bis.ui", self)
        self.data = data
        self.refreshComboBox()

    # Fonction de mise à jour de l'affichage

    def refreshComboBox(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT distinct categorieEp FROM V0_LesEpreuves"
            )
        except Exception as e:
            display.refreshLabel(self.ui.label_fct_comp_3, "Impossible d'afficher les résultats : " + repr(e))
        else:
            display.refreshGenericCombo(self.ui.comboBox, result)
        pass

    def refreshResult(self):
        # TODO 1.2 : fonction à modifier pour remplacer la zone de saisie par une liste de valeurs issues de la BD une
        #  fois le fichier ui correspondant mis à jour
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                 "SELECT numEp, nomEp, formeEp, nomDi, categorieEp, nbSportifsEp, strftime('%Y-%m-%d',dateEp,'unixepoch') FROM V0_LesEpreuves WHERE categorieEp = ?",
                [self.ui.comboBox.currentText()])

        except Exception as e:
            self.ui.comboBox.setRowCount(0)
        else:
            i = display.refreshGenericData(self.ui.table_fct_comp_3, result)
        pass

    pass
