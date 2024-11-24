# <p align="center">Anleitung zur Nutzung der SWEB</p>
## Steuerung der Anwendung:
Die Anwendung verfügt über ein Hauptbedienfeld mit 5 Tasten pro Menü (insgesamt 10 Tasten): 
![MENU_1](https://github.com/forsenior/senior-os/blob/main/sweb/screens/sweb_menu1.png)
![MENU_2](https://github.com/forsenior/senior-os/blob/main/sweb/screens/sweb_menu2_de.png)
1. **Menü** - ermöglicht es Ihnen, zwischen zwei verschiedenen Teilen der Anwendung zu wechseln (Menü 1 und Menü 2).
2.	**Rote Taste mit weißem Kreuz** - dient zum Beenden der Anwendung.
3.	**Schaltflächen mit Website-Symbolen** - schneller Zugang zu einer bestimmten Website, ein Klick und die Website öffnet sich auf dem Bildschirm. 
4.	**Schaltfläche "Suchen"** - öffnet ein leeres Feld, in das der Benutzer eine beliebige Webadresse eingeben kann.

## Een website openen
- **Beschermingsniveau 1: Basisbescherming**
1. **Openen via menu:** Klik op een knop of pictogram in Menu 1/2 om de website direct te openen.
2. **Openen via Zoeken:**  Klik op de zoekknop, voer uw zoektekst in en de invoer wordt gecontroleerd aan de hand van een “zwarte lijst” en phishingdetectie met behulp van een neuraal netwerk.

- **Beschermingsniveau 2: Verbeterde bescherming**
1. **Openen via menu:** Klik op een knop of pictogram in Menu 1/2 om de website direct te openen.
2. **Openen via Zoeken:**  Klik op de zoekknop, voer je zoektekst in en de invoer wordt geverifieerd aan de hand van een witte lijst. Het systeem opent alleen URL's die overeenkomen met de invoer in de witte lijst.
  
- **Beschermingsniveau 3: maximale bescherming**
1. **Openen via menu:** Klik op een knop of pictogram in Menu 1/2 om de website direct te openen.
2. **Geen zoekopdracht:** De zoekknop wordt uitgeschakeld en de zoekfunctie is niet beschikbaar op dit beschermingsniveau.
   
## Waarschuwing voor phishingdetectie

- Phishing-detectie:
    - URL invoeren of website bezoeken: Wanneer de gebruiker een URL invoert of een website bezoekt, controleert het systeem of de URL is opgenomen in de zwarte lijst of via het neurale netwerk is gedetecteerd voor phishing.

- **Waarschuwingsmechanisme:**
    - Als een potentiële phishing-bedreiging wordt gedetecteerd, verandert de knop op de menubalk van kleur in rood om de gebruiker te waarschuwen voor het potentiële gevaar.

- **De waarschuwing negeren:**
    - Als de gebruiker de rode waarschuwing negeert en doorgaat met het invoeren van gegevens op de website, stuurt de app automatisch een e-mailmelding naar de bewaker om hen te informeren over de verdachte activiteit.

![phishing](https://github.com/forsenior/senior-os/blob/main/sweb/screens/sweb_phishing_de.png)
