# speler.py
# Het vierkantje dat de speler bestuurt.

import math
from instellingen import (SPELER_X, SPELER_GROOT, SPRING_KRACHT,
                           ZWAARTEKRACHT, GROND_Y,
                           SPELER_KLEUR, OOG_KLEUR)


class Speler:
    """Het gele vierkantje — loopt automatisch en kan springen."""

    def __init__(self):
        self.x = SPELER_X
        self.y = GROND_Y              # Begint op de grond
        self.breedte = SPELER_GROOT
        self.hoogte  = SPELER_GROOT
        self.snelheid_y = 0           # Verticale snelheid (omhoog positief)
        self.op_grond = True          # Staat hij op de grond?
        self._stap_teller = 0         # Voor de loopanimatie

    def spring(self):
        """Laat het vierkantje springen (alleen als het op de grond staat)."""
        if self.op_grond:
            self.snelheid_y = SPRING_KRACHT
            self.op_grond = False

    def bijwerken(self):
        """Beweeg het vierkantje omhoog/omlaag door zwaartekracht."""
        self._stap_teller += 1

        # Zwaartekracht trekt het vierkantje naar beneden
        self.snelheid_y -= ZWAARTEKRACHT
        self.y += self.snelheid_y

        # Niet verder vallen dan de grond
        if self.y <= GROND_Y:
            self.y = GROND_Y
            self.snelheid_y = 0
            self.op_grond = True

    def teken(self, scherm):
        """Teken het vierkantje met een grappig gezicht."""
        import pygame

        x = int(self.x)
        y = int(scherm.get_height() - self.y - self.hoogte)  # Flip y-as
        w = self.breedte
        h = self.hoogte

        # Kleine loopanimatie: wiebelt een beetje als hij loopt
        if self.op_grond:
            wiebel = math.sin(self._stap_teller * 0.3) * 2
            y += int(wiebel)

        # Schaduw onder het vierkantje
        pygame.draw.ellipse(scherm, (0, 0, 0, 80),
                            (x + 4, y + h - 4, w - 8, 10))

        # Lijf — geel vierkant
        pygame.draw.rect(scherm, SPELER_KLEUR, (x, y, w, h), border_radius=6)
        pygame.draw.rect(scherm, (200, 160, 0), (x, y, w, h), 3, border_radius=6)

        # Ogen — kijken naar rechts
        oog_y = y + h // 3
        # Rechter oog (vooraan)
        pygame.draw.circle(scherm, (255, 255, 255), (x + w - 10, oog_y), 7)
        pygame.draw.circle(scherm, OOG_KLEUR,       (x + w - 8,  oog_y + 1), 4)
        pygame.draw.circle(scherm, (255, 255, 255), (x + w - 7,  oog_y - 1), 1)

        # Klein oogje achteraan
        pygame.draw.circle(scherm, (255, 255, 255), (x + 10, oog_y), 5)
        pygame.draw.circle(scherm, OOG_KLEUR,       (x + 11, oog_y + 1), 3)

        # Mond (lachend of angstig in de lucht)
        if not self.op_grond:
            # In de lucht: angstige O-mond
            pygame.draw.ellipse(scherm, OOG_KLEUR,
                                (x + w // 2 - 5, y + h - 14, 10, 9))
        else:
            # Op de grond: lachend
            pygame.draw.arc(scherm, OOG_KLEUR,
                            (x + 8, y + h - 16, w - 16, 10),
                            math.pi, 2 * math.pi, 2)

    def geeft_botsing(self, bx, by_scherm, bw, bh):
        """Controleer of het vierkantje een blok raakt."""
        # Omzetten: blok-y is al in scherm-coordinaten, speler-y moet ook
        # (deze berekening doen we in main.py, zie daar)
        pass
