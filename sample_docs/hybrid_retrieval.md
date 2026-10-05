# Hybrid Retrieval

Hybrid retrieval combines **sparse** lexical matching (BM25) with **dense**
vector similarity. Sparse search excels at exact keywords and rare tokens.
Dense search captures semantic paraphrase. Reciprocal Rank Fusion (RRF)
merges ranked lists without needing score calibration.

## Why it matters for RAG

Pure vector search often misses exact identifiers (error codes, API names).
Pure BM25 misses paraphrases. Hybrid systems reduce both failure modes and
improve citation faithfulness when the LLM is grounded on top-k chunks.
