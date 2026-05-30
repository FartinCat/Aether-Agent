---
description: Audit and upgrade UI/UX to premium standards, powered by UI/UX Pro Max.
category: ui
---

Invoke `.agent/.agents/skills/13-web-aesthetics` in tandem with [ui-ux-pro-max](file:///d:/Git_Work/Aether%20Agent/.agent/skills/ui-ux-pro-max/SKILL.md).

### 🛠️ Execution Pipeline:
1. **Synthesize Design System**:
   ```bash
   python .agent/skills/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <keywords>" --design-system -p "Project Name" -f markdown --persist
   ```
2. **Retrieve Stack Rules (Default: html-tailwind)**:
   ```bash
   python .agent/skills/ui-ux-pro-max/scripts/search.py "layout navbar grid" --stack html-tailwind
   ```
3. **Domain Details (as needed)**:
   ```bash
   python .agent/skills/ui-ux-pro-max/scripts/search.py "<query>" --domain ux
   ```

### 🎨 Pro Max Premium Audits:
- **Colors**: Custom palettes only. Strict Light mode contrast (Slate body `#0F172A`/`#475569`, glass elements `bg-white/80` minimum).
- **Icons**: **NO emoji icons**. Always use verified inline SVGs (Lucide/Heroicons) with `viewBox="0 0 24 24"` and `w-6 h-6`.
- **Interactions**: Add `cursor-pointer` to clickable card items. Smooth hover state transitions ($150\text{ms}-300\text{ms}$). No scale transforms causing layout shifts.
- **Typography**: Maximum 2 font families (Google Fonts), clean scale hierarchies.
- **Responsiveness**: Verify at **375px** (mobile) and **1440px** (desktop). Zero horizontal overflow.

