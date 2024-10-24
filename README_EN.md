# WorkLogger - Work Time Tracker

## Project Description

The **Work Time Tracker** is a desktop application for tracking work hours. The application offers a simple user interface where users can log their work hours, activities, and start and end times.
Additionally, the app allows saving data in a JSON file and generating PDF reports.
Users can manage, edit, and delete work time entries, as well as view statistics such as total work hours and gross and net salary.

## Features

- **Add Work Time Entries**: Log workdays with start, end, activity, and worked hours.
- **Edit and Delete Entries**: Manage existing entries directly in the application.
- **Summary Statistics**: Displays total worked hours and calculates gross and net salary.
- **Save Function**: Work time entries are automatically saved in a JSON file and can be loaded at any time.
- **PDF Export**: Generate a PDF file with all work time entries.
- **Folder Selection**: Choose a save location for the PDF files.

## Installation and Usage
### Requirements

- **Python 3.6+**
- The following Python libraries need to be installed:
  - `tkinter`: For the user interface (usually pre-installed with Python)
  - `tkcalendar`: For the date input field
  - `fpdf`: For creating PDF files

### Installing Required Libraries

Run the following commands to install the dependencies:

```bash
pip install tkcalendar
pip install fpdf
