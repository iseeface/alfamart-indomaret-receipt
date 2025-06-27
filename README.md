# Receipt Generator GUI

<p align="center">
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Black code style"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.7%2B-blue.svg" alt="Python version"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT license"></a>
</p>

This is a Python-based application that mimics the style and layout of receipts commonly printed in stores like Alfamart or Indomaret.

---

## 📋 Table of Contents

- [Features](#%EF%B8%8F-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Development](#-development)
- [Contributing](#-contributing)
- [License](#-license)

---

## ⚙️ Features

- GUI built using `Tkinter`.
- Receipt output in PDF format via `fpdf`.
- Dynamic item entry with quantity, price, and discount.
- Built-in 11% VAT (PPN) calculation.
- Manual or auto-generated NPWP and receipt number (BON).
- Support for both `Tunai` (Cash) and `Debit` payment methods.
- Input validations to prevent empty or invalid fields.
- PDF output is formatted to match real receipt width (80mm).

---

## 🛠 Installation

### Requirements
- Python 3.7 or later

### Quick Start
Install dependencies
```bash
pip install -r requirements.txt
```
Run the application
```bash
python main.py
```

---

## 🛠 Usage

1. Fill in store details (name, address, NPWP, BON, cashier).
2. Add item rows: name, quantity, price, discount.
3. Set payment method and amount.
4. Choose PPN option and timestamp (manual or auto).
5. Click "Cetak Struk" to save a PDF receipt.

---

## 📁 Project Structure
```
project/
├── main.py               # Entry point launcher
├── struk_gui.py          # Main GUI application
├── pdf/
│   ├── generator.py      # PDF generation class
│   └── formatter.py      # Format helpers (rupiah, NPWP, BON)
├── requirements.txt      # Dependency list
├── setup.py              # Installation metadata
├── README.md             # Project documentation
```

---

## 📌 Development

All code is formatted using [Black](https://github.com/psf/black):
```bash
black .
```

To install the project locally:
```bash
pip install .
```

---

## 🤝 Contributing

Contributions are welcome! To contribute:
1. Fork this repository.
2. Create a new branch (`git checkout -b feature-xyz`).
3. Make your changes.
4. Submit a pull request.

Please follow PEP8 style and use `black` to format your code.

---

## 📜 License

This repository is licensed under the [MIT License](LICENSE).
