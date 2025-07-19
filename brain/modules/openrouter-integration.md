# OpenRouter Integration Module

## 🔗 LLM Intelligence Services

### Embeddings Engine
**Model**: text-embedding-ada-002
**Dimensions**: 1536
**Cost**: ~$0.0001 per intent (~$3/month heavy usage)
**Storage**: brain/cache/intent-vectors.json + Supabase

### Contradiction Detection
**Model**: openai/gpt-4o-mini
**Trigger**: Content conflicts with existing state
**Response**: Flag inconsistencies, suggest resolution
**Integration**: /log command auto-checking

### API Implementation
```python
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

async def get_intent_embedding(intent_text: str) -> List[float]:
    response = await openrouter_client.embeddings.create(
        model="text-embedding-ada-002", input=intent_text
    )
    return response.data[0].embedding
```

### Intelligence Services
- **Intent Similarity**: Cosine similarity matching >0.85 threshold
- **Pattern Recognition**: Semantic clustering for recipe creation
- **Learning Enhancement**: Feedback loop for improved accuracy