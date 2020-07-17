import abc
from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer


class AEmbeddingModel(abc.ABC):

    @abc.abstractmethod
    def get_embeddings(self, sentences: List[str]) -> List[np.ndarray]: pass

    @abc.abstractmethod
    def get_name(self) -> str: pass


class SBERTEmbedding(AEmbeddingModel):
    def __init__(self, model_path: str):
        self.model = SentenceTransformer(model_path)
        self.name = "SBERT"
    
    def get_embeddings(self, sentences: List[str]) -> List[np.ndarray]:
        return self.model.encode(sentences, show_progress_bar=False)

    def get_name(self) -> str:
        return self.name
