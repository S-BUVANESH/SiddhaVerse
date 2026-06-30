---
description: To efficiently use quota/tokens.
---

When generating any output:
- Assume the user has full context of the project
- Skip all background/context sections
- Omit "why" unless asked — only give "what" and "how"
- Max response length: fit within 800 tokens unless task demands more
- For code: write the final version directly, no draft→refine loop