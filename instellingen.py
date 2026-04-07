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
# Blokken zijn nu platte platforms die op verschillende hoogtes vliegen!
BLOK_BREEDTE     = 80    # Blokken zijn breder zodat je erop kunt staan
BLOK_HOOGTE      = 20    # Plat platform (niet meer hoge muren)
BLOK_MIN_VLIEG_Y = 0     # Minimale vlieghoogte (op de grond)
BLOK_MAX_VLIEG_Y = 160   # Maximale vlieghoogte
BEGIN_SNELHEID   = 5
SNELHEID_TOENAME = 0.3

# --- Kleuren ---
ACHTERGROND_KLEUR = (30, 30, 50)
GROND_KLEUR       = (60, 200, 60)
GROND_RAND_KLEUR  = (40, 140, 40)
SPELER_KLEUR      = (255, 220, 50)
OOG_KLEUR         = (30, 30, 30)
BLOK_KLEUR        = (200, 60, 60)
BLOK_RAND_KLEUR   = (140, 20, 20)
SCORE_KLEUR       = (255, 255, 255)
