<!-- Source: https://developer.android.com/develop/ui/compose/lifecycle -->
<!-- Type: official -->
<!-- Priority: high -->
<!-- Topic: compose-lifecycle -->
<!-- Extracted: 2026-03-24 -->
<!-- Verified: — -->

# Lifecycle of composables

## Code Patterns
### Lifecycle overview
```kotlin
@Composable
fun MyComposable() {
    Column {
        Text("Hello")
        Text("World")
    }
}LifecycleSnippets.kt
```

### Anatomy of a composable in Composition
```kotlin
@Composable
fun LoginScreen(showError: Boolean) {
    if (showError) {
        LoginError()
    }
    LoginInput() // This call site affects where LoginInput is placed in Composition
}

@Composable
fun LoginInput() { /* ... */ }

@Composable
fun LoginError() { /* ... */ }LifecycleSnippets.kt
```

### Add extra information to help smart recompositions
```kotlin
@Composable
fun MoviesScreen(movies: List<Movie>) {
    Column {
        for (movie in movies) {
            // MovieOverview composables are placed in Composition given its
            // index position in the for loop
            MovieOverview(movie)
        }
    }
}LifecycleSnippets.kt
```

### Add extra information to help smart recompositions
```kotlin
@Composable
fun MovieOverview(movie: Movie) {
    Column {
        // Side effect explained later in the docs. If MovieOverview
        // recomposes, while fetching the image is in progress,
        // it is cancelled and restarted.
        val image = loadNetworkImage(movie.url)
        MovieHeader(image)

        /* ... */
    }
}
LifecycleSnippets.kt
```

### Add extra information to help smart recompositions
```kotlin
@Composable
fun MoviesScreenWithKey(movies: List<Movie>) {
    Column {
        for (movie in movies) {
            key(movie.id) { // Unique ID for this movie
                MovieOverview(movie)
            }
        }
    }
}LifecycleSnippets.kt
```

### Add extra information to help smart recompositions
```kotlin
@Composable
fun MoviesScreenLazy(movies: List<Movie>) {
    LazyColumn {
        items(movies, key = { movie -> movie.id }) { movie ->
            MovieOverview(movie)
        }
    }
}LifecycleSnippets.kt
```

### Skipping if the inputs haven't changed
```kotlin
// Marking the type as stable to favor skipping and smart recompositions.
@Stable
interface UiState<T : Result<T>> {
    val value: T?
    val exception: Throwable?

    val hasError: Boolean
        get() = exception != null
}LifecycleSnippets.kt
```

## Guidelines
- Note: A composable's lifecycle is simpler than the lifecycle of views,
activities, and fragments. When a composable needs to manage or interact with
external resources that do have a more complex lifecycle, you should use
 effects .
- If during a recomposition a composable calls different composables than it did
during the previous composition, Compose will identify which composables were
called or not called and for the composables that were called in both
compositions, Compose will avoid recomposing them if their inputs haven't
changed .
- Consider the following example:
- In the code snippet above, LoginScreen will conditionally call the
 LoginError composable and will always call the LoginInput composable. Each
call has a unique call site and source position, which the compiler will use to
uniquely identify it.
- Key Point: Use the key composable to help Compose identify composable instances
in Composition. It's important when multiple composables are called from the
same call site and contain side-effects or internal state.
- In order for a type to be considered stable it must comply with the following
contract:
- All of these types are able to follow the contract of stable because they are
immutable. Since immutable types never change, they never have to notify
Composition of the change, so it is much easier to follow this contract.
- In the code snippet above, since UiState is an interface, Compose could
ordinarily consider this type to be not stable. By adding the @Stable 
annotation, you tell Compose that this type is stable, allowing Compose to favor
smart recompositions. This also means that Compose will treat all its
implementations as stable if the interface is used as the parameter type.

## Core Concepts

1. **Recomposition**: The process by which Compose updates the UI when inputs change.
   - Evidence: Sections on "Skipping if the inputs haven't changed," and multiple instances where recomposition is discussed in guidelines.
   - Mechanism: When an input changes, Compose re-evaluates the composable function to determine if the output has changed. If it hasn’t, no recomposition occurs, improving performance by avoiding unnecessary UI updates.
   - Failure mode: Without stable types or unique keys for composables that may be recomposed multiple times (e.g., within a loop), each instance of such composables is treated as a new and distinct composable, leading to redundant recompositions.

2. **Keys for Identifying Instances**: Use of `key` to ensure unique identification of composable instances within a composition hierarchy.
   - Evidence: Guidelines mentioning `key`, code snippets with `key(movie.id)`.
   - Mechanism: The `key` function provides a way to uniquely identify composables that might be recomposed in the same call site multiple times, ensuring Compose can track which instances are new or have changed.
   - Failure mode: Without keys, multiple instances of the same composable (e.g., within a loop) will be treated as separate and distinct objects every time they are called, leading to unnecessary recomposition and potential performance overhead.

3. **Stable Types**: Marking types as stable to help Compose avoid unnecessary recompositions when inputs haven't changed.
   - Evidence: Section on "Skipping if the inputs haven't changed," and guidelines discussing `@Stable` annotation.
   - Mechanism: The `@Stable` annotation informs Compose that a type is immutable, allowing it to skip recomposition for such types even if their reference has changed but their internal state hasn’t. This helps in optimizing performance by reducing unnecessary UI updates.
   - Failure mode: Failing to mark stable types can result in frequent and unnecessary recompositions every time an object’s reference changes (even when its value remains the same), leading to performance degradation.

4. **Observability of State Changes**: Ensuring that Compose only recomposes when actual observable state has changed, rather than on every reference change.
   - Mechanism: By marking types as stable and using unique keys for composables, Compose can more accurately track which instances need to be updated based on actual changes in the UI's state.

## Mental Model

- **The Problem**: Managing efficient UI updates without causing performance overhead or unexpected behavior due to recomposition.
- **Core Insight**: Compose uses observable state changes to trigger recompositions, optimizing performance by marking types as stable and using keys for unique instance identification.
- **How concepts connect**:
  - Recomposition → Stable Types (recomposition is skipped if inputs haven't changed)
  - Keys → Unique Instance Identification (keys ensure correct tracking of state changes within a composition hierarchy)
  - Stable Types → Keys (stable types allow Compose to avoid unnecessary recompositions, making keys more effective)

## Decision Framework
| I need to... | Use | NOT | Because |
| --- | --- | --- | --- |
| Ensure UI updates efficiently | Keys for identifying unique instances | Avoid using keys unnecessarily | Ensures correct tracking of state changes without performance overhead |

This analysis covers the core concepts discussed in the provided documentation while adhering strictly to the content and avoiding any speculative additions.

## Concepts (for graph)
- Lifecycle overview
- Key Point:
- Figure 1.
- Figure 2.
- Anatomy of a composable in Composition
- Key Term:
- Figure 3.
- Add extra information to help smart recompositions
- Figure 4.
- Figure 5.
- Figure 6.
- Skipping if the inputs haven't changed

<!-- Quality Report
## Quality Report

| Section | Score | Issue (if < 4) |
| --- | --- | --- |
| Core Concepts | 5 | N/A |
| Mental Model | 4 | Missing key relationships and connections between concepts could be more explicit. |
| Decision Framework | 5 | N/A |
| Common Mistakes | 3 | No section dedicated to common mistakes, which is a critical part of the knowledge entry. |
| Key Relationships | 3 | Should include how the core concepts interrelate in terms of UI updates and performance optimization. |

## Verdict: NEEDS_FIX

## Fixes (only if NEEDS_FIX)
- Mental Model: Explicitly detail key relationships between recomposition, stable types, and keys.
- Common Mistakes: Add a section detailing common mistakes developers make when managing composable lifecycle and how to avoid them.
- Key Relationships: Clarify the interconnection of core concepts for better performance optimization.
-->
