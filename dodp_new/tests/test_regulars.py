import re
from typing import Optional, List

import pytest

from dodp_new.general import TagInfo
from dodp_new.tests.pairs import tag_info_test_pairs, full_tag_name_valid_test_pairs, full_tag_name_invalid_test_pairs, \
    multiple_tag_info_test_pairs, tag_info_by_params_test_pairs_invalid, tag_info_by_params_test_pairs_valid
from dodp_new.functions import get_tag_info, get_full_tag_name, get_tag_info_list, get_tag_info_by_params
from dodp_new.tests.texts import text_1


def get_normalized(text: Optional[str]) -> Optional[str]:
    return re.sub(r'\n|\s{2,}', '', text) if text else None


@pytest.mark.parametrize("tag_name, test_text, name, params, content", tag_info_test_pairs)
def test_get_tag_info(tag_name: str, test_text: str, name: str, params: dict, content: str):
    # Act
    tag_info = get_tag_info(tag_name, test_text)

    # Assert
    assert tag_info is not None
    assert tag_info.name == name
    assert tag_info.params == params
    assert get_normalized(tag_info.content) == get_normalized(content)


@pytest.mark.parametrize('tag_name, test_text, name', full_tag_name_valid_test_pairs)
def test_get_full_tag_name_valid(tag_name: str, test_text: str, name: str):
    # Act
    tag_name = get_full_tag_name(tag_name, test_text)

    # Assert
    assert tag_name is not None
    assert tag_name == name


@pytest.mark.parametrize('tag_name, test_text, name', full_tag_name_invalid_test_pairs)
def test_get_full_tag_name_invalid(tag_name: str, test_text: str, name: Optional[str]):
    # Act
    tag_name = get_full_tag_name(tag_name, test_text)

    # Assert
    assert tag_name is None


@pytest.mark.parametrize('tag_name, test_text, list_to_assert', multiple_tag_info_test_pairs)
def test_get_tag_info_list(tag_name: str, test_text: str, list_to_assert: List[TagInfo]):
    # Act
    tag_info_list = get_tag_info_list(tag_name, test_text)

    # Assert
    assert tag_info_list is not None
    assert len(tag_info_list) == len(list_to_assert)

    for i in range(len(tag_info_list)):
        tag_info = tag_info_list[i]
        tag_info_to_assert = list_to_assert[i]

        assert tag_info.name == tag_info_to_assert.name
        assert tag_info.params == tag_info_to_assert.params
        assert get_normalized(tag_info.content) == get_normalized(tag_info_to_assert.content)


@pytest.mark.parametrize('tag_name, test_text, with_content, params', tag_info_by_params_test_pairs_invalid)
def test_get_tag_info_by_params_invalid(tag_name: str, test_text: str, with_content: bool, params: dict):
    # Act
    tag_info = get_tag_info_by_params(tag_name, test_text, with_content, **params)

    # Assert
    assert tag_info is None


@pytest.mark.parametrize('tag_name, test_text, with_content, params, result', tag_info_by_params_test_pairs_valid)
def test_get_tag_info_by_params_valid(tag_name: str, test_text: str, with_content: bool, params: dict, result: TagInfo):
    # Act
    tag_info = get_tag_info_by_params(tag_name, test_text, with_content, **params)

    # Assert
    assert tag_info is not None
    assert tag_info.name == result.name
    assert tag_info.params == result.params
    assert get_normalized(tag_info.content) == get_normalized(result.content)
