# Mapper - Topological Data Analysis

## Installation

Create a virtual environment using anaconda or venv.

All requirements are listed in requirements.txt. These can be installed by
```
pip install -r requirements.txt
```
after creating a virtual environment with python 3.6.x.

## Starting the Applications
```
python run_cm.py
python run_gateway.py
python run_hiup -hiu_id=[x] -hip_id=[y]
```

where x and y are integers. Make sure that the hiu_id and hip_id are unique.

Register the HIUs and HIPs to the gateway first if they do not already exist. No UI exists for this, thus it requires direct access to the database:
1. Open the gateway database by
```
sqlite3 gateway/site.db
```
2. Create entries into the HIU and HIP tables using SQL.
```
INSERT INTO HI[X] VALUES (...)
```

Once the applications are running, use the given URLs to access the sites.

## Creating Documentation

Sphinx is required. Clear existing documentation files by
```
make clean
```

Create HTML documentation by
```
make html
```

and latex files by
```
make latex
```
 The latex files can be compiled into a pdf.

 View the HTML documentation by opening the index.html file in _build/html.