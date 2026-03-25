<!-- Source: https://developer.android.com/develop/ui/compose/kotlin?hl=en -->
<!-- Type: official -->
<!-- Priority: high -->
<!-- Topic: compose-kotlin -->
<!-- Extracted: 2026-03-24 -->
<!-- Verified: — -->

# Kotlin for Jetpack Compose

## Code Patterns
### Default arguments
```
// We don't need to do this in Kotlin!
void drawSquare(int sideLength) { }

void drawSquare(int sideLength, int thickness) { }

void drawSquare(int sideLength, int thickness, Color edgeColor) { }JavaSnippets.java
```

### Default arguments
```kotlin
fun drawSquare(
    sideLength: Int,
    thickness: Int = 2,
    edgeColor: Color = Color.Black
) {
}KotlinSnippets.kt
```

### Default arguments
```
drawSquare(30, 5, Color.Red);JavaSnippets.java
```

### Default arguments
```
drawSquare(sideLength = 30, thickness = 5, edgeColor = Color.Red)KotlinSnippets.kt
```

### Default arguments
```
Text(text = "Hello, Android!")KotlinSnippets.kt
```

### Default arguments
```
Text(
    text = "Hello, Android!",
    color = Color.Unspecified,
    fontSize = TextUnit.Unspecified,
    letterSpacing = TextUnit.Unspecified,
    overflow = TextOverflow.Clip
)KotlinSnippets.kt
```

### Higher-order functions and lambda expressions
```
Button(
    // ...
    onClick = myClickFunction
)
// ...KotlinSnippets.kt
```

### Higher-order functions and lambda expressions
```
Button(
    // ...
    onClick = {
        // do something
        // do something else
    }
) { /* ... */ }KotlinSnippets.kt
```

### Trailing lambdas
```
Column(
    modifier = Modifier.padding(16.dp),
    content = {
        Text("Some text")
        Text("Some more text")
        Text("Last text")
    }
)KotlinSnippets.kt
```

### Trailing lambdas
```
Column(modifier = Modifier.padding(16.dp)) {
    Text("Some text")
    Text("Some more text")
    Text("Last text")
}KotlinSnippets.kt
```

### Trailing lambdas
```
Column {
    Text("Some text")
    Text("Some more text")
    Text("Last text")
}KotlinSnippets.kt
```

### Scopes and receivers
```
Row {
    Text(
        text = "Hello world",
        // This Text is inside a RowScope so it has access to
        // Alignment.CenterVertically but not to
        // Alignment.CenterHorizontally, which would be available
        // in a ColumnScope.
        modifier = Modifier.align(Alignment.CenterVertically)
    )
}KotlinSnippets.kt
```

### Scopes and receivers
```
Box(
    modifier = Modifier.drawBehind {
        // This method accepts a lambda of type DrawScope.() -> Unit
        // therefore in this lambda we can access properties and functions
        // available from DrawScope, such as the `drawRectangle` function.
        drawRect(
            /*...*/
            /* ...
        )
    }
)KotlinSnippets.kt
```

### Delegated properties
```
class DelegatingClass {
    var name: String by nameGetterFunction()

    // ...
}KotlinSnippets.kt
```

### Delegated properties
```kotlin
val myDC = DelegatingClass()
println("The name property is: " + myDC.name)KotlinSnippets.kt
```

### Delegated properties
```
var showDialog by remember { mutableStateOf(false) }

// Updating the var automatically triggers a state change
showDialog = trueKotlinSnippets.kt
```

### Destructuring data classes
```kotlin
data class Person(val name: String, val age: Int)KotlinSnippets.kt
```

### Destructuring data classes
```kotlin
val mary = Person(name = "Mary", age = 35)

// ...

val (name, age) = maryKotlinSnippets.kt
```

### Destructuring data classes
```
Row {

    val (image, title, subtitle) = createRefs()

    // The `createRefs` function returns a data object;
    // the first three components are extracted into the
    // image, title, and subtitle variables.

    // ...
}KotlinSnippets.kt
```

### Type-safe builders and DSLs
```kotlin
@Composable
fun MessageList(messages: List<Message>) {
    LazyColumn {
        // Add a single item as a header
        item {
            Text("Message List")
        }

        // Add list of messages
        items(messages) { message ->
            Message(message)
        }
    }
}KotlinSnippets.kt
```

### Type-safe builders and DSLs
```kotlin
Canvas(Modifier.size(120.dp)) {
    // Draw grey background, drawRect function is provided by the receiver
    drawRect(color = Color.Gray)

    // Inset content by 10 pixels on the left/right sides
    // and 12 by the top/bottom
    inset(10.0f, 12.0f) {
        val quadrantSize = size / 2.0f

        // Draw a rectangle within the inset bounds
        drawRect(
            size = quadrantSize,
            color = Color.Red
        )

        rotate(45.0f) {
            drawRect(size = quadrantSize, color = Color.Blue)
        }
    }
}KotlinSnippets.kt
```

### Kotlin coroutines
```kotlin
// Create a CoroutineScope that follows this composable's lifecycle
val composableScope = rememberCoroutineScope()
Button(
    // ...
    onClick = {
        // Create a new coroutine that scrolls to the top of the list
        // and call the ViewModel to load data
        composableScope.launch {
            scrollState.animateScrollTo(0) // This is a suspend function
            viewModel.loadData()
        }
    }
) { /* ... */ }KotlinSnippets.kt
```

### Kotlin coroutines
```kotlin
@Composable
fun MoveBoxWhereTapped() {
    // Creates an `Animatable` to animate Offset and `remember` it.
    val animatedOffset = remember {
        Animatable(Offset(0f, 0f), Offset.VectorConverter)
    }

    Box(
        // The pointerInput modifier takes a suspend block of code
        Modifier
            .fillMaxSize()
            .pointerInput(Unit) {
                // Create a new CoroutineScope to be able to create new
                // coroutines inside a suspend function
                coroutineScope {
                    while (true) {
                        // Wait for the user to tap on the screen and animate
                        // in the same block
                        awaitPointerEventScope {
                            val offset = awaitFirstDown().position

                            // Launch a new coroutine to asynchronously animate to
                            // where the user tapped on the screen
                            launch {
                                // Animate to the pressed position
                                animatedOffset.animateTo(offset)
                            }
                        }
                    }
                }
            }
    ) {
        Text("Tap anywhere", Modifier.align(Alignment.Center))
        Box(
            Modifier
                .offset {
                    // Use the animated offset as the offset of this Box
                    IntOffset(
                        animatedOffset.value.x.roundToInt(),
                        animatedOffset.value.y.roundToInt()
                    )
                }
                .size(40.dp)
                .background(Color(0xff3c1361), CircleShape)
        )
    }KotlinSnippets.kt
```

## Guidelines
- // We don't need to do this in Kotlin! 
 void drawSquare ( int sideLength ) { } 

 void drawSquare ( int sideLength , int thickness ) { } 

 void drawSquare ( int sideLength , int thickness , Color edgeColor ) { } JavaSnippets . java 

 In Kotlin, you can write a single function and specify the default values for
the arguments:
- Most Compose libraries use default arguments, and it's a good practice to do the
same for the composable functions that you write. This practice makes your
composables customizable, but still makes the default behavior simple to invoke.
So, for example, you might create a simple text element like this:
- Kotlin offers a special syntax for calling higher-order functions whose last 
parameter is a lambda. If you want to pass a lambda expression as that
parameter, you can use trailing lambda
syntax .
Instead of putting the lambda expression within the parentheses, you put it
afterwards. This is a common situation in Compose, so you need to be familiar
with how the code looks.
- Some methods and properties are only available in a certain scope. The limited
scope lets you offer functionality where it's needed and avoid accidentally
using that functionality where it isn't appropriate.
- Consider an example used in Compose. When you call the Row layout
composable, your content lambda is automatically invoked within a RowScope .
This enables Row to expose functionality which is only valid within a Row .
The example below demonstrates how Row has exposed a row-specific value for
the align modifier:
- Kotlin supports delegated
properties .
These properties are called as if they were fields, but their value is
determined dynamically by evaluating an expression. You can recognize these
properties by their use of the by syntax:
- Kotlin makes it easy to declare singletons , classes which always have one and
only one instance. These singletons are declared with the object keyword .
Compose often makes use of such objects. For example,
 MaterialTheme is
defined as a singleton object; the MaterialTheme.colors , shapes , and
 typography properties all contain the values for the current theme.

## Core Concepts

1. **Default Arguments**
   - Evidence: Multiple sections illustrate how default arguments can simplify function calls by specifying default values for parameters, making it easier to call functions without providing all required arguments. For instance:
     ```kotlin
     fun drawSquare(
         sideLength: Int,
         thickness: Int = 2,
         edgeColor: Color = Color.Black
     ) {
     }
     ```

2. **Trailing Lambdas**
   - Evidence: Several examples show using trailing lambdas to enhance readability and flexibility in Compose UI components by moving the lambda outside of the function parentheses:
     ```kotlin
     Column(modifier = Modifier.padding(16.dp)) {
         Text("Some text")
         Text("Some more text")
         Text("Last text")
     }
     ```

3. **Scopes and Receivers**
   - Evidence: The documentation explains that scopes like `RowScope` enable specific functionality only within certain composables, which is crucial for understanding the context-aware nature of Jetpack Compose UI elements:
     ```kotlin
     Row {
         Text(
             text = "Hello world",
             modifier = Modifier.align(Alignment.CenterVertically)
         )
     }
     ```

4. **Delegated Properties**
   - Evidence: Code examples demonstrate using delegated properties with `remember`, a common pattern in Jetpack Compose for managing state:
     ```kotlin
     var showDialog by remember { mutableStateOf(false) }

     // Updating the var automatically triggers a state change
     showDialog = true
     ```

5. **Type-safe Builders and DSLs**
   - Evidence: The documentation provides multiple examples illustrating type-safe builders used extensively in Jetpack Compose, such as the `LazyColumn` example which uses a scope-specific DSL:
     ```kotlin
     @Composable
     fun MessageList(messages: List<Message>) {
         LazyColumn {
             // Add a single item as a header
             item {
                 Text("Message List")
             }

             // Add list of messages
             items(messages) { message ->
                 Message(message)
             }
         }
     }
     ```

## Mental Model

- **The Problem**: Jetpack Compose requires an understanding of functional programming concepts to build efficient and maintainable UI components.
  
- **Core Insight**: In Jetpack Compose, UI is determined by state (`UI = f(state)`), and changes to observable state automatically trigger recomposition of the affected UI elements.

- **How concepts connect**:
   - Default Arguments → Trailing Lambdas: Simplifies function calls, making it easier to pass complex configurations via lambdas.
   - Scopes and Receivers → Delegated Properties: Context-aware functions are enabled by scoped receivers which make properties like `Modifier.align` available only within certain scopes.

## Decision Framework

| I need to... | Use | NOT | Because |
| --- | --- | --- | --- |
| Simplify function calls | Default arguments | Unnecessary parameters | Reduces boilerplate and enhances readability. |
| Enhance readability of composables | Trailing lambdas | Inline lambda definitions | Improves clarity by reducing nesting levels. |

## Common Mistakes

### Incorrect Use of Default Arguments
- **Name**: Unnecessary Overload Creation
- **Looks like**:
  ```kotlin
  fun drawSquare(sideLength: Int, thickness: Int) {}
  fun drawSquare(sideLength: Int, thickness: Int, edgeColor: Color) {}
  ```
  - Why it breaks: This approach results in redundant and hard-to-maintain function overloads.
  
- **Correct**:
  ```kotlin
  fun drawSquare(
      sideLength: Int,
      thickness: Int = 2,
      edgeColor: Color = Color.Black
  )
  ```

### Misusing Scope in Composables
- **Name**: Incorrect Modifier Usage Outside of Scopes
- **Looks like**:
  ```kotlin
  Row {
    Text(modifier = Modifier.align(Alignment.CenterHorizontally)) // Incorrect scope usage
  }
  ```
  
- **Why it breaks**: `Modifier.align` is only valid within a specific scope, and using it outside will result in compilation errors or unexpected behavior.

- **Correct**:
  ```kotlin
  Row {
    Text(
        text = "Hello world",
        modifier = Modifier.align(Alignment.CenterVertically)
    )
  }
  ```

## Key Relationships

- Default Arguments enable Trailing Lambdas to be more readable and concise.
- Scopes provide context for Delegated Properties, making them only accessible within the intended scope.
- Type-safe Builders rely on Context-Aware functions which are enabled by Scope Receivers.

This structured approach ensures mid-level developers understand not just how to use Jetpack Compose features but also why they're crucial and how they interconnect.

## Concepts (for graph)
- Default arguments
- Higher-order functions and lambda expressions
- Trailing lambdas
- Scopes and receivers
- Delegated properties
- Destructuring data classes
- Singleton objects
- Type-safe builders and DSLs
- Kotlin coroutines
- Recommended for you
- function → default (uses)
- libraries → default (uses)

<!-- Quality Report
## Quality Report

| Section | Score | Issue (if < 4) |
| --- | --- | --- |
| Core Concepts | 5 | N/A |
| Mental Model | 4 | Minor clarity improvements possible |
| Decision Framework | 4 | Could be more explicit in benefits of using trailing lambdas over inline definitions |
| Common Mistakes | 4 | Example for "Incorrect Use of Default Arguments" can be more detailed to explain the issue better |
| Key Relationships | 5 | N/A |

## Verdict: NEEDS_FIX

## Fixes (only if NEEDS_FIX)
Mental Model: Enhance clarity by providing a concrete example.
Decision Framework: Emphasize readability and maintainability benefits of trailing lambdas.
Common Mistakes: Provide additional explanation for the "Unnecessary Overload Creation" issue.
-->
