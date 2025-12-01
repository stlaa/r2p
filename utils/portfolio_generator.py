import json
from typing import Dict

import requests


class PortfolioGenerator:
    """Generate portfolio from resume content using Perplexity API."""

    def __init__(self, api_key: str, api_url: str, model: str):
        self.api_key = api_key
        self.api_url = api_url
        self.model = model

    def _get_system_prompt(self) -> str:
        return """Create a professional portfolio website inspired by HTML5 UP's 'Directive' template.

OUTPUT: Start with <!DOCTYPE html> immediately. NO text before/after HTML. NO markdown blocks.

DIRECTIVE STYLE:
1. FONT: <link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;600;700;900&display=swap" rel="stylesheet">
   - font-family: 'Source Sans Pro', sans-serif
   - CRITICAL COLOR CONTRAST: Body text MUST be #2c2c2c on light backgrounds (white, #f5f5f5), and white (#ffffff) on dark backgrounds (var(--primary))
   - Body: font-size: clamp(16px, 2.5vw, 18px); font-weight: 400; line-height: 1.7; color: #2c2c2c
   - Headings on light backgrounds: color: #1a1a1a (very dark gray, NOT theme colors)
   - Headings on dark backgrounds: color: #ffffff (white)
   - Headings: font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em
   - Large headings: font-size: clamp(32px, 5vw, 48px); font-weight: 900
   - Medium headings: font-size: clamp(24px, 4vw, 32px); font-weight: 700
   - Small headings: font-size: clamp(18px, 3vw, 24px); font-weight: 600

2. TOP NAVIGATION BAR: position: fixed; top: 0; width: 100%; height: clamp(60px, 8vh, 70px); background: var(--primary); padding: 0 clamp(20px, 5vw, 60px); z-index: 1000
   - Display: flex; align-items: center; justify-content: space-between
   - Logo/Name on left: font-size: clamp(16px, 2.5vw, 20px); font-weight: 700; uppercase; letter-spacing: 0.08em; color: white
   - Nav links on right: display: inline-flex; gap: clamp(15px, 3vw, 30px); font-size: clamp(12px, 1.8vw, 14px); font-weight: 500; uppercase; letter-spacing: 0.05em; color: rgba(255,255,255,0.8)
   - Link hover: color: white; text-decoration: underline

3. MAIN CONTENT: margin-top: clamp(60px, 8vh, 70px); padding-top: 0; width: 100%; max-width: 100%

4. HERO: min-height: clamp(500px, 80vh, 100vh); padding: clamp(60px, 10vw, 100px) clamp(30px, 8vw, 80px); background: var(--primary); display: flex; align-items: center; justify-content: center
   - Content wrapper: max-width: 900px; margin: 0 auto; text-align: center; width: 100%
   - ALL TEXT IN HERO: color: #ffffff !important (pure white for maximum contrast)
   - Greeting: font-size: clamp(16px, 2.5vw, 20px); font-weight: 400; uppercase; letter-spacing: 0.05em; margin-bottom: 15px; color: #ffffff; opacity: 0.95
   - Name: font-size: clamp(32px, 6vw, 56px); font-weight: 900; uppercase; letter-spacing: 0.08em; line-height: 1.2; margin: 0 auto 20px; text-align: center; color: #ffffff
   - Title: font-size: clamp(18px, 3vw, 24px); font-weight: 400; uppercase; letter-spacing: 0.05em; color: #ffffff; opacity: 0.9; text-align: center
   - IMPORTANT: DO NOT include phone number or mobile number anywhere in portfolio

5. SECTIONS: padding: clamp(60px, 10vw, 100px) clamp(30px, 8vw, 80px); width: 100%; max-width: 100%; box-sizing: border-box; alternating backgrounds (white, #f5f5f5); opacity: 0; transform: translateY(30px); transition: opacity 0.8s ease, transform 0.8s ease
   - Container: max-width: 1400px; margin: 0 auto
   - Section headings: font-size: clamp(28px, 5vw, 42px); font-weight: 700; uppercase; letter-spacing: 0.06em; margin-bottom: clamp(30px, 5vw, 50px); color: #1a1a1a !important (dark gray, NOT theme color); text-align: center
   - Subheadings: font-size: clamp(18px, 3vw, 22px); font-weight: 600; margin-bottom: 15px; color: #2c2c2c !important
   - Body text in sections: color: #2c2c2c !important (dark gray on light backgrounds)
   - Add class "visible" when in viewport: opacity: 1; transform: translateY(0)

6. LAYOUT: display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr)); gap: clamp(30px, 5vw, 50px); width: 100%
   - Content blocks: padding: clamp(20px, 4vw, 30px); border-left: 4px solid var(--accent); background: transparent
   - NO border-radius, NO box-shadows - flat minimal design
   - Text in blocks: font-size: clamp(15px, 2vw, 17px); line-height: 1.7; color: #2c2c2c !important
   - Job titles/company names: color: #1a1a1a !important; font-weight: 600
   - Dates: color: #5a5a5a !important; font-style: italic

7. SKILLS SECTION - MODERN GRAPHIC DESIGN:
   - Display as grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 20px
   - Each skill card: padding: 20px 24px; background: #ffffff; border: 2px solid #e0e0e0; border-left: 4px solid var(--accent); position: relative; transition: all 0.3s ease
   - Skill name: font-size: clamp(14px, 2vw, 16px); font-weight: 600; color: #1a1a1a !important; text-transform: uppercase; letter-spacing: 0.03em
   - Progress bar container: width: 100%; height: 6px; background: #e8e8e8; margin-top: 12px; border-radius: 3px; overflow: hidden
   - Progress fill: height: 100%; background: linear-gradient(90deg, var(--accent), var(--primary)); animation: fillBar 1.5s ease-out forwards
   - Card hover: transform: translateY(-5px); border-color: var(--accent); box-shadow: 0 8px 20px rgba(0,0,0,0.1)
   - Animation: @keyframes fillBar { from { width: 0; } to { width: 100%; } }

8. BUTTONS: border: 2px solid var(--primary); background: transparent; padding: clamp(12px, 2vw, 15px) clamp(25px, 4vw, 35px); font-size: clamp(12px, 1.8vw, 14px); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; cursor: pointer; transition: all 0.3s
   - Hover: background: var(--primary); color: white

9. FOOTER: padding: clamp(40px, 6vw, 60px) clamp(30px, 8vw, 80px); background: #2e3141; color: rgba(255,255,255,0.6); text-align: center
   - Text: font-size: clamp(11px, 1.5vw, 13px); text-transform: uppercase; letter-spacing: 0.08em

10. SCROLL ANIMATIONS - CRITICAL:
   - CSS: section { opacity: 1 !important; transform: translateY(0) !important; } (ALL sections visible by default)
   - CSS: section.animate-on-scroll:not(.visible) { opacity: 0; transform: translateY(30px); }
   - CSS: section.animate-on-scroll { transition: opacity 0.8s ease, transform 0.8s ease; }
   - CSS: section.animate-on-scroll.visible { opacity: 1; transform: translateY(0); }
   - Add class "animate-on-scroll" to sections that should animate (NOT to #intro)
   - Add JavaScript at end of <body> BEFORE closing </body> tag:
     <script>
     document.addEventListener('DOMContentLoaded', function() {
       const sections = document.querySelectorAll('.animate-on-scroll');
       const observer = new IntersectionObserver((entries) => {
         entries.forEach(entry => {
           if (entry.isIntersecting) {
             entry.target.classList.add('visible');
           }
         });
       }, { threshold: 0.1 });
       sections.forEach(section => observer.observe(section));
     });
     </script>

11. RESPONSIVE:
   - All sizing uses clamp() for fluid scaling
   - Grid layouts use auto-fit with minmax for flexible columns
   - @media (max-width: 768px): nav links font-size: 11px, reduce letter-spacing to 0.03em, skills grid 2 columns
   - @media (max-width: 480px): single column layouts, padding: 40px 20px, skills grid 1 column

CRITICAL CSS RULES TO INCLUDE:
section { opacity: 1 !important; }
.animate-on-scroll:not(.visible) { opacity: 0; transform: translateY(30px); }
.animate-on-scroll { transition: opacity 0.8s ease, transform 0.8s ease; }
.animate-on-scroll.visible { opacity: 1; transform: translateY(0); }

CRITICAL JAVASCRIPT (must be exactly this):
<script>
document.addEventListener('DOMContentLoaded', function() {
  const sections = document.querySelectorAll('.animate-on-scroll');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.1 });
  sections.forEach(section => observer.observe(section));
});
</script>

STRUCTURE: <!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0">..Source Sans Pro..<style>* {box-sizing: border-box;} :root {--primary: X; --secondary: Y; --accent: Z;} body {margin: 0; overflow-x: hidden; color: #2c2c2c; background: #ffffff;} nav * {color: #ffffff !important;} #intro, #intro * {color: #ffffff !important;} section {opacity: 1 !important; background: #ffffff; color: #2c2c2c;} section h1, section h2, section h3 {color: #1a1a1a !important;} section p, section li, section span {color: #2c2c2c !important;} .animate-on-scroll:not(.visible) {opacity:0; transform:translateY(30px);} .animate-on-scroll {transition: opacity 0.8s ease, transform 0.8s ease;} .animate-on-scroll.visible {opacity:1; transform:translateY(0);} @keyframes fillBar {from {width:0;} to {width:100%;}}</style></head><body><nav id="navbar">LOGO (white) + NAV LINKS (white)</nav><main><section id="intro">HERO (no animate class)</section><section id="summary" class="animate-on-scroll">SUMMARY</section><section id="experience" class="animate-on-scroll">EXPERIENCE</section><section id="skills" class="animate-on-scroll">SKILLS with progress bars</section><section id="education" class="animate-on-scroll">EDUCATION</section><footer>COPYRIGHT</footer></main><script>document.addEventListener('DOMContentLoaded', function() { const sections = document.querySelectorAll('.animate-on-scroll'); const observer = new IntersectionObserver((entries) => { entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('visible'); } }); }, { threshold: 0.1 }); sections.forEach(section => observer.observe(section)); });</script></body></html>

CRITICAL COLOR CONTRAST RULES:
1. Hero section (#intro): ALL text MUST be #ffffff (white) on var(--primary) background
2. Navigation bar: ALL text MUST be #ffffff (white) on var(--primary) background
3. Content sections: ALL text MUST be #1a1a1a or #2c2c2c (dark) on white/#f5f5f5 backgrounds
4. Footer: text rgba(255,255,255,0.6) on #2e3141 background
5. NEVER use theme colors (primary/secondary/accent) for text on similar colored backgrounds
6. Use !important to enforce color contrast where needed

CRITICAL REMINDERS:
- DO NOT include phone numbers or mobile numbers anywhere
- Skills MUST have progress bars with gradient fill animation
- Name MUST be perfectly centered in hero section
- ALL sections MUST be visible by default (opacity: 1 !important on section element)
- Use class "animate-on-scroll" on sections (except #intro) to enable fade-in animation
- Hero section (#intro) MUST NOT have "animate-on-scroll" class
- JavaScript targets ".animate-on-scroll" class, not all sections
- ALWAYS ensure sufficient color contrast between text and background
- JavaScript MUST be inside <script> tags at end of <body> before </body>

Output pure HTML only."""

    def _get_user_prompt(self, resume_content: str, color_theme: Dict[str, str]) -> str:
        return f"""Generate portfolio HTML with this resume:

{resume_content}

Colors:
- Primary: {color_theme['primary']}
- Secondary: {color_theme['secondary']}
- Accent: {color_theme['accent']}
- Background: {color_theme['background']}
- Text: {color_theme['text']}

Use Directive style. Start with <!DOCTYPE html>. NO text before/after."""

    def generate_portfolio(self, resume_content: str, color_theme: Dict[str, str]) -> Dict[str, any]:
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": self._get_user_prompt(resume_content, color_theme)}
                ],
                "temperature": 0.3,
                "top_p": 0.95,
                "max_tokens": 6000,
                "stream": False
            }

            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=120
            )

            response.raise_for_status()
            result = response.json()
            html_content = result['choices'][0]['message']['content']
            html_content = self._clean_html_response(html_content)

            if not self._validate_html(html_content):
                return {
                    'success': False,
                    'error': 'Generated HTML failed validation',
                    'html': None
                }

            return {
                'success': True,
                'html': html_content,
                'error': None
            }

        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Portfolio generation timed out. Please try again.',
                'html': None
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'API request failed: {str(e)}',
                'html': None
            }
        except (KeyError, IndexError) as e:
            return {
                'success': False,
                'error': f'Invalid API response format: {str(e)}',
                'html': None
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Portfolio generation failed: {str(e)}',
                'html': None
            }

    def _clean_html_response(self, html_content: str) -> str:
        html_content = html_content.strip()
        if html_content.startswith('`html'):
            html_content = html_content[7:]
        if html_content.startswith('`'):
            html_content = html_content[3:]
        if html_content.endswith('`'):
            html_content = html_content[:-3]
        html_content = html_content.strip()

        if '<!DOCTYPE html>' in html_content:
            start_idx = html_content.find('<!DOCTYPE html>')
            html_content = html_content[start_idx:]

        if '</html>' in html_content:
            end_idx = html_content.rfind('</html>') + 7
            html_content = html_content[:end_idx]

        return html_content

    def _validate_html(self, html_content: str) -> bool:
        required = ['<!DOCTYPE html>', '<html', '<head>', '</head>', '<body>', '</body>', '</html>']
        for element in required:
            if element not in html_content:
                if len(html_content) > 500:
                    return True
                return False
        if len(html_content) < 50:
            return False
        return True

    def save_portfolio(self, html_content: str, file_path: str) -> bool:
        """Save HTML content to file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return True
        except Exception as e:
            print(f"Error saving portfolio: {str(e)}")
            return False
