# main.py
# MennoTrash — Spring over de blokken en kom zo ver mogelijk!
# Druk op SPATIE om te springen. Je kunt ook bovenop de blokken landen!

import pygame
import random
import math
import sys
from instellingen import *
from speler import Speler


# =============================================
# Initialiseer pygame
# =============================================
pygame.init()
scherm = pygame.display.set_mode((SCHERM_BREEDTE, SCHERM_HOOGTE))
pygame.display.set_caption(SCHERM_TITEL)
klok = pygame.time.Clock()

# Lettertypen
font_groot  = pygame.font.SysFont("Arial", 52, bold=True)
font_middel = pygame.font.SysFont("Arial", 28, bold=True)
font_klein  = pygame.font.SysFont("Arial", 20)


# =============================================
# Hulpfuncties
# =============================================

def y_naar_scherm(game_y, obj_hoogte):
    """Zet spel-y (grond=0) om naar scherm-y (links-boven=0)."""
    return SCHERM_HOOGTE - game_y - obj_hoogte


def teken_grond(schuif):
    """Teken een groene grond-balk onderaan, met meeschuivende tegels."""
    grond_rect = (0, SCHERM_HOOGTE - GROND_Y, SCHERM_BREEDTE, GROND_Y)
    pygame.draw.rect(scherm, GROND_KLEUR, grond_rect)
    pygame.draw.rect(scherm, GROND_RAND_KLEUR,
                     (0, SCHERM_HOOGTE - GROND_Y, SCHERM_BREEDTE, 6))

    tegel_breedte = 60
    offset = int(schuif) % tegel_breedte
    for tx in range(-offset, SCHERM_BREEDTE + tegel_breedte, tegel_breedte):
        pygame.draw.line(scherm, GROND_RAND_KLEUR,
                         (tx, SCHERM_HOOGTE - GROND_Y + 8),
                         (tx, SCHERM_HOOGTE - 4), 2)

    for gx in range(-offset, SCHERM_BREEDTE + 30, 30):
        vaste = (int(gx + schuif) * 7) % 10
        pygame.draw.polygon(scherm, (80, 220, 80), [
            (gx + vaste,      SCHERM_HOOGTE - GROND_Y),
            (gx + vaste + 6,  SCHERM_HOOGTE - GROND_Y),
            (gx + vaste + 3,  SCHERM_HOOGTE - GROND_Y - 9),
        ])


def teken_achtergrond(teller):
    """Teken een simpele bewegende achtergrond met sterren."""
    scherm.fill(ACHTERGROND_KLEUR)
    ster_posities = [
        (100, 60), (230, 90), (350, 40), (500, 110), (650, 70),
        (720, 130), (170, 150), (420, 160), (580, 50), (780, 100),
        (50, 200), (300, 180), (470, 210), (620, 190), (740, 220),
    ]
    for i, (sx, sy) in enumerate(ster_posities):
        beweeg_x = (sx - teller * 0.3) % SCHERM_BREEDTE
        grootte = 2 + int(math.sin(teller * 0.05 + i) > 0.7)
        pygame.draw.circle(scherm, (255, 255, 200), (int(beweeg_x), sy), grootte)


def teken_blok(blok):
    """Teken één vliegend platform met stekels boven en onder.
    blok = [x, vlieg_y, breedte, hoogte, op_speler]
    """
    bx   = int(blok[0])
    bvY  = blok[1]
    bw   = blok[2]
    bh   = blok[3]

    by_scherm = SCHERM_HOOGTE - GROND_Y - bvY - bh

    # Schaduw onder het blok
    schaduw_y = SCHERM_HOOGTE - GROND_Y + 2
    pygame.draw.ellipse(scherm, (0, 0, 0),
                        (bx + 4, schaduw_y, bw - 8, 6))

    # Het blok zelf
    pygame.draw.rect(scherm, BLOK_KLEUR,
                     (bx, by_scherm, bw, bh), border_radius=4)
    pygame.draw.rect(scherm, BLOK_RAND_KLEUR,
                     (bx, by_scherm, bw, bh), 3, border_radius=4)

    # Glanzend streepje bovenop
    pygame.draw.rect(scherm, (230, 100, 100),
                     (bx + 4, by_scherm + 3, bw - 8, 4), border_radius=2)

    # Kleine oogjes — alleen als het blok breed genoeg is
    if bw >= 60:
        oog_y = by_scherm + bh // 2 - 3
        pygame.draw.circle(scherm, (255, 255, 255), (bx + bw - 22, oog_y), 5)
        pygame.draw.circle(scherm, OOG_KLEUR,       (bx + bw - 21, oog_y + 1), 3)
        pygame.draw.circle(scherm, (255, 255, 255), (bx + bw - 10, oog_y), 5)
        pygame.draw.circle(scherm, OOG_KLEUR,       (bx + bw - 9,  oog_y + 1), 3)
        pygame.draw.line(scherm, OOG_KLEUR,
                         (bx + bw - 26, oog_y - 6), (bx + bw - 18, oog_y - 3), 2)
        pygame.draw.line(scherm, OOG_KLEUR,
                         (bx + bw - 14, oog_y - 3), (bx + bw - 6,  oog_y - 6), 2)

    # Stekels (zwarte driehoeken) op willekeurige plekken boven en onder
    teken_driehoeken(bx, bvY, bh, blok[5])


def teken_driehoeken(bx, bvY, bh, stekel_posities, stekel_grootte=10):
    """Teken zwarte stekels op de opgegeven posities (boven of onder het blok).
    stekel_posities = lijst van (relatieve_x, kant) waarbij kant 'boven' of 'onder' is.
    """
    blok_top_s   = SCHERM_HOOGTE - GROND_Y - bvY - bh
    blok_onder_s = SCHERM_HOOGTE - GROND_Y - bvY

    for (rel_x, kant) in stekel_posities:
        mx = int(bx + rel_x)

        if kant == 'boven':
            pygame.draw.polygon(scherm, (10, 10, 10), [
                (mx - stekel_grootte, blok_top_s),
                (mx + stekel_grootte, blok_top_s),
                (mx,                  blok_top_s - stekel_grootte),
            ])
        else:
            pygame.draw.polygon(scherm, (10, 10, 10), [
                (mx - stekel_grootte, blok_onder_s),
                (mx + stekel_grootte, blok_onder_s),
                (mx,                  blok_onder_s + stekel_grootte),
            ])


def teken_grond_stekels(grond_stekels):
    """Teken zwarte driehoeken op de grond (stekels die omhoog wijzen)."""
    stekel_b = 10
    stekel_h = 14
    grond_s  = SCHERM_HOOGTE - GROND_Y   # y-coördinaat van de grond op het scherm

    for sx in grond_stekels:
        mx = int(sx)
        pygame.draw.polygon(scherm, (10, 10, 10), [
            (mx - stekel_b, grond_s),
            (mx + stekel_b, grond_s),
            (mx,            grond_s - stekel_h),
        ])


def raakt_grondstekel(speler, grond_stekels):
    """Controleer of de speler een grondstekel aanraakt."""
    if speler.y > GROND_Y + 2:
        return False   # Speler is in de lucht, geen gevaar
    stekel_b = 10
    marge = 4
    sx_speler = speler.x + marge
    ex_speler = speler.x + speler.breedte - marge
    for sx in grond_stekels:
        if sx_speler < sx + stekel_b and ex_speler > sx - stekel_b:
            return True
    return False


def teken_hud(score, snelheid, game_over, hoogste_score):
    """Teken de score en informatie bovenaan het scherm."""
    score_tekst = font_middel.render(f"Score: {score}", True, SCORE_KLEUR)
    scherm.blit(score_tekst, (20, 16))
    snelheid_tekst = font_klein.render(f"Snelheid: {snelheid:.1f}", True, (180, 180, 255))
    scherm.blit(snelheid_tekst, (SCHERM_BREEDTE - 160, 20))
    if hoogste_score > 0:
        record_tekst = font_klein.render(f"Record: {hoogste_score}", True, (255, 220, 100))
        scherm.blit(record_tekst, (SCHERM_BREEDTE // 2 - 55, 20))


def teken_game_over(score, hoogste_score, is_nieuw_record):
    """Teken het game over scherm."""
    overlay = pygame.Surface((SCHERM_BREEDTE, SCHERM_HOOGTE), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    scherm.blit(overlay, (0, 0))
    tekst = font_groot.render("GAME OVER", True, (255, 80, 80))
    scherm.blit(tekst, (SCHERM_BREEDTE // 2 - tekst.get_width() // 2, 100))
    score_tekst = font_middel.render(f"Je score: {score}", True, (255, 255, 255))
    scherm.blit(score_tekst, (SCHERM_BREEDTE // 2 - score_tekst.get_width() // 2, 175))
    if is_nieuw_record:
        record_tekst = font_middel.render("NIEUW RECORD!", True, (255, 220, 50))
        scherm.blit(record_tekst, (SCHERM_BREEDTE // 2 - record_tekst.get_width() // 2, 215))
    else:
        record_tekst = font_klein.render(f"Record: {hoogste_score}", True, (180, 180, 180))
        scherm.blit(record_tekst, (SCHERM_BREEDTE // 2 - record_tekst.get_width() // 2, 220))
    opnieuw_tekst = font_middel.render("Druk SPATIE om opnieuw te spelen", True, (200, 255, 200))
    scherm.blit(opnieuw_tekst, (SCHERM_BREEDTE // 2 - opnieuw_tekst.get_width() // 2, 280))


def teken_start_scherm():
    """Teken het startscherm."""
    titel = font_groot.render("MennoTrash!", True, (255, 220, 50))
    scherm.blit(titel, (SCHERM_BREEDTE // 2 - titel.get_width() // 2, 80))
    regels = [
        "Spring over de rode blokken!",
        "Je kunt ook BOVENOP de blokken landen.",
        "Druk op SPATIE om te springen.",
        "Hoe verder je komt, hoe sneller het gaat!",
    ]
    for i, regel in enumerate(regels):
        tekst = font_klein.render(regel, True, (200, 220, 255))
        scherm.blit(tekst, (SCHERM_BREEDTE // 2 - tekst.get_width() // 2, 185 + i * 28))
    start_tekst = font_middel.render("Druk SPATIE om te starten!", True, (100, 255, 100))
    scherm.blit(start_tekst, (SCHERM_BREEDTE // 2 - start_tekst.get_width() // 2, 320))


def controleer_botsing(speler, blok, prev_y):
    """Controleer of de speler een blok raakt.
    Geeft terug: 'geen', 'landen' (van boven), of 'crash' (van de zijkant).

    prev_y = positie van speler VOOR de beweging deze frame.
    blok = [x, vlieg_y, breedte, hoogte, op_speler]
    """
    bx  = blok[0]
    bvY = blok[1]   # vlieg_y (boven de grond)
    bw  = blok[2]
    bh  = blok[3]

    # Speler-positie in spel-coördinaten
    sx     = speler.x
    sw     = speler.breedte
    sh     = speler.hoogte
    sy     = speler.y         # onderkant van de speler
    sy_top = sy + sh          # bovenkant van de speler

    # Blok-coördinaten in spelpixels
    blok_boven  = GROND_Y + bvY + bh    # bovenkant van het platform
    blok_onder  = GROND_Y + bvY         # onderkant van het platform

    # Horizontaal overlappend? (met kleine marge zodat het eerlijker voelt)
    marge = 5
    horizontaal = (sx + marge < bx + bw and sx + sw - marge > bx)

    if not horizontaal:
        return 'geen'

    # Verticaal overlappend?
    if sy_top <= blok_onder or sy >= blok_boven:
        return 'geen'

    # --- Overlap gevonden! Bepaal of landing of crash ---

    # Controleer of de speler van BOVEN op het platform is gevallen.
    # prev_y = positie vóór deze frame. Als prev_y >= blok_boven was de speler erBOVEN.
    if speler.snelheid_y <= 0 and prev_y >= blok_boven - 4:
        return 'landen'

    # Alles anders (zijkant, van onder, door stekels) = crash
    return 'crash'


def nieuw_blok():
    """Maak een nieuw vliegend platform.
    Geeft een lijst terug: [x, vlieg_y, breedte, hoogte, op_speler, stekel_posities]
    Sommige blokken zijn lang, anderen kort.
    """
    vlieg_y = random.randint(BLOK_MIN_VLIEG_Y, BLOK_MAX_VLIEG_Y)
    kans_lang = random.random()
    if kans_lang < 0.25:
        breedte = random.randint(160, 260)
    elif kans_lang < 0.6:
        breedte = random.randint(80, 140)
    else:
        breedte = random.randint(40, 75)
    hoogte = BLOK_HOOGTE

    # Bereken stekelposities: elke mogelijke plek heeft 5% kans op een stekel BOVEN
    stekel_grootte = 10
    stekel_posities = []
    for i in range(max(1, breedte // (stekel_grootte * 2))):
        rel_x = i * (stekel_grootte * 2) + stekel_grootte
        if random.random() < 0.05:   # 5% kans: stekel boven op het blok
            stekel_posities.append((rel_x, 'boven'))

    return [float(SCHERM_BREEDTE + 20), vlieg_y, breedte, hoogte, False, stekel_posities]


# =============================================
# Spelstatus
# =============================================

def reset_spel():
    """Reset alle speldata voor een nieuw potje."""
    speler = Speler()
    blokken = []
    grond_stekels = []        # Lijst van x-posities van stekels op de grond
    teller = 0
    score = 0
    snelheid = BEGIN_SNELHEID
    volgende_blok = random.randint(60, 110)
    volgende_stekel = random.randint(40, 90)   # Wanneer de volgende grondstekel spawnt
    schuif = 0.0
    return speler, blokken, grond_stekels, teller, score, snelheid, volgende_blok, volgende_stekel, schuif


# =============================================
# HOOFDLUS
# =============================================

def speel():
    """De hoofdlus van het spel."""
    hoogste_score = 0
    status = "start"

    speler, blokken, grond_stekels, teller, score, snelheid, volgende_blok, volgende_stekel, schuif = reset_spel()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    if status == "start":
                        status = "spelen"
                    elif status == "spelen":
                        speler.spring()
                    elif status == "game_over":
                        speler, blokken, grond_stekels, teller, score, snelheid, volgende_blok, volgende_stekel, schuif = reset_spel()
                        status = "spelen"

        teken_achtergrond(teller)
        teken_grond(schuif)

        if status == "start":
            speler.teken(scherm)
            teken_start_scherm()

        elif status == "spelen":
            teller += 1
            schuif += snelheid

            if teller % 6 == 0:
                score += 1

            if teller % 300 == 0:
                snelheid += SNELHEID_TOENAME

            # Reset de "op_speler" markering van alle blokken
            for blok in blokken:
                blok[4] = False

            # Sla de positie op VOOR de beweging (nodig voor landing-detectie)
            prev_y = speler.y

            # Speler bijwerken (zwaartekracht + grond-botsing)
            speler.bijwerken()

            # Nieuw blok spawnen?
            volgende_blok -= 1
            if volgende_blok <= 0:
                blokken.append(nieuw_blok())
                min_pauze = max(15, 45 - int(snelheid * 3))
                max_pauze = max(30,  80 - int(snelheid * 4))
                volgende_blok = random.randint(min_pauze, max_pauze)

            # Nieuwe grondstekel spawnen?
            volgende_stekel -= 1
            if volgende_stekel <= 0:
                grond_stekels.append(float(SCHERM_BREEDTE + 20))
                volgende_stekel = random.randint(50, 130)

            # Grondstekels bewegen naar links
            for i in range(len(grond_stekels)):
                grond_stekels[i] -= snelheid
            grond_stekels = [sx for sx in grond_stekels if sx > -20]

            # Blokken bewegen, botsing controleren
            game_over_nu = False
            for blok in blokken:
                blok[0] -= snelheid

                resultaat = controleer_botsing(speler, blok, prev_y)
                if resultaat == 'landen':
                    blok_boven = GROND_Y + blok[1] + blok[3]
                    speler.y = blok_boven
                    speler.snelheid_y = 0
                    speler.op_grond = True
                    blok[4] = True
                elif resultaat == 'crash':
                    game_over_nu = True
                    break

            # Grondstekel botsing controleren
            if not game_over_nu and raakt_grondstekel(speler, grond_stekels):
                game_over_nu = True

            # Als de speler op een platform stond en het platform schuift weg
            if not game_over_nu:
                op_platform = any(b[4] for b in blokken)
                if not op_platform and speler.y > GROND_Y:
                    speler.op_grond = False

            if game_over_nu:
                if score > hoogste_score:
                    hoogste_score = score
                status = "game_over"

            # Blokken tekenen
            for blok in blokken:
                teken_blok(blok)

            # Verwijder blokken die voorbij het scherm zijn
            blokken = [b for b in blokken if b[0] > -300]

            # Grondstekels tekenen (na de grond, zodat ze erop staan)
            teken_grond_stekels(grond_stekels)

            speler.teken(scherm)
            teken_hud(score, snelheid, False, hoogste_score)

        elif status == "game_over":
            for blok in blokken:
                teken_blok(blok)
            teken_grond_stekels(grond_stekels)
            speler.teken(scherm)
            teken_hud(score, snelheid, True, hoogste_score)
            teken_game_over(score, hoogste_score, score >= hoogste_score and score > 0)

        pygame.display.flip()
        klok.tick(60)


# Start het spel!
speel()


import pygame
import random
import math
import sys
from instellingen import *
from speler import Speler


# =============================================
# Initialiseer pygame
# =============================================
pygame.init()
scherm = pygame.display.set_mode((SCHERM_BREEDTE, SCHERM_HOOGTE))
pygame.display.set_caption(SCHERM_TITEL)
klok = pygame.time.Clock()

# Lettertypen
font_groot  = pygame.font.SysFont("Arial", 52, bold=True)
font_middel = pygame.font.SysFont("Arial", 28, bold=True)
font_klein  = pygame.font.SysFont("Arial", 20)


# =============================================
# Hulpfuncties
# =============================================

def y_naar_scherm(game_y, obj_hoogte):
    """Zet spel-y (grond=0) om naar scherm-y (links-boven=0)."""
    return SCHERM_HOOGTE - game_y - obj_hoogte


def teken_grond(schuif):
    """Teken een groene grond-balk onderaan, met meeschuivende tegels."""
    grond_rect = (0, SCHERM_HOOGTE - GROND_Y, SCHERM_BREEDTE, GROND_Y)
    pygame.draw.rect(scherm, GROND_KLEUR, grond_rect)
    # Groene rand bovenop de grond
    pygame.draw.rect(scherm, GROND_RAND_KLEUR,
                     (0, SCHERM_HOOGTE - GROND_Y, SCHERM_BREEDTE, 6))

    # Grond-tegels schuiven mee naar links
    tegel_breedte = 60
    offset = int(schuif) % tegel_breedte
    for tx in range(-offset, SCHERM_BREEDTE + tegel_breedte, tegel_breedte):
        # Donkere scheidingslijntjes tussen de tegels
        pygame.draw.line(scherm, GROND_RAND_KLEUR,
                         (tx, SCHERM_HOOGTE - GROND_Y + 8),
                         (tx, SCHERM_HOOGTE - 4), 2)

    # Graspikjes schuiven ook mee
    for gx in range(-offset, SCHERM_BREEDTE + 30, 30):
        vaste = (int(gx + schuif) * 7) % 10
        pygame.draw.polygon(scherm, (80, 220, 80), [
            (gx + vaste,      SCHERM_HOOGTE - GROND_Y),
            (gx + vaste + 6,  SCHERM_HOOGTE - GROND_Y),
            (gx + vaste + 3,  SCHERM_HOOGTE - GROND_Y - 9),
        ])


def teken_achtergrond(teller):
    """Teken een simpele bewegende achtergrond met sterren."""
    scherm.fill(ACHTERGROND_KLEUR)

    # Sterren bewegen langzaam mee (parallax-effect)
    ster_posities = [
        (100, 60), (230, 90), (350, 40), (500, 110), (650, 70),
        (720, 130), (170, 150), (420, 160), (580, 50), (780, 100),
        (50, 200), (300, 180), (470, 210), (620, 190), (740, 220),
    ]
    for i, (sx, sy) in enumerate(ster_posities):
        # Sterren schuiven heel langzaam mee naar links
        beweeg_x = (sx - teller * 0.3) % SCHERM_BREEDTE
        # Kleine twinkeling
        grootte = 2 + int(math.sin(teller * 0.05 + i) > 0.7)
        pygame.draw.circle(scherm, (255, 255, 200), (int(beweeg_x), sy), grootte)


def teken_blok(bx, bh):
    """Teken één rood blok op positie bx met hoogte bh."""
    by_scherm = SCHERM_HOOGTE - GROND_Y - bh
    # Rood blok
    pygame.draw.rect(scherm, BLOK_KLEUR,
                     (bx, by_scherm, BLOK_BREEDTE, bh), border_radius=4)
    pygame.draw.rect(scherm, BLOK_RAND_KLEUR,
                     (bx, by_scherm, BLOK_BREEDTE, bh), 3, border_radius=4)
    # Kleine oogjes op het blok (het blok kijkt je aan 👀)
    oog_y = by_scherm + 10
    pygame.draw.circle(scherm, (255, 255, 255), (bx + 8,  oog_y), 5)
    pygame.draw.circle(scherm, OOG_KLEUR,       (bx + 9,  oog_y + 1), 3)
    pygame.draw.circle(scherm, (255, 255, 255), (bx + 20, oog_y), 5)
    pygame.draw.circle(scherm, OOG_KLEUR,       (bx + 21, oog_y + 1), 3)
    # Boze wenkbrauwen
    pygame.draw.line(scherm, OOG_KLEUR,
                     (bx + 4, oog_y - 7), (bx + 12, oog_y - 4), 2)
    pygame.draw.line(scherm, OOG_KLEUR,
                     (bx + 16, oog_y - 4), (bx + 24, oog_y - 7), 2)


def teken_hud(score, snelheid, game_over, hoogste_score):
    """Teken de score en informatie bovenaan het scherm."""
    # Score linksboven
    score_tekst = font_middel.render(f"Score: {score}", True, SCORE_KLEUR)
    scherm.blit(score_tekst, (20, 16))

    # Snelheid rechtsboven
    snelheid_tekst = font_klein.render(f"Snelheid: {snelheid:.1f}", True, (180, 180, 255))
    scherm.blit(snelheid_tekst, (SCHERM_BREEDTE - 160, 20))

    # Hoogste score midden bovenin
    if hoogste_score > 0:
        record_tekst = font_klein.render(f"Record: {hoogste_score}", True, (255, 220, 100))
        scherm.blit(record_tekst, (SCHERM_BREEDTE // 2 - 55, 20))


def teken_game_over(score, hoogste_score, is_nieuw_record):
    """Teken het game over scherm."""
    # Donkere overlay
    overlay = pygame.Surface((SCHERM_BREEDTE, SCHERM_HOOGTE), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    scherm.blit(overlay, (0, 0))

    # "GAME OVER" tekst
    tekst = font_groot.render("GAME OVER", True, (255, 80, 80))
    scherm.blit(tekst, (SCHERM_BREEDTE // 2 - tekst.get_width() // 2, 100))

    # Score
    score_tekst = font_middel.render(f"Je score: {score}", True, (255, 255, 255))
    scherm.blit(score_tekst, (SCHERM_BREEDTE // 2 - score_tekst.get_width() // 2, 175))

    # Nieuw record?
    if is_nieuw_record:
        record_tekst = font_middel.render("🏆 NIEUW RECORD!", True, (255, 220, 50))
        scherm.blit(record_tekst, (SCHERM_BREEDTE // 2 - record_tekst.get_width() // 2, 215))
    else:
        record_tekst = font_klein.render(f"Record: {hoogste_score}", True, (180, 180, 180))
        scherm.blit(record_tekst, (SCHERM_BREEDTE // 2 - record_tekst.get_width() // 2, 220))

    # Opnieuw spelen
    opnieuw_tekst = font_middel.render("Druk SPATIE om opnieuw te spelen", True, (200, 255, 200))
    scherm.blit(opnieuw_tekst, (SCHERM_BREEDTE // 2 - opnieuw_tekst.get_width() // 2, 280))


def teken_start_scherm():
    """Teken het startscherm."""
    # Titel
    titel = font_groot.render("MennoTrash 🗑️", True, (255, 220, 50))
    scherm.blit(titel, (SCHERM_BREEDTE // 2 - titel.get_width() // 2, 80))

    # Uitleg
    regels = [
        "Spring over de rode blokken!",
        "Druk op SPATIE om te springen.",
        "Hoe verder je komt, hoe sneller het gaat!",
    ]
    for i, regel in enumerate(regels):
        tekst = font_klein.render(regel, True, (200, 220, 255))
        scherm.blit(tekst, (SCHERM_BREEDTE // 2 - tekst.get_width() // 2, 185 + i * 32))

    # Start-knop
    start_tekst = font_middel.render("Druk SPATIE om te starten!", True, (100, 255, 100))
    scherm.blit(start_tekst, (SCHERM_BREEDTE // 2 - start_tekst.get_width() // 2, 310))


def botsing(speler, bx, bh):
    """Controleer of de speler een blok raakt."""
    # Speler-rechthoek (in scherm-coördinaten)
    sx = speler.x
    sy = y_naar_scherm(speler.y, speler.hoogte)
    sw = speler.breedte
    sh = speler.hoogte

    # Blok-rechthoek (in scherm-coördinaten)
    bx_s = bx
    by_s = SCHERM_HOOGTE - GROND_Y - bh
    bw = BLOK_BREEDTE

    # Kleine marge zodat het iets eerlijker voelt (4 pixels kleiner aan elke kant)
    marge = 5
    return (sx + marge < bx_s + bw and
            sx + sw - marge > bx_s and
            sy + marge < by_s + bh and
            sy + sh - marge > by_s)


# =============================================
# Spelstatus
# =============================================

def reset_spel():
    """Reset alle speldata voor een nieuw potje."""
    speler = Speler()
    blokken = []          # Lijst van (x, hoogte) tuples
    teller = 0            # Hoeveel frames al gespeeld
    score = 0
    snelheid = BEGIN_SNELHEID
    volgende_blok = random.randint(60, 100)   # Wanneer het volgende blok verschijnt
    schuif = 0.0          # Hoe ver de grond al geschoven is
    return speler, blokken, teller, score, snelheid, volgende_blok, schuif


# =============================================
# HOOFDLUS
# =============================================

def speel():
    """De hoofdlus van het spel."""
    hoogste_score = 0
    status = "start"      # "start", "spelen", "game_over"

    speler, blokken, teller, score, snelheid, volgende_blok, schuif = reset_spel()

    while True:
        # --- Gebeurtenissen afhandelen ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    if status == "start":
                        status = "spelen"
                    elif status == "spelen":
                        speler.spring()
                    elif status == "game_over":
                        # Nieuw potje starten
                        speler, blokken, teller, score, snelheid, volgende_blok, schuif = reset_spel()
                        status = "spelen"

        # --- Achtergrond tekenen ---
        teken_achtergrond(teller)
        teken_grond(schuif)

        if status == "start":
            # Teken een voorbeeldspeler op het startscherm
            speler.teken(scherm)
            teken_start_scherm()

        elif status == "spelen":
            teller += 1
            schuif += snelheid   # Grond schuift mee met de snelheid

            # Score stijgt elke 6 frames
            if teller % 6 == 0:
                score += 1

            # Snelheid stijgt elke 300 frames (5 seconden)
            if teller % 300 == 0:
                snelheid += SNELHEID_TOENAME

            # Speler bijwerken
            speler.bijwerken()

            # Nieuw blok spawnen?
            volgende_blok -= 1
            if volgende_blok <= 0:
                hoogte = random.randint(BLOK_MIN_HOOGTE, BLOK_MAX_HOOGTE)
                blokken.append([SCHERM_BREEDTE + 10, hoogte])
                # Hoe sneller het spel, hoe korter de pauze tussen blokken
                min_pauze = max(25, 60 - int(snelheid * 3))
                max_pauze = max(50, 110 - int(snelheid * 4))
                volgende_blok = random.randint(min_pauze, max_pauze)

            # Blokken bewegen en tekenen
            for blok in blokken:
                blok[0] -= snelheid     # Beweeg naar links

                # Botsing controleren
                if botsing(speler, blok[0], blok[1]):
                    if score > hoogste_score:
                        hoogste_score = score
                    status = "game_over"
                    break

                teken_blok(blok[0], blok[1])

            # Verwijder blokken die voorbij het scherm zijn
            blokken = [b for b in blokken if b[0] > -BLOK_BREEDTE - 10]

            # Speler tekenen
            speler.teken(scherm)

            # HUD tekenen
            teken_hud(score, snelheid, False, hoogste_score)

        elif status == "game_over":
            # Blokken en speler nog tekenen (bevroren beeld)
            for blok in blokken:
                teken_blok(blok[0], blok[1])
            speler.teken(scherm)
            teken_hud(score, snelheid, True, hoogste_score)
            teken_game_over(score, hoogste_score, score >= hoogste_score and score > 0)

        # --- Scherm vernieuwen ---
        pygame.display.flip()
        klok.tick(60)   # 60 frames per seconde


# Start het spel!
speel()
