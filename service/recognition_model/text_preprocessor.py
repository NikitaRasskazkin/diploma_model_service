import re
from typing import List, NewType


Sentence = NewType('Sentence', str)


class TextPreprocessor:
    """A tool for processing and converting texts"""
    def __init__(self) -> None:
        pass

    @classmethod
    def split_text_by_sentences(cls, text: str) -> List[Sentence]:
        """Split text by sentences. Return list of sentences"""
        text = text.strip()
        split_text = re.split(r'([.!?]) ', text)
        sentences = []
        for string in split_text:
            if string in ['.', '!', '?'] and sentences:
                sentences[-1] += string
            else:
                sentences.append(Sentence(string.strip()))
        if sentences and sentences[-1][-1] not in ['.', '!', '?']:
            sentences[-1] += '.'
        return sentences
