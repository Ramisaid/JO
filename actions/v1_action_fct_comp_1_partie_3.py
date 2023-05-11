import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QPushButton
from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5 import uic


# TODO 3.1 En cours : Gérer les inscriptions aux épreuves
# Classe de gestion des inscriptions aux épreuves
class AppFctCompP3(QDialog):

    # Constructeur
    def __init__(self, parent, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_P3_1.ui", self)
        self.data = data
        self.parent = parent
        self.setup_comboBox()
        self.refreshResult()

    # Fonction permettant de remplir les comboBox forme et catégorie des épreuves
    def setup_comboBox(self):
        self._refreshFormeList()
        self._refreshCatList()

        self._refreshNumInListDel()

        # On rafraichis les autres comboBox
        self.refreshLists()
        pass

    # Permet de mettre à jour la comboBox forme des épreuves
    def _refreshFormeList(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT DISTINCT formeEp FROM LesEpreuves"
            )
        except Exception as e:
            self.ui.comboBox_forme_ep.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_forme_ep, result)
            pass
        pass

    # Permet de mettre à jour la comboBox catégorie des épreuves
    def _refreshCatList(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT DISTINCT categorieEp FROM LesEpreuves WHERE formeEp = ?",
                [self.ui.comboBox_forme_ep.currentText()]
            )
        except Exception as e:
            self.ui.comboBox_cat_ep.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_cat_ep, result)
            pass
        pass

    # Permet de mettre à jour la comboBox numIn des participants à supprimer/modifier
    def _refreshNumInListDel(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT DISTINCT numIn FROM LesInscriptions"
            )
        except Exception as e:
            self.ui.comboBox_numIn_del.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_numIn_del, result)
            pass
        self._refreshNumEpListDel()
        pass

    # Permet de mettre à jour la comboBox numEp des participants à supprimer/modifier
    def _refreshNumEpListDel(self):
        if self.ui.comboBox_numIn_del.count() != 0:
            try:
                cursor = self.data.cursor()
                result = cursor.execute(
                    "SELECT numEp FROM LesInscriptions WHERE numIn = ?",
                    [self.ui.comboBox_numIn_del.currentText()]
                )
            except Exception as e:
                self.ui.comboBox_numEp_del.clear()
            else:
                display.refreshGenericCombo(self.ui.comboBox_numEp_del, result)
                pass

        self._refreshNumEpListUpdate()
        pass

    def _refreshNumEpListUpdate(self):
        if self.ui.comboBox_numIn_del.count() != 0:
            try:
                cursor = self.data.cursor()
                result = cursor.execute(
                    """with equipes_infos as
                            (SELECT E.numEq, SB.categorieSp, COUNT(E.numSp) as nbSportifs FROM LesEquipes E JOIN LesSportifs SB ON (SB.numSp = E.numSp) GROUP BY E.numEq, SB.categorieSp HAVING COUNT(E.numSp) >= 2
                                    UNION
                                    SELECT numEq, categorieSp, nbSportifs FROM equipes_mixtes),

                    sportifs_and_equipes as ( \
                        SELECT numSp as numIn, categorieSp, NULL as nbSportifs FROM LesSportifs \
                        UNION \
                        SELECT numEq as numIn, categorieSp, nbSportifs FROM equipes_infos \
                    ), \
                    already_exist_ep as ( \
                        SELECT numEp FROM LesInscriptions WHERE numIn = ? \
                    ) \
                    SELECT numEp FROM ( \
                        SELECT * FROM LesEpreuves E JOIN sportifs_and_equipes I ON \
                            ( \
                                I.categorieSp = E.categorieEp \
                                and \
                                ( \
                                    (I.nbSportifs = E.nbSportifsEp) \
                                    OR \
                                    (E.nbSportifsEp is NULL and I.nbSportifs is not NULL and E.formeEp == \"par equipe\") \
                                    OR \
                                    (E.nbSportifsEp is NULL and I.nbSportifs is NULL and E.formeEp != \"par equipe\") \
                                ) \
                            ) WHERE numIn = ? \
                    ) WHERE numEp NOT IN already_exist_ep""",
                    [self.ui.comboBox_numIn_del.currentText(), self.ui.comboBox_numIn_del.currentText()]
                )
            except Exception as e:
                self.ui.comboBox_numEp_update.clear()
            else:
                display.refreshGenericCombo(self.ui.comboBox_numEp_update, result)
                pass
        pass

    # Fonction de mise à jour de l'affichage des inscriptions
    def refreshResult(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT numIn, numEp FROM LesInscriptions"
            )
        except Exception as e:
            self.ui.table_fct_comp_7.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_comp_7, "Impossible d'afficher les résultats : " + repr(e))
        else:
            i = display.refreshGenericData(self.ui.table_fct_comp_7, result)
            if i == 0:
                display.refreshLabel(self.ui.label_fct_comp_7, "Aucun résultat")
        pass

    # Fonction de mise à jour des épreuves affichés dans la comboBox inscription
    @pyqtSlot()
    def refreshLists(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT numEp FROM LesEpreuves WHERE formeEp = ? and categorieEp = ?",
                [self.ui.comboBox_forme_ep.currentText(), self.ui.comboBox_cat_ep.currentText()]
            )
        except Exception as e:
            print("Impossible de rafraîchir la liste des épreuves : ", repr(e))
            pass
        else:
            display.refreshGenericCombo(self.ui.comboBox_numEp, result)
            pass
        pass

    @pyqtSlot()
    def refreshParticipantsLists(self):
        self.ui.comboBox_numIn.clear()

        if self.ui.comboBox_numEp.count() != 0:
            if self.ui.comboBox_forme_ep.currentText() == "individuelle":
                try:
                    cursor = self.data.cursor()
                    result = cursor.execute(
                        "SELECT numSp FROM LesSportifs WHERE categorieSp = ? AND numSp NOT IN (Select numIn FROM LesInscriptions WHERE numEP = ?)",
                        [self.ui.comboBox_cat_ep.currentText(), self.ui.comboBox_numEp.currentText()]
                    )
                except Exception as e:
                    self.ui.comboBox_numIn.clear()
                    pass
                else:
                    display.refreshGenericCombo(self.ui.comboBox_numIn, result)
                    pass
                pass
            else:
                try:
                    cursor = self.data.cursor()
                    result = cursor.execute("""
                        with equipes_infos as
                            (SELECT E.numEq, SB.categorieSp, COUNT(E.numSp) as nbSportifs FROM LesEquipes E JOIN LesSportifs SB ON (SB.numSp = E.numSp) GROUP BY E.numEq, SB.categorieSp HAVING COUNT(E.numSp) >= 2
                                UNION
                             SELECT numEq, categorieSp, nbSportifs FROM equipes_mixtes)
                        SELECT I.numEq FROM LesEpreuves E JOIN equipes_infos I ON (I.categorieSp = E.categorieEp and (I.nbSportifs = E.nbSportifsEp or E.nbSportifsEp is NULL)) WHERE E.numEP = ?""",
                        [self.ui.comboBox_numEp.currentText()]
                    )
                except Exception as e:
                    self.ui.comboBox_numIn.clear()
                    pass
                else:
                    display.refreshGenericCombo(self.ui.comboBox_numIn, result)
                    pass
            pass

        pass

    # Fonction permettant d'ajouter un participant
    def addParticipant(self):
        if self.ui.comboBox_numIn.count() != 0 and self.ui.comboBox_numEp.count() != 0:
            try:
                cursor = self.data.cursor()
                result = cursor.execute(
                    "INSERT INTO LesInscriptions (numIn, numEp) VALUES (?, ?)",
                    [self.ui.comboBox_numIn.currentText(), self.ui.comboBox_numEp.currentText()]
                )
            except Exception as e:
                print("Impossible d'inscrire le(s) participant(s) : ", repr(e))
                pass
            else:
                # On modifie la base de données et on propage les modifications aux autres fenêtres
                self.data.commit()
                self.parent.changedValue.emit()

                # On rafraîchit les résultats de la fenêtre
                self.refreshResult()
                self.refreshParticipantsLists()
                display.refreshLabel(self.ui.label_fct_comp_7,
                                     "Ajout de la nouvelle participation effectué")
                pass
            pass
        else:
            display.refreshLabel(self.ui.label_fct_comp_7,
                                 "Impossible d'inscrire le(s) participant(s) : Champs manquants")
            pass
        pass

    # Fonction permettant de supprimer un participant
    def removeParticipant(self):
        if self.ui.comboBox_numIn_del.count() != 0 and self.ui.comboBox_numEp_del.count() != 0:
            try:
                cursor = self.data.cursor()
                result = cursor.execute(
                    "DELETE FROM LesInscriptions WHERE numIn = ? and numEp = ?",
                    [self.ui.comboBox_numIn_del.currentText(), self.ui.comboBox_numEp_del.currentText()]
                )
            except Exception as e:
                print("Impossible de supprimer le(s) participant(s) : ", repr(e))
                pass
            else:
                # On modifie la base de données et on propage les modifications aux autres fenêtres
                self.data.commit()
                self.parent.changedValue.emit()

                # On rafraîchit les résultats de la fenêtre
                self.refreshResult()
                self.refreshParticipantsLists()
                self._refreshNumInListDel()
                pass
            pass
        else:
            display.refreshLabel(self.ui.label_fct_comp_7,
                                 "Impossible de supprimer le(s) participant(s) : Champs manquants")
            pass
        pass

    # Fonction permettant de modifier un participant
    def updateParticipant(self):
        if self.ui.comboBox_numIn_del.count() != 0 and self.ui.comboBox_numEp_del.count() != 0 and self.ui.comboBox_numEp_update.count() != 0:

            numSp = int(self.ui.comboBox_numIn_del.currentText())
            numEp = int(self.ui.comboBox_numEp_update.currentText())

            # sportif
            if numSp >= 1000 and numSp <= 1500:

                try:
                    cursor = self.data.cursor()
                    result = cursor.execute(
                        "SELECT numEP FROM LesEpreuves E JOIN LesSportifs SB ON (E.categorieEp = SB.categorieSp and E.formeEp = \"individuelle\") WHERE SB.numSp = ?",
                        [self.ui.comboBox_numIn_del.currentText()]
                    )
                except Exception as e:
                    print("error : ", repr(e))
                    pass
                else:
                    ep_array = []
                    for row_num, row_data in enumerate(result):
                        ep_array.append(row_data[0])
                    if numEp in ep_array:
                        self._update_participant()
                        pass
                    pass
                pass
            # équipe
            else:
                try:
                    cursor = self.data.cursor()
                    result = cursor.execute(
                        "with equipes_list_ as ( \
                             SELECT numEp, nbSportifsEp, categorieEp, formeEp FROM LesEpreuves E WHERE formeEp != \"individuelle\" \
                        ), \
                        check_equipe as ( \
                            SELECT E.numEq, L.numEp FROM equipes_infos E JOIN equipes_list_ L ON \
                                ( \
                                    ((E.nbSportifs = L.nbSportifsEp and E.nbSportifs >= 2 and L.formeEp = \"par equipe\") \
                                        OR \
                                    (L.nbSportifsEp = 2 and E.nbSportifs = 2 and L.formeEp = \"par couple\" and E.categorieSp = \"mixte\")) \
                                        AND \
                                    (L.categorieEp = E.categorieSp) \
                                ) \
                        ) \
                        Select numEq FROM check_equipe WHERE numEq = ? and numEp = ?",
                        [self.ui.comboBox_numIn_del.currentText(), self.ui.comboBox_numEp_update.currentText()]
                    )
                except Exception as e:
                    print("error : ", repr(e))
                    pass
                else:
                    ep_array = []
                    for row_num, row_data in enumerate(result):
                        ep_array.append(row_data[0])
                    if numSp in ep_array:
                        self._update_participant()
                        pass
                    else:
                        display.refreshLabel(self.ui.label_fct_comp_7,
                                             "Impossible de modifier le(s) participant(s) : L'épreuve ne correspond pas au(x) participant(s)")
                        pass
                    pass
                pass
        else:
            display.refreshLabel(self.ui.label_fct_comp_7,
                                 "Impossible de modifier le(s) participant(s) : Champs manquants")
            pass
        pass

    def _update_participant(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "UPDATE LesInscriptions SET numEp = ? WHERE numIn = ? and numEp = ?",
                [self.ui.comboBox_numEp_update.currentText(), self.ui.comboBox_numIn_del.currentText(),
                 self.ui.comboBox_numEp_del.currentText()]
            )
        except Exception as e:
            print("Impossible de modifier le(s) participant(s) : ", repr(e))
            pass
        else:
            # On modifie la base de données et on propage les modifications aux autres fenêtres
            self.data.commit()
            self.parent.changedValue.emit()

            display.refreshLabel(self.ui.label_fct_comp_7,
                                 "Inscription mise à jour : participant " + self.ui.comboBox_numIn_del.currentText() + " : épreuve : " + self.ui.comboBox_numEp_del.currentText() + " -> " + self.ui.comboBox_numEp_update.currentText())

            # On rafraîchit les résultats de la fenêtre
            self.refreshResult()
            self.refreshParticipantsLists()
            self._refreshNumInListDel()
        pass