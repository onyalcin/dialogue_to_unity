# Dialogue to Unity (text only)

This is the first pass to tie the dialogue system to Unity via TCP connection.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

Use command-line to start the system. It requires python3.x and virtualenv package.

```
pip install virtualenv
```

### Installing 

Activate virtualenv:

```
cd venv/Scripts
activate
cd ../..
```

Install requirements:

```
pip install -r requirements.txt
```

## Running the system

Make sure the server is online on Unity side.

```
python test_unity.py
```

Start typing and get responses. If you want to get an echoing agent, comment out this part in test_unity.py:

```
            # remove quotes if you want to have real response
            clean_query = clean(query)
            query, intent, context = return_response(clean_query)
            print('response: ', query)
```


## Authors

* **Ozge Nilay Yalcin - 2018**
