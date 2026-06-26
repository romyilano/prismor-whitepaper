# Notes — Prismor: The Zero Trust Layer for AI Agents

## Omissions (concepts not covered in these 8 pages)

- **EU Cyber Resilience Act detail** — mentioned in passing on page 7's divider but not explored. The CRA's requirement for SBOM and VEX documentation, and how Prismor generates these as byproducts of monitoring, would make a strong page 9 or standalone panel. Audience would need a brief EU regulatory context primer.
- **Self-configuration flow** — the whitepaper notes that agents can self-configure Prismor integration through guided documentation (30-second setup). This is a strong practical detail that the manga skips in favor of narrative arc. Could be a technical appendix page or a "getting started" sidebar.
- **Deterministic vs. AI-powered gates in Warden** — page 5 shows Warden blocking commands but doesn't distinguish between the two evaluation modes. A practitioner audience would benefit from understanding which protections are rule-based and which use AI reasoning.
- **VEX / SBOM compliance** — regulatory compliance as a free byproduct of security operations is genuinely surprising and worth illustrating. Possible page 9 concept: "The Compliance Report That Wrote Itself."

## Possible Sequel Pages

- **Page 9: The Compliance Report** — Prismor's monitoring generates SBOM and VEX reports as byproducts. The Architect didn't file a compliance report; the system built it while working.
- **Page 10: Self-Configuration** — An agent walks through the 30-second Prismor setup, demonstrating how the immunity layer installs itself.
- **Page 0 (prequel): The Before Times** — A page showing what the stack looked like before Prismor, set purely in Shadow's world, as a horror-adjacent contrast.

## Visual Metaphors Considered

- **The Flag as a Light Switch vs. a Circuit Breaker** — initially considered showing `--dangerously-skip-permissions` as a light switch (on/off binary) vs. Prismor as a circuit breaker (contextual). Abandoned in favor of the "two doors" metaphor which better carries the choice framing.
- **Kira as a Postal Worker** — considered the metaphor of a courier who can only deliver to addresses on an approved list. Kept elements of this (courier jacket, package-scanning checkpoint on page 7) but made Kira more autonomous and purposeful than a courier.
- **Shadow as Many vs. One** — page 2 uses the multiplication of Shadow to show attack scale. The choice to show Shadow as sometimes singular (pages 3, 5) and sometimes multiplied (page 2) reflects the dual nature of the threat: a principle that manifests at scale.

## Assumptions Made

- Audience knows what a PR, a pipeline, and a dependency manager are; no explanation given for these terms.
- LiteLLM incident (March 2026) treated as known context at practitioner level; a broader audience would need a sentence of explanation.
- "Zero trust" as a security principle assumed to be unfamiliar to the audience — page 4 explains it from first principles rather than name-dropping it as established practice.

## References for Future Expansion

- CrowdStrike 2026 Global Threat Report (89% AI attack increase figure)
- EU Cyber Resilience Act — supply chain documentation requirements
- NIST definition of zero-trust architecture (NIST SP 800-207)
- LiteLLM supply chain incident post-mortems (March 2026)
