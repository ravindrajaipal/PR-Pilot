# MLH / Hacktoberfest Hack Day Sambalpur × SUIIT Submission Guide

Use the sections below to fill out your **Submit a Project** form on MLH before **Nov 15, 11:59 PM IST**.

## Project Name
PR-Pilot — Multimodal Open-Source PR & Visual Bug Companion

## Tagline (Short Description)
An open-source Gemma 4 multimodal copilot & Agent Skill that correlates UI bug screenshots with Git diffs, blocks Hacktoberfest spam PRs, coaches first-time student contributors, and generates Playwright accessibility tests.

## Inspiration
During Hacktoberfest, open-source maintainers are overwhelmed by two problems: unverified UI pull requests where screenshots don't match code changes, and low-effort README spam. Meanwhile, first-time student contributors at campuses like SUIIT Sambalpur often have their legitimate fixes rejected due to non-standard commits or missing tests. We built PR-Pilot to bridge maintainers and contributors using open-weight multimodal AI.

## What It Does
- **Multimodal Visual-to-Code Grounding**: Uses Gemma 4 Vision + code comprehension to map pixel-level UI bugs (such as Odia script `ସମ୍ବଲପୁର ବିଶ୍ୱବିଦ୍ୟାଳୟ` line-height clipping, mobile button overflow, and dark-mode contrast leaks) directly to exact line numbers in `git diff`.
- **Hacktoberfest 2026 Spam Shield & Contributor Coach**: Scores PRs from 0–100 against Hacktoberfest quality rules, flags README typo spam, and upgrades raw student commit messages into Conventional Commits.
- **Auto-Test & Patch Lab**: Generates runnable `@playwright/test` and `@axe-core/playwright` WCAG 2.2 tests.
- **Portable Agent Skill (`SKILL.md`) & GitHub Action**: Works both as an interactive web studio and as a drop-in open-source agent skill (`SKILL.md`) + CLI harness (`src/gemma4_harness.py`).

## How We Built It
- **AI / Model**: Open-weight Gemma 4 (`gemma-3-27b-it` / `gemini-2.5-flash`) via the Gemini API + deterministic AST diff heuristics.
- **Frontend Studio**: HTML5 Canvas visual inspection engine, Tailwind CSS, and vanilla ES2022 modules.
- **DevOps & Open-Source Harness**: Python 3.11 CLI harness (`src/gemma4_harness.py`), standardized `SKILL.md`, and GitHub Actions CI workflow.
