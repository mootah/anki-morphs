import os
import sys
from collections.abc import Iterator
from test.test_globals import PATH_TESTS_DATA
from unittest import mock

import pytest

from ankimorphs.morpheme import Morpheme
from ankimorphs.morphemizers import spacy_wrapper
from ankimorphs.morphemizers.morphemizer_utils import get_morphemizer_by_description


@pytest.fixture(
    scope="module"  # module-scope: created and destroyed once per module. Cached.
)
def _fake_environment_fixture() -> Iterator[None]:
    patch_testing_variable = mock.patch.object(
        spacy_wrapper, "testing_environment", True
    )
    fake_morphemizers_path = os.path.join(PATH_TESTS_DATA, "morphemizers")

    sys.path.append(fake_morphemizers_path)
    patch_testing_variable.start()
    yield
    patch_testing_variable.stop()
    sys.path.remove(fake_morphemizers_path)


@pytest.mark.external_morphemizers
def test_mecab_morpheme_generation(  # pylint:disable=unused-argument
    _fake_environment_fixture: None,
) -> None:
    morphemizer = get_morphemizer_by_description("AnkiMorphs: Japanese")
    assert morphemizer is not None

    sentence = "本当に重要な任務の時しか 動かない"
    correct_morphs: set[Morpheme] = {
        Morpheme("本当に", "本当に"),
        Morpheme("重要", "重要"),
        Morpheme("だ", "な"),
        Morpheme("任務", "任務"),
        Morpheme("の", "の"),
        Morpheme("時", "時"),
        Morpheme("しか", "しか"),
        Morpheme("動く", "動か"),
        Morpheme("ない", "ない"),
    }

    extracted_morphs = next(morphemizer.get_morphemes([sentence]))
    assert len(extracted_morphs) == 9

    for morph in extracted_morphs:
        assert morph in correct_morphs


@pytest.mark.external_morphemizers
def test_jieba_morpheme_generation(  # pylint:disable=unused-argument
    _fake_environment_fixture: None,
) -> None:
    morphemizer = get_morphemizer_by_description("AnkiMorphs: Chinese")
    assert morphemizer is not None

    sentence = "请您说得慢些好吗？"
    correct_morphs: set[Morpheme] = {
        Morpheme("吗", "吗"),
        Morpheme("好", "好"),
        Morpheme("得", "得"),
        Morpheme("您", "您"),
        Morpheme("慢些", "慢些"),
        Morpheme("说", "说"),
        Morpheme("请", "请"),
    }

    extracted_morphs = next(morphemizer.get_morphemes([sentence]))
    assert len(extracted_morphs) == 7

    for morph in extracted_morphs:
        assert morph in correct_morphs

    sentence = "一，二，三，跳！"
    correct_morphs = {
        Morpheme("一", "一"),
        Morpheme("二", "二"),
        Morpheme("三", "三"),
        Morpheme("跳", "跳"),
    }

    extracted_morphs = next(morphemizer.get_morphemes([sentence]))
    assert len(extracted_morphs) == 4

    for morph in extracted_morphs:
        assert morph in correct_morphs


@pytest.mark.external_morphemizers
def test_mecabko_morpheme_generation(  # pylint:disable=unused-argument
    _fake_environment_fixture: None,
) -> None:
    morphemizer = get_morphemizer_by_description("AnkiMorphs: Korean")
    assert morphemizer is not None

    sentence = "정말 중요한 임무일 때만 움직인다"
    correct_morphs: set[Morpheme] = {
        Morpheme("정말", "정말", "感動詞", "感動詞"),
        Morpheme("중요", "중요", "名詞", "一般"),
        Morpheme("하", "한", "接尾辞", "形容詞接尾辞"),
        Morpheme("임무", "임무", "名詞", "一般"),
        Morpheme("이", "일", "用言", "指定詞"),
        Morpheme("때", "때", "名詞", "一般"),
        Morpheme("만", "만", "助詞", "補助詞"),
        Morpheme("움직이", "움직인다", "用言", "動詞"),
    }

    extracted_morphs = next(morphemizer.get_morphemes([sentence]))
    assert len(extracted_morphs) == 8

    for morph in extracted_morphs:
        assert morph in correct_morphs
