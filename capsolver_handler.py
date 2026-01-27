import aiohttp
import asyncio
from typing import Optional
from dataclasses import dataclass

# Replace with your actual API Key
CAPSOLVER_API_KEY = 'YOUR_CAPSOLVER_API_KEY'

@dataclass
class TaskResult:
    status: str
    solution: Optional[dict] = None
    error_description: Optional[str] = None

class CapSolverService:
    """
    A reusable service to interact with CapSolver API for various CAPTCHA types.
    """
    def __init__(self, api_key: str = CAPSOLVER_API_KEY):
        self.api_key = api_key
        self.base_url = 'https://api.capsolver.com'

    async def create_task(self, task_data: dict) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'{self.base_url}/createTask',
                json={
                    'clientKey': self.api_key,
                    'task': task_data
                }
            ) as response:
                data = await response.json()
                if data.get('errorId', 0) != 0:
                    raise Exception(f"CapSolver error: {data.get('errorDescription')}")
                return data['taskId']

    async def get_task_result(self, task_id: str, max_attempts: int = 60) -> TaskResult:
        async with aiohttp.ClientSession() as session:
            for _ in range(max_attempts):
                await asyncio.sleep(2)
                async with session.post(
                    f'{self.base_url}/getTaskResult',
                    json={
                        'clientKey': self.api_key,
                        'taskId': task_id
                    }
                ) as response:
                    data = await response.json()
                    if data.get('status') == 'ready':
                        return TaskResult(
                            status='ready',
                            solution=data.get('solution')
                        )
                    if data.get('status') == 'failed':
                        raise Exception(f"Task failed: {data.get('errorDescription')}")
        raise Exception('Timeout waiting for CAPTCHA solution')

    async def solve_recaptcha_v2(self, website_url: str, website_key: str) -> str:
        task_id = await self.create_task({
            'type': 'ReCaptchaV2TaskProxyLess',
            'websiteURL': website_url,
            'websiteKey': website_key
        })
        result = await self.get_task_result(task_id)
        return result.solution.get('gRecaptchaResponse', '') if result.solution else ''

    async def solve_recaptcha_v3(
        self,
        website_url: str,
        website_key: str,
        page_action: str = 'submit'
    ) -> str:
        task_id = await self.create_task({
            'type': 'ReCaptchaV3TaskProxyLess',
            'websiteURL': website_url,
            'websiteKey': website_key,
            'pageAction': page_action
        })
        result = await self.get_task_result(task_id)
        return result.solution.get('gRecaptchaResponse', '') if result.solution else ''

    async def solve_turnstile(
        self,
        website_url: str,
        website_key: str,
        action: Optional[str] = None,
        cdata: Optional[str] = None
    ) -> str:
        task_data = {
            'type': 'AntiTurnstileTaskProxyLess',
            'websiteURL': website_url,
            'websiteKey': website_key
        }
        if action or cdata:
            metadata = {}
            if action: metadata['action'] = action
            if cdata: metadata['cdata'] = cdata
            task_data['metadata'] = metadata

        task_id = await self.create_task(task_data)
        result = await self.get_task_result(task_id)
        return result.solution.get('token', '') if result.solution else ''

# Global instance for easy import
capsolver = CapSolverService()
