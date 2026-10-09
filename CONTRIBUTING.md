# Contributing to Vyra (Wealth OS)

First off, thank you for considering contributing to Vyra! It's people like you that make Vyra such a great tool for personal finance and wealth management.

## 1. Where do I go from here?

If you've noticed a bug or have a feature request, make sure to check our [Issues](../../issues) first. If it doesn't exist, feel free to open a new issue!

## 2. Fork & create a branch

If this is something you think you can fix, then fork Vyra and create a branch with a descriptive name.

```bash
git checkout -b your-branch-name
```

## 3. Local Development Setup

1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment.
4. Install dependencies (make sure `requirements.txt` is updated).
5. Run migrations: `python manage.py migrate`
6. Run the server: `python manage.py runserver`

## 4. Coding Standards

- **Python:** Follow PEP 8 guidelines.
- **Django:** Keep business logic separated from views (use `services.py` if necessary). Keep models fat and views skinny.
- **Frontend:** Use vanilla JS and Bootstrap 5 (Neumorphic design system) to keep it consistent.

## 5. Submitting a Pull Request

- Ensure any new features are covered by tests.
- Update the documentation if your changes require it.
- Open a Pull Request with a clear title and description against the `main` branch.

We actively welcome your pull requests!
