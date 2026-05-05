import functools
import importlib.util
from typing import Any

from ..morpheme import Morpheme

successful_import: bool = False
_mecabko: Any = None


def setup_mecabko() -> None:
    global successful_import
    global _mecabko

    if importlib.util.find_spec("anki_morphs_mecab_korean"):
        reading = importlib.import_module("anki_morphs_mecab_korean.reading")
    else:
        return

    _mecabko = reading.MecabKoreanController()
    successful_import = True


# the cache needs to have a max size to maintain garbage collection
@functools.lru_cache(maxsize=131072)
def get_morphemes_mecabko(expression: str) -> list[Morpheme]:
    if not successful_import or _mecabko is None:
        return []

    morphs = _mecabko.get_morphs(expression)
    actual_morphs: list[Morpheme] = []

    for lemma, surface, pos, sub_pos, _ in morphs:
        if pos in ["記号", "その他"]:
            continue
        actual_morphs.append(
            Morpheme(
                lemma=lemma,
                inflection=surface,
                part_of_speech=pos,
                sub_part_of_speech=sub_pos,
            )
        )

    return actual_morphs
