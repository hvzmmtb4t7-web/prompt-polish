# prompt-polish

> Your prompts deserve better. Analyze, score, and optimize them in seconds.

A CLI tool that uses AI to evaluate and improve your prompts for ChatGPT, Claude, DeepSeek, or any LLM.

## Install

```bash
git clone https://github.com/hvzmmtb4t7-web/prompt-polish.git
cd prompt-polish

# Zero dependencies — just copy the file
cp prompt_polish.py /usr/local/bin/prompt-polish
chmod +x /usr/local/bin/prompt-polish
```

**Zero dependencies** — only Python 3.7+ stdlib.

## Quick Start

```bash
# Set your API key
export PROMPT_POLISH_API_KEY="sk-xxx"
export PROMPT_POLISH_BASE_URL="https://api.deepseek.com/v1"
export PROMPT_POLISH_MODEL="deepseek-chat"

# Analyze a prompt
python prompt_polish.py analyze "帮我写个代码"

# Score a prompt
python prompt_polish.py score "写一个Python函数，输入一个列表，返回去重后的排序结果"

# Optimize a rough idea
python prompt_polish.py optimize "帮我写个爬虫"
```

## Commands

### `analyze` — Analyze & Improve

Shows what's wrong with your prompt and gives you an improved version.

```bash
python prompt_polish.py analyze "帮我写个代码"
```

Output:
```
┌─ Prompt Score ─────────────────────┐
  Overall      ███░░░░░░░ 3/10
└────────────────────────────────────┘

⚠  Issues found:
   1. Extremely vague — no language, no task specifics
   2. No context about what you're building
   3. No output format requirements

✨ What was improved:
   • Added specific programming language
   • Defined the actual task
   • Added output format and constraints

──────────────────────────────────────────────────
Improved prompt:

Write a Python function called `deduplicate_and_sort` that takes a list of
integers as input and returns a new list with duplicates removed, sorted in
ascending order. Include type hints and a docstring with examples.
──────────────────────────────────────────────────
```

### `score` — Rate Your Prompt

Get a detailed breakdown across 5 dimensions.

```bash
python prompt_polish.py score "解释量子计算"
```

```
┌─ Prompt Score Breakdown ───────────┐
  Clarity      ██████░░░░ 6/10
  Specificity  ███░░░░░░░ 3/10
  Context      ██░░░░░░░░ 2/10
  Constraints  █░░░░░░░░░ 1/10
  Format       ██░░░░░░░░ 2/10
├────────────────────────────────────┤
  OVERALL      ███░░░░░░░ 3/10
└────────────────────────────────────┘

💬 Too vague — needs audience level, specific aspects, and output format.
```

### `optimize` — Polish a Rough Idea

Turn a half-baked thought into a well-structured prompt.

```bash
python prompt_polish.py optimize "帮我写个爬虫"
```

```
Optimized prompt:

──────────────────────────────────────────────────
You are an expert Python developer specializing in web scraping.

**Task:** Write a Python web scraper that:

1. **Target:** [Specify the website URL]
2. **Data to extract:** [Specify what data you need]
3. **Output format:** CSV file with columns: [list columns]
4. **Requirements:**
   - Use `requests` + `BeautifulSoup` (or `playwright` for JS-rendered pages)
   - Handle pagination if applicable
   - Add rate limiting (1 request per second)
   - Include error handling and retry logic
   - Add logging for debugging

**Constraints:**
- Python 3.8+
- Respect robots.txt
- Include a `requirements.txt`

Please provide the complete, runnable code with comments explaining key sections.
──────────────────────────────────────────────────
```

## Pipe Support

```bash
# Read from stdin
echo "帮我写个API" | python prompt_polish.py analyze

# Pipe from clipboard (Windows)
powershell Get-Clipboard | python prompt_polish.py score
```

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `PROMPT_POLISH_API_KEY` | API key | (required) |
| `PROMPT_POLISH_BASE_URL` | API base URL | `https://api.deepseek.com/v1` |
| `PROMPT_POLISH_MODEL` | Model name | `deepseek-chat` |

Also supports `OPENAI_API_KEY` and `DEEPSEEK_API_KEY` as fallbacks.

## Why?

Most people write prompts like:
- "帮我写个代码" → **3/10**
- "解释量子计算" → **3/10**
- "写个爬虫" → **2/10**

With prompt-polish, you learn **why** your prompts are weak and get **instant fixes**.

Better prompts = better AI output. Every time.

## License

MIT
