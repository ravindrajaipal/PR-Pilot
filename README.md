# PR-Pilot — Multimodal Open-Source PR & Visual Bug Companion (Gemma 4)

Built for **Hacktoberfest Hack Day Sambalpur × SUIIT 2026** (APJ Abdul Kalam Auditorium, Sambalpur University Institute of Information Technology, Odisha).

## Prize Categories Targeted
1. **Best Use of Gemma 4**: Jointly analyzes UI bug screenshots (including Odia script rendering on SUIIT's portal) and unified Git diffs via Gemma 4 on the Gemini API.
2. **Best Open-Source AI Project (DigitalOcean)**: Ships a standardized open-source Agent Skill (`SKILL.md`), a portable Python open-weight model harness (`src/gemma4_harness.py`), and a turnkey GitHub Action (`.github/workflows/pr-pilot.yml`).
3. **Best Software Project & Hackday Overall**: Zero-dependency interactive web studio (`index.html`) with visual bounding-box correlation, Hacktoberfest 2026 spam-shield scoring, First-Time Contributor commit coaching, and Playwright + WCAG 2.2 test synthesis.

## Quickstart
1. **Run Web Studio**: Open `index.html` in any browser (or deploy to GitHub Pages / DigitalOcean App Platform).
2. **Run CLI Model Harness**:
   ```bash
   export GEMINI_API_KEY="your-gemini-api-key"
   python3 src/gemma4_harness.py --diff-cmd "git diff HEAD~1" --screenshot bug.png
   ```
3. **Install as an Agent Skill**: Copy `SKILL.md` into your repository's `.agents/skills/pr-pilot/` or `.claude/skills/` directory.

## License
MIT Open-Source License — Happy Hacktoberfest 2026!
