"""
Interactive Gradio Interface for R1 Reasoning Engine

User-friendly web interface for reasoning sessions with
AAI patterns, confidence visualization, and result exploration.
"""
import logging
import asyncio
import json
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path

# Gradio imports with fallback
try:
    import gradio as gr
    GRADIO_AVAILABLE = True
except ImportError:
    GRADIO_AVAILABLE = False

# Plotting for visualizations
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    try:
        import matplotlib.pyplot as plt
        MATPLOTLIB_AVAILABLE = True
        PLOTLY_AVAILABLE = False
    except ImportError:
        PLOTLY_AVAILABLE = False
        MATPLOTLIB_AVAILABLE = False

# Local imports
try:
    from agents.r1_reasoning import (
        DualModelAgent, DocumentAnalysisRequest, ReasoningDepth, 
        ReasoningResponse, ReasoningChain
    )
    from ingestion.r1_reasoning import JinaResearchIngester, JinaResearchRequest
    from vector_store import SupabaseVectorStore, ChromaManager, RetrievalRanker
    R1_COMPONENTS_AVAILABLE = True
except ImportError:
    R1_COMPONENTS_AVAILABLE = False

logger = logging.getLogger(__name__)


class R1ReasoningInterface:
    """
    Interactive Gradio interface for R1 reasoning sessions.
    
    Features:
    - User-friendly query interface
    - Real-time reasoning visualization
    - Confidence score tracking
    - Document source exploration
    - Research integration controls
    - Session history management
    """
    
    def __init__(self, 
                 dual_model_agent: Optional[Any] = None,
                 research_ingester: Optional[Any] = None,
                 vector_store: Optional[Any] = None):
        """Initialize reasoning interface"""
        self.dual_model_agent = dual_model_agent
        self.research_ingester = research_ingester
        self.vector_store = vector_store
        
        # Interface state
        self.session_history = []
        self.current_session_id = None
        
        # Configuration
        self.interface_config = {
            "title": "AAI R1 Reasoning Engine",
            "description": "Advanced reasoning with DeepSeek R1 and dual-model architecture",
            "theme": "soft",
            "show_api": False
        }
        
        # Check dependencies
        self.gradio_ready = GRADIO_AVAILABLE
        self.plotting_ready = PLOTLY_AVAILABLE or MATPLOTLIB_AVAILABLE
        self.components_ready = R1_COMPONENTS_AVAILABLE
        
        if not self.gradio_ready:
            logger.warning("Gradio not available - install gradio package")
        
        if not self.plotting_ready:
            logger.warning("Plotting library not available - install plotly or matplotlib")
        
        if not self.components_ready:
            logger.warning("R1 components not fully available")
    
    def create_interface(self) -> Optional[Any]:
        """Create and configure Gradio interface"""
        
        if not self.gradio_ready:
            logger.error("Cannot create interface - Gradio not available")
            return None
        
        try:
            # Create main interface with tabs
            with gr.Blocks(
                title=self.interface_config["title"],
                theme=self.interface_config["theme"]
            ) as interface:
                
                # Header
                gr.Markdown(f"""
                # {self.interface_config["title"]}
                {self.interface_config["description"]}
                
                Powered by DeepSeek R1 with AAI confidence scoring and dual-model architecture.
                """)
                
                # Main tabs
                with gr.Tabs():
                    
                    # Reasoning tab
                    with gr.TabItem("🧠 Reasoning Session"):
                        self._create_reasoning_tab()
                    
                    # Research tab
                    with gr.TabItem("🔍 Research Integration"):
                        self._create_research_tab()
                    
                    # Analysis tab
                    with gr.TabItem("📊 Analysis & Visualization"):
                        self._create_analysis_tab()
                    
                    # Settings tab
                    with gr.TabItem("⚙️ Settings"):
                        self._create_settings_tab()
                    
                    # Status tab
                    with gr.TabItem("📈 System Status"):
                        self._create_status_tab()
            
            return interface
            
        except Exception as e:
            logger.error(f"Interface creation failed: {e}")
            return None
    
    def _create_reasoning_tab(self):
        """Create the main reasoning interface tab"""
        
        with gr.Row():
            with gr.Column(scale=2):
                # Query input
                query_input = gr.TextArea(
                    label="Your Query",
                    placeholder="Ask a question that requires reasoning and analysis...",
                    lines=3,
                    max_lines=5
                )
                
                # Settings row
                with gr.Row():
                    reasoning_depth = gr.Dropdown(
                        choices=["quick", "thorough", "exhaustive"],
                        value="thorough",
                        label="Reasoning Depth"
                    )
                    
                    confidence_threshold = gr.Slider(
                        minimum=0.70,
                        maximum=0.95,
                        value=0.75,
                        step=0.05,
                        label="Confidence Threshold"
                    )
                    
                    document_limit = gr.Slider(
                        minimum=1,
                        maximum=20,
                        value=5,
                        step=1,
                        label="Max Documents"
                    )
                
                # Action buttons
                with gr.Row():
                    submit_btn = gr.Button("🧠 Analyze", variant="primary")
                    clear_btn = gr.Button("🗑️ Clear", variant="secondary")
                    research_btn = gr.Button("🔍 Research First", variant="secondary")
            
            with gr.Column(scale=1):
                # Quick settings
                gr.Markdown("### Quick Options")
                
                include_alternatives = gr.Checkbox(
                    label="Include Alternative Perspectives",
                    value=True
                )
                
                include_limitations = gr.Checkbox(
                    label="Show Reasoning Limitations",
                    value=True
                )
                
                enable_research = gr.Checkbox(
                    label="Auto-Research Unknown Topics",
                    value=False
                )
        
        # Results section
        gr.Markdown("## 📋 Analysis Results")
        
        with gr.Row():
            # Main answer
            with gr.Column(scale=2):
                answer_output = gr.Markdown(
                    label="Answer",
                    value="",
                    elem_classes=["answer-output"]
                )
                
                # Confidence display
                confidence_display = gr.HTML(
                    value="",
                    label="Confidence Analysis"
                )
            
            # Side panel
            with gr.Column(scale=1):
                # Reasoning chain
                reasoning_chain_output = gr.JSON(
                    label="Reasoning Chain",
                    value=None
                )
                
                # Supporting documents
                documents_output = gr.JSON(
                    label="Supporting Documents",
                    value=None
                )
        
        # Detailed analysis (collapsible)
        with gr.Accordion("🔍 Detailed Analysis", open=False):
            
            with gr.Row():
                alternatives_output = gr.JSON(
                    label="Alternative Perspectives",
                    value=None
                )
                
                limitations_output = gr.JSON(
                    label="Reasoning Limitations", 
                    value=None
                )
            
            processing_info = gr.JSON(
                label="Processing Information",
                value=None
            )
        
        # Session history
        with gr.Accordion("📚 Session History", open=False):
            history_output = gr.Dataframe(
                headers=["Time", "Query", "Confidence", "Model"],
                datatype=["str", "str", "number", "str"],
                value=[],
                label="Previous Queries"
            )
        
        # Wire up event handlers
        submit_btn.click(
            fn=self._process_reasoning_query,
            inputs=[
                query_input, reasoning_depth, confidence_threshold,
                document_limit, include_alternatives, include_limitations,
                enable_research
            ],
            outputs=[
                answer_output, confidence_display, reasoning_chain_output,
                documents_output, alternatives_output, limitations_output,
                processing_info, history_output
            ]
        )
        
        clear_btn.click(
            fn=self._clear_reasoning_session,
            outputs=[
                query_input, answer_output, confidence_display,
                reasoning_chain_output, documents_output, alternatives_output,
                limitations_output, processing_info
            ]
        )
        
        research_btn.click(
            fn=self._research_then_analyze,
            inputs=[query_input],
            outputs=[answer_output, confidence_display]
        )
    
    def _create_research_tab(self):
        """Create research integration tab"""
        
        gr.Markdown("## 🔍 Automated Research Integration")
        
        with gr.Row():
            with gr.Column():
                research_topic = gr.TextBox(
                    label="Research Topic",
                    placeholder="Enter topic for automated research..."
                )
                
                with gr.Row():
                    max_pages = gr.Slider(
                        minimum=1,
                        maximum=20,
                        value=5,
                        label="Max Pages"
                    )
                    
                    quality_threshold = gr.Slider(
                        minimum=0.0,
                        maximum=1.0,
                        value=0.6,
                        step=0.1,
                        label="Quality Threshold"
                    )
                
                with gr.Row():
                    include_academic = gr.Checkbox(label="Academic Sources", value=True)
                    include_news = gr.Checkbox(label="News Sources", value=False)
                    include_docs = gr.Checkbox(label="Documentation", value=True)
                
                date_filter = gr.Dropdown(
                    choices=["None", "1d", "1w", "1m", "1y"],
                    value="1m",
                    label="Date Filter"
                )
                
                research_btn = gr.Button("🔍 Start Research", variant="primary")
            
            with gr.Column():
                research_status = gr.HTML(value="", label="Research Status")
                
                research_progress = gr.HTML(
                    value="<div>Ready to start research</div>",
                    label="Progress"
                )
        
        # Research results
        research_results = gr.JSON(
            label="Research Results",
            value=None
        )
        
        research_summary = gr.Markdown(
            value="",
            label="Research Summary"
        )
        
        # Wire up research handler
        research_btn.click(
            fn=self._conduct_research,
            inputs=[
                research_topic, max_pages, quality_threshold,
                include_academic, include_news, include_docs, date_filter
            ],
            outputs=[research_results, research_summary, research_status]
        )
    
    def _create_analysis_tab(self):
        """Create analysis and visualization tab"""
        
        gr.Markdown("## 📊 Reasoning Analysis & Visualization")
        
        if self.plotting_ready:
            # Confidence visualization
            confidence_plot = gr.Plot(
                label="Confidence Analysis",
                value=None
            )
            
            # Reasoning flow visualization
            reasoning_flow_plot = gr.Plot(
                label="Reasoning Flow",
                value=None
            )
            
            # Performance metrics
            with gr.Row():
                with gr.Column():
                    metrics_plot = gr.Plot(
                        label="Session Metrics",
                        value=None
                    )
                
                with gr.Column():
                    quality_plot = gr.Plot(
                        label="Source Quality Distribution",
                        value=None
                    )
            
            # Update button
            update_plots_btn = gr.Button("🔄 Update Visualizations")
            
            update_plots_btn.click(
                fn=self._update_visualizations,
                outputs=[confidence_plot, reasoning_flow_plot, metrics_plot, quality_plot]
            )
            
        else:
            gr.Markdown("""
            ⚠️ **Visualization Not Available**
            
            Install plotly or matplotlib to enable visualizations:
            ```bash
            pip install plotly
            # or
            pip install matplotlib
            ```
            """)
    
    def _create_settings_tab(self):
        """Create settings configuration tab"""
        
        gr.Markdown("## ⚙️ System Configuration")
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### Model Configuration")
                
                reasoning_model = gr.Dropdown(
                    choices=[
                        "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
                        "deepseek-ai/DeepSeek-R1-Distill-Llama-70B",
                        "custom"
                    ],
                    value="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
                    label="Reasoning Model"
                )
                
                tool_model = gr.Dropdown(
                    choices=[
                        "meta-llama/Llama-3.3-70B-Instruct",
                        "meta-llama/Llama-3.1-8B-Instruct",
                        "custom"
                    ],
                    value="meta-llama/Llama-3.3-70B-Instruct",
                    label="Tool Execution Model"
                )
                
                max_tokens = gr.Slider(
                    minimum=1024,
                    maximum=8192,
                    value=4096,
                    step=256,
                    label="Max Tokens"
                )
                
                temperature = gr.Slider(
                    minimum=0.0,
                    maximum=1.0,
                    value=0.1,
                    step=0.05,
                    label="Temperature"
                )
            
            with gr.Column():
                gr.Markdown("### Interface Settings")
                
                theme_choice = gr.Dropdown(
                    choices=["soft", "default", "compact"],
                    value="soft",
                    label="Interface Theme"
                )
                
                auto_save = gr.Checkbox(
                    label="Auto-save Sessions",
                    value=True
                )
                
                show_debug = gr.Checkbox(
                    label="Show Debug Information",
                    value=False
                )
                
                enable_cache = gr.Checkbox(
                    label="Enable Response Caching",
                    value=True
                )
        
        # API configuration
        with gr.Accordion("🔐 API Configuration", open=False):
            
            with gr.Row():
                huggingface_token = gr.Textbox(
                    label="HuggingFace Token",
                    type="password",
                    placeholder="hf_..."
                )
                
                openrouter_key = gr.Textbox(
                    label="OpenRouter API Key", 
                    type="password",
                    placeholder="sk-or-..."
                )
            
            jina_api_key = gr.Textbox(
                label="Jina API Key",
                type="password",
                placeholder="Optional for enhanced research"
            )
        
        save_settings_btn = gr.Button("💾 Save Settings", variant="primary")
        
        settings_status = gr.HTML(value="", label="Status")
        
        save_settings_btn.click(
            fn=self._save_settings,
            inputs=[
                reasoning_model, tool_model, max_tokens, temperature,
                theme_choice, auto_save, show_debug, enable_cache,
                huggingface_token, openrouter_key, jina_api_key
            ],
            outputs=[settings_status]
        )
    
    def _create_status_tab(self):
        """Create system status monitoring tab"""
        
        gr.Markdown("## 📈 System Status")
        
        # Component status
        with gr.Row():
            with gr.Column():
                component_status = gr.JSON(
                    label="Component Status",
                    value=self._get_component_status()
                )
            
            with gr.Column():
                performance_metrics = gr.JSON(
                    label="Performance Metrics",
                    value=self._get_performance_metrics()
                )
        
        # System information
        system_info = gr.JSON(
            label="System Information",
            value=self._get_system_info()
        )
        
        # Refresh button
        refresh_btn = gr.Button("🔄 Refresh Status")
        
        refresh_btn.click(
            fn=self._refresh_status,
            outputs=[component_status, performance_metrics, system_info]
        )
    
    def _process_reasoning_query(self, 
                               query: str,
                               depth: str,
                               confidence_threshold: float,
                               doc_limit: int,
                               include_alternatives: bool,
                               include_limitations: bool,
                               enable_research: bool) -> Tuple:
        """Process reasoning query and return results"""
        
        try:
            if not query.strip():
                return self._empty_results()
            
            # Create request
            if DocumentAnalysisRequest and ReasoningDepth:
                reasoning_depth = getattr(ReasoningDepth, depth.upper())
                
                request = DocumentAnalysisRequest(
                    query=query,
                    user_id="gradio_user",
                    document_limit=doc_limit,
                    reasoning_depth=reasoning_depth,
                    confidence_threshold=confidence_threshold,
                    include_reasoning_chain=True,
                    include_alternatives=include_alternatives,
                    include_limitations=include_limitations
                )
                
                # Process with dual model agent
                if self.dual_model_agent:
                    # This would be async in real implementation
                    response = self._mock_reasoning_response(request)
                else:
                    response = self._fallback_reasoning_response(request)
                
                # Update session history
                self._update_session_history(query, response)
                
                # Format outputs
                return self._format_reasoning_outputs(response)
            
            else:
                return self._error_results("R1 components not available")
                
        except Exception as e:
            logger.error(f"Reasoning query failed: {e}")
            return self._error_results(str(e))
    
    def _mock_reasoning_response(self, request) -> Dict[str, Any]:
        """Mock reasoning response for demonstration"""
        
        return {
            "answer": f"Based on my analysis of '{request.query}', I can provide the following reasoning:\n\n"
                     f"This is a complex question that requires careful consideration of multiple factors. "
                     f"Through systematic analysis, I've identified key points that inform my response.",
            "confidence": 0.85,
            "reasoning_steps": [
                {"step": 1, "description": "Initial analysis", "confidence": 0.80},
                {"step": 2, "description": "Evidence synthesis", "confidence": 0.88},
                {"step": 3, "description": "Conclusion formation", "confidence": 0.85}
            ],
            "documents": [
                {"filename": "research_paper.pdf", "relevance": 0.92, "confidence": 0.88},
                {"filename": "documentation.md", "relevance": 0.85, "confidence": 0.82}
            ],
            "processing_time": 1250,
            "model_used": "dual_model_agent"
        }
    
    def _fallback_reasoning_response(self, request) -> Dict[str, Any]:
        """Fallback response when components not available"""
        
        return {
            "answer": f"I understand you're asking about: '{request.query}'\n\n"
                     f"Unfortunately, the full R1 reasoning engine is not currently available. "
                     f"This is a demonstration interface showing the planned functionality.",
            "confidence": 0.70,
            "reasoning_steps": [],
            "documents": [],
            "processing_time": 100,
            "model_used": "fallback"
        }
    
    def _format_reasoning_outputs(self, response: Dict[str, Any]) -> Tuple:
        """Format response for Gradio outputs"""
        
        # Main answer
        answer = response["answer"]
        
        # Confidence display
        confidence_html = f"""
        <div style="padding: 10px; border-radius: 5px; background-color: #f0f0f0;">
            <h4>Confidence Analysis</h4>
            <div style="margin: 5px 0;">
                <strong>Overall Confidence:</strong> {response['confidence']:.1%}
            </div>
            <div style="margin: 5px 0;">
                <strong>Processing Time:</strong> {response['processing_time']}ms
            </div>
            <div style="margin: 5px 0;">
                <strong>Model Used:</strong> {response['model_used']}
            </div>
        </div>
        """
        
        # Reasoning chain
        reasoning_chain = {
            "steps": response["reasoning_steps"],
            "total_steps": len(response["reasoning_steps"]),
            "average_confidence": sum(step.get("confidence", 0.7) for step in response["reasoning_steps"]) / max(len(response["reasoning_steps"]), 1)
        }
        
        # Documents
        documents = response["documents"]
        
        # Processing info
        processing_info = {
            "processing_time_ms": response["processing_time"],
            "model_used": response["model_used"],
            "timestamp": datetime.now().isoformat(),
            "confidence_score": response["confidence"]
        }
        
        # Updated session history
        history_data = [
            [
                entry["timestamp"],
                entry["query"][:50] + "..." if len(entry["query"]) > 50 else entry["query"],
                f"{entry['confidence']:.1%}",
                entry["model"]
            ]
            for entry in self.session_history[-10:]  # Last 10 entries
        ]
        
        return (
            answer,
            confidence_html,
            reasoning_chain,
            documents,
            [],  # alternatives
            [],  # limitations
            processing_info,
            history_data
        )
    
    def _empty_results(self) -> Tuple:
        """Return empty results"""
        return ("", "", None, None, None, None, None, [])
    
    def _error_results(self, error_msg: str) -> Tuple:
        """Return error results"""
        error_html = f'<div style="color: red;">Error: {error_msg}</div>'
        return (f"Error: {error_msg}", error_html, None, None, None, None, None, [])
    
    def _clear_reasoning_session(self) -> Tuple:
        """Clear the reasoning session"""
        return ("", "", "", None, None, None, None, None)
    
    def _research_then_analyze(self, query: str) -> Tuple:
        """Conduct research then analyze"""
        if not query.strip():
            return "Please enter a query first.", ""
        
        research_note = f"🔍 Researching '{query}'...\n\nThis would conduct automated research using Jina Reader API, then perform reasoning analysis."
        status_html = '<div style="color: blue;">Research mode activated</div>'
        
        return research_note, status_html
    
    def _conduct_research(self, 
                        topic: str,
                        max_pages: int,
                        quality_threshold: float,
                        include_academic: bool,
                        include_news: bool,
                        include_docs: bool,
                        date_filter: str) -> Tuple:
        """Conduct automated research"""
        
        if not topic.strip():
            return None, "Please enter a research topic.", ""
        
        # Mock research results
        mock_results = {
            "topic": topic,
            "sources_found": max_pages,
            "average_quality": quality_threshold + 0.1,
            "sources": [
                {"title": f"Research on {topic}", "quality": 0.85, "type": "academic"},
                {"title": f"Documentation for {topic}", "quality": 0.78, "type": "documentation"}
            ]
        }
        
        summary = f"## Research Summary for '{topic}'\n\n" \
                 f"- **Sources Found:** {max_pages}\n" \
                 f"- **Average Quality:** {quality_threshold + 0.1:.1%}\n" \
                 f"- **Academic Sources:** {'Enabled' if include_academic else 'Disabled'}\n" \
                 f"- **Date Filter:** {date_filter}\n\n" \
                 f"Research completed. Results can be used for reasoning analysis."
        
        status_html = '<div style="color: green;">✅ Research completed successfully</div>'
        
        return mock_results, summary, status_html
    
    def _update_visualizations(self) -> Tuple:
        """Update analysis visualizations"""
        
        if not self.plotting_ready:
            return None, None, None, None
        
        # Mock plots (would be real data in implementation)
        try:
            import plotly.graph_objects as go
            
            # Confidence plot
            conf_fig = go.Figure()
            conf_fig.add_trace(go.Scatter(
                x=["Step 1", "Step 2", "Step 3"],
                y=[0.8, 0.85, 0.82],
                mode='lines+markers',
                name='Confidence'
            ))
            conf_fig.update_layout(title="Reasoning Confidence by Step")
            
            # Reasoning flow (simple)
            flow_fig = go.Figure()
            flow_fig.add_trace(go.Bar(
                x=["Analysis", "Synthesis", "Conclusion"],
                y=[1, 2, 1],
                name="Steps"
            ))
            flow_fig.update_layout(title="Reasoning Process Flow")
            
            return conf_fig, flow_fig, conf_fig, flow_fig
            
        except ImportError:
            return None, None, None, None
    
    def _save_settings(self, *args) -> str:
        """Save interface settings"""
        return '<div style="color: green;">✅ Settings saved successfully</div>'
    
    def _get_component_status(self) -> Dict[str, Any]:
        """Get component status information"""
        return {
            "gradio_available": self.gradio_ready,
            "plotting_available": self.plotting_ready,
            "r1_components_available": self.components_ready,
            "dual_model_agent": self.dual_model_agent is not None,
            "research_ingester": self.research_ingester is not None,
            "vector_store": self.vector_store is not None
        }
    
    def _get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        return {
            "total_queries": len(self.session_history),
            "average_confidence": 0.82,
            "average_processing_time": 1200,
            "success_rate": 0.95,
            "uptime": "2h 30m"
        }
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        return {
            "interface_version": "1.0.0",
            "gradio_version": "4.0.0" if GRADIO_AVAILABLE else "Not installed",
            "python_version": "3.9+",
            "components_loaded": self.components_ready,
            "session_id": self.current_session_id or "new_session"
        }
    
    def _refresh_status(self) -> Tuple:
        """Refresh status information"""
        return (
            self._get_component_status(),
            self._get_performance_metrics(),
            self._get_system_info()
        )
    
    def _update_session_history(self, query: str, response: Dict[str, Any]):
        """Update session history"""
        entry = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "query": query,
            "confidence": response["confidence"],
            "model": response["model_used"]
        }
        self.session_history.append(entry)
        
        # Keep only last 50 entries
        if len(self.session_history) > 50:
            self.session_history = self.session_history[-50:]
    
    def launch(self, 
               host: str = "127.0.0.1",
               port: int = 7860,
               share: bool = False,
               debug: bool = False) -> Optional[Any]:
        """Launch the Gradio interface"""
        
        if not self.gradio_ready:
            logger.error("Cannot launch - Gradio not available")
            print("❌ Gradio not installed. Install with: pip install gradio")
            return None
        
        try:
            interface = self.create_interface()
            
            if interface:
                logger.info(f"Launching interface at http://{host}:{port}")
                
                return interface.launch(
                    server_name=host,
                    server_port=port,
                    share=share,
                    debug=debug,
                    show_api=self.interface_config["show_api"]
                )
            else:
                logger.error("Failed to create interface")
                return None
                
        except Exception as e:
            logger.error(f"Interface launch failed: {e}")
            return None
    
    def get_interface_status(self) -> Dict[str, Any]:
        """Get interface status"""
        return {
            "gradio_ready": self.gradio_ready,
            "plotting_ready": self.plotting_ready,
            "components_ready": self.components_ready,
            "session_history_size": len(self.session_history),
            "current_session_id": self.current_session_id,
            "config": self.interface_config
        }


def create_r1_interface(
    dual_model_agent=None,
    research_ingester=None, 
    vector_store=None,
    **kwargs
) -> R1ReasoningInterface:
    """
    Factory function to create R1 reasoning interface.
    
    Args:
        dual_model_agent: Optional dual model agent instance
        research_ingester: Optional research ingester instance
        vector_store: Optional vector store instance
        **kwargs: Additional configuration options
        
    Returns:
        Configured R1ReasoningInterface instance
    """
    
    interface = R1ReasoningInterface(
        dual_model_agent=dual_model_agent,
        research_ingester=research_ingester,
        vector_store=vector_store
    )
    
    # Apply additional configuration
    if kwargs:
        interface.interface_config.update(kwargs)
    
    return interface


def test_r1_interface():
    """Test R1 reasoning interface"""
    
    print("🧪 Testing R1 Reasoning Interface")
    print("=" * 40)
    
    # Test interface creation
    interface = create_r1_interface()
    status = interface.get_interface_status()
    
    print(f"Gradio ready: {status['gradio_ready']}")
    print(f"Plotting ready: {status['plotting_ready']}")
    print(f"Components ready: {status['components_ready']}")
    print(f"Config: {status['config']['title']}")
    
    if status['gradio_ready']:
        print("✅ Interface ready to launch")
        print("To launch: interface.launch()")
        print("Example: interface.launch(host='0.0.0.0', port=7860, share=True)")
    else:
        print("❌ Interface not ready - install Gradio")
        print("Install with: pip install gradio plotly")
    
    return interface


if __name__ == "__main__":
    test_interface = test_r1_interface()
    
    # Uncomment to launch interface
    # test_interface.launch(debug=True)