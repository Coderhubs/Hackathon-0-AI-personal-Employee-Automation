#!/usr/bin/env python3
"""
Vector Store - Platinum Tier
Long-term memory using Pinecone or ChromaDB
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import logging

# Try Pinecone first, fall back to ChromaDB
try:
    import pinecone
    PINECONE_AVAILABLE = True
except ImportError:
    PINECONE_AVAILABLE = False

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

from sentence_transformers import SentenceTransformer

class VectorStore:
    """
    Vector Store for long-term memory.

    Supports:
    - Pinecone (cloud-based)
    - ChromaDB (local/self-hosted)

    Features:
    - Store conversations
    - Semantic search
    - Context retrieval
    - Memory persistence
    """

    def __init__(self, provider="chromadb", base_dir="Platinum_Tier"):
        self.base_dir = Path(base_dir)
        self.memory_dir = self.base_dir / "Memory" / "data"
        self.memory_dir.mkdir(parents=True, exist_ok=True)

        self.provider = provider
        self.client = None
        self.collection = None

        # Embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

        self.setup_logging()
        self.initialize_store()

    def setup_logging(self):
        """Setup logging"""
        log_file = self.base_dir / "Logs" / f"vector_store_{datetime.now().strftime('%Y%m%d')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('VectorStore')

    def initialize_store(self):
        """Initialize vector store based on provider"""
        try:
            if self.provider == "pinecone" and PINECONE_AVAILABLE:
                self._initialize_pinecone()
            elif self.provider == "chromadb" and CHROMADB_AVAILABLE:
                self._initialize_chromadb()
            else:
                self.logger.error(f"Provider {self.provider} not available")
                raise Exception(f"Vector store provider {self.provider} not available")

        except Exception as e:
            self.logger.error(f"Error initializing vector store: {e}")
            raise

    def _initialize_pinecone(self):
        """Initialize Pinecone"""
        try:
            api_key = os.getenv('PINECONE_API_KEY')
            environment = os.getenv('PINECONE_ENVIRONMENT', 'us-west1-gcp')

            if not api_key:
                raise Exception("PINECONE_API_KEY not set")

            pinecone.init(api_key=api_key, environment=environment)

            index_name = "platinum-ai-memory"

            # Create index if doesn't exist
            if index_name not in pinecone.list_indexes():
                pinecone.create_index(
                    name=index_name,
                    dimension=384,  # all-MiniLM-L6-v2 dimension
                    metric="cosine"
                )
                self.logger.info(f"Created Pinecone index: {index_name}")

            self.client = pinecone.Index(index_name)
            self.logger.info("Pinecone initialized successfully")

        except Exception as e:
            self.logger.error(f"Error initializing Pinecone: {e}")
            raise

    def _initialize_chromadb(self):
        """Initialize ChromaDB"""
        try:
            # Use persistent storage
            self.client = chromadb.PersistentClient(
                path=str(self.memory_dir),
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )

            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name="conversations",
                metadata={"description": "Long-term conversation memory"}
            )

            self.logger.info("ChromaDB initialized successfully")

        except Exception as e:
            self.logger.error(f"Error initializing ChromaDB: {e}")
            raise

    def add_conversation(self, conversation_id: str, text: str, metadata: Dict = None) -> bool:
        """
        Add conversation to vector store.

        Args:
            conversation_id: Unique conversation ID
            text: Conversation text
            metadata: Additional metadata

        Returns:
            True if successful
        """
        try:
            # Generate embedding
            embedding = self.embedding_model.encode(text).tolist()

            # Prepare metadata
            if metadata is None:
                metadata = {}

            metadata.update({
                'conversation_id': conversation_id,
                'timestamp': datetime.now().isoformat(),
                'text_length': len(text)
            })

            if self.provider == "pinecone":
                # Upsert to Pinecone
                self.client.upsert(
                    vectors=[(conversation_id, embedding, metadata)]
                )
            elif self.provider == "chromadb":
                # Add to ChromaDB
                self.collection.add(
                    ids=[conversation_id],
                    embeddings=[embedding],
                    documents=[text],
                    metadatas=[metadata]
                )

            self.logger.info(f"Added conversation: {conversation_id}")
            return True

        except Exception as e:
            self.logger.error(f"Error adding conversation: {e}")
            return False

    def search_similar(self, query: str, top_k: int = 5, filter_dict: Dict = None) -> List[Dict]:
        """
        Search for similar conversations.

        Args:
            query: Search query
            top_k: Number of results to return
            filter_dict: Optional metadata filters

        Returns:
            List of similar conversations with scores
        """
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query).tolist()

            results = []

            if self.provider == "pinecone":
                # Query Pinecone
                response = self.client.query(
                    vector=query_embedding,
                    top_k=top_k,
                    include_metadata=True,
                    filter=filter_dict
                )

                for match in response['matches']:
                    results.append({
                        'id': match['id'],
                        'score': match['score'],
                        'metadata': match.get('metadata', {})
                    })

            elif self.provider == "chromadb":
                # Query ChromaDB
                response = self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k,
                    where=filter_dict
                )

                for i, doc_id in enumerate(response['ids'][0]):
                    results.append({
                        'id': doc_id,
                        'score': response['distances'][0][i],
                        'text': response['documents'][0][i],
                        'metadata': response['metadatas'][0][i]
                    })

            self.logger.info(f"Found {len(results)} similar conversations")
            return results

        except Exception as e:
            self.logger.error(f"Error searching: {e}")
            return []

    def get_conversation_history(self, conversation_id: str) -> Optional[Dict]:
        """
        Get specific conversation by ID.

        Args:
            conversation_id: Conversation ID

        Returns:
            Conversation dict or None
        """
        try:
            if self.provider == "pinecone":
                response = self.client.fetch(ids=[conversation_id])
                if conversation_id in response['vectors']:
                    return response['vectors'][conversation_id]

            elif self.provider == "chromadb":
                response = self.collection.get(
                    ids=[conversation_id],
                    include=['documents', 'metadatas']
                )

                if response['ids']:
                    return {
                        'id': response['ids'][0],
                        'text': response['documents'][0],
                        'metadata': response['metadatas'][0]
                    }

            return None

        except Exception as e:
            self.logger.error(f"Error getting conversation: {e}")
            return None

    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete conversation from vector store"""
        try:
            if self.provider == "pinecone":
                self.client.delete(ids=[conversation_id])
            elif self.provider == "chromadb":
                self.collection.delete(ids=[conversation_id])

            self.logger.info(f"Deleted conversation: {conversation_id}")
            return True

        except Exception as e:
            self.logger.error(f"Error deleting conversation: {e}")
            return False

    def get_stats(self) -> Dict:
        """Get vector store statistics"""
        try:
            stats = {}

            if self.provider == "pinecone":
                index_stats = self.client.describe_index_stats()
                stats = {
                    'total_vectors': index_stats['total_vector_count'],
                    'dimension': index_stats['dimension']
                }
            elif self.provider == "chromadb":
                count = self.collection.count()
                stats = {
                    'total_vectors': count,
                    'dimension': 384
                }

            return stats

        except Exception as e:
            self.logger.error(f"Error getting stats: {e}")
            return {}

if __name__ == "__main__":
    # Test vector store
    store = VectorStore(provider="chromadb")

    # Add test conversation
    store.add_conversation(
        conversation_id="test_001",
        text="Hello, I need to schedule an appointment for next week.",
        metadata={'type': 'appointment', 'status': 'pending'}
    )

    # Search
    results = store.search_similar("appointment scheduling", top_k=3)
    print(f"Found {len(results)} results")

    # Get stats
    stats = store.get_stats()
    print(f"Stats: {stats}")
