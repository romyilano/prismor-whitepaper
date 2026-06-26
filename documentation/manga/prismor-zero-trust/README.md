# Prismor: The Zero Trust Layer for AI Agents — Educational Manga

**Source:** Prismor whitepaper — https://www.prismor.dev/whitepaper
**Topic slug:** `prismor-zero-trust`
**Total pages:** 8
**Art style:** Technical Noir (high-contrast, heavy blacks, cyberpunk atmosphere)
**Voice:** Noir literary — dry, precise, world-weary, complete grammatical sentences

---

## Summary

Modern AI coding agents are production-capable: they open PRs, rewrite services, and deploy code independently. This creates a dilemma — manually approve every action, or disable safety checks with a flag named to make you feel its danger. While developers deliberate, the threat landscape accelerates: 89% more AI-driven attacks, 29-minute propagation windows, supply-chain packages poisoned and deployed to tens of thousands of machines before anyone notices.

Prismor answers with a zero-trust layer — four components that watch every action, every secret, every package, and every fix in real time. When the infrastructure exists to verify continuously, the dilemma between agent capability and security disappears.

---

## Key Concepts

1. The capability-vs-safety dilemma in AI coding agents
2. AI-driven attack velocity (89% increase, 29-min propagation, LiteLLM incident)
3. Identity debt (80:1 machine-to-human ratio, 97% overpermissioned)
4. Zero trust as architectural principle, not a product feature
5. Warden — command evaluation and blocking, with non-disableable protections
6. Cloak — credential interception before secrets can escape
7. IAM — role-based access constraints that hold even under compromise
8. Semantic Guard — intent analysis to catch prompt injection attacks
9. Package shield — risk assessment across pip, npm, and seven other managers
10. Auto-Fix Agent — targeted CVE patches, human-reviewed PRs, 58-day → sprint cycle

---

## Characters

| Character | Role |
|-----------|------|
| **Kira** | Protagonist; a capable AI coding agent, personified as a cyberpunk courier |
| **The Architect** | The human developer facing the dilemma; audience entry point |
| **The Warden** | Prismor's enforcement component; laconic, incorruptible, always present |
| **Shadow** | The collective threat — attacks, supply-chain poisons, prompt injectors |

---

## Page List

| Page | Concept |
|------|---------|
| 01 | The Dilemma — two bad choices, a named danger flag |
| 02 | The Threat Landscape — attack velocity and scale |
| 03 | Identity Crisis — 80:1 machines, 97% overpermissioned |
| 04 | Zero Trust Enters — Prismor's architectural answer |
| 05 | Warden & Cloak — command enforcement and credential interception |
| 06 | IAM & Semantic Guard — role constraints and intent analysis |
| 07 | Package Shield & Auto-Fix — supply-chain defense and CVE remediation |
| 08 | The Vision — no dangerously-skip needed; the city is watched |

---

## Pipeline

1. Open `index.html` to copy each page's image prompt
2. Paste into your image model (Midjourney, DALL·E, Gemini, etc.)
3. Save rendered images to `panels/prismor-zero-trust_pageNN.png`
4. Re-run `build_prompt_site.py` to preview rendered images in the site
5. Optionally run `manga-pdf-generator` to bundle into a PDF
