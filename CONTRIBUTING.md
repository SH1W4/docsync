# Contributing to DocSync

First off, thanks for taking the time to contribute! 🎉
The following is a set of guidelines for contributing to DocSync and its packages.

## 🧠 Philosophy

DocSync is an **Agentic Infrastructure** tool. We prioritize:
1.  **Machine Reliability:** Code must be deterministic and typed (MyPy strict).
2.  **Human Clarity:** Documentation logic must be clear enough for an LLM to follow.

## 🛠️ Development Setup

1.  **Clone the repo**
    ```bash
    git clone https://github.com/SH1W4/docsync.git
    cd docsync
    ```

2.  **Install dependencies**
    ```bash
    padding install -e ".[dev]"
    pre-commit install
    ```

##  workflow

1.  Create your branch from `main`.
2.  If you've added code that should be tested, add tests.
3.  If you've changed APIs, update the documentation.
4.  Ensure the test suite passes.
5.  Make sure your code lints.

## 🧪 Testing

We use `pytest`.
```bash
pytest
```

## 📝 Commit Messages

We adhere to the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.
- `feat`: structure for features
- `fix`: structure for bug fixes
- `docs`: documentation only changes
- `chore`: maintenance tasks

## 🤖 AI Co-Authoring

If you used AI to generate code, please tag it in the PR description so we can validate loop hallucinations.

---
Happy Coding!
