#!/usr/bin/env python3
"""
PR-Pilot v3.0 — Open-Weight Model Harness & Static/Multimodal Diff Analyzer for Gemma 4.
Built for Hacktoberfest Hack Day Sambalpur x SUIIT 2026.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass, asdict


@dataclass
class DiffSummary:
    added_lines: list[tuple[int, str]]
    removed_lines: list[tuple[int, str]]
    total_additions: int
    total_deletions: int
    complexity_delta: int


def parse_unified_diff(diff_text: str) -> DiffSummary:
    """Parses a unified git diff and extracts additions, deletions, and branch complexity delta."""
    added: list[tuple[int, str]] = []
    removed: list[tuple[int, str]] = []
    branch_pattern = re.compile(r"(?:\b(?:if|else|for|while|switch|case|catch)\b|&&|\|\|)")
    complexity_delta = 0

    for idx, raw_line in enumerate(diff_text.splitlines(), start=1):
        stripped = raw_line.strip()
        if stripped.startswith("+++") or stripped.startswith("---"):
            continue
        if stripped.startswith("+"):
            content = stripped[1:].strip()
            added.append((idx, content))
            complexity_delta += len(branch_pattern.findall(content))
        elif stripped.startswith("-"):
            content = stripped[1:].strip()
            removed.append((idx, content))
            complexity_delta -= len(branch_pattern.findall(content))

    return DiffSummary(
        added_lines=added,
        removed_lines=removed,
        total_additions=len(added),
        total_deletions=len(removed),
        complexity_delta=complexity_delta,
    )


def relative_luminance(hex_color: str) -> float:
    """Computes WCAG 2.2 relative luminance for a 3- or 6-digit hex color string."""
    clean = hex_color.lstrip("#").strip()
    if len(clean) == 3:
        clean = "".join(ch * 2 for ch in clean)
    if len(clean) != 6:
        raise ValueError(f"Invalid hex color: {hex_color}")
    r = int(clean[0:2], 16) / 255.0
    g = int(clean[2:4], 16) / 255.0
    b = int(clean[4:6], 16) / 255.0

    def to_linear(channel: float) -> float:
        return channel / 12.92 if channel <= 0.03928 else ((channel + 0.055) / 1.055) ** 2.4

    return 0.2126 * to_linear(r) + 0.7152 * to_linear(g) + 0.0722 * to_linear(b)


def calculate_wcag_contrast(fg_hex: str, bg_hex: str) -> float:
    """Returns the WCAG 2.2 contrast ratio (1.0 to 21.0) between two hex colors."""
    lum1 = relative_luminance(fg_hex)
    lum2 = relative_luminance(bg_hex)
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    return round((lighter + 0.05) / (darker + 0.05), 2)


def audit_diff_security_and_a11y(diff_text: str) -> list[dict[str, str]]:
    """Audits added lines in a git diff for security vulnerabilities and UI/accessibility defects."""
    summary = parse_unified_diff(diff_text)
    findings: list[dict[str, str]] = []

    secret_re = re.compile(r"(AIza[0-9A-Za-z\-_]{20,}|ghp_[0-9A-Za-z]{20,}|sk-[0-9A-Za-z]{20,})")
    xss_re = re.compile(r"(\beval\s*\(|dangerouslySetInnerHTML)")
    fixed_px_re = re.compile(r"width:\s*([3-9]\d{2}|\d{4,})px")

    for line_no, code in summary.added_lines:
        if secret_re.search(code):
            findings.append({
                "line": str(line_no),
                "severity": "CRITICAL",
                "rule": "SECRET_LEAK",
                "message": "Hardcoded API key or token detected in added line.",
            })
        if xss_re.search(code):
            findings.append({
                "line": str(line_no),
                "severity": "HIGH",
                "rule": "UNSAFE_EXECUTION",
                "message": "Unsafe eval() or dangerouslySetInnerHTML sink detected.",
            })
        px_match = fixed_px_re.search(code)
        if px_match and "max-width" not in code:
            findings.append({
                "line": str(line_no),
                "severity": "MEDIUM",
                "rule": "MOBILE_VIEWPORT_OVERFLOW",
                "message": f"Hardcoded width ({px_match.group(1)}px) risks overflowing 375px mobile viewports.",
            })

    return findings


def score_hacktoberfest_pr(diff_text: str, commit_message: str) -> dict[str, object]:
    """Scores a PR from 0 to 100 according to Hacktoberfest 2026 quality & anti-spam rules."""
    summary = parse_unified_diff(diff_text)
    findings = audit_diff_security_and_a11y(diff_text)
    conventional_re = re.compile(r"^(fix|feat|perf|refactor|docs|test|chore)(\([\w\-]+\))?:\s+.{10,}")
    issue_ref_re = re.compile(r"#\d+")

    if summary.total_additions == 0 and summary.total_deletions == 0:
        return {"score": 0, "verdict": "SPAM_REJECTED", "reasons": ["Empty diff"]}

    total_changed_chars = sum(len(x[1]) for x in summary.added_lines)
    if summary.total_additions <= 1 and total_changed_chars < 15 and not issue_ref_re.search(commit_message):
        return {
            "score": 15,
            "verdict": "SPAM_REJECTED",
            "reasons": ["Low-effort / trivial change without linked issue"],
        }

    score = 55
    reasons: list[str] = []

    if summary.total_additions >= 2:
        score += 15
        reasons.append("Substantive multi-line code change")
    if conventional_re.match(commit_message.strip()):
        score += 15
        reasons.append("Follows Conventional Commits specification")
    if issue_ref_re.search(commit_message):
        score += 10
        reasons.append("Links to tracked repository issue")
    if not any(f["severity"] == "CRITICAL" for f in findings):
        score += 5
    else:
        score -= 40
        reasons.append("Critical security finding detected in diff")

    score = max(0, min(100, score))
    verdict = (
        "HACKTOBERFEST-ACCEPTED"
        if score >= 75
        else ("NEEDS_REVISION" if score >= 40 else "SPAM_REJECTED")
    )
    return {"score": score, "verdict": verdict, "reasons": reasons, "findings": findings}


def build_gemma4_multimodal_payload(diff_text: str, screenshot_b64: str | None = None) -> dict[str, object]:
    """Constructs the JSON request payload for Gemma 4 / Gemini API multimodal analysis."""
    parts: list[dict[str, object]] = [
        {
            "text": (
                "You are PR-Pilot, an open-source multimodal PR companion built with Gemma 4.\n"
                "Correlate visual anomalies in the screenshot with exact lines in the git diff.\n\n"
                f"GIT DIFF:\n{diff_text}"
            )
        }
    ]
    if screenshot_b64:
        parts.append({"inline_data": {"mime_type": "image/png", "data": screenshot_b64}})
    return {"contents": [{"parts": parts}]}


def main() -> None:
    parser = argparse.ArgumentParser(description="PR-Pilot v3.0 Gemma 4 Multimodal CLI Harness")
    parser.add_argument("--diff-cmd", default="git diff HEAD~1", help="Git diff command")
    parser.add_argument("--commit-msg", default="fix(i18n): resolve Odia clipping (#142)", help="Commit message")
    args = parser.parse_args()

    proc = subprocess.run(args.diff_cmd, shell=True, capture_output=True, text=True, check=False)
    diff_output = proc.stdout if proc.returncode == 0 else ""
    if not diff_output.strip():
        diff_output = (
            "- .odia-Notice-title { line-height: 1.05; height: 26px; }\n"
            "+ .odia-Notice-title { line-height: 1.65; min-height: 36px; }\n"
            "+ .register-btn { width: 100%; max-width: 240px; color: #ffffff; background: #4f46e5; }"
        )
    summary = parse_unified_diff(diff_output)
    quality = score_hacktoberfest_pr(diff_output, args.commit_msg)
    print(json.dumps({"diff_summary": asdict(summary), "quality_gate": quality}, indent=2))


if __name__ == "__main__":
    main()
