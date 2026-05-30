---
name: "source-command-web-aesthetics"
description: "Audit and upgrade UI/UX to premium standards, powered by UI/UX Pro Max intelligence."
category: ui
---

# source-command-web-aesthetics

Use this skill when the user asks to run the migrated source command `web-aesthetics`. It provides elite UI/UX auditing and design enforcement, powered by the **ui-ux-pro-max** search engine and design library.

## Command Template

Invoke `.agent/.agents/skills/13-web-aesthetics` in tandem with [ui-ux-pro-max](file:///d:/Git_Work/Aether%20Agent/.agent/skills/ui-ux-pro-max/SKILL.md).

### Step 1: Initialize Design System via UI/UX Pro Max
Before modifying any files, run the python-based search engine to synthesize matching guidelines and establish a design system:
```bash
python .agent/skills/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <keywords>" --design-system -p "Project Name" -f markdown --persist
```
*Note: This creates `design-system/MASTER.md` as the global visual and layout source of truth.*

### Step 2: Extract Domain & Stack-Specific Guidelines
Enhance layout details, animations, or typography using focused domain queries:
* **UX/Interaction Rules**: `python .agent/skills/ui-ux-pro-max/scripts/search.py "hover transitions animation" --domain ux`
* **Typography Pairings**: `python .agent/skills/ui-ux-pro-max/scripts/search.py "elegant professional sans-serif" --domain typography`
* **Framework Stack (Default: html-tailwind)**: `python .agent/skills/ui-ux-pro-max/scripts/search.py "responsive navbar card grid" --stack html-tailwind`

### Step 3: Comprehensive Audit & Implementation Rules
Enforce the premium standards of both skills:
- **Layout consistency and visual hierarchy**: Standardized grid spacing and containers.
- **Color system**: Verified palettes via `ui-ux-pro-max` (HSL tailored, Slate text `#0F172A`/`#475569` for light mode contrast, glassmorphism `bg-white/80` or higher, no simple primary red/blue/greens).
- **Typography**: Max 2 font families (from Google Fonts), max 2 sizes per view, bold for strict hierarchy.
- **Icon Integrity**: **NO emoji icons** (e.g. 🎨 🚀 ⚙️). Use verified inline SVGs (Lucide/Heroicons) with a consistent 24x24 `viewBox` (w-6 h-6).
- **Interaction & Cursor**: All clickable/hoverable cards/buttons MUST have `cursor-pointer`.
- **Transitions**: Smooth color/opacity interaction transitions between 150ms and 300ms. No scale transitions that trigger layout shifts.

### Step 4: Verification Gate (Pre-Delivery Checklist)
Review the implemented designs against the **Pre-Delivery Checklist** in [ui-ux-pro-max/SKILL.md](file:///d:/Git_Work/Aether%20Agent/.agent/skills/ui-ux-pro-max/SKILL.md):
- Check visual responsiveness at **375px** (mobile) and **1440px** (desktop). Ensure no horizontal scrolls.
- Run color contrast audit for both Light and Dark mode readability.
- Verify keyboard focus states (`focus-visible`) and semantic HTML.

