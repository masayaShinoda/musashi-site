## Project Overview

Fullstack Django website for Musashi Lubricant. It uses HTMX for dynamic content loading and Alpine.js for client-side interactivity, with Tailwind CSS for styling.

## Important Directories and Files

-   `base/`: The core Django app, containing the main layout, homepage, and static assets.
-   `products/`: A Django app to manage product listings, categories, and related details.
-   `musashi_site/`: The main Django project configuration, including settings, and URL routing.
-   `requirements.txt`: A list of Python dependencies for the project.
-   `manage.py`: The Django command-line utility for administrative tasks.
-   `templates/`: Contains the Django templates for rendering the website's pages.
-   `static/`: Holds static files like CSS, JavaScript, and images.

## Environment Variables

Create a `.env` file in the root directory of the project with the following variables:

```
SECRET_KEY='your-secret-key'
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

## Setup and Installation

1.  **Create and activate a virtual environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

4.  **Run the development server with Tailwind CSS:**

    This command starts the Tailwind CSS watcher and the Django development server in parallel.

    ```bash
    tailwindcss -i ./base/assets/css/input.css -o ./base/static/css/output.css --watch --minify & python manage.py runserver
    ```

5. **Create a superuser to access the admin panel**
   ```bash
   python manage.py createsuperuser
   ```

The website will be available at `http://127.0.0.1:8000`.

The admin panel will be available at `http://127.0.0.1:8000/admin`.

## Deployment

For production, you will need to collect the static files into the `staticfiles` directory.

```bash
python manage.py collectstatic
```
This project is configured to use `sqlite` as the database and is intended to be deployed with `nginx` and a WSGI server like `gunicorn`.

