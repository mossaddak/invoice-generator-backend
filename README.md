# Invoice generator backend

All the backend business logics are connected to the <b>invoice_generator</b> project. It's a Django project running Django REST Framework.


## API Document

    http://127.0.0.1:8000/api/v1/docs

---

**Setting up a virtualenv**

    cd ~
    python3 -m venv env
    source ~/env/bin/activate
    source venv/bin/activate


**Install the Python dependencies for the project**

    pip install -r requirements/development.txt


**Run the development server**

    python manage.py runserver 0:8000

You can now visit 127.0.0.1:8000 on your browser and see that the project is running.

---