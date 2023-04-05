"""ML model and datastructure for recognition automatic paraphrases in texts"""

from typing import List
from dataclasses import dataclass

from .text_preprocessor import TextPreprocessor, Sentence


@dataclass()
class RecognitionResult:
    """The result of recognizing a sentence"""
    sentence: Sentence      # Sentence text.
    is_paraphrase: bool     # Binary classification of a sentence. True if the sentence is paraphrased.
    probability: float      # The probability that the sentence is rephrased.


class RecognitionModel:
    """ML model for recognition automatic paraphrases in texts"""
    def __init__(self) -> None:
        self.__text_preprocessor = TextPreprocessor()

    @property
    def version(self):
        """Version of the ML model"""
        return '0.0.0'

    @property
    def weights_slug(self):
        """Slug of the ML model weights. <weights_name>_<weights_version>"""
        return 'base_model_000'

    def get_recognition(self, text: str) -> List[RecognitionResult]:
        """
            Performs recognition of paraphrased sentences. The text is submitted to the input.
            The result is a list of RecognitionResult for each sentence.
        """
        sentences = self.__text_preprocessor.split_text_by_sentences(text)
        return [
            RecognitionResult(sentence, False, 0.0)
            for sentence in sentences
        ]
