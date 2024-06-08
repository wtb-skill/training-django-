# App Title

Short app description

## Features

(list of features with short descriptions, example below)
- **Add Books:** Users can add new books to the library, including titles, descriptions, and authors.
- **Manage Authors:** Authors can be added, edited, and associated with specific books.
- **Update Book Details:** Allows users to modify book information and their associations with authors.
- **API Structure:** Provides an API overview detailing endpoints for interacting with books and authors.
- **Homepage:** The main interface displaying available functionalities and API endpoints.

## Project Structure

- `app`: Contains the core Flask application files.
- `static`: Stores static assets like images, stylesheets, and client-side scripts.
- `templates`: Holds HTML templates for rendering views.
- `migrations`: Includes database migration scripts generated by Flask-Migrate.
- `config.py`: Configuration file for the Flask app.
- `db_manager.py`: Development tool to delete all data from the library.db.
- `library.db`: SQLite database file storing book, author, and status information.
- `requirements.txt`: Lists all Python dependencies for the project.
- `run.py`: Entry point to run the Flask application.

## Usage

1. Install project dependencies from `requirements.txt`.
2. Run the Flask application using `python run.py`.
3. Access the application in a web browser at `http://localhost:5000`.
4. Explore the available features and functionalities provided in the interface.

## Authors

    Adam Bałdyga

## License

This project is licensed under the MIT License.