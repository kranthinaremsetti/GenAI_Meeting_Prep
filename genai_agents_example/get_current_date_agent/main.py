import asyncio
from datetime import datetime

from genai_session.session import GenAISession

session = GenAISession(
    jwt_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiNjE5M2U5Yy1mMGU5LTRhNDQtOWRhYS05ZGFiM2VkZjY0NzQiLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6ImM3MWUyZmQwLTc0ODMtNDI5MC05YzFlLWEyNTc1OTA0Y2VjNyJ9.S6O_9RowRtyVgRFKlkY19kSfkvuAoHLB1aVx_AaDsgM"
)


@session.bind(name="get_current_date", description="Return current date")
async def get_current_date(agent_context):
    agent_context.logger.info("Inside get_current_date")
    return datetime.now().strftime("%Y-%m-%d")


async def main():
    await session.process_events()


if __name__ == "__main__":
    asyncio.run(main())
