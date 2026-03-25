<!-- Source: https://developer.android.com/develop/ui/compose/phases -->
<!-- Type: official -->
<!-- Priority: high -->
<!-- Topic: compose-phases -->
<!-- Extracted: 2026-03-24 -->
<!-- Verified: — -->

# Jetpack Compose phases

## Rules
- DO: An x, y coordinate where it should be drawn
- DO: Use that state as input to a layout modifier ( padding() , height() , or
similar)

## Code Patterns
### State reads
```kotlin
// State read without property delegate.
val paddingState: MutableState<Dp> = remember { mutableStateOf(8.dp) }
Text(
    text = "Hello",
    modifier = Modifier.padding(paddingState.value)
)PhasesSnippets.kt
```

### State reads
```
// State read with property delegate.
var padding: Dp by remember { mutableStateOf(8.dp) }
Text(
    text = "Hello",
    modifier = Modifier.padding(padding)
)PhasesSnippets.kt
```

### Phase 1: Composition
```
var padding by remember { mutableStateOf(8.dp) }
Text(
    text = "Hello",
    // The `padding` state is read in the composition phase
    // when the modifier is constructed.
    // Changes in `padding` will invoke recomposition.
    modifier = Modifier.padding(padding)
)PhasesSnippets.kt
```

### Phase 2: Layout
```
var offsetX by remember { mutableStateOf(8.dp) }
Text(
    text = "Hello",
    modifier = Modifier.offset {
        // The `offsetX` state is read in the placement step
        // of the layout phase when the offset is calculated.
        // Changes in `offsetX` restart the layout.
        IntOffset(offsetX.roundToPx(), 0)
    }
)PhasesSnippets.kt
```

### Phase 3: Drawing
```
var color by remember { mutableStateOf(Color.Red) }
Canvas(modifier = modifier) {
    // The `color` state is read in the drawing phase
    // when the canvas is rendered.
    // Changes in `color` restart the drawing.
    drawRect(color)
}PhasesSnippets.kt
```

### Optimize state reads
```kotlin
Box {
    val listState = rememberLazyListState()

    Image(
        // ...
        // Non-optimal implementation!
        Modifier.offset(
            with(LocalDensity.current) {
                // State read of firstVisibleItemScrollOffset in composition
                (listState.firstVisibleItemScrollOffset / 2).toDp()
            }
        )
    )

    LazyColumn(state = listState) {
        // ...
    }
}PhasesSnippets.kt
```

### Recomposition loop (cyclic phase dependency)
```
Box {
    var imageHeightPx by remember { mutableIntStateOf(0) }

    Image(
        painter = painterResource(R.drawable.rectangle),
        contentDescription = "I'm above the text",
        modifier = Modifier
            .fillMaxWidth()
            .onSizeChanged { size ->
                // Don't do this
                imageHeightPx = size.height
            }
    )

    Text(
        text = "I'm below the image",
        modifier = Modifier.padding(
            top = with(LocalDensity.current) { imageHeightPx.toDp() }
        )
    )
}PhasesSnippets.kt
```

## Pitfalls
- Key Point: The measurement step and the placement step have separate restart
scopes, meaning that state reads in the placement step don't re-invoke the
measurement step before that. However, these two steps are often intertwined, so
a state read in the placement step can affect other restart scopes
- Note: You might wonder if taking a lambda parameter might add extra cost
compared to taking a value. It does. However, the benefit of limiting
the state read to the layout phase overweighs the cost in this case. The value 
of firstVisibleItemScrollOffset changes every frame during scroll, and by
def

## Guidelines
- Consider the following example. This example has an Image() which uses the
offset modifier to offset its final layout position, resulting in a parallax
effect as the user scrolls.
- This version takes a lambda parameter, where the resulting offset is returned by
the lambda block. Update the code to use it:
- This guide previously mentioned that the phases of Compose are always invoked in
the same order, and that there is no way to go backwards while in the same
frame. However, that doesn't prohibit apps getting into composition loops
across different frames. Consider this example:
- The fix for the preceding sample is to use the proper layout primitives. The
preceding example can be implemented with a Column() , but you may have a more
complex example which requires something custom, which will require writing a
custom layout. See the Custom layouts guide for more inform
- The general principle here is to have a single source of truth for multiple UI
elements that should be measured and placed with regards to one another. Using
a proper layout primitive or creating a custom layout means that the minimal
shared parent serves as the source of truth that can coordinate the relation
between multiple elements. Introducing a dynamic state breaks this principle.

## Core Concepts

1. **State Reads and Observability**:
   - Evidence from the doc includes sections on "Optimize state reads", "Recomposition loop (cyclic phase dependency)", guidelines about avoiding recomposition loops, and rules around using `mutableStateOf` to ensure observability of UI elements.
   
   **Mechanism**: 
     - State changes trigger recompositions in Jetpack Compose. Observing states through `MutableState<T>` ensures that the UI updates correctly on state changes.
   
   **Failure Mode**: 
     - Non-observable states or incorrect placement of observable states can lead to infinite loops and inefficient recomposition, which may cause performance issues.

2. **Phases in Compose Lifecycle**:
   - Evidence from the doc includes sections explicitly titled "Phase 1: Composition", "Phase 2: Layout", and "Phase 3: Drawing". The guidelines also emphasize understanding these phases' roles.
   
   **Mechanism**: 
     - Each phase is responsible for specific tasks (composition builds UI elements, layout measures and places them, drawing renders the canvas).
   
   **Failure Mode**: 
     - Misunderstanding or misusing state reads in different phases can lead to unnecessary recompositions, poor performance, or incorrect UI updates.

3. **Single Source of Truth**:
   - Evidence from the doc includes a direct mention in the guidelines section, emphasizing that using proper layout primitives or custom layouts ensures there is one source of truth for measurements and placements across multiple UI elements.
   
   **Mechanism**: 
     - A single parent element manages state changes affecting its children, preventing inconsistencies.
   
   **Failure Mode**: 
     - Introducing dynamic states without a central coordinator can lead to inconsistent UI updates, recomposition loops, or performance bottlenecks.

## Mental Model

- **The Problem**: Ensuring efficient recomposition and avoiding infinite loops while managing state changes in Jetpack Compose can be tricky without understanding how observability triggers recompositions and the interplay between different lifecycle phases.
  
- **Core Insight**: UI is a function of observable state. State changes trigger recomposition, which ensures that the UI updates to reflect the current state correctly.

- **How concepts connect**:
  - Phases in Compose Lifecycle → Observability (state reads) → Recomposition
  - Single Source of Truth → Avoiding Infinite Loops

## Decision Framework

| I need to... | Use | NOT | Because |
| --- | --- | --- | --- |
| Ensure UI updates correctly on state changes | `mutableStateOf` for observable states | Non-observable states (e.g., plain variables) | Compose won't trigger recomposition if the state is not observed |

## Common Mistakes

### Name: Infinite Recomposition Loop
- **Looks like**: 
  ```kotlin
  var imageHeightPx by remember { mutableIntStateOf(0) }
  
  Image(
      modifier = Modifier.onSizeChanged { size -> imageHeightPx = size.height },
      //...
  )
  
  Text(
      modifier = Modifier.padding(top = with(LocalDensity.current) { imageHeightPx.toDp() }),
      //...
  )
  ```
- **Why it breaks**: The height of the image is set after it has been laid out, causing a recomposition loop as the `Text`'s padding changes.
- **Correct**: 
  ```kotlin
  Box {
    Image(
        modifier = Modifier.fillMaxWidth().onSizeChanged { size -> 
            // Use proper layout or custom layout to ensure only one source of truth
        },
        //...
    )
    
    Text(
        modifier = Modifier.padding(top = 8.dp), // Fixed padding or use proper layout
        //...
    )
  }
  ```

### Name: Inefficient State Reads During Composition

- **Looks like**: 
  ```kotlin
  val listState = rememberLazyListState()
  
  Image(
      modifier = Modifier.offset {
          with(LocalDensity.current) { (listState.firstVisibleItemScrollOffset / 2).toDp() }
      },
      //...
  )
  ```
- **Why it breaks**: The offset calculation is done in composition, leading to recomposition on every frame change, which can be costly.
- **Correct**:
  ```kotlin
  Image(
      modifier = Modifier.offset {
          IntOffset(listState.firstVisibleItemScrollOffset / 2, 0)
      },
      //...
  )
  ```

## Key Relationships

- Observability (state reads) enables Recomposition to happen correctly.
- Single Source of Truth prevents Infinite Loops in recompositions by ensuring consistent state management across UI elements.

## Concepts (for graph)
- The three phases of a frame
- Composition
- Layout
- Drawing
- Figure 1.
- Understand the phases
- Figure 2.
- Figure 3.
- Figure 4.
- Measure children
- Decide own size
- Place children

<!-- Quality Report
## Quality Report

| Section | Score | Issue (if < 4) |
| --- | --- | --- |
| Core Concepts | 5 | - |
| Mental Model | 5 | - |
| Decision Framework | 4 | Use table format correctly and ensure consistency in the "Because" column. |
| Common Mistakes | 4 | Ensure examples are directly linked to explanations of why they break and how to fix them for clarity. |
| Key Relationships | 5 | - |

## Verdict: NEEDS_FIX

## Fixes (only if NEEDS_FIX)
Decision Framework: Use table format correctly and ensure consistency in the "Because" column.
Common Mistakes: Ensure examples are directly linked to explanations of why they break and how to fix them for clarity.
-->
