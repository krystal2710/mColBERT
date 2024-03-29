import os
import sys
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.getenv('COLBERT_PATH'))
from colbert.infra.run import Run
from colbert.infra.config import ColBERTConfig, RunConfig
from colbert import Trainer


def train():
    # use 4 gpus (e.g. four A100s, but you can use fewer by changing nway,accumsteps,bsize).
    with Run().context(RunConfig(nranks=1)):
        triples = os.getenv("TRAINING_TRIPLES_PATH") # `wget https://huggingface.co/colbert-ir/colbertv2.0_msmarco_64way/resolve/main/examples.json?download=true` (26GB)
        queries = os.getenv("TRAINING_QUERIES_PATH")
        collection = os.getenv("TRAINING_CONTEXTS_PATH")

        config = ColBERTConfig(bsize=8, lr=1e-05, warmup=20_000, doc_maxlen=180, dim=128, attend_to_mask_tokens=False, nway=2, accumsteps=1, similarity='cosine', use_ib_negatives=True)
        trainer = Trainer(triples=triples, queries=queries, collection=collection, config=config)

        trainer.train(checkpoint='FacebookAI/xlm-roberta-base')  # or start from scratch, like `bert-base-uncased`


if __name__ == '__main__':
    train()