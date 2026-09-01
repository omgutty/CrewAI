# LinkedIn Post — QA Bug Triage Crew

**Post text (copy-paste ready):**

---

🤖 **I built an AI Bug Triage Crew that reads Jira tickets and produces a full triage report in minutes.**

A daily 30-person triage meeting used to burn ~300 hours a month just gathering context. This crew pre-processes every ticket before you even sit down — so the meeting becomes decisions, not data gathering.

**How it works — 3 specialized agents in sequence:**

🔍 **1. Bug Triage Analyst** — Severity (S0–S4), Priority (P0–P4), Category, Business Impact & Confidence, with evidence quoted straight from the ticket.

🕵️ **2. Root Cause Investigator** — Differential diagnosis, 3 ranked hypotheses each with a kill test, the suspect system layer, and blast radius.

🧪 **3. Test Strategy Advisor** — The missing test, a regression set, boundary & edge cases, and **runnable Playwright TypeScript** — each pinned to the cheapest layer that catches the bug.

**The stack:**
• CrewAI — multi-agent orchestration
• OpenRouter (DeepSeek) — LLM provider
• Atlassian Jira REST API — live bug data
• Sequential process — each agent builds on the previous output

**The result:** a structured, consistent, evidence-backed verdict for every ticket. Same quality bar, every single time — no meeting prep needed.

Built as a self-learning project on my own time — details are in the code, happy to share.

#QA #AI #CrewAI #SoftwareTesting #Jira

---

**Alternative: longer hashtag set**
`#CrewAI #QA #AI #SoftwareTesting #Jira #OpenRouter #Automation #RootCauseAnalysis #Playwright`
