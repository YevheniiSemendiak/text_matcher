# Text Matcher :mag:
##### Utility for storing texts in sentence-wise approach and searching for similar sentences in a context-aware approach.
##### Based on BERT NLP model ([bert-base-nli-mean-tokens](https://github.com/UKPLab/sentence-transformers/blob/master/docs/pretrained-models/nli-models.md#bert-models)).

### Deployment
1. Clone repository with `git clone git@github.com:YevheniiSemendiak/text_matcher.git`;
2. Deploy TextMatcher with `docker-compose up --build`;

### Usage
1. [Simple CLI tool](./back/simple_cli.py).
    - Being in *text_matcher/back* folder hit `python3 simple_cli.py`.
    - Requires `pika` and `pymongo` Python3 modules installed.

2. Web GUI:
    - Build using Vue.js & Vuetify.js frameworks.
    - Add, read texts and compare sentences.

### Questions or Suggestions?
Contact me at [TG](https://t.me/semendiak) or [:email:](mailto:semendyak@mail.com).
