import os
import json

# Load Environment variables.
with open('private.test.env.json') as f:
    data = json.load(f)
    for key, value in data.get('test').items():
        os.environ[key] = value



