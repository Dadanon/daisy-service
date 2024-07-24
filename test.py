import json
import time

from dodp_new import client_login
from dodp_new.exceptions import GetClientError

start_time = time.time()
client = client_login('https://do.av3715.ru', 'motorina@ia-group.ru', '23610')
if not client:
    raise GetClientError()
print(f'Client version: {client.version}')
book_content = client.get_book_content('b232849')
print(book_content.to_dict())
# book_list = client.get_book_list('Пушк')
# print('Book list info:\n')
# print(f'Total: {book_list.total}')
# for book in book_list.books:
#     print(book.__dict__)
end_time = time.time()
print(f'Delta time: {end_time - start_time}')
