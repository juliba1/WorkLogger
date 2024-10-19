import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
import json
import os
from fpdf import FPDF
import subprocess


class ArbeitszeitTracker:
    def __init__(self, master):
        self.master = master
        master.title("Arbeitszeit Tracker")
        master.geometry("1100x750")  # Größeres Fenster, um Platz für die neuen Informationen zu bieten

        # Frame für Eingabefelder
        frame_entries = tk.Frame(master)
        frame_entries.pack(pady=10)

        self.label_tag = tk.Label(frame_entries, text="Tag:")
        self.label_tag.grid(row=0, column=0, padx=5, pady=5)

        self.entry_tag = DateEntry(frame_entries, width=47, background='darkblue',
                                   foreground='white', borderwidth=1, date_pattern='dd.mm.yyyy')
        self.entry_tag.grid(row=0, column=1, padx=5, pady=5)

        self.label_beginn = tk.Label(frame_entries, text="Beginn (HH:MM):")
        self.label_beginn.grid(row=1, column=0, padx=5, pady=5)

        self.entry_beginn = tk.Entry(frame_entries, width=50)
        self.entry_beginn.grid(row=1, column=1, padx=5, pady=5)

        self.label_ende = tk.Label(frame_entries, text="Ende (HH:MM):")
        self.label_ende.grid(row=2, column=0, padx=5, pady=5)

        self.entry_ende = tk.Entry(frame_entries, width=50)
        self.entry_ende.grid(row=2, column=1, padx=5, pady=5)

        self.label_tatigkeit = tk.Label(frame_entries, text="Tätigkeit:")
        self.label_tatigkeit.grid(row=3, column=0, padx=5, pady=5)

        self.entry_tatigkeit = tk.Entry(frame_entries, width=50)
        self.entry_tatigkeit.grid(row=3, column=1, padx=5, pady=5)

        # Buttons zum Bearbeiten und Löschen von Einträgen
        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)

        self.button_add = tk.Button(button_frame, text="Eintrag hinzufügen", command=self.add_entry, bg='#42ed53', fg='white', bd=0)
        self.button_add.grid(row=0, column=0, padx=5)

        self.button_edit = tk.Button(button_frame, text="Eintrag bearbeiten", command=self.edit_entry, bg='#ff9036', fg='white', bd=0)
        self.button_edit.grid(row=0, column=1, padx=5)

        self.button_delete = tk.Button(button_frame, text="Eintrag löschen", command=self.delete_entry, bg='#c93232', fg='white', bd=0)
        self.button_delete.grid(row=0, column=2, padx=5)

        self.button_delete_all = tk.Button(button_frame, text="Alle Einträge löschen", command=self.delete_all_entries, bg='#ff0000', fg='white', bd=0)
        self.button_delete_all.grid(row=0, column=3, padx=5)

        # Tabelle zur Anzeige der Einträge
        columns = ("Tag", "Beginn", "Ende", "Tätigkeit", "Gearbeitete Zeit")
        self.tree = ttk.Treeview(master, columns=columns, show='headings')
        self.tree.heading("Tag", text="Tag")
        self.tree.heading("Beginn", text="Beginn")
        self.tree.heading("Ende", text="Ende")
        self.tree.heading("Tätigkeit", text="Tätigkeit")
        self.tree.heading("Gearbeitete Zeit", text="Gearbeitete Zeit (Stunden)")
        self.tree.pack(padx=15, pady=10, fill='both', expand=True)

        # Frame für Speicherpfad
        frame_path = tk.Frame(master)
        frame_path.pack(pady=10)

        self.button_select_folder = tk.Button(frame_path, text="Speicherort auswählen", command=self.select_folder)
        self.button_select_folder.grid(row=0, column=0, padx=5)

        self.entry_save_folder = tk.Entry(frame_path, width=50, state='readonly')
        self.entry_save_folder.grid(row=0, column=1, padx=5)

        self.button_open_folder = tk.Button(frame_path, text="Verzeichnis öffnen", command=self.open_folder)
        self.button_open_folder.grid(row=0, column=2, padx=5)
        
        self.button_pdf = tk.Button(master, text="PDF erstellen", command=self.create_pdf, bg='#0bbfb9', fg='white', bd=0)
        self.button_pdf.pack(pady=10)

        # Bereich zur Anzeige der Berechnungen in einer Zeile
        self.summary_frame = tk.Frame(master)
        self.summary_frame.pack(pady=10, padx=20)  # Padding hinzugefügt

        self.label_summary = tk.Label(self.summary_frame, text="", font=('Arial', 12))
        self.label_summary.pack()

        self.entries = []
        self.save_folder = ""  # Variable, um den Pfad des ausgewählten Ordners zu speichern
        self.data_file = "arbeitszeit_daten.json"  # Datei zum Speichern der Einträge

        # Lade gespeicherte Einträge
        self.load_entries()
        self.update_summary()

        # Übersetzungstabelle für die Monate
        self.month_names = {
            1: "Januar", 2: "Februar", 3: "März", 4: "April", 5: "Mai", 6: "Juni",
            7: "Juli", 8: "August", 9: "September", 10: "Oktober", 11: "November", 12: "Dezember"
        }

    def open_folder(self):
        """Öffnet den ausgewählten Speicherort im Dateiexplorer."""
        if self.save_folder:
            try:
                # Öffne den Ordner im Dateiexplorer
                subprocess.Popen(f'explorer {os.path.realpath(self.save_folder)}')
            except Exception as e:
                messagebox.showerror("Fehler", f"Das Verzeichnis konnte nicht geöffnet werden: {e}")
        else:
            messagebox.showwarning("Kein Verzeichnis", "Es wurde noch kein Speicherort ausgewählt.")

    def add_entry(self):
        try:
            tag = self.entry_tag.get()
            beginn = datetime.strptime(self.entry_beginn.get(), "%H:%M")
            ende = datetime.strptime(self.entry_ende.get(), "%H:%M")
            tatigkeit = self.entry_tatigkeit.get()

            # Gearbeitete Zeit in Dezimalstunden umrechnen
            delta = ende - beginn
            gearbeitete_zeit = delta.seconds / 3600

            entry = {
                "Tag": tag,
                "Beginn": beginn.strftime("%H:%M"),
                "Ende": ende.strftime("%H:%M"),
                "Tätigkeit": tatigkeit,
                "Gearbeitete Zeit": gearbeitete_zeit
            }

            self.entries.append(entry)
            self.save_entries()  # Speichere Einträge nach Hinzufügen eines neuen Eintrags
            self.update_treeview()  # Aktualisiere die Tabelle
            self.update_summary()  # Aktualisiere die Zusammenfassung
            
            self.clear_entries()
        except ValueError as e:
            messagebox.showerror("Fehler", f"Ungültiges Zeitformat: {e}")

    def clear_entries(self):
        self.entry_tag.set_date(datetime.now())
        self.entry_beginn.delete(0, tk.END)
        self.entry_ende.delete(0, tk.END)
        self.entry_tatigkeit.delete(0, tk.END)

    def delete_all_entries(self):
        confirm = messagebox.askyesno("Alle Einträge löschen",
                                      "Sind Sie sicher, dass Sie alle Einträge löschen möchten?")
        if confirm:
            self.entries.clear()  # Alle Einträge löschen
            self.save_entries()  # Änderungen speichern
            self.update_treeview()  # Tabelle aktualisieren
            self.update_summary()  # Zusammenfassung aktualisieren

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.save_folder = folder
            self.entry_save_folder.config(state='normal')
            self.entry_save_folder.delete(0, tk.END)
            self.entry_save_folder.insert(0, folder)
            self.entry_save_folder.config(state='readonly')
            self.save_entries()  # Speicherort in der JSON-Datei aktualisieren
            messagebox.showinfo("Ordner ausgewählt", f"PDF wird gespeichert in: {folder}")

    def create_pdf(self):
        if not self.save_folder:
            messagebox.showwarning("Kein Speicherort", "Bitte wählen Sie einen Speicherort aus.")
            return

        if not self.entries:
            messagebox.showwarning("Keine Einträge", "Keine Einträge zum Erstellen der PDF vorhanden.")
            return

        # Sortiere Einträge nach Datum und Uhrzeit
        self.entries.sort(
            key=lambda x: (datetime.strptime(x["Tag"], "%d.%m.%Y"), datetime.strptime(x["Beginn"], "%H:%M")))

        # Finde den Monat aus den Einträgen
        last_entry_date = datetime.strptime(self.entries[-1]["Tag"], "%d.%m.%Y")
        month_number = last_entry_date.month
        month_name = self.month_names[month_number]  # Monatname auf Deutsch
        year = last_entry_date.year

        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)

        # Titel
        pdf.cell(0, 10, f'Arbeitsnachweis {month_name}', 0, 1, 'L')

        # Tabellenüberschrift
        pdf.set_font('Arial', 'B', 10)
        header_height = 5  # Höhe der Tabellenüberschrift

        # Hintergrundfarbe für Spaltenköpfe
        pdf.set_fill_color(2, 59, 112)
        pdf.set_text_color(255, 255, 255)  # Weiß

        # Spaltenbreite
        col_widths = [30, 30, 30, 60, 110]  # Breiten der Spalten

        pdf.cell(col_widths[0], header_height, 'Datum', 1, fill=True)
        pdf.cell(col_widths[1], header_height, 'Startzeit', 1, fill=True)
        pdf.cell(col_widths[2], header_height, 'Ende', 1, fill=True)
        pdf.cell(col_widths[3], header_height, 'Gearbeitete Zeit (Stunden)', 1, fill=True)
        pdf.cell(col_widths[4], header_height, 'Tätigkeit', 1, ln=1, fill=True)

        # Tabelleninhalte
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(0, 0, 0)  # Schwarz
        total_hours = 0
        header_height += 1

        # Zählen, wie oft jedes Datum vorkommt
        date_counts = {}
        for entry in self.entries:
            if entry["Tag"] in date_counts:
                date_counts[entry["Tag"]] += 1
            else:
                date_counts[entry["Tag"]] = 1

        # Set zur Verfolgung, ob das Datum bereits ausgegeben wurde
        printed_dates = set()

        # Variable für abwechselnde Hintergrundfarben
        alternate_color = False

        # Iteriere über die Einträge und erstelle die Tabelle
        for i, entry in enumerate(self.entries):
            # Prüfe, ob das Datum bereits ausgegeben wurde
            if entry["Tag"] not in printed_dates:
                # Ändere die Hintergrundfarbe basierend auf dem Wechsel
                alternate_color = not alternate_color
                printed_dates.add(entry["Tag"])
                pdf.set_fill_color(220, 220, 220) if alternate_color else pdf.set_fill_color(255, 255, 255)

                # Datum einmal pro Block drucken
                pdf.cell(col_widths[0], header_height * date_counts[entry["Tag"]], entry["Tag"], 1, fill=True)
            else:
                # Wenn das Datum bereits gedruckt wurde, leere Zelle hinzufügen
                pdf.cell(col_widths[0], header_height, "", 0)

            # Zellen für den Rest der Einträge
            pdf.cell(col_widths[1], header_height, entry["Beginn"], 1, fill=True)
            pdf.cell(col_widths[2], header_height, entry["Ende"], 1, fill=True)
            pdf.cell(col_widths[3], header_height, f"{entry['Gearbeitete Zeit']:.2f}", 1, fill=True)
            pdf.cell(col_widths[4], header_height, entry["Tätigkeit"], 1, ln=1, fill=True)

            total_hours += entry["Gearbeitete Zeit"]

        # Füge Zusammenfassung hinzu
        pdf.cell(0, 2, '', 0, ln=1)  # Leerzeile
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 10, f"Gesamte gearbeitete Stunden: {total_hours:.2f}", 0, 1, 'L')

        # Dateinamen erstellen
        pdf_filename = os.path.join(self.save_folder,
                                    f"{last_entry_date.strftime('%m')}-{month_name}-Arbeitsnachweis-{year}.pdf")
        pdf.output(pdf_filename)
        messagebox.showinfo("PDF", f"PDF wurde erstellt und gespeichert in {pdf_filename}.")

    def save_entries(self):
        """Speichert die Einträge und den Speicherort in einer JSON-Datei."""
        data = {
            "entries": self.entries,
            "save_folder": self.save_folder
        }
        with open(self.data_file, 'w') as file:
            json.dump(data, file)

    def load_entries(self):
        """Lädt die Einträge und den Speicherort aus einer JSON-Datei, falls diese existiert."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as file:
                    data = json.load(file)

                # Sicherstellen, dass die Daten ein Dictionary sind
                if isinstance(data, dict):
                    self.entries = data.get("entries", [])
                    self.save_folder = data.get("save_folder", "")
                    self.entry_save_folder.config(state='normal')
                    self.entry_save_folder.delete(0, tk.END)
                    self.entry_save_folder.insert(0, self.save_folder)
                    self.entry_save_folder.config(state='readonly')
                    self.update_treeview()
                    self.update_summary()
                else:
                    raise ValueError("Unerwartetes Format in der JSON-Datei.")
            except (json.JSONDecodeError, ValueError) as e:
                messagebox.showerror("Fehler", f"Fehler beim Laden der Einträge: {e}")
        else:
            self.entries = []
            self.save_folder = ""
            self.update_treeview()
            self.update_summary()

    def update_treeview(self):
        """Aktualisiert die Tabelle mit den Einträgen."""
        # Lösche alle vorhandenen Einträge in der Tabelle
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Sortiere Einträge nach Datum und Uhrzeit
        self.entries.sort(
            key=lambda x: (datetime.strptime(x["Tag"], "%d.%m.%Y"), datetime.strptime(x["Beginn"], "%H:%M")))

        # Füge die gespeicherten Einträge hinzu
        for entry in self.entries:
            self.tree.insert("", "end", values=(
                entry["Tag"], entry["Beginn"], entry["Ende"], entry["Tätigkeit"], f"{entry['Gearbeitete Zeit']:.2f}"
            ))

    def update_summary(self):
        """Aktualisiert die Zusammenfassungsanzeige in einer Zeile."""
        total_hours = sum(entry["Gearbeitete Zeit"] for entry in self.entries)
        brutto_gehalt = total_hours * 21
        netto_gehalt = brutto_gehalt * 0.907

        summary_text = (f"Gesamte gearbeitete Stunden: {total_hours:.2f} | "
                        f"Brutto Gehalt: {brutto_gehalt:.2f} EUR | "
                        f"Netto Gehalt: {netto_gehalt:.2f} EUR")

        self.label_summary.config(text=summary_text)

    def edit_entry(self):
        """Bearbeitet den ausgewählten Eintrag."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie einen Eintrag zum Bearbeiten aus.")
            return

        item = self.tree.item(selected_item)
        entry = item['values']

        # Setze die Eingabefelder auf die Werte des ausgewählten Eintrags
        self.entry_tag.set_date(datetime.strptime(entry[0], "%d.%m.%Y"))
        self.entry_beginn.delete(0, tk.END)
        self.entry_beginn.insert(0, entry[1])
        self.entry_ende.delete(0, tk.END)
        self.entry_ende.insert(0, entry[2])
        self.entry_tatigkeit.delete(0, tk.END)
        self.entry_tatigkeit.insert(0, entry[3])

        # Entferne den Eintrag aus der Liste, um ihn zu ersetzen
        self.entries = [e for e in self.entries if
                        e["Tag"] != entry[0] or e["Beginn"] != entry[1] or e["Ende"] != entry[2] or e["Tätigkeit"] !=
                        entry[3]]
        self.save_entries()  # Speichere den Zustand nach Entfernen des alten Eintrags

        self.button_add.config(command=self.save_edited_entry)  # Ändere die Funktion des Hinzufügen-Buttons

    def save_edited_entry(self):
        """Speichert den bearbeiteten Eintrag."""
        try:
            tag = self.entry_tag.get()
            beginn = datetime.strptime(self.entry_beginn.get(), "%H:%M")
            ende = datetime.strptime(self.entry_ende.get(), "%H:%M")
            tatigkeit = self.entry_tatigkeit.get()

            # Gearbeitete Zeit in Dezimalstunden umrechnen
            delta = ende - beginn
            gearbeitete_zeit = delta.seconds / 3600

            entry = {
                "Tag": tag,
                "Beginn": beginn.strftime("%H:%M"),
                "Ende": ende.strftime("%H:%M"),
                "Tätigkeit": tatigkeit,
                "Gearbeitete Zeit": gearbeitete_zeit
            }

            self.entries.append(entry)
            self.save_entries()  # Speichere Einträge nach Bearbeitung eines Eintrags
            self.update_treeview()  # Aktualisiere die Tabelle
            self.update_summary()  # Aktualisiere die Zusammenfassung
            messagebox.showinfo("Eintrag", "Eintrag bearbeitet!")
            self.clear_entries()
            self.button_add.config(command=self.add_entry)  # Setze die Funktion des Hinzufügen-Buttons zurück
        except ValueError as e:
            messagebox.showerror("Fehler", f"Ungültiges Zeitformat: {e}")

    def delete_entry(self):
        """Löscht den ausgewählten Eintrag."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie einen Eintrag zum Löschen aus.")
            return

        item = self.tree.item(selected_item)
        entry = item['values']

        # Entferne den Eintrag aus der Liste
        self.entries = [e for e in self.entries if
                        e["Tag"] != entry[0] or e["Beginn"] != entry[1] or e["Ende"] != entry[2] or e["Tätigkeit"] !=
                        entry[3]]
        self.save_entries()  # Speichere den Zustand nach Entfernen des Eintrags
        self.update_treeview()  # Aktualisiere die Tabelle
        self.update_summary()  # Aktualisiere die Zusammenfassung
        messagebox.showinfo("Eintrag", "Eintrag gelöscht!")


root = tk.Tk()
my_gui = ArbeitszeitTracker(root)
root.mainloop()
