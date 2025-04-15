"""
Memory module for storing and retrieving conversation history.
"""

from mem0 import Memory

class MemoryProvider:
    """
    Provider class for memory functionality.
    Handles creation and access to memory instances.
    """
    
    @staticmethod
    def create_memory():
        """
        Create a memory instance.
        
        Returns:
            Memory instance
        """
        return Memory()
    
    @staticmethod
    def search(memory_instance, query, user_id="default_user", limit=3):
        """
        Retrieve relevant memories for a given query and user.
        
        Args:
            memory_instance: Memory instance to search
            query: Search query string
            user_id: User identifier
            limit: Maximum number of results to return
            
        Returns:
            List of memory dicts
        """
        return memory_instance.search(query=query, user_id=user_id, limit=limit)["results"]
    
    @staticmethod
    def add(memory_instance, messages, user_id="default_user"):
        """
        Add a list of messages to memory for a user.
        
        Args:
            memory_instance: Memory instance to add to
            messages: List of message dicts with 'role' and 'content'
            user_id: User identifier
            
        Returns:
            Result of the add operation
        """
        return memory_instance.add(messages, user_id=user_id)

# Singleton memory instance
memory = Memory()

def memory_search(query, user_id="default_user", limit=3):
    """
    Retrieve relevant memories for a given query and user.
    Returns a list of memory dicts.
    """
    return memory.search(query=query, user_id=user_id, limit=limit)["results"]

def memory_add(messages, user_id="default_user"):
    """
    Add a list of messages (dicts with 'role' and 'content') to memory for a user.
    """
    return memory.add(messages, user_id=user_id)
