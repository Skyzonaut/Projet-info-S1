def move(self, tuple):
	self.playIA("noir")
	self.newId = self.id

	self.bouton = self.dict_bouton[(tuple[0], tuple[1])]

	self.couleurPion = ""

	if self.event_log[-1].getAction() != "click":

		if self.tourCouleurVerificateur(self.plat.getCase(tuple[0], tuple[1]).getCouleur(), self.tourColorDisplay):

			# On crée un nouvel évènement de click simple
			self.newEvent = event(str(self.newId), tuple, "click")

			# On récupère la couleur du pion à jouer
			self.couleurPion = self.plat.getCase(tuple[0], tuple[1]).getCouleur()

			# Comme c'est un click et non un place, ça signifie que ce bouton est
			# l'origine du mouvement, donc contient le pion à bouger
			if self.plat.getCase(tuple[0], tuple[1]):
				self.newEvent.setCache(self.plat.getCase(tuple[0], tuple[1]).getImage())

			# Colorie la case en gris pour indiquer l'origine du mouvement
			self.bouton.config(bg="#aaaaaa")

			self.possibleMoves = self.plat.getPath(tuple)

			couleurEnnemie = "blanc" if self.couleurPion == "noir" else "noir"

			pieceEnnemies = self.plat.getMatriceByCouleur(couleurEnnemie)

			pieceAllie = self.plat.getMatriceByCouleur(self.couleurPion)

			# Empeche le roi de se déplacer dans une case qui le mettrait en situation d'échec
			if self.plat.getCaseTuple(tuple).getType() == "roi":

				zoneEnEchec = []

				for piece in pieceEnnemies:
					# zoneEnEchec += self.plat.getPath(piece, pion=True)
					zoneEnEchec += self.plat.getPath(piece, pion=True)

				for move in zoneEnEchec:

					if move in self.possibleMoves:
						self.possibleMoves.remove(move)

			else:

				# Empeche une piece de bouger si cela met son roi en echec
				pieceAttaque = []
				roi = self.plat.getRoi(self.couleurPion)

				for piece in pieceEnnemies:

					allieSurLeChemin = []

					for allie in pieceAllie:

						if allie in self.plat.getCasePathFinding(roi, piece, True):
							allieSurLeChemin.append(allie)

					if len(allieSurLeChemin) <= 2:

						if roi in self.plat.getCasePathFinding(roi, piece, True):

							if tuple in self.plat.getPath(piece):

								if tuple in self.plat.getCasePathFinding(roi, piece, True):
									self.possibleMoves.clear()
									break

			for case in self.possibleMoves:
				self.dict_bouton[case].config(bg="#CD4C4C")

			self.newEvent.setTrace(self.possibleMoves)

		else:

			print("C'est aux", "blanc" if self.tourColorDisplay else "noirs", "de jouer")

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

		for traceCase in self.event_log[-1].getTrace():
			self.dict_bouton[traceCase].config(bg=self.coul_bouton[traceCase])

		if self.image:

			# possibleMove = self.plat.getPath(self.former_case)
			possibleMove = self.event_log[-1].getTrace()

			if tuple in possibleMove:

				# Retire l'image du bouton de l'ancienne case
				self.dict_bouton[self.former_case].config(image="")

				if "empty" in self.plat.getCaseTuple(tuple).getName():
					self.printPanneau(self.former_case, tuple, "move")
				else:
					self.printPanneau(self.former_case, tuple, "take")

				self.plat.move(self.former_case, tuple)

				# Place l'image de l'ancienne case sur la nouvelle
				self.bouton.config(image=self.image)

				self.tourColorDisplay = not self.tourColorDisplay
				self.textTourStringVar.set("AU TOUR DES BLANCS" if self.tourColorDisplay else "AU TOUR DES NOIRS")
				self.tourLabel['fg'] = "black" if self.tourColorDisplay else "white"
				self.tourLabel['bg'] = "white" if self.tourColorDisplay else "black"

				self.tour += 1
				self.textNbTour.set(str(self.tour))

			else:

				print("Impossible move")

	self.listPionBlackPlayEchec = self.plat.checkEchec("blanc")
	self.listPionWhitePlayEchec = self.plat.checkEchec("noir")

	self.echecTrace = {"whitePlayEchec": [], "blackPlayEchec": []}

	if self.listPionBlackPlayEchec:

		self.dict_bouton[self.plat.getRoi("blanc")].config(bg="#CD4C4C")

		for pionEchec in self.listPionBlackPlayEchec:
			self.dict_bouton[pionEchec].config(bg="#e08f38")

		self.echecTrace["blackPlayEchec"] = self.listPionBlackPlayEchec

		self.textAffichage.set("ECHEC")
		self.affichage['fg'] = "white"
		self.affichage['bg'] = "#A02B2B"
		self.whiteEnEchec = True


	else:

		self.original_color = self.coul_bouton[self.plat.getRoi("blanc")]
		self.dict_bouton[self.plat.getRoi("blanc")].config(bg=self.original_color)

		self.echecTraceToEmpty = self.event_log[-1].getEchecTrace()

		if self.echecTraceToEmpty:

			for pionEchec in self.echecTraceToEmpty["blackPlayEchec"]:
				# On récupère sa couleur de base (originelle)
				self.pionEchecOriginalColor = self.coul_bouton[pionEchec]

				# Et on lui remet sa couleur de base.
				self.dict_bouton[pionEchec].config(bg=self.pionEchecOriginalColor)

		self.textAffichage.set("")
		self.affichage['fg'] = "black"
		self.affichage['bg'] = "#789FDE"

	if self.listPionWhitePlayEchec:

		self.dict_bouton[self.plat.getRoi("noir")].config(bg="#CD4C4C")

		for pionEchec in self.listPionWhitePlayEchec:
			self.dict_bouton[pionEchec].config(bg="#e08f38")

		self.echecTrace["whitePlayEchec"] = self.listPionWhitePlayEchec

		self.textAffichage.set("ECHEC")
		self.affichage['fg'] = "white"
		self.affichage['bg'] = "#A02B2B"
		self.blackEnEchec = True

	else:

		self.original_color = self.coul_bouton[self.plat.getRoi("noir")]
		self.dict_bouton[self.plat.getRoi("noir")].config(bg=self.original_color)

		self.echecTraceToEmpty = self.event_log[-1].getEchecTrace()

		if self.echecTraceToEmpty:

			for pionEchec in self.echecTraceToEmpty["whitePlayEchec"]:
				# On récupère sa couleur de base (originelle)
				self.pionEchecOriginalColor = self.coul_bouton[pionEchec]

				# Et on lui remet sa couleur de base.
				self.dict_bouton[pionEchec].config(bg=self.pionEchecOriginalColor)

		self.textAffichage.set("")
		self.affichage['fg'] = "black"
		self.affichage['bg'] = "#789FDE"

	checkMateWhiteTestResult = self.plat.checkMate("blanc")
	checkMateBlackTestResult = self.plat.checkMate("noir")
	print("@@@@@@@@@@@@@@@", checkMateWhiteTestResult)
	print("@@@@@@@@@@@@@@@", checkMateBlackTestResult)

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

	if checkMateWhiteTestResult == "mat":

		self.textAffichage.set("ECHEC ET MAT\nLes Noirs l'emportent")
		self.affichage['fg'] = "black"
		self.affichage['bg'] = "#A02B2B"

		self.freezeGrid()

	elif type(checkMateWhiteTestResult) == list:

		listeSauveteurWhite = []
		listeSauveteurWhiteTrace = []

		listeMoveRoiSave = checkMateWhiteTestResult

		for el in listeMoveRoiSave:

			if self.plat.getCaseTuple(el[0]).getType() != 'roi':

				self.dict_bouton[el[0]].config(bg="#5fb1cf")

				listeSauveteurWhite.append(el[0])

				for move in el[1]:
					self.dict_bouton[el[1]].config(bg="#31cc55")

					listeSauveteurWhiteTrace.append(el[1])

		self.newEventSauveteur["whiteSaver"] = listeSauveteurWhite
		self.newEventSauveteur["whiteSaverTrace"] = listeSauveteurWhiteTrace

		listButtonNotToDisable = listeSauveteurWhite + listeSauveteurWhiteTrace
		roiBlanc = self.plat.getRoi("blanc")
		listButtonNotToDisable.append(roiBlanc)
		listButtonNotToDisable += self.plat.getPath(roiBlanc)

		self.newEvent.setEnabledButton(listButtonNotToDisable)

		self.disableButtonInCaseOfEchec(self.dict_bouton, listButtonNotToDisable)


	elif checkMateWhiteTestResult == "no-echec":

		self.whiteSaverToEmpty = self.event_log[-1].getSaver()

		if self.whiteSaverToEmpty:

			for saver in self.whiteSaverToEmpty["whiteSaver"]:
				# On récupère sa couleur de base (originelle)
				self.pionEchecOriginalColor = self.coul_bouton[saver]

				# Et on lui remet sa couleur de base.
				self.dict_bouton[saver].config(bg=self.pionEchecOriginalColor)

			for saverMove in self.whiteSaverToEmpty["whiteSaverTrace"]:
				# On récupère sa couleur de base (originelle)
				self.pionEchecOriginalColor = self.coul_bouton[saverMove]

				# Et on lui remet sa couleur de base.
				self.dict_bouton[saverMove].config(bg=self.pionEchecOriginalColor)

		self.enableAllButtons()

	# Black Test Echec ----------------------------------------------------------------------------

	if checkMateBlackTestResult == "mat":

		self.textAffichage.set("ECHEC ET MAT\nLes Blancs l'emportent")
		self.affichage['fg'] = "black"
		self.affichage['bg'] = "#A02B2B"

		self.freezeGrid()

	elif type(checkMateBlackTestResult) == list:

		listeSauveteurBlack = []
		listeSauveteurBlackTrace = []

		listeMoveRoiSave = checkMateBlackTestResult

		for el in listeMoveRoiSave:

			if self.plat.getCaseTuple(el[0]).getType() != 'roi':

				self.dict_bouton[el[0]].config(bg="#5fb1cf")

				listeSauveteurBlack.append(el[0])

				for move in el[1]:
					self.dict_bouton[el[1]].config(bg="#31cc55")
					listeSauveteurBlackTrace.append(el[1])

		self.newEventSauveteur["blackSaver"] = listeSauveteurBlack
		self.newEventSauveteur["blackSaverTrace"] = listeSauveteurBlackTrace

		listButtonNotToDisable = listeSauveteurBlack + listeSauveteurBlackTrace
		roiNoir = self.plat.getRoi("noir")
		listButtonNotToDisable.append(roiNoir)
		listButtonNotToDisable += self.plat.getPath(roiNoir)

		self.newEvent.setEnabledButton(listButtonNotToDisable)

		self.disableButtonInCaseOfEchec(self.dict_bouton, listButtonNotToDisable)

	elif checkMateBlackTestResult == "no-echec":

		self.blackSaverToEmpty = self.event_log[-1].getSaver()

		if self.blackSaverToEmpty:

			for saver in self.blackSaverToEmpty["blackSaver"]:
				# On récupère sa couleur de base (originelle)
				self.pionEchecOriginalColor = self.coul_bouton[saver]

				# Et on lui remet sa couleur de base.
				self.dict_bouton[saver].config(bg=self.pionEchecOriginalColor)

			for saverMove in self.blackSaverToEmpty["blackSaverTrace"]:
				# On récupère sa couleur de base (originelle)
				self.pionEchecOriginalColor = self.coul_bouton[saverMove]

				# Et on lui remet sa couleur de base.
				self.dict_bouton[saverMove].config(bg=self.pionEchecOriginalColor)

		self.enableAllButtons()

	self.newEvent.setSaver(self.newEventSauveteur)
	self.newEvent.setEchecTrace(self.echecTrace)
	self.newEvent.apercu()

	# On rajoute l'evènement à la liste des évènements
	self.event_log.append(self.newEvent)

	# On incrémente la chaine qui sert à créer le nom/id des évènements pour le prochain
	# évènement. Toujours de x + 1
	self.id += 1

	# self.plat.apercu()

# def run():
#     gamePlaying = True
#     oldTime = datetime.now().strftime("%H:%M:%S")
#     while gamePlaying:
#         now = datetime.now().strftime("%H:%M:%S")
#         if oldTime != now:
#             print(now)
#             oldTime = now
#
#
# control_thread = Thread(target=run, daemon=True)

# control_thread.start()