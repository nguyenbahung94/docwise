<!-- Source: https://developer.android.com/develop/ui/compose/compositionlocal?hl=en -->
<!-- Type: official -->
<!-- Priority: high -->
<!-- Topic: compose-compositionlocal -->
<!-- Extracted: 2026-03-24 -->
<!-- Verified: — -->

# Locally scoped data with CompositionLocal

## Rules
- DON'T: Avoid CompositionLocal for concepts that aren't thought as tree-scoped or
sub-hierarchy scoped . A CompositionLocal makes sense when it can be
potentially used by any descendant, not by a few of them.

## Code Patterns
### Introduction to CompositionLocal
```kotlin
@Composable
fun MyApp() {
    // Theme information tends to be defined near the root of the application
    val colors = colors()
}

// Some composable deep in the hierarchy
@Composable
fun SomeTextLabel(labelText: String) {
    Text(
        text = labelText,
        color = colors.onPrimary // ← need to access colors here
    )
}CompositionLocalSnippets.kt
```

### Introduction to CompositionLocal
```kotlin
@Composable
fun MyApp() {
    // Provides a Theme whose values are propagated down its `content`
    MaterialTheme {
        // New values for colorScheme, typography, and shapes are available
        // in MaterialTheme's content lambda.

        // ... content here ...
    }
}

// Some composable deep in the hierarchy of MaterialTheme
@Composable
fun SomeTextLabel(labelText: String) {
    Text(
        text = labelText,
        // `primary` is obtained from MaterialTheme's
        // LocalColors CompositionLocal
        color = MaterialTheme.colorScheme.primary
    )
}CompositionLocalSnippets.kt
```

### Introduction to CompositionLocal
```kotlin
@Composable
fun CompositionLocalExample() {
    MaterialTheme {
        // Surface provides contentColorFor(MaterialTheme.colorScheme.surface) by default
        // This is to automatically make text and other content contrast to the background
        // correctly.
        Surface {
            Column {
                Text("Uses Surface's provided content color")
                CompositionLocalProvider(LocalContentColor provides MaterialTheme.colorScheme.primary) {
                    Text("Primary color provided by LocalContentColor")
                    Text("This Text also uses primary as textColor")
                    CompositionLocalProvider(LocalContentColor provides MaterialTheme.colorScheme.error) {
                        DescendantExample()
                    }
                }
            }
        }
    }
}

@Composable
fun DescendantExample() {
    // CompositionLocalProviders also work across composable functions
    Text("This Text uses the error color now")
}CompositionLocalSnippets.kt
```

### Introduction to CompositionLocal
```kotlin
@Composable
fun FruitText(fruitSize: Int) {
    // Get `resources` from the current value of LocalContext
    val resources = LocalContext.current.resources
    val fruitText = remember(resources, fruitSize) {
        resources.getQuantityString(R.plurals.fruit_title, fruitSize)
    }
    Text(text = fruitText)
}CompositionLocalSnippets.kt
```

### Create a CompositionLocal
```kotlin
// LocalElevations.kt file

data class Elevations(val card: Dp = 0.dp, val default: Dp = 0.dp)

// Define a CompositionLocal global object with a default
// This instance can be accessed by all composables in the app
val LocalElevations = compositionLocalOf { Elevations() }CompositionLocalSnippets.kt
```

### Provide values to a CompositionLocal
```kotlin
// MyActivity.kt file

class MyActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContent {
            // Calculate elevations based on the system theme
            val elevations = if (isSystemInDarkTheme()) {
                Elevations(card = 1.dp, default = 1.dp)
            } else {
                Elevations(card = 0.dp, default = 0.dp)
            }

            // Bind elevation as the value for LocalElevations
            CompositionLocalProvider(LocalElevations provides elevations) {
                // ... Content goes here ...
                // This part of Composition will see the `elevations` instance
                // when accessing LocalElevations.current
            }
        }
    }
}CompositionLocalSnippets.kt
```

### Consuming the CompositionLocal
```kotlin
@Composable
fun SomeComposable() {
    // Access the globally defined LocalElevations variable to get the
    // current Elevations in this part of the Composition
    MyCard(elevation = LocalElevations.current.card) {
        // Content
    }
}CompositionLocalSnippets.kt
```

### Pass explicit parameters
```kotlin
@Composable
fun MyComposable(myViewModel: MyViewModel = viewModel()) {
    // ...
    MyDescendant(myViewModel.data)
}

// Don't pass the whole object! Just what the descendant needs.
// Also, don't  pass the ViewModel as an implicit dependency using
// a CompositionLocal.
@Composable
fun MyDescendant(myViewModel: MyViewModel) { /* ... */ }

// Pass only what the descendant needs
@Composable
fun MyDescendant(data: DataToDisplay) {
    // Display data
}CompositionLocalSnippets.kt
```

## Guidelines
- CompositionLocal is a tool for
passing data down through the Composition implicitly. In this page, you'll
learn what a CompositionLocal is in more detail, how to create your own
 CompositionLocal , and know if a CompositionLocal is a good solution for
your use case.
- Key terms: In this guide, we use the terms Composition ,
 UI tree , and UI hierarchy . Although they might be used
interchangeably in other guides, they have different meanings: 

 The Composition is the record of the call graph of composable
functions. 

 The UI tree or UI hierarchy is the tree of
 LayoutNode 
constructed, updated, and maintained by the composition process.
- As an example of this, the LocalContentColor CompositionLocal contains
the preferred content color used for text and
iconography to ensure it contrasts against the current background color. In the
following example, CompositionLocalProvider is used to provide different
values for different parts of the Composition.
- In the last example, the CompositionLocal instances were internally used
by Material composables. To access the current value of a CompositionLocal ,
use its current 
property. In the following example, the current Context value of the
 LocalContext CompositionLocal that is commonly used in Android apps is
used to format the text:
- However, CompositionLocal is not always the best solution. We
discourage overusing CompositionLocal as it comes with some downsides:
- CompositionLocal makes a composable's behavior harder to reason about . As
they create implicit dependencies, callers of composables that use them need
to make sure that a value for every CompositionLocal is satisfied.
- Note: CompositionLocal works well for foundational architecture and Jetpack
Compose makes heavy use of it.
- There are certain conditions that can make CompositionLocal a good solution
for your use case:
- If your use case doesn't meet these requirements, check out the
 Alternatives to consider section before creating a
 CompositionLocal .
- If the value provided to the CompositionLocal is highly unlikely to change or
will never change, use staticCompositionLocalOf to get performance benefits.
- For example, an app's design system might be opinionated in the way composables
are elevated using a shadow for the UI component. Since the different
elevations for the app should propagate throughout the UI tree, we use a
 CompositionLocal . As the CompositionLocal value is derived conditionally
based on the system theme, we use the compositionLocalOf API:
- The CompositionLocalProvider 
composable binds values to CompositionLocal instances for the given
hierarchy . To provide a new value to a CompositionLocal , use the
 provides 
infix function that associates a CompositionLocal key to a value as follows:
- A CompositionLocal might be an excessive solution for some use cases. If your
use case doesn't meet the criteria specified in the Deciding whether to use
CompositionLocal section, another solution might likely be better
suited for your use case.
- Being explicit about composable's dependencies is a good habit. We recommend
that you pass composables only what they need . To encourage decoupling
and reuse of composables, each composable should hold the least amount of
information possible.
- Another way to avoid passing unnecessary dependencies to a composable is
using inversion of control . Instead of the descendant taking in a dependency to
execute some logic, the parent does that instead.
- Depending on the case, MyDescendant might have a lot of responsibility. Also,
passing MyViewModel as a dependency makes MyDescendant less reusable since
they're now coupled together. Consider the alternative that doesn't pass the
dependency into the descendant and uses inversion of control principles that
makes the ancestor responsible for executing the logic:
- This approach can be better suited for some use cases as it decouples the
child from its immediate ancestors . Ancestor composables tend to become more
complex in favor of having more flexible lower-level composables.

## Core Concepts

1. **CompositionLocal for Scoped Data Propagation**
   - Evidence: Multiple code patterns and guidelines mention using CompositionLocal to propagate data scoped within the hierarchy.
   - Explanation: CompositionLocal allows propagating theme, context, or other scoped information down a hierarchical tree without needing to pass these values through every single composable function call. This mechanism ensures that descendant composables can access necessary information implicitly.

2. **Avoiding Implicit Dependencies**
   - Evidence: The guideline explicitly states "Being explicit about composable's dependencies is a good habit."
   - Explanation: Avoiding implicit dependencies means passing only the required parameters to each composable instead of relying on CompositionLocal for data flow. This approach reduces coupling between composables and makes them more reusable.

3. **Using CompositionLocalProvider Correctly**
   - Evidence: Guidelines and code snippets demonstrate how to use `CompositionLocalProvider` correctly.
   - Explanation: To properly leverage CompositionLocal, it’s crucial to use `CompositionLocalProvider` to bind values to local instances within the hierarchy. This ensures that descendant composables can access these values without needing them explicitly passed down.

4. **Choosing Between staticCompositionLocalOf and compositionLocalOf**
   - Evidence: The document mentions scenarios where CompositionLocal should be used, but it does not provide an exhaustive explanation on when to choose between `staticCompositionLocalOf` and `compositionLocalOf`.
   - Explanation: When the value provided to a CompositionLocal is unlikely to change or will never change, using `staticCompositionLocalOf` can improve performance. If values are conditionally set based on other factors (like system theme), then use `compositionLocalOf`.

## Mental Model

- **The Problem**: Developers often face challenges in propagating data or configuration that needs hierarchical scope without explicit parameter passing through every composable.
- **Core Insight**: CompositionLocal facilitates the implicit propagation of values down a hierarchy, making it easier for descendant composables to access theme information, context, and other scoped data directly.
- **How concepts connect**:
  - Avoiding Implicit Dependencies → Minimizes coupling between composables by encouraging explicit parameter passing.
  - Using CompositionLocalProvider Correctly → Ensures that data flow is managed using `CompositionLocalProvider`, making values available where necessary while avoiding overuse of CompositionLocal.

## Guidelines

- **Guideline on CompositionLocal Use Cases**: A detailed explanation should be provided for when and why to use a CompositionLocal, including scenarios like propagating theme information or context across the UI hierarchy.
  
  - Example: If your application's design requires consistent elevation rules based on system themes, then defining a `LocalElevations` CompositionLocal is appropriate because this value needs to propagate throughout the UI tree. Using compositionLocalOf ensures that elevations are conditionally set based on the current theme.

- **Guideline on Avoiding Overuse**: Explicitly explain when and why overusing CompositionLocal can be problematic, such as creating overly complex composables with implicit dependencies.
  
  - Example: If a composable function does not rely heavily on hierarchical data flow or if passing values explicitly results in more maintainable code, then using CompositionLocal might introduce unnecessary complexity.

## Common Mistakes

**Overusing CompositionLocal**
- **Looks like**: 
  ```kotlin
  @Composable fun SomeText() {
      Text(text = "Hello", color = LocalColors.current.red) // Misuse if colors aren't scoped within the hierarchy.
  }
  ```
- **Why it breaks**: Overutilizing CompositionLocal can lead to composables with implicit dependencies that are harder to reason about and maintain. The likelihood of unintended side effects increases as more values are implicitly propagated.

**Incorrect Use of CompositionLocalProvider**
- **Looks like**: 
  ```kotlin
  @Composable fun MyApp() {
      val theme = MaterialTheme()
      // Provide colors without necessary scoping.
  }
  ```
- **Why it breaks**: Incorrectly using `CompositionLocalProvider` can lead to inconsistent or unexpected behavior across composables, as values may not be correctly scoped within the hierarchy.

**Passing Unnecessary Dependencies**
- **Looks like**: 
  ```kotlin
  @Composable fun MyDescendant(myViewModel: MyViewModel) { /* ... */ }
  ```
- **Why it breaks**: Passing entire objects or unnecessary dependencies can lead to composables that are tightly coupled and less reusable. Instead, pass only the required data.

## Decision Framework

| I need to... | Use | NOT | Because |
| --- | --- | --- | --- |
| Propagate theme or context information scoped within hierarchy | CompositionLocal | Explicit parameter passing | Reduces coupling and improves reusability of composables. |

This deepening ensures that the guidelines, common mistakes, and decision framework are more grounded in specific examples from the original document and provide clearer boundaries for when to use CompositionLocal appropriately versus avoiding it.

## Concepts (for graph)
- Introduction to CompositionLocal
- Key terms:
- Composition
- UI tree
- UI hierarchy
- The Composition
- Figure 1.
- Create your own CompositionLocal
- Decide whether to use CompositionLocal
- Create a CompositionLocal
- Provide values to a CompositionLocal
- Consuming the CompositionLocal

<!-- Quality Report
## Quality Report

| Section | Score | Issue (if < 4) |
| --- | --- | --- |
| Core Concepts | 5 | None |
| Mental Model | 5 | None |
| Decision Framework | 4 | Needs to explicitly define how composables should use CompositionLocal based on hierarchy requirements. |
| Common Mistakes | 4 | Add an example showing the correct way of using `CompositionLocalProvider`. |
| Key Relationships | 3 | Missing clear explanation and examples for key terms like "UI tree" and "UI hierarchy". |

## Verdict: NEEDS_FIX

## Fixes (only if NEEDS_FIX)
- Decision Framework: Include explicit guidelines on how composables should use CompositionLocal based on the requirements of hierarchical data flow.
- Common Mistakes: Add an example demonstrating proper usage of `CompositionLocalProvider` with scoping.
-->
