---
name: A06-schema-scanner
aliases:
  - data-model-finder
  - model-scanner
  - schema-mapper
description: Automated database schema and data model extractor. Discovers database tables, ORM models, field names, and data types across Prisma, SQL, Pydantic, SQLAlchemy, and Drizzle to eliminate hallucinated field names.
category: scan
---

# Skill: A06-schema-scanner (Data Model & Database Schema Finder)

> **Core Purpose**: The "Database Blueprint Finder". Scans the codebase to discover and catalog all database tables, ORM models, field names, and data types to prevent hallucinated column names and broken queries.

---

## 1. Skill Package Structure (Self-Contained)

This skill packages its own lightweight, zero-dependency schema parser within its own folder:

```
A06-schema-scanner/
├── SKILL.md                  # Schema discovery protocol & query safety guidelines
├── scripts/
│   └── scan_schemas.py       # Pure standard-library schema & model extractor (<100ms)
└── agents/
    └── openai.yaml           # Antigravity/OpenAI UI display metadata
```

Anyone can copy `A06-schema-scanner/` into any `.agents/skills/` directory to instantly map data models across any backend or fullstack project.

---

## 2. Core Operating Principles

1. **Zero-Hallucination Querying**:
   The #1 reason AI-generated database code crashes is guessing column names (e.g. guessing `user.created_at` when the schema uses `user.createdAt` or `user.joinedDate`). Never write a query or mutation without verifying the exact field name and casing from this scanner.
2. **Universal Schema Recognition**:
   - **Prisma**: `schema.prisma` (`model User { id String @id ... }`).
   - **SQL Migrations**: `migrations/*.sql` (`CREATE TABLE users (...)`).
   - **Python**: Pydantic models (`class User(BaseModel)`), SQLAlchemy models (`class User(Base)`), Django models.
   - **TypeScript ORMs**: Drizzle (`pgTable`), TypeORM (`@Entity`), Mongoose schemas.
3. **Entity-Relationship Awareness**:
   Identifies foreign keys and relationships so the agent understands how data connects (e.g. `User 1:N Orders`, `Order -> user_id`).

---

## 3. The 3-Step Schema Discovery Protocol

```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: ORM & Schema Engine Detection                       │
│ (Identify whether repo uses Prisma, SQL, Pydantic, Drizzle) │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Step 2: Execute Self-Contained Schema Crawler               │
│ (Run internal helper: python scan_schemas.py .)             │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│ Step 3: Entity Blueprint & Field Contract Generation        │
│ (Emit Schema Directory: Models, Fields, Types, Relations)   │
└─────────────────────────────────────────────────────────────┘
```

### Step 1: ORM & Schema Engine Detection
Check manifests (`package.json`, `pyproject.toml`) and directory trees from `A01-deep-scan` to locate schema definitions (`prisma/`, `models/`, `migrations/`, `schemas/`).

### Step 2: Execute Self-Contained Schema Crawler
Run the skill's self-contained script:
```bash
python "<path_to_skill>/scripts/scan_schemas.py" .
```
In `<100ms`, the script returns a compact JSON inventory of all models, tables, columns, and data types with exact source files.

### Step 3: Entity Blueprint Generation
Generate an Entity Blueprint Sheet showing exact field names and types for all agents to reference.

---

## 4. Output Modes

### Mode A: Standalone Entity Blueprint Sheet
*Use this when invoked directly by the user or before writing database queries.*

```markdown
## 🗄️ Database Entity Blueprint: [Project Name]

### 1. `User` Model (`prisma/schema.prisma` / `src/models/user.ts`)
| Field Name | Data Type | Key / Constraints |
| :--- | :--- | :--- |
| `id` | `String (UUID)` | 🔑 Primary Key |
| `email` | `String` | Unique, Not Null |
| `passwordHash` | `String` | Private / Hashed |
| `role` | `Role (Enum)` | Default: `USER` |
| `createdAt` | `DateTime` | Default: `now()` |

### 2. `Order` Model (`prisma/schema.prisma`)
| Field Name | Data Type | Key / Constraints |
| :--- | :--- | :--- |
| `id` | `String (UUID)` | 🔑 Primary Key |
| `userId` | `String` | 🔗 Foreign Key -> `User.id` |
| `totalAmount` | `Decimal` | Not Null |
| `status` | `OrderStatus` | Default: `PENDING` |

### 3. Key Observations & Query Guidelines
- **Casing Convention**: Uses `camelCase` for all database column names (e.g. `userId`, not `user_id`).
- **IDs**: Uses UUID strings rather than auto-incrementing integers.
- **Relations**: `User` has a 1-to-many relationship with `Order`.
```

### Mode B: Ensemble Machine Context Anchor
*Use this when feeding into `Category B (Planner)` or `Category C (Language Specialist / Python / TS)`.*

```markdown
<!-- CONTEXT_ANCHOR:SCHEMAS -->
{
  "total_models": 2,
  "models": {
    "User": {
      "fields": {"id": "UUID", "email": "String", "role": "Enum", "createdAt": "DateTime"},
      "primary_key": "id"
    },
    "Order": {
      "fields": {"id": "UUID", "userId": "String", "totalAmount": "Decimal", "status": "Enum"},
      "primary_key": "id",
      "foreign_keys": {"userId": "User.id"}
    }
  },
  "casing": "camelCase"
}
<!-- /CONTEXT_ANCHOR -->
```

---

## 5. Invocation & Workflow Integration
- **Manual**: Run whenever you want to inspect database models or write database code (`/schema-scanner`).
- **In Workflow**: Ingested by `Category B (Planner)` when designing database-backed features, and by `Category C (Implementer)` to guarantee 100% field name accuracy without database crashes.
