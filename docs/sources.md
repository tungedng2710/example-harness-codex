# Verified official references

Access date for every entry: 2026-11-04. Pages opened through the web tool;
claims below are concise paraphrases. Markdown-suffix fetches for the first two
failed due to tool content-type handling; their HTML pages were successfully read.
No quoted benchmark or product pricing is used.

| Title | URL | Supported claim |
| --- | --- | --- |
| Custom instructions with AGENTS.md | https://learn.chatgpt.com/docs/agent-configuration/agents-md | Repository guidance is combined with inherited/global guidance; nested instructions matter. |
| Build skills | https://learn.chatgpt.com/docs/build-skills | SKILL.md front matter; progressive loading; repository .agents/skills discovery and explicit invocation. |
| Codex as a platform: build on the open agent harness | https://developers.openai.com/blog/codex-as-a-platform | Runtime handles context, tools, execution, configured boundaries and approvals; separate from model. |
| Customization | https://learn.chatgpt.com/docs/customization/overview | Instructions and skills are customization surfaces; availability does not prove invocation. |
| Command line options — Codex CLI | https://learn.chatgpt.com/docs/cli/reference | -C working directory; profiles layer config; ignore-user-config only skips config.toml. Also compared with local 0.166.0 help. |
| Testing — FastAPI | https://fastapi.tiangolo.com/tutorial/testing/ | TestClient allows application tests in process. |
| Working on projects — uv | https://docs.astral.sh/uv/guides/projects/ | Project environment, lock and synchronization workflows. |
| How to invoke pytest | https://docs.pytest.org/en/stable/how-to/usage.html | Explicit path selection and python -m pytest invocation. |
| Ruff | https://docs.astral.sh/ruff/ | Python linting and formatting tooling. |

Repository algorithms, scoring choices, repair limit and experimental design are
this project's conventions, not product requirements. No A/B/C outcomes exist.
