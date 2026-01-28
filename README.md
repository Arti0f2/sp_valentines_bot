#  Charity Valentine Telegram Bot

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Aiogram](https://img.shields.io/badge/Aiogram-3.x-blueviolet?style=for-the-badge&logo=telegram)](https://aiogram.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-336791?style=for-the-badge&logo=postgresql)](https://neon.tech/)

A fully asynchronous Telegram bot designed for **Charity Valentine's Day campaigns**.
The core concept is simple: **Donations turn into Valentines.** Users donate to a charity jar (Monobank), receive internal currency (valentines), and send anonymous messages to their friends, which are delivered on February 14th.

---

##  Key Features

###  User Features
* **Anonymous Valentines:** Users can send messages to any Telegram user via their `@username`.
* **Scheduled Delivery:** Messages are stored and delivered specifically on Feb 14th (Morning/Afternoon/Evening slots).
* **Teaser Notifications:** If a user receives a valentine before the date, they get an instant notification ("You have a secret message waiting for Feb 14!").


###  Payments & Monobank Integration
* **Automated Top-up:** The bot polls the Monobank API to check for new transactions.
* **Comment System:** Users receive a unique ID to put in the payment comment for auto-verification.
* **Manual Verification:** If a user forgets the comment, they can send a screenshot to admins for manual approval.


###  Admin & Technical
* **Admin Panel:** Approve/Reject manual top-up requests.
* **Force Delivery:** Command `/force_delivery` to manually trigger message sending in case of scheduler failure.
* **Rate Limiting:** Intelligent queuing system to avoid Telegram "Flood Wait" bans during mass delivery.
* **PostgreSQL:** Robust data storage using SQLAlchemy + Asyncpg.

---

##  Tech Stack

* **Language:** Python 3.10+
* **Framework:** [Aiogram 3.x](https://docs.aiogram.dev/) (Asynchronous)
* **Database:** PostgreSQL (SQLAlchemy ORM + Alembic for migrations)
* **Banking:** Monobank Personal API
* **Scheduler:** Custom async loop for payment checking & delivery.


## 🚀 Installation & Setup

### 1. Create a virtual environment
First, create and activate a virtual environment to isolate dependencies:

```bash
# Create the environment
python -m venv venv

# Activate it:
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate



Install dependencies
pip install -r requirements.txt



Configuration
Create a .env file in the root directory:

# Telegram Bot Token
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# Database Connection (PostgreSQL)
DB_URL=postgresql+asyncpg://user:password@host:port/dbname

# Monobank Configuration
# You can use multiple accounts in settings.py, or define a main one here
MONO_TOKEN=your_monobank_token
JAR_ID=your_jar_id

# Admin IDs (comma separated)
ADMIN_IDS=123456789,987654321


Database Migration
Initialize the database tables using Alembic:
alembic upgrade head

### 5. Run the Bot
Start the application:

python main.py

```
---

## License
Developed for a charitable cause 

License: MIT

