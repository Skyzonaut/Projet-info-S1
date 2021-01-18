from tkinter import *
from pprint import *
from classe.plateau import *
from classe.event import *
from functools import partial
from time import *
from datetime import *
from random import randint

running = True

class initPlateau(Frame):

    def __init__(self, parent, typeOfGame, platInitType, difficulty="hard"):
        """
        Création et initialisation du jeu

        :param parent: Fenêtre tkinter parente
        :type parent: Tkinter
        :param typeOfGame: Type du jeu (IA/PVP)
        :param platInitType: Agencement initial des pièces d'echecs
        :param difficulty: Difficulté du jeu
        """

        # On initialise cette fenêtre sur la racine donnée @Frame
        Frame.__init__(self, parent)

        # Root window
        self.parent = parent
        parent.resizable(False, False)

        # Partie contre une IA ou contre un autre joueur
        self.typeOfGame = typeOfGame

        # Difficulté de l'IA
        self.difficulty = difficulty

        # Valeur indépendantes
        self.fenX = 1300
        self.fenY = 880

        # Event id generator
        self.id = 1

        # Nombre du tour
        self.tour = 1

        # Event history
        initEvent = event("0", (0,0), "place")
        self.event_log = [initEvent]

        # Objet plateau qui contient les positions et infos et pions.
        # Utilisant comme repertoire un Set de pion limité
        self.plat = Plateau(platInitType)

        # Dictionnaire de type { (x,y) : button } contenant tous les boutons (ou cases) de l'échiquier,
        # permet de faire la lisaison avec les cases du plateau.
        # En cas d'action sur un bouton on parcours ce dictionnaire pour retrouver sa matrice,
        # et ainsi pouvoir mettre à jour celle du plateau.
        # En quelque sorte ce dictionnaire est la matrice graphique, là où celle du plateau est la "base de donnée"
        self.dict_bouton = {}
        self.coul_bouton = {}

        # Valeur permettant d'alterner les couleurs
        self.black = False

        # Valeur contenant le tour actuel
        self.tourColorDisplay = True
        self.textTourStringVar = StringVar()
        self.textTourStringVar.set("AU TOUR DES BLANCS")

        # Echec ou non, permet de bloquer le jeu si il y a un echec
        self.whiteEnEchec = False
        self.blackEnEchec = False
        self.pionWhitePlayEchec = []
        self.pionBlackPlayEchec = []

        # Valeur contenant le panneau d'affichage d'état du jeu
        self.textAffichage = StringVar()
        self.textAffichage.set("")

        # Valeur contenant le numéro du tour
        self.textNbTour = StringVar()
        self.textNbTour.set(str(self.tour))

        # Protocol Handler
        parent.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Initialisation de l'interface graphique
        self.initiateUI()


    def initiateUI(self):

        # Fenetre sur laquelle on placera tous les composants
        self.parent.geometry(str(self.fenX) + "x" + str(self.fenY))

        # Echiquier, Canvas sur lequel placer les boutons, lui-meme placé sur la fenêtre fen.
        self.echiquier = Canvas(self.parent, bg='white', width=950, height=int(self.fenY))
        self.echiquier.pack(side=LEFT)

        # Console, Canvas sur lequel placer les textes et autres commandes, lui-meme placé sur la fenêtre fen.
        self.console = Canvas(self.parent, bg="grey", width=(self.fenX - 950), height=int(self.fenY))
        self.console.pack(side=LEFT)

        # Label affichant le numéro du tour actuel
        self.nbTour = Label(self.console, width=45, height=2)
        self.nbTour['textvariable'] = self.textNbTour
        self.nbTour['fg'] = "black"
        self.nbTour['bg'] = "#3BCB38"
        self.nbTour.place(x=self.console.winfo_x()+11, y=8)

        # Label affichant la couleur qui doit jouer
        self.tourLabel = Label(self.console, width=45, height=9)
        self.tourLabel['textvariable'] = self.textTourStringVar
        self.tourLabel['fg'] = "black"
        self.tourLabel['bg'] = "white"
        self.tourLabel.place(x=self.console.winfo_x()+11, y=55)

        # Label affichant l'historique des coups
        self.historiquePanneau = Text(self.console, width=34, height=22)
        self.historiquePanneau['fg'] = "black"
        self.historiquePanneau['bg'] = "#babfbb"
        self.historiquePanneau['cursor'] = "arrow"
        self.historiquePanneau['padx'] = "5px"
        self.historiquePanneau['pady'] = "5px"
        self.historiquePanneau['relief'] = "solid"
        self.historiquePanneau['borderwidth'] = "1px"
        self.historiquePanneau['state'] = "disabled"
        self.historiquePanneau['wrap'] = "word"
        self.historiquePanneau['font'] = ("Courier", 11, "bold")
        self.historiquePanneau.place(x=self.console.winfo_x()+11, y=205)

        # Label affichant les echecs
        self.affichage = Label(self.console, width=45, height=7)
        self.affichage['textvariable'] = self.textAffichage
        self.affichage['fg'] = "black"
        self.affichage['bg'] = "#789FDE"
        self.affichage.place(x=self.console.winfo_x()+12, y=600)

        # Bouton pour restart le jeu
        self.restartButton = Button(self.console, text="RESTART GAME", width=45, height=4, command=self.restart)
        self.restartButton['borderwidth'] = 3
        self.restartButton['fg'] = "black"
        self.restartButton['bg'] = "grey"
        self.restartButton.place(x=self.console.winfo_x()+11, y=720)

        # Bouton pour quitter la fenêtre
        self.quitButton = Button(self.console, text="QUIT", width=45, height=4, command=self.on_closing)
        self.quitButton['borderwidth'] = 3
        self.quitButton['fg'] = "white"
        self.quitButton['bg'] = "#A02B2B"
        self.quitButton.place(x=self.console.winfo_x()+11, y=800)

        # Crée la grille du plateau
        self.create_grid()


    def create_grid(self):
        """
        Fonction créant la grille du plateau et initialisant les boutons/cases
        """

        # On parcours de gauche à droite, puis de haut en bas
        # Du bas vers le haut
        self.y = 1
        while self.y <= 8:

            # De gaughe à droite
            self.x = 1
            while self.x <= 8:

                # On récupère la photo correspondant au pion contenant à cette emplacement du plateau
                self.photo = self.plat.getCase(self.x, self.y).getImage()

                # On crée un bouton à cette position, avec la photo de sa case du plateau, on lui donne une couleur.
                # Et une fonction onClick()
                self.bouton = Button(self.echiquier)

                # On ajoute ce bouton au dictionnaire de boutons
                self.dict_bouton[(self.x, self.y)] = self.bouton
                self.coul_bouton[(self.x, self.y)] = "#638f6e" if self.black else "white"
                self.bouton.config(
                    width=self.echiquier.winfo_reqwidth()//8,  #119px
                        height=self.echiquier.winfo_reqheight()//8,  #113px
                            bg="#638f6e" if self.black else "white",
                                activebackground="#46634d" if self.black else "#bbbfbc",
                                    image=self.photo,
                                        command=partial(self.play, (self.x, self.y)))

                # Et pour finir on place le bouton sur le canvas pour l'afficher
                self.bouton.place(x=(self.x-1)*self.echiquier.winfo_reqwidth()/8, y=(self.y-1)*self.echiquier.winfo_reqheight()/8)

                # On passe à la colonne suivante et change de couleur
                self.x += 1 ; self.black = not self.black

            # On passe à la Ligne suivante et change de couleur
            self.y += 1 ; self.black = not self.black


    def play(self, tuple: tuple):
        """
        Gère les règles du jeu au moment du clic et lance le coup.
        Les coups de l'IA étant tous lancés directements à la fin du coup du joueur

        :param tuple: Coordonnées de la case qui a été cliquée
        """

        if self.typeOfGame == "ia":

            # Si le jeu est contre un IA, on empêche de cliquer sur les pions noirs (ceux de l'IA)
            self.disableButtons(self.dict_bouton, self.plat.getMatriceByCouleur("noir"))

            # Si c'est au joueur de jouer, joue puis lance les coups de l'IA
            if not self.black:

                self.move(tuple)

                if self.event_log[-1].getAction() == "place":

                    self.nextMoveIA = self.getMoveIA(tuple)
                    self.moveIA(self.nextMoveIA[0])
                    sleep(0.1)
                    self.moveIA(self.nextMoveIA[1])

        else:

            self.move(tuple)


    def move(self, tuple: tuple):
        """
        Fonction gérant l'affichage, les calculs des règles du jeu, l'état du jeu, les mouvements, etc...
        Le jeu se met à jour à chaque appel de cette fonction

        :param tuple: Coordonnées de la case qui a été cliquée
        """

        # Id du nouvel évènement
        self.newId = self.id

        # Bouton qui a été cliqué
        self.bouton = self.dict_bouton[(tuple[0], tuple[1])]

        # On récupère la couleur du pion à jouer
        self.couleurPion = self.plat.getCase(tuple[0], tuple[1]).getCouleur()

        # Si le clic précédant étant un placement, alors celui-ci sera une sélection de pion
        if self.event_log[-1].getAction() != "click":

            # Si c'est la bonne couleur qui est jouée
            if self.tourCouleurVerificateur(self.plat.getCase(tuple[0], tuple[1]).getCouleur(), self.tourColorDisplay):

                # On crée un nouvel évènement de click simple
                self.newEvent = event(str(self.newId), tuple, "click")

                # Comme c'est un click et non un place, ça signifie que ce bouton est
                # l'origine du mouvement, donc contient le pion à bouger
                if self.plat.getCase(tuple[0], tuple[1]):

                    self.newEvent.setCache(self.plat.getCase(tuple[0], tuple[1]).getImage())

                # Colorie la case en gris pour indiquer l'origine du mouvement
                self.bouton.config(bg="#aaaaaa")

                # Déplacement possibles simple du pion qui a été cliqué
                self.possibleMoves = self.plat.getPath(tuple)

                couleurEnnemie = "blanc" if self.couleurPion == "noir" else "noir"

                pieceEnnemies = self.plat.getMatriceByCouleur(couleurEnnemie)

                pieceAllie = self.plat.getMatriceByCouleur(self.couleurPion)

                # Empeche le roi de se déplacer dans une case qui le mettrait en situation d'échec
                self.possibleMoves = self.getPossibleMoves(tuple)

                # Colorie en rouge les déplacements possibles du pion
                for case in self.possibleMoves:
                    self.dict_bouton[case].config(bg="#CD4C4C")

                # Stocke les boutons qui ont été coloriés pour qu'ils puissent être décoloriés plus tard
                self.newEvent.setTrace(self.possibleMoves)

            # Si le joueur ne joue pas la bonne couleur
            else:

                print("C'est aux", "blanc" if self.tourColorDisplay else "noirs", "de jouer")

        # Si le coup précédent était une sélection, on déplace le pion sélectionné à cette nouvelle case
        else:

            # On crée un nouvel évènement de placement.
            self.newEvent = event(str(self.newId), tuple, "place")

            # L'évènement est un event de placement, donc l'évènement juste avant
            # est un évènement d'origine (de click) donc on va chercher l'image
            # contenu en cache dans cet évènement pour l'utiliser ici
            self.image = self.event_log[-1].getCache()

            # On récupère les coordonnées de la case cliquée à l'évènement précédant
            self.former_case = self.event_log[-1].getOrigin()

            # On récupère sa couleur de base (originelle)
            self.former_button_normal_color = self.coul_bouton[self.former_case]

            # Et on lui remet sa couleur de base.
            self.dict_bouton[self.former_case].config(bg=self.former_button_normal_color)

            # On récupère la couleur du pion qui a été sélectionné
            self.couleurPion = self.plat.getCase(self.former_case[0], self.former_case[1]).getCouleur()

            # On remet la couleur de base des cases coloriées précédemment pour montrer les movements possibles
            for traceCase in self.event_log[-1].getTrace():

                self.dict_bouton[traceCase].config(bg=self.coul_bouton[traceCase])

            # Si la case d'arrivée n'est pas vide = Contient un pion
            if self.image:

                possibleMove = self.event_log[-1].getTrace()

                # Si la case cliquée appartient aux mouvements possibles
                if tuple in possibleMove:

                    # Retire l'image du bouton de l'ancienne case
                    self.dict_bouton[self.former_case].config(image="")

                    # On affiche sur le panneau d'historique des coups, le résumé de ce tour
                    if "empty" in self.plat.getCaseTuple(tuple).getName():
                        self.printPanneau(self.former_case, tuple, "move")

                    else:
                        self.printPanneau(self.former_case, tuple, "take")

                    # On déplace le pion dans le plateau
                    self.plat.move(self.former_case, tuple)

                    # Place l'image de l'ancienne case sur la nouvelle
                    self.bouton.config(image=self.image)

                    # On met à jour les affichagues des panneaux de droites
                    self.tourColorDisplay = not self.tourColorDisplay
                    self.textTourStringVar.set("AU TOUR DES BLANCS" if self.tourColorDisplay else "AU TOUR DES NOIRS")
                    self.tourLabel['fg'] = "black" if self.tourColorDisplay else "white"
                    self.tourLabel['bg'] = "white" if self.tourColorDisplay else "black"

                    # On incrémente le numéro du tour et on le met à jour
                    self.tour += 1
                    self.textNbTour.set(str(self.tour))

                # Si la case cliquée n'appartient pas aux cases où le pion présélectionné peut se déplacer
                else:

                    print("Impossible move")

        # On récupère les pions qui mettent en echec ou non les rois adverses
        self.listPionBlackPlayEchec = self.plat.checkEchec("blanc")
        self.listPionWhitePlayEchec = self.plat.checkEchec("noir")

        self.echecTrace = {"whitePlayEchec" : [], "blackPlayEchec" : []}

        # Si il y a echec
        if self.listPionBlackPlayEchec:

            # On colorie en rouge le roi noir
            self.dict_bouton[self.plat.getRoi("blanc")].config(bg="#CD4C4C")

            # On colorie en orange les pions attaquants
            for pionEchec in self.listPionBlackPlayEchec:

                self.dict_bouton[pionEchec].config(bg="#e08f38")

            # On stocke les pions les cases des pions attaquants qui ont été coloriées
            self.echecTrace["blackPlayEchec"] = self.listPionBlackPlayEchec

            # On informe de l'echec sur le panneau d'informations et d'affichage des eches à droite
            self.textAffichage.set("ECHEC")
            self.affichage['fg'] = "white"
            self.affichage['bg'] = "#A02B2B"
            self.whiteEnEchec = True

        # Si il n'y a plus d'echec
        else:

            # On décolorie le roi
            self.original_color = self.coul_bouton[self.plat.getRoi("blanc")]
            self.dict_bouton[self.plat.getRoi("blanc")].config(bg=self.original_color)

            # On décolorie les anciennes cases des pions attaquants
            self.echecTraceToEmpty = self.event_log[-1].getEchecTrace()

            if self.echecTraceToEmpty:

                for pionEchec in self.echecTraceToEmpty["blackPlayEchec"]:

                    # On récupère sa couleur de base (originelle)
                    self.pionEchecOriginalColor = self.coul_bouton[pionEchec]

                    # Et on lui remet sa couleur de base.
                    self.dict_bouton[pionEchec].config(bg=self.pionEchecOriginalColor)

            # On remet le panneau d'informations et d'affichage des eches à droite en mode neutre
            self.textAffichage.set("")
            self.affichage['fg'] = "black"
            self.affichage['bg'] = "#789FDE"

        if self.listPionWhitePlayEchec:

            # On colorie en rouge le roi blanc
            self.dict_bouton[self.plat.getRoi("noir")].config(bg="#CD4C4C")

            # On colorie en orange les pions attaquants
            for pionEchec in self.listPionWhitePlayEchec:

                self.dict_bouton[pionEchec].config(bg="#e08f38")

            # On stocke les pions les cases des pions attaquants qui ont été coloriées
            self.echecTrace["whitePlayEchec"] = self.listPionWhitePlayEchec

            # On informe de l'echec sur le panneau d'informations et d'affichage des eches à droite
            self.textAffichage.set("ECHEC")
            self.affichage['fg'] = "white"
            self.affichage['bg'] = "#A02B2B"
            self.blackEnEchec = True

        # Si il n'y a plus d'echec
        else:

            # On décolorie le roi
            self.original_color = self.coul_bouton[self.plat.getRoi("noir")]
            self.dict_bouton[self.plat.getRoi("noir")].config(bg=self.original_color)

            # On décolorie les anciennes cases des pions attaquants
            self.echecTraceToEmpty = self.event_log[-1].getEchecTrace()

            if self.echecTraceToEmpty:

                for pionEchec in self.echecTraceToEmpty["whitePlayEchec"]:

                    # On récupère sa couleur de base (originelle)
                    self.pionEchecOriginalColor = self.coul_bouton[pionEchec]

                    # Et on lui remet sa couleur de base.
                    self.dict_bouton[pionEchec].config(bg=self.pionEchecOriginalColor)

            # On remet le panneau d'informations et d'affichage des eches à droite en mode neutre
            self.textAffichage.set("")
            self.affichage['fg'] = "black"
            self.affichage['bg'] = "#789FDE"

        # On récupère les moves possibles en cas d'échecs, ou à défaut, le type de l'échec
        checkMateWhiteTestResult = self.plat.checkMate("blanc")
        checkMateBlackTestResult = self.plat.checkMate("noir")

        # =============================================================================================
        # Check echec et mats
        # =============================================================================================

        self.newEventSauveteur = {
            "whiteSaver" : [],
            "blackSaver" : [],
            "whiteSaverTrace" : [],
            "blackSaverTrace" : []
        }

        # White Test Echec ----------------------------------------------------------------------------

        # Si echec et mat, on freeze le jeu et affiche l'echec et mat
        if checkMateWhiteTestResult == "mat":

            self.textAffichage.set("ECHEC ET MAT\nLes Noirs l'emportent")
            self.affichage['fg'] = "black"
            self.affichage['bg'] = "#A02B2B"

            self.freezeGrid()

        # Si des moves pour sauver le roi son possibles
        elif type(checkMateWhiteTestResult) == list:

            listeSauveteurWhite = []
            listeSauveteurWhiteTrace = []

            listeMoveRoiSave = [move for move in checkMateWhiteTestResult]

            # Pour chaque move possible sauvant le roi
            for el in listeMoveRoiSave:

                # On rajoute à la liste de moves possibles si il n'y est pas déjà
                if not el[0] in listeSauveteurWhite:
                    listeSauveteurWhite.append(el[0])

                # On rajoute le move (origin, destination) à la liste des moves possibles
                listeSauveteurWhiteTrace.append(el)

                # Si le pion n'est pas un roi, puisque le roi a déjà été géré
                if self.plat.getCaseTuple(el[0]).getType() != 'roi':

                    # On colorie la pièce qui pourrait sauver le roi en bleu
                    self.dict_bouton[el[0]].config(bg="#5fb1cf")

                    # On colorie le déplacement en vert
                    for move in el[1]:
                        self.dict_bouton[el[1]].config(bg="#31cc55")

            # On stocke le sauveur, et ses mouvements possibles pour plus tard
            self.newEventSauveteur["whiteSaver"] = listeSauveteurWhite
            self.newEventSauveteur["whiteSaverTrace"] = listeSauveteurWhiteTrace

            # On disable les pions/cases/move qui ne peuvent pas sauver le roi pour forcer au sauvetage
            listButtonNotToDisable = []
            for saver in listeSauveteurWhite:
                listButtonNotToDisable.append(saver)

            for move in listeSauveteurWhiteTrace: listButtonNotToDisable.append(move[1])

            roiBlanc = self.plat.getRoi("blanc")
            listButtonNotToDisable.append(roiBlanc)

            # On stocke les boutons/cases/move qui vont être disable dans l'event pour les réactiver plus tard
            self.newEvent.setEnabledButton(listButtonNotToDisable)

            # On désactive les boutons/cases/move
            self.disableButtonInCaseOfEchec(self.dict_bouton, listButtonNotToDisable)

        # S'il n'y a pas d'échecs
        elif checkMateWhiteTestResult == "no-echec":

            # On récupère les sauveurs du roi du move précédant
            self.whiteSaverToEmpty = self.event_log[-1].getSaver()

            if self.whiteSaverToEmpty:

                # On remet aux sauvers précédants leur couleur originelle
                for saver in self.whiteSaverToEmpty["whiteSaver"]:

                    # On récupère sa couleur de base (originelle)
                    self.pionEchecOriginalColor = self.coul_bouton[saver]

                    # Et on lui remet sa couleur de base.
                    self.dict_bouton[saver].config(bg=self.pionEchecOriginalColor)

                # On remet aux moves des sauvers précédants leur couleur originelle
                for saverMove in self.whiteSaverToEmpty["whiteSaverTrace"]:

                    # On récupère sa couleur de base (originelle)
                    self.pionEchecOriginalColor = self.coul_bouton[saverMove[1]]

                    # Et on lui remet sa couleur de base.
                    self.dict_bouton[saverMove[1]].config(bg=self.pionEchecOriginalColor)

            # On réactive tous les boutons
            self.enableAllButtons()

        # Black Test Echec ----------------------------------------------------------------------------

        # Si echec et mat, on freeze le jeu et affiche l'echec et mat
        if checkMateBlackTestResult == "mat":

            self.textAffichage.set("ECHEC ET MAT\nLes Blancs l'emportent")
            self.affichage['fg'] = "black"
            self.affichage['bg'] = "#A02B2B"

            self.freezeGrid()

        # Si des moves pour sauver le roi son possibles
        elif type(checkMateBlackTestResult) == list:

            listeSauveteurBlack = []
            listeSauveteurBlackTrace = []

            listeMoveRoiSave = [move for move in checkMateBlackTestResult]

            # Pour chaque move possible sauvant le roi
            for el in listeMoveRoiSave:

                # On rajoute à la liste de moves possibles si il n'y est pas déjà
                if el[0] not in listeSauveteurBlack:
                    listeSauveteurBlack.append(el[0])

                # On rajoute le move (origin, destination) à la liste des moves possibles
                listeSauveteurBlackTrace.append(el)

                # Si le pion n'est pas un roi, puisque le roi a déjà été géré
                if self.plat.getCaseTuple(el[0]).getType() != 'roi':

                    # On colorie la pièce qui pourrait sauver le roi en bleu
                    self.dict_bouton[el[0]].config(bg="#5fb1cf")

                    # On colorie le déplacement en vert
                    for move in el[1]:
                        self.dict_bouton[el[1]].config(bg="#31cc55")

            # On stocke le sauveur, et ses mouvements possibles pour plus tard
            self.newEventSauveteur["blackSaver"] = listeSauveteurBlack
            self.newEventSauveteur["blackSaverTrace"] = listeSauveteurBlackTrace

            # On disable les pions/cases/move qui ne peuvent pas sauver le roi pour forcer au sauvetage
            listButtonNotToDisable = []
            for saver in listeSauveteurBlack:
                listButtonNotToDisable.append(saver)

            for move in listeSauveteurBlackTrace: listButtonNotToDisable.append(move[1])

            roiNoir = self.plat.getRoi("noir")
            listButtonNotToDisable.append(roiNoir)

            # On stocke les boutons/cases/move qui vont être disable dans l'event pour les réactiver plus tard
            self.newEvent.setEnabledButton(listButtonNotToDisable)

            # On désactive les boutons/cases/move
            self.disableButtonInCaseOfEchec(self.dict_bouton, listButtonNotToDisable)

        # S'il n'y a pas d'échecs
        elif checkMateBlackTestResult == "no-echec":

            # On récupère les sauveurs du roi du move précédant
            self.blackSaverToEmpty = self.event_log[-1].getSaver()

            if self.blackSaverToEmpty:

                # On remet aux sauvers précédants leur couleur originelle
                for saver in self.blackSaverToEmpty["blackSaver"]:

                    # On récupère sa couleur de base (originelle)
                    self.pionEchecOriginalColor = self.coul_bouton[saver]

                    # Et on lui remet sa couleur de base.
                    self.dict_bouton[saver].config(bg=self.pionEchecOriginalColor)

                # On remet aux moves des sauvers précédants leur couleur originelle
                for saverMove in self.blackSaverToEmpty["blackSaverTrace"]:

                    # On récupère sa couleur de base (originelle)
                    self.pionEchecOriginalColor = self.coul_bouton[saverMove[1]]

                    # Et on lui remet sa couleur de base.
                    self.dict_bouton[saverMove[1]].config(bg=self.pionEchecOriginalColor)

            # On réactive tous les boutons
            self.enableAllButtons()

        # On ajout les sauveteurs eventuels et leurs move au nouvel évènement
        self.newEvent.setSaver(self.newEventSauveteur)
        self.newEvent.setEchecTrace(self.echecTrace)
        self.newEvent.apercu()

        # On rajoute l'evènement à la liste des évènements
        self.event_log.append(self.newEvent)

        # On incrémente la chaine qui sert à créer le nom/id des évènements pour le prochain
        # évènement. Toujours de x + 1
        self.id += 1


    def moveIA(self, tuple):
        """
        FONCTION UNIQUEMENT POUR L'IA
        Fonction gérant l'affichage, les calculs des règles du jeu, l'état du jeu, les mouvements, etc...
        Le jeu se met à jour à chaque appel de cette fonction

        :param tuple: Coordonnées de la case qui a été cliquée
        """

        # Id du nouvel évènement
        self.newId = self.id

        # Bouton qui a été cliqué
        self.bouton = self.dict_bouton[(tuple[0], tuple[1])]

        # On récupère la couleur du pion à jouer
        self.couleurPion = self.plat.getCase(tuple[0], tuple[1]).getCouleur()

        # Si le clic précédant étant un placement, alors celui-ci sera une sélection de pion
        if self.event_log[-1].getAction() != "click":

            # Si c'est la bonne couleur qui est jouée
            if self.tourCouleurVerificateur(self.plat.getCase(tuple[0], tuple[1]).getCouleur(),
                                            self.tourColorDisplay):

                # On crée un nouvel évènement de click simple
                self.newEvent = event(str(self.newId), tuple, "click")

                # Comme c'est un click et non un place, ça signifie que ce bouton est
                # l'origine du mouvement, donc contient le pion à bouger
                if self.plat.getCase(tuple[0], tuple[1]):
                    self.newEvent.setCache(self.plat.getCase(tuple[0], tuple[1]).getImage())

                # Colorie la case en gris pour indiquer l'origine du mouvement
                self.bouton.config(bg="#aaaaaa")

                # Déplacement possibles simple du pion qui a été cliqué
                self.possibleMoves = self.getPossibleMoves(tuple)

                # Colorie en rouge les déplacements possibles du pion
                for case in self.possibleMoves:
                    self.dict_bouton[case].config(bg="#CD4C4C")

                # Stocke les boutons qui ont été coloriés pour qu'ils puissent être décoloriés plus tard
                self.newEvent.setTrace(self.possibleMoves)

            # Si le joueur ne joue pas la bonne couleur
            else:

                print("C'est aux", "blanc" if self.tourColorDisplay else "noirs", "de jouer")

        # Si le coup précédent était une sélection, on déplace le pion sélectionné à cette nouvelle case
        else:

            # On crée un nouvel évènement de placement.
            self.newEvent = event(str(self.newId), tuple, "place")

            # L'évènement est un event de placement, donc l'évènement juste avant
            # est un évènement d'origine (de click) donc on va chercher l'image
            # contenu en cache dans cet évènement pour l'utiliser ici
            self.image = self.event_log[-1].getCache()

            # On récupère les coordonnées de la case cliquée à l'évènement précédant
            self.former_case = self.event_log[-1].getOrigin()

            # On récupère sa couleur de base (originelle)
            self.former_button_normal_color = self.coul_bouton[self.former_case]

            # Et on lui remet sa couleur de base.
            self.dict_bouton[self.former_case].config(bg=self.former_button_normal_color)

            # On récupère la couleur du pion qui a été sélectionné
            self.couleurPion = self.plat.getCase(self.former_case[0], self.former_case[1]).getCouleur()

            # On remet la couleur de base des cases coloriées précédemment pour montrer les movements possibles
            for traceCase in self.event_log[-1].getTrace():

                self.dict_bouton[traceCase].config(bg=self.coul_bouton[traceCase])

            # Si la case d'arrivée n'est pas vide = Contient un pion
            if self.image:

                possibleMove = self.event_log[-1].getTrace()

                # Si la case cliquée appartient aux mouvements possibles
                if tuple in possibleMove:

                    # Retire l'image du bouton de l'ancienne case
                    self.dict_bouton[self.former_case].config(image="")

                    # On affiche sur le panneau d'historique des coups, le résumé de ce tour
                    if "empty" in self.plat.getCaseTuple(tuple).getName():
                        self.printPanneau(self.former_case, tuple, "move")

                    else:
                        self.printPanneau(self.former_case, tuple, "take")

                    # On déplace le pion dans le plateau
                    self.plat.move(self.former_case, tuple)

                    # Place l'image de l'ancienne case sur la nouvelle
                    self.bouton.config(image=self.image)

                    self.tourColorDisplay = not self.tourColorDisplay
                    self.textTourStringVar.set("AU TOUR DES BLANCS" if self.tourColorDisplay else "AU TOUR DES NOIRS")
                    self.tourLabel['fg'] = "black" if self.tourColorDisplay else "white"
                    self.tourLabel['bg'] = "white" if self.tourColorDisplay else "black"

                    # On incrémente le numéro du tour et on le met à jour
                    self.tour += 1
                    self.textNbTour.set(str(self.tour))

                # Si la case cliquée n'appartient pas aux cases où le pion présélectionné peut se déplacer
                else:

                    print("Impossible move")

        # On récupère les pions qui mettent en echec ou non les rois adverses
        self.listPionBlackPlayEchec = self.plat.checkEchec("blanc")
        self.listPionWhitePlayEchec = self.plat.checkEchec("noir")

        self.echecTrace = {"whitePlayEchec": [], "blackPlayEchec": []}

        # Si il y a echec
        if self.listPionBlackPlayEchec:

            # On colorie en rouge le roi noir
            self.dict_bouton[self.plat.getRoi("blanc")].config(bg="#CD4C4C")

            # On colorie en orange les pions attaquants
            for pionEchec in self.listPionBlackPlayEchec:
                self.dict_bouton[pionEchec].config(bg="#e08f38")

            # On stocke les pions les cases des pions attaquants qui ont été coloriées
            self.echecTrace["blackPlayEchec"] = self.listPionBlackPlayEchec

            # On informe de l'echec sur le panneau d'informations et d'affichage des eches à droite
            self.textAffichage.set("ECHEC")
            self.affichage['fg'] = "white"
            self.affichage['bg'] = "#A02B2B"
            self.whiteEnEchec = True

        # Si il n'y a plus d'echec
        else:

            # On décolorie le roi
            self.original_color = self.coul_bouton[self.plat.getRoi("blanc")]
            self.dict_bouton[self.plat.getRoi("blanc")].config(bg=self.original_color)

            # On décolorie les anciennes cases des pions attaquants
            self.echecTraceToEmpty = self.event_log[-1].getEchecTrace()

            if self.echecTraceToEmpty:

                for pionEchec in self.echecTraceToEmpty["blackPlayEchec"]:
                    # On récupère sa couleur de base (originelle)
                    self.pionEchecOriginalColor = self.coul_bouton[pionEchec]

                    # Et on lui remet sa couleur de base.
                    self.dict_bouton[pionEchec].config(bg=self.pionEchecOriginalColor)

            # On remet le panneau d'informations et d'affichage des eches à droite en mode neutre
            self.textAffichage.set("")
            self.affichage['fg'] = "black"
            self.affichage['bg'] = "#789FDE"

        if self.listPionWhitePlayEchec:

            # On colorie en rouge le roi blanc
            self.dict_bouton[self.plat.getRoi("noir")].config(bg="#CD4C4C")

            # On colorie en orange les pions attaquants
            for pionEchec in self.listPionWhitePlayEchec:
                self.dict_bouton[pionEchec].config(bg="#e08f38")

            # On stocke les pions les cases des pions attaquants qui ont été coloriées
            self.echecTrace["whitePlayEchec"] = self.listPionWhitePlayEchec

            # On informe de l'echec sur le panneau d'informations et d'affichage des eches à droite
            self.textAffichage.set("ECHEC")
            self.affichage['fg'] = "white"
            self.affichage['bg'] = "#A02B2B"
            self.blackEnEchec = True

        # Si il n'y a plus d'echec
        else:

            # On décolorie le roi
            self.original_color = self.coul_bouton[self.plat.getRoi("noir")]
            self.dict_bouton[self.plat.getRoi("noir")].config(bg=self.original_color)

            # On décolorie les anciennes cases des pions attaquants
            self.echecTraceToEmpty = self.event_log[-1].getEchecTrace()

            if self.echecTraceToEmpty:

                for pionEchec in self.echecTraceToEmpty["whitePlayEchec"]:

                    # On récupère sa couleur de base (originelle)
                    self.pionEchecOriginalColor = self.coul_bouton[pionEchec]

                    # Et on lui remet sa couleur de base.
                    self.dict_bouton[pionEchec].config(bg=self.pionEchecOriginalColor)

            # On remet le panneau d'informations et d'affichage des eches à droite en mode neutre
            self.textAffichage.set("")
            self.affichage['fg'] = "black"
            self.affichage['bg'] = "#789FDE"

        # On récupère les moves possibles en cas d'échecs, ou à défaut, le type de l'échec
        checkMateWhiteTestResult = self.plat.checkMate("blanc")
        checkMateBlackTestResult = self.plat.checkMate("noir")

        # =============================================================================================
        # Check echec et mats
        # =============================================================================================

        self.newEventSauveteur = {
            "whiteSaver": [],
            "blackSaver": [],
            "whiteSaverTrace": [],
            "blackSaverTrace": []
        }

        # White Test Echec ----------------------------------------------------------------------------

        # Si echec et mat, on freeze le jeu et affiche l'echec et mat
        if checkMateWhiteTestResult == "mat":

            self.textAffichage.set("ECHEC ET MAT\nLes Noirs l'emportent")
            self.affichage['fg'] = "black"
            self.affichage['bg'] = "#A02B2B"

            self.freezeGrid()

        # Si des moves pour sauver le roi son possibles
        elif type(checkMateWhiteTestResult) == list:

            listeSauveteurWhite = []
            listeSauveteurWhiteTrace = []

            listeMoveRoiSave = [move for move in checkMateWhiteTestResult]

            # Pour chaque move possible sauvant le roi
            for el in listeMoveRoiSave:

                # On rajoute à la liste de moves possibles si il n'y est pas déjà
                if el[0] not in listeSauveteurWhite:
                    listeSauveteurWhite.append(el[0])

                # On rajoute le move (origin, destination) à la liste des moves possibles
                listeSauveteurWhiteTrace.append(el)


                # Si le pion n'est pas un roi, puisque le roi a déjà été géré
                if self.plat.getCaseTuple(el[0]).getType() != 'roi':

                    # On colorie la pièce qui pourrait sauver le roi en bleu
                    self.dict_bouton[el[0]].config(bg="#5fb1cf")

                    # On colorie le déplacement en vert
                    for move in el[1]:
                        self.dict_bouton[el[1]].config(bg="#31cc55")

            # On stocke le sauveur, et ses mouvements possibles pour plus tard
            self.newEventSauveteur["whiteSaver"] = listeSauveteurWhite
            self.newEventSauveteur["whiteSaverTrace"] = listeSauveteurWhiteTrace

            # On disable les pions/cases/move qui ne peuvent pas sauver le roi pour forcer au sauvetage
            listButtonNotToDisable = []
            for saver in listeSauveteurWhite:
                listButtonNotToDisable.append(saver)

            for move in listeSauveteurWhiteTrace: listButtonNotToDisable.append(move[1])

            roiBlanc = self.plat.getRoi("blanc")
            listButtonNotToDisable.append(roiBlanc)

            # On stocke les boutons/cases/move qui vont être disable dans l'event pour les réactiver plus tard
            self.newEvent.setEnabledButton(listButtonNotToDisable)

            # On désactive les boutons/cases/move
            self.disableButtonInCaseOfEchec(self.dict_bouton, listButtonNotToDisable)

        # S'il n'y a pas d'échecs
        elif checkMateWhiteTestResult == "no-echec":

            # On récupère les sauveurs du roi du move précédant
            self.whiteSaverToEmpty = self.event_log[-1].getSaver()

            if self.whiteSaverToEmpty:

                # On remet aux sauvers précédants leur couleur originelle
                for saver in self.whiteSaverToEmpty["whiteSaver"]:

                    # On récupère sa couleur de base (originelle)
                    self.pionEchecOriginalColor = self.coul_bouton[saver]

                    # Et on lui remet sa couleur de base.
                    self.dict_bouton[saver].config(bg=self.pionEchecOriginalColor)

                # On remet aux moves des sauvers précédants leur couleur originelle
                for saverMove in self.whiteSaverToEmpty["whiteSaverTrace"]:

                    # On récupère sa couleur de base (originelle)
                    self.pionEchecOriginalColor = self.coul_bouton[saverMove[1]]

                    # Et on lui remet sa couleur de base.
                    self.dict_bouton[saverMove[1]].config(bg=self.pionEchecOriginalColor)

            # On réactive tous les boutons
            self.enableAllButtons()

        # Black Test Echec ----------------------------------------------------------------------------

        # Si echec et mat, on freeze le jeu et affiche l'echec et mat
        if checkMateBlackTestResult == "mat":

            self.textAffichage.set("ECHEC ET MAT\nLes Blancs l'emportent")
            self.affichage['fg'] = "black"
            self.affichage['bg'] = "#A02B2B"

            self.freezeGrid()

        # Si des moves pour sauver le roi son possibles
        elif type(checkMateBlackTestResult) == list:

            listeSauveteurBlack = []
            listeSauveteurBlackTrace = []

            listeMoveRoiSave = [move for move in checkMateBlackTestResult]

            # Pour chaque move possible sauvant le roi
            for el in listeMoveRoiSave:

                # On rajoute à la liste de moves possibles si il n'y est pas déjà
                if el[0] not in listeSauveteurBlack:
                    listeSauveteurBlack.append(el[0])

                # On rajoute le move (origin, destination) à la liste des moves possibles
                listeSauveteurBlackTrace.append(el)

                # Si le pion n'est pas un roi, puisque le roi a déjà été géré
                if self.plat.getCaseTuple(el[0]).getType() != 'roi':

                    # On colorie la pièce qui pourrait sauver le roi en bleu
                    self.dict_bouton[el[0]].config(bg="#5fb1cf")

                    # On colorie le déplacement en vert
                    for move in el[1]:
                        self.dict_bouton[el[1]].config(bg="#31cc55")

            # On stocke le sauveur, et ses mouvements possibles pour plus tard
            self.newEventSauveteur["blackSaver"] = listeSauveteurBlack
            self.newEventSauveteur["blackSaverTrace"] = listeSauveteurBlackTrace

            # On disable les pions/cases/move qui ne peuvent pas sauver le roi pour forcer au sauvetage
            listButtonNotToDisable = []
            for saver in listeSauveteurBlack:
                listButtonNotToDisable.append(saver)

            for move in listeSauveteurBlackTrace: listButtonNotToDisable.append(move[1])

            roiNoir = self.plat.getRoi("noir")
            listButtonNotToDisable.append(roiNoir)

            # On stocke les boutons/cases/move qui vont être disable dans l'event pour les réactiver plus tard
            self.newEvent.setEnabledButton(listButtonNotToDisable)

            # On désactive les boutons/cases/move
            self.disableButtonInCaseOfEchec(self.dict_bouton, listButtonNotToDisable)

        # S'il n'y a pas d'échecs
        elif checkMateBlackTestResult == "no-echec":

            # On récupère les sauveurs du roi du move précédant
            self.blackSaverToEmpty = self.event_log[-1].getSaver()

            if self.blackSaverToEmpty:

                # On remet aux sauvers précédants leur couleur originelle
                for saver in self.blackSaverToEmpty["blackSaver"]:

                    # On récupère sa couleur de base (originelle)
                    self.pionEchecOriginalColor = self.coul_bouton[saver]

                    # Et on lui remet sa couleur de base.
                    self.dict_bouton[saver].config(bg=self.pionEchecOriginalColor)

                # On remet aux moves des sauvers précédants leur couleur originelle
                for saverMove in self.blackSaverToEmpty["blackSaverTrace"]:
                    # On récupère sa couleur de base (originelle)
                    self.pionEchecOriginalColor = self.coul_bouton[saverMove[1]]

                    # Et on lui remet sa couleur de base.
                    self.dict_bouton[saverMove[1]].config(bg=self.pionEchecOriginalColor)

            # On réactive tous les boutons
            self.enableAllButtons()

        # On ajout les sauveteurs eventuels et leurs move au nouvel évènement
        self.newEvent.setSaver(self.newEventSauveteur)
        self.newEvent.setEchecTrace(self.echecTrace)
        self.newEvent.apercu()

        # On rajoute l'evènement à la liste des évènements
        self.event_log.append(self.newEvent)

        # On incrémente la chaine qui sert à créer le nom/id des évènements pour le prochain
        # évènement. Toujours de x + 1
        self.id += 1


    def getPossibleMoves(self, tuple):
        """
        Fonction commune à l'IA et au joueur
        Permet de récupérer les déplacements possibles des pions.
        NE SERT PAS EN CAS D'ECHEC, en cas d'échec, les déplacements possibles sont
        calculés par la fonction move(), au moment du test de l'échec.

        Args:
            tuple: pion duquel l'on veut récupérer les déplacements possibles
        """

        couleurPion = self.plat.getCaseTuple(tuple).getCouleur()
        possibleMoves = self.plat.getPath(tuple)
        couleurEnnemie = "blanc" if couleurPion == "noir" else "noir"
        pieceEnnemies = self.plat.getMatriceByCouleur(couleurEnnemie)
        pieceAllie = self.plat.getMatriceByCouleur(couleurPion)

        # Empeche le roi de se déplacer dans une case qui le mettrait en situation d'échec
        if self.plat.getCaseTuple(tuple).getType() == "roi":

            zoneEnEchec = []

            for piece in pieceEnnemies:

                zoneEnEchec += self.plat.getPath(piece, pion=True)

            for move in zoneEnEchec:

                # Si l'un des moves possibles du roi est sur le chemin d'un enemi, on le retire
                if move in possibleMoves:
                    possibleMoves.remove(move)

        # Si la pièce n'est pas un roi
        else:

            # Empeche une piece de bouger si cela met son roi en echec
            pieceAttaque = []
            roi = self.plat.getRoi(couleurPion)
            safeType = ["cavalier", "pion"]

            # Pour chaque pièce ennemie
            for piece in pieceEnnemies:

                # Si ce n'est ni un cavalier, ni un pion
                if self.plat.getCaseTuple(piece).getType() not in safeType:

                    allieSurLeChemin = []

                    # Si il y a un allié sur le chemin on l'ajoute à une liste d'allié sur le chemin
                    for allie in pieceAllie:

                        if allie in self.plat.getCasePathFinding(roi, piece, True):
                            allieSurLeChemin.append(allie)

                    # Et s'il y en a
                    if len(allieSurLeChemin) <= 2:

                        # Si le roi est le roi est en danger et qu'un pion est peut s'interposer, on le fait
                        if roi in self.plat.getCasePathFinding(roi, piece, True):

                            if tuple in self.plat.getPath(piece):

                                if tuple in self.plat.getCasePathFinding(roi, piece, True):
                                    possibleMoves.clear()
                                    break

        return possibleMoves


    def getMoveIA(self, tuple):
        """
        Fonction récupérant ou calculant les moves possibles/les meilleurs moves à faire

        :param tuple: Coordonnées du pion qui doit jouer
        """

        # Score gagné si ces pions sont pris
        scoreTable = {"tour": 3, "cavalier": 2, "fou": 3, "reine": 10, "pion": 1, "empty": 0, "roi": 15}

        blackSaver = self.event_log[-1].getSaver()["blackSaver"]
        blackSaverTrace = self.event_log[-1].getSaver()["blackSaverTrace"]
        playsRdNb = 1

        # S'il y a pas de blackSaver ET DONC Echec
        if not blackSaver:

            listPLays = {}
            listPionsIA = self.plat.getMatriceByCouleur("noir")
            iaMoveNb = 0

            # Pour tous les pions de l'IA
            for pionIA in listPionsIA:

                movePionIa = self.getPossibleMoves(pionIA)

                # Si ce n'est pas un pion
                if self.plat.getCaseTuple(pionIA).getType() != "roi":

                    # On leur donne un id, et un score calculé en fonction de la pièce à destination
                    # Qui peut potentiellement être prise, et on stocke le tout
                    for move in movePionIa:

                        scoreMove = scoreTable[self.plat.getCaseTuple(move).getType()]
                        listPLays[playsRdNb] = [pionIA, move, scoreMove]
                        playsRdNb += 1

                # Si c'est un roi
                else:

                    # Si le roi ne peut pas bouger
                    if len(movePionIa) == 0:

                        listePieceEnnemie = self.plat.getMatriceByCouleur("blanc")
                        listeMovePieceEnnemie = []

                        # On récupère la liste de toutes les cases sur le chemin des ennemis
                        for pieceEnnemie in listePieceEnnemie:
                            for moveEnnemie in self.plat.getPath(pieceEnnemie, pion=True):
                                if moveEnnemie not in listeMovePieceEnnemie:
                                    listeMovePieceEnnemie.append(moveEnnemie)

                        # On vérifie si toutes les cases autour du roi sont sur le trajet d'ennemis ou non
                        canMove = False
                        for moveRoi in self.plat.getPath(pionIA, takeFriends=True):
                            if not moveRoi in listeMovePieceEnnemie:
                                canMove = True

                        # Si le roi ne peut pas bouger, c'est considéré comme un match nul
                        # Mais ici on le considérera comme un echec et mat
                        if not canMove:

                            self.textAffichage.set("ECHEC ET MAT\nLes Blancs l'emportent")
                            self.affichage['fg'] = "black"
                            self.affichage['bg'] = "#A02B2B"

                            self.freezeGrid()

                    # Si le roi peut bouger alors on stocke ses déplacements possibles
                    else:

                        for move in movePionIa:

                            scoreMove = scoreTable[self.plat.getCaseTuple(move).getType()]
                            listPLays[playsRdNb] = [pionIA, move, scoreMove]
                            playsRdNb += 1

            # Si la difficulté du jeu est en HARD, on calcule le score d'un move, en fonction du score
            # de la prise, et du score du preneur, l'idée étant de prendre le pion le plus cher avec son
            # pion le moins cher
            if self.difficulty == "hard":

                max = 0
                for nbMove, move in listPLays.items():
                   if move[2] >= max:
                       max = move[2]

                listMove = {}
                newNbMove = 1
                for nbMove, move in listPLays.items():
                    if move[2] == max:
                        listMove[newNbMove] = move
                        newNbMove += 1

                min = 11
                for nbMove, move in listMove.items():
                    scoreDeCeMove = scoreTable[self.plat.getCaseTuple(move[0]).getType()]
                    if scoreDeCeMove <= min:
                        min = scoreDeCeMove

                listMoveDefinitive = {}
                newNbMove = 1
                for nbMove, move in listMove.items():
                    scoreOrigin = scoreTable[self.plat.getCaseTuple(move[0]).getType()]
                    if scoreOrigin == min:
                        listMoveDefinitive[newNbMove] = move
                        newNbMove += 1

                # On retourne le move aléatoirement parmi les moves les plus avantageux
                iaMoveNb = randint(1, newNbMove-1)
                return listMoveDefinitive[iaMoveNb]


            elif self.difficulty == "easy":

                # On retourne le move aléatoirement
                iaMoveNb = randint(1, playsRdNb-1)
                return listPLays[iaMoveNb]


        else:

            # On retourne le move
            iaMoveNb = randint(0, len(blackSaverTrace)-1)
            return blackSaverTrace[iaMoveNb]


    def printPanneau(self, origin: tuple, target: tuple, type: str):
        """
        Fonction qui affiche sur le panneau d'historique le résumé des tours

        :param origin: pièce d'origine du move
        :param target: pièce de destination du move
        :param type: type du move, "take" ou "move"
        """

        self.historiquePanneau["state"] = "normal"

        pionOrigin = self.plat.getCaseTuple(origin)
        pionTarget = self.plat.getCaseTuple(target)

        txt = f"Tour : {self.tour} - {pionOrigin.getCouleur().upper()}\n"

        if type == "take":
            txt += f"{pionOrigin.getType()} {pionOrigin.getCouleur()} en {origin} prends "
            txt += f"{pionTarget.getType()} {pionTarget.getCouleur()} en {target}\n\n"

        elif type == "move":
            txt += f"{pionOrigin.getType()} {pionOrigin.getCouleur()} en {origin} va en {target}\n\n"

        # Pour de futures évolutions
        elif type == "echec":
            pass

        elif type == "mat":
            pass

        self.historiquePanneau.insert(END, txt)
        self.historiquePanneau["state"] = "disabled"
        self.historiquePanneau.see("end")


    def tourCouleurVerificateur(self, couleur: str, boolean: bool) -> bool:
        """
        Fonction vérifiant que la couleur donnée est bien celle du tour

        :param couleur: couleur donnée
        :param boolean: couleur du jeu, matérialisée par un Boolean : True si noir, False si blanc
        :return:
        """

        if (couleur == "blanc" or couleur == None) and boolean:

            return True

        elif (couleur == "noir" or couleur == None) and not boolean:

            return True

        else:

            return False


    def disableButtonInCaseOfEchec(self, allButtonDict: dict, buttonNotToDisableList: list):
        """
        Fonction qui désactive tous les boutons d'un dictionnaire donné sauf ceux spécifiés

        :param allButtonDict: Dictionnaire de tous les boutons
        :param buttonNotToDisableList: liste des coordonnées des boutons à ne pas désactiver
        """

        for coords, button in allButtonDict.items():

            if coords not in buttonNotToDisableList:

                button['state'] = DISABLED


    def disableButtons(self, dict: dict, buttonsToDisable: list):
        """
        Fonction qui désactive tous les boutons donnés

        :param dict: Dictionnaire de tous les boutons
        :param buttonsToDisable: liste des coordonnées des boutons à désactiver
        """

        for coords, button in dict.items():

            if coords in buttonsToDisable:

                button['state'] = DISABLED


    def enableAllButtons(self):
        """
        Active tous les boutons
        """

        for coords, button in self.dict_bouton.items():

            button['state'] = NORMAL

    def diableAllButtons(self):
        """
        Désactive tous les boutons
        """

        for coords, button in self.dict_bouton.items():
            button['state'] = DISABLED


    def freezeGrid(self):
        """
        Retire toutes les commandes des boutons, ce qui a pour effet de rendre le plateau non clickable.
        Et donc non jouable
        """

        for coords, button in self.dict_bouton.items():

            button['command'] = self.freezeButton


    def freezeButton(self):
        # pass volontaire, permet de rajouter une commande null aux boutons
        # pour que l'on puisse les freeze
        pass


    def restart(self):
        """
        Handler de l'event .quit(), qui redémarre la game
        """

        self.on_closing()
        self.parent.quit()


    def on_closing(self):
        """
        Handler de l'event .destroy(), qui supprime la fenêtre de jeu
        """

        self.parent.destroy()


class initGame(Frame):
    """
    Classe gérant l'initialisation du jeu d'échec initPlateau
    """

    def __init__(self, parent):
        """
        Classe gérant l'initialisation du jeu d'échec initPlateau

        :param parent: Racine Tkinter
        """

        # On initialise cette fenêtre sur la racine donnée @Frame
        Frame.__init__(self, parent)

        # Root window
        self.parent = parent
        parent.resizable(False, False)

        # Valeur indépendantes
        self.size = 600

        # Protocol Handler
        parent.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Fenetre sur laquelle on placera tous les composants
        self.parent.geometry(str(self.size) + "x" + str(self.size))

        # Initialisation de l'interface graphique qui affichera la page d'initialisation
        self.createIntroGui()


    def createIntroGui(self):
        """
        Fonction créant la fenêtre de sélection et d'initialisation des modes de jeu du jeu d'échec
        """

        # Chargement de l'image de fond
        self.background_image = PhotoImage(file='../res/intro_background.png')

        # Echiquier, Canvas sur lequel placer les boutons, lui-meme placé sur la fenêtre fen.
        self.mainCanvas = Canvas(self.parent, width=self.size, height=self.size)
        self.mainCanvas.pack(side=LEFT)
        self.mainCanvas.create_image(0, 0, image=self.background_image, anchor='nw')

        # Bouton lançant une game de PVP 1 contre 1
        self.startPVPGameButton = Button(self.mainCanvas, text="START A PVP GAME", width=20, height=3, command=self.startPVPGame)
        self.startPVPGameButton['fg'] = "white"
        self.startPVPGameButton['bg'] = "#000000"
        self.startPVPGameButton['borderwidth'] = "2"
        self.startPVPGameButton['relief'] = "raised"
        self.startPVPGameButton.place(x=230, y=260)

        # Bouton lançant une game de PVE contre une IA Facile
        self.startPVEGameEasyButton = Button(self.mainCanvas, text="EASY IA", width=20, height=3, command=self.startPVEGameEasy)
        self.startPVEGameEasyButton['borderwidth'] = 3
        self.startPVEGameEasyButton['fg'] = "white"
        self.startPVEGameEasyButton['bg'] = "#000000"
        self.startPVEGameEasyButton['borderwidth'] = "2"
        self.startPVEGameEasyButton['relief'] = "raised"
        self.startPVEGameEasyButton.place(x=230, y=330)

        # Bouton lançant une game de PVE contre une IA Difficile
        self.startPVEGameHardButton = Button(self.mainCanvas, text="JIHAD IA", width=20, height=3, command=self.startPVEGameHard)
        self.startPVEGameHardButton['borderwidth'] = 3
        self.startPVEGameHardButton['fg'] = "white"
        self.startPVEGameHardButton['bg'] = "#000000"
        self.startPVEGameHardButton['borderwidth'] = "2"
        self.startPVEGameHardButton['relief'] = "raised"
        self.startPVEGameHardButton.place(x=230, y=400)

        # Bouton pour reprendre une célèbre game en pleins cours, contre une IA Difficile
        self.resumeGameButton = Button(self.mainCanvas, text="RESUME A SPECIAL GAME", width=20, height=3, command=self.resumeGame)
        self.resumeGameButton['borderwidth'] = 3
        self.resumeGameButton['fg'] = "white"
        self.resumeGameButton['bg'] = "#000000"
        self.resumeGameButton['borderwidth'] = "2"
        self.resumeGameButton['relief'] = "raised"
        self.resumeGameButton.place(x=230, y=470)


    def startPVPGame(self):
        """
        Fonction lançant une partie d'échec avec sa fenètre
            - En 1 VS 1
            - Placement des pions classics
        """

        while running:
            newWindow = Toplevel(rootGame)
            game = initPlateau(newWindow, "pvp", "classic")
            game.mainloop()


    def startPVEGameEasy(self):
        """
        Fonction lançant une partie d'échec avec sa fenètre
            - En 1 VSIA
            - IA Facile
            - Placement des pions classics
        """

        while running:
            newWindow = Toplevel(rootGame)
            game = initPlateau(newWindow, "ia", "classic", "easy")
            game.mainloop()


    def startPVEGameHard(self):
        """
        Fonction lançant une partie d'échec avec sa fenètre
            - En 1 VS IA
            - IA Difficile
            - Placement des pions classics
        """

        while running:
            newWindow = Toplevel(rootGame)
            game = initPlateau(newWindow, "ia", "classic", "hard")
            game.mainloop()


    def resumeGame(self):
        """
        Fonction lançant une partie d'échec avec sa fenètre
            - En 1 VS IA
            - IA Difficile
            - Placement des pions récupérés d'une célèbre partie en cours
        """

        while running:
            newWindow = Toplevel(rootGame)
            game = initPlateau(newWindow, "ia", "other", "hard")
            game.mainloop()


    def on_closing(self):
        """
        Handler de l'event .destroy(), qui supprime la fenêtre de jeu
        """

        self.parent.destroy()


if __name__ == '__main__':

    rootGame = Tk(className=" Echec The VideoGame by Hideo Kojima")
    intro = initGame(rootGame)
    intro.mainloop()

