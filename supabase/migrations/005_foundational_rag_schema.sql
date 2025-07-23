-- Foundational RAG Agent Schema Migration
-- Extends existing AAI Supabase schema with RAG-specific tables

-- Enable required extensions (if not already enabled)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- 1. RAG Documents Table
-- Stores uploaded documents with their metadata
CREATE TABLE IF NOT EXISTS aai_rag_documents (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    filename TEXT NOT NULL,
    original_filename TEXT NOT NULL,
    file_type TEXT NOT NULL, -- 'pdf', 'txt', 'md', etc.
    file_size_bytes INTEGER NOT NULL,
    upload_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    document_hash TEXT UNIQUE NOT NULL, -- For deduplication
    title TEXT,
    author TEXT,
    document_metadata JSONB DEFAULT '{}',
    processing_status TEXT DEFAULT 'pending', -- 'pending', 'processing', 'completed', 'failed'
    processing_error TEXT,
    total_chunks INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. RAG Document Chunks Table
-- Stores processed document chunks with embeddings
CREATE TABLE IF NOT EXISTS aai_rag_chunks (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    document_id UUID NOT NULL REFERENCES aai_rag_documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL, -- Order within document
    content TEXT NOT NULL,
    content_length INTEGER NOT NULL,
    chunk_type TEXT DEFAULT 'text', -- 'text', 'heading', 'table', etc.
    
    -- Embedding for semantic search
    embedding vector(1536), -- OpenAI text-embedding-3-small
    
    -- Chunk metadata
    page_number INTEGER,
    section_title TEXT,
    chunk_metadata JSONB DEFAULT '{}',
    
    -- Quality scoring (AAI pattern)
    confidence_score NUMERIC(3,2) DEFAULT 0.70 CHECK (confidence_score >= 0.70 AND confidence_score <= 0.95),
    quality_score NUMERIC(3,2) DEFAULT 0.50,
    
    -- Usage tracking
    retrieval_count INTEGER DEFAULT 0,
    last_retrieved TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. RAG Search Sessions Table
-- Tracks search/question sessions for analytics
CREATE TABLE IF NOT EXISTS aai_rag_sessions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_token TEXT UNIQUE NOT NULL,
    user_identifier TEXT, -- Optional user tracking
    
    -- Session metadata
    session_start TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    session_end TIMESTAMP WITH TIME ZONE,
    total_queries INTEGER DEFAULT 0,
    successful_queries INTEGER DEFAULT 0,
    
    -- Quality metrics
    average_confidence NUMERIC(3,2),
    average_relevance NUMERIC(3,2),
    user_satisfaction INTEGER, -- 1-5 rating
    
    session_metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. RAG Query History Table
-- Stores individual queries and responses for learning
CREATE TABLE IF NOT EXISTS aai_rag_queries (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id UUID NOT NULL REFERENCES aai_rag_sessions(id) ON DELETE CASCADE,
    
    -- Query details
    query_text TEXT NOT NULL,
    query_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    query_type TEXT DEFAULT 'question', -- 'question', 'search', 'summary'
    
    -- Response details
    response_text TEXT,
    response_sources TEXT[], -- Array of source references
    
    -- Retrieved chunks (for analysis)
    retrieved_chunk_ids UUID[],
    top_chunk_scores NUMERIC[],
    
    -- Quality metrics (AAI standards)
    confidence_score NUMERIC(3,2) DEFAULT 0.70 CHECK (confidence_score >= 0.70 AND confidence_score <= 0.95),
    relevance_score NUMERIC(3,2) DEFAULT 0.50,
    response_time_ms INTEGER,
    
    -- User feedback
    user_rating INTEGER, -- 1-5 scale
    user_feedback TEXT,
    helpful BOOLEAN,
    
    -- Processing metadata
    processing_metadata JSONB DEFAULT '{}',
    error_message TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. RAG Knowledge Base Table
-- Stores curated knowledge items for enhanced responses
CREATE TABLE IF NOT EXISTS aai_rag_knowledge (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    knowledge_type TEXT NOT NULL, -- 'fact', 'definition', 'process', 'example'
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    source_reference TEXT,
    
    -- Knowledge quality
    confidence_score NUMERIC(3,2) DEFAULT 0.85 CHECK (confidence_score >= 0.70 AND confidence_score <= 0.95),
    authority_score NUMERIC(3,2) DEFAULT 0.50, -- How authoritative is this knowledge
    recency_score NUMERIC(3,2) DEFAULT 0.50, -- How recent/current is this knowledge
    
    -- Categorization
    domain TEXT, -- 'technical', 'business', 'general'
    tags TEXT[],
    keywords TEXT[],
    
    -- Embedding for search
    embedding vector(1536),
    
    -- Usage tracking
    reference_count INTEGER DEFAULT 0,
    last_referenced TIMESTAMP WITH TIME ZONE,
    
    -- Lifecycle
    active BOOLEAN DEFAULT TRUE,
    verified BOOLEAN DEFAULT FALSE,
    verification_source TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create performance indexes

-- Document indexes
CREATE INDEX idx_rag_docs_status ON aai_rag_documents(processing_status);
CREATE INDEX idx_rag_docs_type ON aai_rag_documents(file_type);
CREATE INDEX idx_rag_docs_hash ON aai_rag_documents(document_hash);
CREATE INDEX idx_rag_docs_created ON aai_rag_documents(created_at);

-- Chunk indexes
CREATE INDEX idx_rag_chunks_doc ON aai_rag_chunks(document_id);
CREATE INDEX idx_rag_chunks_confidence ON aai_rag_chunks(confidence_score);
CREATE INDEX idx_rag_chunks_quality ON aai_rag_chunks(quality_score);
CREATE INDEX idx_rag_chunks_retrieval ON aai_rag_chunks(retrieval_count);

-- Session indexes
CREATE INDEX idx_rag_sessions_token ON aai_rag_sessions(session_token);
CREATE INDEX idx_rag_sessions_start ON aai_rag_sessions(session_start);
CREATE INDEX idx_rag_sessions_confidence ON aai_rag_sessions(average_confidence);

-- Query indexes
CREATE INDEX idx_rag_queries_session ON aai_rag_queries(session_id);
CREATE INDEX idx_rag_queries_timestamp ON aai_rag_queries(query_timestamp);
CREATE INDEX idx_rag_queries_confidence ON aai_rag_queries(confidence_score);
CREATE INDEX idx_rag_queries_rating ON aai_rag_queries(user_rating);

-- Knowledge indexes
CREATE INDEX idx_rag_knowledge_type ON aai_rag_knowledge(knowledge_type);
CREATE INDEX idx_rag_knowledge_domain ON aai_rag_knowledge(domain);
CREATE INDEX idx_rag_knowledge_active ON aai_rag_knowledge(active);
CREATE INDEX idx_rag_knowledge_tags ON aai_rag_knowledge USING GIN(tags);

-- Full-text search indexes
CREATE INDEX idx_rag_chunks_fts ON aai_rag_chunks USING GIN(to_tsvector('english', content));
CREATE INDEX idx_rag_queries_fts ON aai_rag_queries USING GIN(to_tsvector('english', query_text));
CREATE INDEX idx_rag_knowledge_fts ON aai_rag_knowledge USING GIN(to_tsvector('english', content));

-- Vector similarity search indexes (for embeddings)
CREATE INDEX idx_rag_chunks_embedding ON aai_rag_chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX idx_rag_knowledge_embedding ON aai_rag_knowledge USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Update triggers for timestamps
CREATE TRIGGER update_rag_docs_timestamp BEFORE UPDATE ON aai_rag_documents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_rag_chunks_timestamp BEFORE UPDATE ON aai_rag_chunks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_rag_sessions_timestamp BEFORE UPDATE ON aai_rag_sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_rag_knowledge_timestamp BEFORE UPDATE ON aai_rag_knowledge
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Useful stored functions for RAG operations

-- Function to search document chunks by similarity
CREATE OR REPLACE FUNCTION search_rag_chunks(
    query_embedding vector(1536),
    similarity_threshold float DEFAULT 0.5,
    max_results int DEFAULT 10
)
RETURNS TABLE (
    chunk_id UUID,
    document_id UUID,
    content TEXT,
    similarity_score FLOAT,
    confidence_score NUMERIC,
    filename TEXT,
    chunk_index INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id,
        c.document_id,
        c.content,
        1 - (c.embedding <=> query_embedding) AS similarity,
        c.confidence_score,
        d.filename,
        c.chunk_index
    FROM aai_rag_chunks c
    JOIN aai_rag_documents d ON c.document_id = d.id
    WHERE 
        d.processing_status = 'completed'
        AND c.embedding IS NOT NULL
        AND 1 - (c.embedding <=> query_embedding) > similarity_threshold
    ORDER BY c.embedding <=> query_embedding
    LIMIT max_results;
END;
$$ LANGUAGE plpgsql;

-- Function to get document statistics
CREATE OR REPLACE FUNCTION get_rag_document_stats()
RETURNS TABLE (
    total_documents BIGINT,
    total_chunks BIGINT,
    processed_documents BIGINT,
    average_confidence NUMERIC,
    total_queries BIGINT,
    average_response_time NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(*)::BIGINT as total_docs,
        COALESCE(SUM(total_chunks), 0)::BIGINT as total_chunks,
        COUNT(CASE WHEN processing_status = 'completed' THEN 1 END)::BIGINT as processed_docs,
        (SELECT AVG(confidence_score) FROM aai_rag_chunks WHERE confidence_score IS NOT NULL),
        (SELECT COUNT(*)::BIGINT FROM aai_rag_queries),
        (SELECT AVG(response_time_ms) FROM aai_rag_queries WHERE response_time_ms IS NOT NULL)
    FROM aai_rag_documents;
END;
$$ LANGUAGE plpgsql;

-- Function to update chunk retrieval count
CREATE OR REPLACE FUNCTION increment_chunk_retrieval(chunk_ids UUID[])
RETURNS VOID AS $$
BEGIN
    UPDATE aai_rag_chunks 
    SET 
        retrieval_count = retrieval_count + 1,
        last_retrieved = NOW()
    WHERE id = ANY(chunk_ids);
END;
$$ LANGUAGE plpgsql;

-- Success message
SELECT 'Foundational RAG schema created successfully! Ready for document processing and semantic search.' as message;

-- View for easy chunk retrieval with document info
CREATE OR REPLACE VIEW rag_chunks_with_documents AS
SELECT 
    c.id as chunk_id,
    c.content,
    c.chunk_index,
    c.confidence_score,
    c.quality_score,
    c.retrieval_count,
    c.created_at as chunk_created_at,
    d.id as document_id,
    d.filename,
    d.original_filename,
    d.file_type,
    d.title as document_title,
    d.author,
    d.upload_timestamp,
    d.processing_status
FROM aai_rag_chunks c
JOIN aai_rag_documents d ON c.document_id = d.id;

-- View for query analytics
CREATE OR REPLACE VIEW rag_query_analytics AS
SELECT 
    DATE_TRUNC('day', query_timestamp) as query_date,
    COUNT(*) as total_queries,
    AVG(confidence_score) as avg_confidence,
    AVG(relevance_score) as avg_relevance,
    AVG(response_time_ms) as avg_response_time_ms,
    COUNT(CASE WHEN user_rating >= 4 THEN 1 END) as positive_ratings,
    COUNT(CASE WHEN helpful = true THEN 1 END) as helpful_responses
FROM aai_rag_queries
GROUP BY DATE_TRUNC('day', query_timestamp)
ORDER BY query_date DESC;