# TaskMaster

TaskMaster is a modern, premium task management application built with **Django**. It features a beautiful **Glassmorphism UI**, interactive dashboards, productivity tracking, and a robust trash bin system.

![TaskMaster Logo](static/images/logo.svg)
*(You can replace this path with a screenshot of your dashboard later: `static/images/screenshot.png`)*

## 🌟 Key Features

* **📊 Interactive Dashboard:** Get an at-a-glance view of Total, Completed, and In-Progress tasks. Includes a visual **Productivity Trend Chart** powered by Chart.js.
* **✅ Task Management:** Create, Read, Update, and Complete tasks with ease.
* **🏷️ Categorization & Priority:** Organize tasks by categories (Work, Personal, School) and set priorities (High, Medium, Low) with visual badges.
* **🗑️ Smart Trash Bin:** Deleted tasks are moved to a Trash Bin where they can be **Restored** or **Permanently Deleted**.
* **🔍 Sorting & Filtering:** Sort tasks by "Newest", "Recently Updated", or "Urgency" (Due Date).
* **✨ Premium UI/UX:** Built with Tailwind CSS, featuring glassmorphism effects, SVG icons, and smooth custom modals for confirmations (no native browser alerts).

## 🛠️ Tech Stack

* **Backend:** Django (Python)
* **Frontend:** HTML5, Tailwind CSS
* **Database:** SQLite (Default)
* **Scripts:** JavaScript, Chart.js (for analytics)
* **Icons:** Custom SVG Vectors

## 🚀 Installation & Setup

Follow these steps to get TaskMaster running on your local machine.

### 1. Clone the Repository

```bash
git clone [https://github.com/yourusername/taskmaster.git](https://github.com/yourusername/taskmaster.git)
cd taskmaster
```

### 2. Create a Virtual Environment
## It is recommended to use a virtual environment to manage dependencies.
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install django
# If you have a requirements.txt file, use: pip install -r requirements.txt
```

### 4. Database Setup
## Run migrations to set up the SQLite database structure.
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (Admin)
## To access the Django admin panel:
```bash
python manage.py createsuperuser
```

### 6. Run the Server

```bash
python manage.py runserver
```
Open your browser and navigate to:
```bash
http://127.0.0.1:8000/
```

### 📂 Project Structure
## Here is an overview of the project's file organization to help you navigate the codebase:

```
TaskMaster/
├── dashboard/                  # The main application logic
│   ├── migrations/             # Database migration files
│   ├── templates/              # HTML templates (Glassmorphism UI)
│   │   ├── base.html           # Main layout with navbar & footer
│   │   ├── dashboard.html      # Main dashboard with charts
│   │   ├── task_list.html      # Sortable/Filterable list view
│   │   ├── task_form.html      # Create/Edit form
│   │   └── trash_bin.html      # Deleted items recovery area
│   ├── models.py               # Task database schema (Title, Priority, Due Date)
│   ├── views.py                # View controllers (Filtering, Sorting, CRUD)
│   ├── forms.py                # Django forms with Tailwind styling widgets
│   └── urls.py                 # Dashboard-specific URL routing
├── static/                     # Static assets folder (Root level)
│   └── images/                 # Stores branding assets (logo.svg)
├── taskmaster/                 # Project configuration
│   ├── settings.py             # Main settings (Static files config, Apps)
│   └── urls.py                 # Main URL entry point
├── manage.py                   # Django CLI utility
└── db.sqlite3                  # Development database
```

### 🎨 UI Customization

## The project uses a clean, modern aesthetic powered by Tailwind CSS.

1. Changing the Logo
> The application logo is an SVG file located at: static/images/logo.svg

> To update the branding, simply replace this file with your own SVG. The HTML is configured to scale it perfectly within the navbar container.

2. Styling & Colors
> The UI relies on utility classes directly in the HTML templates (e.g., bg-blue-50, backdrop-blur-xl).

> Theme Color: The primary brand color is "Apple Blue" (#007AFF / blue-500).

> Glass Effect: Achieved using bg-white/50, backdrop-blur, and border-white/40.

> To change the color scheme, find-and-replace the Tailwind color classes (e.g., replace blue-500 with purple-500) in the template files.

### 🤝 Contributing
## Contributions make the open-source community an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

> Fork the Project

> Create your Feature Branch ```bash git checkout -b feature/AmazingFeature

> Commit your Changes ```bash git commit -m 'Add some AmazingFeature'

> Push to the Branch ```bash git push origin feature/AmazingFeature

> Open a Pull Request

### 📄 License
Distributed under the MIT License. This means you are free to use, modify, and distribute this software as you see fit.

> See the LICENSE file for more information.
