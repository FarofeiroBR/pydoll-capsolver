import asyncio
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pydoll.browser import Chrome
from utils.capsolver_handler import capsolver

def extract_cdp_value(response):
    """Extract the actual value from a CDP response."""
    if isinstance(response, dict):
        return response.get('result', {}).get('result', {}).get('value', '')
    return response

async def solve_turnstile_example():
    async with Chrome() as browser:
        tab = await browser.start()

        # Target URL with Cloudflare Turnstile
        target_url = 'https://peet.ws/turnstile-test/non-interactive.html'
        await tab.go_to(target_url)

        try:
            print('Detecting Cloudflare Turnstile...')
            
            # Get the site key
            site_key_response = await tab.execute_script(
                "return document.querySelector('[name=cf-turnstile-response]').parentElement.getAttribute('data-sitekey') || '0x4AAAAAAADnPIDROMAp0J_5'"
            )
            site_key = extract_cdp_value(site_key_response)

            print(f'Turnstile detected (Site Key: {site_key}), solving via CapSolver...')

            # Solve the CAPTCHA
            token = await capsolver.solve_turnstile(
                website_url=target_url,
                website_key=site_key
            )

            print(f'Solution obtained: {token[:30]}...')

            # Inject the token
            await tab.execute_script(
                f"document.querySelector('[name=cf-turnstile-response]').value = '{token}';"
            )
            
            print('Token injected. Proceeding with automation...')
            await asyncio.sleep(5)

        except Exception as e:
            print(f'An error occurred: {e}')

if __name__ == "__main__":
    asyncio.run(solve_turnstile_example())
