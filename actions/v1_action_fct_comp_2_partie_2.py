
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fenetre de la partie 2.1
class AppFctCompP2_2(QDialog):

    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_P2_2.ui", self)
        self.data = data
        self.refreshResult()

        # Fonction de mise à jour de l'affichage

    def refreshResult(self):
        display.refreshLabel(self.ui.label_fct_comp_2_P2, "")

        try:
            cursor = self.data.cursor()
            result = cursor.execute(

                ("""
                               with Sportifs_or as (
                                   SELECT SB.pays, COUNT(SB.numSp) as Medaille_or, 0 as Medaille_Argent, 0 as Medaille_bronze FROM LesResultats R JOIN LesSportifs SB ON (SB.numSp == R.gold) GROUP BY SB.pays
                                   UNION
                                   SELECT SB.pays, 0 as Medaille_or, COUNT(SB.numSp) as Medaille_Argent, 0 as Medaille_bronze FROM LesResultats R JOIN LesSportifs SB ON (SB.numSp == R.silver) GROUP BY SB.pays
                                   UNION
                                   SELECT SB.pays, 0 as Medaille_or, 0 as Medaille_Argent, COUNT(SB.numSp) as Medaille_bronze FROM LesResultats R JOIN LesSportifs SB ON (SB.numSp == R.bronze) GROUP BY SB.pays
                               ),
                               EquipePays as (
                                   SELECT distinct E.numEq, SB.pays FROM LesEquipes E JOIN LesSportifs SB ON (E.numSp == SB.numSp)
                               ),
                               Equipes_or as (
                                   SELECT E.pays, count(E.numEq) as Medaille_or, 0 as Medaille_Argent, 0 as Medaille_bronze FROM LesResultats R JOIN EquipePays E ON (E.numEq == R.gold) GROUP BY E.pays
                                   UNION
                                   SELECT E.pays, 0 as Medaille_or, COUNT(E.numEq) as Medaille_Argent, 0 as Medaille_bronze FROM LesResultats R JOIN EquipePays E ON (E.numEq == R.silver) GROUP BY E.pays
                                   UNION
                                   SELECT E.pays, 0 as Medaille_or, 0 as Medaille_Argent, COUNT(E.numEq) as Medaille_bronze FROM LesResultats R JOIN EquipePays E ON (E.numEq == R.bronze) GROUP BY E.pays
                               )
                               SELECT pays, SUM(Medaille_or) as Medaille_or, SUM(Medaille_Argent) as Medaille_Argent, SUM(Medaille_bronze) as Medaille_bronze FROM (
                                   SELECT pays, Medaille_or, Medaille_Argent, Medaille_bronze FROM Sportifs_or
                                       UNION ALL
                                   SELECT pays, Medaille_or, Medaille_Argent, Medaille_bronze FROM Equipes_or
                               ) GROUP BY pays ORDER BY Medaille_or DESC, Medaille_Argent DESC, Medaille_bronze DESC""")
            )
        except Exception as e:
            self.ui.table_fct_comp_2_P2.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_comp_2_P2, "Impossible d'afficher les résultats : " + repr(e))
        else:
            i = display.refreshGenericData(self.ui.table_fct_comp_2_P2, result)
            if i == 0:
                display.refreshLabel(self.ui.label_fct_comp_2_P2, "Aucun résultat")