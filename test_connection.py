#!/usr/bin/env python3
"""
ChromaDB Render Deployment Test Script

This script tests the connection to your ChromaDB instance deployed on Render.
It creates a collection, adds documents, and performs a query to verify functionality.

Usage:
  python test_connection.py https://your-chromadb-instance.onrender.com
"""

import sys
import chromadb
from chromadb.utils import embedding_functions

def test_chromadb_connection(url):
    """Test connection to a ChromaDB instance."""
    print(f"Testing connection to ChromaDB at: {url}")
    
    try:
        # Initialize the client
        client = chromadb.HttpClient(host=url)
        
        # Check if connection works by getting the list of collections
        collections = client.list_collections()
        print(f"Connection successful! Found {len(collections)} existing collections.")
        
        # Create a test collection
        test_collection_name = "render_test_collection"
        
        # Delete the collection if it exists
        for collection in collections:
            if collection.name == test_collection_name:
                client.delete_collection(test_collection_name)
                print(f"Deleted existing test collection: {test_collection_name}")
        
        # Create a new test collection
        print(f"Creating test collection: {test_collection_name}")
        collection = client.create_collection(
            name=test_collection_name,
            embedding_function=embedding_functions.DefaultEmbeddingFunction()
        )
        
        # Add documents
        print("Adding documents to test collection...")
        collection.add(
            documents=[
                "ChromaDB is an open-source embedding database",
                "Render.com makes it easy to deploy services",
                "Vector databases are useful for semantic search"
            ],
            metadatas=[
                {"source": "docs", "category": "database"},
                {"source": "web", "category": "deployment"},
                {"source": "article", "category": "search"}
            ],
            ids=["doc1", "doc2", "doc3"]
        )
        
        # Query the collection
        print("Querying the test collection...")
        results = collection.query(
            query_texts=["How do I deploy a database?"],
            n_results=2
        )
        
        # Display results
        print("\nQuery Results:")
        if (results and 
            "documents" in results and results["documents"] and 
            "metadatas" in results and results["metadatas"] and 
            "distances" in results and results["distances"] and 
            len(results["documents"]) > 0 and 
            len(results["documents"][0]) > 0):
            
            for i, (doc, metadata, distance) in enumerate(
                zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0]
                )
            ):
                print(f"Result {i+1}:")
                print(f"  Document: {doc}")
                print(f"  Metadata: {metadata}")
                print(f"  Distance: {distance}")
                print("")
        else:
            print("No results found in the query response or results are in unexpected format.")
            print(f"Raw results: {results}")
        
        # Cleanup - delete the test collection
        client.delete_collection(test_collection_name)
        print(f"Test completed successfully and test collection '{test_collection_name}' deleted.")
        
        return True
    
    except Exception as e:
        print(f"Error connecting to ChromaDB: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_connection.py https://your-chromadb-instance.onrender.com")
        sys.exit(1)
    
    url = sys.argv[1]
    success = test_chromadb_connection(url)
    
    if success:
        print("\n✅ ChromaDB deployment is working correctly!")
    else:
        print("\n❌ Failed to connect to ChromaDB. Please check your deployment.")
        sys.exit(1)
