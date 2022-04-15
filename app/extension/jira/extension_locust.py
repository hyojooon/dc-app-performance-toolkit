import re
from locustio.common_utils import init_logger, jira_measure, run_as_specific_user  # noqa F401
import random

logger = init_logger(app_type='jira')


@jira_measure("locust_app_specific_action")
# @run_as_specific_user(username='admin', password='admin')  # run as specific user
def app_specific_action(locust):
    num = random.randrange(1,1000)
    body = {"formParams": '{"name":"Test%d","description":"Test Description","recipientPickerTo":"us:JIRAUSER10000","individual":"yes","summary":"Summary","message":"Hello Template!!"}'%num}
    r = locust.client.put('/rest/doamo/email/1.0/template', data=body, catch_response=True)
    content = r.content.decode('utf-8')
    if 'OK' not in content:
        logger.error(f"Test{num} was not create")
    assert 'OK' in content

    r = locust.get('/rest/doamo/email/1.0/template/all', catch_response=True)  # call app-specific GET endpoint
    content = r.content.decode('utf-8')   # decode response content

    if 'templateName' not in content:
        logger.error(f"'templateName' was not found in {content}")
    assert 'templateName' in content  # assert specific string in response content
