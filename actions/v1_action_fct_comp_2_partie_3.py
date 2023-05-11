
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic


# TODO 3.2  : RESULTS DES EPREUVES
# Classe de gestion des résultats
class AppFctCompP3_2(QDialog):

    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        try:
            self.ui = uic.loadUi("gui/fct_comp_P3_2.ui", self)
        except Exception as e:
            print(e)
        self.data = data
        self.tablerefresh()
        self.refreshComboBox()
        self.tablerefresh()

    def refreshComboBox(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT distinct numEp FROM LesEpreuves"
            )
        except Exception as e:
            display.refreshLabel(self.ui.label_fct_comp_7, "Impossible d'afficher les résultats : " + repr(e))
        else:
            display.refreshGenericCombo(self.ui.comboBox_forme_ep, result)
        pass

    def refreshComboBox2(self):
        try:
            cursor = self.data.cursor() 
            result = cursor.execute(
                "SELECT distinct numIn FROM LesInscriptions WHERE numEp = ?",
                [self.ui.comboBox_forme_ep.currentText()]
               
            )
        except Exception as e:
            display.refreshLabel(self.ui.label_fct_comp_7, "Impossible d'afficher les résultats : " + repr(e))
        else:
            display.refreshGenericCombo(self.ui.comboBox_numIn_del, result)

        pass

    def refreshComboBox4(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT distinct numIn FROM LesInscriptions WHERE numEp = ?",
                [self.ui.comboBox_forme_ep.currentText()]
               
            )
        except Exception as e:
            display.refreshLabel(self.ui.label_fct_comp_7, "Impossible d'afficher les résultats : " + repr(e))
        else:
            display.refreshGenericCombo(self.ui.comboBox_numEp_del, result)

        pass

    def refreshComboBox3(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT distinct numIn FROM LesInscriptions WHERE numEp = ?",
                [self.ui.comboBox_forme_ep.currentText()]
               
            )
        except Exception as e:
            display.refreshLabel(self.ui.label_fct_comp_7, "Impossible d'afficher les résultats : " + repr(e))
        else:
            display.refreshGenericCombo(self.ui.comboBox_numEp_update, result)

        pass


    # Fonction de mise à jour de l'affichage
    def refreshResult(self):
       
       try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "INSERT INTO LesResultats (numEp,gold,silver,bronze) VALUES (?,?,?,?)",
                [self.ui.comboBox_forme_ep.currentText(),self.ui.comboBox_numIn_del.currentText(),self.ui.comboBox_numEp_del.currentText(),self.ui.comboBox_numEp_update.currentText()])          
       except Exception as e:
            display.refreshLabel(self.ui.label_fct_comp_7, "Impossible d'afficher les résultats : " + repr(e))
            
       pass
       self.tablerefresh()
    pass


    def refreshedit(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "UPDATE LesResultats SET gold = ? ,silver = ? , bronze = ? WHERE numEp = ?",
                [self.ui.comboBox_numIn_del.currentText(),self.ui.comboBox_numEp_del.currentText(),self.ui.comboBox_numEp_update.currentText(),self.ui.comboBox_forme_ep.currentText()])          
        except Exception as e:
            display.refreshLabel(self.ui.label_fct_comp_7, "Impossible d'afficher les résultats : " + repr(e))
            
        pass
        self.tablerefresh()

    def refreshdelete(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "DELETE FROM LesResultats WHERE numEp = ?",
                [self.ui.comboBox_forme_ep.currentText()])          
        except Exception as e:
            display.refreshLabel(self.ui.label_fct_comp_7, "Impossible d'afficher les résultats : " + repr(e))
            
        pass
        self.tablerefresh()

    def tablerefresh(self):
       
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT numEp,gold,silver,bronze FROM LesResultats")
            
        except Exception as e:
       
            display.refreshLabel(self.ui.label_fct_comp_7, "Impossible d'afficher les résultats : " + repr(e))
        else:
          
            i = display.refreshGenericData(self.ui.table_fct_comp_7, result)
        pass
    pass

    def refreshmedailles(self):
        self.refreshComboBox2()
        self.refreshComboBox3()
        self.refreshComboBox4()

