# 👗 Clothing Rental Backend

A backend system for a clothing rental application built with Django and Django REST Framework.

---

## 🚀 Overview

This project provides backend services for a clothing rental platform, focusing on user management, authentication, and rental system foundations.

The architecture is modular and designed for scalability and future expansion of rental business logic.

---

## 🧰 Tech Stack

- Python
- Django
- Django REST Framework (DRF)
- PostgreSQL
- JWT Authentication (SimpleJWT)

---

## ⚙️ Key Features

### 🔐 Authentication System
- OTP-based login (phone number authentication)
- JWT token generation (access & refresh tokens)
- Secure user authentication flow

---

### 👤 User Management
- Custom user model
- Phone-based authentication system
- User profile handling

---

### 🔄 Rental System (Core Structure)
- Base structure for clothing rental logic
- Ready for implementing:
  - rental orders
  - booking periods
  - availability tracking

---

### 🗄️ Database
- PostgreSQL database
- Designed for scalability and production use

---

### 🔌 API Architecture
- RESTful API design using Django REST Framework
- Modular app structure for maintainability
- Clean separation of business logic

---

## 📂 Project Structure

- apps/
  - users
  - (other modules based on rental logic)

---

## ⚙️ Installation

```bash
git clone https://github.com/t-zare-Programmer/clothing_rental.git
cd clothing_rental

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
