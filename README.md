# CityIO_Flask

A lightweight version of cityIO for locally testing CityScope tables.

The initial state of the table is established from a local json file. GET, POST and DELETE requests can be made following the main [cityIO](https://cityscope.media.mit.edu/backend/API) structure: 

To run, first install flask and flask_cors in a clean environment. Then call cityio_lite.py with the table names as arguments:
```
pip install flask flask_cors
python cityio_lite.py table_name_1 table_name_2
```

Each table is initialised from the corresponding json file stored in the 'base' directory.