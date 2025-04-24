# **Project: AI Code Review Agent**

**Objective**: Build a local or prompt-based AI agent that can analyze Python code, detect potential issues, suggest improvements, and act like a code reviewer.

---

## Project Overview

You’ll build a Python-based agent that can:

- Accept code files or code snippets
- Analyze for bugs, clarity, readability, and standards
- Suggest improvements using prompt templates
- Generate a review summary in Markdown or terminal output

You will use GenAI tools:

- **LLM APIs**: like OpenAI or Claude (via key-based config)
- **Local Ollama Models**: using models like `mistral`, `phi`, etc.

and optionally integrate `streamlit`, or just structure the logic using functions.

---

## Core Design Principles

### **Dual Mode Interface**

- CLI flag or config setting: `--provider openai`, `--provider ollama`, `--provider anthropic`
- Abstracted prompt runner in a `llm_interface.py` module

### 📂 **Project Structure**

```bash
code_review_agent/
├── agent/
│   ├── analyzer.py          # Review logic + prompt construction
│   └── llm_interface.py     # Unified API/Ollama abstraction
├── examples/
│   ├── buggy_script.py
│   └── clean_script.py
├── prompts/
│   └── templates.yaml       # Stores different prompt styles
├── reviews/
│   └── review_output.md
├── cli.py                   # Command-line runner
├── config.yaml              # API keys, model config
├── README.md
└── requirements.txt
```

---

## Features

### 🔍 Review Targets

- Input: one or more Python files
- Output: markdown summary of:
  - Bugs
  - Style issues
  - Missing tests
  - Clarity suggestions

### 💬 Prompt Profiles

In `prompts/templates.yaml`:

```yaml
strict:
  description: Act as a strict code reviewer...
mentor:
  description: Pretend you are mentoring a junior...
test_focus:
  description: Focus only on missing or weak tests...
```

### `llm_interface.py`

```python
class LLMClient:
    def __init__(self, provider, model):
        ...

    def run(self, prompt, code_snippet):
        if self.provider == "openai":
            return self._call_openai(prompt, code_snippet)
        elif self.provider == "ollama":
            return self._call_ollama(prompt, code_snippet)
        elif self.provider == "anthropic":
            return self._call_claude(prompt, code_snippet)
```

---

## Example CLI Usage

```bash
python cli.py --file examples/buggy_script.py --mode strict --provider ollama
```

```bash
python cli.py --file examples/clean_script.py --mode mentor --provider openai
```

---

## Requirements

### `requirements.txt`:

```text
openai
pyyaml
requests
anthropic
```

> Optional: Add `streamlit` if you want a GUI later.

---
