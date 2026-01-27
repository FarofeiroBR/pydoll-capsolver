# Pydoll + CapSolver: The Ultimate Stealth Web Automation 🚀

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CapSolver](https://img.shields.io/badge/CAPTCHA-CapSolver-orange)](https://www.capsolver.com/?utm_source=github)

**Pydoll** is a lightweight, asynchronous Python library that interacts directly with Chrome via the DevTools Protocol (CDP), bypassing traditional WebDriver detection. Combined with **[CapSolver](https://www.capsolver.com/?utm_source=github)**, you can build powerful, undetectable automation scripts that handle even the toughest CAPTCHA challenges.

---

## 🌟 Key Features

### 🤖 Pydoll (The Stealth Engine)
- **No WebDriver Required**: Direct CDP connection eliminates common bot detection vectors.
- **Human-Like Interactions**: Realistic keystroke timing, physics-based scrolling, and natural mouse movements.
- **Async Architecture**: Built on `asyncio` for high-performance, non-blocking I/O.
- **Total Control**: Intercept network traffic, manage browser fingerprints, and handle multi-tab sessions.

### 🧩 CapSolver (The Solution)
- **AI-Powered Solving**: Fast and reliable solutions for reCAPTCHA (v2/v3), Cloudflare Turnstile, AWS WAF, and more.
- **Seamless Integration**: Simple API calls to get tokens and bypass challenges in seconds.
- **Production Ready**: Scalable infrastructure designed for high-volume automation.

---

## 🛠️ Installation

Install the necessary dependencies using pip:

```bash
pip install pydoll-python aiohttp
```

*Note: Pydoll requires a Chromium-based browser (Chrome, Edge, etc.) installed on your system.*

---

## 🚀 Quick Start

### 1. Configure your API Key
Replace `YOUR_CAPSOLVER_API_KEY` in your script or set it as an environment variable.

### 2. Basic Integration Example
This snippet shows how to use the `CapSolverService` utility to solve a reCAPTCHA v2 challenge.

```python
from pydoll.browser import Chrome
from utils.capsolver_handler import capsolver

async def main():
    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to("https://example.com/captcha-page")
        
        # Solve reCAPTCHA v2
        token = await capsolver.solve_recaptcha_v2(
            website_url="https://example.com/captcha-page",
            website_key="SITE_KEY_HERE"
        )
        print(f"Solved! Token: {token[:20]}...")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

---

## 📂 Project Structure

| File | Description |
|------|-------------|
| `README.md` | Project overview and documentation. |
| `utils/capsolver_handler.py` | Reusable CapSolver utility class for various CAPTCHA types. |
| `examples/solve_recaptcha_v2.py` | Full example for solving reCAPTCHA v2. |
| `examples/solve_turnstile.py` | Full example for bypassing Cloudflare Turnstile. |

---

## ⚙️ Humanization Features in Pydoll

| Feature | Description |
|---------|-------------|
| **Variable Keystrokes** | 30-120ms delays with ~2% simulated typos. |
| **Physics Scrolling** | Momentum and friction-based scrolling for natural movement. |
| **Bezier Mouse Paths** | Mimics human hand movement curves. |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue for any bugs or feature requests.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Ready to automate?** [Get your CapSolver API Key now!](https://www.capsolver.com/?utm_source=github)
