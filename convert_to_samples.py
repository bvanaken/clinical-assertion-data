import pandas as pd
import fire


def index_of_punctuation(str, backwards=False):
    # Find the index of the next punctuation (to determine sentence boundaries)
    punctuations = [".", "\n\n", "!", "?"]
    if backwards:
        i_punct = -1
        for punc in punctuations:
            i_temp = str.rfind(punc)
            if i_temp > i_punct:
                i_punct = i_temp
    else:
        i_punct = 1000000
        for punc in punctuations:
            i_temp = str.find(punc)
            if i_temp != -1 and i_temp < i_punct:
                i_punct = i_temp
    return i_punct


def create_sentences_from_labels(label_path, mimic_notes_path, save_path="assertion_samples.csv"):
    labels_df = pd.read_csv(label_path)
    notes_df = pd.read_csv(mimic_notes_path)

    sentences = []
    labels = []
    for i, annotation in labels_df.iterrows():
        start = annotation["start_index"]
        end = annotation["end_index"]

        sample = notes_df[notes_df.ROW_ID == annotation["row_id"]].iloc[0]
        text = sample.TEXT

        text = text[:start] + " [entity] " + text[start:end] + " [entity] " + text[end:]

        sent_start = index_of_punctuation(text[:start], backwards=True) + 1
        sent_end = index_of_punctuation(text[end:], backwards=False) + len(text[:end]) + 1

        sentence = text[sent_start:sent_end].replace("\n", " ").strip()

        sentences.append(sentence)
        if annotation["label"] == "PRESENT":
            labels.append(0)
        elif annotation["label"] == "ABSENT":
            labels.append(1)
        elif annotation["label"] == "POSSIBLE":
            labels.append(2)

    df = pd.DataFrame(columns=["text", "label"])
    df["text"] = sentences
    df["label"] = labels
    df.to_csv(save_path, index=False)


if __name__ == '__main__':
    fire.Fire(create_sentences_from_labels)
