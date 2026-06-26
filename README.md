# Prismor: The Zero Trust Layer for AI Agents

**Live Whitepaper:** https://www.prismor.dev/whitepaper

**GitHub Repository:** https://github.com/romyilano/prismor-whitepaper

---

## Documentation

### Whitepaper: The Zero Trust Layer for AI Agents

#### Overview

Prismor presents a security framework designed to enable AI agents to operate efficiently while maintaining protective guardrails through continuous monitoring.

#### The Core Problem

##### The Current Dilemma

Modern AI coding agents have become production-capable systems that can open pull requests, rewrite services, and deploy code independently. However, this autonomy creates a critical tension: developers must choose between two problematic approaches.

The first option involves manually approving each agent action—a labor-intensive process that wastes agent productivity. The second requires disabling safety mechanisms entirely through deliberately-named flags like `--dangerously-skip-permissions`, acknowledging the risk while accepting it anyway.

##### Threat Landscape

Recent security data underscores the urgency:

- CrowdStrike reported an 89% increase in AI-driven attacks during 2025-2026
- Attack propagation timelines have compressed to 29 minutes on average, with incidents occurring in as little as 27 seconds
- The LiteLLM supply chain incident (March 2026) demonstrated how poisoned packages can achieve tens of thousands of installations within 40 minutes

##### Identity and Access Challenges

The underlying infrastructure compounds these risks:

- Machine identities now outnumber human users by approximately 80:1 in typical enterprises
- Roughly 97% of these identities possess excessive permissions relative to their functional requirements
- Only 16% of organizations can confidently detect agent-specific threats
- 82% have discovered unauthorized AI agents already operating in their environments

#### The Immunity Solution

Prismor's answer centers on implementing continuous zero-trust verification—treating each agent action as requiring explicit authorization rather than relying on identity or reputation.

##### Four Protective Components

**Warden** functions as the enforcement layer, evaluating every command before execution. It applies deterministic rules and AI-powered gates to block dangerous operations, with specific protections (disk wiping, reverse shells, security circumvention) that cannot be disabled.

**Cloak** prevents credential exposure by intercepting API keys and passwords at the moment agents attempt unauthorized movement, before secrets can embed themselves in logs or external requests.

**IAM** implements granular role-based access, assigning each agent a specific function with corresponding permissions. A read-only research agent cannot write, deploy, or access sensitive data, even if compromised mid-operation.

**Semantic Guard** analyzes intent through language processing to catch instruction injection attacks—adversarial prompts embedded in files or web content that attempt to override agent directives. This capability reportedly improves detection rates by approximately 30%.

##### Package Management Protection

The immunity-agent CLI wraps package installation across pip, npm, and seven additional package managers. Each package receives a risk assessment before installation, with known-malicious packages rejected immediately and suspicious packages (newly published, anonymous ownership, environment-variable targeting) flagged with guidance toward safe alternatives.

#### Addressing Existing Vulnerabilities

##### Auto-Fix Agent

Rather than only preventing future threats, Prismor addresses accumulated security debt through automated remediation. The Auto-Fix Agent identifies known vulnerabilities, generates patches, and opens pull requests for human review. This approach maintains safety by:

- Keeping patches small and focused on specific flaws
- Requiring human approval before any deployment
- Preventing fixes that would break existing functionality

Industry data shows average remediation timelines reach approximately 58 days—Prismor's automation allows organizations to address vulnerabilities during normal development cycles rather than emergency incident response.

#### Regulatory and Compliance Context

The EU's Cyber Resilience Act ties software marketability in European regions to supply-chain security documentation. Prismor's monitoring generates Software Bill of Materials (SBOMs) and Vulnerability Exploit eXchange (VEX) reports as byproducts of its protective operations, satisfying compliance requirements automatically.

#### Implementation

The setup process requires approximately 30 seconds, with agents capable of self-configuring Prismor integration through guided documentation.

#### Vision Statement

The whitepaper concludes by reframing the fundamental question organizations should ask: rather than choosing between agent capability and security, robust monitoring infrastructure allows both. The goal involves eliminating the need for "dangerously skip" flags by ensuring continuous verification creates sufficient confidence that security and capability coexist.

#### Key Takeaway

> "Once a layer is watching every action, every secret, every package, and every fix in real time, organizations no longer must stand guard" over agent operations.
