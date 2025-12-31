# Faster-Parts — Project Summary

Description
-----------
`E-commerce-Platform` is a local e-commerce platform based on Django (located in `E-commerce-Platform`). The project includes apps for item management, shopping cart, user dashboard, and user-to-user conversations.

Features and What the Project Provides
-------------------------------------
- User-facing pages: HTML templates, CSS and JS for product listings, product detail pages, cart page, and auth pages (login/signup).
- Product management: Create, update and delete products via the `items` app and Django admin.
- Shopping cart: Add items to cart and view cart contents.
- Messaging system: The `conversation` app enables messages between users.
- Dashboard: The `Dashboard` app provides administrative and reporting pages.
- Internationalization: Locale files for Arabic and English are included.

Tech Stack and Tools
--------------------
- Language: Python (virtual environment in `env` indicates Python 3.11).
- Framework: Django (project README mentions Django 5.2).
- Database: SQLite used by default (`Faster-Parts/E-commerce-Platform/db.sqlite3`).
- Virtual environment: `env/` contains the project's virtualenv with activation scripts (`env\Scripts\activate`).
- Common packages observed in the environment: `sqlparse`, `tzdata` (check `env/Lib/site-packages`).
- Frontend: HTML and Tailwind CSS used in templates and static files.

Project Structure (important locations)
-------------------------------------
- Project README: [README.md](README.md)
- Django settings: [settings.py](settings.py)
- Django management script: [manage.py](manage.py)
- Virtual environment folder: [env](env)

Quick: How to Set Up and Run (Windows)
-------------------------------------
1. Activate the virtual environment:

```powershell
.\env\Scripts\activate
```

2. Install requirements (if `requirements.txt` exists in `E-commerce-Platform`):

```powershell
pip install -r E-commerce-Platform\requirements.txt
# If no requirements file: pip install django sqlparse tzdata
```

3. Run migrations and create a superuser (from repository root):

```powershell
python Faster-Parts\E-commerce-Platform\manage.py migrate
python Faster-Parts\E-commerce-Platform\manage.py createsuperuser
```

4. Start the development server:

```powershell
python Faster-Parts\E-commerce-Platform\manage.py runserver
```

Developer Notes
---------------
- To use a production-grade database (Postgres/MySQL), update the `DATABASES` setting in `settings.py` and set the appropriate environment variables.
- Media and product images are stored under `item-image` and static files exist inside each app's static directory.
- If there is no reliable `requirements.txt`, you can generate one from the current virtual environment:

```powershell
.\env\Scripts\activate
pip freeze > E-commerce-Platform\requirements.txt
```

Quick Links in the Repo
----------------------
- Django app root: [E-commerce-Platform](Faster-Parts/E-commerce-Platform)
- Project-level README: [E-commerce-Platform/README.md](E-commerce-Platform/README.md)

Next steps I can do for you:
- Generate/update `requirements.txt` from the current environment.
- Add deployment instructions for Docker, Heroku, or Render.

End of summary.

Deployment (recommended)
------------------------
Below are recommended commands and notes for deploying this Django project to Render.com or running it locally with a production-like server.

1) Environment variables (set these on Render or export locally):

	- `SECRET_KEY` — a long random string
	- `DEBUG` — `False` in production
	- `DJANGO_ALLOWED_HOSTS` — space-separated hosts (e.g. `example.com my-app.onrender.com`)
	- `DATABASE_URL` — Postgres URL when using a managed Postgres database

2) Build / start commands (Render web service):

	- Build command:

	  ```bash
	  ./build.sh
	  ```

	- Start command (Render or local gunicorn):

	  ```bash
	  gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
	  ```

3) Local quick check:

	```bash
	python -m venv .venv
	source .venv/bin/activate   # or .venv\Scripts\activate on Windows
	pip install -r requirements.txt
	python manage.py migrate
	python manage.py collectstatic --no-input
	gunicorn config.wsgi:application --bind 127.0.0.1:8000
	```

4) Notes for Render.com

	- Use the `build.sh` script as the "Build Command" so static files are collected and migrations run.
	- Set the "Start Command" to: `gunicorn config.wsgi:application`
	- Choose the Postgres add-on or provide `DATABASE_URL` for production; `dj-database-url` is included in `requirements.txt`.

If you want, I can also add a `Procfile` and a `render.yaml` with sensible defaults.
