from flask import Flask
from cryptotax.transaction import transaction_single, transaction_collection
from cryptotax.kraken import kraken_csv
app = Flask(__name__)

#export FLASK_APP=hello.py
#flask run

@app.route('/')
def hello_world():
    return 'Hello world'

app.register_blueprint(transaction_single)
app.register_blueprint(transaction_collection)

app.register_blueprint(kraken_csv)
