from typing import Optional, List, Iterator, Dict
import re

from result import Result, Err, Ok

from dodp_new.general import Label, AudioContent, InputQuestion, MultipleChoiceQuestion, Choice, Questions, TagInfo, \
    BookContent, LGKContent, LKFContent


# INFO: regular functions block ----------------------------------------------------------------


# INFO: tested functions block -----------------------------------------------------------------


def get_full_tag_name(tag_name: str, body: str) -> Optional[str]:
    """Внутренний метод, использование вовне под сомнением.
    Получение полного названия тега в тексте(включая возможный префикс)"""
    full_name_match = re.search(rf'<((?:\w+:)?{tag_name})', body, re.DOTALL)
    return full_name_match.group(1) if full_name_match else None


def get_tag_info_list_by_params(tag_name: str, body: str, **kwargs) -> List[TagInfo]:
    """Внешний метод.
    Получение списка объектов TagInfo по названию тега и параметрам (опционально)"""
    full_tag_name = get_full_tag_name(tag_name, body)
    if not full_tag_name:
        return []
    tag_info_list: List[TagInfo] = []

    tag_header_matches = re.finditer(rf'<{full_tag_name}(|\s+?|\s+?.*?|\s+?.*?\s+?)(?:>|(/>))', body, flags=re.DOTALL)
    if not kwargs:  # Тогда берем ВСЕ
        for tag_header_match in tag_header_matches:
            finish_slash = tag_header_match.group(2)
            params = dict(re.findall(r'\b(.*?)="(.*?)"', tag_header_match.group(1), flags=re.DOTALL))
            tag_info: TagInfo = TagInfo(name=full_tag_name, params=params)
            if not finish_slash:
                tag_content_match = re.search(rf'(.*?)</{full_tag_name}>', body[tag_header_match.end():],
                                              flags=re.DOTALL)
                if tag_content_match:
                    tag_info.content = tag_content_match.group(1)
            tag_info_list.append(tag_info)
        return tag_info_list

    kwargs_found: bool = False
    for tag_header_match in tag_header_matches:
        tag_info: TagInfo = TagInfo(name=full_tag_name)
        params_str, finish_slash = tag_header_match.group(1), tag_header_match.group(2)
        params = dict(re.findall(r'\b(.*?)="(.*?)"', params_str, flags=re.DOTALL))
        for k, v in kwargs.items():
            if params.get(k) == v:
                kwargs_found = True
            else:
                kwargs_found = False
                break
        if kwargs_found:
            tag_info.params = params
            if not finish_slash:
                tag_content_match = re.search(rf'(.*?)</{full_tag_name}>', body[tag_header_match.end():],
                                              flags=re.DOTALL)
                if tag_content_match:
                    tag_info.content = tag_content_match.group(1)
            tag_info_list.append(tag_info)
            kwargs_found = False
            continue
    return tag_info_list


def get_tag_info_by_params(tag_name: str, body: str, **kwargs) -> Optional[TagInfo]:
    """Внешний метод.
    Получение объекта TagInfo по названию тега и параметрам (опционально)"""
    full_tag_name = get_full_tag_name(tag_name, body)
    if not full_tag_name:
        return None
    tag_info: TagInfo = TagInfo(name=full_tag_name)

    tag_header_matches = re.finditer(rf'<{full_tag_name}(|\s+?|\s+?.*?|\s+?.*?\s+?)(?:>|(/>))', body, flags=re.DOTALL)
    if not kwargs:  # Тогда берем первый попавшийся
        first_match = tag_header_matches.__next__()
        tag_info.params = dict(re.findall(r'\b(.*?)="(.*?)"', first_match.group(1), flags=re.DOTALL))
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
    if finish_slash:
        return tag_info
    else:
        if match_end:
            tag_content_match = re.search(rf'(.*?)</{full_tag_name}>', body[match_end:],
                                          flags=re.DOTALL)
            if tag_content_match:
                tag_info.content = tag_content_match.group(1)
            return tag_info


def get_root_tag_info(tag_name: str, body: str) -> Optional[TagInfo]:
    full_tag_name = get_full_tag_name(tag_name, body)
    if not full_tag_name:
        return None
    search_content = body  # Начальная установка для поиска
    while True:
        any_tag_match = re.search(r'<([^/].*?)(?:|\s+?|\s+?.*?|\s+?.*?\s+?)(>|/>)', search_content, flags=re.DOTALL)
        if not any_tag_match:
            return None
        any_tag_full_name, any_tag_end = any_tag_match.group(1), any_tag_match.group(2)
        if any_tag_full_name == full_tag_name:  # Идеальный вариант
            return get_tag_info_by_params(tag_name, search_content[any_tag_match.start():])
        else:  # Любой другой - худший вариант :)
            if any_tag_end == '/>':  # Самозакрывающийся тег
                search_content = search_content[any_tag_match.end():]
            elif any_tag_end == '>':  # Ищем закрывающий тег и ищем дальше от него
                close_tag_match = re.search(rf'</{any_tag_full_name}>', search_content[any_tag_match.end():],
                                            flags=re.DOTALL)
                if not close_tag_match:
                    return None
                search_content = search_content[close_tag_match.end():]
            else:
                return None


# INFO: end block ------------------------------------------------------------------------------


def get_label(body: str | TagInfo) -> Optional[Label]:
    if isinstance(body, str):
        label_tag: TagInfo = get_tag_info_by_params('label', body)
        if not label_tag:
            return None
    else:
        label_tag: TagInfo = body
    label_text_tag: TagInfo = get_tag_info_by_params('text', label_tag.content)
    label_audio_tag: TagInfo = get_tag_info_by_params('audio', label_tag.content)
    audio_content: Optional[AudioContent] = None
    if label_audio_tag:
        audio_content = AudioContent(uri=label_audio_tag.params.get('uri'),
                                     size=float(label_audio_tag.params.get('size')))
    label: Label = Label(text=label_text_tag.content, audio=audio_content)
    return label


def get_content_list_ref(body: str) -> Optional[str]:
    content_list_ref_tag: TagInfo = get_root_tag_info('contentListRef', body)
    return content_list_ref_tag.content if content_list_ref_tag else None


def get_input_questions(iq_body: str) -> List[InputQuestion]:
    input_questions: List[InputQuestion] = []
    input_question_tags: List[TagInfo] = get_tag_info_list_by_params('inputQuestion', iq_body)
    for iq_tag in input_question_tags:
        iq_id: str = iq_tag.params.get('id')
        iq_label: Label = get_label(iq_tag.content)
        input_types_tag: TagInfo = get_tag_info_by_params('inputTypes', iq_tag.content)
        if iq_id is None or not iq_label or not input_types_tag:
            continue
        input_tags: List[TagInfo] = get_tag_info_list_by_params('input', input_types_tag.content)
        input_types: List[str] = [input_tag.params.get('type') for input_tag in input_tags]
        input_question: InputQuestion = InputQuestion(id=iq_id, label=iq_label, input_types=input_types)
        input_questions.append(input_question)
    return input_questions


def get_mc_questions(body: str) -> List[MultipleChoiceQuestion]:
    mc_questions: List[MultipleChoiceQuestion] = []
    mcq_tags: List[TagInfo] = get_tag_info_list_by_params('multipleChoiceQuestion', body)
    for mcq_tag in mcq_tags:
        mcq_id: str = mcq_tag.params.get('id')
        mcq_label_tag: TagInfo = get_root_tag_info('label', mcq_tag.content)
        mcq_label: Label = get_label(mcq_label_tag)
        choices_tag: TagInfo = get_tag_info_by_params('choices', mcq_tag.content)
        choice_tags: List[TagInfo] = get_tag_info_list_by_params('choice', choices_tag.content)

        mcq_choices: List[Choice] = [
            Choice(
                id=choice_tag.params.get('id'),
                label=get_label(choice_tag.content)
            )
            for choice_tag in choice_tags
        ]

        mcq: MultipleChoiceQuestion = MultipleChoiceQuestion(id=mcq_id, label=mcq_label, choices=mcq_choices)
        mc_questions.append(mcq)
    return mc_questions


def get_questions_object(response_body: str) -> Optional[Questions]:
    """Общий метод для получения объекта questions из тела ответа"""
    questions_tag: TagInfo = get_tag_info_by_params('questions', response_body)
    if not questions_tag:
        return None
    questions: Questions = Questions()
    # Добавляем label
    label_tag: TagInfo = get_root_tag_info('label', questions_tag.content)
    if label_tag:
        q_label = get_label(label_tag)
        if q_label:
            questions.label = q_label
    # Добавляем contentListRef
    q_content_list_ref: Optional[str] = get_content_list_ref(questions_tag.content)
    if q_content_list_ref:
        questions.content_list_ref = q_content_list_ref
    # Добавляем inputQuestion
    input_questions: List[InputQuestion] = get_input_questions(questions_tag.content)

    questions.input_questions = input_questions
    # Добавляем multipleChoiceQuestion
    mc_questions: List[MultipleChoiceQuestion] = get_mc_questions(questions_tag.content)
    questions.multiple_choice_questions = mc_questions

    return questions


def get_book_content_object(book_id: str, response_body: str) -> Result[BookContent, str]:
    book_content: BookContent = BookContent()
    lgk_tag = get_tag_info_by_params('resource', response_body, mimeType='application/lgk')
    if not lgk_tag:
        return Err(f'LGK block not found in book content resources with id: {book_id}')
    lgk_uri, lgk_size = lgk_tag.params['uri'], float(lgk_tag.params['size'])
    lgk_content: LGKContent = LGKContent(lgk_uri, lgk_size)
    book_content.lgk_content = lgk_content
    lkf_tags = get_tag_info_list_by_params('resource', response_body, mimeType='audio/x-lkf')
    for lkf_tag in lkf_tags:
        lkf_content: LKFContent = LKFContent(uri=lkf_tag.params['uri'], size=float(lkf_tag.params['size']))
        book_content.lkf_content.append(lkf_content)
    return Ok(book_content)
