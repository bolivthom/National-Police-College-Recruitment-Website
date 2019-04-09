# National Police College of Jamaica Recruitment Website

**Clone and run for a quick way to see the Website in action.**

A Prototype Website built in Flask for applicants applying to the National Police College

## To Use

To clone and run this repository you'll need [Git](https://git-scm.com), [Python 3](https://www.python.org/downloads/) and [Mysql](https://www.mysql.com/downloads/) installed on your computer. From your command line:

```bash
# Clone this repository
git clone git@github.com:bolivthom/National-Police-College-of-Jamaica-Recruitment-Website.git

# Go into the repository
cd National-Police-College-Recruitment-Website

# Install the virtualenv package
pip install virtualenv

# Create the virtual environment
py -m venv venv 

# Activate virtual environment
source venv/bin/activate
or
.\venv\Scripts\activate (if using Windows)

# Install dependencies
pip install -r requirements.txt

#Connect to mysql (Ensure you have mysql server running)

#Create Database and add the required info in your init.py file

#migrate the database models
python flask-migrate.py db init 
python flask-migrate.py db 
migrate python flask-migrate.py db upgrade

# Run the app
python run.py
```

