import time

from dodp_new import client_login
from dodp_new.exceptions import GetClientError

start_time = time.time()
client = client_login('https://do.av3715.ru', 'motorina@ia-group.ru', '23610')
# # client = client_login('http://127.0.0.1:8081/service.php', 'kolibre', 'kolibre')
if not client:
    raise GetClientError()
# print(f'Client version: {client.version}\n')
# print(f'{client.get_search_questions().to_dict()}\n')
print(f'{client.get_questions("searchrequest", "Пушк").to_dict()}\n')
end_time = time.time()
print(f'Delta time: {end_time - start_time}')


