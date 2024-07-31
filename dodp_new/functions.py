from typing import Optional, List, Iterator, Dict, Tuple
import re
from dodp_new.general import Label, AudioContent, InputQuestion, MultipleChoiceQuestion, Choice, Questions, TagInfo


def method_not_override(method_name: str) -> str:
    return f'Метод {method_name} не переопределен'


# INFO: regular functions block ----------------------------------------------------------------


# INFO: tested functions block -----------------------------------------------------------------


def get_full_tag_name(tag_name: str, body: str) -> Optional[str]:
    full_name_match = re.search(rf'<((?:\w+:)?{tag_name})', body, re.DOTALL)
    return full_name_match.group(1) if full_name_match else None


def get_tag_info_by_params(tag_name: str, body: str, with_content: bool = False, **kwargs) -> Optional[TagInfo]:
    full_tag_name = get_full_tag_name(tag_name, body)
    if not full_tag_name:
        return None
    tag_info: TagInfo = TagInfo(name=full_tag_name)

    tag_header_matches = re.finditer(rf'<{full_tag_name}(|\s+?|\s+?.*?|\s+?.*?\s+?)(?:>|(/>))', body, flags=re.DOTALL)
    if not kwargs:  # Тогда берем первый попавшийся
        first_match = tag_header_matches.__next__()
        tag_info.params = dict(re.findall(r'\b(.*?)="(.*?)"', first_match.group(1), flags=re.DOTALL))
        if not with_content:
            return tag_info
        else:
            tag_content_match = re.search(rf'(.*?)</{full_tag_name}>', body[first_match.end():],
                                          flags=re.DOTALL)
            if tag_content_match:
                tag_info.content = tag_content_match.group(1)
            return tag_info
    kwargs_found: bool = False
    params: Dict[str, str] = {}
    finish_slash: Optional[str] = None
    match_end: Optional[int] = None
    for tag_header_match in tag_header_matches:
        params_str, finish_slash = tag_header_match.group(1), tag_header_match.group(2)
        params = dict(re.findall(r'\b(.*?)="(.*?)"', params_str, flags=re.DOTALL))
        for k, v in kwargs.items():
            if params.get(k) == v:
                kwargs_found = True
            else:
                kwargs_found = False
                break
        if not kwargs_found:
            continue
        else:
            match_end = tag_header_match.end()
            break

    if not kwargs_found:
        return None

    tag_info.params = params
    if not with_content:
        return tag_info
    elif finish_slash:
        return tag_info
    else:
        if match_end:
            tag_content_match = re.search(rf'(.*?)</{full_tag_name}>', body[match_end:],
                                          flags=re.DOTALL)
            if content := tag_content_match.group(1):
                tag_info.content = content
            return tag_info


def get_tag_info_list(tag_name: str, body: str) -> List[TagInfo]:
    tag_info_list: List[TagInfo] = []
    full_tag_name = get_full_tag_name(tag_name, body)
    if not full_tag_name:
        return tag_info_list
    tag_header_iter = re.finditer(rf'<{full_tag_name}(|\s+?|\s+?.*?|\s+?.*?\s+?)(?:>|(/>))', body, flags=re.DOTALL)
    for tag_header_match in tag_header_iter:
        params_str, finish_slash = tag_header_match.group(1), tag_header_match.group(2)
        params: Dict[str, str] = {}
        params_iter = re.finditer(r'\b(.*?)="(.*?)"', params_str, flags=re.DOTALL)
        for param in params_iter:
            params[param.group(1)] = param.group(2)
        tag_info: TagInfo = TagInfo(name=full_tag_name, params=params)
        if not finish_slash:
            # Нет финишного слэша - значит, есть контент
            tag_content_match = re.search(rf'(.*?)</{full_tag_name}>', body[tag_header_match.end():], flags=re.DOTALL)
            if content := tag_content_match.group(1):
                tag_info.content = content
        tag_info_list.append(tag_info)
    return tag_info_list


def get_tag_info(tag_name: str, body: str) -> Optional[TagInfo]:
    full_tag_name = get_full_tag_name(tag_name, body)
    if not full_tag_name:
        return None
    tag_header_match = re.search(rf'<{full_tag_name}(|\s+?|\s+?.*?|\s+?.*?\s+?)(?:>|(/>))', body, flags=re.DOTALL)
    if not tag_header_match:
        return None
    params_str, finish_slash = tag_header_match.group(1), tag_header_match.group(2)
    params: Dict[str, str] = {}
    params_iter = re.finditer(r'\b(.*?)="(.*?)"', params_str, flags=re.DOTALL)
    for param in params_iter:
        params[param.group(1)] = param.group(2)
    tag_info: TagInfo = TagInfo(name=full_tag_name, params=params)
    if not finish_slash:
        # Нет финишного слэша - значит, есть контент
        tag_content_match = re.search(rf'{tag_header_match.group(0)}(.*?)</{full_tag_name}>', body, flags=re.DOTALL)
        if content := tag_content_match.group(1):
            tag_info.content = content
    return tag_info


# INFO: end block ------------------------------------------------------------------------------





def get_tag_full_content(tag_name: str, body: str) -> Optional[str]:
    """Получить полный контент тега (с закрывающим и открывающим тегами)
    Пример: <tag par1="par1" par2="par2">content</tag>
    В случае наличия самозакрывающего тега возвращает его.
    Пример: <tag par1="par1" />"""
    open_tag_match = re.search(rf'<((?:\w+:)?{tag_name}).*?>', body, re.DOTALL)
    if open_tag_match:
        open_tag_text = open_tag_match.group(1)  # Название тега с возможным префиксом
        full_text_match = re.search(rf'<{open_tag_text}.*?</{open_tag_text}>', body, re.DOTALL)
        if full_text_match:
            return full_text_match.group(0)
        return open_tag_match.group(0)  # Возвращаем текст только открывающего или самозакрывающего тега
    return None


def get_tag_content(tag_name: str, content_body: str, get_full_text: bool = False) -> Optional[str]:
    """Получить содержимое тега (внутри открывающего и закрывающего тега)
    по названию тега и тексту, в котором этот тег встречается. Указав
    get_full_text = True мы получим полный контент тега, включая открывающий
    и закрывающий теги (или самозакрывающий тег сам по себе). Это может быть полезно
    для получения параметров тега в контенте, возвращенном с флагом get_full_text = True"""
    open_tag_text_match = re.search(rf'<((?:\w+:)?{tag_name})>', content_body, re.DOTALL)
    if not open_tag_text_match and not get_full_text:
        return None
    open_tag_text = open_tag_text_match.group(1)
    close_tag_text = '/' + open_tag_text
    tag_content_match = re.search(rf'<{open_tag_text}[^>]*>(.*?)<{close_tag_text}>', content_body, re.DOTALL)
    if tag_content_match:
        return tag_content_match.group(0) if get_full_text else tag_content_match.group(1)
    else:
        if get_full_text:
            return get_tag_params_content(tag_name, content_body)
    return None


def get_tag_params_content(tag_name: str, content_body: str) -> Optional[str]:
    """Получить содержимое тега, в котором находятся его параметры -
    обычно в самозакрывающемся теге (между названием тега и />) или
    в открывающем теге (между названием тега и >)"""
    pattern = rf'<(?:\w+:)?{tag_name}(\s[^>/]*)?(?:/?>|/>)'
    tag_params_content_match = re.search(pattern, content_body, re.DOTALL)
    return tag_params_content_match.group(1) if tag_params_content_match else None


def get_tag_params_content_iter(tag_name: str, content_body: str) -> Iterator[re.Match[str]]:
    """Получить итератор для содержимого тегов с их параметрами"""
    pattern = rf'<(?:\w+:)?{tag_name}(\s[^>/]*)?(?:/?>|/>)'
    return re.finditer(pattern, content_body, re.DOTALL)


def get_tag_param_text(param_name: str, tag_params_content: str) -> Optional[str]:
    """Получить значение параметра тега"""
    pattern = rf'{param_name}="(.*?)"'
    param_text_match = re.search(pattern, tag_params_content, re.DOTALL)
    return param_text_match.group(1) if param_text_match else None


# INFO: end block ------------------------------------------------------------------------------


def get_label(body: str) -> Optional[Label]:
    label_content = get_tag_content('label', body)
    if label_content is None:
        return None
    label_text_content = get_tag_content('text', label_content)
    audio_content: Optional[AudioContent] = None
    audio_params_content = get_tag_params_content('audio', label_content)
    audio_uri = get_tag_param_text('uri', audio_params_content)
    audio_size = get_tag_param_text('size', audio_params_content)
    if audio_uri and audio_size:
        audio_content = AudioContent(uri=audio_uri, size=float(audio_size))
    label_obj: Label = Label(text=label_text_content, audio=audio_content)
    return label_obj


def get_content_list_ref(body: str) -> Optional[str]:
    return get_tag_content('contentListRef', body)


def get_input_question(iq_body: str) -> Optional[InputQuestion]:
    iq_id = get_tag_param_text('id', iq_body)
    if iq_id is None:
        return None
    iq_label = get_label(iq_body)
    if iq_label is None:
        return None
    input_types_body = get_tag_content('inputTypes', iq_body)
    input_types = []
    if input_types_body is None:
        return None
    input_params_iter = get_tag_params_content_iter('input', input_types_body)
    for input_match in input_params_iter:
        input_type_value = get_tag_param_text('type', input_match.group(1))
        if input_type_value is not None:
            input_types.append(input_type_value)
    input_question: InputQuestion = InputQuestion(id=iq_id, label=iq_label, input_types=input_types)
    return input_question


def get_choice(choice_body: str) -> Optional[Choice]:

    choice_id = get_tag_param_text('choice', choice_body)
    if choice_id is None:
        return None

    choice_label = get_label(choice_body)
    if choice_label is None:
        return None

    choice: Choice = Choice(id=choice_id, label=choice_label)
    return choice


def get_mc_question(mcq_body: str) -> Optional[MultipleChoiceQuestion]:
    mcq_id = get_tag_param_text('id', mcq_body)
    choices_body = get_tag_content('choices', mcq_body)
    mcq_choices: List[Choice] = []
    if choices_body is not None:
        choice_matches = re.finditer(r'<ns1:choice .*?>.*?</ns1:choice>', choices_body, re.DOTALL)
        for choice_match in choice_matches:
            choice_body = choice_match.group(0)
            if choice := get_choice(choice_body):
                mcq_choices.append(choice)

        mcq_body = mcq_body.replace(choices_body, '')

    mcq_label = get_label(mcq_body)
    if mcq_label is None:
        return None

    mcq: MultipleChoiceQuestion = MultipleChoiceQuestion(id=mcq_id, label=mcq_label, choices=mcq_choices)
    return mcq


def _get_questions(questions_body: str) -> Questions:
    print(f'Questions body: {questions_body}')
    questions: Questions = Questions()

    input_question_matches = re.finditer(r'<ns1:inputQuestion.*?</ns1:inputQuestion>', questions_body, re.DOTALL)
    # Избавляемся от inputQuestion в теле ответа и формируем набор inputQuestion
    input_questions: List[InputQuestion] = []
    for iq_match in input_question_matches:
        iq = iq_match.group(0)
        if input_question := get_input_question(iq):
            input_questions.append(input_question)
            questions_body = questions_body.replace(iq, '')
    questions.input_questions = input_questions

    multiple_choice_question_matches = re.finditer(r'<ns1:multipleChoiceQuestion.*?</ns1:multipleChoiceQuestion>',
                                                   questions_body, re.DOTALL)
    # Избавляемся от multipleChoiceQuestion в теле ответа и формируем набор multipleChoiceQuestion
    mc_questions: List[MultipleChoiceQuestion] = []
    for mcq_match in multiple_choice_question_matches:
        mcq = mcq_match.group(0)
        if multiple_choice_question := get_mc_question(mcq):
            mc_questions.append(multiple_choice_question)
            questions_body = questions_body.replace(mcq, '')
    # print(f'Questions body after clean: {questions_body}')
    questions.multiple_choice_questions = mc_questions
    # Text is sanitized - no more inputQuestion and multipleChoiceQuestion
    if content_list_ref := get_content_list_ref(questions_body):
        questions.content_list_ref = content_list_ref
        return questions

    if label := get_label(questions_body):
        questions.label = label
        return questions

    return questions
