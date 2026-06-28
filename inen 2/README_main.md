# 🌡 Temperature Converter

> **Prodigy Infotech Internship — Software Development Track | Task 01**
> Repository: `PRODIGY_SD_01`

A desktop temperature conversion app built with Python and Tkinter. Converts between Celsius, Fahrenheit, and Kelvin with a modern dark-themed GUI.

---

## Features

- Convert between Celsius, Fahrenheit, and Kelvin
- Shows all three unit equivalents at once
- Displays the conversion formula used
- Swap units with one click
- Absolute zero validation
- Press Enter to convert instantly
- Dark professional UI

---

## Project Structure

```
PRODIGY_SD_01/
├── main.py          # Application source
└── README.md
```

---

## Installation & Running

**Requirements:** Python 3.10+, Tkinter (bundled with Python)

**Linux (if Tkinter missing):**
```bash
sudo apt-get install python3-tk
```

**Run:**
```bash
python main.py
```

---

## Usage

1. Enter a temperature value in the input field
2. Select the **From** unit
3. Select the **To** unit
4. Click **Convert** or press **Enter**
5. Use **Swap Units** to reverse the conversion

---

## Conversion Formulas

| From | To | Formula |
|---|---|---|
| Celsius | Fahrenheit | (°C × 9/5) + 32 |
| Celsius | Kelvin | °C + 273.15 |
| Fahrenheit | Celsius | (°F − 32) × 5/9 |
| Fahrenheit | Kelvin | (°F − 32) × 5/9 + 273.15 |
| Kelvin | Celsius | K − 273.15 |
| Kelvin | Fahrenheit | (K − 273.15) × 9/5 + 32 |

---

## Author

**Vasudev Sivakumar**
Software Development Intern — Prodigy Infotech
GitHub: [@vasudevsivakum](https://github.com/vasudevsivakum)
