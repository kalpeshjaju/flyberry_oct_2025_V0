#!/usr/bin/env python3
"""
Query Flyberry Brand Package in ChromaDB using semantic search

PURPOSE: Search across all 58 documents using natural language queries
USAGE: python3 query-chromadb.py "your search query"
"""

import chromadb
from chromadb.config import Settings
import sys
from pathlib import Path

# Configuration
DB_PATH = "./chromadb"
COLLECTION_NAME = "flyberry_brand_package"

def format_result(result: dict, index: int):
    """Format a single search result for display"""
    metadata = result['metadatas'][0][index]
    document = result['documents'][0][index]
    distance = result['distances'][0][index]

    # Similarity score (1 - distance, assuming cosine distance)
    similarity = 1 - distance

    print(f"\n{'=' * 80}")
    print(f"Result #{index + 1} | Similarity: {similarity:.2%}")
    print(f"{'=' * 80}")
    print(f"📄 File: {metadata['source_file']}")
    print(f"📖 Title: {metadata['title']}")
    print(f"🎬 Act: {metadata['act']}")
    print(f"📍 Chunk: {metadata['chunk_index'] + 1} of {metadata['total_chunks']}")
    print(f"\n{'-' * 80}")
    print(f"Content Preview:")
    print(f"{'-' * 80}")

    # Show first 500 characters of chunk
    preview = document[:500] + "..." if len(document) > 500 else document
    print(preview)

def search(query: str, n_results: int = 5):
    """
    Search the Flyberry brand package

    Args:
        query: Natural language search query
        n_results: Number of results to return (default: 5)
    """
    print(f"\n🔍 Searching Flyberry Brand Package")
    print(f"Query: \"{query}\"")
    print(f"Returning top {n_results} results\n")

    # Initialize ChromaDB client
    try:
        client = chromadb.PersistentClient(path=DB_PATH)
        collection = client.get_collection(name=COLLECTION_NAME)
    except Exception as e:
        print(f"❌ Error loading database: {e}")
        print(f"\n💡 Make sure you've run: python3 ingest-to-chromadb.py")
        sys.exit(1)

    # Perform semantic search
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    # Display results
    if not results['documents'][0]:
        print("No results found.")
        return

    for i in range(len(results['documents'][0])):
        format_result(results, i)

    print(f"\n{'=' * 80}")
    print(f"✅ Found {len(results['documents'][0])} results")

def interactive_mode():
    """Run in interactive query mode"""
    print("\n🔍 Flyberry Brand Package - Interactive Search")
    print("=" * 60)
    print("Enter your queries below. Type 'exit' or 'quit' to stop.")
    print("=" * 60)

    while True:
        try:
            query = input("\n🔍 Query: ").strip()

            if query.lower() in ['exit', 'quit', 'q']:
                print("\nGoodbye!")
                break

            if not query:
                continue

            # Check for custom result count
            if query.startswith('/'):
                # Command mode
                if query.startswith('/n '):
                    parts = query[3:].split(' ', 1)
                    if len(parts) == 2 and parts[0].isdigit():
                        n_results = int(parts[0])
                        query = parts[1]
                        search(query, n_results)
                        continue

            search(query, n_results=5)

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def preset_queries():
    """Run preset consistency check queries"""
    print("\n🧪 Running Preset Consistency Check Queries")
    print("=" * 80)

    queries = [
        ("Fortune 500 clients", "Find all mentions of Fortune 500 clients and corporate partners"),
        ("Brand positioning", "What is the brand positioning and north star statement?"),
        ("Pricing tiers", "What are the pricing ranges and tier structure?"),
        ("Brand archetype", "What is the brand archetype and personality?"),
        ("Target audience", "Who is the target audience and customer persona?"),
        ("Differentiation", "How does Flyberry differentiate from competitors?"),
    ]

    for i, (name, query) in enumerate(queries, 1):
        print(f"\n{'#' * 80}")
        print(f"Query {i}/{len(queries)}: {name}")
        print(f"{'#' * 80}")
        search(query, n_results=3)
        print("\n")

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        # Command-line query mode
        if sys.argv[1] == '--preset':
            preset_queries()
        else:
            query = ' '.join(sys.argv[1:])
            search(query, n_results=5)
    else:
        # Interactive mode
        interactive_mode()

if __name__ == "__main__":
    main()
