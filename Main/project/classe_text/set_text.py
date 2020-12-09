from .pion_text import *

class set_text:

    def __init__(self):

            self.listePions = {}

            for couleur in ["blanc","noir"]:
                for i in range(1,9):
                    name = f"{i}_pion_{couleur}"
                    piece = pion_text(name, "pion", couleur, False)
                    self.listePions[name] = piece

                for i in range(1,3):
                    name = f"{i}_cavalier_{couleur}"
                    piece = pion_text(name, "cavalier", couleur, False)
                    self.listePions[name] = piece

                for i in range(1,3):
                    name = f"{i}_fou_{couleur}"
                    piece = pion_text(name, "fou", couleur, False)
                    self.listePions[name] = piece

                for i in range(1,3):
                    name = f"{i}_tour_{couleur}"
                    piece = pion_text(name, "tour", couleur, False)
                    self.listePions[name] = piece

                name = f"1_reine_{couleur}"
                piece = pion_text(name, "reine", couleur, False)
                self.listePions[name] = piece

                name = f"1_roi_{couleur}"
                piece = pion_text(name, "roi", couleur, False)
                self.listePions[name] = piece

                for i in range(1,66):
                    name = f"{i}_empty"
                    piece = pion_text(name, "", "", False, None)