"""
This script demonstrates a simple pipeline that takes text as an input, detects disease entities via scispacy and
classifies their assertion type with our assertion classification model.
"""

from enum import Enum
import re
from typing import List

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

import spacy
import scispacy

nlp = spacy.load("en_ner_bc5cdr_md")


class AssertionType(Enum):
    PRESENT = 0
    ABSENT = 1
    POSSIBLE = 2


class AnnotatedSentence:
    def __init__(self, sentence: str, entity_start_char: int, entity_end_char: int):
        self.entity_start_char = entity_start_char
        self.entity_end_char = entity_end_char
        self.sentence = sentence
        self.entity = sentence[entity_start_char:entity_end_char]

    def bert_annotated_text(self) -> str:
        return self.sentence[:self.entity_start_char] \
               + "[entity] " + self.entity + " [entity]" \
               + self.sentence[self.entity_end_char:]


class EntityWithAssertion:
    def __init__(self, entity: str, assertion_type: AssertionType):
        self.entity = entity
        self.assertion_type = assertion_type

    def __repr__(self) -> str:
        return f"{self.assertion_type.name}: {self.entity}"


def split_into_sentences(text: str) -> List[str]:
    regex_pattern = r"(\.|!|\?)"
    split = re.split(regex_pattern, text)  # split by punctuation
    result = [split[i] + split[i + 1] for i in range(0, len(split) - 1, 2)]  # merge punctuation with text
    if len(split) % 2 != 0:
        result.append(split[-1])
    return [sentence for sentence in result if sentence.strip() != ""]  # remove empty strings


def build_entity_annotated_sentences(input_sentence) -> List[AnnotatedSentence]:
    found_entities = nlp(input_sentence).ents
    return [AnnotatedSentence(input_sentence, ent.start_char, ent.end_char) for ent in found_entities if
            ent.label_ == "DISEASE"]


def classify_assertions_in_sentences(sentences: List[AnnotatedSentence]) -> List[EntityWithAssertion]:
    bert_input_texts = [sentence.bert_annotated_text() for sentence in sentences]

    tokenizer = AutoTokenizer.from_pretrained("bvanaken/clinical-assertion-negation-bert")
    model = AutoModelForSequenceClassification.from_pretrained("bvanaken/clinical-assertion-negation-bert")

    tokenized_input = tokenizer(bert_input_texts, return_tensors="pt", padding=True)
    outputs = model(**tokenized_input)

    predicted_labels = torch.argmax(outputs.logits, dim=1)

    entities_with_assertions = []
    for i, sentence in enumerate(sentences):
        label = predicted_labels[i].item()
        entity_with_assertion = EntityWithAssertion(sentence.entity, AssertionType(label))
        entities_with_assertions.append(entity_with_assertion)

    return entities_with_assertions


def find_and_classify_assertions_in_text(input_text: str) -> List[EntityWithAssertion]:
    sentences = split_into_sentences(input_text)

    input_sentences = []
    for sentence in sentences:
        entity_annotated_sentences = build_entity_annotated_sentences(sentence)
        input_sentences += entity_annotated_sentences

    return classify_assertions_in_sentences(input_sentences)


if __name__ == '__main__':
    text = "The patient has measles and fever but denies any chest pain. She also has shoulder pain."

    assertions = find_and_classify_assertions_in_text(text)
    print(assertions)
