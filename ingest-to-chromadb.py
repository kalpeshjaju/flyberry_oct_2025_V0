#!/usr/bin/env python3
"""
Ingest Flyberry Brand Package HTML files into ChromaDB for semantic search

PURPOSE: Enable semantic search across all 58 documents in the Flyberry package
USAGE: python3 ingest-to-chromadb.py
"""

import chromadb
from chromadb.config import Settings
from bs4 import BeautifulSoup
from pathlib import Path
import re
import sys

# Configuration
CHUNK_SIZE = 2000  # characters per chunk
CHUNK_OVERLAP = 200  # overlap between chunks
DB_PATH = "./chromadb"
COLLECTION_NAME = "flyberry_brand_package"

def clean_text(text: str) -> str:
    """Clean extracted text from HTML"""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove empty lines
    text = re.sub(r'\n\s*\n', '\n', text)
    return text.strip()

def extract_text_from_html(html_path: Path) -> dict:
    """
    Extract text content from HTML file

    Returns:
        dict with 'title', 'act', 'content', 'metadata'
    """
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Extract title
    title_tag = soup.find('title')
    title = title_tag.get_text() if title_tag else html_path.stem

    # Extract Act number from title or filename
    act_match = re.search(r'Act (\d+)', title, re.IGNORECASE)
    if not act_match:
        act_match = re.search(r'act-(\d+)', html_path.stem)
    act = f"Act {act_match.group(1)}" if act_match else "Unknown"

    # Remove script, style, nav elements
    for tag in soup(['script', 'style', 'nav', 'header', 'footer']):
        tag.decompose()

    # Extract main content
    main_content = soup.find('main') or soup.find('body') or soup
    text = main_content.get_text(separator='\n')
    text = clean_text(text)

    return {
        'title': title,
        'act': act,
        'content': text,
        'metadata': {
            'source_file': html_path.name,
            'file_path': str(html_path)
        }
    }

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """
    Split text into overlapping chunks

    WHY: Large documents need chunking for effective semantic search
    HOW: Create chunks with overlap to preserve context at boundaries
    """
    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = start + chunk_size
        chunk = text[start:end]

        # Try to break at sentence boundary if not at end
        if end < text_len:
            # Look for sentence end within last 200 chars of chunk
            last_period = chunk.rfind('. ')
            last_newline = chunk.rfind('\n')
            break_point = max(last_period, last_newline)

            if break_point > chunk_size - 200:  # Found good break point
                chunk = text[start:start + break_point + 1]
                end = start + break_point + 1

        chunks.append(chunk.strip())
        start = end - overlap

    return chunks

def ingest_html_file(client: chromadb.ClientAPI, collection, html_path: Path, doc_id_prefix: str):
    """
    Ingest a single HTML file into ChromaDB

    Returns:
        Number of chunks created
    """
    print(f"  Processing: {html_path.name}")

    # Extract text from HTML
    extracted = extract_text_from_html(html_path)

    # Chunk the content
    chunks = chunk_text(extracted['content'])

    # Prepare data for ChromaDB
    ids = [f"{doc_id_prefix}_{i}" for i in range(len(chunks))]
    documents = chunks
    metadatas = [
        {
            'source_file': extracted['metadata']['source_file'],
            'file_path': extracted['metadata']['file_path'],
            'title': extracted['title'],
            'act': extracted['act'],
            'chunk_index': i,
            'total_chunks': len(chunks)
        }
        for i in range(len(chunks))
    ]

    # Add to collection
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    print(f"    ✓ Created {len(chunks)} chunks")
    return len(chunks)

def main():
    """Main ingestion workflow"""
    print("🔄 Flyberry Brand Package → ChromaDB Ingestion")
    print("=" * 60)

    # Initialize ChromaDB client
    client = chromadb.PersistentClient(path=DB_PATH)

    # Delete existing collection if exists
    try:
        client.delete_collection(name=COLLECTION_NAME)
        print("✓ Deleted existing collection\n")
    except:
        pass

    # Create new collection
    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={
            "description": "Flyberry Brand Package - Complete 58-document set",
            "chunk_size": str(CHUNK_SIZE),
            "chunk_overlap": str(CHUNK_OVERLAP)
        }
    )
    print(f"✓ Created collection: {COLLECTION_NAME}\n")

    # Find all Act HTML files
    docs_dir = Path('./docs')
    act_files = [
        docs_dir / 'index.html',
        docs_dir / 'act-1-who-we-are.html',
        docs_dir / 'act-2-where-we-are.html',
        docs_dir / 'act-3-where-we-go.html',
        docs_dir / 'act-4-where-we-should-go.html',
        docs_dir / 'act-5-data-validation.html',
        docs_dir / 'act-6-operating-plan.html',
    ]

    # Ingest each file
    total_chunks = 0
    for i, html_path in enumerate(act_files):
        if not html_path.exists():
            print(f"  ⚠️  Skipping (not found): {html_path.name}")
            continue

        doc_id_prefix = f"doc_{i:02d}_{html_path.stem}"
        chunks_created = ingest_html_file(client, collection, html_path, doc_id_prefix)
        total_chunks += chunks_created

    print("\n" + "=" * 60)
    print(f"✅ Ingestion Complete")
    print(f"   Files ingested: {len([f for f in act_files if f.exists()])}")
    print(f"   Total chunks: {total_chunks}")
    print(f"   Database: {DB_PATH}")
    print(f"   Collection: {COLLECTION_NAME}")
    print("\n💡 Next: Run semantic search queries with query-chromadb.py")

if __name__ == "__main__":
    # Check for required dependencies
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("❌ Missing dependency: beautifulsoup4")
        print("Install with: pip install beautifulsoup4")
        sys.exit(1)

    main()
