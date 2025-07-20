# Course transcripts

Crafting code that is easy to and maintain.

## Purpose

Build habits for productivity and reliability.

```mermaid
graph LR
    subgraph Productivity
        A1["Quick releases"]
        A2["More features"]
        A3["Smaller teams"]
        A4["Deadlines"]
        A[Productivity]
        A1 --> A
        A2 --> A
        A3 --> A
        A4 --> A
    end

    subgraph Reliability
        B1["Test coverage"]
        B2["Linters"]
        B3["Modularity"]
        B4["Graceful degradation"]
        B[Reliability]
        B1 --> B
        B2 --> B
        B3 --> B
        B4 --> B
    end

    C["Productivity AND Reliability"]
    A --> C
    B --> C
```

## Modularity

Modularity is the practice of breaking down code into smaller pieces. This makes it easier to understand, test, and maintain. 

However, cutting code arbitrarily can lead to confusion. Principles that help in a beneficial cut:

### Separate by lifecycle

Keep stable code separate from evolving code.
The feature to "display the color manual" can change by user-preference.
Hence, separate it from "color-pair mapping", which goes by the standard.

### Name by purpose

Names for files, classes, or functions should be self-evident.
A good name conveys purpose - without digging further into their code or comments.
This saves time when reading code.

### Avoid side effects

Side effects are changes to state - display, storage, network, etc.
They bring dependency. Isolate your logic into pure functions that return a value without changing the state.
Keep dependencies separate.

### Inject dependencies

When it isn't possible to isolate with pure functions, inject dependencies.
Pass in the dependencies as parameters, rather than hardcoding them.
This makes it easy to mock the dependencies in tests, and to swap them out in production.

## Tests

Follow the FIRST principles for writing tests:

| Principle | Enables | Benefits |
|-----------|---------|----------|
| Fast      | Frequent execution | Find issues early |
| Independent| Isolation of tests | Easier failure diagnosis |
| Repeatable | Consistent results | Stable tests, low maintenance |
| Self-validating| Automatic pass/fail | Reduced manual effort - single Pass/Fail result |
| Thorough   | Coverage with strong asserts | Passing tests ensure customer satisfaction |
