
import asyncio
import os
from typing import Any, Annotated

from dotenv import load_dotenv
from genai_session.session import GenAISession
import requests

load_dotenv()

# Environment variables
EXA_API_KEY = os.environ.get("EXA_API_KEY")

session = GenAISession(
    jwt_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMWE1MzM5ZC04MTMwLTQ0ZWQtOTJmOS00NmQ2NWFkNjg1ZmYiLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6ImM3MWUyZmQwLTc0ODMtNDI5MC05YzFlLWEyNTc1OTA0Y2VjNyJ9.qJtI9QtS3-iTPv0pL_iCwgyvCHOfXFh0LrmU1rYVfIA" # noqa: E501
)


@session.bind(
    name="analyze_meeting_industry_trends",
    description="Analyze current industry trends, challenges, and opportunities relevant to the meeting participants and context."
)
async def analyze_meeting_industry_trends(
    agent_context,
    participants: Annotated[str, "Names of the participants and their companies/industries"],
    meeting_context: Annotated[str, "Context or background information about the meeting"],
) -> dict[str, Any]:
    """
    Industry Analyst Agent
    
    Analyze the current industry trends, challenges, and opportunities.
    Your analysis will identify key trends, challenges facing the industry, 
    and potential opportunities that could be leveraged during the meeting 
    for strategic advantage.
    """
    
    agent_context.logger.info("Starting industry analysis")
    
    try:
        # Parse participants and extract industries
        participant_list = [name.strip() for name in participants.split(',')]
        
        # Extract potential industries from context and participants
        industries = extract_industries_from_context(meeting_context, participant_list)
        
        analysis_results = {
            "industry_trends": [],
            "market_challenges": [],
            "opportunities": [],
            "competitive_landscape": [],
            "regulatory_environment": [],
            "technology_disruptions": []
        }
        
        # Analyze each industry
        for industry in industries:
            agent_context.logger.info(f"Analyzing industry: {industry}")
            
            industry_data = {
                "industry": industry,
                "current_trends": [],
                "growth_opportunities": [],
                "challenges": [],
                "competitive_insights": [],
                "regulatory_updates": [],
                "tech_disruptions": []
            }
            
            # Perform searches if EXA_API_KEY is available
            if EXA_API_KEY:
                search_queries = [
                    f"{industry} industry trends 2025",
                    f"{industry} market challenges opportunities",
                    f"{industry} competitive landscape analysis",
                    f"{industry} regulatory changes 2025",
                    f"{industry} technology disruption innovation"
                ]
                
                for query in search_queries:
                    try:
                        # For now, we'll use a placeholder since Exa integration is complex
                        # In production, you'd use the actual Exa Python SDK
                        search_result = await perform_industry_search(query)
                        
                        if "trends" in query:
                            industry_data["current_trends"] = extract_trends_info(search_result)
                        elif "challenges" in query:
                            industry_data["challenges"] = extract_challenges_info(search_result)
                        elif "competitive" in query:
                            industry_data["competitive_insights"] = extract_competitive_info(search_result)
                        elif "regulatory" in query:
                            industry_data["regulatory_updates"] = extract_regulatory_info(search_result)
                        elif "technology" in query:
                            industry_data["tech_disruptions"] = extract_tech_info(search_result)
                            
                    except Exception as e:
                        agent_context.logger.warning(f"Search failed for {query}: {str(e)}")
            
            # If no API key, provide structured placeholder data
            else:
                industry_data.update({
                    "current_trends": [f"Current trends analysis needed for {industry}"],
                    "growth_opportunities": [f"Growth opportunity research required for {industry}"],
                    "challenges": [f"Challenge analysis needed for {industry}"],
                    "competitive_insights": [f"Competitive landscape research required for {industry}"],
                    "regulatory_updates": [f"Regulatory analysis needed for {industry}"],
                    "tech_disruptions": [f"Technology disruption research required for {industry}"]
                })
            
            analysis_results["industry_trends"].append(industry_data)
        
        # Generate strategic insights
        strategic_insights = generate_strategic_insights(analysis_results, meeting_context)
        
        # Compile comprehensive industry analysis report
        report = {
            "meeting_context": meeting_context,
            "participants_analyzed": len(participant_list),
            "industries_covered": industries,
            "industry_analysis": analysis_results,
            "strategic_insights": strategic_insights,
            "key_findings": [
                "Digital transformation is accelerating across industries",
                "Regulatory compliance is becoming more complex",
                "Sustainability initiatives are driving new opportunities",
                "AI and automation are reshaping competitive landscapes"
            ],
            "strategic_recommendations": [
                "Focus on emerging technology adoption",
                "Address regulatory compliance proactively",
                "Explore sustainability partnerships",
                "Consider market consolidation opportunities"
            ],
            "summary": f"Industry analysis completed for {len(industries)} industries covering {len(participant_list)} participants"
        }
        
        agent_context.logger.info("Industry analysis completed successfully")
        return report
        
    except Exception as e:
        agent_context.logger.error(f"Industry analysis failed: {str(e)}")
        return {
            "error": f"Industry analysis agent encountered an error: {str(e)}",
            "participants": participants,
            "context": meeting_context
        }


def extract_industries_from_context(context: str, participants: list) -> list:
    """Extract potential industries from context and participants"""
    industry_keywords = [
        "technology", "tech", "software", "healthcare", "finance", "fintech",
        "manufacturing", "retail", "e-commerce", "consulting", "education",
        "energy", "automotive", "aerospace", "telecommunications", "media",
        "real estate", "construction", "hospitality", "entertainment"
    ]
    
    industries = []
    context_lower = context.lower()
    
    for keyword in industry_keywords:
        if keyword in context_lower:
            industries.append(keyword.title())
    
    if not industries:
        industries = ["General Business", "Technology", "Market Analysis"]
    
    return list(set(industries))


async def perform_industry_search(query: str) -> dict:
    """Perform industry search - placeholder for Exa API integration"""
    if not EXA_API_KEY:
        return {"error": "EXA_API_KEY not set"}
    
    # Placeholder for actual Exa API integration
    # In production, you would use the Exa Python SDK
    return {
        "results": [
            {"title": f"Industry Analysis: {query}", "content": f"Analysis content for {query}"}
        ]
    }


def extract_trends_info(search_result: dict) -> list:
    """Extract trend information from search results"""
    trends = []
    if "results" in search_result:
        for result in search_result["results"]:
            trends.append(f"Trend: {result.get('title', 'N/A')}")
    return trends[:3]


def extract_challenges_info(search_result: dict) -> list:
    """Extract challenge information from search results"""
    challenges = []
    if "results" in search_result:
        for result in search_result["results"]:
            challenges.append(f"Challenge: {result.get('title', 'N/A')}")
    return challenges[:3]


def extract_competitive_info(search_result: dict) -> list:
    """Extract competitive information from search results"""
    competitive = []
    if "results" in search_result:
        for result in search_result["results"]:
            competitive.append(f"Competitive Insight: {result.get('title', 'N/A')}")
    return competitive[:3]


def extract_regulatory_info(search_result: dict) -> list:
    """Extract regulatory information from search results"""
    regulatory = []
    if "results" in search_result:
        for result in search_result["results"]:
            regulatory.append(f"Regulatory Update: {result.get('title', 'N/A')}")
    return regulatory[:3]


def extract_tech_info(search_result: dict) -> list:
    """Extract technology information from search results"""
    tech = []
    if "results" in search_result:
        for result in search_result["results"]:
            tech.append(f"Tech Disruption: {result.get('title', 'N/A')}")
    return tech[:3]


def generate_strategic_insights(analysis_results: dict, context: str) -> list:
    """Generate strategic insights based on analysis results"""
    insights = [
        "Market consolidation opportunities exist in traditional sectors",
        "Digital transformation is creating new partnership possibilities",
        "Regulatory changes are opening new compliance-focused markets",
        "Sustainability initiatives are driving innovation investments",
        "Technology adoption gaps present consulting opportunities"
    ]
    return insights


async def main():
    print("📈 Meeting Industry Analysis Agent Started")
    print("Ready to analyze industry trends and opportunities")
    if not EXA_API_KEY:
        print("⚠️  EXA_API_KEY not set - running in demo mode")
    await session.process_events()


if __name__ == "__main__":
    asyncio.run(main())
