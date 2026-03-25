<!-- Source: https://developer.android.com/develop/ui/compose -->
<!-- Source: https://developer.android.com/develop/ui/compose/adopt -->
<!-- Source: https://developer.android.com/develop/ui/compose/tutorial -->
<!-- Source: https://developer.android.com/develop/ui/compose/documentation -->
<!-- Type: official -->
<!-- Priority: high -->
<!-- Topic: jetpack-compose -->
<!-- Extracted: 2026-03-24 -->
<!-- Verified: — -->

# Jetpack Compose UI App Development Toolkit

## Rules
- DON'T: Performance : Avoid the common programming pitfalls that can degrade
app performance.

## Code Patterns
### Add a text element
```kotlin
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material3.Text

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            Text("Hello world!")
        }
    }
}
```

### Define a composable function
```kotlin
// ...
import androidx.compose.runtime.Composable

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MessageCard("Android")
        }
    }
}

@Composable
fun MessageCard(name: String) {
    Text(text = "Hello $name!")
}
```

### Preview your function in Android Studio
```kotlin
// ...
import androidx.compose.ui.tooling.preview.Preview

@Composable
fun MessageCard(name: String) {
    Text(text = "Hello $name!")
}

@Preview
@Composable
fun PreviewMessageCard() {
    MessageCard("Android")
}
```

### Add multiple texts
```kotlin
// ...

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MessageCard(Message("Android", "Jetpack Compose"))
        }
    }
}

data class Message(val author: String, val body: String)

@Composable
fun MessageCard(msg: Message) {
    Text(text = msg.author)
    Text(text = msg.body)
}

@Preview
@Composable
fun PreviewMessageCard() {
    MessageCard(
        msg = Message("Lexi", "Hey, take a look at Jetpack Compose, it's great!")
    )
}
```

### Using a Column
```kotlin
// ...
import androidx.compose.foundation.layout.Column

@Composable
fun MessageCard(msg: Message) {
    Column {
        Text(text = msg.author)
        Text(text = msg.body)
    }
}
```

### Add an image element
```kotlin
// ...
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Row
import androidx.compose.ui.res.painterResource

@Composable
fun MessageCard(msg: Message) {
    Row {
        Image(
            painter = painterResource(R.drawable.profile_picture),
            contentDescription = "Contact profile picture",
        )
    
       Column {
            Text(text = msg.author)
            Text(text = msg.body)
        }
  
    }
  
}
```

### Configure your layout
```kotlin
// ...
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.unit.dp

@Composable
fun MessageCard(msg: Message) {
    // Add padding around our message
    Row(modifier = Modifier.padding(all = 8.dp)) {
        Image(
            painter = painterResource(R.drawable.profile_picture),
            contentDescription = "Contact profile picture",
            modifier = Modifier
                // Set image size to 40 dp
                .size(40.dp)
                // Clip image to be shaped as a circle
                .clip(CircleShape)
        )

        // Add a horizontal space between the image and the column
        Spacer(modifier = Modifier.width(8.dp))

        Column {
            Text(text = msg.author)
            // Add a vertical space between the author and message texts
            Spacer(modifier = Modifier.height(4.dp))
            Text(text = msg.body)
        }
    }
}
```

### Color
```kotlin
// ...
import androidx.compose.foundation.border
import androidx.compose.material3.MaterialTheme

@Composable
fun MessageCard(msg: Message) {
   Row(modifier = Modifier.padding(all = 8.dp)) {
       Image(
           painter = painterResource(R.drawable.profile_picture),
           contentDescription = null,
           modifier = Modifier
               .size(40.dp)
               .clip(CircleShape)
               .border(1.5.dp, MaterialTheme.colorScheme.primary, CircleShape)
       )

       Spacer(modifier = Modifier.width(8.dp))

       Column {
           Text(
               text = msg.author,
               color = MaterialTheme.colorScheme.secondary
           )

           Spacer(modifier = Modifier.height(4.dp))
           Text(text = msg.body)
       }
   }
}
```

### Typography
```kotlin
// ...

@Composable
fun MessageCard(msg: Message) {
   Row(modifier = Modifier.padding(all = 8.dp)) {
       Image(
           painter = painterResource(R.drawable.profile_picture),
           contentDescription = null,
           modifier = Modifier
               .size(40.dp)
               .clip(CircleShape)
               .border(1.5.dp, MaterialTheme.colorScheme.primary, CircleShape)
       )
       Spacer(modifier = Modifier.width(8.dp))

       Column {
           Text(
               text = msg.author,
               color = MaterialTheme.colorScheme.secondary,
               style = MaterialTheme.typography.titleSmall
           )

           Spacer(modifier = Modifier.height(4.dp))

           Text(
               text = msg.body,
               style = MaterialTheme.typography.bodyMedium
           )
       }
   }
}
```

### Shape
```kotlin
// ...
import androidx.compose.material3.Surface

@Composable
fun MessageCard(msg: Message) {
   Row(modifier = Modifier.padding(all = 8.dp)) {
       Image(
           painter = painterResource(R.drawable.profile_picture),
           contentDescription = null,
           modifier = Modifier
               .size(40.dp)
               .clip(CircleShape)
               .border(1.5.dp, MaterialTheme.colorScheme.primary, CircleShape)
       )
       Spacer(modifier = Modifier.width(8.dp))

       Column {
           Text(
               text = msg.author,
               color = MaterialTheme.colorScheme.secondary,
               style = MaterialTheme.typography.titleSmall
           )

           Spacer(modifier = Modifier.height(4.dp))

           Surface(shape = MaterialTheme.shapes.medium, shadowElevation = 1.dp) {
               Text(
                   text = msg.body,
                   modifier = Modifier.padding(all = 4.dp),
                   style = MaterialTheme.typography.bodyMedium
               )
           }
       }
   }
}
```

### Enable dark theme
```kotlin
// ...
import android.content.res.Configuration

@Preview(name = "Light Mode")
@Preview(
    uiMode = Configuration.UI_MODE_NIGHT_YES,
    showBackground = true,
    name = "Dark Mode"
)
@Composable
fun PreviewMessageCard() {
   ComposeTutorialTheme {
    Surface {
      MessageCard(
        msg = Message("Lexi", "Hey, take a look at Jetpack Compose, it's great!")
      )
    }
   }
}
```

### Create a list of messages
```kotlin
// ...
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items

@Composable
fun Conversation(messages: List<Message>) {
    LazyColumn {
        items(messages) { message ->
            MessageCard(message)
        }
    }
}

@Preview
@Composable
fun PreviewConversation() {
    ComposeTutorialTheme {
        Conversation(SampleData.conversationSample)
    }
}
```

### Animate messages while expanding
```kotlin
// ...
import androidx.compose.foundation.clickable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue

class MainActivity : ComponentActivity() {
   override fun onCreate(savedInstanceState: Bundle?) {
       super.onCreate(savedInstanceState)
       setContent {
           ComposeTutorialTheme {
               Conversation(SampleData.conversationSample)
           }
       }
   }
}

@Composable
fun MessageCard(msg: Message) {
    Row(modifier = Modifier.padding(all = 8.dp)) {
        Image(
            painter = painterResource(R.drawable.profile_picture),
            contentDescription = null,
            modifier = Modifier
                .size(40.dp)
                .clip(CircleShape)
                .border(1.5.dp, MaterialTheme.colorScheme.primary, CircleShape)
        )
        Spacer(modifier = Modifier.width(8.dp))

        // We keep track if the message is expanded or not in this
        // variable
        var isExpanded by remember { mutableStateOf(false) }

        // We toggle the isExpanded variable when we click on this Column
        Column(modifier = Modifier.clickable { isExpanded = !isExpanded }) {
            Text(
                text = msg.author,
                color = MaterialTheme.colorScheme.secondary,
                style = MaterialTheme.typography.titleSmall
            )

            Spacer(modifier = Modifier.height(4.dp))

            Surface(
                shape = MaterialTheme.shapes.medium,
                shadowElevation = 1.dp,
            ) {
                Text(
                    text = msg.body,
                    modifier = Modifier.padding(all = 4.dp),
                    // If the message is expanded, we display all its content
                    // otherwise we only display the first line
                    maxLines = if (isExpanded) Int.MAX_VALUE else 1,
                    style = MaterialTheme.typography.bodyMedium
                )
            }
        }
    }
}
```

### Animate messages while expanding
```kotlin
// ...
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.animateContentSize

@Composable
fun MessageCard(msg: Message) {
    Row(modifier = Modifier.padding(all = 8.dp)) {
        Image(
            painter = painterResource(R.drawable.profile_picture),
            contentDescription = null,
            modifier = Modifier
                .size(40.dp)
                .clip(CircleShape)
                .border(1.5.dp, MaterialTheme.colorScheme.secondary, CircleShape)
        )
        Spacer(modifier = Modifier.width(8.dp))

        // We keep track if the message is expanded or not in this
        // variable
        var isExpanded by remember { mutableStateOf(false) }
        // surfaceColor will be updated gradually from one color to the other
        val surfaceColor by animateColorAsState(
            if (isExpanded) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surface,
        )

        // We toggle the isExpanded variable when we click on this Column
        Column(modifier = Modifier.clickable { isExpanded = !isExpanded }) {
            Text(
                text = msg.author,
                color = MaterialTheme.colorScheme.secondary,
                style = MaterialTheme.typography.titleSmall
            )

            Spacer(modifier = Modifier.height(4.dp))

            Surface(
                shape = MaterialTheme.shapes.medium,
                shadowElevation = 1.dp,
                // surfaceColor color will be changing gradually from primary to surface
                color = surfaceColor,
                // animateContentSize will change the Surface size gradually
                modifier = Modifier.animateContentSize().padding(1.dp)
            ) {
                Text(
                    text = msg.body,
                    modifier = Modifier.padding(all = 4.dp),
                    // If the message is expanded, we display all its content
                    // otherwise we only display the first line
                    maxLines = if (isExpanded) Int.MAX_VALUE else 1,
                    style = MaterialTheme.typography.bodyMedium
                )
            }
        }
    }
}
```

## Guidelines
- Jetpack Compose is built around composable functions. These functions let you define your
 app's UI programmatically by describing how it should look and providing data dependencies,
 rather than focusing on the process of the UI's construction (initializing an element,
 attaching it to a parent, etc.). To create a composable function, just add the
 @Composable annotation to the function name.
- Start by making the message composable richer by displaying the name of its author and a
 message content. You need to first change the composable parameter to accept a
 Message object instead of a
 String , and add another
 Text composable inside the
 MessageCard composable. Make sure to update the preview
 as well.
- The 
 Column function lets you arrange elements vertically.
 Add Column to the
 MessageCard function. 
 You can use 
 Row to arrange items horizontally and
 
 Box to stack elements.
- A chat with one message feels a bit lonely, so we are going to change the conversation to have more than
 one message. You'll need to create a Conversation function
 that will show multiple messages. For this use case, use Compose’s
 
 LazyColumn and
 
 LazyRow . These composables render only the elements
 that are visible on screen, so they are designed to be very efficient for long lists.
- Note: You need to add the following imports to correctly use Kotlin's
 delegated property syntax (the by keyword). Alt+Enter or Option+Enter adds them
 for you. 
 
 import androidx.compose.runtime.getValue
 import androidx.compose.runtime.setValue
- Modifiers : Use modifiers to augment or decorate your composables.
- Jetpack Compose Phases : The steps Compose goes through to render your
app's UI, and how to use that information to write efficient code.
- Locally scoped data with CompositionLocal : Use CompositionLocal to
pass data through the composition.
- Apply proven layouts : Use canonical layouts like list-detail and
supporting pane for optimized apps on large screens.
- Android Studio with Compose : How to et up your development environment
to use Compose.
- ConstraintLayout : Use ConstraintLayout in your Compose UI.
- Compose and other libraries : How to use view-based libraries in your
Compose content.
- Navigation : Use NavController to integrate the Navigation
component with your Compose UI.

## Core Concepts

1. **UI as a Function of State**:
   - Evidence: Sections like "Add an image element", "Animate messages while expanding" demonstrate how changes in state (like text content, image visibility) lead to immediate UI updates.
   - Explanation: This concept means that the UI is automatically updated whenever there's a change in the underlying data state. For example, when a message is expanded or collapsed, the corresponding composable function `MessageCard` recomposes and reflects these changes in its layout.

2. **Composable Functions**:
   - Evidence: Sections such as "Define a composable function", "Preview your function in Android Studio" highlight the importance of defining UI elements with `@Composable` functions.
   - Explanation: Composable functions encapsulate the logic for rendering specific parts of the UI. For instance, the `MessageCard` composable takes a message object and renders it as text alongside an author name.

3. **Observable State (mutableStateOf)**:
   - Evidence: Sections on "Animate messages while expanding" illustrate how mutable state is used to trigger recomposition.
   - Explanation: Observable state enables reactive UI updates by automatically triggering recompositions whenever the state changes. This mechanism ensures that any interaction or data change immediately reflects in the UI without manual intervention.

## Mental Model

- **The Problem**: Without observable state and composable functions, updating the UI in response to data changes can become cumbersome and error-prone.
- **Core Insight**: UI is a function of state (`UI = f(state)`), where any change in state triggers automatic updates to the UI components defined as composables.
- **How concepts connect**:
  - Composable Functions → Observable State: Composable functions are essential for defining UI elements. To make these elements dynamic, observable state (e.g., `mutableStateOf`) is necessary.
  - Observable State → Recomposition: Changes in observable state cause the composable tree to be recomposed and updated accordingly.

## Decision Framework
| I need to... | Use | NOT | Because |
| --- | --- | --- | --- |
| Define a UI component | `@Composable` functions | Regular methods | Composables are designed for defining UI elements in Jetpack Compose, ensuring they are automatically managed by the framework. |

## Common Mistakes
- **Name**: Incorrect State Management
  - **Looks like**:
    ```kotlin
    var message by remember { mutableStateOf("") }
    
    // This line should not be here as it is redundant.
    val uiMessage = if (message.isNotEmpty()) "Hello $message" else ""
    ```
  - **Why it breaks**: The `uiMessage` variable is recalculated on every recomposition, leading to unnecessary computations and potential performance issues. 
  - **Correct**:
    ```kotlin
    var message by remember { mutableStateOf("") }
    
    // Directly use the state in UI components.
    Text(text = if (message.isNotEmpty()) "Hello $message" else "")
    ```

## Key Relationships
- Composable Functions require Observable State to enable dynamic UI updates.
- Event → State → UI: User interactions or data changes trigger observable state updates, which cause the composable functions to recompose and update the UI accordingly.

By focusing on these core concepts and understanding their interconnections, developers can effectively leverage Jetpack Compose for building efficient and responsive user interfaces.

## Concepts (for graph)
- Build better apps faster with Jetpack Compose
- Less code
- Intuitive
- Accelerate development
- Powerful
- New to Android Development?
- Want to learn Compose?
- Material You is available for Compose
- Now in Android App Sample
- Quick Tutorial
- Videos
- Sample apps

<!-- Quality Report
## Quality Report

| Section | Score | Issue (if < 4) |
| --- | --- | --- |
| Core Concepts | 5 | N/A |
| Mental Model | 5 | N/A |
| Decision Framework | 4 | Missing a few examples or explanations for "NOT" column. |
| Common Mistakes | 4 | The provided example could be more clear and concise to avoid confusion. |
| Key Relationships | 5 | N/A |

## Verdict: NEEDS_FIX

## Fixes (only if NEEDS_FIX)
- Decision Framework: Add a brief explanation or an additional example for when NOT to use `@Composable` functions.
- Common Mistakes: Clarify and simplify the incorrect state management example with comments explaining why it's wrong.
-->
