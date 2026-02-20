# Contributing to AI Personal Employee

Thank you for your interest in contributing to the AI Personal Employee project! This document provides guidelines for contributing.

---

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Your environment (OS, Python version, etc.)
- Relevant logs or screenshots

### Suggesting Features

Feature requests are welcome! Please open an issue with:
- Clear description of the feature
- Use case and benefits
- Possible implementation approach (optional)

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Follow the existing code style
   - Add tests if applicable
   - Update documentation
4. **Test your changes**
   ```bash
   python quick_test.py
   ```
5. **Commit your changes**
   ```bash
   git commit -m "Add: your feature description"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request**

---

## 📝 Code Style Guidelines

### Python Code
- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small
- Add comments for complex logic

### Documentation
- Update README.md if adding new features
- Update command guides in `.claude` directory
- Add examples for new functionality
- Keep documentation clear and concise

### Commit Messages
Use clear, descriptive commit messages:
- `Add: new feature description`
- `Fix: bug description`
- `Update: what was updated`
- `Docs: documentation changes`
- `Test: test-related changes`

---

## 🧪 Testing

Before submitting a PR:

1. **Run all tests**
   ```bash
   python quick_test.py
   ```

2. **Test individual components**
   ```bash
   python test_gmail_manual.py
   python linkedin_safety_check.py
   python test_whatsapp_send.py
   ```

3. **Check for errors**
   - Review logs in `AI_Employee_Vault/Logs/`
   - Ensure no credentials are exposed
   - Verify .gitignore is working

---

## 🔒 Security

### Never Commit
- Real credentials or API keys
- .env files
- Browser session data
- Personal information
- Logs with sensitive data

### Always
- Use .env.example for templates
- Keep credentials in .env (gitignored)
- Review changes before committing
- Use environment variables for secrets

---

## 📖 Documentation

When adding new features:

1. **Update README.md**
   - Add to features list
   - Update usage examples
   - Add to table of contents if needed

2. **Update Command Guides**
   - Add commands to `.claude/ALL_COMMANDS.md`
   - Create platform-specific guide if needed
   - Update quick reference card

3. **Add Examples**
   - Provide usage examples
   - Include expected output
   - Document edge cases

---

## 🎯 Areas for Contribution

### High Priority
- [ ] Improve error handling
- [ ] Add more comprehensive tests
- [ ] Enhance LinkedIn safety system
- [ ] Add more platform integrations
- [ ] Improve documentation

### Medium Priority
- [ ] Add GUI interface
- [ ] Create Docker container
- [ ] Add more MCP servers
- [ ] Improve logging system
- [ ] Add analytics dashboard

### Low Priority
- [ ] Add more batch files
- [ ] Create video tutorials
- [ ] Add more examples
- [ ] Improve code comments
- [ ] Add internationalization

---

## 🐛 Known Issues

Check the [Issues](https://github.com/yourusername/AI_personal_Employee/issues) page for current known issues and feature requests.

---

## 💬 Questions?

If you have questions about contributing:
- Open an issue with the "question" label
- Check existing documentation
- Review closed issues for similar questions

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🙏 Thank You!

Every contribution helps make this project better. Thank you for taking the time to contribute!

---

**Last Updated:** 2026-02-20
