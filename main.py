# main.py
# MennoTrash — Spring over de blokken en kom zo ver mogelijk!
# Druk op SPATIE om te springen.

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


def teken_grond():
    """Teken een groene grond-balk onderaan."""
    grond_rect = (0, SCHERM_HOOGTE - GROND_Y, SCHERM_BREEDTE, GROND_Y)
    pygame.draw.rect(scherm, GROND_KLEUR, grond_rect)
    # Groene rand bovenop de grond
    pygame.draw.rect(scherm, GROND_RAND_KLEUR,
                     (0, SCHERM_HOOGTE - GROND_Y, SCHERM_BREEDTE, 6))
    # Graspikjes
    for gx in range(0, SCHERM_BREEDTE, 30):
        offset = (gx * 7) % 10   # Beetje variatie
        pygame.draw.polygon(scherm, (80, 220, 80), [
            (gx + offset,      SCHERM_HOOGTE - GROND_Y),
            (gx + offset + 6,  SCHERM_HOOGTE - GROND_Y),
            (gx + offset + 3,  SCHERM_HOOGTE - GROND_Y - 9),
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
    return speler, blokken, teller, score, snelheid, volgende_blok


# =============================================
# HOOFDLUS
# =============================================

def speel():
    """De hoofdlus van het spel."""
    hoogste_score = 0
    status = "start"      # "start", "spelen", "game_over"

    speler, blokken, teller, score, snelheid, volgende_blok = reset_spel()

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
                        speler, blokken, teller, score, snelheid, volgende_blok = reset_spel()
                        status = "spelen"

        # --- Achtergrond tekenen ---
        teken_achtergrond(teller)
        teken_grond()

        if status == "start":
            # Teken een voorbeeldspeler op het startscherm
            speler.teken(scherm)
            teken_start_scherm()

        elif status == "spelen":
            teller += 1

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
