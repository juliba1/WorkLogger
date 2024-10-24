# WorkLogger - Arbeitszeit Tracker

## Projektbeschreibung

Der **Arbeitszeit Tracker** ist eine Desktop-Anwendung zur Verfolgung von Arbeitszeiten. Die Anwendung bietet eine einfache Benutzeroberfläche, in der Benutzer ihre Arbeitszeiten, Tätigkeiten sowie Start- und Endzeiten eintragen können.
Zusätzlich ermöglicht die App das Speichern der Daten in einer JSON-Datei und die Generierung von PDF-Berichten.
Der Benutzer kann die Arbeitszeitdaten verwalten, bearbeiten und löschen sowie Statistiken wie Gesamtarbeitszeit, Brutto- und Nettogehalt anzeigen lassen.

## Features

- **Arbeitszeiteinträge hinzufügen**: Trage Arbeitstage mit Beginn, Ende, Tätigkeit und gearbeiteter Zeit ein.
- **Bearbeiten und Löschen von Einträgen**: Verwalte bestehende Einträge direkt in der Anwendung.
- **Zusammenfassungsstatistik**: Zeigt die gesamten gearbeiteten Stunden und berechnet Brutto- und Nettogehalt.
- **Speicherfunktion**: Arbeitszeiteinträge werden automatisch in einer JSON-Datei gespeichert und können jederzeit geladen werden.
- **PDF-Export**: Generiere eine PDF-Datei mit allen Arbeitszeiteinträgen.
- **Ordnerauswahl**: Wähle einen Speicherort für die PDF-Dateien aus.

## Installation und Verwendung
### Voraussetzungen

- **Python 3.6+**
- Die folgenden Python-Bibliotheken müssen installiert sein:
  - `tkinter`: Für die Benutzeroberfläche (ist normalerweise in Python vorinstalliert)
  - `tkcalendar`: Für das Datumseingabefeld
  - `fpdf`: Für die Erstellung von PDF-Dateien

### Installation der benötigten Bibliotheken

Führe die folgenden Befehle aus, um die Abhängigkeiten zu installieren:

```bash
pip install tkcalendar
pip install fpdf
