"""ML model and datastructure for recognition automatic paraphrases in texts"""

from typing import List
from dataclasses import dataclass

from .text_preprocessor import TextPreprocessor, Sentence


@dataclass()
class RecognitionResult:
    """The result of recognizing a sentence"""
    sentence: Sentence
    is_paraphrase: bool
    probability: float


class RecognitionModel:
    """ML model for recognition automatic paraphrases in texts"""
    def __init__(self) -> None:
        self.__text_preprocessor = TextPreprocessor()

    def get_recognition(self, text: str) -> List[RecognitionResult]:
        sentences = self.__text_preprocessor.split_text_by_sentences(text)
        return [
            RecognitionResult(sentence, False, 0.0)
            for sentence in sentences
        ]
