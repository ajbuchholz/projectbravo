# Installation

Make sure `Python >= 3.7` and `pip` are installed before proceeding with the installation instructions.

1. Clone this repository.

2. Change the directory to `projectbravo` using `cd projectbravo/`.

3. Create a virtual environment using `python3 -m venv venv`.

4. Activate the virtual environment using `source venv/bin/activate`.

5. Install the `Python` dependencies using `pip install -r requirements.txt`.

6. Change the directory to `projectbravo` using `cd projectbravo/`.

7. Apply the migrations using `python manage.py migrate`.

8. Create a superuser account using `python manage.py createsuperuser`.