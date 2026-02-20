#!/usr/bin/env python3
"""
Memory Store - Platinum Tier
Long-term memory using ChromaDB for RAG
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import hashlib

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    print("Warning: ChromaDB not installed. Install with: pip install chromadb")

class MemoryStore:
    """
    Long-term memory system using vector database.

    Features:
    - Conversation history storage
    - Semantic search
    - RAG (Retrieval Augmented Generation)
    - Persistent storage
    """

    def __init__(self, base_dir="Platinum_Tier"):
        self.base_dir = Path(base_dir)
        self.memory_dir = self.base_dir / "Memory"
        self.memory_dir.mkdir(parents=True, exist_ok=True)

        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('MemoryStore')

        # Initialize ChromaDB (if available)
        self.chroma_available = CHROMADB_AVAILABLE
        if self.chroma_available:
            self._initialize_chromadb()
        else:
            self.logger.warning("ChromaDB not available - using fallback JSON storage")
            self.fallback_storage = self.memory_dir / "conversations.json"
            self._initialize_fallback()

    def _initialize_chromadb(self):
        """Initialize ChromaDB client"""
        try:
            self.client = chromadb.PersistentClient(
                path=str(self.memory_dir / "chroma_db")
            )

            # Create or get collection
            self.collection = self.client.get_or_create_collection(
                name="conversations",
                metadata={"description": "AI Employee conversation history"}
            )

            self.logger.info("ChromaDB initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize ChromaDB: {e}")
            self.chroma_available = False
            self._initialize_fallback()

    def _initialize_fallback(self):
        """Initialize fallback JSON storage"""
        if not self.fallback_storage.exists():
            self.fallback_storage.write_text(json.dumps([], indent=2))

    def store_conversation(self, content: str, metadata: Dict) -> str:
        """
        Store a conversation in memory.

        Args:
            content: The conversation content
            metadata: Additional metadata (source, timestamp, etc.)

        Returns:
            conversation_id
        """
        # Generate ID
        conversation_id = hashlib.md5(
            f"{content}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]

        # Add timestamp
        metadata['timestamp'] = datetime.now().isoformat()
        metadata['conversation_id'] = conversation_id

        if self.chroma_available:
            # Store in ChromaDB
            try:
                self.collection.add(
                    documents=[content],
                    metadatas=[metadata],
                    ids=[conversation_id]
                )
                self.logger.info(f"Stored conversation: {conversation_id}")
            except Exception as e:
                self.logger.error(f"Failed to store in ChromaDB: {e}")
                self._store_fallback(conversation_id, content, metadata)
        else:
            # Store in fallback
            self._store_fallback(conversation_id, content, metadata)

        return conversation_id

    def _store_fallback(self, conversation_id: str, content: str, metadata: Dict):
        """Store in fallback JSON storage"""
        try:
            conversations = json.loads(self.fallback_storage.read_text())
            conversations.append({
                'id': conversation_id,
                'content': content,
                'metadata': metadata
            })
            self.fallback_storage.write_text(json.dumps(conversations, indent=2))
            self.logger.info(f"Stored in fallback: {conversation_id}")
        except Exception as e:
            self.logger.error(f"Failed to store in fallback: {e}")

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search conversations using semantic similarity.

        Args:
            query: Search query
            top_k: Number of results to return

        Returns:
            List of matching conversations
        """
        if self.chroma_available:
            try:
                results = self.collection.query(
                    query_texts=[query],
                    n_results=top_k
                )

                # Format results
                matches = []
                if results['documents'] and results['documents'][0]:
                    for i, doc in enumerate(results['documents'][0]):
                        matches.append({
                            'content': doc,
                            'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                            'distance': results['distances'][0][i] if results['distances'] else None
                        })

                self.logger.info(f"Found {len(matches)} matches for query: {query[:50]}...")
                return matches
            except Exception as e:
                self.logger.error(f"Search failed: {e}")
                return self._search_fallback(query, top_k)
        else:
            return self._search_fallback(query, top_k)

    def _search_fallback(self, query: str, top_k: int) -> List[Dict]:
        """Fallback search using simple text matching"""
        try:
            conversations = json.loads(self.fallback_storage.read_text())

            # Simple keyword matching
            query_lower = query.lower()
            matches = []

            for conv in conversations:
                if query_lower in conv['content'].lower():
                    matches.append({
                        'content': conv['content'],
                        'metadata': conv['metadata'],
                        'distance': None
                    })

            # Return top_k results
            return matches[:top_k]
        except Exception as e:
            self.logger.error(f"Fallback search failed: {e}")
            return []

    def get_recent_conversations(self, limit: int = 10) -> List[Dict]:
        """Get most recent conversations"""
        if self.chroma_available:
            try:
                # Get all and sort by timestamp
                results = self.collection.get()

                conversations = []
                if results['documents']:
                    for i, doc in enumerate(results['documents']):
                        conversations.append({
                            'content': doc,
                            'metadata': results['metadatas'][i] if results['metadatas'] else {}
                        })

                # Sort by timestamp
                conversations.sort(
                    key=lambda x: x['metadata'].get('timestamp', ''),
                    reverse=True
                )

                return conversations[:limit]
            except Exception as e:
                self.logger.error(f"Failed to get recent conversations: {e}")
                return []
        else:
            try:
                conversations = json.loads(self.fallback_storage.read_text())
                conversations.sort(
                    key=lambda x: x['metadata'].get('timestamp', ''),
                    reverse=True
                )
                return conversations[:limit]
            except Exception as e:
                self.logger.error(f"Failed to get recent conversations: {e}")
                return []

    def get_stats(self) -> Dict:
        """Get memory statistics"""
        if self.chroma_available:
            try:
                count = self.collection.count()
                return {
                    'total_conversations': count,
                    'storage_type': 'chromadb',
                    'storage_path': str(self.memory_dir / "chroma_db")
                }
            except Exception as e:
                self.logger.error(f"Failed to get stats: {e}")
                return {'error': str(e)}
        else:
            try:
                conversations = json.loads(self.fallback_storage.read_text())
                return {
                    'total_conversations': len(conversations),
                    'storage_type': 'json_fallback',
                    'storage_path': str(self.fallback_storage)
                }
            except Exception as e:
                return {'error': str(e)}

    def run_demo(self):
        """Run a demo of the memory system"""
        self.logger.info("=== Memory Store Demo ===")

        # Store some conversations
        conversations = [
            ("Discussed AI employee architecture with user",
             {"source": "chat", "topic": "architecture"}),
            ("Reviewed Gold Tier implementation plan",
             {"source": "planning", "topic": "gold_tier"}),
            ("Analyzed watcher performance metrics",
             {"source": "monitoring", "topic": "performance"}),
        ]

        for content, metadata in conversations:
            conv_id = self.store_conversation(content, metadata)
            self.logger.info(f"Stored: {conv_id}")

        # Search
        results = self.search("architecture", top_k=2)
        self.logger.info(f"Search results: {len(results)}")

        # Get stats
        stats = self.get_stats()
        self.logger.info(f"Stats: {stats}")

def main():
    """Main entry point"""
    memory = MemoryStore()

    print("=" * 70)
    print("Memory Store - Platinum Tier")
    print("=" * 70)
    print()

    # Run demo
    memory.run_demo()

    print()
    print("=" * 70)
    print("Memory system operational")
    print("=" * 70)

if __name__ == "__main__":
    main()
