from flask import Flask, jsonify, request
from faker import Faker
import boto3
import json

app = Flask(__name__)
fake = Faker()

kinesis = boto3.client('kinesis', region_name='us-east-1') # Altere para a sua região

@app.route('/generate-data', methods=['POST'])
def generate_data():
    num_records = int(request.args.get('num_records', 1)) # Obter o número de registros a partir do parâmetro de consulta, padrão para 1 se não for fornecido
    data = []
    records = []

    for _ in range(num_records):
        record = {
            "name": fake.name(),
            "address": fake.address(),
            "email": fake.email()
        }
        data.append(record)
        records.append({
            'Data': json.dumps(record), 
            'PartitionKey': 'partitionkey' 
        })

    if records:
        response = kinesis.put_records(
            Records=records,
            StreamName='Stream-97c9a098' 
        )

    return jsonify(data), 200

if __name__ == "__main__":
    app.run(debug=True)
