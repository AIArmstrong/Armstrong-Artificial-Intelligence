FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js for MCP server support
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install MCP servers
RUN npm install -g @modelcontextprotocol/server-filesystem \
    @modelcontextprotocol/server-git \
    @modelcontextprotocol/server-puppeteer \
    @modelcontextprotocol/server-brave-search

# Create directories
RUN mkdir -p /app/research/_knowledge-base \
    /app/research/general \
    /app/research/projects \
    /app/research/_map \
    /app/research/validation \
    /app/research/_semantic \
    /app/logs

# Set permissions
RUN chmod +x /app/research/_map/*.py \
    /app/research/scripts/*.sh

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Default command
CMD ["python", "research/mcp/server.py"]