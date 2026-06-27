# FitMart-Full-Stack-Fitness-Platform

# 📖 Overview

FitMart is a full-stack web application designed to help users manage their health and fitness in one place.

The system allows users to register, log in securely, manage fitness plans, book appointments, monitor health information, and interact with different system modules through dedicated dashboards.

The application demonstrates the integration of frontend development, backend programming, database management, authentication, and API usage.

---

# ✨ Features

## 👤 User Module

- User Registration
- Secure Login
- Profile Management
- Password Authentication

## 🏋️ Fitness Module

- Workout Plans
- Fitness Dashboard
- Exercise Recommendations
- Health Tracking

## 🩺 Healthcare Module

- Doctor Dashboard
- Appointment Booking
- Medical Information
- Patient Records

## 👨‍💼 Admin Module

- Admin Dashboard
- User Management
- Data Management
- System Monitoring

## 📧 Additional Features

- Email Notifications
- SQL Database Integration
- REST API Integration
- Session Management
- Responsive User Interface

---

# 🛠 Technology Stack

| Category | Technology |
|-----------|------------|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python |
| Database | SQLite / SQL |
| APIs | REST APIs |
| Authentication | Session-Based Authentication |
| IDE | Visual Studio Code |

---

# 🏗 System Architecture

```
                User

                  │

                  ▼

        HTML • CSS • JavaScript

                  │

                  ▼

           Python Backend

                  │

                  ▼

             REST APIs

                  │

                  ▼

           SQLite Database
```

---

# 📂 Project Structure

```
FitMart/
│
├── frontend/
│   ├── assets/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── HTML Pages
│
├── backend/
│   ├── main.py
│   ├── routes/
│   ├── models/
│   ├── email_service.py
│   ├── requirements.txt
│   └── .env.example
│
├── database/
│   └── schema.sql
│
├── screenshots/
│
├── docs/
│
├── README.md
├── LICENSE
└── .gitignore
```

---

# 🚀 Getting Started

## Prerequisites

- Python 3.x
- Git
- SQLite
- Visual Studio Code (Recommended)

---

## Installation

### Clone the repository

```bash
git clone https://github.com/YourUsername/FitMart-Full-Stack-Fitness-Platform.git
```

### Navigate into the project

```bash
cd FitMart-Full-Stack-Fitness-Platform
```

### Install dependencies

```bash
pip install -r backend/requirements.txt
```

### Configure Environment Variables

Create a `.env` file using the provided `.env.example`.

Example:

```
SECRET_KEY=your_secret_key
EMAIL=your_email
EMAIL_PASSWORD=your_password
DATABASE_URL=sqlite:///fitmart.db
```

### Initialize the Database

Run the SQL schema provided in the `database` folder.

---

## Run the Project

```bash
python backend/main.py
```

Open your browser and visit

```
http://localhost:5000
```

*(Update the port if your project uses a different one.)*

---



# 📚 Key Learning Outcomes

This project helped strengthen practical skills in:

- Full Stack Web Development
- Backend Development with Python
- Frontend Development
- SQL Database Design
- API Integration
- Authentication & Authorization
- CRUD Operations
- Session Management
- Software Engineering Practices
- Team Collaboration
- Version Control with Git & GitHub

---

# 🔒 Environment Variables

This project uses environment variables to protect sensitive information.

Create a `.env` file using `.env.example`.

Do **not** upload your actual `.env` file or API keys.

---

# 🚧 Future Improvements

- JWT Authentication
- Docker Support
- Cloud Database
- Payment Gateway
- AI Fitness Recommendation
- Mobile Application
- Deployment on AWS/Azure
- Real-Time Notifications

---

# 👨‍💻 Contributors

**Khizar Alam**

BS Software Engineering

Air University Islamabad

---

# 🤝 Contributing

Contributions are welcome.

If you'd like to improve this project, please fork the repository and submit a Pull Request.

---

# 📄 License

This project is licensed under the MIT License.

See the LICENSE file for more information.

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

It helps others discover the project and motivates future improvements.
