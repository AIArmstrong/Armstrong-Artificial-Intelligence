-- AAI Memory Enhancement Schema Migration
-- Migration: 004 - Memory Enhancement System
-- Created: 2025-07-19
-- Purpose: Add memory enhancement tables for AAI command memory intelligence

-- Enable required extensions (if not already enabled)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- =====================================================
-- MEMORY CORE TABLES
-- =====================================================

-- 1. Core Memories Table - Stores all memory items with embeddings
CREATE TABLE IF NOT EXISTS aai_mem0_memories (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    content TEXT NOT NULL,
    content_type TEXT NOT NULL, -- 'prp', 'implementation', 'analysis', 'research', etc.
    content_hash TEXT UNIQUE, -- For deduplication
    embedding vector(1536), -- OpenAI text-embedding-3-small compatible
    metadata JSONB DEFAULT '{}',
    confidence_score NUMERIC(3,2) DEFAULT 0.85 CHECK (confidence_score >= 0.70 AND confidence_score <= 0.95),
    quality_score NUMERIC(3,2) DEFAULT 0.0 CHECK (quality_score >= 0.0 AND quality_score <= 1.0),
    usage_count INTEGER DEFAULT 0,
    tags TEXT[] DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_accessed TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. User Preferences Table - Stores learned user preferences
CREATE TABLE IF NOT EXISTS aai_mem0_user_preferences (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id TEXT NOT NULL,
    preferences JSONB NOT NULL DEFAULT '{}',
    preference_type TEXT DEFAULT 'general', -- 'coding', 'architecture', 'tools', etc.
    confidence_score NUMERIC(3,2) DEFAULT 0.80,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, preference_type)
);

-- 3. Memory Patterns Table - Stores successful workflow patterns
CREATE TABLE IF NOT EXISTS aai_mem0_patterns (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id TEXT NOT NULL,
    pattern_type TEXT NOT NULL, -- 'workflow', 'implementation', 'solution'
    command_type TEXT NOT NULL, -- 'generate-prp', 'implement', 'analyze'
    pattern_data JSONB NOT NULL,
    success_rate NUMERIC(3,2) DEFAULT 1.0,
    usage_count INTEGER DEFAULT 1,
    confidence_score NUMERIC(3,2) DEFAULT 0.85,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_used TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Memory Interactions Table - Tracks memory usage and effectiveness
CREATE TABLE IF NOT EXISTS aai_mem0_interactions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    memory_id TEXT REFERENCES aai_mem0_memories(id) ON DELETE CASCADE,
    user_id TEXT NOT NULL,
    interaction_type TEXT NOT NULL, -- 'retrieve', 'enhance', 'feedback'
    command_type TEXT,
    context_query TEXT,
    relevance_score NUMERIC(3,2),
    user_feedback TEXT, -- 'helpful', 'not_helpful', 'partially_helpful'
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. Enhancement Events Table - Tracks command enhancement events
CREATE TABLE IF NOT EXISTS aai_mem0_enhancement_events (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id TEXT,
    session_id TEXT,
    command_type TEXT NOT NULL,
    original_args JSONB,
    enhanced_args JSONB,
    memory_context_available BOOLEAN DEFAULT FALSE,
    confidence_score NUMERIC(3,2),
    enhancement_success BOOLEAN,
    execution_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 6. Memory Quality Metrics Table - Tracks memory quality over time
CREATE TABLE IF NOT EXISTS aai_mem0_quality_metrics (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    memory_id TEXT REFERENCES aai_mem0_memories(id) ON DELETE CASCADE,
    quality_dimension TEXT NOT NULL, -- 'relevance', 'accuracy', 'usefulness', 'freshness'
    score NUMERIC(3,2) NOT NULL,
    measured_by TEXT DEFAULT 'system', -- 'system', 'user', 'ai'
    measurement_context TEXT,
    measured_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- Memory search indexes
CREATE INDEX idx_mem0_memories_user_id ON aai_mem0_memories(user_id);
CREATE INDEX idx_mem0_memories_content_type ON aai_mem0_memories(content_type);
CREATE INDEX idx_mem0_memories_confidence ON aai_mem0_memories(confidence_score);
CREATE INDEX idx_mem0_memories_quality ON aai_mem0_memories(quality_score);
CREATE INDEX idx_mem0_memories_usage ON aai_mem0_memories(usage_count);
CREATE INDEX idx_mem0_memories_created ON aai_mem0_memories(created_at);
CREATE INDEX idx_mem0_memories_accessed ON aai_mem0_memories(last_accessed);
CREATE INDEX idx_mem0_memories_tags ON aai_mem0_memories USING GIN(tags);
CREATE INDEX idx_mem0_memories_metadata ON aai_mem0_memories USING GIN(metadata);

-- Vector similarity search index
CREATE INDEX idx_mem0_memories_embedding ON aai_mem0_memories 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Full text search index
CREATE INDEX idx_mem0_memories_content_fts ON aai_mem0_memories 
USING GIN(to_tsvector('english', content));

-- User preferences indexes
CREATE INDEX idx_mem0_user_prefs_user_id ON aai_mem0_user_preferences(user_id);
CREATE INDEX idx_mem0_user_prefs_type ON aai_mem0_user_preferences(preference_type);
CREATE INDEX idx_mem0_user_prefs_confidence ON aai_mem0_user_preferences(confidence_score);

-- Pattern indexes
CREATE INDEX idx_mem0_patterns_user_id ON aai_mem0_patterns(user_id);
CREATE INDEX idx_mem0_patterns_type ON aai_mem0_patterns(pattern_type);
CREATE INDEX idx_mem0_patterns_command ON aai_mem0_patterns(command_type);
CREATE INDEX idx_mem0_patterns_success ON aai_mem0_patterns(success_rate);
CREATE INDEX idx_mem0_patterns_usage ON aai_mem0_patterns(usage_count);

-- Interaction indexes
CREATE INDEX idx_mem0_interactions_memory_id ON aai_mem0_interactions(memory_id);
CREATE INDEX idx_mem0_interactions_user_id ON aai_mem0_interactions(user_id);
CREATE INDEX idx_mem0_interactions_type ON aai_mem0_interactions(interaction_type);
CREATE INDEX idx_mem0_interactions_command ON aai_mem0_interactions(command_type);
CREATE INDEX idx_mem0_interactions_created ON aai_mem0_interactions(created_at);

-- Enhancement events indexes
CREATE INDEX idx_mem0_enhancement_user_id ON aai_mem0_enhancement_events(user_id);
CREATE INDEX idx_mem0_enhancement_session ON aai_mem0_enhancement_events(session_id);
CREATE INDEX idx_mem0_enhancement_command ON aai_mem0_enhancement_events(command_type);
CREATE INDEX idx_mem0_enhancement_success ON aai_mem0_enhancement_events(enhancement_success);
CREATE INDEX idx_mem0_enhancement_created ON aai_mem0_enhancement_events(created_at);

-- Quality metrics indexes
CREATE INDEX idx_mem0_quality_memory_id ON aai_mem0_quality_metrics(memory_id);
CREATE INDEX idx_mem0_quality_dimension ON aai_mem0_quality_metrics(quality_dimension);
CREATE INDEX idx_mem0_quality_score ON aai_mem0_quality_metrics(score);
CREATE INDEX idx_mem0_quality_measured_at ON aai_mem0_quality_metrics(measured_at);

-- =====================================================
-- TRIGGERS AND FUNCTIONS
-- =====================================================

-- Function to update timestamps
CREATE OR REPLACE FUNCTION update_mem0_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Function to update last_accessed on memory retrieval
CREATE OR REPLACE FUNCTION update_mem0_last_accessed()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE aai_mem0_memories 
    SET last_accessed = NOW(), usage_count = usage_count + 1
    WHERE id = NEW.memory_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Function to generate content hash
CREATE OR REPLACE FUNCTION generate_mem0_content_hash()
RETURNS TRIGGER AS $$
BEGIN
    NEW.content_hash = encode(digest(NEW.content, 'md5'), 'hex');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply triggers
CREATE TRIGGER trigger_mem0_memories_updated_at 
    BEFORE UPDATE ON aai_mem0_memories
    FOR EACH ROW EXECUTE FUNCTION update_mem0_updated_at();

CREATE TRIGGER trigger_mem0_user_prefs_updated_at 
    BEFORE UPDATE ON aai_mem0_user_preferences
    FOR EACH ROW EXECUTE FUNCTION update_mem0_updated_at();

CREATE TRIGGER trigger_mem0_memories_content_hash 
    BEFORE INSERT OR UPDATE ON aai_mem0_memories
    FOR EACH ROW EXECUTE FUNCTION generate_mem0_content_hash();

CREATE TRIGGER trigger_mem0_interaction_access 
    AFTER INSERT ON aai_mem0_interactions
    FOR EACH ROW 
    WHEN (NEW.interaction_type = 'retrieve')
    EXECUTE FUNCTION update_mem0_last_accessed();

-- =====================================================
-- UTILITY FUNCTIONS
-- =====================================================

-- Function to search memories by vector similarity
CREATE OR REPLACE FUNCTION search_mem0_memories_by_similarity(
    p_user_id TEXT,
    p_embedding vector(1536),
    p_content_type TEXT DEFAULT NULL,
    p_limit INTEGER DEFAULT 10,
    p_min_confidence NUMERIC DEFAULT 0.70
)
RETURNS TABLE (
    id TEXT,
    content TEXT,
    content_type TEXT,
    confidence_score NUMERIC,
    quality_score NUMERIC,
    similarity NUMERIC,
    usage_count INTEGER,
    tags TEXT[],
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        m.id,
        m.content,
        m.content_type,
        m.confidence_score,
        m.quality_score,
        (1 - (m.embedding <=> p_embedding))::NUMERIC as similarity,
        m.usage_count,
        m.tags,
        m.metadata,
        m.created_at
    FROM aai_mem0_memories m
    WHERE m.user_id = p_user_id
        AND m.confidence_score >= p_min_confidence
        AND (p_content_type IS NULL OR m.content_type = p_content_type)
        AND m.embedding IS NOT NULL
    ORDER BY m.embedding <=> p_embedding
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;

-- Function to get user preferences with defaults
CREATE OR REPLACE FUNCTION get_mem0_user_preferences(
    p_user_id TEXT,
    p_preference_type TEXT DEFAULT 'general'
)
RETURNS JSONB AS $$
DECLARE
    preferences JSONB;
BEGIN
    SELECT p.preferences INTO preferences
    FROM aai_mem0_user_preferences p
    WHERE p.user_id = p_user_id AND p.preference_type = p_preference_type;
    
    RETURN COALESCE(preferences, '{}'::JSONB);
END;
$$ LANGUAGE plpgsql;

-- Function to update memory quality based on interactions
CREATE OR REPLACE FUNCTION update_mem0_quality_from_feedback()
RETURNS TRIGGER AS $$
DECLARE
    new_quality NUMERIC;
BEGIN
    -- Calculate quality based on user feedback
    SELECT AVG(
        CASE 
            WHEN user_feedback = 'helpful' THEN 1.0
            WHEN user_feedback = 'partially_helpful' THEN 0.6
            WHEN user_feedback = 'not_helpful' THEN 0.2
            ELSE 0.5
        END
    ) INTO new_quality
    FROM aai_mem0_interactions
    WHERE memory_id = NEW.memory_id
        AND user_feedback IS NOT NULL;
    
    -- Update memory quality if we have feedback
    IF new_quality IS NOT NULL THEN
        UPDATE aai_mem0_memories 
        SET quality_score = new_quality
        WHERE id = NEW.memory_id;
        
        -- Record quality metric
        INSERT INTO aai_mem0_quality_metrics (memory_id, quality_dimension, score, measured_by)
        VALUES (NEW.memory_id, 'user_feedback', new_quality, 'user');
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply quality update trigger
CREATE TRIGGER trigger_mem0_quality_from_feedback 
    AFTER INSERT OR UPDATE ON aai_mem0_interactions
    FOR EACH ROW 
    WHEN (NEW.user_feedback IS NOT NULL)
    EXECUTE FUNCTION update_mem0_quality_from_feedback();

-- =====================================================
-- MEMORY CLEANUP FUNCTIONS
-- =====================================================

-- Function to cleanup old, low-quality memories
CREATE OR REPLACE FUNCTION cleanup_mem0_old_memories(
    p_max_age_days INTEGER DEFAULT 90,
    p_min_quality_threshold NUMERIC DEFAULT 0.3
)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    -- Delete old, low-quality memories that haven't been accessed recently
    DELETE FROM aai_mem0_memories
    WHERE (
        (created_at < NOW() - INTERVAL '1 day' * p_max_age_days)
        OR (quality_score < p_min_quality_threshold AND usage_count = 0)
        OR (last_accessed < NOW() - INTERVAL '30 days' AND usage_count < 2)
    )
    AND quality_score < 0.7; -- Don't delete high-quality memories
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    
    -- Log cleanup event
    INSERT INTO aai_mem0_enhancement_events (
        command_type, 
        metadata,
        created_at
    ) VALUES (
        'memory_cleanup',
        jsonb_build_object(
            'deleted_count', deleted_count,
            'max_age_days', p_max_age_days,
            'min_quality_threshold', p_min_quality_threshold
        ),
        NOW()
    );
    
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- MEMORY ANALYTICS VIEWS
-- =====================================================

-- View for memory usage analytics
CREATE OR REPLACE VIEW mem0_memory_analytics AS
SELECT 
    user_id,
    content_type,
    COUNT(*) as memory_count,
    AVG(confidence_score) as avg_confidence,
    AVG(quality_score) as avg_quality,
    SUM(usage_count) as total_usage,
    MAX(last_accessed) as latest_access,
    MIN(created_at) as earliest_memory
FROM aai_mem0_memories
GROUP BY user_id, content_type;

-- View for enhancement effectiveness
CREATE OR REPLACE VIEW mem0_enhancement_analytics AS
SELECT 
    command_type,
    COUNT(*) as total_enhancements,
    COUNT(*) FILTER (WHERE memory_context_available) as with_memory_context,
    COUNT(*) FILTER (WHERE enhancement_success) as successful_enhancements,
    AVG(confidence_score) as avg_confidence,
    AVG(execution_time_ms) as avg_execution_time_ms
FROM aai_mem0_enhancement_events
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY command_type;

-- View for user preference insights
CREATE OR REPLACE VIEW mem0_user_preference_insights AS
SELECT 
    user_id,
    preference_type,
    jsonb_object_keys(preferences) as preference_key,
    preferences,
    confidence_score,
    last_updated
FROM aai_mem0_user_preferences;

-- =====================================================
-- ROW LEVEL SECURITY (OPTIONAL)
-- =====================================================

-- Enable RLS on memory tables (uncomment if needed)
-- ALTER TABLE aai_mem0_memories ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE aai_mem0_user_preferences ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE aai_mem0_patterns ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE aai_mem0_interactions ENABLE ROW LEVEL SECURITY;

-- Example RLS policies (uncomment and customize if needed)
-- CREATE POLICY mem0_memories_user_access ON aai_mem0_memories
--     FOR ALL USING (user_id = current_setting('app.current_user'));

-- =====================================================
-- INITIAL DATA AND TESTING
-- =====================================================

-- Insert initial system preferences
INSERT INTO aai_mem0_user_preferences (user_id, preference_type, preferences, confidence_score)
VALUES 
    ('system', 'default_confidence', '{"min": 0.70, "target": 0.85, "max": 0.95}', 0.95),
    ('system', 'quality_thresholds', '{"min_useful": 0.3, "good": 0.6, "excellent": 0.8}', 0.95)
ON CONFLICT (user_id, preference_type) DO NOTHING;

-- Success message
SELECT 'AAI Memory Enhancement schema (004) created successfully!' as message,
       'Tables: aai_mem0_memories, aai_mem0_user_preferences, aai_mem0_patterns, aai_mem0_interactions, aai_mem0_enhancement_events, aai_mem0_quality_metrics' as tables_created,
       'Features: Vector search, Quality tracking, Pattern learning, User preferences, Enhancement analytics' as features_enabled;