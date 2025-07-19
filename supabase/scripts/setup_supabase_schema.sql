-- AAI Supabase Schema Setup
-- Run this in Supabase SQL Editor to set up all necessary tables

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- 1. Brain Cache Tables
CREATE TABLE IF NOT EXISTS aai_cache_entries (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    key TEXT UNIQUE NOT NULL,
    value JSONB NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    accessed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    access_count INTEGER DEFAULT 1,
    ttl INTEGER DEFAULT NULL,
    expires_at TIMESTAMP WITH TIME ZONE DEFAULT NULL
);

-- 2. Conversation States
CREATE TABLE IF NOT EXISTS aai_conversation_states (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id TEXT UNIQUE NOT NULL,
    state JSONB NOT NULL,
    context JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_interaction TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Research Documents
CREATE TABLE IF NOT EXISTS aai_research_docs (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    source_url TEXT,
    source_file TEXT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    content_hash TEXT UNIQUE,
    metadata JSONB DEFAULT '{}',
    category TEXT,
    quality_score NUMERIC(3,2),
    embedding vector(1536),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    accessed_count INTEGER DEFAULT 0
);

-- 4. Code Examples
CREATE TABLE IF NOT EXISTS aai_code_examples (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    code TEXT NOT NULL,
    language TEXT NOT NULL,
    tags TEXT[],
    category TEXT,
    success_score NUMERIC(3,2) DEFAULT 0,
    usage_count INTEGER DEFAULT 0,
    embedding vector(1536),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. Task Analytics
CREATE TABLE IF NOT EXISTS aai_task_analytics (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    task_id TEXT NOT NULL,
    task_title TEXT NOT NULL,
    category TEXT,
    priority TEXT,
    status TEXT NOT NULL,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    duration_minutes INTEGER,
    success_score NUMERIC(3,2),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 6. Search Index
CREATE TABLE IF NOT EXISTS aai_search_index (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    content_type TEXT NOT NULL, -- 'research', 'example', 'task', 'idea'
    content_id UUID NOT NULL,
    searchable_text TEXT NOT NULL,
    tags TEXT[],
    embedding vector(1536),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 7. Idea Registry
CREATE TABLE IF NOT EXISTS aai_ideas (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    stage TEXT NOT NULL, -- 'seed', 'sprout', 'growth', 'fruit', 'harvest', 'archive'
    category TEXT,
    mode TEXT, -- 'innovator', 'critic', 'enhancer', 'logic'
    research_ready BOOLEAN DEFAULT FALSE,
    next_action TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_cache_key ON aai_cache_entries(key);
CREATE INDEX idx_cache_expires ON aai_cache_entries(expires_at) WHERE expires_at IS NOT NULL;
CREATE INDEX idx_research_category ON aai_research_docs(category);
CREATE INDEX idx_research_quality ON aai_research_docs(quality_score);
CREATE INDEX idx_examples_tags ON aai_code_examples USING GIN(tags);
CREATE INDEX idx_examples_category ON aai_code_examples(category);
CREATE INDEX idx_search_content_type ON aai_search_index(content_type);
CREATE INDEX idx_search_tags ON aai_search_index USING GIN(tags);
CREATE INDEX idx_ideas_stage ON aai_ideas(stage);
CREATE INDEX idx_ideas_category ON aai_ideas(category);

-- Full text search indexes
CREATE INDEX idx_research_fts ON aai_research_docs USING GIN(to_tsvector('english', content));
CREATE INDEX idx_search_fts ON aai_search_index USING GIN(to_tsvector('english', searchable_text));

-- Vector similarity search indexes (for embeddings)
CREATE INDEX idx_research_embedding ON aai_research_docs USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_examples_embedding ON aai_code_examples USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_search_embedding ON aai_search_index USING ivfflat (embedding vector_cosine_ops);

-- Update triggers
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_cache_timestamp BEFORE UPDATE ON aai_cache_entries
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_states_timestamp BEFORE UPDATE ON aai_conversation_states
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_research_timestamp BEFORE UPDATE ON aai_research_docs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_examples_timestamp BEFORE UPDATE ON aai_code_examples
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_ideas_timestamp BEFORE UPDATE ON aai_ideas
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Row Level Security (RLS) - Enable if needed
-- ALTER TABLE aai_cache_entries ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE aai_conversation_states ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE aai_research_docs ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE aai_code_examples ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE aai_task_analytics ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE aai_search_index ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE aai_ideas ENABLE ROW LEVEL SECURITY;

-- Grant permissions (adjust based on your auth setup)
-- GRANT ALL ON ALL TABLES IN SCHEMA public TO authenticated;
-- GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO authenticated;
-- GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO authenticated;

-- Success message
SELECT 'AAI Supabase schema created successfully!' as message;