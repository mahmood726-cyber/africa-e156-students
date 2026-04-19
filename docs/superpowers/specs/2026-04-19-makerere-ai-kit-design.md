# Makerere AI Kit — Offline LLM Bundle for Uganda E156 Students

**Status:** Design locked, pending written-spec review
**Date:** 2026-04-19
**Author:** MA + Claude (brainstorming session)
**Parent project:** `africa-e156-students` (Makerere University cohort, 190 E156 papers)
**New project slug:** `makerere-ai-kit` (hosting decision O1 pending — default: new repo)

---

## 1. Problem statement

Uganda-based Makerere students working on the 190-paper `africa-e156-students` assignment face three reliability blockers that the existing website does not address:

1. **Unreliable bandwidth** — claude.ai is frequently unreachable; completing assignment steps 3–5 (download code → rerun → rewrite E156 paper in own voice) depends on AI assistance that students cannot access on demand.
2. **No local code-aware assistant** — students need to understand, modify, and extend Python scripts that query ClinicalTrials.gov. Generic online tutorials don't know about the 7-sentence / 156-word E156 contract or the CT.gov API idioms used in their specific scripts.
3. **No student-safe subset of the author's system** — the author's full toolchain (Overmind, Sentinel, AGENTS.md, MEMORY.md) contains portfolio-private content (editorial-board COI, in-progress submissions, co-author names) that must not ship to students, but the enforcement and contract parts are exactly what they need.

**Goal:** ship an offline, one-click, CPU-only LLM bundle that runs on 8–16 GB Windows laptops and provides code help + E156 paper-rewriting + deterministic verification — with a trimmed, student-safe subset of the author's rule infrastructure.

## 2. Non-goals (v0.1)

- RAG over the full 190-paper repo (32K context handles single-paper work)
- Multi-language UI (English only, matching the parent site)
- Models larger than 4B parameters (binding constraint: 8 GB tier)
- Aider-style "fix this for me" auto-edit mode (students edit their own code — pedagogical decision)
- Nightly verification orchestration (single-shot verifier only)
- Multi-student concurrency / lab server (each student runs locally)
- Any telemetry or phone-home (fully offline)

## 3. Locked design decisions

| # | Decision | Chosen | Alternatives rejected |
|---|---|---|---|
| D1 | Integration shape | **Hybrid**: local LLM is student-facing chat/drafting only; Sentinel and Overmind-lite stay deterministic Python | Offline-Claude-replacement chat; LLM-as-verifier; minimal |
| D2 | Primary student workflow | **Code help + E156 paper rewriting** (based on assignment steps 3–5: download → rerun → rewrite) | Single-purpose (drafting-only or tutor-only) |
| D3 | LLM–code interaction | **File-reading chat with tool-calling** (`read_file`, `list_dir`, `grep`; read-only, sandboxed to the unzipped repo) | Paste-in CLI; aider edit-loop; VS Code extension |
| D4 | Distribution | **Offline ZIP bundle** (~5.2 GB, single download, everything included) | Thin installer + on-demand; USB-only; shared lab server |
| D5 | Author-system subset to ship | **Sentinel + trimmed AGENTS.md + starter MEMORY.md + Overmind-lite verify.py** | Sentinel-only; full stack; minimal (nothing) |
| D6 | Chat UI surface | **Single-file HTML matching dashboard aesthetic** + Python CORS proxy to Ollama | Terminal CLI; Open WebUI; plain localhost web app |

## 4. Model selection

Two models, side-by-side in Ollama, loaded one at a time.

| Role | Model | Size (Q4_K_M) | Rationale |
|---|---|---|---|
| Code help | `qwen2.5-coder:3b-instruct` | ~2.0 GB disk, ~4.5 GB RSS | Trained on code, supports OpenAI-compatible tool-calling, 32K native context |
| Paper rewriting | `gemma-3:4b-it` | ~2.5 GB disk, ~5.0 GB RSS | Better prose quality at this parameter count, stronger instruction-following on long-form rewrites |

**Fallback tier** (activated by `--low-mem` flag in `start.bat` if 8 GB tier fails benchmarks): `qwen2.5-coder:1.5b` (~1.1 GB RSS) replaces the 3B code model. Paper model unchanged.

**Licensing:** Qwen2.5 and Gemma-3 both permit educational redistribution; exact license text confirmed at spec-review time (action item).

## 5. Architecture — bundle shape

```
makerere-ai-kit.zip  (~5.2 GB)
├── start.bat                     # one-click: boots Ollama + proxy, opens chat in browser
├── ollama/                       # Ollama portable for Windows (~50 MB)
│   └── ollama.exe
├── models/                       # pre-pulled GGUF blobs in Ollama's format
│   ├── qwen2.5-coder-3b-q4_K_M/
│   └── gemma-3-4b-it-q4_K_M/
├── python-portable/              # Python 3.11 portable (~30 MB) — no system Python assumption
├── chat/
│   ├── index.html                # single-file chat UI, matches paper-dashboard aesthetic
│   ├── proxy.py                  # CORS proxy + tool-call executor + model-switch
│   └── prompts/
│       ├── coder.system.md       # [USER-WRITTEN] system prompt for qwen-coder
│       ├── writer.system.md      # [USER-WRITTEN] system prompt for gemma E156 voice
│       └── rewrite-e156.tmpl.md  # [USER-WRITTEN] paper-rewrite prompt template
├── africa-e156-students/         # snapshot of the parent repo (190 papers)
│   └── ...
├── sentinel/                     # trimmed rule engine (~7 rules, see §8.1)
│   ├── rules/
│   └── sentinel.py
├── AGENTS.md                     # trimmed rules doc (~150 lines, see §8.2)
├── MEMORY.md                     # [USER-WRITTEN] starter memory scaffold
├── memory/
│   └── references/               # [USER-WRITTEN] starter reference files (E156, CT.gov, Synthēsis)
├── verify.py                     # Overmind-lite verifier (see §9)
└── README.md                     # quickstart, hardware floor, troubleshooting
```

## 6. Runtime flow

1. Student unzips → double-clicks `start.bat`
2. `start.bat` launches `ollama serve` (binds `localhost:11434`)
3. `start.bat` launches `python-portable\python.exe chat\proxy.py` (binds `localhost:8000`)
4. Browser opens `http://localhost:8000/chat`
5. Chat UI renders:
   - Left sidebar: file tree of `africa-e156-students/`, plus a "Verify my paper" button
   - Main pane: chat messages
   - Top bar: mode toggle `[Code help] [Paper rewrite]`
   - Bottom: text input
6. Mode toggle behavior:
   - **Code help** → proxy routes to qwen2.5-coder-3b with tool-calling enabled; read-only sandbox limits tool scope to the unzipped `africa-e156-students/` directory
   - **Paper rewrite** → proxy unloads qwen, loads gemma-3-4b-it, no tool-calling; paper sidebar click prefills the rewrite template
7. "Verify my paper" → proxy runs `verify.py <paper-dir>` as a subprocess, renders the returned JSON as a checklist in the UI

**Model-swap cost:** ~3–6 s on the 32 GB test box; ~8–12 s on 8 GB student tier (acceptable; students don't switch constantly).

## 7. Chat UI + two-model routing details

### 7.1 UI layout

Single-file HTML (Tailwind-inline, no CDN dependency — offline-ready) matching the paper-dashboard visual vocabulary:

```
┌─────────────────────┬──────────────────────────────────┐
│ africa-e156-students│                                  │
│ ├─ geographic-equity│  [ Code help ] [ Paper rewrite ] │
│ │  ├─ angle-11...md │  ──────────────────────────────  │
│ │  └─ code/         │                                  │
│ ├─ health-disease   │  >  Chat messages here           │
│ └─ ...              │                                  │
│                     │                                  │
│ [ Verify my paper ] │  ┌────────────────────────────┐  │
│                     │  │ Ask a question...       ▶  │  │
└─────────────────────┴──┴────────────────────────────┴──┘
```

### 7.2 Tool-calling (Code-help mode)

Tools exposed to qwen-coder:
- `read_file(path: str) -> str` — returns file contents, 200 KB cap
- `list_dir(path: str) -> list[str]` — returns entries, non-recursive
- `grep(pattern: str, path: str) -> list[str]` — returns line matches, 100 max

All three resolve paths against the unzipped `africa-e156-students/` root; absolute paths and `..` escapes are rejected. No write tools (pedagogical: students do their own edits).

### 7.3 Paper-rewrite mode

- Sidebar lists only paper markdown files (glob: `*/papers/*.md`) — hides code files, dashboards, and build scripts to keep the rewrite surface unambiguous
- Click a `.md` paper in the sidebar → UI fetches via proxy (`GET /api/file?path=...`) → prefills the chat input with the filled `rewrite-e156.tmpl.md` template + the paper body
- Model generates → post-process runs `verify.py`'s E156 format witness on the output → if fail, UI highlights the violation and offers "regenerate with this feedback" (feeding the violation back as a follow-up message)

## 8. Author-system subset trimming

### 8.1 Sentinel rules (travels vs stays)

| Travels to student bundle | Stays author-side |
|---|---|
| P0 hardcoded local paths in shipped code | Workbook `SUBMITTED:[x]` toggle rule |
| P0 empty-DataFrame `.iloc[0]` access | TruthCert HMAC signing rules |
| P0 XSS in HTML / unescaped innerHTML | Editorial-board COI rule |
| P0 localStorage key collision | Synthēsis OJS submission rules |
| P0 SE_FLOOR / Clopper-Pearson statistics edges | Portfolio-reconciliation gates |
| P1 JS lockfile present + scripts resolvable | E156 workbook entry validator |
| P1 empty-DataFrame access (WARN) | Overmind nightly orchestration |

Result: ~7 rules ship; pre-push hook fires for the student on the same rule runner as the author uses, on a smaller sharper set.

### 8.2 AGENTS.md — trimmed

**Travels:**
- E156 7-sentence × 156-word contract (S1–S7 roles, word targets)
- Code-quality rules (no hardcoded paths, no XSS, lockfiles, no marketing language)
- Testing discipline (run full suite, never claim "done" without pass count)
- Git hygiene (commit per batch, no `--no-verify`)
- Common regression traps (encoding/BOM, identifier validation, division-by-zero)

**Scrubbed:**
- Portfolio-reconciliation gates (assumes author's INDEX.md)
- Workbook protection rules (private rewrite log)
- Editorial-board COI policy (author-specific)
- SubmissionCockpit / push_all_repos / `mahmood726-cyber` references
- Past-incident lessons that name specific author projects — keep the *pattern*, drop the names

Target length: ~150 lines.

### 8.3 MEMORY.md — starter scaffold only

Author's MEMORY.md does not travel at all. Student bundle ships an empty-index starter plus three pre-written references:

```
MEMORY.md                     # index; My E156 Papers section starts empty
memory/references/
├── e156_format.md            # 7-sentence contract, S1-S7 roles, word budgets
├── ctgov_tips.md             # common CT.gov API pitfalls (lowercase intervention types, etc.)
└── synthesis_submission.md   # OJS 5-step wizard, file formats, COI statement template
```

Chat UI injects `MEMORY.md` + referenced files as system context on every turn, so the LLM always knows about E156 without the student having to re-explain.

## 9. Overmind-lite `verify.py`

Pure Python, deterministic, no LLM call. Called via proxy subprocess on "Verify my paper" click.

### 9.1 Five witnesses

```
verify.py <paper-dir>
│
├── 1. Sentinel scan       → 0 BLOCK     (rules from sentinel/)
├── 2. E156 format check   → 7 sentences + ≤156 words + S1–S7 role hints + single paragraph
├── 3. Code smoke test     → code/*.py runs in <60 s (CT.gov call) OR SKIP if offline
├── 4. References check    → ≥2 refs in paper.md References section (PubMed/WHO/CT.gov)
└── 5. pytest              → exit 0 OR SKIP if no tests/ dir

→ Verdict: PASS / FAIL / UNVERIFIED
```

### 9.2 Verdict rules (precedence ordered — evaluate top to bottom, first match wins)

1. **FAIL** if any of: Sentinel BLOCK > 0; E156 format witness = FAIL; code witness = FAIL (crash or timeout); references witness = FAIL (count < 2)
2. **UNVERIFIED** if Sentinel + E156 + references all PASS, and code witness = SKIP with reason "network unreachable"
3. **PASS** otherwise (pytest SKIP with reason "no tests/ dir" is expected and does not demote the verdict; any other unhandled SKIP defaults to UNVERIFIED, never PASS)

**UNVERIFIED is not a pass.** Encodes the lesson from the author's real Overmind SKIP-as-pass fix (2026-04-15). Tells the student "re-run when connectivity is restored"; does not authorise submission.

### 9.3 Output format

```json
{
  "verdict": "FAIL",
  "witnesses": {
    "sentinel":  {"status": "PASS", "blocks": 0, "warns": 1},
    "e156":      {"status": "FAIL", "reason": "8 sentences, expected 7"},
    "code":      {"status": "PASS", "runtime_s": 12.4},
    "refs":      {"status": "PASS", "count": 3},
    "pytest":    {"status": "SKIP", "reason": "no tests/ dir"}
  },
  "next_actions": [
    "Combine S5 and S6 — the rewrite split one sentence into two."
  ]
}
```

The `next_actions` strings are the specific, pedagogical feedback the student sees — not generic error messages.

## 10. User-written code contributions (Learning Mode)

Five small files where author judgment shapes the product more than code skill does. I scaffold surrounding context + TODO markers; the user writes these.

| # | File | Lines | What it shapes |
|---|---|---|---|
| C1 | `chat/prompts/coder.system.md` | ~8 | qwen-coder behavior, tool-call idiom, teacher/peer voice |
| C2 | `chat/prompts/writer.system.md` | ~10 | gemma E156-contract enforcement, "Ugandan voice" guidance |
| C3 | `chat/prompts/rewrite-e156.tmpl.md` | ~6 | exact rewrite prompt filled per paper click |
| C4 | `MEMORY.md` + three reference files | ~30 total | tone (dry/friendly), scope (narrow/broad), voice (prescriptive/descriptive) |
| C5 | `verify.py::decide(witnesses) -> dict` + `next_actions` strings | ~12 | verdict thresholds (strict/lenient), pedagogical feedback strings |

Without C1–C5 the bundle runs but is pedagogically empty.

## 11. Test plan

Two-tier strategy on the author's 32 GB i7-8665U box.

### 11.1 Tier 1 — Native (daily iteration)

**Phase A — Bundle assembly** (one-shot per release)
- `make_bundle.py` pulls Ollama portable + GGUFs + zips chat UI + snapshots repo → `makerere-ai-kit-v0.1.zip`
- Pass: ZIP unzips clean, `start.bat` boots without errors

**Phase B — Functional smoke** (per code change)
- Fresh dir unzip → `start.bat` → browser opens → "hello" to coder replies ≤30 s → switch to writer replies ≤30 s → Verify on known-good paper returns JSON
- Pass: no exceptions, both models reply, verify.py exits clean

**Phase C — End-to-end student workflow** (per meaningful change; ~20 min)
- Target paper: `health-disease/papers/hiv-saturation-index.md`
- Simulate student: ask script explanation → ask for date-filter modification → apply diff → run → switch mode → click paper → draft rewrite → Verify
- Pass: <10 min wall-clock, sensible verdict

**Phase D — Performance benchmarks** (per release)

| Metric | Target (i7-8665U, CPU-only) |
|---|---|
| qwen2.5-coder-3b tok/s | ≥5 |
| qwen2.5-coder-3b cold load | ≤8 s |
| gemma-3-4b-it tok/s | ≥3.5 |
| gemma-3-4b-it cold load | ≤10 s |
| Model swap (unload + load) | ≤12 s |
| E156 rewrite end-to-end (~250 tokens) | ≤75 s |
| verify.py on one paper (incl CT.gov call) | ≤120 s |

Fail any → evaluate drop to qwen2.5-coder-1.5b for 8 GB tier, or accept slower UX.

**RAM observation** (continuous)
- `ollama ps` + Task Manager. Peak RSS targets:
  - qwen loaded: ≤4.5 GB
  - gemma loaded: ≤5.0 GB
  - Simultaneous: not allowed

### 11.2 Tier 2 — Hyper-V 8 GB cap (authenticity, once per release)

- New Win11 VM, 8 GB RAM, 4 vCPUs, no GPU passthrough
- Copy ZIP, unzip, run `start.bat`, repeat Phase B + C
- Pass: commit charge <9 GB, no OOM, no swap thrash
- If fail: engage fallback tier (1.5B code model)

### 11.3 Out of test scope

- Actual Ugandan laptops (no hardware access)
- Degraded network conditions (UNVERIFIED verdict handles this declaratively)
- Models other than Qwen + Gemma
- Multi-student concurrency

## 12. Success criteria

### 12.1 v0.1 (author's own test complete)

All five required:
1. Tier 1 Phase B passes in a fresh-unzip dir, no manual repair
2. Tier 1 Phase C completes in <10 min, sensible verdict
3. Tier 1 Phase D benchmarks all met, OR slower number explicitly accepted
4. Tier 2 Hyper-V 8 GB Phase B + C passes without OOM / thrash
5. User-written C1–C5 contributions are written

### 12.2 v1.0 (ready for Uganda hand-off)

Beyond v0.1:
- README states hardware floor (8 GB RAM, 5 GB disk, Win10/11), boot procedure, verify workflow, UNVERIFIED meaning, help channel
- Bundle hosted on GitHub Releases with SHA256 checksum
- One end-to-end pilot run by a non-author (or the author in a fresh VM with no prior knowledge of internals)

## 13. Open questions (decide before implementation, not now)

| # | Question | Default if unspecified |
|---|---|---|
| O1 | Host repo | New `makerere-ai-kit` repo |
| O2 | Python bundling | Bundle portable Python 3.11 (~30 MB) |
| O3 | Update path | Patch ZIP for rules+chat; full ZIP for model updates |
| O4 | License | MIT for code; CC BY-SA for trimmed AGENTS.md content |
| O5 | Telemetry | None |
| O6 | Sentinel rule subset | §8.1 as written |
| O7 | Student help channel (WhatsApp, Matrix, GitHub Issues, email) | GitHub Issues on the bundle repo |
| O8 | Model license audit — confirm Qwen2.5 + Gemma-3 educational-redistribution terms before first ZIP build | Block v0.1 ship if any license ambiguous |

## 14. Risks & mitigations

| Risk | Mitigation |
|---|---|
| qwen2.5-coder tool-calling unreliable at 3B | Validate in Phase B; fall back to non-tool-call paste-in mode if <90% success |
| gemma-3-4b can't hit 156-word target reliably | Post-process validates; regenerate loop with specific feedback; max 3 attempts |
| Ollama portable on Windows has intermittent model-load bugs | Pin to a known-good Ollama version; document the version in README |
| 5 GB ZIP too large for some student connections | Mirror on GitHub Releases + a Kampala intermediary's USB-drive chain |
| Bundle includes a model file with unclear commercial-use clause | License audit at spec-review gate; reject any model with ambiguous educational-use terms |

## 15. Implementation phase gate

After user reviews this spec:
- If approved → proceed to `writing-plans` skill to generate the implementation plan (broken into TDD-sized tasks, one preflight task for prereq checking, explicit code-contribution stops at C1–C5)
- If changes requested → revise, re-run self-review, re-present

Implementation skill chosen: **writing-plans only**. Not frontend-design (scope too narrow for that skill), not mcp-builder (no MCP server in this design).
