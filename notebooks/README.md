# PodCast Agent - Research Notebooks

This directory contains Jupyter notebooks used for prototyping and validating the core AI components of the PodCast Agent before production implementation.

## 📋 Notebook Overview

### 1. `01_firecrawl_exploration.ipynb`
**Purpose**: Test FireCrawl API for web content extraction
- ✅ URL scraping to markdown conversion
- ✅ Content quality validation
- ✅ API integration patterns
- **Key Finding**: Reliable markdown extraction for podcast content

### 2. `02_pdf_extraction_testing.ipynb`
**Purpose**: Compare PDF extraction libraries (PyPDF vs PyMuPDF vs pdfplumber)
- ✅ Performance benchmarking
- ✅ Text quality comparison
- **Key Finding**: PyMuPDF is 33x faster than alternatives
- **Production Choice**: PyMuPDF for `app/core/ai_core/tools/pdf_parser.py`

### 3. `03_gemini_tts.ipynb`
**Purpose**: Validate Gemini 2.5 Flash TTS for multi-speaker audio generation
- ✅ Single speaker audio generation
- ✅ Multi-speaker conversation synthesis
- ✅ Audio quality validation
- **Key Finding**: Native multi-speaker support eliminates need for external TTS

### 4. `04_dspy_prompt_engineering.ipynb`
**Purpose**: Optimize podcast script generation using DSpy
- ✅ Signature definition for context-to-script conversion
- ✅ Quality metrics (coherence, engagement, structure)
- ✅ Few-shot optimization with BootstrapFewShot
- **Key Finding**: 15% quality improvement with optimized prompts

### 5. `05_langGraph_agent.ipynb`
**Purpose**: Complete end-to-end pipeline orchestration with LangGraph
- ✅ State machine design for podcast generation
- ✅ Parallel source processing
- ✅ Error handling and checkpointing
- ✅ Full pipeline validation
- **Key Finding**: State-driven architecture enables resumable workflows

## 🚀 Quick Setup

1. **Environment Setup**:
   ```bash
   # Run the setup script
   .\setup_notebooks_env.ps1
   
   # Activate environment
   .\.venv-notebooks\Scripts\activate
   
   # Start Jupyter
   jupyter lab
   ```

2. **Environment Variables**:
   - Copy `.env.example` to `.env`
   - Add your API keys:
     - `GEMINI_API_KEY`
     - `FIRECRAWL_API_KEY`

## 📊 Key Performance Metrics

| Component | Tool | Performance | Quality Score |
|-----------|------|-------------|---------------|
| **URL Processing** | FireCrawl | ~3s per page | ⭐⭐⭐⭐⭐ |
| **PDF Processing** | PyMuPDF | ~80ms per doc | ⭐⭐⭐⭐⭐ |
| **Script Generation** | DSpy + Gemini | ~5s | ⭐⭐⭐⭐⭐ |
| **Audio Generation** | Gemini TTS | ~20s per 2min | ⭐⭐⭐⭐⭐ |

## 🏗️ Production Integration

These notebooks directly informed the backend architecture:

```
notebooks/01_firecrawl_exploration.ipynb → agent/app/core/ai_core/tools/url_crawler.py
notebooks/02_pdf_extraction_testing.ipynb → agent/app/core/ai_core/tools/pdf_parser.py
notebooks/04_dspy_prompt_engineering.ipynb → agent/app/core/ai_core/prompts/signatures.py
notebooks/05_langGraph_agent.ipynb → agent/app/core/ai_core/graphs/podcast_flow_graph.py
```

## 🔒 Security Notes

- `.env` files are gitignored - never commit API keys
- Generated audio files are excluded (too large for git)
- Virtual environment is gitignored
- Test PDFs and temporary files are excluded

## 📝 Next Steps

1. ✅ Notebook prototyping complete
2. 🔄 **Current**: Service layer implementation
3. ⏳ **Next**: AI Core tools integration
4. ⏳ **Future**: LangGraph production workflow

---

**Status**: ✅ Prototyping Complete - Ready for Production Implementation