
import asyncio
import os
from typing import Any, Annotated

from dotenv import load_dotenv
from genai_session.session import GenAISession
import google.generativeai as genai

load_dotenv()

# Environment variables
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
JWT_TOKEN = os.environ.get("JWT_TOKEN")

# Configure Google Gemini instead of OpenAI
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-pro')
else:
    gemini_model = None

session = GenAISession(
    jwt_token=JWT_TOKEN
)


@session.bind(
    name="develop_meeting_strategy",
    description="Develop talking points, questions, and strategic angles for the meeting based on research and industry analysis."
)
async def develop_meeting_strategy(
    agent_context,
    meeting_context: Annotated[str, "Context or background information about the meeting"],
    meeting_objective: Annotated[str, "Your specific objective for this meeting"],
    research_data: Annotated[str, "Research findings about the participants (optional)"] = "",
    industry_analysis: Annotated[str, "Industry analysis and trends data (optional)"] = "",
) -> dict[str, Any]:
    """
    Meeting Strategy Advisor Agent
    
    Develop talking points, questions, and strategic angles for the meeting.
    Your expertise will guide the development of talking points, insightful questions, 
    and strategic angles to ensure the meeting's objectives are achieved.
    """
    
    agent_context.logger.info("Developing meeting strategy")
    
    try:
        # Generate core strategy components
        strategy_components = await generate_strategy_components(
            meeting_context, meeting_objective, research_data, industry_analysis
        )
        
        # Generate AI-enhanced talking points if Google Gemini is available
        if gemini_model:
            enhanced_strategy = await enhance_strategy_with_ai(
                meeting_context, meeting_objective, strategy_components
            )
            strategy_components.update(enhanced_strategy)
        
        # Create meeting flow and timing suggestions
        meeting_flow = generate_meeting_flow(meeting_context, meeting_objective)
        
        # Generate contingency plans
        contingency_plans = generate_contingency_plans()
        
        # Compile comprehensive strategy report
        report = {
            "meeting_context": meeting_context,
            "meeting_objective": meeting_objective,
            "strategy_components": strategy_components,
            "meeting_flow_suggestions": meeting_flow,
            "key_success_factors": [
                "Active listening and engagement",
                "Clear articulation of value proposition",
                "Addressing concerns proactively",
                "Establishing clear next steps",
                "Building genuine rapport"
            ],
            "contingency_plans": contingency_plans,
            "pre_meeting_checklist": [
                "Review participant backgrounds thoroughly",
                "Practice key talking points",
                "Prepare supporting materials",
                "Anticipate potential objections",
                "Set up meeting logistics"
            ],
            "success_metrics": [
                "Clear understanding of all parties' positions",
                "Agreement on next steps and timeline",
                "Positive rapport established",
                "Objective progress made",
                "Follow-up actions defined"
            ],
            "summary": f"Strategic meeting plan developed for: {meeting_objective}"
        }
        
        agent_context.logger.info("Meeting strategy developed successfully")
        return report
        
    except Exception as e:
        agent_context.logger.error(f"Strategy development failed: {str(e)}")
        return {
            "error": f"Meeting strategy agent encountered an error: {str(e)}",
            "context": meeting_context,
            "objective": meeting_objective
        }


async def generate_strategy_components(context: str, objective: str, research: str, industry: str) -> dict:
    """Generate core strategy components"""
    
    # Generate talking points based on objective and context
    talking_points = [
        f"Opening discussion about {context}",
        f"Alignment on {objective}",
        "Mutual benefits and value proposition",
        "Timeline and implementation discussion",
        "Resource requirements and commitments",
        "Success metrics and measurement",
        "Risk mitigation and contingencies"
    ]
    
    # Generate strategic questions
    strategic_questions = [
        f"How does this align with your current priorities regarding {context}?",
        "What are the key success metrics you'd like to see?",
        "What potential challenges do you foresee?",
        "How can we ensure mutual value creation?",
        "What would an ideal outcome look like for you?",
        "What timeline are you working with?",
        "Who else should be involved in this decision?"
    ]
    
    # Generate conversation starters
    conversation_starters = [
        "I'd love to hear your perspective on the current market situation",
        "What trends are you seeing in your industry?",
        "How has your experience been with similar initiatives?",
        "What's driving your interest in this area?",
        "What challenges are you currently facing?"
    ]
    
    return {
        "talking_points": talking_points,
        "strategic_questions": strategic_questions,
        "conversation_starters": conversation_starters,
        "value_propositions": generate_value_propositions(objective),
        "potential_objections": generate_potential_objections(context, objective),
        "common_ground_areas": identify_common_ground(research, industry)
    }


async def enhance_strategy_with_ai(context: str, objective: str, components: dict) -> dict:
    """Use Google Gemini to enhance strategy components"""
    try:
        prompt = f"""
        Given this meeting context: {context}
        And this objective: {objective}
        
        Please provide:
        1. 3 sophisticated conversation starters
        2. 3 strategic questions that demonstrate industry knowledge
        3. 3 potential objections and how to address them
        
        Format as JSON with keys: advanced_conversation_starters, strategic_industry_questions, objection_responses
        """
        
        response = gemini_model.generate_content(prompt)
        ai_content = response.text
        
        return {
            "ai_enhanced_content": ai_content,
            "ai_generated": True
        }
        
    except Exception as e:
        return {
            "ai_enhanced_content": "AI enhancement not available",
            "ai_generated": False,
            "error": str(e)
        }


def generate_meeting_flow(context: str, objective: str) -> list:
    """Generate suggested meeting flow and timing"""
    return [
        "1. Opening and rapport building (5-10 minutes)",
        "2. Context setting and objective alignment (10-15 minutes)",
        "3. Main discussion and exploration (20-30 minutes)",
        "4. Address concerns and objections (10-15 minutes)",
        "5. Next steps and follow-up (5-10 minutes)"
    ]


def generate_contingency_plans() -> dict:
    """Generate contingency plans for various scenarios"""
    return {
        "if_discussion_stalls": [
            "Use prepared conversation starters",
            "Ask open-ended questions about their challenges",
            "Share relevant industry insights"
        ],
        "if_objections_arise": [
            "Acknowledge concerns respectfully",
            "Ask clarifying questions to understand root issues",
            "Provide evidence-based responses"
        ],
        "if_time_runs_short": [
            "Focus on most critical priorities",
            "Schedule dedicated follow-up meeting",
            "Provide summary of key points"
        ]
    }


def generate_value_propositions(objective: str) -> list:
    """Generate value propositions based on objective"""
    return [
        f"Direct value: Achievement of {objective}",
        "Long-term partnership and collaboration opportunities",
        "Market advantage and competitive positioning",
        "Risk mitigation and shared expertise",
        "Scalability and growth potential"
    ]


def generate_potential_objections(context: str, objective: str) -> list:
    """Generate potential objections and responses"""
    return [
        {
            "objection": "Timeline concerns",
            "response": "We can discuss flexible timeline options and phased implementation"
        },
        {
            "objection": "Budget or resource constraints",
            "response": "Let's explore cost-effective approaches and ROI projections"
        },
        {
            "objection": "Risk concerns",
            "response": "We can address risk mitigation strategies and pilot programs"
        }
    ]


def identify_common_ground(research: str, industry: str) -> list:
    """Identify potential areas of common ground"""
    return [
        "Shared industry challenges and opportunities",
        "Mutual interest in market growth",
        "Common goals for efficiency and innovation",
        "Shared commitment to quality and excellence",
        "Interest in sustainable business practices"
    ]


async def main():
    print("🎯 Meeting Strategy Agent Started")
    print("Ready to develop strategic talking points and meeting approaches")
    if not GOOGLE_API_KEY:
        print("⚠️  GOOGLE_API_KEY not set - AI enhancement not available")
    await session.process_events()


if __name__ == "__main__":
    asyncio.run(main())
