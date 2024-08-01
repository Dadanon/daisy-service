from typing import Optional, List

import pytest

from dodp_new.general import TagInfo
from dodp_new.tests.pairs import (
    tag_info_test_pairs,
    full_tag_name_valid_test_pairs,
    full_tag_name_invalid_test_pairs,
    tag_info_list_test_pairs,
    tag_info_by_params_test_pairs_invalid,
    tag_info_by_params_test_pairs_valid,
    tag_info_list_by_params_test_pairs, root_tag_info_test_pairs
)
from dodp_new.functions import (
    get_full_tag_name,
    get_tag_info_by_params,
    get_tag_info_list_by_params, get_root_tag_info
)


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


@pytest.mark.parametrize('tag_name, test_text, params', tag_info_by_params_test_pairs_invalid)
def test_get_tag_info_by_params_invalid(tag_name: str, test_text: str, params: dict):
    # Act
    tag_info = get_tag_info_by_params(tag_name, test_text, **params)

    # Assert
    assert tag_info is None


@pytest.mark.parametrize('tag_name, test_text, params, result', [*tag_info_by_params_test_pairs_valid, *tag_info_test_pairs])
def test_get_tag_info_by_params_valid(tag_name: str, test_text: str, params: dict, result: TagInfo):
    # Act
    tag_info = get_tag_info_by_params(tag_name, test_text, **params)

    # Assert
    assert tag_info is not None
    assert tag_info.name == result.name
    assert tag_info.params == result.params
    assert tag_info.content == result.content


@pytest.mark.parametrize('tag_name, test_text, params, list_to_assert', [*tag_info_list_by_params_test_pairs, *tag_info_list_test_pairs])
def test_get_tag_info_list_by_params(tag_name: str, test_text: str, params: dict, list_to_assert: List[TagInfo]):
    # Act
    tag_info_list = get_tag_info_list_by_params(tag_name, test_text, **params)

    # Assert
    assert len(tag_info_list) == len(list_to_assert)
    for i in range(len(tag_info_list)):
        tag_info = tag_info_list[i]
        tag_info_to_assert = list_to_assert[i]

        assert tag_info.name == tag_info_to_assert.name
        assert tag_info.params == tag_info_to_assert.params
        assert tag_info.content == tag_info_to_assert.content


@pytest.mark.parametrize('tag_name, test_text, result', root_tag_info_test_pairs)
def test_get_root_tag_info(tag_name: str, test_text: str, result: TagInfo):
    # Act
    tag_info = get_root_tag_info(tag_name, test_text)

    # Assert
    assert tag_info is not None
    assert tag_info.name == result.name
    assert tag_info.params == result.params
    assert tag_info.content == result.content
