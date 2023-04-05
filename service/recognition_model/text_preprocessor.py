import re
import os
from typing import List, NewType, Sequence

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import pymorphy2
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from numpy import ndarray

from common.settings import BASE_DIR


Sentence = NewType('Sentence', str)
Word = NewType('Word', str)


class TextPreprocessor:
    """A tool for processing and converting texts"""
    def __init__(self, tokenizer_name: str, num_words: int = 10000, max_review_len: int = 100) -> None:
        self.__tokenizer = self.__load_tokenizer(tokenizer_name)
        self.__punctuation_marks = ['!', ',', '(', ')', ':', '-', '?', '.', '..', '...']
        self.__stop_words = stopwords.words("russian")
        self.__morph = pymorphy2.MorphAnalyzer()
        self.num_words = num_words
        self.max_review_len = max_review_len

    def preprocess(self, text: str) -> List[Word]:
        """
            Text preprocessing. Removing stop words and punctuation marks and bringing words into normal form.
            Return the text as a list of words.
        """
        tokens = word_tokenize(text.lower())
        preprocessed_text = []
        for token in tokens:
            if token not in self.__punctuation_marks:
                lemma = self.__morph.parse(token)[0].normal_form
                if lemma not in self.__stop_words:
                    preprocessed_text.append(lemma)
        return preprocessed_text

    def transform_text(self, texts: Sequence[Sequence[Word]]) -> ndarray:
        """Transform text to list of tokens wive fixed length self.max_review_len"""
        return pad_sequences(
            self.__tokenizer.texts_to_sequences(texts),
            maxlen=self.max_review_len,
        )

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

    @classmethod
    def __load_tokenizer(cls, tokenizer_name: str) -> Tokenizer:
        """Load tokenizer from pickle"""
        path = os.path.join(BASE_DIR, 'service', 'recognition_model', 'model_pickle', f'{tokenizer_name}.pickle')
        with open(path, 'rb') as handle:
            return pickle.load(handle)


nltk.download('stopwords')
