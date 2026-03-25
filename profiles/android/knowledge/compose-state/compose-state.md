<!-- Source: https://developer.android.com/develop/ui/compose/state -->
<!-- Source: https://developer.android.com/develop/ui/compose/state-hoisting -->
<!-- Source: https://developer.android.com/develop/ui/compose/state-saving -->
<!-- Source: https://developer.android.com/develop/ui/compose/state-lifespans -->
<!-- Source: https://developer.android.com/develop/ui/compose/state-callbacks -->
<!-- Source: https://developer.android.com/develop/ui/compose/state-hoisting -->
<!-- Source: https://developer.android.com/develop/ui/compose/state-saving -->
<!-- Source: https://developer.android.com/develop/ui/compose/state-lifespans -->
<!-- Source: https://developer.android.com/develop/ui/compose/state-callbacks -->
<!-- Type: official -->
<!-- Priority: high -->
<!-- Topic: compose-state -->
<!-- Extracted: 2026-03-24 -->
<!-- Verified: — -->

# State and Jetpack Compose

## Rules
- DO: Flow : collectAsStateWithLifecycle() 

 collectAsStateWithLifecycle() collects values from a
 Flow in a lifecycle-aware manner, allowing your app to
conserve app resources. It represents the latest emitted value from the
Compose State . Use this API as the recommended way to collect flows on
Android
- DO: Use collectAsState for platform-agnostic code instead of
 collectAsStateWithLifecycle , which is Android-only.
- DON'T: Single source of truth: By moving state instead of duplicating it, we're
ensuring there's only one source of truth. This helps avoid bugs.
- DO: State should be hoisted to at least the lowest common
 parent of all composables that use the state (read).
- DO: State should be hoisted to at least the highest level it may
 be changed (write).
- DO: If two states change in response to the same events they should
 be hoisted together.
- DO: Use the saveable API of SavedStateHandle to read and write UI element
state as MutableState , so it survives activity and process recreation with
minimal code setup.
- DO: Use getStateFlow() to store UI element state and consume it as a flow
from the SavedStateHandle . The StateFlow is read
only, and the API requires you to specify a key so you can replace the flow to
emit a new value. With the key you configured, you can retrieve the StateFlow 
and collect the latest
- DON'T: Must not reference any objects that would be leaked if the activity is destroyed
- DO: Must be serializable (either with a custom Saver or with kotlinx.serialization )
- DON'T: Avoid retaining objects that are created and managed outside of your control,
 including Activity , View , Fragment ,
 ViewModel , Context , Lifecycle ,
 and any object that references one of these types. Generally speaking, if you
 wouldn't store an object in a ViewModel , you shouldn't retain it
- DON'T: Don't retain an object that has a shorter lifespan from retain
- DON'T: Don't remember an object twice
- DO: Ensure that stateful composables are always called in the same place in the
composition hierarchy. Implement adaptive layouts by altering the layout logic
instead of relocating objects in the composition hierarchy.
- DO: Use MovableContent to relocate stateful composables gracefully. Instances
of MovableContent are able to move remembered and retained values from their
old to new locations.
- DON'T: Prefix the function name with remember . Optionally, if the function
implementation depends on the object being retained and the API will never
evolve to rely on a different variation of remember , use the retain prefix
instead.
- DO: Use rememberSaveable or rememberSerializable if state persistence is
chosen and it's possible to write a correct Saver implementation.
- DON'T: Avoid side effects or initializing values based on CompositionLocal s that
might not be relevant to the usage. Remember, the place your state is created
might not be where it is consumed.
- DO: All composable functions should have no side-effects

## Code Patterns
### State and composition
```kotlin
@Composable
private fun HelloContent() {
    Column(modifier = Modifier.padding(16.dp)) {
        Text(
            text = "Hello!",
            modifier = Modifier.padding(bottom = 8.dp),
            style = MaterialTheme.typography.bodyMedium
        )
        OutlinedTextField(
            value = "",
            onValueChange = { },
            label = { Text("Name") }
        )
    }
}StateOverviewSnippets.kt
```

### State in composables
```
interface MutableState<T> : State<T> {
    override var value: T
}
```

### State in composables
```kotlin
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
```

### State in composables
```kotlin
@Composable
fun HelloContent() {
    Column(modifier = Modifier.padding(16.dp)) {
        var name by remember { mutableStateOf("") }
        if (name.isNotEmpty()) {
            Text(
                text = "Hello, $name!",
                modifier = Modifier.padding(bottom = 8.dp),
                style = MaterialTheme.typography.bodyMedium
            )
        }
        OutlinedTextField(
            value = name,
            onValueChange = { name = it },
            label = { Text("Name") }
        )
    }
}StateOverviewSnippets.kt
```

### Other supported types of state
```kotlin
dependencies {
      ...
      implementation("androidx.lifecycle:lifecycle-runtime-compose:2.10.0")
}
```

### Other supported types of state
```kotlin
dependencies {
      ...
      implementation("androidx.compose.runtime:runtime-livedata:1.10.5")
}
```

### State hoisting
```kotlin
@Composable
fun HelloScreen() {
    var name by rememberSaveable { mutableStateOf("") }

    HelloContent(name = name, onNameChange = { name = it })
}

@Composable
fun HelloContent(name: String, onNameChange: (String) -> Unit) {
    Column(modifier = Modifier.padding(16.dp)) {
        Text(
            text = "Hello, $name",
            modifier = Modifier.padding(bottom = 8.dp),
            style = MaterialTheme.typography.bodyMedium
        )
        OutlinedTextField(value = name, onValueChange = onNameChange, label = { Text("Name") })
    }
}StateOverviewSnippets.kt
```

### Parcelize
```kotlin
@Parcelize
data class City(val name: String, val country: String) : Parcelable

@Composable
fun CityScreen() {
    var selectedCity = rememberSaveable {
        mutableStateOf(City("Madrid", "Spain"))
    }
}StateOverviewSnippets.kt
```

### MapSaver
```kotlin
data class City(val name: String, val country: String)

val CitySaver = run {
    val nameKey = "Name"
    val countryKey = "Country"
    mapSaver(
        save = { mapOf(nameKey to it.name, countryKey to it.country) },
        restore = { City(it[nameKey] as String, it[countryKey] as String) }
    )
}

@Composable
fun CityScreen() {
    var selectedCity = rememberSaveable(stateSaver = CitySaver) {
        mutableStateOf(City("Madrid", "Spain"))
    }
}StateOverviewSnippets.kt
```

### Retrigger remember calculations when keys change
```
var name by remember { mutableStateOf("") }StateOverviewSnippets.kt
```

### Retrigger remember calculations when keys change
```kotlin
val brush = remember {
    ShaderBrush(
        BitmapShader(
            ImageBitmap.imageResource(res, avatarRes).asAndroidBitmap(),
            Shader.TileMode.REPEAT,
            Shader.TileMode.REPEAT
        )
    )
}StateOverviewSnippets.kt
```

### Retrigger remember calculations when keys change
```kotlin
@Composable
private fun BackgroundBanner(
    @DrawableRes avatarRes: Int,
    modifier: Modifier = Modifier,
    res: Resources = LocalContext.current.resources
) {
    val brush = remember(key1 = avatarRes) {
        ShaderBrush(
            BitmapShader(
                ImageBitmap.imageResource(res, avatarRes).asAndroidBitmap(),
                Shader.TileMode.REPEAT,
                Shader.TileMode.REPEAT
            )
        )
    }

    Box(
        modifier = modifier.background(brush)
    ) {
        /* ... */
    }
}StateOverviewSnippets.kt
```

### Retrigger remember calculations when keys change
```kotlin
@Composable
private fun rememberMyAppState(
    windowSizeClass: WindowSizeClass
): MyAppState {
    return remember(windowSizeClass) {
        MyAppState(windowSizeClass)
    }
}

@Stable
class MyAppState(
    private val windowSizeClass: WindowSizeClass
) { /* ... */ }StateOverviewSnippets.kt
```

### Store state with keys beyond recomposition
```
var userTypedQuery by rememberSaveable(typedQuery, stateSaver = TextFieldValue.Saver) {
    mutableStateOf(
        TextFieldValue(text = typedQuery, selection = TextRange(typedQuery.length))
    )
}StateOverviewSnippets.kt
```

### No state hoisting needed
```kotlin
@Composable
fun ChatBubble(
    message: Message
) {
    var showDetails by rememberSaveable { mutableStateOf(false) } // Define the UI element expanded state

    Text(
        text = AnnotatedString(message.content),
        modifier = Modifier.clickable {
            showDetails = !showDetails // Apply UI logic
        }
    )

    if (showDetails) {
        Text(message.timestamp)
    }
}StateHoistingSnippets.kt
```

### Hoisting within composables
```kotlin
@Composable
private fun ConversationScreen(/*...*/) {
    val scope = rememberCoroutineScope()

    val lazyListState = rememberLazyListState() // State hoisted to the ConversationScreen

    MessagesList(messages, lazyListState) // Reuse same state in MessageList

    UserInput(
        onMessageSent = { // Apply UI logic to lazyListState
            scope.launch {
                lazyListState.scrollToItem(0)
            }
        },
    )
}

@Composable
private fun MessagesList(
    messages: List<Message>,
    lazyListState: LazyListState = rememberLazyListState() // LazyListState has a default value
) {

    LazyColumn(
        state = lazyListState // Pass hoisted state to LazyColumn
    ) {
        items(messages, key = { message -> message.id }) { item ->
            Message(/*...*/)
        }
    }

    val scope = rememberCoroutineScope()

    JumpToBottom(onClicked = {
        scope.launch {
            lazyListState.scrollToItem(0) // UI logic being applied to lazyListState
        }
    })
}StateHoistingSnippets.kt
```

### Plain state holder class as state owner
```kotlin
// LazyListState.kt

@Stable
class LazyListState constructor(
    firstVisibleItemIndex: Int = 0,
    firstVisibleItemScrollOffset: Int = 0
) : ScrollableState {
    /**
     *   The holder class for the current scroll position.
     */
    private val scrollPosition = LazyListScrollPosition(
        firstVisibleItemIndex, firstVisibleItemScrollOffset
    )

    suspend fun scrollToItem(/*...*/) { /*...*/ }

    override suspend fun scroll() { /*...*/ }

    suspend fun animateScrollToItem() { /*...*/ }
}StateHoistingSnippets.kt
```

### Screen UI state
```kotlin
class ConversationViewModel(
    channelId: String,
    messagesRepository: MessagesRepository
) : ViewModel() {

    val messages = messagesRepository
        .getLatestMessages(channelId)
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = emptyList()
        )

    // Business logic
    fun sendMessage(message: Message) { /* ... */ }
}StateHoistingSnippets.kt
```

### Screen UI state
```kotlin
@Composable
private fun ConversationScreen(
    conversationViewModel: ConversationViewModel = viewModel()
) {

    val messages by conversationViewModel.messages.collectAsStateWithLifecycle()

    ConversationScreen(
        messages = messages,
        onSendMessage = { message: Message -> conversationViewModel.sendMessage(message) }
    )
}

@Composable
private fun ConversationScreen(
    messages: List<Message>,
    onSendMessage: (Message) -> Unit
) {

    MessagesList(messages, onSendMessage)
    /* ... */
}StateHoistingSnippets.kt
```

### UI element state
```kotlin
class ConversationViewModel(/*...*/) : ViewModel() {

    // Hoisted state
    var inputMessage by mutableStateOf("")
        private set

    val suggestions: StateFlow<List<Suggestion>> =
        snapshotFlow { inputMessage }
            .filter { hasSocialHandleHint(it) }
            .mapLatest { getHandle(it) }
            .mapLatest { repository.getSuggestions(it) }
            .stateIn(
                scope = viewModelScope,
                started = SharingStarted.WhileSubscribed(5_000),
                initialValue = emptyList()
            )

    fun updateInput(newInput: String) {
        inputMessage = newInput
    }
}StateHoistingSnippets.kt
```

### Caveat
```kotlin
class ConversationViewModel(/*...*/) : ViewModel() {

    val drawerState = DrawerState(initialValue = DrawerValue.Closed)

    private val _drawerContent = MutableStateFlow(DrawerContent.Empty)
    val drawerContent: StateFlow<DrawerContent> = _drawerContent.asStateFlow()

    fun closeDrawer(uiScope: CoroutineScope) {
        viewModelScope.launch {
            withContext(uiScope.coroutineContext) { // Use instead of the default context
                drawerState.close()
            }
            // Fetch drawer content and update state
            _drawerContent.update { content }
        }
    }
}

// in Compose
@Composable
private fun ConversationScreen(
    conversationViewModel: ConversationViewModel = viewModel()
) {
    val scope = rememberCoroutineScope()

    ConversationScreen(onCloseDrawer = { conversationViewModel.closeDrawer(uiScope = scope) })
}StateHoistingSnippets.kt
```

### UI logic
```kotlin
@Composable
fun rememberLazyListState(
    initialFirstVisibleItemIndex: Int = 0,
    initialFirstVisibleItemScrollOffset: Int = 0
): LazyListState {
    return rememberSaveable(saver = LazyListState.Saver) {
        LazyListState(
            initialFirstVisibleItemIndex, initialFirstVisibleItemScrollOffset
        )
    }
}SavingUIStateSnippets.kt
```

### Compose State
```kotlin
class ConversationViewModel(
    savedStateHandle: SavedStateHandle
) : ViewModel() {

    var message by savedStateHandle.saveable(stateSaver = TextFieldValue.Saver) {
        mutableStateOf(TextFieldValue(""))
    }
        private set

    fun update(newMessage: TextFieldValue) {
        message = newMessage
    }

    /*...*/
}

val viewModel = ConversationViewModel(SavedStateHandle())

@Composable
fun UserInput(/*...*/) {
    TextField(
        value = viewModel.message,
        onValueChange = { viewModel.update(it) }
    )
}SavingUIStateSnippets.kt
```

### StateFlow
```kotlin
private const val CHANNEL_FILTER_SAVED_STATE_KEY = "ChannelFilterKey"

class ChannelViewModel(
    channelsRepository: ChannelsRepository,
    private val savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val savedFilterType: StateFlow<ChannelsFilterType> = savedStateHandle.getStateFlow(
        key = CHANNEL_FILTER_SAVED_STATE_KEY, initialValue = ChannelsFilterType.ALL_CHANNELS
    )

    private val filteredChannels: Flow<List<Channel>> =
        combine(channelsRepository.getAll(), savedFilterType) { channels, type ->
            filter(channels, type)
        }.onStart { emit(emptyList()) }

    fun setFiltering(requestType: ChannelsFilterType) {
        savedStateHandle[CHANNEL_FILTER_SAVED_STATE_KEY] = requestType
    }

    /*...*/
}

enum class ChannelsFilterType {
    ALL_CHANNELS, RECENT_CHANNELS, ARCHIVED_CHANNELS
}SavingUIStateSnippets.kt
```

### rememberSaveable and rememberSerializable
```kotlin
data class Size(val x: Int, val y: Int) {
    object Saver : androidx.compose.runtime.saveable.Saver<Size, Any> by listSaver(
        save = { listOf(it.x, it.y) },
        restore = { Size(it[0], it[1]) }
    )
}

@Composable
fun rememberSize(x: Int, y: Int) {
    rememberSaveable(x, y, saver = Size.Saver) {
        Size(x, y)
    }
}StateLifespansSnippets.kt
```

### retain
```kotlin
@Composable
fun MediaPlayer() {
    // Use the application context to avoid a memory leak
    val applicationContext = LocalContext.current.applicationContext
    val exoPlayer = retain { ExoPlayer.Builder(applicationContext).apply { /* ... */ }.build() }
    // ...
}StateLifespansSnippets.kt
```

### Combine retain and rememberSaveable or rememberSerializable
```kotlin
@Composable
fun rememberAndRetain(): CombinedRememberRetained {
    val saveData = rememberSerializable(serializer = serializer<ExtractedSaveData>()) {
        ExtractedSaveData()
    }
    val retainData = retain { ExtractedRetainData() }
    return remember(saveData, retainData) {
        CombinedRememberRetained(saveData, retainData)
    }
}

@Serializable
data class ExtractedSaveData(
    // All values that should persist process death should be managed by this class.
    var savedData: AnotherSerializableType = defaultValue()
)

class ExtractedRetainData {
    // All values that should be retained should appear in this class.
    // It's possible to manage a CoroutineScope using RetainObserver.
    // See the full sample for details.
    var retainedData = Any()
}

class CombinedRememberRetained(
    private val saveData: ExtractedSaveData,
    private val retainData: ExtractedRetainData,
) {
    fun doAction() {
        // Manipulate the retained and saved state as needed.
    }
}StateLifespansSnippets.kt
```

### Remember factory functions
```kotlin
@Composable
fun rememberImageState(
    imageUri: String,
    initialZoom: Float = 1f,
    initialPanX: Int = 0,
    initialPanY: Int = 0
): ImageState {
    return rememberSaveable(imageUri, saver = ImageState.Saver) {
        ImageState(
            imageUri, initialZoom, initialPanX, initialPanY
        )
    }
}

data class ImageState(
    val imageUri: String,
    val zoom: Float,
    val panX: Int,
    val panY: Int
) {
    object Saver : androidx.compose.runtime.saveable.Saver<ImageState, Any> by listSaver(
        save = { listOf(it.imageUri, it.zoom, it.panX, it.panY) },
        restore = { ImageState(it[0] as String, it[1] as Float, it[2] as Int, it[3] as Int) }
    )
}StateLifespansSnippets.kt
```

### Run initialization side effects during onRemembered or onRetained , not construc
```kotlin
class MyComposeObject : RememberObserver {
    private val job = Job()
    private val coroutineScope = CoroutineScope(Dispatchers.Main + job)

    init {
        // Not recommended: This will cause work to begin during composition instead of
        // with other effects. Move this into onRemembered().
        coroutineScope.launch { loadData() }
    }

    override fun onRemembered() {
        // Recommended: Move any cancellable or effect-driven work into the onRemembered
        // callback. If implementing RetainObserver, this should go in onRetained.
        coroutineScope.launch { loadData() }
    }

    private suspend fun loadData() { /* ... */ }

    // ...
}RememberAndRetainObserverSnippets.kt
```

### Keep RememberObserver and RetainObserver implementations private
```kotlin
abstract class MyManager

// Not Recommended: Exposing a public constructor (even implicitly) for an object implementing
// RememberObserver can cause unexpected invocations if it is remembered multiple times.
class MyComposeManager : MyManager(), RememberObserver { ... }

// Not Recommended: The return type may be an implementation of RememberObserver and should be
// remembered explicitly.
fun createFoo(): MyManager = MyComposeManager()
```

### Keep RememberObserver and RetainObserver implementations private
```kotlin
abstract class MyManager

class MyComposeManager : MyManager() {
    // Callers that construct this object must manually call initialize and teardown
    fun initialize() { /*...*/ }
    fun teardown() { /*...*/ }
}

@Composable
fun rememberMyManager(): MyManager {
    // Protect the RememberObserver implementation by never exposing it outside the library
    return remember {
        object : RememberObserver {
            val manager = MyComposeManager()
            override fun onRemembered() = manager.initialize()
            override fun onForgotten() = manager.teardown()
            override fun onAbandoned() { /* Nothing to do if manager hasn't initialized */ }
        }
    }.manager
}RememberAndRetainObserverSnippets.kt
```

### Only remember objects once
```kotlin
val first: RememberObserver = rememberFoo()

// Not Recommended: Re-remembered `Foo` now gets double callbacks
val second = remember { first }
```

### Only remember objects once
```kotlin
val foo: Foo = rememberFoo()

// Acceptable:
val bar: Bar = remember { Bar(foo) }

// Recommended key usage:
val barWithKey: Bar = remember(foo) { Bar(foo) }RememberAndRetainObserverSnippets.kt
```

### Assume function arguments are already remembered
```kotlin
@Composable
fun MyComposable(
    parameter: Foo
) {
    // Not Recommended: Input should be remembered by the caller.
    val rememberedParameter = remember { parameter }
}
```

## Pitfalls
- Caution: Using mutable objects such as ArrayList<T> or mutableListOf() as
state in Compose causes your users to see incorrect or stale data in your app.
Mutable objects that are not observable, such as ArrayList or a mutable data
class, are not observable by Compose and don't trigger a recomposition
- Key Point: Keeping UI element state internal to composable functions is
acceptable. This is a good solution if the state and logic you apply to it is
simple and other parts of the UI hierarchy don't need the state. For example,
this is usually the case of animation state.
- Key Point: Hoist state to the lowest common ancestor and avoid passing it to
composables that don't need it.
- Warning: Calling some suspend functions exposed from Compose UI element state
that trigger animations throw exceptions if called from a CoroutineScope 
that's not scoped to the Composition. For example,
 LazyListState.animateScrollTo() and DrawerState.close() .
- Caution: The saveable API is experimental.
- Caution: retain shouldn't be used with objects that have
 a lifespan that is shorter than the lifespan given by retain, because this
 can cause memory leaks. This also applies to the key inputs of
 retain , which are referenced for as long as the value is
 retained.
 
 Avoid retaining objects that a
- Note: Don't retain an object that was created by
 remember ,
 rememberSaveable , or rememberSerializable . Retaining
and remembering the
same object is an antipattern and violates two broader recommendations:
 
 Don't retain an object that has a shorter lifespan from retain 
 Don't remember an objec

## Decision Tables
### SavedStateHandle APIs
| Compose State | saveable() |
| --- | --- |
| StateFlow | getStateFlow() |

### Summary
| Event | UI logic | Business logic in a ViewModel |
| --- | --- | --- |
| Configuration changes | rememberSaveable | Automatic |
| System-initiated process death | rememberSaveable | SavedStateHandle |

### Choose the correct lifespan
|  | remember | retain | rememberSaveable , rememberSerializable |
| --- | --- | --- | --- |
| Values survive recompositions? | ✅ | ✅ | ✅ |
| Values survive activity recreations? | ❌ | ✅ The same ( === ) instance will always be returned | ✅ An equivalent ( == ) object will be returned, possibly a deserialized copy |
| Values survive process death? | ❌ | ❌ | ✅ |
| Supported data types | All | Must not reference any objects that would be leaked if the activity is destroyed | Must be serializable (either with a custom Saver or with kotlinx.serialization ) |
| Use cases | Objects that are scoped to the composition 
 Configuration objects for composables 
 State that could be recreated without losing UI fidelity | Caches 
 Long-lived or "manager" objects | User input 
 State that can't be recreated by the app, including text field input, scroll state, toggles, etc. |

### retain versus ViewModel
|  | retain | ViewModel |
| --- | --- | --- |
| Scoping | No shared values; each value is retained at and associated with a
 specific point in the composition hierarchy. Retaining the same type in a
 different location always acts on a new instance. | ViewModel s are singletons within a
 ViewModelStore |
| Destruction | When permanently leaving the composition hierarchy | When the ViewModelStore is cleared or destroyed |
| Additional functionality | Can receive callbacks when the object is in the composition hierarchy
 or not | Built-in coroutineScope , support for
 SavedStateHandle , can be injected using Hilt |
| Owned by | RetainedValuesStore | ViewModelStore |
| Use cases | Persisting UI-specific values local to individual composable
 instances 
 Impression tracking, possibly through RetainedEffect 
 Building block for defining a custom "ViewModel-like" architecture
 component | Extracting interactions between UI and data layers into a separate
 class, both for code organization and testing 
 Transforming Flow s into State objects and
 calling suspend functions that shouldn't be interrupted by configuration
 changes 
 Sharing states over large UI areas, like entire screens 
 Interoperability with View |

## Guidelines
- Jetpack Compose helps you be explicit about where and how you store and use
state in an Android app. This guide focuses on the connection between state and
composables, and on the APIs that Jetpack Compose offers to work with state more
easily.
- Composable functions can use the
 remember 
API to store an object in memory. A value computed by remember is
stored in the Composition during
initial composition, and the stored value is returned during recomposition.
 remember can be used to store both mutable and immutable objects.
- These declarations are equivalent, and are provided as syntax sugar for
different uses of state. You should pick the one that produces the
easiest-to-read code in the composable you're writing.
- import androidx.compose.runtime.getValue 
 import androidx.compose.runtime.setValue 
 
 You can use the remembered value as a parameter for other composables or even as
logic in statements to change which composables are displayed. For example, if
you don't want to display the greeting if the name is empty, use the state in an
 if statement:
- While remember helps you retain state across recompositions, the state is not
retained across configuration changes. For this, you must use
 rememberSaveable . rememberSaveable automatically saves any value that can be
saved in a Bundle . For other values, you can pass in a custom saver object.
- Compose doesn't require that you use MutableState<T> to hold state; it
supports other observable types. Before reading another observable type in
Compose, you must convert it to a State<T> so that composables can
automatically recompose when the state changes.
- collectAsStateWithLifecycle() collects values from a
 Flow in a lifecycle-aware manner, allowing your app to
conserve app resources. It represents the latest emitted value from the
Compose State . Use this API as the recommended way to collect flows on
Android apps.
- The following dependency is required in the build.gradle file (it should
be 2.6.0-beta01 or newer):
- Flow : collectAsState() 

 collectAsState is similar to collectAsStateWithLifecycle , because it also
collects values from a Flow and transforms it into Compose State . 

 Use collectAsState for platform-agnostic code instead of
 collectAsStateWithLifecycle , which is Android-only. 

 Additional dependencies are not required for collectAsState , because it is
available in compose-runtime .
- Key Point: Compose automatically recomposes from reading State objects. If you
use another observable type such as LiveData in Compose, you should
convert it to State before reading it. Make sure that type conversion happens
in a composable, using a composable extension function like
 LiveData<T>.observeAsState() .
- As you develop reusable composables, you often want to expose both a stateful
and a stateless version of the same composable. The stateful version is
convenient for callers that don't care about the state, and the stateless
version is necessary for callers that need to control or hoist the state.
- However, you are not limited to onValueChange . If more specific events are
appropriate for the composable, you should define them using lambdas.
- By hoisting the state out of HelloContent , it's easier to reason about the
composable, reuse it in different situations, and test. HelloContent is
decoupled from how its state is stored. Decoupling means that if you modify or
replace HelloScreen , you don't have to change how HelloContent is
implemented.
- Key Point: When hoisting state, there are three rules to help
 you figure out where state should go:
- If for some reason @Parcelize is not suitable, you can use mapSaver to
define your own rule for converting an object into a set of values that the
system can save to the Bundle .
- To avoid needing to define the keys for the map, you can also use listSaver 
and use its indices as keys:
- Apart from caching state, you can also use remember to store any object or
result of an operation in the Composition that is expensive to initialize or
calculate. You might not want to repeat this calculation in every recomposition.
An example is creating this ShaderBrush object, which is an expensive
operation:
- Note: At first glance, using remember with keys might seem similar to using
other Compose APIs, like derivedStateOf . See the Jetpack Compose — When
should I use derivedStateOf? blog post to learn about the
difference.
- Note: There is a difference in API naming that you should note. In the
 remember API, you use the parameter name keys , and in rememberSaveable you
use inputs for the same purpose. If any of these parameters changes, the
cached value is invalidated.
- You should hoist UI state to the lowest common ancestor between all the
composables that read and write it. You should keep state closest to where it is
consumed. From the state owner, expose to consumers immutable state and events
to modify the state.

## Core Concepts

1. **State Hoisting**
   - **Explanation**: The process of moving state up to a common ancestor among composables that use or modify the state.
   - **Failure Mode**: Failing to hoist state can lead to inconsistencies and duplicate states across composables, making maintenance difficult.
   - **Boundaries**: Applies when multiple composables need to access or update shared mutable data.

2. **Single Source of Truth**
   - **Explanation**: Ensuring that any piece of mutable data has only one authoritative source within the composition hierarchy.
   - **Failure Mode**: Duplicating state across composables can lead to inconsistent UI states and complex maintenance.
   - **Boundaries**: Applies when multiple composables depend on the same mutable data.

3. **UI State Management with Compose APIs**
   - **Explanation**: Using `remember`, `MutableState`, and lifecycle-aware collection methods like `collectAsStateWithLifecycle()` to manage state in Jetpack Compose applications.
   - **Failure Mode**: Failing to use these APIs can lead to resource leaks or inconsistent UI updates.

4. **Compose Lifecycle-Aware Collection**
   - **Explanation**: Collecting values from Flows in a lifecycle-aware manner to conserve resources and avoid unnecessary emissions when composables are not active.
   - **Failure Mode**: Without lifecycle awareness, flows could emit values even when the composition is paused or destroyed, leading to resource wastage.

5. **Saving UI Element State with SavedStateHandle**
   - **Explanation**: Using `SavedStateHandle` in conjunction with `rememberSaveable` to preserve state across configuration changes and process death.
   - **Failure Mode**: Failing to save state can lead to loss of user input or other critical data during lifecycle events.

## Mental Model
- **The Problem**: Managing state efficiently in Jetpack Compose to ensure that the app updates correctly when configuration changes or process death occurs, while also conserving resources.
- **Core Insight**: UI is a function of state (`UI = f(state)`), and Jetpack Compose relies on observable state (e.g., `MutableState`, `StateFlow`) to automatically trigger recompositions. State management practices in Compose aim at ensuring that the state remains consistent across different lifecycle events without causing memory leaks or resource wastage.
- **How Concepts Connect**: 
  - **Single Source of Truth → Hoisting** (A single piece of mutable data should not be duplicated across multiple composables; instead, it should be hoisted to a common ancestor.)
  - **Hoisting → Lifecycle-Aware Collection** (State that is hoisted needs to be collected in a lifecycle-aware manner to ensure proper cleanup and resource management when the lifecycle changes.)
  - **Lifecycle-Aware Collection → Saving State Across Config Changes & Process Death** (The state collected with lifecycle-aware methods can be preserved using `rememberSaveable` or `SavedStateHandle`, ensuring that UI retains its state across different lifecycle events.)

## Decision Tables
### SavedStateHandle APIs
| Compose State | saveable() |
| --- | --- |
| StateFlow | getStateFlow() |

### Choose the correct lifespan
|  | remember | retain | rememberSaveable , rememberSerializable |
| --- | --- | --- | --- |
| Values survive recompositions? | ✅ | ✅ | ✅ |
| Values survive activity recreations? | ❌ | ✅ The same ( === ) instance will always be returned | ✅ An equivalent ( == ) object will be returned, possibly a deserialized copy |
| Values survive process death? | ❌ | ❌ | ✅ |

## Guidelines
- Jetpack Compose requires explicit management of where and how state is stored and used. This guide focuses on integrating state with composables through `remember`, `MutableState`, and lifecycle-aware collection mechanisms.
- **Remember API**: Used for retaining objects across recompositions but not configuration changes unless combined with `rememberSaveable`.
- **Collecting Flows**: Use `collectAsStateWithLifecycle()` to collect values from flows in a lifecycle-aware manner, ensuring resource conservation.

## Concepts (for graph)
- State and composition
- Key Term:
- Composition:
- Initial composition:
- Recomposition:
- State in composables
- Other supported types of state
- Key Point:
- Stateful versus stateless
- State hoisting
- Single source of truth:
- Encapsulated:

<!-- Quality Report
## Quality Report

| Section | Score | Issue (if < 4) |
| --- | --- | --- |
| Core Concepts | 5 | None |
| Mental Model | 5 | None |
| Decision Framework | 4 | Minor improvements needed for clarity and alignment with the guidelines. |
| Common Mistakes | 4 | Could be more actionable, providing concrete examples or steps to avoid common pitfalls. |
| Key Relationships | 5 | None |

## Verdict: PASS

There are no sections scoring below a 4, ensuring that the knowledge base entry is precise, grounded, and actionable without any hallucinations or missing core concepts.

## Fixes (only if NEEDS_FIX)
N/A
-->
