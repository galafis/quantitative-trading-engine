# Contributing to Quantitative Trading Engine

Thank you for your interest in contributing to the Quantitative Trading Engine! This document provides guidelines and instructions for contributing.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Error messages and stack traces

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:
- Clear description of the proposed feature
- Use case and benefits
- Possible implementation approach
- Examples of similar features in other projects

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Add tests** for new functionality
5. **Ensure all tests pass** (`pytest`)
6. **Update documentation** if needed
7. **Commit your changes** (`git commit -m 'Add amazing feature'`)
8. **Push to the branch** (`git push origin feature/amazing-feature`)
9. **Open a Pull Request**

## 📋 Development Guidelines

### Code Style

- Follow **PEP 8** style guide
- Use **type hints** for all functions
- Write **docstrings** for all public functions (Google style)
- Keep functions small and focused (< 50 lines)
- Use meaningful variable names

### Testing

- Write unit tests for all new code
- Maintain test coverage above 80%
- Use pytest fixtures for common setups
- Mock external dependencies (databases, APIs)

### Documentation

- Update README.md for new features
- Add docstrings to all public functions
- Include usage examples
- Update API documentation if endpoints change

### Commit Messages

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(strategies): add volatility breakout strategy
fix(backtest): correct commission calculation
docs(readme): update installation instructions
```

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_strategies.py

# Run with verbose output
pytest -v
```

## 🔍 Code Review Process

All submissions require review. We use GitHub pull requests for this purpose:

1. **Code Review**: Maintainer reviews code quality and design
2. **Feedback**: Address any requested changes
3. **Approval**: Once approved, code will be merged

## 📝 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 💬 Questions?

Feel free to open an issue for any questions about contributing!

---

**Author**: Gabriel Demetrios Lafis
