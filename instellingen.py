# instellingen.py
# Alle instellingen van MennoTrash op één plek.

# --- Scherm ---
SCHERM_BREEDTE = 800
SCHERM_HOOGTE  = 400
SCHERM_TITEL   = "MennoTrash 🗑️"

# --- Grond ---
GROND_Y = 60       # Hoe hoog de grond is (in pixels vanaf de onderkant)

# --- Speler ---
SPELER_X      = 120     # Vaste x-positie van het vierkantje
SPELER_GROOT  = 40      # Hoe groot het vierkantje is (breedte en hoogte)
SPRING_KRACHT = 14      # Hoe hoog het vierkantje springt
ZWAARTEKRACHT = 0.6     # Hoe snel het vierkantje valt

# --- Blokken ---
BLOK_BREEDTE       = 30    # Hoe breed een blok is
BLOK_MIN_HOOGTE    = 40    # Minimale hoogte van een blok
BLOK_MAX_HOOGTE    = 100   # Maximale hoogte van een blok
BEGIN_SNELHEID     = 5     # Hoe snel de blokken beginnen te bewegen
SNELHEID_TOENAME   = 0.3   # Hoe veel sneller het wordt per 10 seconden

# --- Kleuren ---
ACHTERGROND_KLEUR = (30, 30, 50)       # Donkerblauw
GROND_KLEUR       = (60, 200, 60)      # Groen
GROND_RAND_KLEUR  = (40, 140, 40)      # Donkerder groen voor rand
SPELER_KLEUR      = (255, 220, 50)     # Geel vierkantje
OOG_KLEUR         = (30, 30, 30)       # Donker voor de ogen
BLOK_KLEUR        = (200, 60, 60)      # Rood blok
BLOK_RAND_KLEUR   = (140, 20, 20)      # Donkere rand van blok
SCORE_KLEUR       = (255, 255, 255)    # Witte tekst
