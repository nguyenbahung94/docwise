<!-- Source: https://developer.android.com/develop/ui/compose/performance/bestpractices?hl=en -->
<!-- Type: official -->
<!-- Priority: high -->
<!-- Topic: compose-performance -->
<!-- Extracted: 2026-03-24 -->
<!-- Verified: — -->

# Follow best practices

## Code Patterns
### [DON'T] Use remember to minimize expensive calculations
```kotlin
@Composable
fun ContactList(
    contacts: List<Contact>,
    comparator: Comparator<Contact>,
    modifier: Modifier = Modifier
) {
    LazyColumn(modifier) {
        // DON’T DO THIS
        items(contacts.sortedWith(comparator)) { contact ->
            // ...
        }
    }
}PerformanceSnippets.kt
```

### [DO] Use remember to minimize expensive calculations
```kotlin
@Composable
fun ContactList(
    contacts: List<Contact>,
    comparator: Comparator<Contact>,
    modifier: Modifier = Modifier
) {
    val sortedContacts = remember(contacts, comparator) {
        contacts.sortedWith(comparator)
    }

    LazyColumn(modifier) {
        items(sortedContacts) {
            // ...
        }
    }
}PerformanceSnippets.kt
```

### [DON'T] Use lazy layout keys
```kotlin
@Composable
fun NotesList(notes: List<Note>) {
    LazyColumn {
        items(
            items = notes
        ) { note ->
            NoteRow(note)
        }
    }
}PerformanceSnippets.kt
```

### [DO] Use lazy layout keys
```kotlin
@Composable
fun NotesList(notes: List<Note>) {
    LazyColumn {
        items(
            items = notes,
            key = { note ->
                // Return a stable, unique key for the note
                note.id
            }
        ) { note ->
            NoteRow(note)
        }
    }
}PerformanceSnippets.kt
```

### [DON'T] Use derivedStateOf to limit recompositions
```kotlin
val listState = rememberLazyListState()

LazyColumn(state = listState) {
    // ...
}

val showButton = listState.firstVisibleItemIndex > 0

AnimatedVisibility(visible = showButton) {
    ScrollToTopButton()
}PerformanceSnippets.kt
```

### [DO] Use derivedStateOf to limit recompositions
```kotlin
val listState = rememberLazyListState()

LazyColumn(state = listState) {
    // ...
}

val showButton by remember {
    derivedStateOf {
        listState.firstVisibleItemIndex > 0
    }
}

AnimatedVisibility(visible = showButton) {
    ScrollToTopButton()
}PerformanceSnippets.kt
```

### Defer reads as long as possible
```kotlin
@Composable
fun SnackDetail() {
    // ...

    Box(Modifier.fillMaxSize()) { // Recomposition Scope Start
        val scroll = rememberScrollState(0)
        // ...
        Title(snack, scroll.value)
        // ...
    } // Recomposition Scope End
}

@Composable
private fun Title(snack: Snack, scroll: Int) {
    // ...
    val offset = with(LocalDensity.current) { scroll.toDp() }

    Column(
        modifier = Modifier
            .offset(y = offset)
    ) {
        // ...
    }
}PerformanceSnippets.kt
```

### Defer reads as long as possible
```kotlin
@Composable
fun SnackDetail() {
    // ...

    Box(Modifier.fillMaxSize()) { // Recomposition Scope Start
        val scroll = rememberScrollState(0)
        // ...
        Title(snack) { scroll.value }
        // ...
    } // Recomposition Scope End
}

@Composable
private fun Title(snack: Snack, scrollProvider: () -> Int) {
    // ...
    val offset = with(LocalDensity.current) { scrollProvider().toDp() }
    Column(
        modifier = Modifier
            .offset(y = offset)
    ) {
        // ...
    }
}PerformanceSnippets.kt
```

### Defer reads as long as possible
```kotlin
@Composable
private fun Title(snack: Snack, scrollProvider: () -> Int) {
    // ...
    Column(
        modifier = Modifier
            .offset { IntOffset(x = 0, y = scrollProvider()) }
    ) {
        // ...
    }
}PerformanceSnippets.kt
```

### Defer reads as long as possible
```kotlin
// Here, assume animateColorBetween() is a function that swaps between
// two colors
val color by animateColorBetween(Color.Cyan, Color.Magenta)

Box(
    Modifier
        .fillMaxSize()
        .background(color)
)PerformanceSnippets.kt
```

### Defer reads as long as possible
```kotlin
val color by animateColorBetween(Color.Cyan, Color.Magenta)
Box(
    Modifier
        .fillMaxSize()
        .drawBehind {
            drawRect(color)
        }
)PerformanceSnippets.kt
```

### Avoid backwards writes
```kotlin
@Composable
fun BadComposable() {
    var count by remember { mutableIntStateOf(0) }

    // Causes recomposition on click
    Button(onClick = { count++ }, Modifier.wrapContentSize()) {
        Text("Recompose")
    }

    Text("$count")
    count++ // Backwards write, writing to state after it has been read</b>
}PerformanceSnippets.kt
```

## Guidelines
- Composable functions can run very frequently , as often as for every frame
of an animation. For this reason, you should do as little calculation in the
body of your composable as you can.
- The solution here is to provide item keys . Providing a stable key for
each item lets Compose avoid unnecessary recompositions. In this case, Compose
can determine the item now at spot 3 is the same item that used to be at spot 2.
Since none of the data for that item has changed, Compose doesn't have to
recompose it.
- The problem here is, if the user scrolls the list, listState is constantly
changing as the user drags their finger. That means the list is constantly being
recomposed. However, you don't actually need to recompose it that often—you
don't need to recompose until a new item becomes visible at the bottom. So,
that's a lot of extra computation, which makes your UI perform badly.
- The solution is to use derived state . Derived state lets you tell Compose
which changes of state actually should trigger recomposition. In this case,
specify that you care about when the first visible item changes. When that 
state value changes, the UI needs to recompose, but if the user hasn't yet
scrolled enough to bring a new item to the top, it doesn't have to recompose.
- This is a good improvement, but you can do better! You should be suspicious if
you are causing recomposition just to re-layout or redraw a Composable. In
this case, all you are doing is changing the offset of the Title composable,
which could be done in the layout phase.
- To improve this, use a lambda-based modifier—in this case, drawBehind .
That means the color state is only read during the draw phase. As a result,
Compose can skip the composition and layout phases entirely—when the color
changes, Compose goes straight to the draw phase.
- Compose has a core assumption that you will never write to state that has
already been read . When you do this, it is called a backwards write and it
can cause recomposition to occur on every frame, endlessly.
- You can avoid backwards writes altogether by never writing to state in
Composition. If at all possible, always write to state in response to an event
and in a lambda like in the preceding onClick example.

## Core Concepts

1. **Use `remember` to Minimize Expensive Calculations**
   - Evidence: [DON'T] Use remember to minimize expensive calculations; [DO] Use remember to minimize expensive calculations
   - Explanation: Using `remember` allows you to defer the evaluation of complex expressions until they are needed, preventing unnecessary recompositions and improving performance.
   
2. **Use Lazy Layout Keys for Stable Identification**
   - Evidence: [DON'T] Use lazy layout keys; [DO] Use lazy layout keys
   - Explanation: Providing unique, stable keys for each item in a `LazyColumn` ensures that Compose can identify unchanged elements without recomposing them.

3. **Use `derivedStateOf` to Limit Recompositions**
   - Evidence: [DON'T] Use derivedStateOf to limit recompositions; [DO] Use derivedStateOf to limit recompositions
   - Explanation: The use of `derivedStateOf` allows you to specify exact conditions under which a state change should trigger a recomposition, reducing unnecessary UI updates.

4. **Defer Reads as Long as Possible**
   - Evidence: Defer reads as long as possible (Multiple sections)
   - Explanation: By deferring the evaluation of state until it is strictly necessary (e.g., during layout or draw phases), you can prevent premature evaluations that lead to inefficiencies and unnecessary recompositions.

5. **Avoid Backwards Writes**
   - Evidence: Avoid backwards writes
   - Explanation: Writing to state after reading it within a composable leads to unpredictable recomposition patterns, often causing performance issues.


## Mental Model

- **The Problem**: Composable functions can run frequently due to UI updates or animations, leading to unnecessary computation and poor performance if not optimized.
- **Core Insight**: Minimizing recompositions by deferring state reads until the last possible moment, using stable keys for layouts, and leveraging `derivedStateOf` can significantly improve UI performance in Jetpack Compose applications.
- **How concepts connect**:
  - Use of `remember` → Defers expensive calculations until absolutely necessary
  - Lazy layout keys → Ensures that items are only recomposed when they actually change, improving performance by reducing unnecessary recompositions
  - `derivedStateOf` → Limits recomposition to specific state changes rather than every frame update, maintaining efficient UI updates
  - Deferring reads → Prevents premature evaluation of state, ensuring efficient use of resources and avoiding unnecessary recalculations
  - Avoiding backwards writes → Ensures that state changes are predictable and managed correctly, preventing excessive recompositions


## Decision Framework

| I need to... | Use                           | NOT                                 | Because                                               |
| ---          | ---                          | ---                                | ---                                                  |
| Minimize calculations     | `remember`                    | Directly calculating within composable body             | Prevents unnecessary recompositions for expensive operations, improving performance. |
| Ensure stable layouts    | Lazy layout keys               | Default item keys in `LazyColumn`                       | Ensures that items are only recomposed when necessary, improving overall UI efficiency by avoiding redundant updates. |
| Limit UI updates         | `derivedStateOf`              | Directly referencing state within visibility conditions  | Reduces unnecessary recompositions by specifying explicit dependencies, ensuring that UI components update only when required changes occur. |
| Optimize layout          | Defer reads as long as possible     | Evaluating state in the composition phase               | Allows deferring computation until it is absolutely necessary, improving performance and reducing redundant evaluations. |
| Maintain UI stability   | Avoid backwards writes         | Writing to state after reading it within a composable    | Ensures that recompositions are predictable and controlled, preventing unnecessary updates due to unintended side effects. |

## Concepts (for graph)
- Use remember to minimize expensive calculations
- Use lazy layout keys
- Use derivedStateOf to limit recompositions
- Defer reads as long as possible
- Avoid backwards writes
- Additional Resources
- App performance guide
- Inspect Performance :
- Benchmarking :
- App startup :
- Baseline profiles :
- Recommended for you

<!-- Quality Report
## Quality Report

| Section | Score | Issue (if < 4) |
| --- | --- | --- |
| Core Concepts | 5 | - |
| Mental Model | 5 | - |
| Decision Framework | 5 | - |
| Common Mistakes | 3 | Missing specific examples of common mistakes and their impacts. |
| Key Relationships | 4 | Could be more detailed in explaining how concepts interrelate to provide a holistic understanding. |

## Verdict: NEEDS_FIX

## Fixes (only if NEEDS_FIX)
Common Mistakes: Include specific examples for each concept explaining why they are problematic.
Key Relationships: Elaborate on the interconnectedness of the core concepts to provide a more cohesive mental model.
-->
