import secrets
import pickle
import logging
import datetime
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
        sentences_ids = [secrets.token_hex(12) for _ in range(len(sentences))]
        text_id = secrets.token_hex(12)
        self.logger.info(f"Processing text {request['text'][:10]}... ({len(sentences_ids)} sentences) ID: {text_id}")
        self.dbdao.write_one_record(
            collection_name="Text",
            record={
                "_id": text_id,
                "sentencesUUID": sentences_ids,
                "text": request["text"],
                "title": request.get("title"),
                "dateAdded": datetime.datetime.now().isoformat()
                }
            )

        embeddings = self.model.get_embeddings(sentences)

        sentence_records = []
        for sentence, s_uuid, embedding in zip(sentences, sentences_ids, embeddings):
            sentence_records.append({
                "sentence": sentence,
                "embedding": pickle.dumps(embedding, protocol=pickle.HIGHEST_PROTOCOL),
                "_id": s_uuid,
                "textUUID": text_id
            })
        
        self.dbdao.write_many_records("Sentence", sentence_records)
        self.logger.info(f"Text {text_id} processed successfully.")
        self.state = IDLE
        return text_id
    
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
                "_id": t_sentences[sort_idx]["_id"],
                "textUUID": t_sentences[sort_idx]["textUUID"],
                "sentence": t_sentences[sort_idx]["sentence"]
            })
        return distances
