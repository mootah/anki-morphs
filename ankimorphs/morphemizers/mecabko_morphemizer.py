from collections.abc import Iterator

from ..morpheme import Morpheme
from ..morphemizers.morphemizer import Morphemizer
from . import mecabko_wrapper


class MecabKoMorphemizer(Morphemizer):
    def __init__(self) -> None:
        super().__init__()
        mecabko_wrapper.setup_mecabko()

    def init_successful(self) -> bool:
        return mecabko_wrapper.successful_import

    def get_morphemes(self, sentences: list[str]) -> Iterator[list[Morpheme]]:
        for sentence in sentences:
            yield mecabko_wrapper.get_morphemes_mecabko(sentence)

    def get_description(self) -> str:
        return "AnkiMorphs: Korean"
