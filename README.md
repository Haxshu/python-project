# 📒 Contact Book Dashboard (Python Tkinter GUI)

A modern **Contact Book Dashboard Application** built using **Python + Tkinter GUI**. This project allows users to manage contacts with a beautiful dashboard interface, including search, sorting, and detailed contact views.

---

## 🌟 Project Overview

This Contact Book is not just a simple CLI tool — it is a **fully functional GUI-based dashboard application**.

It helps users:

* Store contact information
* Search and filter contacts
* View detailed profiles
* Perform CRUD operations with ease

---

## 🖥️ Dashboard Preview

The application features a **two-panel dashboard layout**:

### 📌 Left Sidebar

* 🔍 Search bar (real-time filtering)
* 📋 Contact list with scroll
* 📊 Contact count display

### 📌 Right Panel

* ➕ Add Contact
* ✏️ Edit Contact
* ❌ Delete Contact
* 📄 Contact detail view (with avatar & info)

---

## 🚀 Features

### 🔹 Contact Management

* ➕ Add new contact (Name, Phone, Email, Address, Notes)
* ✏️ Edit existing contact
* ❌ Delete contact with confirmation
* 📋 View all contacts in a list

### 🔹 Smart Dashboard

* 🔍 Live search (name, phone, email)
* 🔃 Sorting options:

  * Name ↑ / ↓
  * Newest / Oldest
* 📊 Contact count display

### 🔹 UI/UX Features

* 🎨 Modern dark theme UI
* 🧑 Avatar with initials
* 🪟 Popup dialog forms
* 🖱️ Double-click to edit contact
* 📱 Responsive window layout

### 🔹 Data Handling

* 💾 Data stored in `contacts.json`
* 🔄 Auto-load contacts on startup
* 📝 JSON structured storage

---

## 🛠️ Technologies Used

* **Python 3**
* **Tkinter (GUI Framework)**
* JSON (Data Storage)
* Regex (Validation)
* OS Module (File Handling)

---

## 📂 Project Structure

```bash
contact-book-dashboard/
│
├── main.py              # Main GUI application
├── contacts.json       # Stored contact data
└── README.md           # Documentation
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/contact-book-dashboard.git
```

### 2️⃣ Navigate to Folder

```bash
cd contact-book-dashboard
```

### 3️⃣ Run Application

```bash
python main.py
```

---

## 💡 How It Works

* The app loads contacts from `contacts.json`
* Displays them in a sidebar list
* Selecting a contact shows details on the right panel
* Users can:

  * Add → Opens form dialog
  * Edit → Modify selected contact
  * Delete → Remove contact with confirmation
* Changes are saved instantly

---

## 📊 Contact Data Format (JSON)

```json
{
  "name": "Niraj Singh",
  "phone": "+91 9876543210",
  "email": "niraj@google.com",
  "company": "ABC Ltd",
  "address": "Nagpur, India",
  "notes": "Friend from college"
}
```

---

## 🔒 Validation System

The application includes built-in validation:

* ✅ Phone number format check (regex)
* ✅ Email format validation
* ⚠ Required fields:

  * Name
  * Phone

---

## 🎨 UI Design Details

* Dark Theme Colors
* Accent highlights (Purple tones)
* Custom fonts (Georgia, Courier New)
* Card-based layout
* Hover effects on buttons

---

## 🧠 Key Concepts Used

* Object-Oriented Programming (OOP)
* Event-driven programming (Tkinter)
* File handling (JSON)
* Data filtering & sorting
* Input validation using Regex

---

## 📈 Advanced Features

* 🔍 Real-time search filtering
* 📊 Dynamic contact count
* 🔄 Sorting system
* 🧾 Detailed contact view panel
* 🖼️ Auto-generated initials avatar

---

## 🧪 Sample Workflow

1. Open application
2. Click **➕ New**
3. Enter contact details
4. Save contact
5. View in sidebar
6. Click contact → See details
7. Edit/Delete as needed

---

## 🎯 Future Improvements

* 🖥️ Add profile images upload
* 🗄️ SQLite database integration
* ☁️ Cloud sync (Firebase)
* 🔐 Login system
* 📤 Export contacts (CSV/Excel)
* 📱 Mobile version (Kivy/Flutter)

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a branch (`feature-update`)
3. Commit your changes
4. Push to GitHub
5. Open Pull Request

---


## 👨‍💻 Author

**Your Name**
GitHub: https://github.com/Haxshu

---
