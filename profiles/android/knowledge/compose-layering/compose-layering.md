<!-- Source: https://developer.android.com/develop/ui/compose/layering?hl=en -->
<!-- Type: official -->
<!-- Priority: high -->
<!-- Topic: compose-layering -->
<!-- Extracted: 2026-03-24 -->
<!-- Verified: — -->

# Jetpack Compose architectural layering

## Rules
- DO: Use the appropriate level of abstraction to build your app or library

## Code Patterns
### Control
```kotlin
val color = animateColorAsState(if (condition) Color.Green else Color.Red)ArchitectureLayering.kt
```

### Control
```kotlin
val color = remember { Animatable(Color.Gray) }
LaunchedEffect(condition) {
    color.animateTo(if (condition) Color.Green else Color.Red)
}ArchitectureLayering.kt
```

### Customization
```kotlin
@Composable
fun Button(
    // …
    content: @Composable RowScope.() -> Unit
) {
    Surface(/* … */) {
        CompositionLocalProvider(/* … */) { // set LocalContentAlpha
            ProvideTextStyle(MaterialTheme.typography.button) {
                Row(
                    // …
                    content = content
                )
            }
        }
    }
}ArchitectureLayering.kt
```

### Customization
```kotlin
@Composable
fun GradientButton(
    // …
    background: List<Color>,
    modifier: Modifier = Modifier,
    content: @Composable RowScope.() -> Unit
) {
    Row(
        // …
        modifier = modifier
            .clickable(onClick = {})
            .background(
                Brush.horizontalGradient(background)
            )
    ) {
        CompositionLocalProvider(/* … */) { // set material LocalContentAlpha
            ProvideTextStyle(MaterialTheme.typography.button) {
                content()
            }
        }
    }
}ArchitectureLayering.kt
```

### Customization
```kotlin
@Composable
fun BespokeButton(
    // …
    backgroundColor: Color,
    modifier: Modifier = Modifier,
    content: @Composable RowScope.() -> Unit
) {
    Row(
        // …
        modifier = modifier
            .clickable(onClick = {})
            .background(backgroundColor)
    ) {
        // No Material components used
        content()
    }
}ArchitectureLayering.kt
```

## Pitfalls
- Caution: When dropping down to a lower layer to customize a component, ensure
that you do not degrade any functionality by, for example, neglecting
accessibility support. Use the component you are forking as a guide.
- Caution: Forking a component means that you will not benefit from any future additions or bug fixes from the upstream component.

## Guidelines
- Each layer is built upon the lower levels, combining functionality to create
higher level components. Each layer builds on public APIs of the lower layers
to verify the module boundaries and enable you to replace any layer should you
need to. Let's examine these layers from the bottom up.
- Higher level components tend to do more for you, but limit the amount of direct
control that you have. If you need more control, you can "drop down" to use a
lower level component.
- For example, if you want to animate the color of a component you might use the
 animateColorAsState 
API:
- However, if you needed the component to always start out grey, you cannot
do it with this API. Instead, you can drop down to use the lower level
 Animatable 
API:
- Assembling higher level components from smaller building blocks makes it far
easier to customize components should you need to. For example, consider the
 implementation 
of
 Button 
provided by the Material layer:
- A
 ProvideTextStyle 
sets the default text style to use
- The above implementation continues to use components from the Material layer,
such as Material’s concepts of
 current content alpha 
and the current text style. However, it replaces the material Surface with a
 Row and styles it to achieve the desired appearance.
- If you do not want to use Material concepts at all, for example if building your
own bespoke design system, then you can drop down to purely using foundation
layer components:
- Compose’s philosophy of building layered, reusable components means that you
should not always reach for the lower level building blocks. Many higher level
components not only offer more functionality but often implement best practices
such as supporting accessibility.
- As a rule, prefer building on the highest-level component which offers the
functionality you need in order to benefit from the best practices they
include.

## Core Concepts

1. **Layering in Jetpack Compose**: The document emphasizes the importance of building applications using appropriate levels of abstraction and leveraging layers for customization.
   - Evidence: Section headings, rules, guidelines.

2. **Customization via Lower Layers**: Customizing higher-level components by dropping down to lower layers is a key practice discussed throughout the document, including examples in code patterns and pitfalls sections.
   - Evidence: Code Patterns (Customization), Pitfalls.

3. **Accessibility and Best Practices**: The document mentions that using higher level components often means incorporating accessibility support and best practices automatically.
   - Evidence: Guidelines, Picking the right abstraction.

4. **State Management Across Layers**: Understanding how state management works within different layers versus its use by higher-level components helps users decide when to drop down for customization without losing important features like accessibility or other best practices.
   - Evidence: Code Patterns (Control), Pitfalls.

## Mental Model

- **The Problem**: Solving the issue of how to customize UI elements while maintaining usability and adherence to design principles like Material Design.
- **Core Insight**: Compose’s layering system allows developers to build complex UIs by combining higher-level components that offer more functionality with lower-level components that provide granular control.
- **How concepts connect**:
  - Layering → Customization: By understanding how each layer builds upon the other, you can customize components effectively without losing core features like accessibility.
  - Customization → Accessibility: When customizing at a lower level (e.g., bypassing Material components), ensure that you are still supporting essential functionalities like accessibility.

## Decision Framework

| I need to... | Use | NOT | Because |
| --- | --- | --- | --- |
| Customize component appearance | Lower layer APIs | Higher layer APIs | To achieve exact visual control and styling without limitations of higher-level abstractions. |
| Ensure future updates are applied automatically | Higher level components | Forked/customized lower layers | Future changes or bug fixes won't be incorporated if you fork a component. |

## Common Mistakes

**Name: Neglecting Accessibility**

- **Looks like**: Dropping down to the foundation layer and ignoring Material concepts.
  ```kotlin
  @Composable fun BespokeButton(backgroundColor: Color, content: @Composable RowScope.() -> Unit) {
      // No Material components used
      content()
  }
  ```
  
- **Why it breaks**: By avoiding higher-level abstractions like `ProvideTextStyle` and `CompositionLocalProvider`, you lose built-in accessibility enhancements such as default text styles, content alpha adjustments for better contrast, and other best practices.
  
- **Correct**: Use Material concepts for text styles, content alpha, etc., to ensure your custom components are accessible.
  ```kotlin
  @Composable fun BespokeButton(backgroundColor: Color, content: @Composable RowScope.() -> Unit) {
      CompositionLocalProvider(LocalContentAlpha provides ContentAlpha.medium) {
          ProvideTextStyle(MaterialTheme.typography.button) {
              // Custom button implementation
          }
      }
  }
  ```

## Key Relationships

- **Layering enables customization**: By understanding the layers in Compose, you can customize components effectively without sacrificing functionality.
- **Customization requires care with accessibility**: When customizing components by dropping down to lower layers, it's crucial to ensure that accessibility and other best practices are still supported.

## Concepts (for graph)
- Layers
- Figure 1.
- Design principles
- Control
- Customization
- Picking the right abstraction
- Learn more
- Recommended for you
- often → best (implements)
- might → the (uses)
- can → the (uses)

<!-- Quality Report
## Quality Report

| Section | Score | Issue (if < 4) |
| --- | --- | --- |
| Core Concepts | 5 | N/A |
| Mental Model | 4 | Minor improvements in clarity needed. |
| Decision Framework | 5 | N/A |
| Common Mistakes | 4 | Could be more specific about common mistakes and how to avoid them. |
| Key Relationships | 4 | More examples or concrete connections between concepts would strengthen the explanation. |

## Verdict: NEEDS_FIX

## Fixes (only if NEEDS_FIX)
Mental Model: Clarify core insight and how each concept connects.
Common Mistakes: Provide more specific examples of common mistakes and their fixes.
Key Relationships: Include a clear example that illustrates how customization requires care with accessibility.
-->
