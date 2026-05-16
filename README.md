# Agentic SemVer Auto-Tagger

A practical study lab for the **GH-600 Agentic AI Developer** exam. This project implements a lightweight AI agent that analyzes a repository's Git commit history and intelligently determines the next Semantic Version (SemVer) tag using a Large Language Model.

## 🎯 Architecture & Exam Objectives

This repository is designed to demonstrate core agentic design patterns rather than just making simple API calls. It explicitly implements the following GH-600 domains:

*   **Boundary Definition (Planning vs. Execution):** The agent does not execute tags directly. It first analyzes the `git log` and outputs a strict, inspectable JSON plan detailing its reasoning, the highest impact commit, and the proposed tag.
*   **Human-in-the-Loop (HITL) Governance:** To ensure safe deployment, the agent pauses execution and posts its proposed plan to a Pull Request. It requires explicit human authorization (e.g., an `/approve` comment) before triggering the Git tag action.
*   **State Management & Observability:** The agent's intermediate reasoning and API responses are logged and persisted as GitHub Action artifacts, ensuring a durable audit trail if the multi-step workflow fails.

## 📂 Repository Structure

```text
.
├── .github/
│   ├── workflows/
│   │   └── auto-tag.yml       # Orchestrates the trigger, HITL pause, and execution
│   └── scripts/
│       └── suggest_tag.py     # The Python agent logic (Context gathering & LLM reasoning)
├── app.py                     # Dummy application file for generating test commits
└── README.md                  # This file
