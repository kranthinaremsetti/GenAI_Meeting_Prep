
import asyncio
import os
from typing import Any, Annotated

from dotenv import load_dotenv
from genai_session.session import GenAISession
import requests

load_dotenv()

# Environment variables
SERPER_API_KEY = os.environ.get("SERPER_API_KEY")
JWT_TOKEN = os.environ.get("JWT_TOKEN")

session = GenAISession(
    jwt_token=JWT_TOKEN
)


@session.bind(
    name="research_meeting_participants",
    description="Conduct thorough research on people and companies involved in the meeting. Prioritizes data from LinkedIn such as About, Experience, and Education sections."
)
async def research_meeting_participants(
    agent_context,
    participants: Annotated[str, "Names of the participants (other than you) in the meeting. Comma-separated list."],
    meeting_context: Annotated[str, "Context or background information about the meeting."],
) -> dict[str, Any]:
    """
    Research Specialist Agent
    
    Conduct thorough research on people and companies involved in the meeting.
    Your insights will lay the groundwork for strategic meeting preparation.
    
    Prioritizes data from LinkedIn such as About, Experience, and Education sections.
    If full profiles aren't available, uses knowledge to generate educated summaries.
    """
    
    agent_context.logger.info("Starting participant research")
    
    try:
        # Parse participants
        participant_list = [name.strip() for name in participants.split(',')]
        research_results = []
        
        for participant in participant_list:
            agent_context.logger.info(f"Researching participant: {participant}")
            
            participant_data = {
                "name": participant,
                "professional_summary": "",
                "experience": [],
                "education": [],
                "company_info": "",
                "linkedin_profile": "",
                "key_achievements": [],
                "industry_connections": []
            }
            
            # Perform searches if SERPER_API_KEY is available
            if SERPER_API_KEY:
                search_queries = [
                    f"{participant} LinkedIn profile",
                    f"{participant} professional experience",
                    f"{participant} company background",
                    f"{participant} education background"
                ]
                
                for query in search_queries:
                    try:
                        search_result = await perform_serper_search(query)
                        
                        if "LinkedIn" in query:
                            participant_data["linkedin_profile"] = extract_linkedin_info(search_result)
                        elif "experience" in query:
                            participant_data["experience"] = extract_experience_info(search_result)
                        elif "education" in query:
                            participant_data["education"] = extract_education_info(search_result)
                        elif "company" in query:
                            participant_data["company_info"] = extract_company_info(search_result)
                            
                    except Exception as e:
                        agent_context.logger.warning(f"Search failed for {query}: {str(e)}")
            
            # If no API key, provide structured placeholder data
            else:
                participant_data.update({
                    "professional_summary": f"Professional research needed for {participant}",
                    "experience": [f"Experience research required for {participant}"],
                    "education": [f"Education background research needed for {participant}"],
                    "company_info": f"Company information research required for {participant}",
                    "linkedin_profile": f"LinkedIn profile research needed for {participant}",
                    "key_achievements": [f"Achievement research required for {participant}"],
                    "industry_connections": [f"Network research needed for {participant}"]
                })
            
            research_results.append(participant_data)
        
        # Compile comprehensive research report
        report = {
            "meeting_context": meeting_context,
            "participants_researched": len(participant_list),
            "research_findings": research_results,
            "summary": f"Research completed for {len(participant_list)} participants: {', '.join(participant_list)}",
            "recommendations": [
                "Review each participant's professional background before the meeting",
                "Identify common interests and professional connections",
                "Prepare relevant talking points based on their experience",
                "Consider their industry expertise when planning discussion topics"
            ]
        }
        
        agent_context.logger.info("Research completed successfully")
        return report
        
    except Exception as e:
        agent_context.logger.error(f"Research failed: {str(e)}")
        return {
            "error": f"Research agent encountered an error: {str(e)}",
            "participants": participants,
            "context": meeting_context
        }


async def perform_serper_search(query: str) -> dict:
    """Perform search using Serper API"""
    if not SERPER_API_KEY:
        return {"error": "SERPER_API_KEY not set"}
    
    url = "https://google.serper.dev/search"
    payload = {"q": query, "num": 5}
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def extract_linkedin_info(search_result: dict) -> str:
    """Extract LinkedIn information from search results"""
    if "organic" in search_result:
        for result in search_result["organic"]:
            if "linkedin.com" in result.get("link", ""):
                return f"LinkedIn Profile: {result.get('title', 'N/A')} - {result.get('snippet', 'N/A')}"
    return "LinkedIn profile information not found"


def extract_experience_info(search_result: dict) -> list:
    """Extract experience information from search results"""
    experience_info = []
    if "organic" in search_result:
        for result in search_result["organic"]:
            if any(keyword in result.get("snippet", "").lower() for keyword in ["experience", "worked", "position", "role"]):
                experience_info.append(f"{result.get('title', 'N/A')}: {result.get('snippet', 'N/A')}")
    return experience_info[:3]


def extract_education_info(search_result: dict) -> list:
    """Extract education information from search results"""
    education_info = []
    if "organic" in search_result:
        for result in search_result["organic"]:
            if any(keyword in result.get("snippet", "").lower() for keyword in ["education", "university", "degree", "studied"]):
                education_info.append(f"{result.get('title', 'N/A')}: {result.get('snippet', 'N/A')}")
    return education_info[:3]


def extract_company_info(search_result: dict) -> str:
    """Extract company information from search results"""
    if "organic" in search_result:
        for result in search_result["organic"]:
            if any(keyword in result.get("snippet", "").lower() for keyword in ["company", "corporation", "organization"]):
                return f"Company Info: {result.get('title', 'N/A')} - {result.get('snippet', 'N/A')}"
    return "Company information not found"


async def main():
    print("🔍 Meeting Research Agent Started")
    print("Ready to conduct thorough research on meeting participants")
    if not SERPER_API_KEY:
        print("⚠️  SERPER_API_KEY not set - running in demo mode")
    await session.process_events()


if __name__ == "__main__":
    asyncio.run(main())
