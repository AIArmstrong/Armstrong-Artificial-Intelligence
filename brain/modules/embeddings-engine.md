# Intent Similarity Learning Engine (Phase 2)

## 🧠 Semantic Intent Matching

### OpenRouter Embeddings Integration
**Model**: `text-embedding-ada-002`
**Dimensions**: 1536
**Similarity Threshold**: 0.85 (highly similar intents)
**API Endpoint**: OpenRouter proxy to OpenAI embeddings

### Intent Vector Storage
```json
{
  "intent_id": "system-overhaul-001",
  "timestamp": "2025-07-13T00:00:00Z",
  "raw_intent": "comprehensive AAI architecture enhancement",
  "processed_intent": "architecture overhaul system enhancement",
  "embedding_vector": [0.1234, -0.5678, ...], // 1536 dimensions
  "cluster_assignment": "Framework Shifts",
  "similarity_matches": [
    {"intent_id": "cache-refactor-003", "similarity": 0.87},
    {"intent_id": "brain-architecture-001", "similarity": 0.92}
  ],
  "success_outcome": true,
  "execution_time_minutes": 180
}
```

### Similarity Learning Algorithm
1. **Intent Preprocessing**: Extract key terms, normalize language
2. **Vector Generation**: Send to OpenRouter embeddings API
3. **Similarity Search**: Cosine similarity against existing vectors
4. **Pattern Matching**: If similarity > 0.85, recommend previous successful approach
5. **Learning Update**: Store new vector and outcome for future matching

### API Implementation
```python
# Integration with existing .env OpenRouter credentials
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

async def get_intent_embedding(intent_text: str) -> List[float]:
    """Generate embedding vector for intent similarity matching."""
    response = await openrouter_client.embeddings.create(
        model="text-embedding-ada-002",
        input=intent_text
    )
    return response.data[0].embedding

async def find_similar_intents(current_embedding: List[float], threshold: float = 0.85):
    """Find similar historical intents using cosine similarity."""
    # Load from brain/cache/intent-vectors.json
    # Calculate cosine similarity
    # Return matches above threshold
```

### Storage Strategy
- **Vectors**: `brain/cache/intent-vectors.json` (searchable via Supabase)
- **Index**: `brain/cache/similarity-index.json` (fast lookup)
- **Archive**: Auto-archive vectors older than 6 months

### Success Metrics
- **Intent Recognition Accuracy**: Target >90%
- **Pattern Reuse Rate**: Target >75%
- **False Positive Rate**: Target <5%
- **API Cost**: ~$0.0001 per intent (~$3/month for heavy usage)

---
*Semantic intelligence layer for true AI cognition*