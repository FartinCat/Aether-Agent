---
name: A05-route-scanner
aliases:
  - endpoint-scanner
  - url-mapper
  - page-finder
description: Automated web page and API route discovery scanner. Maps all frontend UI pages, Next.js app/pages routes, and backend API endpoints into a unified URL index.
category: scan
---

# Skill: A05-route-scanner (URL, Page & Endpoint Scanner)

> **Core Purpose**: The "Door Finder" of the repository. Scans the codebase to discover and catalog every web page URL that users can visit and every API endpoint that clients can call.

---

## 1. Skill Package Structure (Self-Contained)

This skill packages its own lightweight, zero-dependency crawler within its own folder:

```
A05-route-scanner/
├── SKILL.md                  # Route discovery protocol & categorization guidelines
├── scripts/
│   └── scan_routes.py        # Pure standard-library route & endpoint crawler (<100ms)
└── agents/
    └── openai.yaml           # Antigravity/OpenAI UI display metadata
```

Anyone can copy `A05-route-scanner/` into any `.agents/skills/` directory to instantly map routes across any web or API project.

---

## 2. Core Operating Principles

1. **Clear Division of Routes**:
   - **UI Pages**: Routes that render visual web interfaces for users (e.g. `/`, `/login`, `/dashboard`, `/settings`).
   - **API Routes**: Endpoints that serve data, JSON, or process mutations (e.g. `POST /api/auth`, `GET /api/users`).
2. **Universal Framework Recognition**:
   - **File-Based Routing**: Next.js App Router (`app/**/page.tsx`, `app/**/route.ts`), Next.js Pages Router (`pages/**/*.tsx`), SvelteKit (`+page.svelte`, `+server.ts`), Remix.
   - **Code-Based Routing**: Express (`app.get()`, `router.post()`), FastAPI (`@app.get()`, `@router.post()`), Flask (`@app.route()`), Django (`path()`, `urlpatterns`), React Router (`<Route path="..." />`).
3. **Prevent Duplication & Broken Links**:
   Before creating a new page or API endpoint, verify whether a route with that name or functionality already exists.

---

## 3. The 3-Step Route Discovery Protocol

```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Framework Route Detection                           │
│ (Identify whether repo uses file-based or code-based routes)│
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Step 2: Execute Self-Contained Route Crawler                │
│ (Run internal helper: python scan_routes.py .)              │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Step 3: Route Inventory & Verification                      │
│ (Emit URL Directory Sheet: UI Pages vs API Endpoints)       │
└─────────────────────────────────────────────────────────────┘
```

### Step 1: Framework Route Detection
Check the tech stack from `A01-deep-scan` to determine route strategy:
- Next.js / SvelteKit -> Check `app/`, `pages/`, or `src/routes/`.
- Express / FastAPI -> Check server entrypoints, `routes/`, or `controllers/`.

### Step 2: Execute Self-Contained Route Crawler
Run the skill's self-contained script:
```bash
python "<path_to_skill>/scripts/scan_routes.py" .
```
In `<100ms`, the script returns a compact JSON inventory of all UI pages and API routes with exact file and line locations.

### Step 3: Route Inventory & Verification
Verify that:
- Every public URL has a clean path.
- Dynamic route parameters (e.g. `[id]`, `:id`, `{item_id}`) are clearly noted.
- No dead or duplicate routes exist.

---

## 4. Output Modes

### Mode A: Standalone URL & Route Directory
*Use this when invoked directly by the user or via `/route-scanner`.*

```markdown
## 🚪 URL & Route Directory: [Project Name]

### 1. UI Pages (User-Facing Web Views)
| URL Path | Framework | Source File | Description |
| :--- | :--- | :--- | :--- |
| `/` | Next.js App Router | [`src/app/page.tsx:L1`](file:///path/to/file#L1) | Landing / Home Page |
| `/login` | Next.js App Router | [`src/app/login/page.tsx:L1`](file:///path/to/file#L1) | User Login Screen |
| `/dashboard` | Next.js App Router | [`src/app/dashboard/page.tsx:L1`](file:///path/to/file#L1) | Main User Dashboard |
| `/settings` | Next.js App Router | [`src/app/settings/page.tsx:L1`](file:///path/to/file#L1) | Account Settings |

### 2. API Endpoints (Data & Backend Handlers)
| Method | URL Route | Framework | Source File |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/login` | Next.js Route Handler | [`src/app/api/auth/login/route.ts:L1`](file:///path/to/file#L1) |
| `GET` | `/api/users/profile` | Next.js Route Handler | [`src/app/api/users/profile/route.ts:L1`](file:///path/to/file#L1) |
| `DELETE`| `/api/items/:id` | Express Router | [`src/routes/items.ts:L42`](file:///path/to/file#L42) |

### 3. Summary & Observations
- **Total Pages**: 4 UI Pages | **Total Endpoints**: 3 API Endpoints
- **Convention**: Uses kebab-case URL naming.
- **Recommendations**: New feature routes should follow the existing directory convention under `src/app/`.
```

### Mode B: Ensemble Machine Context Anchor
*Use this when feeding into `Category B (Planner)` or `Category D (Test Engineer)`.*

```markdown
<!-- CONTEXT_ANCHOR:ROUTES -->
{
  "total_routes": 7,
  "ui_pages": ["/", "/login", "/dashboard", "/settings"],
  "api_endpoints": [
    {"method": "POST", "path": "/api/auth/login"},
    {"method": "GET", "path": "/api/users/profile"},
    {"method": "DELETE", "path": "/api/items/:id"}
  ],
  "routing_style": "nextjs_app_router"
}
<!-- /CONTEXT_ANCHOR -->
```

---

## 5. Invocation & Workflow Integration
- **Manual**: Run whenever you want to inspect what pages or URLs exist in the app (`/route-scanner`).
- **In Workflow**: Ingested by `Category B (Planner)` before designing new pages/APIs to prevent duplicate routes, and by `Category D (Test Engineer)` to generate end-to-end and integration test suites.
