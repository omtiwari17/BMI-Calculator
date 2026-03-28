# 🧮 BMI Calculator

A desktop BMI Calculator built with Python and Tkinter. Calculates your BMI, stores history in a local SQLite database, and visualizes trends with Matplotlib.

---

## Features

- **BMI Calculation** - Instant result with category (Underweight / Normal / Overweight / Obese)
- **Persistent Storage** - All records saved to a local SQLite database (`bmi_data.db`)
- **History Viewer** - Browse all past records in a sortable table
- **Delete Records** - Remove individual entries from history
- **BMI Trend Graph** - Line chart showing BMI progression across entries

## Requirements

- Python 3.7+
- `matplotlib`

Install dependencies:

```bash
pip install matplotlib
```

> `tkinter` and `sqlite3` are included in Python's standard library — no extra install needed.

## Setup & Run

```bash
# Clone the repo
git clone https://github.com/omtiwari17/<repo-name>.git
cd <repo-name>

# Install dependencies
pip install matplotlib

# Run the app
python bmi_calculator.py
```

## How to Use

1. Enter your **Name**, **Height** (in meters), and **Weight** (in kg)
2. Click **Calculate BMI** your result and category appear instantly
3. Click **View History** to browse all saved records; select any row and click **Delete Selected Record** to remove it
4. Click **View BMI Trend** to see a line graph of all recorded BMI values

## BMI Categories

| BMI Range | Category |
|---|---|
| < 18.5 | Underweight |
| 18.5 – 24.9 | Normal weight |
| 25 – 29.9 | Overweight |
| ≥ 30 | Obese |

## Project Structure

```
bmi-calculator/
├── bmi_calculator.py   # Main application
├── bmi_data.db         # Auto-generated SQLite database
└── README.md
```

## Tech Stack

| Layer | Technology |
|---|---|
| GUI | Tkinter (Python stdlib) |
| Database | SQLite3 (Python stdlib) |
| Charts | Matplotlib |
| Language | Python 3 |

---

<sub>Built by Om Tiwari
