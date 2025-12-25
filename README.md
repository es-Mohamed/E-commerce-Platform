# Faster-Parts — Project Summary

Description
-----------
`Faster-Parts` is a local e-commerce platform based on Django (located in `Faster-Parts`). The project includes apps for item management, shopping cart, user dashboard, and user-to-user conversations.

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
- Database: SQLite used by default (`Faster-Parts/Faster-Parts/db.sqlite3`).
- Virtual environment: `env/` contains the project's virtualenv with activation scripts (`env\Scripts\activate`).
- Common packages observed in the environment: `sqlparse`, `tzdata` (check `env/Lib/site-packages`).
- Frontend: HTML and Tailwind CSS used in templates and static files.

Project Structure (important locations)
-------------------------------------
- Project README: [Faster-Parts/README.md](Faster-Parts/README.md)
- Django settings: [/Faster-Parts/settings.py](/Faster-Parts/settings.py)
- Django management script: [/Faster-Parts/manage.py](/Faster-Parts/manage.py)
- Local database file: [/Faster-Parts/db.sqlite3](/Faster-Parts/db.sqlite3)
- Virtual environment folder: [env](env)

Quick: How to Set Up and Run (Windows)
-------------------------------------
1. Activate the virtual environment:

```powershell
.\env\Scripts\activate
```

2. Install requirements (if `requirements.txt` exists in `Faster-Parts`):

```powershell
pip install -r Faster-Parts-Project\requirements.txt
# If no requirements file: pip install django sqlparse tzdata
```

3. Run migrations and create a superuser (from repository root):

```powershell
python Faster-Parts\Faster-Parts\manage.py migrate
python Faster-Parts\Faster-Parts\manage.py createsuperuser
```

4. Start the development server:

```powershell
python Faster-Parts\Faster-Parts\manage.py runserver
```

Developer Notes
---------------
- To use a production-grade database (Postgres/MySQL), update the `DATABASES` setting in `Faster-Parts/Faster-Parts/settings.py` and set the appropriate environment variables.
- Media and product images are stored under `item-image` and static files exist inside each app's static directory.
- If there is no reliable `requirements.txt`, you can generate one from the current virtual environment:

```powershell
.\env\Scripts\activate
pip freeze > Faster-Parts-Project\requirements.txt
```

Quick Links in the Repo
----------------------
- Django app root: [Faster-Parts/Faster-Parts](Faster-Parts/Faster-Parts)
- Project-level README: [Faster-Parts/README.md](Faster-Parts/README.md)

Next steps I can do for you:
- Generate/update `Faster-Parts/requirements.txt` from the current environment.
- Add deployment instructions for Docker, Heroku, or Render.

End of summary.
