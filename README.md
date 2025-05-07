# Training App

A web-based application for creating, managing, and tracking training sessions. This project enables users to create custom training templates, log workout sessions, and track progress. It integrates with a robust backend system for managing exercises, sets, and templates, along with a user-friendly interface for both trainers and trainees.

## Features

- 🏋️ **Training Template Management** – Create, edit, and delete personalized training templates with a set list of exercises and sets.
- 📝 **Exercise and Set Management** – Add, remove, and reorder exercises and sets within templates. Track set types, reps, and weight.
- 🗓️ **Training Session Tracker** – Start, process, and finish training sessions. Log progress for each set (reps, weight, and completion status).
- 🔄 **Session History** – View completed training sessions with duration, exercises, and progress.
- 🌐 **Web Interface** – Easy-to-use Django web interface for managing templates, exercises, and sessions.
- 🔒 **Authentication** – Support for user authentication to track training history and templates for individual users.
- 📊 **Session Analytics** – View the duration and completion status of past training sessions.
- ⚡ **API for Templates** – Expose training templates via a RESTful API for integration with other tools.

## Project Structure

```
training-django/
├── README.md                       # Project overview and documentation
├── .gitignore                      # Git ignore file to exclude unnecessary files
├── requirements.txt                # List of project dependencies
└── training_project/               # Main Django project folder
      ├── dashboard/                # Dashboard views
      │   └── views.py
      ├── training_templates/       # Training template-related functionality
      │   ├── views.py
      │   ├── models.py
      │   └── forms.py
      ├── training_sessions/        # Training session-related views and models
      │   ├── views.py
      │   ├── models.py
      │   └── forms.py
      ├── training_history/         # Session history views
      │   └── views.py
      ├── training_project/         # Session history views
      │   ├── asgi.py               # ASGI entry point for the app
      │   ├── settings.py           # Django settings file      
      │   └── wsgi.py               # WSGI entry point for the app
      ├── exercises/                # Exercise models and views
      │   ├── models.py
      │   └── views.py
      ├── manage.py                 # Django project management script
      └── training.sqlite3          # SQLite database for the project
```

## Usage

### 1. Install Project Dependencies

Start by installing the required Python dependencies. You can install them using `pip` from the `requirements.txt` file.

```
pip install -r requirements.txt
```

### 2. Run the Application

First, navigate into the `training_project` directory:
```
cd training_project
```
Then, to start the Django application, run the following command:
```
python manage.py runserver
```
The app will launch and be accessible at:
http://127.0.0.1:8000/

## 🔌 API Route Map

### Main Routes

| Route | Method | Description                                                                 |
|-------|--------|-----------------------------------------------------------------------------|
| `/` | `GET` | Renders the dashboard homepage with an overview of training templates.      |
| `/training-templates` | `GET` | Lists all training templates.                                              |
| `/training-template/<template_id>/edit` | `GET` | Edit an existing training template.                                        |
| `/training-template/<template_id>/add-exercise` | `POST` | Add a new exercise to a template.                                          |
| `/training-template/<template_id>/delete` | `POST` | Delete a training template.                                                |
| `/training-sessions/start/<template_id>` | `GET` | Start a new training session based on the selected template.                |
| `/training-session/<session_id>/finish` | `POST` | Mark a session as finished and save the data for the workout.               |
| `/training-session-history` | `GET` | View a list of all completed training sessions.                             |
| `/training-session/<session_id>/details` | `GET` | View detailed information about a specific training session.               |
| `/api/templates` | `GET` | Fetch training templates as a JSON response for external integration.      |
| `/api/mark-set-completed` | `POST` | Marks a specific set within a session as completed (AJAX request).         |

## 🙋 FAQ ##

**Do I need to create my own training templates?**  
No! You can either create custom training templates or use pre-existing ones. The templates are fully customizable to match your workout goals.

**How are training sessions tracked?**  
Training sessions are tracked by logging exercises, sets, reps, and weights during the session. Once a session is finished, it will be stored with its start time, end time, and the list of completed exercises.

**Can I reuse training templates across sessions?**  
Yes! Once a training template is created, you can use it to start new training sessions anytime.


## Authors

    Adam Bałdyga

## License

This project is licensed under the MIT License.
