# Сервис взаимодействия с электронными библиотеками

Данный модуль предназначен для взаимодействия пользователя с электронными библиотеками
по протоколу DODP (Daisy Online Delivery Protocol). На данный момент существует
3 версии этого протокола: 1, 2.0.1, 2.0.2. В части взаимодействия с интернет-сервисами
данный модуль должен удовлетворять ГОСТ Р58510-2019, соответственно, должны быть
реализованы в общем виде следующие функции:
- самостоятельный выбор книг путем текстового поиска
- самостоятельный выбор книг путем голосового поиска (_)
- выбор книг путем очного и удаленного (по телефону) запроса в библиотеку 
с установкой выбранных книг на электронную полку
- загрузка выбранных книг из электронной полки и библиотечной базы в тифлофлешплеер (специальное устройство для слабовидящих)
- онлайн прослушивание выбранных книг без их загрузки в тифлофлешплеер с сохранением позиции воспроизведения каждой книги

Для выбора книг путем текстового поиска (версия 1.0) необходимо выполнить нижеуказанные функции в корректном порядке:
- перейти в меню поиска (userResponse questionID="search")
- получить полезный id для поиска (в случае av3715 - "searchrequest")
- сделать запрос с полезным id и текстом (questionId="searchrequest" value="book_name")
- полученный id (содержимое contentListRef) использовать в методе getContentList
- из полученного ответа берем общее число записей (ns1:contentList totalItems=), находим все
contentItem, выбираем из них id и текст для показа в списке, возвращаем список в стороннее приложение (API метод)
- у понравившегося item - вызываем getContentResources для данного id и получаем
список ссылок на lgk и lkf файлы, возвращаем эти пути списком в стороннее приложение (API метод)

Список публичных методов:
- залогиниться (параметры - логин, пароль)
- выйти из аккаунта
- получить варианты поиска - объект Questions
- выбрать опцию поиска - объект Questions

## Сценарии использования:
### 1. Инициализация клиента
```
client: DODPClient = client_login(url, username, password)
```
Возвращает ошибку (GetClientError) в случае неудачного логина.  
Возвращает клиента подходящей версии DODP (1 или 2) в случае успеха
### 2. Выйти из аккаунта
```
logoff_result: bool = client.logoff()
```
Возвращает True в случае успешного выхода из аккаунта.  
Возвращает False в случае ошибки выхода из аккаунта
### 3. Выбор книги в динамическом меню
- инициализировать клиент (пункт 1)
- получить возможности поисковых вопросов в виде объекта Questions
- при наличии желаемых опций поиска в списке multiple_choice_questions
у объекта Questions - пройти по ним до появления желаемого inputQuestion
- осуществить поиск с id выбранного inputQuestion и необходимым текстом
- если в ответе присутствует contentListRef - получить соответствующий content list для этого contentListRef
- из списка книг выбрать необходимую и получить контент

Пример для av3715:
- инициализация клиента
```
client: DODPClient = client_login(url, username, password)
```
- получаем опции поисковых запросов  

Запрос:
```
search_options: Questions = client.get_search_questions()
```
Ответ (search_options.to_dict()):
```
{
    'content_list_ref': None, 
    'label': None, 
    'input_questions': [
        {
            'id': 'searchrequest', 
            'label': {
                'text': 'Введите строку для поиска. Поиск производится по автору, наименованию и диктору.', 
                'audio': None
            }, 
            'input_types': [
                'TEXT_ALPHANUMERIC'
            ]
        }
    ], 
    'multiple_choice_questions': []
}
```
- вводим текст поиска для выбранного inputQuestion  

Запрос:
```
questions_clr = client.get_questions('searchrequest', 'Пушкин')
```
Ответ (questions_clr.to_dict()):
```
{
    'content_list_ref': 'LIBRARY.booksBySearch(4592268)', 
    'label': None, 
    'input_questions': [], 
    'multiple_choice_questions': []
}
```
- получаем contentList по полученному content_list_ref и диапазону книг (допустим, 3)  

Запрос:
```
book_list: BookList = client.get_content_list('LIBRARY.booksBySearch(4592268)', 0, 3)
```
Ответ (book_list.to_dict()):
```
{
    'total': 620, 
    'label': {
        'text': 'Поиск Пушкин', 
        'audio': None
    }, 
    'books': [
        {
            'id': 'b22677', 
            'label': {
                'text': 'Авенариус В - Пушкин (Иванова М.) (прочитана)', 
                'audio': None
            }
        }, 
        {
            'id': 'b22802', 
            'label': {
                'text': 'Авенариус В - Чем был для Гоголя Пушкин (Герасимов В.)', 
                'audio': None
            }
        }, 
        {
            'id': 'b221880', 
            'label': {
                'text': 'Аверкиев С - Мой Пушкин. 1996 (Зозулин В., Бочкарев В., Парра А., Ларионов В., Сайфулин Г.)', 
                'audio': None
            }
        }
    ]
}
```
- получаем контент книги (если len(book_list.books) > 0)  

Запрос:
```
book_content: BookContent = client.get_book_content(book_list.books[0].id)
```
Ответ (book_content.to_dict()): ..truncated
```
{
    'lgk_content': {
        'uri': 'https://do.av3715.ru/books/22677/BOOK_001.lgk', 
        'size': 1049.0
    }, 
    'lkf_content': [
        {
            'uri': 'https://do.av3715.ru/books/22677/BOOK_001/001.lkf', 
            'size': 8397687.0
        }, 
        {
            'uri': 'https://do.av3715.ru/books/22677/BOOK_001/002.lkf', 
            'size': 8180767.0
        }, 
        {
            'uri': 'https://do.av3715.ru/books/22677/BOOK_001/003.lkf', 
            'size': 7299918.0
        }, 
        {
            'uri': 'https://do.av3715.ru/books/22677/BOOK_001/004.lkf', 
            'size': 7677179.0
        }, 
        {
            'uri': 'https://do.av3715.ru/books/22677/BOOK_001/005.lkf', 
            'size': 4410514.0
        }
    ]
}
```

## Публичные методы:
### 1. Войти в систему
```
def login(username: str, password: str) -> bool
```
Возвращает True, если удалось успешно войти в систему со своим аккаунтом
и выполнить все промежуточные шаги (getServiceAttributes, setReadingSystemAttributes),
иначе False
### 2. Выйти из системы
```
def logoff() -> bool
```
Возвращает True в случае удачного выхода из аккаунта, иначе False
### 3. Получить список книг по тексту
```
def get_book_list(text: str, first_item: int = 0, last_item: int = -1) -> BookList
```
```
class BookList:
    total: int  # Общее количество книг, не равно len(books) при указании first_item или last_item
    books: List[BookListed]
        
class BookListed:
    id: str
    name: str
```
Параметры:
- text: str - текст, который может быть частью названия книги или автора
- first_item: int - индекс первой записи, по умолчанию 0 (с начала списка)
- last_item: int - индекс последней записи, по умолчанию -1 (до конца списка)

Пример: возвращенный список целиком - [1, 2, 3, 4, 5] (при задании first_item
и last_item по умолчанию). Если first_item = 2, last_item = 4 - вернется список
[3, 5].  
Также у BookList есть метод to_dict(), который возвращает объект класса в формате json. Пример:
```
{
    'total': 2, 
    'books': [
        {
            'id': 1, 
            'name': 'first_book'
        }, 
        {
            'id': 2, 
            'name': 'second_book'
        }
    ]
}
```
### 4. Получить содержимое книги
```
def get_book_content(book_id: str) -> Optional[BookContent]:
```
```
class BookContent:
    lgk_content: Optional[LGKContent]
    lkf_content: List[LKFContent]
    
class LGKContent(AudioContent):
    pass


class LKFContent(AudioContent):
    pass
    
class AudioContent:
    uri: str
    size: float  # Размер файла по ссылке в байтах
```
Параметры:
- book_id: str - идентификатор книги  

Получить содержимое книги по её идентификатору в виде ссылок для проигрывания
и размера файлов по соответствующим ссылкам.  
Также у BookContent есть метод to_dict(), который возвращает объект класса в формате json. Пример:
```
{
    'lgk_content': {
        'uri': 'https://do.av3715.ru/books/232849/BOOK_001.lgk', 
        'size': 193.0
    }, 
    'lkf_content': [
        {
            'uri': 'https://do.av3715.ru/books/232849/BOOK_001/001.lkf', 
            'size': 36178225.0
        }, 
        {
            'uri': 'https://do.av3715.ru/books/232849/BOOK_001/002.lkf', 
            'size': 25922664.0
        }
    ]
}
```
