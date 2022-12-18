from boto3.dynamodb.conditions import Key

from app.core.config import config
from app.core.db import get_resource
from app.core.exceptions import CustomException


class EventService:
    def __init__(self):
        self.db = get_resource("dynamodb")
        self.logs_table = self.db.Table(config.LOGS_TABLE_NAME)

    def get_all_logs(self):
        try:
            response = self.logs_table.scan()
            return response["Items"]
        except Exception as e:
            raise CustomException(message=str(e))

    def get_logs_by_apartment_id(self, apartment_id):
        try:
            response = self.logs_table.query(
                KeyConditionExpression=Key("apartment_id").eq(apartment_id)
            )
            return response["Items"]
        except Exception as e:
            raise CustomException(message=str(e))
