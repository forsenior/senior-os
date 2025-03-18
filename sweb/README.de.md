# Webbrowser für Senioren und geistig Behinderte

## Anwendungsübersicht

Bei diesem Projekt handelt es sich um einen auf Senioren zugeschnittenen Webbrowser, der mit PyQt5 entwickelt wurde und dessen Schwerpunkt auf Barrierefreiheit, Einfachheit und Sicherheit liegt. 
Sein Ziel ist es, eine benutzerfreundlichere Umgebung für ältere Erwachsene zu schaffen, indem er Funktionen wie verbesserte Textlesbarkeit, intuitive Navigation, 
Audiounterstützung, mehrsprachige Optionen und robuste Sicherheitsmaßnahmen zum Schutz vor Phishing-Websites. 
Nachstehend finden Sie das Designkonzept für den Webbrowser:

## MENU1 Überblick
MENU1 bietet eine benutzerfreundliche Oberfläche mit vier großen Schaltflächen fester Größe, die eine einfache Navigation, insbesondere für Senioren, ermöglichen.

<img src=„screens/sweb_screen_1.png“ width=„900“ />

Tasten-Aktionen:

1. MENU1-Taste: Schaltet die Menüleiste auf MENU2 um.
2. Schaltfläche „Beenden“: Schließt die Anwendung.
3. Website-Schaltflächen (3): Öffnen Links zu vordefinierten Websites.
   
## MENU2 Überblick
MENU2 enthält fünf Schaltflächen mit den folgenden Funktionen:

<img src=„screens/sweb_screen_2.png“ width=„900“ />

Tasten-Aktionen:

1. MENU2-Taste: Schaltet die Menüleiste zurück zu MENU1.
2. Website-Schaltflächen (3): Öffnen Links zu vordefinierten Websites.
3. Schaltfläche Suchen: Öffnet eine Suchleiste für Benutzeranfragen.

## Erkennung von Phishing-Websites
Diese Funktion ist das Herzstück unserer App. Sie warnt Nutzer, wenn eine Website möglicherweise eine Phishing-Website ist.

<img src=„screens/sweb_screen_3.png“ width=„900“ />

- Phishing-Warnung: Wenn der Benutzer eine bekannte Phishing-URL eingibt, färbt sich der Hintergrund der Symbolleiste rot, um insbesondere für ältere Menschen gut sichtbar zu sein.

Weitere Details zur Funktionsweise des Phishing-Detektors finden Sie in der Dokumentation.

## Installation

Stellen Sie sicher, dass Sie Python3 oder pip auf Ihrem System installiert haben.
Folgen Sie diesen Schritten, um den Webbrowser im FEDORA-Betriebssystem einzurichten:

```bash
## Installieren Sie die erforderlichen Python-Pakete mit dnf, wenn Sie Fedora verwenden
sudo dnf install python3

# Projekt-Repository klonen
git clone https://github.com/forsenior/senior-os

# Installiere die Anforderungen aus der requirements.txt im sweb-Verzeichnis
py -m pip install -r anforderungen.txt

```
      

## Das Demonstrationsvideo

https://github.com/user-attachments/assets/88fbb138-6467-47d3-ad12-a0fb98515719




# Wie man etwas beiträgt
Fühlen Sie sich frei, Pull-Requests einzureichen oder Fragen zu stellen, wenn Sie auf Probleme stoßen oder Vorschläge für Verbesserungen haben.

## Lizenz
Dieses Projekt ist unter der MIT-Lizenz lizenziert.

Übersetzt mit DeepL.com (kostenlose Version)
