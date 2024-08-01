import time

from dodp_new import client_login, DODPClient

start_time = time.time()
client: DODPClient = client_login('https://do.av3715.ru', 'motorina@ia-group.ru', '23610')
# client = client_login('http://127.0.0.1:8082/service.php', 'kolibre', 'kolibre')
print(f'Client version: {client.version}')
print('\n')
search_questions = client.get_search_questions()
print(search_questions.to_dict())
print('\n')
questions_with_clr = client.get_questions('searchrequest', 'Пушкин')
print(questions_with_clr.to_dict())
print('\n')
if clr := questions_with_clr.content_list_ref:
    book_list = client.get_content_list(clr, 0, 3)
    print(book_list.to_dict())
    print('\n')
    if len(book_list.books) > 0:
        first_book = book_list.books[0]
        book_content = client.get_book_content(first_book.id)
        print(book_content.to_dict())

# print(client.get_content_list('LIBRARY.booksBySearch(4591839)', 0, 3).to_dict())
# print('\n')
# print(f'{client.get_search_questions().to_dict()}\n')
# print(f'{client.get_questions("searchrequest", "Пушк").to_dict()}\n')
end_time = time.time()
print(f'Delta time: {end_time - start_time}')


