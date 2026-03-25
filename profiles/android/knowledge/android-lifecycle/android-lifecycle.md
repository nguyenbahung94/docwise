<!-- Source: https://developer.android.com/topic/libraries/architecture/lifecycle -->
<!-- Type: official -->
<!-- Priority: high -->
<!-- Topic: android-lifecycle -->
<!-- Extracted: 2026-03-24 -->
<!-- Verified: — -->

# Handling lifecycles with lifecycle-aware components

## Rules
- DO: Keep your UI controllers (activities and fragments) as lean as possible. They
should not try to acquire their own data; instead, use a
 ViewModel to do that,
and observe a LiveData 
object to reflect the changes back to the views.
- DON'T: Put your data logic in your
 ViewModel class.
 ViewModel should serve
as the connector between your UI controller and the rest of your app. Be
careful though, it isn't
 ViewModel 's
responsibility to fetch data (for example, from a network). Instead,
 ViewModel should call
the appropriate component
- DO: Use Data Binding to maintain a
clean interface between your views and the UI controller. This allows you to
make your views more declarative and minimize the update code you need to
write in your activities and fragments. If you prefer to do this in the Java
programming language, use a library like
- DON'T: Avoid referencing a View or Activity 
context in your ViewModel .
If the ViewModel outlives the activity (in case of configuration changes),
your activity leaks and isn't properly disposed by the garbage collector.
- DO: Use Kotlin coroutines to manage
long-running tasks and other operations that can run asynchronously.
- DO: Use Kotlin coroutines with lifecycle-aware components

## Code Patterns
### Handling lifecycles with lifecycle-aware components 

   Part of Android Jetpack
```kotlin
internal class MyLocationListener(
        private val context: Context,
        private val callback: (Location) -> Unit
) {

    fun start() {
        // connect to system location service
    }

    fun stop() {
        // disconnect from system location service
    }
}

class MyActivity : AppCompatActivity() {
    private lateinit var myLocationListener: MyLocationListener

    override fun onCreate(...) {
        myLocationListener = MyLocationListener(this) { location ->
            // update UI
        }
    }

    public override fun onStart() {
        super.onStart()
        myLocationListener.start()
        // manage other components that need to respond
        // to the activity lifecycle
    }

    public override fun onStop() {
        super.onStop()
        myLocationListener.stop()
        // manage other components that need to respond
        // to the activity lifecycle
    }
}
```

### Handling lifecycles with lifecycle-aware components 

   Part of Android Jetpack
```kotlin
class MyActivity : AppCompatActivity() {
    private lateinit var myLocationListener: MyLocationListener

    override fun onCreate(...) {
        myLocationListener = MyLocationListener(this) { location ->
            // update UI
        }
    }

    public override fun onStart() {
        super.onStart()
        Util.checkUserStatus { result ->
            // what if this callback is invoked AFTER activity is stopped?
            if (result) {
                myLocationListener.start()
            }
        }
    }

    public override fun onStop() {
        super.onStop()
        myLocationListener.stop()
    }

}
```

### Lifecycle
```kotlin
class MyObserver : DefaultLifecycleObserver {
    override fun onResume(owner: LifecycleOwner) {
        connect()
    }

    override fun onPause(owner: LifecycleOwner) {
        disconnect()
    }
}

myLifecycleOwner.getLifecycle().addObserver(MyObserver())
```

### Implementing a custom LifecycleOwner
```kotlin
class MyActivity : Activity(), LifecycleOwner {

    private lateinit var lifecycleRegistry: LifecycleRegistry

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        lifecycleRegistry = LifecycleRegistry(this)
        lifecycleRegistry.markState(Lifecycle.State.CREATED)
    }

    public override fun onStart() {
        super.onStart()
        lifecycleRegistry.markState(Lifecycle.State.STARTED)
    }

    override fun getLifecycle(): Lifecycle {
        return lifecycleRegistry
    }
}
```

## Guidelines
- Most of the app components that are defined in the Android Framework have
lifecycles attached to them. Lifecycles are managed by the operating system or
the framework code running in your process. They are core to how Android works
and your application must respect them. Not doing so may trigger memory leaks or
even application crashes.
- LifecycleOwner is a
single method interface that denotes that the class has a
 Lifecycle . It has one
method,
 getLifecycle() ,
which must be implemented by the class.
If you're trying to manage the lifecycle of a whole application
process instead, see
 ProcessLifecycleOwner .
- To make this use case easy, the
 Lifecycle class allows
other objects to query the current state.
- If a library provides classes that need to work with the Android lifecycle, we
recommend that you use lifecycle-aware components. Your library clients can
easily integrate those components without manual lifecycle management on the
client side.
- If you have a custom class that you would like to make a
 LifecycleOwner , you
can use the
 LifecycleRegistry 
class, but you need to forward events into that class, as shown in the following
code example:
- If your UI is complex, consider creating a
 presenter 
class to handle UI modifications. This might be a laborious task, but it can
make your UI components easier to test.
- Switching between coarse and fine-grained location updates. Use
lifecycle-aware components to enable fine-grained location updates while your
location app is visible and switch to coarse-grained updates when the app is
in the background. LiveData , a lifecycle-aware component,
allows your app to automatically update the UI when your user changes
locations.
- Stopping and starting video buffering. Use lifecycle-aware components to start
video buffering as soon as possible, but defer playback until app is fully
started. You can also use lifecycle-aware components to terminate buffering
when your app is destroyed.
- Starting and stopping network connectivity. Use lifecycle-aware components to
enable live updating (streaming) of network data while an app is in the
foreground and also to automatically pause when the app goes into the
background.
- Pausing and resuming animated drawables. Use lifecycle-aware components to
handle pausing animated drawables when the app is in the background and
resume drawables after the app is in the foreground.

## Core Concepts

1. **Lifecycle-aware Components**:
   - Evidence: Multiple sections and code patterns emphasize the use of lifecycle-aware components like LiveData, ViewModel, and LifecycleRegistry.
   - Explanation: Utilizing lifecycle-aware components ensures that data management and UI updates are handled efficiently by respecting the Android framework's lifecycle states. For example, LiveData objects automatically update views when data changes, ensuring that the UI stays in sync with the model without manual intervention from activities or fragments.

2. **ViewModel as a Data Holder**:
   - Evidence: Rules explicitly mention using ViewModel to manage data logic outside UI controllers (activities and fragments).
   - Explanation: A ViewModel acts as an intermediary between UI components and data sources, ensuring that UI controllers remain lean by offloading tasks such as fetching data or handling business logic. This separation ensures that activities or fragments do not need to be aware of complex operations like network requests or database interactions.

3. **Data Binding for Declarative Views**:
   - Evidence: Guidelines recommend using Data Binding to maintain a clean interface between views and the UI controller.
   - Explanation: Data Binding allows developers to bind view elements directly to data sources via XML layouts, thereby reducing boilerplate code needed in activities or fragments to update UI elements. This approach enhances readability and maintainability of the UI layer.

4. **Lifecycle States vs Lifecycle Events**:
   - Evidence: The document mentions lifecycle management but does not provide clear distinctions between lifecycle states (CREATED, STARTED) and lifecycle events (onStart, onStop).
   - Explanation: Understanding the difference is crucial for efficient resource management within activities or fragments. Lifecycle states represent the current phase of an activity's life cycle (e.g., created, started), while lifecycle events are methods that trigger actions when state changes occur (e.g., onStart() triggers when the activity becomes visible).

## Mental Model

- **The Problem**: The primary problem addressed is managing activity lifecycles effectively without causing memory leaks or application crashes.
- **Core Insight**: Utilizing lifecycle-aware components ensures that data management and UI updates are handled efficiently, respecting the Android framework's lifecycle states. For instance, LiveData objects automatically update views when data changes, reducing manual intervention from activities or fragments.
- **How concepts connect**:
  - Lifecycle → ViewModel: A lifecycle state change triggers updates in ViewModel through lifecycle-aware mechanisms.
  - ViewModel → Data Binding: ViewModel interacts with Data Binding to declaratively update UI elements based on model changes.

## Lifecycle & Timing

[Activity starts]
  → LifecycleOwner gets initialized
  → Lifecycle events are observed and handled accordingly
[Activity stops or destroys]
  → Lifecycle events notify the ViewModel to stop operations
  → UI updates cease as per LiveData observations

LifecycleRegistry — triggers: onCreate/onStart, cancels: onStop/onDestroy, restarts when: configuration changes.

## Decision Framework

| I need to... | Use | NOT | Because |
| --- | --- | --- | --- |
| Handle data retrieval and persistence | ViewModel | Activities/Fragments | To ensure the UI controller remains lean and focused on view updates. |

## Common Mistakes

**Name**: Inflated Activity Context in ViewModel
- **Looks like**:
  ```kotlin
  class MyViewModel(val context: Context) : ViewModel() {
      // Use of context for data fetching
  }
  ```
- **Why it breaks**: Using an activity's context in ViewModel can lead to memory leaks as the ViewModel outlives the lifecycle of the Activity.
- **Correct**:
  ```kotlin
  class MyViewModel(private val locationService: LocationService) : ViewModel() {
      // Use dependency injection to provide location service
  }
  ```

## Key Relationships

- Lifecycle-aware components enable efficient data handling by respecting activity lifecycles, ensuring that data and UI updates are managed automatically.
- Data Binding simplifies UI updates based on LiveData changes from ViewModel, reducing the need for manual intervention in activities or fragments.

## Concepts (for graph)
- Handling lifecycles with lifecycle-aware components 

   Part of Android Jetpack .
- Lifecycle
- Figure 1.
- LifecycleOwner
- Implementing a custom LifecycleOwner
- Best practices for lifecycle-aware components
- Use cases for lifecycle-aware components
- Handling on stop events
- Additional resources
- Samples
- Codelabs
- Blogs

<!-- Quality Report
## Quality Report

| Section | Score | Issue (if < 4) |
| --- | --- | --- |
| Core Concepts | 5 | N/A |
| Mental Model | 3 | Lack of clarity in the distinction between lifecycle states and events. |
| Decision Framework | 4 | Minor improvements for clarity on ViewModel's role. |
| Common Mistakes | 5 | N/A |
| Key Relationships | 4 | Needs minor enhancement to clearly articulate ViewModel-Data Binding interaction. |

## Verdict: NEEDS_FIX

## Fixes (only if NEEDS_FIX)
Clarify the distinction between lifecycle states and events in Mental Model.
Enhance clarity on ViewModel's role in Decision Framework.
Articulate the relationship between ViewModel and Data Binding more precisely in Key Relationships.
-->
