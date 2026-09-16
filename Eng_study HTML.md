---
name: repo-engineering-learning-html
description: Turn an unfamiliar software, AI, data, or research repository into a concise interactive HTML learning environment. Help the reader understand the system, analyze engineering decisions and trade-offs, connect the repository to reusable SWE/CS concepts, and practice redesigning or extending the system. Use when the goal is not only to understand what a repo does, but to build engineering judgment and design skill from it.
---

# Repo Engineering Learning HTML

Build an evidence-grounded interactive HTML learning surface for studying an unfamiliar repository.

The goal is not to create a prettier README.

The goal is to help the reader move through:

```text
Understand the system
        ↓
Understand why it was designed this way
        ↓
Identify trade-offs and weaknesses
        ↓
Connect concrete code to reusable SWE / CS concepts
        ↓
Practice making engineering decisions
        ↓
Develop independent design judgment
```

The HTML should feel like an interactive engineering case study.

---

# 1. Primary learning outcomes

After studying the page, the reader should be able to answer:

- What problem does this repository solve?
- What are its major components and data flows?
- Where are the important architectural boundaries?
- Why might the authors have chosen this design?
- What engineering benefits does the design provide?
- What weaknesses, constraints, or hidden costs does it introduce?
- What realistic alternative designs exist?
- Under what conditions would another design become better?
- Which reusable SWE / CS concepts appear in this repository?
- How would I modify the architecture if requirements changed?
- How would I instruct an AI coding agent to implement those changes precisely?

Prioritize **engineering reasoning** over memorizing filenames.

---

# 2. Source of truth

Inspect the repository before designing the HTML.

Prefer targeted exploration rather than dumping the repository.

Evidence priority:

1. Current executable code.
2. Tests.
3. Schemas and interfaces.
4. Configuration and dependency files.
5. Current README or architecture documentation.
6. Deployment and runtime configuration.
7. Git history when needed to understand design evolution.
8. Older proposals or planning documents only as historical context.

When sources conflict:

```text
Current code > tests > canonical documentation > historical plans
```

Mark important claims as:

- `Implemented`
- `Designed`
- `Inferred`
- `Historical`

Never present planned functionality as implemented functionality.

Never invent architecture merely because it would be conventional.

---

# 3. Repository reconnaissance

Inspect only information that changes the reader's mental model.

Useful targets include:

- `AGENTS.md`
- README
- package / dependency manifests
- entry points
- API routes
- services
- modules
- model code
- training scripts
- data pipelines
- database schemas
- tests
- deployment configuration
- CI/CD configuration
- environment configuration
- artifact contracts
- notebooks
- important utilities

Prefer:

```text
rg
targeted file reads
directory inspection
dependency inspection
small code traces
```

Avoid reading every file sequentially.

Stop broad exploration once you can confidently describe:

```text
Problem
Inputs
Core components
Data / control flow
Important abstractions
Runtime behavior
Outputs
Key engineering decisions
Important constraints
```

---

# 4. Build a compact system model first

Before generating the HTML, create a concise mental model.

## Overall

Write three short lines:

**Topic**

What kind of system is this?

**Goal**

What concrete result is the system trying to produce?

**Stack**

Only list technologies actually evidenced by the repository.

Example:

```text
Topic: ICU AKI early-warning pipeline using longitudinal EHR data.

Goal: Convert patient records into leakage-safe snapshots and estimate future AKI risk.

Stack: Python, pandas, XGBoost, FastAPI, PostgreSQL.
```

---

# 5. Identify the architecture

Reduce the repository into approximately **5–9 major nodes**.

Examples:

```text
Input
→ preprocessing
→ domain logic
→ model / algorithm
→ persistence
→ API / service layer
→ evaluation
→ runtime / deployment
```

Adapt the architecture to the actual repository.

Do not force ML concepts onto normal software projects.

Possible software architecture:

```text
Client
→ API
→ service layer
→ domain logic
→ repository / database
→ external services
```

Possible ML architecture:

```text
Raw data
→ cohort
→ labels
→ features
→ split
→ training
→ validation
→ inference
```

Possible agent architecture:

```text
User request
→ planner
→ tools
→ memory / state
→ model
→ verification
→ output
```

For each node capture only:

- responsibility
- main input
- main output
- important dependencies
- one important design decision

Keep node descriptions short.

---

# 6. HTML information architecture

The website should contain only five major views.

```text
System Map
Design Review
SWE Concepts
Practice
Glossary
```

Avoid additional top-level tabs unless absolutely necessary.

Use progressive disclosure.

The first screen should remain visually simple.

---

# 7. View 1 — System Map

Purpose:

> Understand how the repository actually works.

Show:

- Overall summary
- interactive architecture diagram
- current implementation status
- selected-node inspector

Clicking a node should reveal:

```text
Role
Input
Output
Important files
Dependencies
Why this component exists
```

Do not show large code dumps.

Show short code snippets only when a specific implementation pattern matters.

Prefer:

```text
architecture diagram + inspector
```

over:

```text
large paragraphs
```

---

# 8. View 2 — Design Review

This is one of the most important views.

Its purpose is not merely to describe architecture.

Its purpose is to analyze **engineering choices**.

Identify approximately **4–8 important design decisions**.

Examples:

```text
Why FastAPI rather than a local script?
Why synchronous processing rather than a queue?
Why PostgreSQL rather than files?
Why one model per target rather than a shared model?
Why service / repository separation?
Why batch preprocessing instead of computing features on demand?
Why REST rather than WebSocket?
Why store derived artifacts rather than regenerate them?
```

For every decision show:

### Decision

What design choice was made?

### Why it makes sense

What problem does this choice solve?

### Benefits

What becomes easier, safer, faster, or clearer?

### Costs

What complexity, performance cost, coupling, maintenance burden, or limitation does it introduce?

### Alternatives

Show one or two realistic alternatives.

### When the alternative becomes better

Explain which requirement changes would justify switching designs.

Example:

```text
Decision:
Use FastAPI instead of a standalone Python script.

Why:
The prediction logic needs to be accessed by a frontend and possibly other services.

Benefits:
Clear HTTP interface, validation, easier integration.

Costs:
Deployment, networking, authentication, monitoring, and failure handling become necessary.

Alternative:
CLI / local Python module.

Better when:
The system is only used locally by one analyst and does not require remote access.
```

Avoid judging architecture as simply:

```text
good / bad
```

Prefer:

```text
appropriate under these constraints
```

---

# 9. Design quality critique

Add a compact section inside `Design Review`:

## What is strong?

Identify architecture choices that are genuinely well-designed.

Examples:

- clear module boundary
- good abstraction
- useful validation
- separation of concerns
- reproducible pipeline
- testable components
- stable artifact contract
- safe handling of state

## What is fragile?

Identify realistic weaknesses.

Examples:

- tight coupling
- hidden mutable state
- duplicated logic
- weak validation
- missing tests
- unclear interfaces
- poor failure handling
- scaling bottleneck
- dependency risk
- premature abstraction

## What would become painful later?

Think about:

```text
5 engineers
100x traffic
10x data
multiple customers
multiple models
production deployment
frequent requirement changes
```

Do not criticize hypothetical problems unless the architecture genuinely makes them plausible.

---

# 10. View 3 — SWE Concepts

Use the repository as a case study for reusable engineering knowledge.

Do not turn this into a general textbook.

Select only **5–10 concepts actually relevant to the repository**.

Possible concepts include:

### Architecture

- abstraction
- modularity
- separation of concerns
- dependency direction
- interface
- coupling
- cohesion
- service layer
- repository pattern
- dependency injection

### Runtime

- process
- thread
- async
- event loop
- concurrency
- queue
- background worker
- stateless service
- stateful service

### Web / backend

- HTTP
- REST
- API
- endpoint
- middleware
- authentication
- serialization
- request validation
- WebSocket

### Data

- database
- schema
- transaction
- migration
- index
- cache
- batch processing
- streaming

### ML / AI

- inference
- training
- feature pipeline
- model checkpoint
- evaluation
- data leakage
- embedding
- vector database
- model serving
- agent state

### Reliability

- logging
- observability
- retry
- idempotency
- failure isolation
- validation
- testing
- CI/CD

For each selected concept explain:

```text
Concept
→ where it appears in this repo
→ what problem it solves
→ trade-off
→ when I should use it myself
```

Example:

```text
Dependency Injection

Where:
The API layer receives a database/service dependency instead of constructing it directly.

Why:
Makes components easier to replace and test.

Trade-off:
Adds abstraction and can make simple code harder to follow.

Use when:
Several components need interchangeable implementations or isolated testing.
```

---

# 11. View 4 — Practice

This is the most important learning section.

Focus heavily on practical engineering reasoning.

Generate approximately **8–12 questions**.

Questions should not mainly test memory.

They should test:

```text
architecture
trade-offs
failure modes
requirements
scaling
interfaces
abstraction
implementation strategy
AI coding instructions
```

Questions should be moderately difficult.

Some should intentionally contain tempting but incomplete solutions.

---

# 12. Practice question categories

Include several categories.

## A. Design diagnosis

Example:

```text
The API currently reads a 2 GB CSV file on every request.

Which redesign would you choose?

A. Increase the server timeout.
B. Load the dataset once into application memory.
C. Move the data into a database or prepared artifact.
D. Rewrite the frontend.

Explain why.
```

The answer should discuss constraints rather than merely identify the letter.

---

## B. Requirement change

Example:

```text
The system was designed for one user running locally.

Now twenty researchers need simultaneous access.

Which parts of the architecture become problematic first?
```

Possible answer areas:

```text
state
database concurrency
deployment
authentication
file access
resource contention
```

---

## C. Failure scenario

Example:

```text
The external model API occasionally times out.

Where should retry logic live?

API route?
service layer?
frontend?
everywhere?

What are the risks of retrying blindly?
```

Expected reasoning may include:

```text
idempotency
backoff
duplicate operations
failure boundaries
```

---

## D. Architecture alternative

Example:

```text
Would replacing FastAPI with a CLI make the system simpler?

Under what requirements would this be a better design?

Under what requirements would it clearly be worse?
```

There may be multiple defensible answers.

---

## E. Scaling scenario

Use realistic changes such as:

```text
100x traffic
100x dataset size
10 models
multiple users
multiple services
real-time requirements
```

Ask which component breaks first and why.

---

## F. Refactoring scenario

Show a simplified version of a problematic structure:

```text
route
  ├─ reads database
  ├─ transforms data
  ├─ runs model
  ├─ writes result
  └─ formats response
```

Ask the reader to redesign the responsibility boundaries.

---

## G. Debugging scenario

Provide architecture-level bugs rather than syntax bugs.

Example:

```text
Training AUROC is excellent.
Production performance is poor.
The preprocessing pipeline is implemented separately in training and serving.

What architecture problem should you investigate?
```

---

## H. AI instruction exercise

Train the reader to instruct coding agents precisely.

Example:

```text
You want an AI agent to extract preprocessing logic from the API route.

Write an implementation instruction that specifies:

- desired module boundary
- unchanged external behavior
- expected interface
- tests
- files allowed to change
- failure behavior
```

After the reader answers, reveal a strong example instruction.

Example reference:

```text
Extract preprocessing from `routes/predict.py` into a pure function in
`services/preprocessing.py`.

Requirements:
- preserve the existing `/predict` API schema
- function input must be the validated request model
- function output must be the existing feature dictionary
- no database or HTTP calls inside the preprocessing function
- update existing route to call the new function
- add unit tests covering missing values and invalid ranges
- do not change model inference logic
```

This exercise is especially important.

---

# 13. Practice interaction design

Questions should use progressive disclosure.

Recommended interaction:

```text
Scenario
↓
User chooses or writes reasoning
↓
Show consequence
↓
Show expert analysis
↓
Show transferable lesson
```

For multiple-choice questions:

- use 2–4 plausible options
- avoid obvious joke answers
- allow trade-off discussion
- explain why tempting wrong answers fail

For open-ended questions:

provide a hidden:

```text
Show expert reasoning
```

button.

Expert reasoning should emphasize the thinking process:

```text
Requirement
→ Constraint
→ Design choice
→ Trade-off
```

---

# 14. Increasing difficulty

Questions should gradually become harder.

Suggested progression:

```text
1–2:
Understand architecture

3–4:
Identify design rationale

5–6:
Analyze trade-offs

7–8:
Diagnose failure / scaling problems

9–10:
Redesign architecture

11–12:
Write precise AI implementation instructions
```

Avoid trivia such as:

```text
Which file contains function X?
```

unless the file organization itself teaches an architectural principle.

---

# 15. View 5 — Glossary

Create one unified glossary for important small concepts.

This prevents the rest of the website from repeatedly explaining terminology.

Include important concepts encountered in the repository.

Examples:

```text
script
server
process
API
REST
FastAPI
Node.js
React
database
schema
endpoint
middleware
async
queue
cache
Docker
CI/CD
ORM
migration
artifact
checkpoint
embedding
inference
```

Do not automatically include all of these.

Only include:

- concepts appearing in the repository
- concepts needed to understand the architecture
- closely related concepts necessary to understand a trade-off

Each glossary entry should be extremely compact.

Use this format:

```text
FastAPI

What:
Python framework for building HTTP APIs.

Use:
Useful when Python logic needs to be exposed as a web service.

Trade-off:
Adds server, deployment, networking, and API-management complexity.
```

Another example:

```text
Script

What:
A program usually executed directly to perform a task.

Use:
Good for automation, experiments, data processing, or one-off workflows.

Trade-off:
Simple to build, but harder to expose as a persistent multi-user service.
```

Another:

```text
Node.js

What:
Runtime that executes JavaScript outside the browser.

Use:
Common for web servers, tooling, and full-stack JavaScript applications.

Trade-off:
Excellent ecosystem and async I/O, but CPU-heavy work often needs another execution strategy.
```

Glossary should support:

- search
- alphabetical navigation
- concept tags

Do not create long encyclopedia entries.

---

# 16. Inline glossary behavior

Important glossary terms appearing elsewhere in the site may be visually marked.

Example:

```text
FastAPI
```

Hover or click:

```text
Python framework for building HTTP APIs.
```

Keep inline tooltips to one sentence.

The full explanation belongs in the Glossary page.

This keeps the main pages clean.

---

# 17. Engineering pattern extraction

While studying the repository, identify reusable patterns.

Examples:

```text
Thin API route
Service layer
Producer / consumer artifact
Training-serving parity
Schema validation
Caching boundary
Adapter around external API
Background worker
Configuration separation
Pure transformation function
```

For each important pattern, briefly state:

```text
Pattern
Why it exists
Where it appears
When useful
Main downside
```

Do not create a separate top-level page.

Place these patterns inside `SWE Concepts`.

---

# 18. Teach design taste

The HTML should explicitly help develop engineering taste.

For important components ask:

```text
Is this complexity paying for something?

What future change does this abstraction make easier?

What future change does it make harder?

Is the abstraction solving a real problem or a hypothetical one?

Which dependency direction makes the system easier to test?

Where should state live?

Where should validation happen?

Which interface should remain stable?

What failure should this component be responsible for?

What knowledge should this module NOT have?
```

Use these questions throughout Design Review and Practice.

---

# 19. Avoid simplistic rules

Do not teach:

```text
Microservices are better.
More abstraction is better.
More classes are better.
More layers are better.
Async is better.
Databases are better than files.
Frameworks are better than scripts.
```

Teach conditional reasoning.

Example:

```text
A script may be better than a web service when the workflow is local,
single-user, short-lived, and rarely integrated with other systems.
```

The reader should learn:

```text
engineering = decisions under constraints
```

not:

```text
engineering = memorizing best practices
```

---

# 20. Connect design to code

When useful, trace one important flow through real code.

Example:

```text
HTTP request
→ route
→ schema validation
→ service
→ database
→ model
→ response
```

Allow the reader to click a stage and reveal:

```text
file
function / class
responsibility
```

Avoid showing large code blocks.

Prefer short excerpts under approximately 10–15 lines.

Only show code that teaches architecture.

---

# 21. Implementation depth

When a repository contains important implementation details, explain them.

Examples:

```text
How async requests propagate
How dependency injection works
How database sessions are managed
How objects are serialized
How model artifacts are loaded
How caching works
How configuration enters the system
How tests replace external dependencies
```

But only explain implementation details that improve architectural understanding.

Do not turn the HTML into line-by-line code documentation.

---

# 22. AI design skill training

The final purpose is partly to improve the reader's ability to direct AI coding agents.

Whenever a redesign exercise appears, show how a vague instruction differs from a strong instruction.

Example:

### Weak

```text
Make the backend cleaner.
```

### Better

```text
Refactor the prediction route so HTTP handling, preprocessing, and inference
are separate responsibilities.

Constraints:
- preserve the existing API contract
- preprocessing should be a pure function
- model loading should happen once at startup
- route should not directly access model internals
- add unit tests for preprocessing
- do not change the frontend
```

Teach the reader that strong AI instructions define:

```text
Goal
Scope
Architecture boundary
Interface
Constraints
Invariants
Failure behavior
Tests
Definition of done
```

---

# 23. HTML density rules

The page should remain visually calm.

Avoid showing all information simultaneously.

Default viewport should contain approximately:

```text
one summary
one main visualization
one selected detail panel
```

Use:

- tabs
- accordions
- click-to-expand
- tooltips
- hidden expert answers

Avoid:

- giant dashboards
- many simultaneous cards
- dense tables
- long scrolling walls of text
- multiple charts describing the same thing
- decorative metrics
- excessive animation

---

# 24. Visual hierarchy

Recommended hierarchy:

```text
Primary:
architecture and active exercise

Secondary:
design explanation

Hidden until requested:
deeper implementation details
expert reasoning
alternatives
glossary definitions
```

Use whitespace aggressively.

Visible cards should usually contain no more than:

```text
1–2 short paragraphs
or
3–5 bullets
```

---

# 25. Navigation

Top-level navigation:

```text
System Map
Design Review
SWE Concepts
Practice
Glossary
```

Do not create more top-level navigation unless the repository is unusually complex.

Inside pages, use secondary selectors rather than new pages.

---

# 26. Practice over passive reading

At least **30–40% of the learning content** should involve active reasoning.

Do not create an HTML page where the reader mainly scrolls and reads.

Frequently ask:

```text
What would you do?

Why?

What breaks?

Which trade-off matters?

What requirement would change your decision?
```

Then reveal expert reasoning.

---

# 27. Repository-specific difficulty

Do not artificially simplify engineering questions.

When the repository contains meaningful complexity, allow questions involving several constraints simultaneously.

Example:

```text
The current model API takes 800 ms.
A new dashboard needs updates every second.
Each user monitors 20 patients.
The server has limited memory.
Model loading takes 4 seconds.

Which changes would you consider?

What should remain synchronous?
What should be cached?
Should inference be batched?
Should the model be loaded per request?
Would a queue help?
```

There may be multiple valid architectures.

The expert explanation should compare them.

---

# 28. Distinguish architecture levels

Teach the reader not to mix different levels.

Possible levels:

```text
Language
Runtime
Framework
Library
Application module
Service
Process
Deployment
Infrastructure
Data model
ML model
```

Example:

```text
Python ≠ FastAPI
FastAPI ≠ server process
API ≠ deployment
Node.js ≠ React
database ≠ ORM
model checkpoint ≠ inference service
```

Use the Glossary and SWE Concepts sections to reinforce these distinctions.

---

# 29. Security and sensitive data

Never expose:

- credentials
- API keys
- tokens
- private URLs
- patient-level records
- customer-level records
- secrets
- private environment variables

When learning from data repositories, use:

```text
schema
column names
aggregates
row counts
synthetic examples
```

rather than sensitive rows.

---

# 30. Static implementation preference

For a repository explainer, prefer a self-contained static HTML site unless persistence is required.

Recommended structure:

```text
repo-learning-site/
└── dist/
    └── index.html
```

Prefer inline CSS and JavaScript when practical.

Avoid unnecessary frontend frameworks for the explainer itself.

The learning artifact should remain easy to move and run locally.

---

# 31. Verification

Before handoff confirm:

- HTML exists.
- Default view loads correctly.
- Architecture nodes are clickable.
- Detail inspector updates.
- Design-review sections expand correctly.
- Glossary search works.
- Tooltips work.
- Practice questions progress correctly.
- Expert reasoning can be revealed.
- Restart resets exercises.
- Navigation targets existing views.
- JavaScript contains no obvious errors.
- No sensitive information is exposed.
- Local server returns HTTP 200.

When browser testing is available:

Smoke-test:

```text
System Map
→ inspect node
→ open Design Review
→ inspect trade-off
→ answer Practice question
→ reveal expert reasoning
→ search Glossary
```

---

# 32. Final handoff

Lead with:

```text
local URL
```

or the artifact path.

Then briefly state:

- what system was analyzed
- which repository evidence was treated as canonical
- major architecture identified
- strongest design decision
- biggest engineering risk
- important concepts covered
- number of practical exercises included

Keep the handoff concise.

---

# 33. Core philosophy

Always optimize for this learning loop:

```text
See
→ Explain
→ Question
→ Compare
→ Redesign
→ Implement
```

The reader should leave understanding not only:

```text
How does this repository work?
```

but also:

```text
Why is it designed this way?

What would I have done differently?

When would my alternative be better?

What engineering concept explains this decision?

How would I tell an AI agent exactly what to change?
```

The purpose of the artifact is to gradually turn unfamiliar repositories into reusable engineering intuition.