from pika import ConnectionParameters
from jsonschema import validate, ValidationError

# Здесь содержаться очереди которые создаются и прослушиваются
BASKET_QUEUE = 'basket'
PRODUCT_MEILISEARCH = 'meilisearch'
FASTAPI_QUEUE = 'fastapi'

class ConnectValidRabbit:
    def __init__(self, queue: str, schema: str, __class=None):
        self.connection_param = ConnectionParameters(
            host='localhost',
            port=5672
        )
        self.queue = queue
        self.schema = schema

    def validations(self, message_data):
        try:
            validate(instance=message_data, schema=self.get_schema())
        except ValidationError as error:
            print(f"Validation error: {error}\nMessage: {message_data}")
            raise
    def get_schema(self):
        match self.schema:
            case 'basket':
                return {"type": "object","properties": {"user": {"type": "number"},"product_id": {"type": "number"},"quantity": {"type": "number"}, "action":{"type":"string"}}, "required": ["user", "product_id", "quantity", "action"], "additionalProperties": False }
            case 'add_data_meiliseacrh':
                return {"type": "object","properties": {"product_id":{"type":"number"}, "type":{"type":"string"}, "index": {"type":"string"}}, "required": ["product_id", "type", "index"], "additionalProperties": False }
            case 'fastapi_meilisearch':
                return None
            case _:
                raise ValueError(f'Нет такой схемы {self.schema}')

