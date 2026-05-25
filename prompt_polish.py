#!/usr/bin/env python3
"""prompt-polish: Analyze and improve your AI prompts with one command."""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

__version__ = "1.0.0"

ANALYZE_PROMPT = """You are a prompt engineering expert. Analyze the following user prompt and provide:

1. **Score** (1-10): Rate the prompt quality
2. **Issues**: List specific problems (vague, missing context, no constraints, etc.)
3. **Improved Version**: Rewrite the prompt to be more effective
4. **Explanation**: Brief explanation of what you changed and why

User prompt to analyze:
---
{prompt}
---

Respond in this exact JSON format:
{{
  "score": <1-10>,
  "issues": ["issue1", "issue2"],
  "improved": "the improved prompt text",
  "changes": ["change1", "change2"]
}}

Output ONLY valid JSON, nothing else."""

OPTIMIZE_PROMPT = """You are a prompt optimization expert. Transform the user's rough idea into a well-structured prompt.

Rules for a good prompt:
1. Clear role/persona for the AI
2. Specific context and background
3. Explicit task instructions
4. Output format requirements
5. Constraints and boundaries
6. Examples if helpful

User's rough idea:
---
{prompt}
---

Generate an optimized prompt that incorporates these best practices.
Output ONLY the improved prompt, nothing else."""

SCORE_PROMPT = """Rate this AI prompt on a scale of 1-10 across these dimensions:

1. **Clarity** (1-10): Is the intent clear?
2. **Specificity** (1-10): Are details concrete?
3. **Context** (1-10): Is background provided?
4. **Constraints** (1-10): Are boundaries set?
5. **Format** (1-10): Is output format specified?

Prompt to rate:
---
{prompt}
---

Respond in this exact JSON format:
{{
  "clarity": <1-10>,
  "specificity": <1-10>,
  "context": <1-10>,
  "constraints": <1-10>,
  "format": <1-10>,
  "overall": <1-10>,
  "feedback": "one sentence summary"
}}

Output ONLY valid JSON, nothing else."""


def call_api(prompt_text, api_key=None, base_url=None, model=None):
    """Call OpenAI-compatible API."""
    api_key = api_key or os.environ.get("PROMPT_POLISH_API_KEY") or os.environ.get("OPENAI_API_KEY") or os.environ.get("DEEPSEEK_API_KEY", "")
    base_url = base_url or os.environ.get("PROMPT_POLISH_BASE_URL", "https://api.deepseek.com/v1")
    model = model or os.environ.get("PROMPT_POLISH_MODEL", "deepseek-chat")

    base_url = base_url.rstrip("/")
    url = f"{base_url}/chat/completions"

    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "user", "content": prompt_text}
        ],
        "temperature": 0.3,
        "max_tokens": 2000
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    })

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode())
            return data["choices"][0]["message"]["content"].strip()
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"API Error {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def print_score_bar(label, score, max_score=10):
    """Print a visual score bar."""
    filled = int(score)
    empty = max_score - filled
    bar = "█" * filled + "░" * empty
    color = "\033[32m" if score >= 7 else "\033[33m" if score >= 5 else "\033[31m"
    reset = "\033[0m"
    print(f"  {label:12s} {color}{bar}{reset} {score}/10")


def cmd_analyze(args):
    """Analyze and improve a prompt."""
    prompt = args.prompt or read_stdin()
    if not prompt:
        print("Error: Provide a prompt as argument or via stdin", file=sys.stderr)
        sys.exit(1)

    print("Analyzing prompt...\n", file=sys.stderr)
    raw = call_api(ANALYZE_PROMPT.format(prompt=prompt), args.api_key, args.base_url, args.model)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print("Raw response:\n")
        print(raw)
        sys.exit(0)

    score = data.get("score", 0)
    issues = data.get("issues", [])
    improved = data.get("improved", "")
    changes = data.get("changes", [])

    # Score
    print(f"┌─ Prompt Score ─────────────────────┐")
    print_score_bar("Overall", score)
    print(f"└────────────────────────────────────┘\n")

    # Issues
    if issues:
        print("⚠  Issues found:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        print()

    # Changes
    if changes:
        print("✨ What was improved:")
        for c in changes:
            print(f"   • {c}")
        print()

    # Improved version
    if improved:
        print("─" * 50)
        print("Improved prompt:\n")
        print(improved)
        print("─" * 50)

    if args.copy:
        import subprocess
        try:
            subprocess.run(["clip"], input=improved.encode(), check=True)
            print("\n(Copied to clipboard)")
        except Exception:
            pass


def cmd_score(args):
    """Score a prompt across dimensions."""
    prompt = args.prompt or read_stdin()
    if not prompt:
        print("Error: Provide a prompt as argument or via stdin", file=sys.stderr)
        sys.exit(1)

    print("Scoring prompt...\n", file=sys.stderr)
    raw = call_api(SCORE_PROMPT.format(prompt=prompt), args.api_key, args.base_url, args.model)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print("Raw response:\n")
        print(raw)
        sys.exit(0)

    print(f"┌─ Prompt Score Breakdown ───────────┐")
    print_score_bar("Clarity", data.get("clarity", 0))
    print_score_bar("Specificity", data.get("specificity", 0))
    print_score_bar("Context", data.get("context", 0))
    print_score_bar("Constraints", data.get("constraints", 0))
    print_score_bar("Format", data.get("format", 0))
    print(f"├────────────────────────────────────┤")
    print_score_bar("OVERALL", data.get("overall", 0))
    print(f"└────────────────────────────────────┘\n")

    feedback = data.get("feedback", "")
    if feedback:
        print(f"💬 {feedback}")


def cmd_optimize(args):
    """Optimize a rough prompt idea."""
    prompt = args.prompt or read_stdin()
    if not prompt:
        print("Error: Provide a prompt as argument or via stdin", file=sys.stderr)
        sys.exit(1)

    print("Optimizing prompt...\n", file=sys.stderr)
    result = call_api(OPTIMIZE_PROMPT.format(prompt=prompt), args.api_key, args.base_url, args.model)

    print("Optimized prompt:\n")
    print("─" * 50)
    print(result)
    print("─" * 50)

    if args.copy:
        import subprocess
        try:
            subprocess.run(["clip"], input=result.encode(), check=True)
            print("\n(Copied to clipboard)")
        except Exception:
            pass


def read_stdin():
    """Read from stdin if available."""
    if sys.stdin.isatty():
        return ""
    return sys.stdin.read().strip()


def main():
    parser = argparse.ArgumentParser(
        prog="prompt-polish",
        description="Analyze and improve your AI prompts with one command"
    )
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("-k", "--api-key", help="API key (or set PROMPT_POLISH_API_KEY)")
    parser.add_argument("-u", "--base-url", help="API base URL")
    parser.add_argument("-m", "--model", help="Model name")
    parser.add_argument("-c", "--copy", action="store_true", help="Copy result to clipboard")

    sub = parser.add_subparsers(dest="command")

    # analyze
    p_analyze = sub.add_parser("analyze", aliases=["a"], help="Analyze & improve a prompt")
    p_analyze.add_argument("prompt", nargs="?", help="The prompt to analyze")

    # score
    p_score = sub.add_parser("score", aliases=["s"], help="Score a prompt (5 dimensions)")
    p_score.add_argument("prompt", nargs="?", help="The prompt to score")

    # optimize
    p_opt = sub.add_parser("optimize", aliases=["o"], help="Turn rough idea into polished prompt")
    p_opt.add_argument("prompt", nargs="?", help="Your rough prompt idea")

    args = parser.parse_args()

    if not args.command:
        # Default: analyze
        args.command = "analyze"
        args.prompt = None
        args.copy = False

    if args.command in ("analyze", "a"):
        cmd_analyze(args)
    elif args.command in ("score", "s"):
        cmd_score(args)
    elif args.command in ("optimize", "o"):
        cmd_optimize(args)


if __name__ == "__main__":
    main()
