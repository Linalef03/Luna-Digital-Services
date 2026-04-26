# Django Service Platform

A web application for managing online service orders.
It includes authentication, role-based access (client, employee, admin), order tracking, and file handling within a complete workflow from request to delivery.

---

## Setup


git clone <repo-url>
cd <project>

python -m venv test
test\Scripts\activate

pip install django

python manage.py migrate
python manage.py runserver


---

## Database

This project is configured to use MySQL.
You can modify the database settings in `settings.py` to use any other system such as SQLite or PostgreSQL.

---

## Notes

Create an admin account with:


python manage.py createsuperuser

