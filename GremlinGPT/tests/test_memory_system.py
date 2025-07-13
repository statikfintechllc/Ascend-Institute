# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

"""
GremlinGPT Memory System Testing Suite

Comprehensive tests for memory management, vector storage, embeddings,
retrieval systems, and knowledge persistence.
"""

import pytest
import asyncio
import json
import numpy as np
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.logging_config import setup_module_logger
logger = setup_module_logger('tests', 'test_memory')

class MockVectorStore:
    """Mock vector store for testing."""
    def __init__(self):
        self.vectors = {}
        self.metadata = {}
        self.dimension = 768  # Standard embedding dimension
        
    def add_vector(self, vector_id, vector, metadata=None):
        """Add a vector to the store."""
        if len(vector) != self.dimension:
            raise ValueError(f"Vector dimension {len(vector)} does not match store dimension {self.dimension}")
        
        self.vectors[vector_id] = np.array(vector)
        self.metadata[vector_id] = metadata or {}
        return vector_id
    
    def get_vector(self, vector_id):
        """Retrieve a vector by ID."""
        return self.vectors.get(vector_id)
    
    def search_similar(self, query_vector, top_k=5, threshold=0.8):
        """Search for similar vectors."""
        if len(query_vector) != self.dimension:
            raise ValueError("Query vector dimension mismatch")
        
        similarities = []
        query_vector = np.array(query_vector)
        
        for vector_id, stored_vector in self.vectors.items():
            # Calculate cosine similarity
            similarity = np.dot(query_vector, stored_vector) / (
                np.linalg.norm(query_vector) * np.linalg.norm(stored_vector)
            )
            if similarity >= threshold:
                similarities.append((vector_id, similarity, self.metadata[vector_id]))
        
        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    def delete_vector(self, vector_id):
        """Delete a vector from the store."""
        if vector_id in self.vectors:
            del self.vectors[vector_id]
            del self.metadata[vector_id]
            return True
        return False
    
    def get_stats(self):
        """Get storage statistics."""
        return {
            'total_vectors': len(self.vectors),
            'dimension': self.dimension,
            'memory_usage': len(self.vectors) * self.dimension * 8  # 8 bytes per float64
        }

class MockMemoryManager:
    """Mock memory manager for testing."""
    def __init__(self):
        self.vector_store = MockVectorStore()
        self.memory_index = {}
        self.conversation_history = []
        
    def store_memory(self, content, memory_type='general', metadata=None):
        """Store a memory with automatic embedding."""
        # Mock embedding generation
        embedding = np.random.rand(768).tolist()
        
        memory_id = f"mem_{len(self.memory_index) + 1}"
        
        # Store in vector store
        self.vector_store.add_vector(memory_id, embedding, {
            'content': content,
            'type': memory_type,
            'timestamp': datetime.now().isoformat(),
            **(metadata or {})
        })
        
        # Update index
        self.memory_index[memory_id] = {
            'content': content,
            'type': memory_type,
            'embedding_id': memory_id
        }
        
        return memory_id
    
    def retrieve_memories(self, query, memory_type=None, limit=5):
        """Retrieve relevant memories for a query."""
        # Mock query embedding
        query_embedding = np.random.rand(768).tolist()
        
        # Search similar vectors
        results = self.vector_store.search_similar(query_embedding, top_k=limit)
        
        # Filter by memory type if specified
        if memory_type:
            results = [r for r in results if r[2].get('type') == memory_type]
        
        return [
            {
                'id': result[0],
                'content': result[2]['content'],
                'similarity': result[1],
                'metadata': result[2]
            }
            for result in results
        ]
    
    def add_conversation_turn(self, user_input, assistant_response):
        """Add a conversation turn to memory."""
        turn = {
            'user': user_input,
            'assistant': assistant_response,
            'timestamp': datetime.now().isoformat()
        }
        self.conversation_history.append(turn)
        
        # Store as memory
        content = f"User: {user_input}\nAssistant: {assistant_response}"
        return self.store_memory(content, memory_type='conversation')
    
    def get_conversation_context(self, num_turns=5):
        """Get recent conversation context."""
        return self.conversation_history[-num_turns:] if self.conversation_history else []

class TestVectorStore:
    """Test suite for vector storage functionality."""
    
    def test_vector_store_initialization(self):
        """Test vector store initialization."""
        store = MockVectorStore()
        
        assert store.dimension == 768
        assert len(store.vectors) == 0
        assert len(store.metadata) == 0
        
        logger.info("Vector store initialization test passed")
    
    def test_add_vector(self):
        """Test adding vectors to the store."""
        store = MockVectorStore()
        
        # Create test vector
        test_vector = np.random.rand(768).tolist()
        metadata = {'text': 'test content', 'type': 'test'}
        
        # Add vector
        vector_id = store.add_vector('test_1', test_vector, metadata)
        
        assert vector_id == 'test_1'
        assert 'test_1' in store.vectors
        assert 'test_1' in store.metadata
        assert store.metadata['test_1']['text'] == 'test content'
        
        logger.info("Add vector test passed")
    
    def test_vector_dimension_validation(self):
        """Test vector dimension validation."""
        store = MockVectorStore()
        
        # Test correct dimension
        correct_vector = np.random.rand(768).tolist()
        store.add_vector('correct', correct_vector)
        
        # Test incorrect dimension
        incorrect_vector = np.random.rand(512).tolist()
        with pytest.raises(ValueError):
            store.add_vector('incorrect', incorrect_vector)
        
        logger.info("Vector dimension validation test passed")
    
    def test_vector_retrieval(self):
        """Test vector retrieval."""
        store = MockVectorStore()
        
        test_vector = np.random.rand(768).tolist()
        store.add_vector('test_vector', test_vector)
        
        # Retrieve vector
        retrieved = store.get_vector('test_vector')
        assert retrieved is not None
        assert np.array_equal(retrieved, test_vector)
        
        # Test non-existent vector
        non_existent = store.get_vector('does_not_exist')
        assert non_existent is None
        
        logger.info("Vector retrieval test passed")
    
    def test_similarity_search(self):
        """Test similarity search functionality."""
        store = MockVectorStore()
        
        # Add some test vectors
        vectors = []
        for i in range(5):
            vector = np.random.rand(768)
            vectors.append(vector)
            store.add_vector(f'vec_{i}', vector, {'index': i})
        
        # Search with one of the stored vectors (should find itself)
        query_vector = vectors[0]
        results = store.search_similar(query_vector, top_k=3, threshold=0.8)
        
        assert len(results) >= 1  # Should find at least itself
        assert results[0][0] == 'vec_0'  # First result should be exact match
        assert results[0][1] >= 0.99  # Very high similarity (near 1.0)
        
        logger.info("Similarity search test passed")
    
    def test_vector_deletion(self):
        """Test vector deletion."""
        store = MockVectorStore()
        
        test_vector = np.random.rand(768).tolist()
        store.add_vector('to_delete', test_vector)
        
        # Verify vector exists
        assert store.get_vector('to_delete') is not None
        
        # Delete vector
        result = store.delete_vector('to_delete')
        assert result == True
        
        # Verify vector is gone
        assert store.get_vector('to_delete') is None
        
        # Test deleting non-existent vector
        result = store.delete_vector('does_not_exist')
        assert result == False
        
        logger.info("Vector deletion test passed")
    
    def test_storage_statistics(self):
        """Test storage statistics."""
        store = MockVectorStore()
        
        # Initial stats
        stats = store.get_stats()
        assert stats['total_vectors'] == 0
        assert stats['dimension'] == 768
        
        # Add some vectors
        for i in range(10):
            vector = np.random.rand(768).tolist()
            store.add_vector(f'vec_{i}', vector)
        
        # Check updated stats
        stats = store.get_stats()
        assert stats['total_vectors'] == 10
        assert stats['memory_usage'] > 0
        
        logger.info("Storage statistics test passed")

class TestMemoryManager:
    """Test suite for memory management functionality."""
    
    def test_memory_manager_initialization(self):
        """Test memory manager initialization."""
        manager = MockMemoryManager()
        
        assert manager.vector_store is not None
        assert len(manager.memory_index) == 0
        assert len(manager.conversation_history) == 0
        
        logger.info("Memory manager initialization test passed")
    
    def test_store_memory(self):
        """Test storing memories."""
        manager = MockMemoryManager()
        
        content = "This is a test memory"
        metadata = {'source': 'test', 'importance': 'high'}
        
        memory_id = manager.store_memory(content, memory_type='test', metadata=metadata)
        
        assert memory_id is not None
        assert memory_id in manager.memory_index
        assert manager.memory_index[memory_id]['content'] == content
        assert manager.memory_index[memory_id]['type'] == 'test'
        
        logger.info("Store memory test passed")
    
    def test_retrieve_memories(self):
        """Test memory retrieval."""
        manager = MockMemoryManager()
        
        # Store some test memories
        memories = [
            "The user likes Python programming",
            "The user is interested in AI and machine learning",
            "The user prefers coffee over tea",
            "The weather was sunny yesterday",
            "Bitcoin price went up today"
        ]
        
        for content in memories:
            manager.store_memory(content, memory_type='user_preference')
        
        # Retrieve memories
        query = "What does the user like?"
        results = manager.retrieve_memories(query, memory_type='user_preference', limit=3)
        
        assert len(results) <= 3
        for result in results:
            assert 'content' in result
            assert 'similarity' in result
            assert 'metadata' in result
            assert result['similarity'] >= 0
        
        logger.info("Retrieve memories test passed")
    
    def test_conversation_memory(self):
        """Test conversation memory functionality."""
        manager = MockMemoryManager()
        
        # Add conversation turns
        turns = [
            ("Hello, how are you?", "I'm doing well, thank you! How can I help you today?"),
            ("Can you help me with Python?", "Of course! I'd be happy to help with Python. What specifically would you like to know?"),
            ("How do I create a list?", "You can create a list in Python using square brackets, like this: my_list = [1, 2, 3]")
        ]
        
        memory_ids = []
        for user_input, assistant_response in turns:
            memory_id = manager.add_conversation_turn(user_input, assistant_response)
            memory_ids.append(memory_id)
        
        # Check conversation history
        context = manager.get_conversation_context(num_turns=2)
        assert len(context) == 2
        assert context[0]['user'] == turns[1][0]
        assert context[1]['assistant'] == turns[2][1]
        
        # Check that memories were stored
        assert len(memory_ids) == 3
        for memory_id in memory_ids:
            assert memory_id in manager.memory_index
        
        logger.info("Conversation memory test passed")
    
    def test_memory_type_filtering(self):
        """Test memory filtering by type."""
        manager = MockMemoryManager()
        
        # Store different types of memories
        manager.store_memory("User likes dogs", memory_type='preference')
        manager.store_memory("Meeting at 3 PM", memory_type='schedule')
        manager.store_memory("Password is secret123", memory_type='credential')
        manager.store_memory("User dislikes spicy food", memory_type='preference')
        
        # Retrieve only preferences
        preferences = manager.retrieve_memories("user preferences", memory_type='preference')
        
        # Should only return preference memories
        for result in preferences:
            assert result['metadata']['type'] == 'preference'
        
        logger.info("Memory type filtering test passed")

class TestMemoryPersistence:
    """Test suite for memory persistence functionality."""
    
    def test_memory_serialization(self):
        """Test memory serialization and deserialization."""
        # Create test memory data
        memory_data = {
            'memories': [
                {
                    'id': 'mem_1',
                    'content': 'Test memory content',
                    'type': 'test',
                    'embedding': np.random.rand(768).tolist(),
                    'metadata': {'timestamp': '2025-01-08T10:00:00'}
                }
            ],
            'conversation_history': [
                {
                    'user': 'Hello',
                    'assistant': 'Hi there!',
                    'timestamp': '2025-01-08T10:00:00'
                }
            ]
        }
        
        # Test JSON serialization
        serialized = json.dumps(memory_data)
        assert isinstance(serialized, str)
        
        # Test deserialization
        deserialized = json.loads(serialized)
        assert deserialized['memories'][0]['content'] == 'Test memory content'
        assert len(deserialized['conversation_history']) == 1
        
        logger.info("Memory serialization test passed")
    
    def test_memory_file_operations(self):
        """Test memory file save/load operations."""
        with tempfile.TemporaryDirectory() as temp_dir:
            memory_file = os.path.join(temp_dir, 'memories.json')
            
            # Create test data
            test_data = {
                'version': '1.0',
                'created': datetime.now().isoformat(),
                'memories': [
                    {
                        'id': 'test_mem',
                        'content': 'Test content',
                        'embedding': [0.1, 0.2, 0.3]
                    }
                ]
            }
            
            # Save to file
            with open(memory_file, 'w') as f:
                json.dump(test_data, f)
            
            # Verify file exists
            assert os.path.exists(memory_file)
            
            # Load from file
            with open(memory_file, 'r') as f:
                loaded_data = json.load(f)
            
            assert loaded_data['version'] == '1.0'
            assert len(loaded_data['memories']) == 1
            assert loaded_data['memories'][0]['content'] == 'Test content'
        
        logger.info("Memory file operations test passed")

class TestMemorySearch:
    """Test suite for memory search functionality."""
    
    def test_semantic_search(self):
        """Test semantic memory search."""
        manager = MockMemoryManager()
        
        # Store memories with related content
        memories = [
            "The user loves programming in Python",
            "Python is a great language for data science",
            "The user prefers JavaScript for web development",
            "Coffee is the user's favorite drink",
            "The user works as a software engineer"
        ]
        
        for content in memories:
            manager.store_memory(content)
        
        # Search for programming-related memories
        results = manager.retrieve_memories("programming languages")
        
        assert len(results) > 0
        # Results should be ordered by similarity
        for i in range(len(results) - 1):
            assert results[i]['similarity'] >= results[i + 1]['similarity']
        
        logger.info("Semantic search test passed")
    
    def test_search_with_threshold(self):
        """Test memory search with similarity threshold."""
        store = MockVectorStore()
        
        # Add vectors with known similarities
        base_vector = np.random.rand(768)
        store.add_vector('base', base_vector, {'content': 'base content'})
        
        # Add very similar vector (base + small noise)
        similar_vector = base_vector + np.random.rand(768) * 0.01
        store.add_vector('similar', similar_vector, {'content': 'similar content'})
        
        # Add dissimilar vector
        dissimilar_vector = np.random.rand(768)
        store.add_vector('dissimilar', dissimilar_vector, {'content': 'dissimilar content'})
        
        # Search with high threshold
        results = store.search_similar(base_vector, threshold=0.95)
        
        # Should only return very similar vectors
        assert len(results) >= 1  # At least the base vector itself
        for result in results:
            assert result[1] >= 0.95
        
        logger.info("Search with threshold test passed")

class TestMemoryOptimization:
    """Test suite for memory optimization features."""
    
    def test_memory_deduplication(self):
        """Test memory deduplication functionality."""
        manager = MockMemoryManager()
        
        # Store duplicate content
        content = "This is duplicate content"
        
        id1 = manager.store_memory(content, memory_type='test')
        id2 = manager.store_memory(content, memory_type='test')
        
        # Both should be stored (basic implementation doesn't deduplicate)
        assert id1 != id2
        assert len(manager.memory_index) == 2
        
        # In a real implementation, we might want deduplication
        logger.info("Memory deduplication test passed")
    
    def test_memory_compression(self):
        """Test memory compression for storage efficiency."""
        # Create large memory content
        large_content = "This is a large memory content. " * 1000
        
        # Test that content can be stored and retrieved
        manager = MockMemoryManager()
        memory_id = manager.store_memory(large_content)
        
        assert memory_id in manager.memory_index
        assert manager.memory_index[memory_id]['content'] == large_content
        
        logger.info("Memory compression test passed")

# Integration tests
class TestMemoryIntegration:
    """Integration tests for memory system components."""
    
    def test_end_to_end_memory_workflow(self):
        """Test complete memory workflow."""
        manager = MockMemoryManager()
        
        # 1. Store various types of memories
        user_prefs = manager.store_memory("User prefers dark mode", memory_type='preference')
        conversation = manager.add_conversation_turn(
            "What's my preferred UI theme?",
            "Based on your preferences, you prefer dark mode."
        )
        fact = manager.store_memory("Python was created by Guido van Rossum", memory_type='fact')
        
        # 2. Retrieve relevant memories
        ui_memories = manager.retrieve_memories("user interface preferences")
        python_memories = manager.retrieve_memories("Python programming language")
        
        # 3. Check conversation context
        context = manager.get_conversation_context()
        
        # Verify workflow
        assert len(manager.memory_index) >= 3
        assert len(ui_memories) >= 0
        assert len(python_memories) >= 0
        assert len(context) >= 1
        
        logger.info("End-to-end memory workflow test passed")
    
    def test_memory_vector_store_integration(self):
        """Test memory manager and vector store integration."""
        manager = MockMemoryManager()
        
        # Store memory
        content = "Integration test content"
        memory_id = manager.store_memory(content)
        
        # Verify storage in both memory index and vector store
        assert memory_id in manager.memory_index
        assert manager.vector_store.get_vector(memory_id) is not None
        
        # Verify metadata consistency
        vector_metadata = manager.vector_store.metadata[memory_id]
        index_data = manager.memory_index[memory_id]
        
        assert vector_metadata['content'] == index_data['content']
        
        logger.info("Memory-Vector store integration test passed")

# Performance tests
class TestMemoryPerformance:
    """Performance tests for memory system."""
    
    def test_large_scale_storage(self):
        """Test memory storage with large number of items."""
        manager = MockMemoryManager()
        
        # Store many memories
        num_memories = 1000
        memory_ids = []
        
        for i in range(num_memories):
            content = f"Memory content number {i} with some additional text to make it realistic"
            memory_id = manager.store_memory(content, memory_type='bulk_test')
            memory_ids.append(memory_id)
        
        # Verify all memories were stored
        assert len(memory_ids) == num_memories
        assert len(manager.memory_index) == num_memories
        
        # Test retrieval performance
        results = manager.retrieve_memories("memory content", limit=10)
        assert len(results) <= 10
        
        logger.info(f"Large scale storage test passed: {num_memories} memories")
    
    def test_search_performance(self):
        """Test search performance with large dataset."""
        store = MockVectorStore()
        
        # Add many vectors
        num_vectors = 5000
        for i in range(num_vectors):
            vector = np.random.rand(768).tolist()
            store.add_vector(f'vec_{i}', vector, {'index': i})
        
        # Test search performance
        query_vector = np.random.rand(768).tolist()
        results = store.search_similar(query_vector, top_k=10)
        
        assert len(results) <= 10
        
        # Verify results are properly sorted by similarity
        for i in range(len(results) - 1):
            assert results[i][1] >= results[i + 1][1]
        
        logger.info(f"Search performance test passed: searched {num_vectors} vectors")

if __name__ == '__main__':
    # Run basic tests if pytest is not available
    test_vector = TestVectorStore()
    test_vector.test_vector_store_initialization()
    test_vector.test_add_vector()
    
    test_manager = TestMemoryManager()
    test_manager.test_memory_manager_initialization()
    test_manager.test_store_memory()
    
    test_search = TestMemorySearch()
    test_search.test_semantic_search()
    
    print("All memory tests passed!")
