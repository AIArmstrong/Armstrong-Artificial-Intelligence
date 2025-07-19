# GitHub Repository Analyzer - Security Sandbox
# Multi-stage build for optimized security
FROM python:3.11-slim AS builder

# Install build dependencies only in builder stage
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg2 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (using binary instead of script)
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - \
    && echo "deb https://deb.nodesource.com/node_18.x bullseye main" > /etc/apt/sources.list.d/nodesource.list \
    && apt-get update && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Go
RUN wget https://go.dev/dl/go1.21.0.linux-amd64.tar.gz \
    && echo "d0398903a16ba2232b389fb31032ddf57cac34efda306a0eebac34f0965a0742  go1.21.0.linux-amd64.tar.gz" | sha256sum -c - \
    && tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz \
    && rm go1.21.0.linux-amd64.tar.gz

# Production stage
FROM python:3.11-slim AS runtime

# Install only runtime dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy binaries from builder stage
COPY --from=builder /usr/local/go /usr/local/go
COPY --from=builder /usr/bin/node /usr/bin/node
COPY --from=builder /usr/bin/npm /usr/bin/npm

# Set working directory
WORKDIR /analysis

# Set environment variables
ENV PATH="/usr/local/go/bin:$PATH"
ENV PYTHONPATH="/analysis"
ENV PYTHONUNBUFFERED=1

# Install Python security and analysis tools
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
    bandit>=1.7.9 \
    safety>=3.2.7 \
    semgrep>=1.45.0 \
    tree-sitter>=0.21.3 \
    GitPython>=3.1.44 \
    requests>=2.32.3 \
    lizard>=1.17.10 \
    radon>=6.0.1

# Create analysis user (non-root for security)
RUN useradd -m -s /bin/bash -u 1001 analyzer \
    && mkdir -p /analysis/repo \
    && mkdir -p /analysis/results \
    && mkdir -p /analysis/temp \
    && mkdir -p /analysis/scripts \
    && chown -R analyzer:analyzer /analysis

# Copy requirements and install additional tools as analyzer user
USER analyzer

# Install Node.js security tools in user space
RUN npm install --prefix /analysis audit-ci @npmcli/arborist

# Set resource limits (will be overridden by Docker run)
ENV ANALYSIS_TIMEOUT=300
ENV MAX_MEMORY=512m
ENV MAX_CPU=0.5

# Default command
CMD ["python", "/analysis/scripts/run_analysis.py"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Labels
LABEL maintainer="AAI System <aai@system.local>"
LABEL description="Secure sandbox for GitHub repository analysis"
LABEL version="1.0.0"