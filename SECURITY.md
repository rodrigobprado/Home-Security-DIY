# Security Policy

Thank you for your interest in the security of **Home Security DIY**, an open-source residential security system project licensed under [GPL v3](LICENSE).

> **Note:** This project is currently in the **planning phase (v0.1)**. There is no production code yet. Most security considerations, architectural decisions, and compliance requirements are documented in the [`docs/`](docs/) and [`rules/`](rules/) directories. This security policy will evolve as the project matures.

---

## Supported Versions

| Version | Status           | Support Level       |
|---------|------------------|---------------------|
| v0.1    | Planning phase   | Documentation only  |

As the project progresses beyond the planning phase and releases working code, this table will be updated to reflect which versions receive active security support.

---

## Reporting a Vulnerability

We take security seriously, even during the planning phase. If you discover a security vulnerability in this project, please report it responsibly.

### How to Report

1. **Preferred method:** Use [GitHub Security Advisories](https://github.com/rodrigo/Home-Security-DIY/security/advisories/new) to submit a private vulnerability report directly through GitHub. This ensures the report remains confidential until a fix is available.

2. **Fallback method:** If you are unable to use GitHub Security Advisories, you may send an email describing the vulnerability. Please include `[SECURITY]` in the subject line. Contact details will be provided in the repository's profile or through GitHub Discussions.

### What to Include in Your Report

To help us understand and address the issue efficiently, please include the following in your report:

- **Description:** A clear and concise description of the vulnerability.
- **Steps to reproduce:** Detailed steps that allow us to reproduce the issue, including any relevant configuration, environment details, or sample inputs.
- **Impact assessment:** Your assessment of the potential impact (e.g., data exposure, unauthorized access, denial of service, physical security compromise).
- **Affected components:** Which part of the project is affected (documentation, architecture design, configuration recommendations, code, hardware integration, etc.).
- **Suggested fix (optional):** If you have a recommendation for how to address the vulnerability, we welcome your input.

### Response Timeline

| Action                     | Expected Timeframe     |
|----------------------------|------------------------|
| Acknowledgment of report   | Within 72 hours        |
| Initial triage and assessment | Within 1 week       |
| Status update to reporter  | At least every 2 weeks |
| Fix or mitigation plan     | Varies by severity     |

We will do our best to meet these timelines. If a delay occurs, we will communicate the reason and provide an updated estimate.

---

## Scope

The following areas are **in scope** for security reports:

- **Documentation recommendations:** Security flaws in documented best practices, installation guides, or configuration recommendations found in `docs/` and `rules/`.
- **Architecture and design:** Vulnerabilities in the proposed system architecture, network topology, communication protocols, or data flow designs.
- **Future code and configurations:** Security issues in any code, scripts, configuration files, or automation workflows committed to this repository.
- **Dependency vulnerabilities:** Known vulnerabilities in third-party libraries or tools recommended or used by this project.
- **CI/CD and infrastructure:** Security issues in GitHub Actions workflows, build pipelines, or repository configuration.

---

## Out of Scope

The following are **not covered** by this security policy:

- **Individual hardware vulnerabilities from vendors:** Security flaws in third-party hardware products (cameras, sensors, controllers, NVR devices, etc.) that are recommended or referenced by this project but are not developed or maintained here. Please report these directly to the respective hardware vendors.
- **Third-party service vulnerabilities:** Security issues in external services (cloud providers, DNS services, ISPs) that the project may reference or integrate with.
- **Physical security of your installation:** While we provide guidance on physical security best practices, we cannot be responsible for vulnerabilities arising from individual installation decisions or environmental factors.
- **Social engineering attacks:** Attacks targeting individual users or contributors rather than the project itself.

---

## Disclosure Policy

This project follows a **coordinated disclosure** approach:

1. **Confidentiality:** All vulnerability reports will be handled confidentially. We will not disclose the details of a vulnerability until a fix or mitigation is available.
2. **90-day timeline:** We aim to resolve reported vulnerabilities within **90 days** of the initial report. If a fix requires more time, we will work with the reporter to agree on an appropriate disclosure date.
3. **Public disclosure:** Once a fix is released, we will publish a security advisory on GitHub describing the vulnerability, its impact, and the remediation steps taken.
4. **Credit:** Reporters will be credited in the advisory unless they request anonymity (see [Recognition](#recognition) below).
5. **No legal action:** We will not pursue legal action against researchers who report vulnerabilities in good faith and follow this disclosure policy.

---

## Recognition

We believe in recognizing the contributions of security researchers who help improve this project:

- Reporters will be **credited by name** (or preferred alias) in the relevant release notes and security advisories.
- A dedicated **Security Hall of Fame** section may be added to the project documentation as the contributor base grows.
- If you wish to remain **anonymous**, please let us know in your report and we will respect that preference.

---

## Additional Resources

- [Project Documentation](docs/)
- [Technical Rules and Compliance](rules/)
- [Architecture Overview](docs/ARCHITECTURE.md)
- [License (GPL v3)](LICENSE)

---

*This security policy is effective as of the project's planning phase (v0.1) and will be updated as the project evolves.*
