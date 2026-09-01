# CrewAI-Agents

Multi-agent system built with [CrewAI](https://www.crewai.com/) for orchestrating AI agents that work together to accomplish complex tasks — including a **QA Bug Triage Crew** that reads live Jira tickets and produces a full triage report (classification → root cause → test strategy).

CrewAI is a Python framework for orchestrating role-based LLM agents. It offers two complementary approaches:

- **Crews** — teams of agents with autonomy, collaborating through role-based delegation
- **Flows** — event-driven workflows that give precise control over execution paths

## Status

Working. The QA Bug Triage Crew runs end-to-end against a live Jira site (see `04_Build_QABugTriageCrew_Prod_openrouter.py`).

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (Python version manager + package manager)
- [OpenRouter](https://openrouter.ai/) API key (one key gives access to many models — DeepSeek, etc.)
- A Jira Cloud site with an **email + API token** for the REST API (or an MCP server)

## Getting Started

### 1. Set up the environment

```powershell
uv sync                  # install everything from uv.lock into .venv
.\.venv\Scripts\Activate.ps1
```

Your terminal prompt should show `(crewai-agents)` when active. Alternatively skip activation — `uv run python <script>` uses the project environment automatically.

### 2. Configure `.env`

Copy `.env.example` to `.env` and fill in your values:

```powershell
copy .env.example .env   # then edit .env
```

Required variables:

| Variable | Purpose |
|----------|---------|
| `OPENROUTER_API_KEY` | OpenRouter API key |
| `OPENROUTER_MODEL` | Model id, e.g. `openrouter/deepseek/deepseek-v4-flash` |
| `BASE_URL` | `https://openrouter.ai/api/v1` |
| `JIRA_URL` / `JIRA_BASE_URL` | Your Jira site, e.g. `https://your-site.atlassian.net` |
| `JIRA_EMAIL` | Login email for Jira REST API |
| `JIRA_API_TOKEN` | Jira API token (not your password) |
| `BUG_ID` | Issue key to analyze, e.g. `IS-6` |

### 3. Configure CrewAI to use OpenRouter

CrewAI uses LiteLLM under the hood, so point it at OpenRouter in your agent code:

```python
from crewai import LLM

llm = LLM(
    model="openrouter/deepseek/deepseek-v4-flash",  # any model from openrouter.ai/models
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
)
```

Then pass `llm=llm` when creating your Agent.

### 4. Run the scripts

```powershell
uv run python 01_test_analyst_Agent.py                     # single QA agent -> test cases
uv run python 02_Research_Write_AI_Agent.py                # researcher + writer crew
uv run python 03_Build_QABugTriageCrew.py                  # basic triage crew
uv run python 04_Build_QABugTriageCrew_Prod_openrouter.py  # full triage crew, live Jira
```

The production triage crew (04) does:

1. **Fetch a bug from Jira** via REST API v3 (`JIRA_BASE_URL` + email/token, or a cached copy in `bug_cache/` if the fetch fails)
2. **Agent 1 — Bug Triage Analyst**: Severity (S0–S4), Priority (P0–P4), Category, Business Impact, Confidence
3. **Agent 2 — Root Cause Investigator**: differential diagnosis, 3 ranked hypotheses with kill tests, suspect layer, blast radius
4. **Agent 3 — Test Strategy Advisor**: missing test, regression set, edge cases, runnable Playwright TypeScript

Each agent runs with its own output-token budget because the prompt grows as context is chained.

### 5. Publish

The `publish/` folder contains a LinkedIn post and a 1200×630 HTML share card for the QA Bug Triage Crew — see `publish/README.md`.

## Windows / corporate network notes

- **Zscaler TLS inspection**: external HTTPS calls (OpenRouter, Jira) fail with `CERTIFICATE_VERIFY_FAILED` because the corporate proxy presents a private CA that certifi doesn't trust. The 04 script disables verification for the Jira fetch (`verify=False`) and disables CrewAI telemetry for local dev. Swap in the real Zscaler root CA for production.
- **Emoji in console**: the scripts force UTF-8 stdout so emoji output doesn't crash on the cp1252 Windows console.

## Managing Packages

```powershell
uv add crewai          # add a new dependency
uv remove crewai       # remove a dependency
uv pip list            # list installed packages
uv sync                # install everything from uv.lock
```

## Project Structure

```
CrewAI-Agents/
├── .venv/              # Virtual environment — Python + installed packages (crewai, etc.)
├── src/
│   └── crewai_agents/  # Package source from `uv init` (src layout). NOT required
│       └── __init__.py # if you write scripts at the project root.
├── .python-version     # Pins the Python version for this folder
├── pyproject.toml      # Project identity + dependencies
├── uv.lock             # Lock file — pins exact dependency versions
├── .env                # Your secrets — git-ignored, never commit
├── .env.example        # Template for .env
├── 01_test_analyst_Agent.py
├── 02_Research_Write_AI_Agent.py
├── 03_Build_QABugTriageCrew.py
├── 04_Build_QABugTriageCrew_Prod.py          # Groq/DeepSeek fallback variant
├── 04_Build_QABugTriageCrew_Prod_openrouter.py  # OpenRouter variant (primary)
├── publish/
│   ├── linkedin_post.md
│   ├── linkedin_card.html
│   └── README.md
└── README.md           # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes
4. Push to the branch
5. Open a pull request

## License

TBD
