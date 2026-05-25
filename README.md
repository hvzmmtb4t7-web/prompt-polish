# prompt-polish

> Your prompts deserve better. Analyze, score, and optimize them in seconds.

A CLI tool that uses AI to evaluate and improve your prompts for ChatGPT, Claude, DeepSeek, or any LLM.

> **你的提示词值得更好。一键分析、评分、优化。**
>
> 用 AI 评估和改进你的 ChatGPT / Claude / DeepSeek 提示词。零依赖，Python 3.7+ 标准库即可运行。

## Install / 安装

```bash
git clone https://github.com/hvzmmtb4t7-web/prompt-polish.git
cd prompt-polish

# Zero dependencies — just copy the file / 零依赖，直接复制文件
cp prompt_polish.py /usr/local/bin/prompt-polish
chmod +x /usr/local/bin/prompt-polish
```

**Zero dependencies** — only Python 3.7+ stdlib.

**零依赖** — 只需 Python 3.7+ 标准库。

## Quick Start / 快速开始

```bash
# Set your API key / 设置 API Key
export PROMPT_POLISH_API_KEY="sk-xxx"
export PROMPT_POLISH_BASE_URL="https://api.deepseek.com/v1"
export PROMPT_POLISH_MODEL="deepseek-chat"

# Analyze a prompt / 分析一个提示词
python prompt_polish.py analyze "帮我写个代码"

# Score a prompt / 给提示词打分
python prompt_polish.py score "写一个Python函数，输入一个列表，返回去重后的排序结果"

# Optimize a rough idea / 把粗糙想法优化成好提示词
python prompt_polish.py optimize "帮我写个爬虫"
```

## Commands / 命令

### `analyze` — Analyze & Improve / 分析并改进

Shows what's wrong with your prompt and gives you an improved version.

展示提示词的问题，并给出改进版本。

```bash
python prompt_polish.py analyze "帮我写个代码"
```

Output / 输出:
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

### `score` — Rate Your Prompt / 给提示词打分

Get a detailed breakdown across 5 dimensions.

从5个维度详细评分。

```bash
python prompt_polish.py score "解释量子计算"
```

```
┌─ Prompt Score Breakdown ───────────┐
  Clarity      ██████░░░░ 6/10     清晰度
  Specificity  ███░░░░░░░ 3/10     具体度
  Context      ██░░░░░░░░ 2/10     上下文
  Constraints  █░░░░░░░░░ 1/10     约束条件
  Format       ██░░░░░░░░ 2/10     输出格式
├────────────────────────────────────┤
  OVERALL      ███░░░░░░░ 3/10     总分
└────────────────────────────────────┘

💬 Too vague — needs audience level, specific aspects, and output format.
```

### `optimize` — Polish a Rough Idea / 把粗糙想法变成好提示词

Turn a half-baked thought into a well-structured prompt.

把一个模糊的想法变成结构清晰的提示词。

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

## Pipe Support / 管道支持

```bash
# Read from stdin / 从标准输入读取
echo "帮我写个API" | python prompt_polish.py analyze

# Pipe from clipboard (Windows) / 从剪贴板读取（Windows）
powershell Get-Clipboard | python prompt_polish.py score
```

## Environment Variables / 环境变量

| Variable | Description / 说明 | Default / 默认值 |
|---|---|---|
| `PROMPT_POLISH_API_KEY` | API key / API 密钥 | (required) |
| `PROMPT_POLISH_BASE_URL` | API base URL / API 地址 | `https://api.deepseek.com/v1` |
| `PROMPT_POLISH_MODEL` | Model name / 模型名称 | `deepseek-chat` |

Also supports `OPENAI_API_KEY` and `DEEPSEEK_API_KEY` as fallbacks.

也支持 `OPENAI_API_KEY` 和 `DEEPSEEK_API_KEY` 作为备选。

## Why? / 为什么用这个？

Most people write prompts like / 大多数人写提示词是这样的：

- "帮我写个代码" → **3/10**
- "解释量子计算" → **3/10**
- "写个爬虫" → **2/10**

With prompt-polish, you learn **why** your prompts are weak and get **instant fixes**.

用 prompt-polish，你能知道提示词**为什么**差，并**立刻修复**。

Better prompts = better AI output. Every time.

更好的提示词 = 更好的 AI 输出。每次都是。

## License

MIT
