<!-- Source: https://developer.android.com/develop/ui/compose/architecture?hl=en -->
<!-- Type: official -->
<!-- Priority: high -->
<!-- Topic: compose-architecture -->
<!-- Extracted: 2026-03-24 -->
<!-- Verified: — -->

# Compose UI Architecture

## Rules
- DO: Prefer passing immutable values for state and event handler lambdas. This
approach has the following benefits:
- DON'T: You avoid concurrency issues because you make sure that the state isn't
mutated from another thread.

### Deepened
- DO: Prefer passing immutable values for state and event handler lambdas. This approach has the following benefits:
  - Avoids concurrency issues because you make sure that the state isn't mutated from another thread.
  - Ensures UI consistency by triggering recomposition whenever state changes, which updates the UI to reflect the latest data.

## Code Patterns
### Compose UI Architecture 

 
 
 
 

 
 
 Stay organized with collections
 
 
 
 S
```
var name by remember { mutableStateOf("") }
OutlinedTextField(
    value = name,
    onValueChange = { name = it },
    label = { Text("Name") }
)ArchitectureSnippets.kt
```

### Define composable parameters
```kotlin
@Composable
fun Header(title: String, subtitle: String) {
    // Recomposes when title or subtitle have changed.
}

@Composable
fun Header(news: News) {
    // Recomposes when a new instance of News is passed in.
}ArchitectureSnippets.kt
```

### Events in Compose
```kotlin
@Composable
fun MyAppTopAppBar(topAppBarText: String, onBackPressed: () -> Unit) {
    TopAppBar(
        title = {
            Text(
                text = topAppBarText,
                textAlign = TextAlign.Center,
                modifier = Modifier
                    .fillMaxSize()
                    .wrapContentSize(Alignment.Center)
            )
        },
        navigationIcon = {
            IconButton(onClick = onBackPressed) {
                Icon(
                    Icons.AutoMirrored.Filled.ArrowBack,
                    contentDescription = localizedString
                )
            }
        },
        // ...
    )
}ArchitectureSnippets.kt
```

### ViewModels, states, and events: an example
```kotlin
class MyViewModel : ViewModel() {
    private val _uiState = mutableStateOf<UiState>(UiState.SignedOut)
    val uiState: State<UiState>
        get() = _uiState

    // ...
}ArchitectureSnippets.kt
```

## Guidelines
- UI consistency : All state updates are immediately reflected in the UI by
the use of observable state holders, like StateFlow or LiveData .
- The type of the TextField composable's value is String , so this can come
from anywhere—from a hardcoded value, from a ViewModel, or passed in from the
parent composable. You don't have to hold it in a State object, but you need
to update the value when onValueChange is called.
- To promote decoupling and reuse, each composable should hold the least amount of
information possible. For example, when building a composable to hold the
header of a news article, prefer passing in only the information that needs to
be displayed, rather than the entire news article:
- Consider carefully the number of parameters you pass in. Having a function with
too many parameters decreases the ergonomics of the function, so in this case
grouping them up in a class is preferred.
- Every input to your app should be represented as an event: taps, text changes,
and even timers or other updates. As these events change the state of your UI,
the ViewModel should handle them and update the UI state.
- The UI layer should never change state outside of an event handler because this
can introduce inconsistencies and bugs in your application.
- For example, a composable that accepts a String and a lambda as parameters can
be called from many contexts and is highly reusable. Suppose that the top app
bar in your app always displays text and has a
back button. You can define a more generic MyAppTopAppBar composable
that receives the text and the back button handle as parameters:
- For example, when implementing a sign-in screen, tapping on a Sign in button
should cause your app to display a progress spinner and a network call. If the
login was successful, then your app navigates to a different screen; in case of
an error the app shows a Snackbar. Here's how you would model the screen state
and the event:

### Deepened
- **UI consistency**: All state updates are immediately reflected in the UI through observable state holders like `StateFlow` or `LiveData`. This ensures that any change in state triggers a re-render of the relevant components.
  - **Enter Composition** → [Composable function starts]
  - **Recomposition** → [Re-render triggered by changes in State objects or other composable inputs]
  - **Key changes** → [Old composable instances are cleaned up; new ones are recomposed as needed based on state updates]
  - **Leave Composition** → [All resources and side effects are cleaned up; composables no longer retain their state]

## Mental Model

**The Problem**: Jetpack Compose solves the problem of efficiently and declaratively building UIs in Android, ensuring that state management and re-rendering are handled automatically. This allows developers to focus on defining how the UI should look based on its current state rather than manually managing view lifecycle and state updates.

**Core Insight**: The key insight is understanding that Compose uses a unidirectional data flow architecture where events (user actions) update the application's internal state, which in turn triggers re-renders of relevant components to reflect changes in UI.

**Classification**:
- **State Management APIs**: These handle the lifecycle and updates of immutable states (`mutableStateOf`, `StateFlow`).
- **Composable APIs**: Used for defining reusable UI components that take parameters and return a layout description (`@Composable` functions).

**Architecture Context**: Compose integrates seamlessly with ViewModel to manage application state in a way that is observable but read-only from the UI layer. This architecture promotes separation of concerns, where ViewModels handle complex logic and state management, while composables handle rendering.

## Lifecycle & Timing

```
Enter Composition
  → [Composable function starts]
Recomposition
  → [Re-render triggered by changes in State objects or other composable inputs]
Key changes
  → [Old composable instances are cleaned up; new ones are recomposed as needed based on state updates]
Leave Composition
  → [All resources and side effects are cleaned up; composables no longer retain their state]
```

**API Triggers, Cancellations, Restarts:**
- `mutableStateOf` — triggers: state change, cancels: nothing specific, restarts when: recomposition occurs due to state or input changes.
- `@Composable` — triggers: call in the UI rendering path, cancels: none directly, restarts when: re-rendering happens upon state changes.

## Decision Framework

| I need to... | Use | NOT | Because |
| --- | --- | --- | --- |
| Update UI based on user input | `mutableStateOf` | Direct mutation of variables | Direct mutations can cause concurrency issues and make code harder to reason about. |
| Handle navigation between screens | `NavController.navigate` with Compose Navigation library | Manual state management in ViewModel | The navigation library handles the stack and back navigation automatically, making it easier to manage UI states consistently. |
| Pass data from parent composable to child | Propagation via parameters or context providers like LocalXXX | Passing through a ViewModel | Using ViewModels can introduce unnecessary complexity for simple data flows between composables. |

### Deepened
| I need to... | Use | NOT | Because |
| --- | --- | --- | --- |
| Update UI based on user input | `mutableStateOf` | Direct mutation of variables | Direct mutations can cause concurrency issues and make code harder to reason about. For instance, direct mutations may not trigger recomposition, leading to stale or inconsistent UI states. |

## Internal Composition

- **X = Y + Z**: Compose's `@Composable` functions are fundamentally built upon Kotlin coroutines and suspending functions, where the state management (Y) ensures that UI changes trigger re-composition (Z).
- This means that any change to a State object within a composable will automatically trigger recomposition of that composable or its descendants.

## Cost & Performance

- **StateFlow**: Allocates resources for maintaining internal states and tracking updates. Becomes expensive when dealing with high-frequency state changes.
  - To minimize cost, limit the use of `StateFlow` to only those cases where asynchronous data streams are necessary, and avoid unnecessary recompositions by optimizing state objects.

### Deepened
- **StateFlow**: Allocates resources for maintaining internal state tracking and emits updates when the source value changes. This becomes expensive in scenarios with high-frequency state modifications as it necessitates frequent recompositions.
  - To minimize cost:
    - Limit `StateFlow` usage to asynchronous data streams where necessary, and optimize state objects to avoid unnecessary recompositions.

## Anti-Patterns

- **Name**: Direct Mutation in Composable
  - **Looks like**:
    ```kotlin
    var name = ""
    OutlinedTextField(
        value = name,
        onValueChange = { name = it }
    )
    ```
  - **Why it breaks**: This approach bypasses recomposition, leading to UI inconsistencies and harder-to-debug state issues.
  - **Fix**:
    ```kotlin
    var name by remember { mutableStateOf("") }
    OutlinedTextField(
        value = name,
        onValueChange = { name = it }
    )
    ```

- **Name**: Overuse of Navigation via ViewModel
  - **Looks like**:
    ```kotlin
    class MyViewModel : ViewModel() {
        fun navigateToNextScreen() {
            viewModelScope.launch { navController.navigate("next_screen") }
        }
    }
    ```
  - **Why it breaks**: This couples UI and navigation logic unnecessarily, complicating state management.
  - **Fix**:
    ```kotlin
    @Composable
    fun MyAppTopAppBar(navController: NavHostController) {
        TopAppBar(
            // Navigation handled directly in Compose with navController
        )
    }
    ```

### Deepened
- **Name**: Direct Mutation in Composable
  - **Looks like**:
    ```kotlin
    var name = ""
    OutlinedTextField(
        value = name,
        onValueChange = { name = it }
    )
    ```
  - **Why it breaks**: This approach bypasses recomposition, leading to UI inconsistencies and harder-to-debug state issues.
  - **Fix**:
    ```kotlin
    var name by remember { mutableStateOf("") }
    OutlinedTextField(
        value = name,
        onValueChange = { name = it }
    )
    ```

- **Name**: Overuse of Navigation via ViewModel
  - **Looks like**:
    ```kotlin
    class MyViewModel : ViewModel() {
        fun navigateToNextScreen() {
            viewModelScope.launch { navController.navigate("next_screen") }
        }
    }
    ```
  - **Why it breaks**: This couples UI and navigation logic unnecessarily, complicating state management. Navigation should ideally be handled within the `@Composable` functions or through dedicated navigation components.
  - **Fix**:
    ```kotlin
    @Composable
    fun MyAppTopAppBar(navController: NavHostController) {
        TopAppBar(
            // Navigation handled directly in Compose with navController
        )
    }
    ```

## Key Relationships

- **Equivalences**: `mutableStateOf` + `@Composable` = Automatic UI re-rendering based on state changes.
- **Dependencies**: Use of `NavController.navigate()` requires a valid NavHost to be present in the Compose hierarchy.
- **Ordering**: Navigation actions (`NavHostController.navigate()`) must happen after the navigation graph is set up via `NavHost`.
- **Conflicts**: Avoid using direct lifecycle management with `ViewModel` and Compose side effects as this can lead to state inconsistencies.

## Internal mechanics
- **X = Y + Z**: Compose's `@Composable` functions are built upon Kotlin coroutines and suspending functions, ensuring that any change to a State object within a composable automatically triggers recomposition.
  - **Why it matters**:
    - This mechanism ensures that UI components remain up-to-date with the current state of your application.

## Architecture integration
- **ViewModel Integration**: Jetpack Compose integrates seamlessly with ViewModel to manage application state. ViewModels handle complex logic and state management, while composables focus on rendering the UI.
  - **Example**:
    ```kotlin
    class MyViewModel : ViewModel() {
        private val _uiState = mutableStateOf<UiState>(UiState.SignedOut)
        val uiState: State<UiState>
            get() = _uiState

        // Update state based on events, e.g., user actions or network responses.
    }
    ```

- **Navigation**: Compose Navigation library is used to handle navigation between screens. This promotes a clean separation of concerns and simplifies the management of UI states across different screens.
  - **Example**:
    ```kotlin
    @Composable
    fun MyAppTopAppBar(navController: NavHostController) {
        TopAppBar(
            title = { Text("Title") },
            navigationIcon = {
                IconButton(onClick = { navController.popBackStack() }) {
                    Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                }
            },
        )
    }
    ```

- **Dependency Injection (Hilt)**: Jetpack Compose can be integrated with Hilt for dependency injection. This allows you to inject dependencies directly into your ViewModel or composable functions.
  - **Example**:
    ```kotlin
    @Composable
    fun MyScreen(
        myViewModel: MyViewModel = viewModel()
    ) {
        // Use myViewModel here
    }
    ```

- **Testing**: Jetpack Compose offers a testing library that allows you to write tests for your composable functions. This promotes testability and ensures that your UI components behave as expected.
  - **Example**:
    ```kotlin
    @Test
    fun myScreen_Render_Correctly() {
        // Arrange
        val context = ApplicationProvider.getApplicationContext<Context>()
        val myViewModel: MyViewModel = mock()

        // Act
        setContent {
            MyScreen(myViewModel)
        }

        // Assert
        // Assertions here to verify the UI renders correctly.
    }
    ```

## Concepts (for graph)
- Unidirectional data flow
- Event
- Update state
- Display state
- Figure 1.
- Testability
- State encapsulation
- UI consistency
- Unidirectional data flow in Jetpack Compose
- Key Point:
- Define composable parameters
- Events in Compose
