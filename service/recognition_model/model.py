"""ML model and datastructure for recognition automatic paraphrases in texts"""

import os
from typing import List
from dataclasses import dataclass

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM

from common.settings import BASE_DIR
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
        num_words = 10000
        max_review_len = 100
        self.__text_preprocessor = TextPreprocessor('tokenizer_mt5', num_words, max_review_len)
        self.__model = Sequential()
        self.__model.add(Embedding(num_words, 64, input_length=max_review_len))
        self.__model.add(LSTM(128, return_sequences=True))
        self.__model.add(LSTM(128))
        self.__model.add(Dense(1, activation='sigmoid'))
        self.__model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy', tf.metrics.Precision()],
        )
        weights_path = os.path.join(
            BASE_DIR, 'service', 'recognition_model', 'model_pickle', f'{self.weights_slug}.h5'
        )
        self.__model.load_weights(weights_path)

    @property
    def version(self):
        """Version of the ML model"""
        return '0.0.0'

    @property
    def weights_slug(self):
        """Slug of the ML model weights. <weights_name>_<weights_version>"""
        return 'base_model_mt5_000'

    def predict(self, text: str) -> List[RecognitionResult]:
        """
            Performs recognition of paraphrased sentences. The text is submitted to the input.
            The result is a list of RecognitionResult for each sentence.
        """
        p_text = self.__text_preprocessor.preprocess(text)
        prediction = self.__model.predict(self.__text_preprocessor.transform_text([p_text]), verbose=0)
        probability = prediction[0][0]
        sentences = self.__text_preprocessor.split_text_by_sentences(text)
        return [
            RecognitionResult(sentence, probability > 0.5, probability)
            for sentence in sentences
        ]
