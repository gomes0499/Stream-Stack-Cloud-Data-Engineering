from flask import Flask, jsonify, request
from faker import Faker
from azure.eventhub import EventHubProducerClient, EventData
import json

app = Flask(__name__)
fake = Faker()

# Cria um cliente do Event Hub
producer = EventHubProducerClient.from_connection_string("Your Event Hubs connection string", eventhub_name="Your Event Hub name")

@app.route('/generate-data', methods=['POST'])
def generate_data():
    num_records = int(request.args.get('num_records', 1)) # Obter o número de registros a partir do parâmetro de consulta, padrão para 1 se não for fornecido
    data = []
    event_data_batch = producer.create_batch() # Cria um lote de eventos

    for _ in range(num_records):
        record = {
            "name": fake.name(),
            "address": fake.address(),
            "email": fake.email()
        }
        data.append(record)
        event_data_batch.add(EventData(json.dumps(record))) # Adiciona o registro ao lote de eventos

    # Envia o lote de eventos para o Event Hub
    producer.send_batch(event_data_batch)

    return jsonify(data), 200

if __name__ == "__main__":
    app.run(debug=True)
