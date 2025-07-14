# 🤖 GenAI Meeting Preparation Agents

A comprehensive multi-agent system for automated meeting preparation, combining real-time research, industry analysis, strategic planning, and executive briefing compilation.

## 📋 Table of Contents

- [Overview](#overview)
- [Agent Architecture](#agent-architecture)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Agent Details](#agent-details)
- [API Integrations](#api-integrations)
- [Troubleshooting](#troubleshooting)
- [Development](#development)

## 🎯 Overview

This system consists of four specialized AI agents that work together to create comprehensive meeting briefings:

1. **Research Agent** - Gathers participant LinkedIn profiles and professional backgrounds
2. **Industry Analysis Agent** - Analyzes market trends, challenges, and opportunities
3. **Meeting Strategy Agent** - Develops talking points and strategic approaches
4. **Summary Briefing Agent** - Compiles everything into executive briefing documents

## 🏗️ Agent Architecture

```
cli/agents/
├── research_agent/                 # Participant research using Serper API
│   ├── reseach_agent.py           # Main agent code
│   ├── pyproject.toml             # Dependencies
│   └── uv.lock                    # Lock file
├── industry_analysis_agent/        # Industry trends using EXA API
│   ├── industry_analysis_agent.py # Main agent code
│   ├── pyproject.toml             # Dependencies
│   └── uv.lock                    # Lock file
├── meeting_strategy_agent/         # Strategic planning using Google Gemini
│   ├── meeting_stratergy_agent.py # Main agent code
│   ├── pyproject.toml             # Dependencies
│   └── uv.lock                    # Lock file
└── summary_briefing_agent/         # Final compilation using Google Gemini
    ├── summary_briefing_agent.py  # Main agent code
    ├── pyproject.toml             # Dependencies
    └── uv.lock                    # Lock file
```

## ✨ Features

### 🔍 Research Agent
- **LinkedIn Profile Extraction**: Automated LinkedIn URL and profile data retrieval
- **Professional Background Research**: Experience, education, and company information
- **Structured Data Output**: Organized participant profiles with contact information
- **Fallback Mode**: Graceful degradation when APIs are unavailable

### 🏭 Industry Analysis Agent
- **Real-time Market Data**: Live industry trends via EXA API
- **Intelligent Context Detection**: Automatic industry identification from meeting context
- **Comprehensive Analysis**: Trends, challenges, opportunities, and competitive landscape
- **Investment Outlook**: Market positioning and risk assessment
- **Multi-Industry Support**: AI, Cloud Computing, Edge Computing, Technology, Finance, Healthcare

### 🎯 Meeting Strategy Agent
- **AI-Enhanced Strategy**: Google Gemini-powered strategic recommendations
- **Talking Points Generation**: Context-aware discussion topics
- **Question Development**: Strategic questions for productive meetings
- **Objection Handling**: Prepared responses to potential concerns
- **Meeting Flow Optimization**: Timing and structure recommendations

### 📋 Summary Briefing Agent
- **5-Part Executive Briefing**: Professional document compilation
- **Cross-Agent Integration**: Combines all agent outputs seamlessly
- **AI Enhancement**: Google Gemini integration for sophisticated insights
- **Action Items**: Clear next steps and follow-up recommendations
- **Quality Scoring**: Briefing completeness assessment

## 📋 Prerequisites

- **Python 3.12+**
- **GenAI OS Platform** access
- **API Keys** (optional but recommended):
  - Serper API key (for LinkedIn research)
  - EXA API key (for industry analysis)
  - Google API key (for AI enhancements)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/kranthinaremsetti/GenAI_Meeting_Prep.git
cd GenAI_Meeting_Prep/cli
```

### 2. Install Dependencies
```bash
# Install main CLI dependencies
pip install -r requirements.txt

# Or use uv (recommended)
uv sync
```

### 3. Set Up Virtual Environments (Optional)
Each agent can have its own virtual environment:
```bash
cd agents/research_agent
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .

# Repeat for other agents...
```

## ⚙️ Configuration

### 1. Environment Variables
Create a `.env` file in the project root:

```env
# GenAI Session (Required)
JWT_TOKEN=your_genai_jwt_token

# API Keys (Optional but recommended)
SERPER_API_KEY=your_serper_api_key
EXA_API_KEY=your_exa_api_key
GOOGLE_API_KEY=your_google_api_key
```

### 2. API Key Setup

#### Serper API (LinkedIn Research)
1. Visit [serper.dev](https://serper.dev)
2. Sign up and get your API key
3. Add to `.env` file

#### EXA API (Industry Analysis)
1. Visit [exa.ai](https://exa.ai)
2. Create account and get API key
3. Add to `.env` file

#### Google API (AI Enhancement)
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create API key for Gemini
3. Add to `.env` file

## 🎮 Usage

### Method 1: CLI Command
```bash
# Start all agents
python cli.py run_agents

# Register individual agents (if needed)
python cli.py register_agent --name "Research Agent" --description "LinkedIn research agent"
```

### Method 2: Direct Function Calls
```python
# In GenAI OS chat interface
research_meeting_participants(
    participants="John Doe, Jane Smith",
    meeting_context="Strategic AI investments discussion"
)

analyze_meeting_industry_trends(
    participants="John Doe, Jane Smith", 
    meeting_context="AI investments in cloud infrastructure"
)

develop_meeting_strategy(
    meeting_context="AI investment meeting",
    meeting_objective="Identify partnership opportunities"
)

compile_meeting_briefing(
    meeting_context="AI investment discussion",
    meeting_objective="Partnership opportunities",
    research_findings="...",
    industry_analysis="...",
    meeting_strategy="..."
)
```

### Method 3: Natural Language Prompt
```
Please use my meeting preparation agents to create a comprehensive briefing:

Participants: Kranthi Naremsetti, Gnana Saketh Periyala, Veda Priya Rapeti
Meeting Context: Strategic AI investments in cloud infrastructure, LLM integration, and edge computing
Meeting Objective: Identify partnership opportunities and create investment pitch

Please call:
- research_meeting_participants for LinkedIn research
- analyze_meeting_industry_trends for industry analysis  
- develop_meeting_strategy for talking points
- compile_meeting_briefing for final document
```

## 🔧 Agent Details

### Research Agent (`research_agent.py`)

**Function**: `research_meeting_participants(participants, meeting_context)`

**Input**:
```python
participants = "Kranthi Naremsetti, Gnana Saketh Periyala"
meeting_context = "AI investment strategy meeting"
```

**Output**:
```json
{
    "research_findings": [
        {
            "name": "Kranthi Naremsetti",
            "linkedin_url": "https://linkedin.com/in/kranthi-naremsetti",
            "linkedin_profile": {
                "url": "https://linkedin.com/in/kranthi-naremsetti",
                "title": "Profile Title",
                "snippet": "Professional summary",
                "profile_summary": "Complete profile info"
            },
            "experience": ["Experience details..."],
            "education": ["Education background..."],
            "company_info": "Company information"
        }
    ],
    "recommendations": ["Meeting preparation suggestions..."]
}
```

### Industry Analysis Agent (`industry_analysis_agent.py`)

**Function**: `analyze_meeting_industry_trends(participants, meeting_context)`

**Detected Industries**: AI, Cloud Computing, Edge Computing, Technology, Investment Banking, Healthcare, Financial Services

**Output**:
```json
{
    "industry_analyses": {
        "Artificial Intelligence": {
            "current_trends": ["AI trends..."],
            "market_challenges": ["Challenges..."],
            "growth_opportunities": ["Opportunities..."],
            "competitive_landscape": ["Competitors..."],
            "investment_outlook": "Market outlook",
            "risk_factors": ["Risk factors..."]
        }
    },
    "cross_industry_insights": ["Insights..."],
    "meeting_specific_recommendations": {
        "talking_points": ["Discussion topics..."],
        "questions_to_ask": ["Strategic questions..."]
    }
}
```

### Meeting Strategy Agent (`meeting_stratergy_agent.py`)

**Function**: `develop_meeting_strategy(meeting_context, meeting_objective, research_data, industry_analysis)`

**Output**:
```json
{
    "strategy_components": {
        "talking_points": ["Strategic discussion points..."],
        "strategic_questions": ["Questions to ask..."],
        "conversation_starters": ["Ice breakers..."],
        "value_propositions": ["Value statements..."],
        "potential_objections": [
            {
                "objection": "Timeline concerns",
                "response": "Suggested response..."
            }
        ]
    },
    "meeting_flow_suggestions": ["Meeting structure..."],
    "contingency_plans": {"scenario": ["backup plans..."]}
}
```

### Summary Briefing Agent (`summary_briefing_agent.py`)

**Function**: `compile_meeting_briefing(meeting_context, meeting_objective, ...)`

**Output**: Complete 5-part executive briefing with:
- Executive Summary
- Participant Profiles
- Industry Analysis
- Strategic Talking Points
- Recommendations & Action Items

## 🔌 API Integrations

### Serper API (Google Search)
- **Purpose**: LinkedIn profile and professional background research
- **Rate Limits**: Check [serper.dev](https://serper.dev) pricing
- **Fallback**: Structured placeholder data when unavailable

### EXA API (Semantic Search)
- **Purpose**: Real-time industry trends and market analysis
- **Features**: Neural search, auto-prompting, content extraction
- **Fallback**: Generic industry insights when unavailable

### Google Gemini API
- **Purpose**: AI-enhanced strategic insights and recommendations
- **Model**: `gemini-pro`
- **Fallback**: Standard strategic framework when unavailable

## 🛠️ Troubleshooting

### Common Issues

#### 1. Agents Not Starting
```bash
# Check virtual environments
ls -la agents/*/venv  # Should exist for each agent

# Verify dependencies
cd agents/research_agent
pip list | grep genai-protocol
```

#### 2. API Errors
```bash
# Verify environment variables
echo $SERPER_API_KEY
echo $EXA_API_KEY
echo $GOOGLE_API_KEY

# Check API key validity
curl -H "X-API-KEY: $SERPER_API_KEY" https://google.serper.dev/search
```

#### 3. Import Errors
```bash
# Reinstall dependencies
cd agents/research_agent
pip install -e .
```

#### 4. GenAI Session Issues
```bash
# Verify JWT token
echo $JWT_TOKEN

# Check GenAI platform connectivity
python -c "from genai_session.session import GenAISession; print('OK')"
```


## 🚧 Development

### Adding New Agents

1. **Create Agent Folder**:
```bash
mkdir agents/new_agent
cd agents/new_agent
```

2. **Create pyproject.toml**:
```toml
[project]
name = "new-agent"
version = "0.1.0"
description = "Description of new agent"
requires-python = ">=3.12"
dependencies = [
    "genai-protocol>=1.0.9",
    "python-dotenv>=1.1.0",
]
```

3. **Create Agent Code**:
```python
import asyncio
from genai_session.session import GenAISession

session = GenAISession(jwt_token=JWT_TOKEN)

@session.bind(
    name="new_agent_function",
    description="Description of what this agent does"
)
async def new_agent_function(agent_context, param1, param2):
    # Agent logic here
    return {"result": "data"}

if __name__ == "__main__":
    asyncio.run(session.process_events())
```

### Testing Agents

```bash
# Test individual agents
cd agents/research_agent
python reseach_agent.py

# Test with sample data
python -c "
import asyncio
from reseach_agent import research_meeting_participants
# Add test code here
"
```

### Code Quality

```bash
# Format code
black agents/
isort agents/

# Type checking
mypy agents/

# Linting
pylint agents/
```

## 📚 Additional Resources

- [GenAI Protocol Documentation](https://docs.genai.com)
- [Serper API Documentation](https://serper.dev/docs)
- [EXA API Documentation](https://docs.exa.ai)
- [Google Gemini API Documentation](https://ai.google.dev)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-agent`
3. Commit changes: `git commit -am 'Add new agent'`
4. Push to branch: `git push origin feature/new-agent`
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🙋‍♂️ Support

For support and questions:
- Create an issue on GitHub
- Documentation: (https://www.notion.so/AI-Prep-Meeting-230d9ca16ad080efa788c1974fe20e45?source=copy_link)

---

## 🎯 Quick Start Example

```bash
# 1. Setup environment
export JWT_TOKEN="your_jwt_token"
export SERPER_API_KEY="your_serper_key"
export EXA_API_KEY="your_exa_key"
export GOOGLE_API_KEY="your_google_key"

# 2. Start agents
cd cli
python cli.py run_agents

# 3. Use in GenAI OS chat
# "Please create a meeting briefing for: [your meeting details]"
```

**Your comprehensive meeting preparation system is ready! 🚀**
