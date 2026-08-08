📰 News Agency

A web application for managing newspapers, publishers and topics.
The project allows editors to create, edit and manage news articles, assign publishers and organize content by topics.

## 🚀 Features

- User authentication
- CRUD operations for newspapers
- CRUD operations for topics
- CRUD operations for editors
- Search by title
- Pagination
- Responsive Bootstrap UI
- Admin panel
- Unit tests

---

## 🛠 Technologies

- Python 3.11
- Django 5
- SQLite
- Bootstrap 5
- Crispy Forms
- HTML/CSS

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/kbatrakov/news-agency.git
cd news-agency
```
Create virtual environment

```bash
python -m venv venv
```

Activate environment

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Apply migrations

```bash
python manage.py migrate
```

Create superuser

```bash
python manage.py createsuperuser
```

Run server

```bash
python manage.py runserver
```

---

## 📂 Project structure

```
news_agency/
│
├── news_agency/
├── publisher/
├── templates/
├── static/
├── manage.py
└── requirements.txt
```
---

## 🧪 Running tests

```bash
python manage.py test
```

---

---

## 👤 Author

Kyrylo Batrakov

GitHub:
https://github.com/kbatrakov
