# DonationManager
Please use python 3 for all the commands.
Excute the commands under project directory.

```
# Setup virtual enviornment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Load existing test data.
python manage.py migrate
python manage.py loaddata testing_data.json

# Run server.
python manage.py runserver
```