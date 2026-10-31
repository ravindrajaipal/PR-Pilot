---
name: pr-pilot-multimodal
description: Multimodal Open-Source PR & Visual Bug Companion powered by Gemma 4. Use when analyzing UI bug screenshots alongside Git diffs, auditing Hacktoberfest PR quality, or synthesizing Playwright visual regression tests.
---

# PR-Pilot Multimodal Agent Skill (`SKILL.md`)

PR-Pilot is an open-source AI agent skill and model harness built for **Hacktoberfest Hack Day Sambalpur x SUIIT 2026**.

## Core Capabilities
1. **Multimodal Screenshot + Diff Correlation (Gemma 4)**: Maps visual UI defects (overflow, clipping, contrast failures, Indic/Odia glyph rendering issues) directly to line numbers in a unified `git diff`.
2. **Hacktoberfest Spam Shield & Contributor Coach**: Evaluates PRs against Hacktoberfest quality rules, blocks low-effort typo spam, and upgrades student commit messages into Conventional Commits.
3. **Automated Playwright + Axe Accessibility Test Synthesis**: Generates ready-to-run `.spec.ts` regression suites.
