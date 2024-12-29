import asyncio
import os
from tqdm.asyncio import tqdm as tqdm_async
from dataclasses import dataclass
import numpy as np
from lightrag.utils import logger
from ..base import BaseVectorStorage
from pinecone import Pinecone
import json

@dataclass
class PineconeVectorDBStorage(BaseVectorStorage):
    def __post_init__(self):
        # Initialize Pinecone client instance
        self.pinecone_client = Pinecone(
            api_key=os.environ.get("PINECONE_API_KEY")
        )

        self.namespace = os.environ.get("NAMESPACE")
        self.index_name = os.environ.get("INDEX_NAME", "default_index")

        # Check if index exists, else create it
        if self.index_name not in [index.name for index in self.pinecone_client.list_indexes()]:
            self.pinecone_client.create_index(
                name=self.index_name,
                dimension=self.embedding_func.embedding_dim,
            )
        
        # Access the index
        self._index = self.pinecone_client.Index(self.index_name)
        self._max_batch_size = self.global_config["embedding_batch_num"]

    def split_into_batches(self, data, max_size=4_000_000):
        current_batch = []
        current_size = 0
        batches = []

        for item in data:
            # Estimate size of the item using JSON encoding
            item_size = len(json.dumps(item).encode('utf-8'))
            if item_size > max_size:
                raise ValueError(f"Item size {item_size} exceeds maximum allowed batch size {max_size}.")
            
            if current_size + item_size > max_size:
                # Finalize the current batch
                if current_batch:
                    batches.append(current_batch)
                current_batch = []
                current_size = 0

            current_batch.append(item)
            current_size += item_size

        # Add the last batch if not empty
        if current_batch:
            batches.append(current_batch)

        return batches

    async def upsert(self, data: dict[str, dict]):
        logger.info(f"Inserting {len(data)} vectors to {self.namespace}")
        if not data:
            logger.warning("You inserted empty data to vector DB")
            return []

        # Prepare list data and calculate embeddings
        list_data = [
            {
                "id": k,
                "metadata": {k1: v1 for k1, v1 in v.items() if k1 in self.meta_fields},
                "values": None,  # To be filled after embedding generation
            }
            for k, v in data.items()
        ]
        contents = [v["content"] for v in data.values()]
        batches = self.split_into_batches(contents, max_size=4_000_000)

        async def wrapped_task(batch):
            result = await self.embedding_func(batch)
            return result

        embedding_tasks = [wrapped_task(batch) for batch in batches]
        embeddings_list = await asyncio.gather(*embedding_tasks)
        embeddings = np.concatenate(embeddings_list)

        for i, d in enumerate(list_data):
            d["values"] = embeddings[i].tolist()

        # Split data for Pinecone upsert
        pinecone_batches = self.split_into_batches(list_data, max_size=4_000_000)

        results = []
        for batch in pinecone_batches:
            results.append(self._index.upsert(vectors=batch, namespace=self.namespace))
        
        return results

    async def query(self, query, top_k=5):
        embedding = await self.embedding_func([query])
        results = self._index.query(
            vector=embedding.tolist(),
            top_k=top_k,
            namespace=self.namespace,
            include_metadata=True,
        )
        print(results)
        matches = results.get("matches", [])
        return [
            {
                "id": dp.get("id"),
                "distance": dp.get("score"),
                **(dp.get("metadata") or {}),  # Safely handle missing metadata
            }
            for dp in matches
        ]

# Setup Environment Variables for Pinecone
# os.environ["INDEX_NAME"] = "rag"
# os.environ["NAMESPACE"] = "LIGHTRAG"

# # Example usage
# PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
# pinecone = Pinecone(api_key=PINECONE_API_KEY)

# # Ensure index setup
# index = pinecone.Index(os.environ["INDEX_NAME"])