# clinical-assertion-data

This repository contains the assertion data introduced in our paper: [Assertion Detection in Clinical Notes: Medical Language Models to the Rescue?](https://www.aclweb.org/anthology/2021.nlpmc-1.5/), NLPMC @ NAACL 2021.

## Assertion Labels

We release 5,000 assertion labels manually annotated based on clinical notes from the MIMIC-III database. The table below shows the distribution of labels for the different note types.

| | PRESENT | POSSIBLE | ABSENT |
| --- | --- | --- | --- |
| Discharge Summaries | 2,610 | 250 | 980 |
| Physician Letters | 204 | 34 | 66 |
| Nurse Letters | 293 | 14 | 59 |
| Radiology Reports | 295 | 67 | 138 |

## Creating sample files

In order to use our data, you need to have access to the MIMIC-III database, which is freely available after completing the steps described here: https://mimic.mit.edu/iv/access/. 

To create training samples from our label files, simply follow these steps:

1. Install Requirements:
`pip install -r requirements.txt`

2. Run conversion script:

```
python3 convert_to_samples.py \
 --label_path {...} \   # required, path to label file, e.g. labels/nursing_labels.csv
 --mimic_notes_path {...} \   # required, path to MIMIC-III NOTEEVENTS.csv
 --save_path {...}   # path to save created samples
```
3. Don't forget to add the special token `[entity]` to your model vocab for training.

## Cite
```
@inproceedings{vanAken21,
    title = "Assertion Detection in Clinical Notes: Medical Language Models to the Rescue?",
    author = "van Aken, Betty  and
      Trajanovska, Ivana  and
      Siu, Amy  and
      Mayrdorfer, Manuel  and
      Budde, Klemens  and
      Loeser, Alexander",
    booktitle = "Proceedings of the Second Workshop on Natural Language Processing for Medical Conversations",
    year = "2021",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2021.nlpmc-1.5"
}
```
