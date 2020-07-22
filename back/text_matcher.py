import uuid
import pickle
import logging
from typing import List, Mapping

import scipy
import numpy as np
import nltk

from utils import MongoDBDAO
from model_wrappers import AEmbeddingModel, SBERTEmbedding

BUSY = 0
IDLE = 1


class TextMatcher:

    def __init__(self, db_dao: MongoDBDAO):
        self.dbdao = db_dao

        self.model: AEmbeddingModel = SBERTEmbedding("bert-base-nli-mean-tokens")
        self.state = IDLE
        self.logger = logging.getLogger(__name__)

    def process_new_text(self, request: Mapping) -> str:

        if self.state != IDLE:
            raise RuntimeError(f"TextMatcher is not IDLE: {self.state}")
        else:
            self.state = BUSY
        sentences = nltk.sent_tokenize(text=request["text"], language="english")
        sentences_uuids = [uuid.uuid4().hex for _ in range(len(sentences))]
        text_uuid = uuid.uuid4().hex
        self.logger.info(f"Processing text {request['text'][:10]}... ({len(sentences_uuids)} sentences) ID: {text_uuid}")
        self.dbdao.write_one_record(
            collection_name="Text",
            record={
                "_id": text_uuid,
                "sentencesUUID": sentences_uuids,
                "text": request["text"],
                "title": request.get("title")
                }
            )

        embeddings = self.model.get_embeddings(sentences)

        sentence_records = []
        for sentence, s_uuid, embedding in zip(sentences, sentences_uuids, embeddings):
            sentence_records.append({
                "sentence": sentence,
                "embedding": pickle.dumps(embedding, protocol=pickle.HIGHEST_PROTOCOL),
                "_id": s_uuid,
                "textUUID": text_uuid
            })
        
        self.dbdao.write_many_records("Sentence", sentence_records)
        self.logger.info(f"Text {text_uuid} processed successfully.")
        self.state = IDLE
        return text_uuid
    
    def get_sorted_distances(self, sentence_uuid: str, ascending: bool = True, metric="cosine") -> List[Mapping]:

        s_sentence = self.dbdao.get_last_record("Sentence", filter_={"_id": sentence_uuid}, projection=["embedding"])
        if not s_sentence:
            raise ValueError(f"Sentence with UUID {sentence_uuid} does not exist!")

        t_sentences = self.dbdao.get_records("Sentence", filter_=None, projection=None)
        t_sentences_embs = [pickle.loads(t_sentence["embedding"]) for t_sentence in t_sentences]

        self.logger.info(f"Comparing {len(t_sentences)} sentences by similarity for SentenceUUID {sentence_uuid}.")
        dists = scipy.spatial.distance.cdist([pickle.loads(s_sentence["embedding"])], t_sentences_embs, metric=metric)[0]

        if not ascending:
            dists *= -1
        
        sort_idxs = np.argsort(dists)

        distances = []
        for sort_idx in sort_idxs:
            distances.append({
                "distance": dists[sort_idx],
                "metric": metric,
                "_id": t_sentences[sort_idx]["_id"]
            })
        return distances
