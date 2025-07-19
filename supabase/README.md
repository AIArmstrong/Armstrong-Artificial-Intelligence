# AAI Supabase Integration

Complete Supabase integration for searchability, persistence, and scalability.

## 📁 Folder Structure

```
supabase/
├── scripts/           # Database setup and utility scripts
├── migrations/        # Migration data and version control
├── modules/          # Python modules for Supabase integration
└── README.md         # This file
```

## 🚀 Quick Start

### 1. Database Setup (✅ COMPLETED)
```sql
-- Run in Supabase SQL Editor
-- File: scripts/setup_supabase_schema.sql
```

### 2. Install Dependencies
```bash
pip install psycopg2-binary python-dotenv
```

### 3. Upload Migration Data
```bash
python3 supabase/scripts/upload_migration_data.py
```

### 4. Set up Embeddings (Optional)
```bash
python3 supabase/scripts/setup_embeddings.py
```

## 📊 Database Schema

### Tables Created
- `aai_cache_entries` - Brain cache data
- `aai_conversation_states` - Conversation persistence
- `aai_research_docs` - Research documents with embeddings
- `aai_code_examples` - Code snippets with metadata
- `aai_task_analytics` - Task completion metrics
- `aai_search_index` - Unified search index
- `aai_ideas` - Idea registry with stages

### Features
- **Vector Embeddings**: 1536-dimensional embeddings for semantic search
- **Full-Text Search**: PostgreSQL full-text search with ranking
- **Auto-Timestamps**: Automatic created_at/updated_at tracking
- **Conflict Resolution**: Upsert support for data updates

## 🔍 Search Capabilities

### Full-Text Search
```python
from supabase.modules.supabase_search import SupabaseSearch

search = SupabaseSearch()
results = search.search_all("AI development", limit=10)
```

### Semantic Search
```python
# Requires embeddings setup
results = search.semantic_search("machine learning patterns", limit=5)
```

### Category Search
```python
results = search.search_by_category("ai-development", limit=20)
```

## 🔄 Auto-Offload System

### Triggers
- Research folder > 5MB → Auto-offload
- Cache files > 50 → Auto-offload
- Examples > 10MB → Auto-offload
- Files older than configured age → Auto-offload

### Run Auto-Offload Check
```bash
python3 supabase/modules/supabase_auto_offload.py
```

## 📂 Files Overview

### Scripts (`scripts/`)
- `setup_supabase_schema.sql` - Database schema setup
- `upload_migration_data.py` - Upload existing data to Supabase
- `test_supabase_connection.py` - Connection testing
- `setup_embeddings.py` - OpenRouter embeddings setup

### Migrations (`migrations/`)
- `supabase_migration_data.json` - Current migration data
- Future migration files will be versioned here

### Modules (`modules/`)
- `supabase_migration.py` - Data preparation for migration
- `supabase_search.py` - Unified search interface
- `supabase_auto_offload.py` - Automatic data offloading

## 🔧 Configuration

### Environment Variables Required
```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=db.your-project.supabase.co
DB_PORT=5432
DB_NAME=postgres
DATABASE_URL=postgresql://postgres:password@host:5432/postgres
```

### Connection Methods
1. **Direct connection**: Using individual DB_* variables
2. **Connection string**: Using DATABASE_URL
3. **Supabase client**: Using SUPABASE_URL + SUPABASE_KEY (legacy)

## 📈 Current Migration Status

### Data Summary
- **Research Documents**: 13 files
- **Code Examples**: 2 files
- **Cache Entries**: 1 entry
- **Conversation States**: 1 state
- **Ideas**: 6 ideas

### Total Size: ~4.5MB (room for massive growth)

## 🎯 Next Steps

1. **Upload data** using `upload_migration_data.py`
2. **Set up embeddings** for semantic search
3. **Update existing modules** to use Supabase instead of local files
4. **Configure auto-offload** thresholds based on usage patterns

## 🔒 Security

- Row Level Security (RLS) templates included
- Environment variable protection
- Content hashing for duplicate prevention
- Secure connection string handling

## 🤝 Integration Points

### Existing Modules Using Supabase
- `brain/modules/supabase-cache.py` - Cache implementation
- `brain/modules/openrouter/*.py` - Embeddings & API
- `research/_semantic/semantic_search.py` - Search functionality

### Future Integrations
- Real-time sync with local files
- Automatic backup scheduling
- Multi-user collaboration features
- Advanced analytics dashboards