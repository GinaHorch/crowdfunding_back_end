release: python crowdfunding/manage.py migrate
web: gunicorn --chdir crowdfunding crowdfunding.wsgi --log-file -