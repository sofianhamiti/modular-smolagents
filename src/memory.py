"""
Memory module for storing and retrieving conversation history.
"""

from mem0 import Memory

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
