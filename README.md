# Django HTMX Introduction - MoviesApp

A sample Django project demonstrating the integration of [HTMX](https://htmx.org/) for dynamic, modern web interfaces without heavy JavaScript. This app manages a collection of films, allowing users to view, search, and interact with film data using Django and HTMX.

## Features
- User authentication (login/register)
- Film listing, detail view, and search
- HTMX-powered partial updates for a dynamic user experience
- File upload for film photos
- Responsive UI with reusable templates and partials

## Project Structure
- `films/` - Django app containing models, views, forms, and templates
- `templates/` - HTML templates (including HTMX partials)
- `static/` - Static files (CSS)
- `media/` - Uploaded film photos
- `htmx/` - Django project settings and configuration

## Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone https://github.com/SvetozarP/DjangoHTMXMoviesApp
   cd DjangoHTMXMoviesApp
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```
6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
7. **Access the app:**
   Open [http://localhost:8000/](http://localhost:8000/) in your browser.

## Usage
- Register or log in to manage your films.
- Use the search bar to find films dynamically (HTMX-powered).
- Add, edit, or delete films.
- Upload and view film photos.

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](LICENSE)

---
Inspired by BugBytes tutorials.
