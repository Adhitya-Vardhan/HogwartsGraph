import os
import json
from dotenv import load_dotenv
from lightrag import LightRAG, QueryParam
from lightrag.utils import EmbeddingFunc
from pinecone import Pinecone
from lightrag.llm import google_gemini_complete, google_embedding

# Load environment variables from a .env file
load_dotenv()

def clean_text(text: str) -> str:
    """Clean text to ensure it's suitable for embedding."""
    text = ' '.join(text.split())  # Remove excessive whitespace
    return text[:3000] if len(text) > 3000 else text  # Truncate if too long


def split_into_batches(data, max_size):
    """Split data into smaller batches ensuring each batch stays below the max_size."""
    current_batch, current_size, batches = [], 0, []

    for item in data:
        item = clean_text(item)
        item_size = len(json.dumps(item).encode('utf-8'))

        if item_size > max_size:
            sub_items = [item[i:i + max_size // 2] for i in range(0, len(item), max_size // 2)]
            for sub_item in sub_items:
                if len(json.dumps(sub_item).encode('utf-8')) > max_size:
                    raise ValueError(f"Sub-item exceeds max size: {len(sub_item)} bytes.")
                batches.append([sub_item])
            continue

        if current_size + item_size > max_size:
            batches.append(current_batch)
            current_batch, current_size = [], 0

        current_batch.append(item)
        current_size += item_size

    if current_batch:
        batches.append(current_batch)

    return batches


def setup_working_dir():
    """Setup and ensure the working directory exists."""
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    WORKING_DIR = os.path.join(ROOT_DIR, "myKG")
    os.makedirs(WORKING_DIR, exist_ok=True)
    return ROOT_DIR, WORKING_DIR


def initialize_pinecone():
    """Initialize Pinecone client and return the index."""
    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("INDEX_NAME")
    pinecone = Pinecone(api_key=api_key)
    return pinecone.Index(index_name)


def initialize_rag(working_dir):
    """Initialize LightRAG instance."""
    return LightRAG(
        working_dir=working_dir,
        llm_model_func=google_gemini_complete,
        embedding_func=EmbeddingFunc(
            embedding_dim=768,
            max_token_size=3072,
            func=lambda texts: google_embedding(text=texts),
        ),
        kv_storage="MongoKVStorage",
        graph_storage="Neo4JStorage",
        vector_storage="PineconeVectorDBStorage",
    )


def process_books_folder(rag):
    """Process text files in the books folder if it exists."""
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    BOOKS_FOLDER = os.path.join(ROOT_DIR, "book")
    MAX_PAYLOAD_SIZE = 4_000_000

    if not os.path.exists(BOOKS_FOLDER):
        print("Books folder does not exist.")
        return

    for filename in os.listdir(BOOKS_FOLDER):
        file_path = os.path.join(BOOKS_FOLDER, filename)
        if filename.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                print(f"Processing {filename}...")

                chunks = split_into_batches(content.split("\n"), max_size=MAX_PAYLOAD_SIZE)
                for i, chunk in enumerate(chunks):
                    try:
                        rag.insert("\n".join(chunk))
                        print(f"Chunk {i + 1} of {filename} inserted successfully.")
                    except Exception as e:
                        print(f"Failed to insert chunk {i + 1}: {e}")
                        break
                else:
                    os.remove(file_path)
                    print(f"{filename} processed and deleted.")


if __name__ == "__main__":
    ROOT_DIR, WORKING_DIR = setup_working_dir()
    pinecone_index = initialize_pinecone()
    rag = initialize_rag(WORKING_DIR)

    # Uncomment the next line to process books folder
    # process_books_folder(rag)

    # Query RAG with a sample question
    query_result = rag.query(
        "What are the diagnostic implications of matching +16.19% deviations in supply frequency and shaft speed sideband frequencies, combined with extreme current waveform asymmetry?",
        param=QueryParam(mode="hybrid"),
    )
    print(query_result)
