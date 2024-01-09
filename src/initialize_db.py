from db_storage import DbStorage
import cfnresponse


def lambda_handler(event, context):
    physical_resource_id = event.get('PhysicalResourceId', None)
    with DbStorage() as storage:
        storage.initialize_db()
    cfnresponse.send(event, context, cfnresponse.SUCCESS, {}, physical_resource_id)


if __name__ == '__main__':
    event = {}
    context = {}
    lambda_handler(event, context)
