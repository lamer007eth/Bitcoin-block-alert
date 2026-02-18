# Bitcoin Block Alert
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Bitcoin](https://img.shields.io/badge/Bitcoin-BTC-orange)
![Alerts](https://img.shields.io/badge/Alerts-Sound%20%2B%20Telegram-2CA5E0)
![Type](https://img.shields.io/badge/Type-Monitoring-purple)
![API](https://img.shields.io/badge/API-REST-grey)

Bitcoin block monitoring bot built with Python.
Alerts user when a specified block height is mined.

---

## ⚙️ Features

* Tracks latest Bitcoin blocks in real time
* Shows time between blocks
* Displays recommended fastest fee
* 🔊 Sound alert notification
* 📩 Telegram alert notification

---

## 📦 Project structure

```
bitcoin-block-alert/
│
├─ btc_block_alert.py        # Sound alert version
├─ btc_block_telegram.py     # Telegram alert version
├─ alert.mp3
├─ .env.example
├─ requirements.txt
└─ README.md
```

---

## 🚀 Setup

Install dependencies:

```
pip install -r requirements.txt
```

Create `.env` file based on `.env.example` and fill your data.

---

## ▶️ Usage

Sound alert:

```
python btc_block_alert.py
```

Telegram alert:

```
python btc_block_telegram.py
```

---

## 🌐 API Used

* https://mempool.space/api/blocks
* https://mempool.space/api/v1/fees/recommended
