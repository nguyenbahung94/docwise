<!-- Source: https://developer.android.com/develop/ui/compose/side-effects -->
<!-- Type: official -->
<!-- Priority: high -->
<!-- Topic: compose-side-effects -->
<!-- Extracted: 2026-03-24 -->
<!-- Verified: — -->

# Side-effects in Compose

## Rules
- DO: Use snapshotFlow 
to convert State<T> 
objects into a cold Flow. snapshotFlow runs its block when collected and emits
the result of the State objects read in it. When one of the State objects
read inside the snapshotFlow block mutates, the Flow will emit the new value
to its collector if the new val
- DO: Restarting effects less than they should could cause bugs in your app.
- DO: Restarting effects more than they should could be inefficient.

## Code Patterns
### LaunchedEffect : run suspend functions in the scope of a composable
```kotlin
// Allow the pulse rate to be configured, so it can be sped up if the user is running
// out of time
var pulseRateMs by remember { mutableLongStateOf(3000L) }
val alpha = remember { Animatable(1f) }
LaunchedEffect(pulseRateMs) { // Restart the effect when the pulse rate changes
    while (isActive) {
        delay(pulseRateMs) // Pulse the alpha every pulseRateMs to alert the user
        alpha.animateTo(0f)
        alpha.animateTo(1f)
    }
}SideEffectsSnippets.kt
```

### rememberCoroutineScope : obtain a composition-aware scope to launch a coroutine 
```kotlin
@Composable
fun MoviesScreen(snackbarHostState: SnackbarHostState) {

    // Creates a CoroutineScope bound to the MoviesScreen's lifecycle
    val scope = rememberCoroutineScope()

    Scaffold(
        snackbarHost = {
            SnackbarHost(hostState = snackbarHostState)
        }
    ) { contentPadding ->
        Column(Modifier.padding(contentPadding)) {
            Button(
                onClick = {
                    // Create a new coroutine in the event handler to show a snackbar
                    scope.launch {
                        snackbarHostState.showSnackbar("Something happened!")
                    }
                }
            ) {
                Text("Press me")
            }
        }
    }
}SideEffectsSnippets.kt
```

### rememberUpdatedState : reference a value in an effect that shouldn't restart if 
```kotlin
@Composable
fun LandingScreen(onTimeout: () -> Unit) {

    // This will always refer to the latest onTimeout function that
    // LandingScreen was recomposed with
    val currentOnTimeout by rememberUpdatedState(onTimeout)

    // Create an effect that matches the lifecycle of LandingScreen.
    // If LandingScreen recomposes, the delay shouldn't start again.
    LaunchedEffect(true) {
        delay(SplashWaitTimeMillis)
        currentOnTimeout()
    }

    /* Landing screen content */
}SideEffectsSnippets.kt
```

### DisposableEffect : effects that require cleanup
```kotlin
@Composable
fun HomeScreen(
    lifecycleOwner: LifecycleOwner = LocalLifecycleOwner.current,
    onStart: () -> Unit, // Send the 'started' analytics event
    onStop: () -> Unit // Send the 'stopped' analytics event
) {
    // Safely update the current lambdas when a new one is provided
    val currentOnStart by rememberUpdatedState(onStart)
    val currentOnStop by rememberUpdatedState(onStop)

    // If `lifecycleOwner` changes, dispose and reset the effect
    DisposableEffect(lifecycleOwner) {
        // Create an observer that triggers our remembered callbacks
        // for sending analytics events
        val observer = LifecycleEventObserver { _, event ->
            if (event == Lifecycle.Event.ON_START) {
                currentOnStart()
            } else if (event == Lifecycle.Event.ON_STOP) {
                currentOnStop()
            }
        }

        // Add the observer to the lifecycle
        lifecycleOwner.lifecycle.addObserver(observer)

        // When the effect leaves the Composition, remove the observer
        onDispose {
            lifecycleOwner.lifecycle.removeObserver(observer)
        }
    }

    /* Home screen content */
}SideEffectsSnippets.kt
```

### SideEffect : publish Compose state to non-Compose code
```kotlin
@Composable
fun rememberFirebaseAnalytics(user: User): FirebaseAnalytics {
    val analytics: FirebaseAnalytics = remember {
        FirebaseAnalytics()
    }

    // On every successful composition, update FirebaseAnalytics with
    // the userType from the current User, ensuring that future analytics
    // events have this metadata attached
    SideEffect {
        analytics.setUserProperty("userType", user.userType)
    }
    return analytics
}SideEffectsSnippets.kt
```

### produceState : convert non-Compose state into Compose state
```kotlin
@Composable
fun loadNetworkImage(
    url: String,
    imageRepository: ImageRepository = ImageRepository()
): State<Result<Image>> {
    // Creates a State<T> with Result.Loading as initial value
    // If either `url` or `imageRepository` changes, the running producer
    // will cancel and will be re-launched with the new inputs.
    return produceState<Result<Image>>(initialValue = Result.Loading, url, imageRepository) {
        // In a coroutine, can make suspend calls
        val image = imageRepository.load(url)

        // Update State with either an Error or Success result.
        // This will trigger a recomposition where this State is read
        value = if (image == null) {
            Result.Error
        } else {
            Result.Success(image)
        }
    }
}SideEffectsSnippets.kt
```

### [After] Correct usage
```kotlin
@Composable
// When the messages parameter changes, the MessageList
// composable recomposes. derivedStateOf does not
// affect this recomposition.
fun MessageList(messages: List<Message>) {
    Box {
        val listState = rememberLazyListState()

        LazyColumn(state = listState) {
            // ...
        }

        // Show the button if the first visible item is past
        // the first item. We use a remembered derived state to
        // minimize unnecessary compositions
        val showButton by remember {
            derivedStateOf {
                listState.firstVisibleItemIndex > 0
            }
        }

        AnimatedVisibility(visible = showButton) {
            ScrollToTopButton()
        }
    }
}SideEffectsSnippets.kt
```

### Incorrect usage
```kotlin
// DO NOT USE. Incorrect usage of derivedStateOf.
var firstName by remember { mutableStateOf("") }
var lastName by remember { mutableStateOf("") }

val fullNameBad by remember { derivedStateOf { "$firstName $lastName" } } // This is bad!!!
val fullNameCorrect = "$firstName $lastName" // This is correctSideEffectsSnippets.kt
```

### snapshotFlow : convert Compose's State into Flows
```kotlin
val listState = rememberLazyListState()

LazyColumn(state = listState) {
    // ...
}

LaunchedEffect(listState) {
    snapshotFlow { listState.firstVisibleItemIndex }
        .map { index -> index > 0 }
        .distinctUntilChanged()
        .filter { it == true }
        .collect {
            MyAnalyticsService.sendScrolledPastFirstItemEvent()
        }
}SideEffectsSnippets.kt
```

### Restarting effects
```
EffectName(restartIfThisKeyChanges, orThisKey, orThisKey, ...) { block }
```

## Pitfalls
- Warning: LaunchedEffect(true) is as suspicious as a while(true) . Even though
there are valid use cases for it, always pause and make sure that's what you
need.
- Caution: derivedStateOf is expensive, and you should only use it to avoid
unnecessary recomposition when a result hasn't changed.
- Warning: The following snippet shows an incorrect usage of derivedStateOf . Do
not use this code in your project.

## Guidelines
- A side-effect is a change to the state of the app that happens outside the
scope of a composable function.
Due to composables' lifecycle and properties such as unpredictable
recompositions, executing recompositions of composables in different orders, or
recompositions that can be discarded, composables should ideally be side-effect
free .
- However, sometimes side-effects are necessary, for example, to trigger a one-off
event such as showing a snackbar or navigate to another screen given a certain
state condition. These actions should be called from a controlled
environment that is aware of the lifecycle of the composable. In this page,
you'll learn about the different side-effect APIs Jetpack Compose offers.
- As covered in the Thinking in Compose 
documentation, composables should be side-effect free. When you need to make
changes to the state of the app (as described in the Managing
state documentation doc), you should use the Effect
APIs so that those side effects are executed in a predictable manner .
- Due to the different possibilities effects open up in Compose, they can be
easily overused. Make sure that the work you do in them is UI related and
doesn't break unidirectional data flow as explained in the Managing state
documentation .
- Following the previous example, you could use this code to show a Snackbar 
when the user taps on a Button :
- For side effects that need to be cleaned up after the keys change or if the
composable leaves the Composition, use
 DisposableEffect .
If the DisposableEffect keys change, the composable needs to dispose (do
the cleanup for) its current effect, and reset by calling the effect again.
- As an example, you might want to send analytics events based on
 Lifecycle events 
by using a
 LifecycleObserver .
To listen for those events in Compose, use a DisposableEffect to register and
unregister the observer when needed.
- A DisposableEffect must include an onDispose clause as the final statement
in its block of code. Otherwise, the IDE displays a build-time error.
- Note: Having an empty block in onDispose is not a good practice. Always
reconsider to see if there's an effect that fits your use case better.
- To share Compose state with objects not managed by compose, use the
 SideEffect 
composable. Using a SideEffect guarantees that the effect executes after every 
successful recomposition. On the other hand, it is incorrect to
perform an effect before a successful recomposition is guaranteed, which is the
case when writing the effect directly in a composable.
- For example, your analytics library might allow you to segment your user
population by attaching custom metadata ("user properties" in this example)
to all subsequent analytics events. To communicate the user type of the
current user to your analytics library, use SideEffect to update its value.
- produceState 
launches a coroutine scoped to the Composition that can push values into a
returned State . Use it to
convert non-Compose state into Compose state, for example bringing external
subscription-driven state such as Flow , LiveData , or RxJava into the
Composition.
- Even though produceState creates a coroutine, it can also be used to observe
non-suspending sources of data. To remove the subscription to that source, use
the
 awaitDispose 
function.
- The following example shows how to use produceState to load an image from the
network. The loadNetworkImage composable function returns a State that can
be used in other composables.
- Note: Composables with a return type should be named the way you'd name a normal
Kotlin function, starting with a lowercase letter.
- Key Point: Under the hood, produceState makes use of
 other effects! It holds a result variable using
 remember { mutableStateOf(initialValue) } , and triggers the
 producer block in a LaunchedEffect . Whenever
 value is updated in the producer block, the
 result state is updated to the new value. 

 You can easily create your own effects building on top of the existing
 APIs.
- The following snippet shows an appropriate use case for derivedStateOf :
- In this snippet, firstVisibleItemIndex changes any time the first visible item
changes. As you scroll, the value becomes 0 , 1 , 2 , 3 , 4 , 5 , etc.
However, recomposition only needs to occur if the value is greater than 0 .
This mismatch in update frequency means that this is a good use case for
 derivedStateOf .
- A common mistake is to assume that, when you combine two Compose state objects,
you should use derivedStateOf because you are "deriving state". However, this
is purely overhead and not required, as shown in the following snippet:
- // DO NOT USE. Incorrect usage of derivedStateOf. 
 var firstName by remember { mutableStateOf ( "" ) } 
 var lastName by remember { mutableStateOf ( "" ) } 

 val fullNameBad by remember { derivedStateOf { " $ firstName $ lastName " } } // This is bad!!! 
 val fullNameCorrect = " $ firstName $ lastName " // This is correct SideEffectsSnippets.kt

## Core Concepts

1. **LaunchedEffect**  
   - **Explanation**: LaunchedEffect is used to run suspend functions within a composable function’s lifecycle scope. It ensures that these side effects are tied to the lifecycle of the composable, meaning they will be automatically canceled when the composable exits composition.
   - **Failure Mode Without It**: Running suspend functions outside of LaunchedEffect can lead to race conditions and memory leaks because the coroutine would not be aware of the composables' lifecycle events like recomposition or removal from the tree.

2. **DisposableEffect**  
   - **Explanation**: DisposableEffect is used for side effects that require cleanup actions, such as registering a LifecycleObserver. It ensures that when keys change (indicating a new composable instance) or if the composition ends, any resources are properly released.
   - **Failure Mode Without It**: Omitting onDispose in DisposableEffect can result in memory leaks and inconsistent state, as resources will not be cleaned up appropriately after changes to keys.

3. **SideEffect**  
   - **Explanation**: SideEffect is used for publishing Compose state changes outside of the composition scope to update other parts of the application, such as updating Firebase Analytics with user properties.
   - **Failure Mode Without It**: If effects are run directly in a composable without using SideEffect, it might execute prematurely before recomposition is guaranteed, leading to incorrect or inconsistent updates.

4. **produceState**  
   - **Explanation**: produceState converts non-Compose state into Compose state by launching a coroutine that can push values into a returned State object. This allows external data sources such as Flow, LiveData, or RxJava to be integrated seamlessly with the Composition lifecycle.
   - **Failure Mode Without It**: Attempting to integrate these external data sources manually could result in inconsistent state updates and improper lifecycle management.

5. **DerivedStateOf**  
   - **Explanation**: DerivedStateOf is used to derive a new state object from one or more existing State objects, minimizing unnecessary recompositions when the derived value has not changed.
   - **Failure Mode Without It**: Using simple concatenation of mutable states instead of DerivedStateOf can lead to excessive recomposition and performance degradation.

6. **SnapshotFlow**  
   - **Explanation**: SnapshotFlow converts Compose’s State objects into cold Flows, emitting new values when the state changes inside a snapshotFlow block.
   - **Failure Mode Without It**: Manually converting State to Flow without SnapshotFlow can lead to incorrect synchronization of state and flow updates.

## Mental Model
Removed due to being flagged as hallucination in review findings.

## Lifecycle & Timing

```
[Composable recomposition]
  → [SideEffect is called]
  → [State changes, UI updates]

[ListState change event (e.g., scrolling)]
  → [snapshotFlow emits new value]
[cleanup event]
  → [DisposableEffect's onDispose block runs to clean up resources]

[LifecycleOwner lifecycle event (ON_START, ON_STOP)]
  → [LifecycleEventObserver triggers DisposableEffect callback]
```

- **LaunchedEffect**: Triggers: Composition starts; Cancels: Composable exits composition
- **DisposableEffect**: Triggers: Keys change or Composition ends; Cleans up: Resources when keys are updated

## Decision Framework

| I need to... | Use | NOT | Because |
| --- | --- | --- | --- |
| Run a suspend function inside the lifecycle of a composable | LaunchedEffect | rememberCoroutineScope + launch | LaunchedEffect ensures proper lifecycle management and re-execution based on keys. |

## How It Works Internally

- **LaunchedEffect**: `LaunchedEffect` internally uses coroutines to run block within its scope, ensuring that side effects are executed in a controlled environment tied to the composable's lifecycle.

- **produceState**: When using `produceState`, Compose creates a coroutine and observes mutable state updates. The producer function can be invoked when keys change or recomposition happens.

## Common Mistakes

- **Incorrect use of derivedStateOf**
  - **Name**: Using derivedStateOf unnecessarily
  - **Looks like**:
    ```kotlin
    var firstName by remember { mutableStateOf("") }
    var lastName by remember { mutableStateOf("") }

    val fullNameBad by remember { derivedStateOf { "$firstName $lastName" } } // This is bad!!!
    ```
  - **Why it breaks**: Derived state should only be used to minimize unnecessary recompositions when a result hasn't changed, not for combining simple states.
  - **Correct**:
    ```kotlin
    val fullNameCorrect = "$firstName $lastName"
    ```

## Key Relationships

- `LaunchedEffect` enables running suspending functions in the lifecycle of a composable without blocking UI threads.
- `DisposableEffect` requires cleanup actions to be specified, ensuring resources are properly managed when keys change or composition ends.
- `SideEffect` allows publishing Compose state changes outside the Composition scope to update other parts of the application.

## Concepts (for graph)
- State and effect use cases
- Key Term:
- LaunchedEffect : run suspend functions in the scope of a composable
- rememberCoroutineScope : obtain a composition-aware scope to launch a coroutine outside a composable
- rememberUpdatedState : reference a value in an effect that shouldn't restart if the value changes
- DisposableEffect : effects that require cleanup
- SideEffect : publish Compose state to non-Compose code
- produceState : convert non-Compose state into Compose state
- Key Point:
- derivedStateOf : convert one or multiple state objects into another state
- snapshotFlow : convert Compose's State into Flows
- Restarting effects

<!-- Quality Report
## Quality Report

| Section | Score | Issue (if < 4) |
| --- | --- | --- |
| Core Concepts | 5 | - |
| Mental Model | 2 | Hallucination detected, missing real-world examples and explanations. |
| Decision Framework | 5 | - |
| Common Mistakes | 5 | - |
| Key Relationships | 5 | - |

## Verdict: NEEDS_FIX

## Fixes (only if NEEDS_FIX)
Mental Model: Remove or replace with a clear explanation of how side effects tie into the lifecycle of composable functions without introducing speculative details.
-->
