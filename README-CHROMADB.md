# Flyberry Brand Package - ChromaDB Semantic Search

## Overview

This package includes ChromaDB integration for semantic search across all 58 brand documents.

**Benefits:**
- ✅ Find information using natural language queries
- ✅ Cross-document consistency checks
- ✅ Discover related content across multiple Acts
- ✅ Verify claims and citations
- ✅ Quality assurance for brand package

## Files

- `ingest-to-chromadb.py` - Ingest HTML files into ChromaDB
- `query-chromadb.py` - Search the brand package
- `chromadb/` - Database directory (created after ingestion)

## Setup

### 1. Install Dependencies

```bash
pip install chromadb beautifulsoup4
```

### 2. Ingest HTML Files

```bash
python3 ingest-to-chromadb.py
```

**What it does:**
- Extracts text from all Act HTML files
- Chunks content (2000 chars, 200 overlap)
- Creates embeddings for semantic search
- Stores in local ChromaDB database

**Expected output:**
```
🔄 Flyberry Brand Package → ChromaDB Ingestion
============================================================
✓ Created collection: flyberry_brand_package

  Processing: index.html
    ✓ Created 15 chunks
  Processing: act-1-who-we-are.html
    ✓ Created 42 chunks
  Processing: act-2-where-we-are.html
    ✓ Created 38 chunks
  ...

============================================================
✅ Ingestion Complete
   Files ingested: 7
   Total chunks: 250+
   Database: ./chromadb
   Collection: flyberry_brand_package
```

## Usage

### Interactive Search

```bash
python3 query-chromadb.py
```

**Example queries:**
```
🔍 Query: What are the Fortune 500 clients?
🔍 Query: What is the brand positioning?
🔍 Query: What are the pricing tiers?
🔍 Query: Who is the target audience?
🔍 Query: How do we differentiate from competitors?
```

### Command-Line Search

```bash
python3 query-chromadb.py "What is the brand archetype?"
```

### Preset Consistency Checks

```bash
python3 query-chromadb.py --preset
```

**Runs 6 preset queries:**
1. Fortune 500 clients - Verify corporate partners mentioned
2. Brand positioning - Check positioning consistency
3. Pricing tiers - Validate pricing ranges across documents
4. Brand archetype - Verify personality alignment
5. Target audience - Check audience definition consistency
6. Differentiation - Validate competitive positioning

## Search Results

Each result shows:
- **Similarity score** (0-100%)
- **Source file** (which Act/document)
- **Title** and **Act number**
- **Chunk position** (chunk X of Y)
- **Content preview** (first 500 characters)

**Example output:**
```
================================================================================
Result #1 | Similarity: 94.32%
================================================================================
📄 File: act-4-where-we-should-go.html
📖 Title: ACT 4: WHERE WE SHOULD GO - Strategic Direction
🎬 Act: Act 4
📍 Chunk: 15 of 87

--------------------------------------------------------------------------------
Content Preview:
--------------------------------------------------------------------------------
Brand Positioning: The North Star Statement

Flyberry is not just a gifting platform—it's India's first luxury...
```

## Use Cases

### 1. Consistency Checks

**Find all mentions of brand values:**
```
Query: What are the brand values?
```

Compare results across Acts 1, 3, and 4 to ensure alignment.

### 2. Citation Verification

**Find proof for claims:**
```
Query: Fortune 500 clients working with Flyberry
```

Verify that Act 5 (Data Validation) has evidence for claims in other Acts.

### 3. Cross-Document Updates

**When updating pricing:**
```
Query: pricing ranges and tiers
```

Find all documents mentioning pricing to ensure consistent updates.

### 4. Quality Assurance

**Check for contradictions:**
```
Query: target customer age and income
```

Verify demographic data is consistent across all documents.

### 5. Quick Reference

**Find specific information:**
```
Query: signature unboxing experience details
```

Locate exact section describing the unboxing ritual.

## Technical Details

### Chunking Strategy

- **Chunk size**: 2000 characters
- **Overlap**: 200 characters
- **Boundary**: Attempts to break at sentence endings
- **Metadata**: Source file, title, Act, chunk position

### Embedding Model

- **Default**: ChromaDB's default embedding function
- **Similarity**: Cosine similarity for search
- **Local**: Runs entirely on your machine (no API calls)

### Database

- **Type**: Persistent ChromaDB
- **Location**: `./chromadb/`
- **Collection**: `flyberry_brand_package`
- **Portability**: Can be copied to other machines

## Troubleshooting

### Ingestion fails with "ModuleNotFoundError"

```bash
pip install chromadb beautifulsoup4
```

### Query fails with "Collection not found"

Run ingestion first:
```bash
python3 ingest-to-chromadb.py
```

### Results seem irrelevant

Try:
- More specific queries
- Increase result count: `query-chromadb.py "query text" --results 10`
- Rephrase using different keywords

### Slow performance

First run is slowest (model download). Subsequent queries are faster.

## Future Enhancements

Potential additions:
- [ ] Support for PDF ingestion (for source PDFs)
- [ ] Custom embedding models (OpenAI, Cohere)
- [ ] Export search results to CSV
- [ ] Bulk consistency checking scripts
- [ ] Integration with brand builder pipeline

---

**Created:** October 22, 2025
**Version:** 1.0.0
**Database:** ChromaDB 0.4.22
