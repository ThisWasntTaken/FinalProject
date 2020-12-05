# Privacy_Aware Activity-based Access Control Framework for EHR

## Installation

Create a virtual environment using anaconda or venv.

All requirements are listed in `requirements.txt`. These can be installed by
```
pip install -r requirements.txt
```
after creating a virtual environment with python 3.6.x.

## Starting the Applications
```python3
python run_cm.py
python run_gateway.py
python run_hiup -hiu_id=[x] -hip_id=[y]
```

where x and y are integers.

Register the HIUs and HIPs to the gateway first if they do not already exist.

Once the applications are running, use the given URLs to access the sites.
The default urls are:
* Consent Manager : http://127.0.0.1:5001/
* Gateway : http://127.0.0.1:5000/
* The HIU and HIP urls are created dynamically. The port is calculated as `10 * hiu_id + hip_id`. For example, for `hiu_id = 1` and `hip_id = 1` : http://127.0.0.1:6011/.

```diff
- Make sure that the `hiu_id` and `hip_id` are unique, and that `10 * hiu_id + hip_id` is unique.
```

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

 View the HTML documentation by opening the `index.html` file in `_build/html`.