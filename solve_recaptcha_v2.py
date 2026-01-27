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

async def solve_recaptcha_v2_example():
    async with Chrome() as browser:
        tab = await browser.start()

        # Target URL with reCAPTCHA v2
        target_url = 'https://www.google.com/recaptcha/api2/demo'
        await tab.go_to(target_url)

        try:
            print('Detecting reCAPTCHA v2...')
            # Get the site key from the data attribute
            site_key_response = await tab.execute_script(
                "return document.querySelector('.g-recaptcha').getAttribute('data-sitekey')"
            )
            site_key = extract_cdp_value(site_key_response)
            
            if not site_key:
                print("Could not find site key.")
                return

            print(f'reCAPTCHA v2 detected (Site Key: {site_key}), solving via CapSolver...')

            # Solve the CAPTCHA
            token = await capsolver.solve_recaptcha_v2(
                website_url=target_url,
                website_key=site_key
            )

            print(f'Solution obtained: {token[:30]}...')

            # Inject the token and submit
            await tab.execute_script(
                f"document.getElementById('g-recaptcha-response').innerHTML = '{token}';"
            )
            
            # Click submit button
            await tab.click('#recaptcha-demo-submit')
            print('Form submitted successfully!')
            
            # Wait a bit to see the result
            await asyncio.sleep(5)

        except Exception as e:
            print(f'An error occurred: {e}')

if __name__ == "__main__":
    asyncio.run(solve_recaptcha_v2_example())
