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
        self.op_grond = True          # Staat hij op de grond of een platform?
        self.platform_y = GROND_Y     # De hoogte waarop hij nu staat
        self._teller = 0              # Voor de animatie

    def spring(self):
        """Laat het vierkantje springen (alleen als het op de grond/platform staat)."""
        if self.op_grond:
            self.snelheid_y = SPRING_KRACHT
            self.op_grond = False

    def bijwerken(self, blokken=None):
        """Beweeg het vierkantje omhoog/omlaag. Controleer of hij op een platform landt."""
        self._teller += 1

        # Zwaartekracht trekt het vierkantje naar beneden
        self.snelheid_y -= ZWAARTEKRACHT
        self.y += self.snelheid_y

        # Standaard is de vloer de grond
        vloer = GROND_Y

        # Kijk of een platform onder de speler zit (kan erop landen)
        if blokken and self.snelheid_y <= 0:
            for blok in blokken:
                bx  = blok[0]
                bvY = blok[2]           # vlieg_y van het blok (hoogte boven de grond)
                bw  = blok[3]           # breedte van het blok
                bh  = blok[4]           # hoogte (dikte) van het blok

                # Bovenkant van het platform (in spel-coördinaten)
                platform_top = GROND_Y + bvY + bh

                # Ligt de speler horizontaal boven het platform?
                if (self.x + self.breedte - 6 > bx and
                        self.x + 6 < bx + bw):
                    # Is de speler vlak boven het platform (met wat marge)?
                    if (self.y <= platform_top + 4 and
                            self.y >= platform_top - 14):
                        # Hoger platform = nieuwe vloer
                        if platform_top > vloer:
                            vloer = platform_top
                            blok[5] = True   # Markeer: speler staat hier op

        # Niet verder vallen dan de vloer
        if self.y <= vloer:
            self.y = vloer
            self.snelheid_y = 0
            self.op_grond = True
            self.platform_y = vloer
        else:
            # In de lucht — maar misschien staat hij op een platform
            # Als hij niet meer boven een platform hangt, valt hij gewoon door
            if self.y > vloer + 2:
                self.op_grond = False

    def teken(self, scherm):
        """Teken het vierkantje met een grappig gezicht (geen benen)."""
        import pygame

        x = int(self.x)
        y = int(scherm.get_height() - self.y - self.hoogte)
        w = self.breedte
        h = self.hoogte

        # Kleine wiebel als hij op de grond staat
        if self.op_grond:
            wiebel = math.sin(self._teller * 0.35) * 1.5
            y += int(wiebel)

        # Schaduw onder het vierkantje
        pygame.draw.ellipse(scherm, (0, 0, 0),
                            (x + 4, y + h + 2, w - 8, 8))

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

        # Mond — lachend op grond, angstig in de lucht
        if not self.op_grond:
            pygame.draw.ellipse(scherm, OOG_KLEUR,
                                (x + w // 2 - 5, y + h - 14, 10, 9))
        else:
            pygame.draw.arc(scherm, OOG_KLEUR,
                            (x + 8, y + h - 16, w - 16, 10),
                            math.pi, 2 * math.pi, 2)

