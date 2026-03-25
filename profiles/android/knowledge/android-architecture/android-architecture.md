<!-- Source: https://developer.android.com/topic/architecture -->
<!-- Source: https://developer.android.com/topic/architecture/intro -->
<!-- Source: https://developer.android.com/topic/architecture/recommendations -->
<!-- Source: https://developer.android.com/topic/architecture/ui-layer -->
<!-- Source: https://developer.android.com/topic/architecture/ui-layer/events -->
<!-- Source: https://developer.android.com/topic/architecture/ui-layer/stateholders -->
<!-- Source: https://developer.android.com/topic/architecture/ui-layer/state-production -->
<!-- Source: https://developer.android.com/topic/architecture/domain-layer -->
<!-- Source: https://developer.android.com/topic/architecture/data-layer -->
<!-- Source: https://developer.android.com/topic/architecture/data-layer/offline-first -->
<!-- Type: official -->
<!-- Priority: high -->
<!-- Topic: android-architecture -->
<!-- Extracted: 2026-03-24 -->
<!-- Verified: — -->

# Guide to app architecture

## Rules
- DON'T: Users don't lose data if the Android OS destroys your app to free up
resources.
- DON'T: Don't store data in app components.
- DON'T: Avoid designating your app's entry points—such as activities, services,
and broadcast receivers—as sources of data. The entry points should only
coordinate with other components to retrieve the subset of data that is relevant
to that entry point. Each app component is short‑lived, depending
on the u
- DON'T: Don't spread the code that loads data from the network across multiple classes
or packages in your codebase. Similarly, don't define multiple unrelated
responsibilities, such as data caching and data binding, in the same class.
Following the recommended app architecture will help.
- DON'T: Don't create shortcuts that expose internal implementation details. You might
gain a bit of time in the short term, but you are then likely to incur technical
debt many times over as your codebase evolves.
- DON'T: Don't reinvent the wheel by writing the same boilerplate code again and again.
Instead, focus your time and energy on what makes your app unique. Let the
Jetpack libraries and other recommended libraries handle the repetitive
boilerplate.
- DO: Use canonical layouts and app design patterns.
- DO: Strongly recommended: You should implement this practice unless it clashes fundamentally with your approach.
- DO: Recommended: This practice is likely to improve your app.
- DO: You should create repositories even if they just contain a single data source.
- DON'T: Do not use ViewModels in reusable pieces of UI. You should use ViewModels in:
- DO: You should make uiState a StateFlow .
- DO: You should create the uiState using the stateIn operator with the WhileSubscribed(5000) policy (example) if the data comes as a stream of data from other layers of the hierarchy.
- DO: You should create a collectJob if using WhileSubscribed
- DON'T: Business logic is the implementation of product requirements for app
data. As mentioned already, one example is bookmarking an article in the
case study app. Business logic is usually placed in the domain or data
layers, but never in the UI layer.
- DO: A UI state object should handle states that are related to each other. 
This leads to fewer inconsistencies and it makes the code easier to
understand. If you expose the list of news items and the number of bookmarks
in two different streams, you might end up in a situation where one was
updated and
- DO: UI states: single stream or multiple streams? The key guiding principle
for choosing between exposing UI state in a single stream or in multiple
streams is the previous bullet point: the relationship between the items
emitted. The biggest advantage to a single-stream exposure is convenience and
data
- DON'T: UiState diffing: The more fields there are in a UiState object, the
more likely it is that the stream will emit as a result of one of its fields
being updated. Because views don't have a diffing mechanism to understand
whether consecutive emissions are different or the same, every emission
causes an
- DO: UI events: Actions that should be handled in the UI layer.
- DO: Each class should do what they're responsible for, not more. The UI is in
charge of screen-specific behavior logic such as navigation calls, click
events, and obtaining permission requests. The ViewModel contains business
logic and converts the results from lower layers of the hierarchy into UI
stat
- DON'T: UI lifecycle independent : This part of the UI layer deals with the data
producing layers of the app (data or domain layers) and is defined by business
logic. Lifecycle, configuration changes, and Activity recreation in the UI
may affect if the UI state production pipeline is active, but do not affe
- DO: Know what APIs you should use to produce UI state. This depends on the
nature of the sources of state change available in your state holders,
following unidirectional data flow principles.
- DO: Know how you should scope the production of UI state to be conscious of
system resources.
- DO: Know how you should expose the UI state for consumption by the UI.
- DO: Lifecycle aware : In the case where the UI is not visible or active, the
state production pipeline should not consume any resources unless explicitly
required.
- DO: Easy to consume : The UI should be able to easily render the produced UI
state. Considerations for the output of the state production pipeline will
vary across different View APIs such as the View system or Jetpack Compose.
- DO: Use the MutableStateFlow API as an observable, mutable
container of state. In Jetpack Compose apps, you can also consider
 mutableStateOf especially when working with
 Compose text APIs . Both APIs offer methods that allow safe
atomic updates to the values they host whether or not the updates are
sy
- DO: Use the withContext method to run Coroutines in a
different concurrent context.
- DO: Use SharingStarted.WhileSubscribed() if the pipeline should only be active
when the UI is visible while collecting the flow in a lifecycle-aware
manner.
- DO: Use SharingStarted.Lazily if the pipeline should be active as long as the
user may return to the UI, that is the UI is on the backstack, or in another
tab offscreen.
- DO: Whether state should be exposed in one or multiple fields from the
state holder.
- DO: Use cases don't have their own lifecycle. Instead, they're scoped to the class
that uses them. This means that you can call use cases from classes in the UI
layer, from services, or from the Application class itself. Because use cases
shouldn't contain mutable data, you should create a new instance
- DO: Use cases from the domain layer must be main-safe ; in other words, they must
be safe to call from the main thread. If use case classes perform long-running
blocking operations, they are responsible for moving that logic to the
appropriate thread. However, before doing that, check if those blocking
- DO: One-shot operations: The data layer should expose suspend functions in
Kotlin; and for the Java programming language, the data layer should expose
functions that provide a callback to notify the result of the operation, or
RxJava Single , Maybe , or Completable types.
- DO: To be notified of data changes over time: The data layer should expose
 flows in Kotlin; and for the Java programming language, the
data layer should expose a callback that emits the new data, or the RxJava
 Observable or Flowable type.
- DON'T: Don't name the data source based on an implementation detail—for example,
 UserSharedPreferencesDataSource —because repositories that use that data source
shouldn't know how the data is saved. If you follow this rule, you can change
the implementation of the data source (for example, migrating from
- DO: Use of the catch operator in a ViewModel is as follows:
- DO: The kind of error the network data source indicated. For example, you should
retry network calls that return an error that indicate a lack of
connectivity. Conversely, you shouldn't retry HTTP requests that are not
authorized until proper credentials are available.
- DO: Use cases for this approach include analytics events and logging.

## Code Patterns
### Views
```kotlin
class MyFragment : Fragment() {

    private val viewModel: MyViewModel by viewModel()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        viewLifecycleOwner.lifecycleScope.launch {
            viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.uiState.collect {
                    // Process item
                }
            }
        }
    }
}
```

### Compose
```kotlin
@Composable
fun MyScreen(
    viewModel: MyViewModel = viewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
}
```

### ViewModel
```kotlin
@HiltViewModel
class BookmarksViewModel @Inject constructor(
    newsRepository: NewsRepository
) : ViewModel() {

    val feedState: StateFlow<NewsFeedUiState> =
        newsRepository
            .getNewsResourcesStream()
            .mapToFeedState(savedNewsResourcesState)
            .stateIn(
                scope = viewModelScope,
                started = SharingStarted.WhileSubscribed(5_000),
                initialValue = NewsFeedUiState.Loading
            )

    // ...
}
```

### Views
```kotlin
class MyFragment: Fragment() {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        viewLifecycleOwner.lifecycle.addObserver(object : DefaultLifecycleObserver {
            override fun onResume(owner: LifecycleOwner) {
                // ...
            }
            override fun onPause(owner: LifecycleOwner) {
                // ...
            }
        }
    }
}
```

### Compose
```kotlin
@Composable
fun MyApp() {

    val lifecycleOwner = LocalLifecycleOwner.current
    DisposableEffect(lifecycleOwner, ...) {
        val lifecycleObserver = object : DefaultLifecycleObserver {
            override fun onStop(owner: LifecycleOwner) {
                // ...
            }
        }

        lifecycleOwner.lifecycle.addObserver(lifecycleObserver)
        onDispose {
            lifecycleOwner.lifecycle.removeObserver(lifecycleObserver)
        }
    }
}
```

### Define UI state
```kotlin
data class NewsUiState(
    val isSignedIn: Boolean = false,
    val isPremium: Boolean = false,
    val newsItems: List<NewsItemUiState> = listOf(),
    val userMessages: List<Message> = listOf()
)

data class NewsItemUiState(
    val title: String,
    val body: String,
    val bookmarked: Boolean = false,
    ...
)
```

### Views
```kotlin
class NewsViewModel(...) : ViewModel() {

    val uiState: StateFlow<NewsUiState> = …
}
```

### Compose
```kotlin
class NewsViewModel(...) : ViewModel() {

    val uiState: NewsUiState = …
}
```

### Views
```kotlin
class NewsViewModel(...) : ViewModel() {

    private val _uiState = MutableStateFlow(NewsUiState())
    val uiState: StateFlow<NewsUiState> = _uiState.asStateFlow()

    ...

}
```

### Compose
```
class NewsViewModel(...) : ViewModel() {

    var uiState by mutableStateOf(NewsUiState())
        private set

    ...
}
```

### Views
```kotlin
class NewsViewModel(
    private val repository: NewsRepository,
    ...
) : ViewModel() {

    private val _uiState = MutableStateFlow(NewsUiState())
    val uiState: StateFlow<NewsUiState> = _uiState.asStateFlow()

    private var fetchJob: Job? = null

    fun fetchArticles(category: String) {
        fetchJob?.cancel()
        fetchJob = viewModelScope.launch {
            try {
                val newsItems = repository.newsItemsForCategory(category)
                _uiState.update {
                    it.copy(newsItems = newsItems)
                }
            } catch (ioe: IOException) {
                // Handle the error and notify the UI when appropriate.
                _uiState.update {
                    val messages = getMessagesFromThrowable(ioe)
                    it.copy(userMessages = messages)
                 }
            }
        }
    }
}
```

### Views
```kotlin
class NewsActivity : AppCompatActivity() {

    private val viewModel: NewsViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        ...

        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.uiState.collect {
                    // Update UI elements
                }
            }
        }
    }
}
```

### Compose
```kotlin
@Composable
fun LatestNewsScreen(
    viewModel: NewsViewModel = viewModel()
) {
    // Show UI elements based on the viewModel.uiState
}
```

### Show in-progress operations
```kotlin
data class NewsUiState(
    val isFetchingArticles: Boolean = false,
    ...
)
```

### Compose
```kotlin
@Composable
fun LatestNewsScreen(
    modifier: Modifier = Modifier,
    viewModel: NewsViewModel = viewModel()
) {
    Box(modifier.fillMaxSize()) {

        if (viewModel.uiState.isFetchingArticles) {
            CircularProgressIndicator(Modifier.align(Alignment.Center))
        }

        // Add other UI elements. For example, the list.
    }
}
```

### Show errors on the screen
```kotlin
data class Message(val id: Long, val message: String)

data class NewsUiState(
    val userMessages: List<Message> = listOf(),
    ...
)
```

### Views
```kotlin
class LatestNewsActivity : AppCompatActivity() {

    private lateinit var binding: ActivityLatestNewsBinding
    private val viewModel: LatestNewsViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        /* ... */

        // The expand details event is processed by the UI that
        // modifies a View's internal state.
        binding.expandButton.setOnClickListener {
            binding.expandedSection.visibility = View.VISIBLE
        }

        // The refresh event is processed by the ViewModel that is in charge
        // of the business logic.
        binding.refreshButton.setOnClickListener {
            viewModel.refreshNews()
        }
    }
}
```

### Compose
```kotlin
@Composable
fun LatestNewsScreen(viewModel: LatestNewsViewModel = viewModel()) {

    // State of whether more details should be shown
    var expanded by remember { mutableStateOf(false) }

    Column {
        Text("Some text")
        if (expanded) {
            Text("More details")
        }

        Button(
          // The expand details event is processed by the UI that
          // modifies this composable's internal state.
          onClick = { expanded = !expanded }
        ) {
          val expandText = if (expanded) "Collapse" else "Expand"
          Text("$expandText details")
        }

        // The refresh event is processed by the ViewModel that is in charge
        // of the UI's business logic.
        Button(onClick = { viewModel.refreshNews() }) {
            Text("Refresh data")
        }
    }
}
```

### User events in RecyclerViews
```kotlin
data class NewsItemUiState(
    val title: String,
    val body: String,
    val bookmarked: Boolean = false,
    val publicationDate: String,
    val onBookmark: () -> Unit
)

class LatestNewsViewModel(
    private val formatDateUseCase: FormatDateUseCase,
    private val repository: NewsRepository
)
    val newsListUiItems = repository.latestNews.map { news ->
        NewsItemUiState(
            title = news.title,
            body = news.body,
            bookmarked = news.bookmarked,
            publicationDate = formatDateUseCase(news.publicationDate),
            // Business logic is passed as a lambda function that the
            // UI calls on click events.
            onBookmark = {
                repository.addBookmark(news.id)
            }
        )
    }
}
```

### Handle ViewModel events
```kotlin
data class LoginUiState(
    val isLoading: Boolean = false,
    val errorMessage: String? = null,
    val isUserLoggedIn: Boolean = false
)
```

### Views
```kotlin
class LoginViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(LoginUiState())
    val uiState: StateFlow<LoginUiState> = _uiState.asStateFlow()
    /* ... */
}

class LoginActivity : AppCompatActivity() {
    private val viewModel: LoginViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        /* ... */

        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.uiState.collect { uiState ->
                    if (uiState.isUserLoggedIn) {
                        // Navigate to the Home screen.
                    }
                    ...
                }
            }
        }
    }
}
```

### Compose
```kotlin
class LoginViewModel : ViewModel() {
    var uiState by mutableStateOf(LoginUiState())
        private set
    /* ... */
}

@Composable
fun LoginScreen(
    viewModel: LoginViewModel = viewModel(),
    onUserLogIn: () -> Unit
) {
    val currentOnUserLogIn by rememberUpdatedState(onUserLogIn)

    // Whenever the uiState changes, check if the user is logged in.
    LaunchedEffect(viewModel.uiState)  {
        if (viewModel.uiState.isUserLoggedIn) {
            currentOnUserLogIn()
        }
    }

    // Rest of the UI for the login screen.
}
```

### Consuming events can trigger state updates
```kotlin
// Models the UI state for the Latest news screen.
data class LatestNewsUiState(
    val news: List<News> = emptyList(),
    val isLoading: Boolean = false,
    val userMessage: String? = null
)
```

### Views
```kotlin
class LatestNewsViewModel(/* ... */) : ViewModel() {

    private val _uiState = MutableStateFlow(LatestNewsUiState(isLoading = true))
    val uiState: StateFlow<LatestNewsUiState> = _uiState

    fun refreshNews() {
        viewModelScope.launch {
            // If there isn't internet connection, show a new message on the screen.
            if (!internetConnection()) {
                _uiState.update { currentUiState ->
                    currentUiState.copy(userMessage = "No Internet connection")
                }
                return@launch
            }

            // Do something else.
        }
    }

    fun userMessageShown() {
        _uiState.update { currentUiState ->
            currentUiState.copy(userMessage = null)
        }
    }
}
```

### Compose
```kotlin
class LatestNewsViewModel(/* ... */) : ViewModel() {

    var uiState by mutableStateOf(LatestNewsUiState())
        private set

    fun refreshNews() {
        viewModelScope.launch {
            // If there isn't internet connection, show a new message on the screen.
            if (!internetConnection()) {
                uiState = uiState.copy(userMessage = "No Internet connection")
                return@launch
            }

            // Do something else.
        }
    }

    fun userMessageShown() {
        uiState = uiState.copy(userMessage = null)
    }
}
```

### Views
```kotlin
class LatestNewsActivity : AppCompatActivity() {
    private val viewModel: LatestNewsViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        /* ... */

        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.uiState.collect { uiState ->
                    uiState.userMessage?.let {
                        // TODO: Show Snackbar with userMessage.

                        // Once the message is displayed and
                        // dismissed, notify the ViewModel.
                        viewModel.userMessageShown()
                    }
                    ...
                }
            }
        }
    }
}
```

### Compose
```kotlin
@Composable
fun LatestNewsScreen(
    snackbarHostState: SnackbarHostState,
    viewModel: LatestNewsViewModel = viewModel(),
) {
    // Rest of the UI content.

    // If there are user messages to show on the screen,
    // show it and notify the ViewModel.
    viewModel.uiState.userMessage?.let { userMessage ->
        LaunchedEffect(userMessage) {
            snackbarHostState.showSnackbar(userMessage)
            // Once the message is displayed and dismissed, notify the ViewModel.
            viewModel.userMessageShown()
        }
    }
}
```

### Views
```kotlin
class LoginActivity : AppCompatActivity() {

    private lateinit var binding: ActivityLoginBinding
    private val viewModel: LoginViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        /* ... */

        binding.helpButton.setOnClickListener {
            navController.navigate(...) // Open help screen
        }
    }
}
```

### Compose
```kotlin
@Composable
fun LoginScreen(
    onHelp: () -> Unit, // Caller navigates to the right screen
    viewModel: LoginViewModel = viewModel()
) {
    // Rest of the UI

    Button(onClick = onHelp) {
        Text("Get help")
    }
}
```

### Views
```kotlin
class LoginActivity : AppCompatActivity() {
    private val viewModel: LoginViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        /* ... */

        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.uiState.collect { uiState ->
                    if (uiState.isUserLoggedIn) {
                        // Navigate to the Home screen.
                    }
                    ...
                }
            }
        }
    }
}
```

### Compose
```kotlin
@Composable
fun LoginScreen(
    onUserLogIn: () -> Unit, // Caller navigates to the right screen
    viewModel: LoginViewModel = viewModel()
) {
    Button(
        onClick = {
            // ViewModel validation is triggered
            viewModel.login()
        }
    ) {
        Text("Log in")
    }
    // Rest of the UI

    val lifecycle = LocalLifecycleOwner.current.lifecycle
    val currentOnUserLogIn by rememberUpdatedState(onUserLogIn)
    LaunchedEffect(viewModel, lifecycle)  {
        // Whenever the uiState changes, check if the user is logged in and
        // call the `onUserLogin` event when `lifecycle` is at least STARTED
        snapshotFlow { viewModel.uiState }
            .filter { it.isUserLoggedIn }
            .flowWithLifecycle(lifecycle)
            .collect {
                currentOnUserLogIn()
            }
    }
}
```

### Views
```kotlin
// Key that identifies the `validationInProgress` state in the Bundle
private const val DOB_VALIDATION_KEY = "dobValidationKey"

class DobValidationFragment : Fragment() {

    private var validationInProgress: Boolean = false
    private val viewModel: DobValidationViewModel by viewModels()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        val binding = // ...
        validationInProgress = savedInstanceState?.getBoolean(DOB_VALIDATION_KEY) ?: false

        binding.continueButton.setOnClickListener {
            viewModel.validateDob()
            validationInProgress = true
        }

        viewLifecycleOwner.lifecycleScope.launch {
            viewModel.uiState
                .flowWithLifecycle(viewLifecycleOwner.lifecycle)
                .collect { uiState ->
                    // Update other parts of the UI ...

                    // If the input is valid and the user wants
                    // to navigate, navigate to the next screen
                    // and reset `validationInProgress` flag
                    if (uiState.isDobValid && validationInProgress) {
                        validationInProgress = false
                        navController.navigate(...) // Navigate to next screen
                    }
                }
        }

        return binding
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        outState.putBoolean(DOB_VALIDATION_KEY, validationInProgress)
    }
}
```

### Compose
```kotlin
class DobValidationViewModel(/* ... */) : ViewModel() {
    var uiState by mutableStateOf(DobValidationUiState())
        private set
}

@Composable
fun DobValidationScreen(
    onNavigateToNextScreen: () -> Unit, // Caller navigates to the right screen
    viewModel: DobValidationViewModel = viewModel()
) {
    // TextField that updates the ViewModel when a date of birth is selected

    var validationInProgress by rememberSaveable { mutableStateOf(false) }

    Button(
        onClick = {
            viewModel.validateInput()
            validationInProgress = true
        }
    ) {
        Text("Continue")
    }
    // Rest of the UI

    /*
     * The following code implements the requirement of advancing automatically
     * to the next screen when a valid date of birth has been introduced
     * and the user wanted to continue with the registration process.
     */

    if (validationInProgress) {
        val lifecycle = LocalLifecycleOwner.current.lifecycle
        val currentNavigateToNextScreen by rememberUpdatedState(onNavigateToNextScreen)
        LaunchedEffect(viewModel, lifecycle) {
            // If the date of birth is valid and the validation is in progress,
            // navigate to the next screen when `lifecycle` is at least STARTED,
            // which is the default Lifecycle.State for the `flowWithLifecycle` operator.
            snapshotFlow { viewModel.uiState }
                .filter { it.isDobValid }
                .flowWithLifecycle(lifecycle)
                .collect {
                    validationInProgress = false
                    currentNavigateToNextScreen()
                }
        }
    }
}
```

### The UI state production pipeline
```kotlin
@Composable
fun Counter() {
    // The UI state is managed by the UI itself
    var count by remember { mutableStateOf(0) }
    Row {
        Button(onClick = { ++count }) {
            Text(text = "Increment")
        }
        Button(onClick = { --count }) {
            Text(text = "Decrement")
        }
    }
}
```

### The UI state production pipeline
```kotlin
@Composable
fun ContactsList(contacts: List<Contact>) {
    val listState = rememberLazyListState()
    val isAtTopOfList by remember {
        derivedStateOf {
            listState.firstVisibleItemIndex < 3
        }
    }

    // Create the LazyColumn with the lazyListState
    ...

    // Show or hide the button (UI logic) based on the list scroll position
    AnimatedVisibility(visible = !isAtTopOfList) {
        ScrollToTopButton()
    }
}
```

### The UI state production pipeline
```kotlin
@Composable
fun UserProfileScreen(viewModel: UserProfileViewModel = hiltViewModel()) {
    // Read screen UI state from the business logic state holder
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    // Call on the UserAvatar Composable to display the photo
    UserAvatar(picture = uiState.profilePicture)
}
```

### The UI state production pipeline
```kotlin
@Composable
fun ContactsList(viewModel: ContactsViewModel = hiltViewModel()) {
    // Read screen UI state from the business logic state holder
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val contacts = uiState.contacts
    val deepLinkedContact = uiState.deepLinkedContact

    val listState = rememberLazyListState()

    // Create the LazyColumn with the lazyListState
    ...

    // Perform UI logic that depends on information from business logic
    if (deepLinkedContact != null && contacts.isNotEmpty()) {
        LaunchedEffect(listState, deepLinkedContact, contacts) {
            val deepLinkedContactIndex = contacts.indexOf(deepLinkedContact)
            if (deepLinkedContactIndex >= 0) {
              // Scroll to deep linked item
              listState.animateScrollToItem(deepLinkedContactIndex)
            }
        }
    }
}
```

### Business logic and its state holder
```kotlin
@HiltViewModel
class AuthorViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val authorsRepository: AuthorsRepository,
    newsRepository: NewsRepository
) : ViewModel() {

    val uiState: StateFlow<AuthorScreenUiState> = …

    // Business logic
    fun followAuthor(followed: Boolean) {
      …
    }
}
```

### UI logic and its state holder
```kotlin
@Stable
class NiaAppState(
    val navController: NavHostController,
    val windowSizeClass: WindowSizeClass
) {

    // UI logic
    val shouldShowBottomBar: Boolean
        get() = windowSizeClass.widthSizeClass == WindowWidthSizeClass.Compact ||
            windowSizeClass.heightSizeClass == WindowHeightSizeClass.Compact

    // UI logic
    val shouldShowNavRail: Boolean
        get() = !shouldShowBottomBar

   // UI State
    val currentDestination: NavDestination?
        @Composable get() = navController
            .currentBackStackEntryAsState().value?.destination

    // UI logic
    fun navigate(destination: NiaNavigationDestination, route: String? = null) { /* ... */ }

     /* ... */
}
```

### State holders are compoundable
```kotlin
@Stable
class DrawerState(/* ... */) {
  internal val swipeableState = SwipeableState(/* ... */)
  // ...
}

@Stable
class MyAppState(
  private val drawerState: DrawerState,
  private val navController: NavHostController
) { /* ... */ }

@Composable
fun rememberMyAppState(
  drawerState: DrawerState = rememberDrawerState(DrawerValue.Closed),
  navController: NavHostController = rememberNavController()
): MyAppState = remember(drawerState, navController) {
  MyAppState(drawerState, navController)
}
```

### State holders are compoundable
```kotlin
class MyScreenViewModel(/* ... */) {
  val uiState: StateFlow<MyScreenUiState> = /* ... */
  fun doSomething() { /* ... */ }
  fun doAnotherThing() { /* ... */ }
  // ...
}

@Stable
class MyScreenState(
  // DO NOT pass a ViewModel instance to a plain state holder class
  // private val viewModel: MyScreenViewModel,

  // Instead, pass only what it needs as a dependency
  private val someState: StateFlow<SomeState>,
  private val doSomething: () -> Unit,

  // Other UI-scoped types
  private val scaffoldState: ScaffoldState
) {
  /* ... */
}

@Composable
fun rememberMyScreenState(
  someState: StateFlow<SomeState>,
  doSomething: () -> Unit,
  scaffoldState: ScaffoldState = rememberScaffoldState()
): MyScreenState = remember(someState, doSomething, scaffoldState) {
  MyScreenState(someState, doSomething, scaffoldState)
}

@Composable
fun MyScreen(
  modifier: Modifier = Modifier,
  viewModel: MyScreenViewModel = viewModel(),
  state: MyScreenState = rememberMyScreenState(
    someState = viewModel.uiState.map { it.toSomeState() },
    doSomething = viewModel::doSomething
  ),
  // ...
) {
  /* ... */
}
```

### StateFlow
```kotlin
data class DiceUiState(
    val firstDieValue: Int? = null,
    val secondDieValue: Int? = null,
    val numberOfRolls: Int = 0,
)

class DiceRollViewModel : ViewModel() {

    private val _uiState = MutableStateFlow(DiceUiState())
    val uiState: StateFlow<DiceUiState> = _uiState.asStateFlow()

    // Called from the UI
    fun rollDice() {
        _uiState.update { currentState ->
            currentState.copy(
            firstDieValue = Random.nextInt(from = 1, until = 7),
            secondDieValue = Random.nextInt(from = 1, until = 7),
            numberOfRolls = currentState.numberOfRolls + 1,
            )
        }
    }
}
```

### Compose State
```kotlin
@Stable
interface DiceUiState {
    val firstDieValue: Int?
    val secondDieValue: Int?
    val numberOfRolls: Int?
}

private class MutableDiceUiState: DiceUiState {
    override var firstDieValue: Int? by mutableStateOf(null)
    override var secondDieValue: Int? by mutableStateOf(null)
    override var numberOfRolls: Int by mutableStateOf(0)
}

class DiceRollViewModel : ViewModel() {

    private val _uiState = MutableDiceUiState()
    val uiState: DiceUiState = _uiState

    // Called from the UI
    fun rollDice() {
        _uiState.firstDieValue = Random.nextInt(from = 1, until = 7)
        _uiState.secondDieValue = Random.nextInt(from = 1, until = 7)
        _uiState.numberOfRolls = _uiState.numberOfRolls + 1
    }
}
```

### StateFlow
```kotlin
data class AddEditTaskUiState(
    val title: String = "",
    val description: String = "",
    val isTaskCompleted: Boolean = false,
    val isLoading: Boolean = false,
    val userMessage: String? = null,
    val isTaskSaved: Boolean = false
)

class AddEditTaskViewModel(...) : ViewModel() {

   private val _uiState = MutableStateFlow(AddEditTaskUiState())
   val uiState: StateFlow<AddEditTaskUiState> = _uiState.asStateFlow()

   private fun createNewTask() {
        viewModelScope.launch {
            val newTask = Task(uiState.value.title, uiState.value.description)
            try {
                tasksRepository.saveTask(newTask)
                // Write data into the UI state.
                _uiState.update {
                    it.copy(isTaskSaved = true)
                }
            }
            catch(cancellationException: CancellationException) {
                throw cancellationException
            }
            catch(exception: Exception) {
                _uiState.update {
                    it.copy(userMessage = getErrorMessage(exception))
                }
            }
        }
    }
}
```

### Compose State
```kotlin
@Stable
interface AddEditTaskUiState {
    val title: String
    val description: String
    val isTaskCompleted: Boolean
    val isLoading: Boolean
    val userMessage: String?
    val isTaskSaved: Boolean
}

private class MutableAddEditTaskUiState : AddEditTaskUiState() {
    override var title: String by mutableStateOf("")
    override var description: String by mutableStateOf("")
    override var isTaskCompleted: Boolean by mutableStateOf(false)
    override var isLoading: Boolean by mutableStateOf(false)
    override var userMessage: String? by mutableStateOf<String?>(null)
    override var isTaskSaved: Boolean by mutableStateOf(false)
}

class AddEditTaskViewModel(...) : ViewModel() {

   private val _uiState = MutableAddEditTaskUiState()
   val uiState: AddEditTaskUiState = _uiState

   private fun createNewTask() {
        viewModelScope.launch {
            val newTask = Task(uiState.value.title, uiState.value.description)
            try {
                tasksRepository.saveTask(newTask)
                // Write data into the UI state.
                _uiState.isTaskSaved = true
            }
            catch(cancellationException: CancellationException) {
                throw cancellationException
            }
            catch(exception: Exception) {
                _uiState.userMessage = getErrorMessage(exception))
            }
        }
    }
}
```

### StateFlow
```kotlin
class DiceRollViewModel(
    private val defaultDispatcher: CoroutineScope = Dispatchers.Default
) : ViewModel() {

    private val _uiState = MutableStateFlow(DiceUiState())
    val uiState: StateFlow<DiceUiState> = _uiState.asStateFlow()

  // Called from the UI
  fun rollDice() {
        viewModelScope.launch() {
            // Other Coroutines that may be called from the current context
            …
            withContext(defaultDispatcher) {
                _uiState.update { currentState ->
                    currentState.copy(
                        firstDieValue = SlowRandom.nextInt(from = 1, until = 7),
                        secondDieValue = SlowRandom.nextInt(from = 1, until = 7),
                        numberOfRolls = currentState.numberOfRolls + 1,
                    )
                }
            }
        }
    }
}
```

### Stream APIs as sources of state change
```kotlin
class InterestsViewModel(
    authorsRepository: AuthorsRepository,
    topicsRepository: TopicsRepository
) : ViewModel() {

    val uiState = combine(
        authorsRepository.getAuthorsStream(),
        topicsRepository.getTopicsStream(),
    ) { availableAuthors, availableTopics ->
        InterestsUiState.Interests(
            authors = availableAuthors,
            topics = availableTopics
        )
    }
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = InterestsUiState.Loading
    )
}
```

### StateFlow
```kotlin
class TaskDetailViewModel @Inject constructor(
    private val tasksRepository: TasksRepository,
    savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val _isTaskDeleted = MutableStateFlow(false)
    private val _task = tasksRepository.getTaskStream(taskId)

    val uiState: StateFlow<TaskDetailUiState> = combine(
        _isTaskDeleted,
        _task
    ) { isTaskDeleted, task ->
        TaskDetailUiState(
            task = taskAsync.data,
            isTaskDeleted = isTaskDeleted
        )
    }
        // Convert the result to the appropriate observable API for the UI
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = TaskDetailUiState()
        )

    fun deleteTask() = viewModelScope.launch {
        tasksRepository.deleteTask(taskId)
        _isTaskDeleted.update { true }
    }
}
```

### State production pipeline initialization
```kotlin
class MyViewModel : ViewModel() {

    private var initializeCalled = false

    // This function is idempotent provided it is only called from the UI thread.
    @MainThread
    fun initialize() {
        if(initializeCalled) return
        initializeCalled = true

        viewModelScope.launch {
            // seed the state production pipeline
        }
    }
}
```

### Dependencies
```kotlin
class GetLatestNewsWithAuthorsUseCase(
  private val newsRepository: NewsRepository,
  private val authorsRepository: AuthorsRepository
) { /* ... */ }
```

### Call use cases in Kotlin
```kotlin
class FormatDateUseCase(userRepository: UserRepository) {

    private val formatter = SimpleDateFormat(
        userRepository.getPreferredDateFormat(),
        userRepository.getPreferredLocale()
    )

    operator fun invoke(date: Date): String {
        return formatter.format(date)
    }
}
```

### Call use cases in Kotlin
```kotlin
class MyViewModel(formatDateUseCase: FormatDateUseCase) : ViewModel() {
    init {
        val today = Calendar.getInstance()
        val todaysDate = formatDateUseCase(today)
        /* ... */
    }
}
```

### Threading
```kotlin
class MyUseCase(
    private val defaultDispatcher: CoroutineDispatcher = Dispatchers.Default
) {

    suspend operator fun invoke(...) = withContext(defaultDispatcher) {
        // Long-running blocking operations happen on a background thread.
    }
}
```

### Combine repositories
```kotlin
/**
 * This use case fetches the latest news and the associated author.
 */
class GetLatestNewsWithAuthorsUseCase(
  private val newsRepository: NewsRepository,
  private val authorsRepository: AuthorsRepository,
  private val defaultDispatcher: CoroutineDispatcher = Dispatchers.Default
) {
    suspend operator fun invoke(): List<ArticleWithAuthor> =
        withContext(defaultDispatcher) {
            val news = newsRepository.fetchLatestNews()
            val result: MutableList<ArticleWithAuthor> = mutableListOf()
            // This is not parallelized, the use case is linearly slow.
            for (article in news) {
                // The repository exposes suspend functions
                val author = authorsRepository.getAuthor(article.authorId)
                result.add(ArticleWithAuthor(article, author))
            }
            result
        }
}
```

### Data layer architecture
```kotlin
class ExampleRepository(
    private val exampleRemoteDataSource: ExampleRemoteDataSource, // network
    private val exampleLocalDataSource: ExampleLocalDataSource // database
) { /* ... */ }
```

### Represent business models
```kotlin
data class ArticleApiModel(
    val id: Long,
    val title: String,
    val content: String,
    val publicationDate: Date,
    val modifications: Array<ArticleApiModel>,
    val comments: Array<CommentApiModel>,
    val lastModificationDate: Date,
    val authorId: Long,
    val authorName: String,
    val authorDateOfBirth: Date,
    val readTimeMin: Int
)
```

### Represent business models
```kotlin
data class Article(
    val id: Long,
    val title: String,
    val content: String,
    val publicationDate: Date,
    val authorName: String,
    val readTimeMin: Int
)
```

### Create the data source
```kotlin
class NewsRemoteDataSource(
  private val newsApi: NewsApi,
  private val ioDispatcher: CoroutineDispatcher
) {
    /**
     * Fetches the latest news from the network and returns the result.
     * This executes on an IO-optimized thread pool, the function is main-safe.
     */
    suspend fun fetchLatestNews(): List<ArticleHeadline> =
        // Move the execution to an IO-optimized thread since the ApiService
        // doesn't support coroutines and makes synchronous requests.
        withContext(ioDispatcher) {
            newsApi.fetchLatestNews()
        }
    }

// Makes news-related network synchronous requests.
interface NewsApi {
    fun fetchLatestNews(): List<ArticleHeadline>
}
```

### Create the repository
```kotlin
// NewsRepository is consumed from other layers of the hierarchy.
class NewsRepository(
    private val newsRemoteDataSource: NewsRemoteDataSource
) {
    suspend fun fetchLatestNews(): List<ArticleHeadline> =
        newsRemoteDataSource.fetchLatestNews()
}
```

### Cache the result of the network request
```kotlin
class NewsRepository(
  private val newsRemoteDataSource: NewsRemoteDataSource
) {
    // Mutex to make writes to cached values thread-safe.
    private val latestNewsMutex = Mutex()

    // Cache of the latest news got from the network.
    private var latestNews: List<ArticleHeadline> = emptyList()

    suspend fun getLatestNews(refresh: Boolean = false): List<ArticleHeadline> {
        if (refresh || latestNews.isEmpty()) {
            val networkResult = newsRemoteDataSource.fetchLatestNews()
            // Thread-safe write to latestNews
            latestNewsMutex.withLock {
                this.latestNews = networkResult
            }
        }

        return latestNewsMutex.withLock { this.latestNews }
    }
}
```

### Make an operation live longer than the screen
```kotlin
class NewsRepository(
    ...,
    // This could be CoroutineScope(SupervisorJob() + Dispatchers.Default).
    private val externalScope: CoroutineScope
) { ... }
```

### Make an operation live longer than the screen
```kotlin
class NewsRepository(
    private val newsRemoteDataSource: NewsRemoteDataSource,
    private val externalScope: CoroutineScope
) {
    /* ... */

    suspend fun getLatestNews(refresh: Boolean = false): List<ArticleHeadline> {
        return if (refresh) {
            externalScope.async {
                newsRemoteDataSource.fetchLatestNews().also { networkResult ->
                    // Thread-safe write to latestNews.
                    latestNewsMutex.withLock {
                        latestNews = networkResult
                    }
                }
            }.await()
        } else {
            return latestNewsMutex.withLock { this.latestNews }
        } 
    }
}
```

### Schedule tasks using WorkManager
```kotlin
class RefreshLatestNewsWorker(
    private val newsRepository: NewsRepository,
    context: Context,
    params: WorkerParameters
) : CoroutineWorker(context, params) {

    override suspend fun doWork(): Result = try {
        newsRepository.refreshLatestNews()
        Result.success()
    } catch (error: Throwable) {
        Result.failure()
    }
}
```

### Schedule tasks using WorkManager
```kotlin
private const val REFRESH_RATE_HOURS = 4L
private const val FETCH_LATEST_NEWS_TASK = "FetchLatestNewsTask"
private const val TAG_FETCH_LATEST_NEWS = "FetchLatestNewsTaskTag"

class NewsTasksDataSource(
    private val workManager: WorkManager
) {
    fun fetchNewsPeriodically() {
        val fetchNewsRequest = PeriodicWorkRequestBuilder<RefreshLatestNewsWorker>(
            REFRESH_RATE_HOURS, TimeUnit.HOURS
        ).setConstraints(
            Constraints.Builder()
                .setRequiredNetworkType(NetworkType.TEMPORARILY_UNMETERED)
                .setRequiresCharging(true)
                .build()
        )
            .addTag(TAG_FETCH_LATEST_NEWS)

        workManager.enqueueUniquePeriodicWork(
            FETCH_LATEST_NEWS_TASK,
            ExistingPeriodicWorkPolicy.KEEP,
            fetchNewsRequest.build()
        )
    }

    fun cancelFetchingNewsPeriodically() {
        workManager.cancelAllWorkByTag(TAG_FETCH_LATEST_NEWS)
    }
}
```

### Exposing resources
```
data/
├─ local/
│ ├─ entities/
│ │ ├─ AuthorEntity
│ ├─ dao/
│ ├─ NiADatabase
├─ network/
│ ├─ NiANetwork
│ ├─ models/
│ │ ├─ NetworkAuthor
├─ model/
│ ├─ Author
├─ repository/
```

### Exposing resources
```kotlin
/**
 * Network representation of [Author]
 */
@Serializable
data class NetworkAuthor(
    val id: String,
    val name: String,
    val imageUrl: String,
    val twitter: String,
    val mediumPage: String,
    val bio: String,
)

/**
 * Defines an author for either an [EpisodeEntity] or [NewsResourceEntity].
 * It has a many-to-many relationship with both entities
 */
@Entity(tableName = "authors")
data class AuthorEntity(
    @PrimaryKey
    val id: String,
    val name: String,
    @ColumnInfo(name = "image_url")
    val imageUrl: String,
    @ColumnInfo(defaultValue = "")
    val twitter: String,
    @ColumnInfo(name = "medium_page", defaultValue = "")
    val mediumPage: String,
    @ColumnInfo(defaultValue = "")
    val bio: String,
)
```

### Exposing resources
```kotlin
/**
 * External data layer representation of a "Now in Android" Author
 */
data class Author(
    val id: String,
    val name: String,
    val imageUrl: String,
    val twitter: String,
    val mediumPage: String,
    val bio: String,
)
```

### Exposing resources
```kotlin
/**
 * Converts the network model to the local model for persisting
 * by the local data source
 */
fun NetworkAuthor.asEntity() = AuthorEntity(
    id = id,
    name = name,
    imageUrl = imageUrl,
    twitter = twitter,
    mediumPage = mediumPage,
    bio = bio,
)

/**
 * Converts the local model to the external model for use
 * by layers external to the data layer
 */
fun AuthorEntity.asExternalModel() = Author(
    id = id,
    name = name,
    imageUrl = imageUrl,
    twitter = twitter,
    mediumPage = mediumPage,
    bio = bio,
)
```

### Reads
```kotlin
class OfflineFirstTopicsRepository(
    private val topicDao: TopicDao,
    private val network: NiaNetworkDataSource,
) : TopicsRepository {

    override fun getTopicsStream(): Flow<List<Topic>> =
        topicDao.getTopicEntitiesStream()
            .map { it.map(TopicEntity::asExternalModel) }
}
```

### Local data source
```kotlin
class AuthorViewModel(
    authorsRepository: AuthorsRepository,
    ...
) : ViewModel() {
   private val authorId: String = ...

   // Observe author information
    private val authorStream: Flow<Author> =
        authorsRepository.getAuthorStream(
            id = authorId
        )
        .catch { emit(Author.empty()) }
}
```

### Writes
```kotlin
interface UserDataRepository {
    /**
     * Updates the bookmarked status for a news resource
     */
    suspend fun updateNewsResourceBookmark(newsResourceId: String, bookmarked: Boolean)
}
```

### Pull-based synchronization
```kotlin
class FeedRepository(...) {

    fun feedPagingSource(): PagingSource<FeedItem> { ... }
}

class FeedViewModel(
    private val repository: FeedRepository
) : ViewModel() {
    private val pager = Pager(
        config = PagingConfig(
            pageSize = NETWORK_PAGE_SIZE,
            enablePlaceholders = false
        ),
        remoteMediator = FeedRemoteMediator(...),
        pagingSourceFactory = feedRepository::feedPagingSource
    )

    val feedPagingData = pager.flow
}
```

### Push-based synchronization
```kotlin
class UserDataRepository(...) {

    suspend fun synchronize() {
        val userData = networkDataSource.fetchUserData()
        localDataSource.saveUserData(userData)
    }
}
```

### WorkManager in offline-first apps
```kotlin
class SyncInitializer : Initializer<Sync> {
   override fun create(context: Context): Sync {
       WorkManager.getInstance(context).apply {
           // Queue sync on app startup and ensure only one
           // sync worker runs at any time
           enqueueUniqueWork(
               SyncWorkName,
               ExistingWorkPolicy.KEEP,
               SyncWorker.startUpSyncWork()
           )
       }
       return Sync
   }
}
```

### WorkManager in offline-first apps
```kotlin
/**
 Create a WorkRequest to call the SyncWorker using a DelegatingWorker.
 This allows for dependency injection into the SyncWorker in a different
 module than the app module without having to create a custom WorkManager
 configuration.
*/
fun startUpSyncWork() = OneTimeWorkRequestBuilder<DelegatingWorker>()
    // Run sync as expedited work if the app is able to.
    // If not, it runs as regular work.
   .setExpedited(OutOfQuotaPolicy.RUN_AS_NON_EXPEDITED_WORK_REQUEST)
   .setConstraints(SyncConstraints)
    // Delegate to the SyncWorker.
   .setInputData(SyncWorker::class.delegatedData())
   .build()

val SyncConstraints
   get() = Constraints.Builder()
       .setRequiredNetworkType(NetworkType.CONNECTED)
       .build()
```

### WorkManager in offline-first apps
```kotlin
class SyncWorker(...) : CoroutineWorker(appContext, workerParams), Synchronizer {

    override suspend fun doWork(): Result = withContext(ioDispatcher) {
        // First sync the repositories in parallel
        val syncedSuccessfully = awaitAll(
            async { topicRepository.sync() },
            async { authorsRepository.sync() },
            async { newsRepository.sync() },
        ).all { it }

        if (syncedSuccessfully) Result.success()
        else Result.retry()
    }
}
```

## Pitfalls
- Note: The specific StateFlow objects used in this example don't stop
performing work when they have no active collectors, but when you're working
with flows you might not know how they're implemented. Using lifecycle-aware
flow collection lets you make these kinds of changes to the ViewModel flows
l
- Warning: It's bad practice to pass the ViewModel into the RecyclerView adapter
because that tightly couples the adapter with the ViewModel class.
  WHY: that tightly couples the adapter with the ViewModel class
- Note: In some apps, you might have seen ViewModel events being
 exposed to the UI using
 Kotlin
 Channels or other reactive streams. When the producer (the ViewModel)
 outlives the consumer (UI—Compose or Views), these solutions don't guarantee
 the delivery and processing of those events. This can
- Warning: Don't pass ViewModel instances down to other composable functions.
Doing so couples the composable function with the ViewModel type, making it less
reusable and harder to test and preview. Also, there would be no clear single
source of truth (SSOT) that manages the ViewModel instance. Passi
- Note: If ViewModel benefits don't apply to your use case or you do things in a
different way you can move ViewModel's responsibilities into plain state holder
classes.
- Caution: Given that screen level state holders manage the business logic
complexity of a screen or part of it, it wouldn't make sense a screen level
state holder depends on another screen level state holder. If you're in this
scenario, reconsider your screens and state holders and ensure that's what
- Warning: Updating Compose state from a non UI thread without using
 Snapshot.withMutableSnapshot{ } may cause inconsistencies in the state
produced.
- Warning: Avoid launching asynchronous operations in the init block or
constructor of a ViewModel . Asynchronous operations shouldn't be a side
effect of creating an object because the asynchronous code may
read from or write to the object before it is fully initialized. This is also
referred to as l
- Note: The term "domain layer" is used in other software architectures, such as
"clean" architecture, and has a different meaning there. Don't confuse the
definition of "domain layer" defined in the Android official architecture
guidance with other definitions you may have read elsewhere. There may b
- Note: Often, when a repository only contains a single data source and
doesn't depend on other repositories, developers merge the responsibilities of
repositories and data sources into the repository class. If you do this, don't
forget to split functionalities if the repository needs to handle data f
- Note: Another way to model the result of interactions with the data layer is by
using a Result class. This pattern models errors and other signals that can
happen as part of processing the result. In this pattern, the data layer returns
a Result<T> type instead of T , making the UI aware of known er
- Note: Mappers like the above often map between models defined in different
modules. As a result, it's often beneficial to define these mappers in the
modules where they are used to avoid tightly coupled modules. See the
 modularization guide for more details.
- Note: Writing data in offline-first apps often requires more consideration than
reading data because of potential conflicts. Offline-first apps don't need to be
able to write data when offline to be considered offline-first.
  WHY: of potential conflicts

## Decision Tables
### Layered architecture
| Recommendation | Description |
| --- | --- |
| Use a clearly defined data layer .
 Strongly recommended | The data layer exposes application data to the rest of the app and contains the vast majority of business logic of your app.
 
 You should create repositories even if they just contain a single data source. 
 In small apps, you can choose to place data layer types in a data package or module. |
| Use a clearly defined UI layer .
 Strongly recommended | The UI layer displays the application data on the screen and serves as the primary point of user interaction.
 
 In small apps, you can choose to place data layer types in a ui package or module. 
 

 More UI layer best practices here . |
| The data layer should expose application data using a repository.
 Strongly recommended | Components in the UI layer such as composables, activities, or ViewModels shouldn't interact directly with a data source.
Examples of data sources are: 
 
 Databases, DataStore, SharedPreferences, Firebase APIs. 
 GPS location providers. 
 Bluetooth data providers. 
 Network connectivity status provider. |
| Use coroutines and flows .
 Strongly recommended | Use coroutines and flows to communicate between layers.
 More coroutines best practices here . |
| Use a domain layer .
 Recommended in big apps | Use a domain layer , use cases, if you need to reuse business logic that interacts with the data layer across multiple ViewModels, or you want to simplify the business logic complexity of a particular ViewModel |

### UI layer
| Recommendation | Description |
| --- | --- |
| Follow Unidirectional Data Flow (UDF) .
 Strongly recommended | Follow Unidirectional Data Flow (UDF) principles, where ViewModels expose UI state using the observer pattern and receive actions from the UI through method calls. |
| Use AAC ViewModels if their benefits apply to your app.
 Strongly recommended | Use AAC ViewModels to handle business logic , and fetch application data to expose UI state to the UI (Compose or Android Views).
 See more ViewModel best practices here. 
 See the benefits of ViewModels here. |
| Use lifecycle-aware UI state collection.
 Strongly recommended | Collect UI state from the UI using the appropriate lifecycle-aware coroutine builder: repeatOnLifecycle in the View system and collectAsStateWithLifecycle in Jetpack Compose.
 Read more about repeatOnLifecycle . 
 Read more about about collectAsStateWithLifecycle . |
| Do not send events from the ViewModel to the UI.
 Strongly recommended | Process the event immediately in the ViewModel and cause a state update with the result of handling the event.
More about UI events here . |
| Use a single-activity application.
 Recommended | Use Navigation Fragments or Navigation Compose to navigate between screens and deep link to your app if your app has more than one screen. |
| Use Jetpack Compose .
 Recommended | Use Jetpack Compose to build new apps for phones, tablets and foldables and Wear OS. |

### ViewModel
| Recommendation | Description |
| --- | --- |
| ViewModels should be agnostic of the Android lifecycle.
 Strongly recommended | ViewModels shouldn't hold a reference to any Lifecycle-related type. Don't pass Activity, Fragment, Context or Resources as a dependency.
If something needs a Context in the ViewModel, you should strongly evaluate if that is in the right layer. |
| Use coroutines and flows .
 Strongly recommended | The ViewModel interacts with the data or domain layers using: 
 
 Kotlin flows for receiving application data, 
 suspend functions to perform actions using viewModelScope . |
| Use ViewModels at screen level.
 Strongly recommended | Do not use ViewModels in reusable pieces of UI. You should use ViewModels in: 
 
 Screen-level composables, 
 Activities/Fragments in Views, 
 Destinations or graphs when using Jetpack Navigation . |
| Use plain state holder classes in reusable UI components.
 Strongly recommended | Use plain state holder classes for handling complexity in reusable UI components. By doing this, the state can be hoisted and controlled externally. |
| Do not use AndroidViewModel .
 Recommended | Use the ViewModel class, not AndroidViewModel . The Application class shouldn't be used in the ViewModel. Instead, move the dependency to the UI or the data layer. |
| Expose a UI state.
 Recommended | ViewModels should expose data to the UI through a single property called uiState . If the UI shows multiple, unrelated pieces of data, the VM can expose multiple UI state properties .
 
 You should make uiState a StateFlow . 
 You should create the uiState using the stateIn operator with the WhileSubscribed(5000) policy (example) if the data comes as a stream of data from other layers of the hierarchy. 
 For simpler cases with no streams of data coming from the data layer, it's acceptable to use a MutableStateFlow exposed as an immutable StateFlow (example) . 
 You can choose to have the ${Screen}UiState as a data class that can contain data, errors and loading signals. This class could also be a sealed class if the different states are exclusive. |

### Lifecycle
| Recommendation | Description |
| --- | --- |
| Do not override lifecycle methods in Activities or Fragments.
 Strongly recommended | Do not override lifecycle methods such as onResume in Activities or Fragments. Use LifecycleObserver instead. If the app needs to perform work when the lifecycle reaches a certain Lifecycle.State , use the repeatOnLifecycle API. |

### Handle dependencies
| Recommendation | Description |
| --- | --- |
| Use dependency injection .
 Strongly recommended | Use dependency injection best practices, mainly constructor injection when possible. |
| Scope to a component when necessary.
 Strongly recommended | Scope to a dependency container when the type contains mutable data that needs to be shared or the type is expensive to initialize and is widely used in the app. |
| Use Hilt .
 Recommended | Use Hilt or manual dependency injection in simple apps. Use Hilt if your project is complex enough. For example, if you have:
 
 Multiple screens with ViewModels—integration 
 WorkManager usage—integration 
 Advance usage of Navigation, such as ViewModels scoped to the nav graph—integration. |

### Testing
| Recommendation | Description |
| --- | --- |
| Know what to test .
 Strongly recommended | Unless the project is roughly as simple as a hello world app, you should test it, at minimum with: 
 
 Unit test ViewModels, including Flows. 
 Unit test data layer entities. That is, repositories and data sources. 
 UI navigation tests that are useful as regression tests in CI. |
| Prefer fakes to mocks.
 Strongly recommended | Read more in the Use test doubles in Android documentation . |
| Test StateFlows.
 Strongly recommended | When testing StateFlow :
 
 Assert on the value property whenever possible 
 You should create a collectJob if using WhileSubscribed |

### Models
| Recommendation | Description |
| --- | --- |
| Create a model per layer in complex apps.
 Recommended | In complex apps, create new models in different layers or components when it makes sense. Consider the following examples: 
 
 A remote data source can map the model that it receives through the network to a simpler class with just the data the app needs 
 Repositories can map DAO models to simpler data classes with just the information the UI layer needs. 
 ViewModel can include data layer models in UiState classes. |

### Naming conventions
| Recommendation | Description |
| --- | --- |
| Naming methods.
 Optional | Methods should be a verb phrase. For example, makePayment() . |
| Naming properties.
 Optional | Properties should be a noun phrase. For example, inProgressTopicSelection . |
| Naming streams of data.
 Optional | When a class exposes a Flow stream, LiveData, or any other stream, the naming convention is get{model}Stream() . For example, getAuthorStream(): Flow<Author> 
 If the function returns a list of models the model name should be in the plural: getAuthorsStream(): Flow<List<Author>> |
| Naming interfaces implementations.
 Optional | Names for the implementations of interfaces should be meaningful. Have Default as the prefix if a better name cannot be found. For example, for a NewsRepository interface, you could have an OfflineFirstNewsRepository , or InMemoryNewsRepository . If you can find no good name, then use DefaultNewsRepository .
 Fake implementations should be prefixed with Fake , as in FakeAuthorsRepository . |

### Android lifecycle and the types of UI state and logic
| UI Lifecycle independent | UI Lifecycle dependent |
| --- | --- |
| Business logic | UI Logic |
| Screen UI state |  |

### Business logic and its state holder
| Property | Detail |
| --- | --- |
| Produces UI State | Business logic state holders are responsible for producing the UI state for their UIs. This UI state is often the result of processing user events and reading data from the domain and data layers. |
| Retained through activity recreation | Business logic state holders retain their state and state processing pipelines across Activity recreation, helping provide a seamless user experience. In the cases where the state holder is unable to be retained and is recreated (usually after process death ), the state holder must be able to easily recreate its last state to ensure a consistent user experience. |
| Possess long lived state | Business logic state holders are often used to manage state for navigation destinations. As a result, they often preserve their state across navigation changes until they are removed from the navigation graph. |
| Is unique to its UI and is not reusable | Business logic state holders typically produce state for a certain app function, for example a TaskEditViewModel or a TaskListViewModel , and therefore only ever applicable to that app function. The same state holder can support these app functions across different form factors. For example, mobile, TV, and tablet versions of the app may reuse the same business logic state holder. |

### UI State production 

 
 
 
 

 
 
 Stay organized with collections
 
 
 
 Save and categorize content based on your preferences.
| Events | State |
| --- | --- |
| Transient, unpredictable, and exist for a finite period. | Always exists. |
| The inputs of state production. | The output of state production. |
| The product of the UI or other sources. | Is consumed by the UI. |

### State production APIs
| Pipeline stage | API |
| --- | --- |
| Input | You should use asynchronous APIs to perform work off the UI thread to keep the UI jank free.
For example, Coroutines or Flows in Kotlin, and RxJava or callbacks in the Java Programming Language. |
| Output | You should use observable data holder APIs to invalidate and rerender the UI when state changes.
For example, StateFlow, Compose State, or LiveData. Observable data holders guarantee the UI always has a UI state to display on the screen |

### Output types in state production pipelines
| Input | Consumer | Output |
| --- | --- | --- |
| One-shot APIs | Views | StateFlow or LiveData |
| One-shot APIs | Compose | StateFlow or Compose State |
| Stream APIs | Views | StateFlow or LiveData |
| Stream APIs | Compose | StateFlow |
| One-shot and stream APIs | Views | StateFlow or LiveData |
| One-shot and stream APIs | Compose | StateFlow |

### Pull-based synchronization
| Advantages | Disadvantages |
| --- | --- |
| Relatively easy to implement. | Prone to heavy data use. This is because repeated visits to a navigation destination triggers unnecessary refetching of unchanged information. You can mitigate this through proper caching. This can be done in the UI layer with the cachedIn operator, or in the network layer with a HTTP cache. |
| Data that is not needed will never be fetched. | Does not scale well with relational data since the model pulled needs to be self sufficient. If the model being synchronized depends on other models to be fetched to populate itself, the heavy data use problem mentioned earlier will be made even more significant. Furthermore, it may cause dependencies between repositories of the parent model and repositories of the nested model. |

### Push-based synchronization
| Advantages | Disadvantages |
| --- | --- |
| The app can remain offline indefinitely. | Versioning data for conflict resolution is non-trivial. |
| Minimum data use. The app only fetches data that has changed. | You need to take into consideration write concerns during synchronization. |
| Works well for relational data. Each repository is only responsible for fetching data for the model it supports. | The network data source needs to support synchronization. |

## Guidelines
- The user interface of an app is also a component. Historically, UIs were built
using multiple activities . However, modern apps use a
single-activity architecture. A single Activity serves as a container for
screens implemented as fragments or Jetpack Compose destinations.
- In a resource-constrained environment, the components of your app can be
launched individually and out of order; what's more, the operating system or
user can destroy them at any time. As a result, don't store any application data
or state in your app components. Your app components should be self-contained,
independent of each other.
- If you can't use app components to store application data and state, how
should you design your app?
- As Android apps grow in size, it's important to define an architecture that
allows the app to scale. A well-designed app architecture defines the boundaries
between parts of the app and the responsibilities each part should have.
- This ephemeral nature makes them unsuitable for holding application data or
state. If you store data in an Activity or Fragment , that data is lost when
the component is recreated. To ensure data persistence and provide a stable user
experience, don't entrust state to these UI components.
- Your app should gracefully handle configuration changes, such as device
 orientation changes or changes in the size of the app window.
Implement the adaptive canonical layouts to provide an
optimal user experience on a variety of form factors.
- Another important principle is that you should drive your UI from data models,
preferably persistent models. Data models represent the data of an app. They're
independent from the UI elements and other components in your app. This means
that they are not tied to the UI and app component lifecycle but will still be
destroyed when the OS removes the app's process from memory.
- When a new data type is defined in your app, you should assign a single source
of truth (SSOT) to it. The SSOT is the owner of that data, and only the SSOT
can modify or mutate it. To achieve this, the SSOT exposes the data using an
immutable type; to modify the data, the SSOT exposes functions or receives
events that other types can call.
- Considering common architectural principles, each application should have at
least two layers:
- The role of the UI layer (or presentation layer ) is to display the application
data on screen. Whenever the data changes, either due to user interaction
(such as pressing a button) or external input (such as a network response), the
UI should update to reflect the changes.
- The data layer is made up of repositories each of which can contain zero to many
data sources. You should create a repository class for each different type of
data you handle in your app. For example, you might create a MoviesRepository 
class for data related to movies or a PaymentsRepository class for data
related to payments.
- Each data source class should have the responsibility of working with only one
source of data, which can be a file, a network source, or a local database.
Data-source classes are the bridge between the application and the system for
data operations.
- The domain layer is responsible for encapsulating complex business logic or
simpler business logic that is reused by multiple view models. The domain layer
is optional because not all apps have these requirements. Use it only when
needed, for example, to handle complexity or favor reusability.
- Classes in the domain layer are commonly called use cases or interactors .
Each use case should have responsibility for a single functionality. For
example, your app could have a GetTimeZoneUseCase class if multiple view
models rely on time zones to display the proper message on the screen.
- Classes in your app depend on other classes to function properly. You can use
either of the following design patterns to gather the dependencies of a
particular class:
- Key Point: Use the dependency injection pattern and the Hilt library in
Android apps. Hilt automatically constructs objects by walking the dependency
tree, provides compile-time verification of dependencies, and creates dependency
containers for Android framework classes.
- Your app components should be the only classes that rely on Android framework
SDK APIs such as Context or Toast . Abstracting other classes in your
app away from the app components helps with testability and reduces
 coupling within your app.
- The Jetpack Compose libraries provide robust APIs for building adaptive user
interfaces. Use the canonical layouts in your app to
optimize the user experience on multiple form factors and display sizes. Review
the gallery of app design patterns to select the layouts that work
best for your use cases.
- When designing for adaptive layouts, preserve UI state across configuration
changes such as display resizing, folding, and orientation changes. Your
architecture should verify that the user's current state is maintained,
providing a seamless experience.
- Consider how to make each part of your app testable in isolation.

## Concepts (for graph)
- App composition
- Multiple form factors
- Resource constraints
- Variable launch conditions
- Common architectural principles
- Separation of concerns
- Adaptive layouts
- Drive UI from data models
- Single source of truth
- Unidirectional data flow
- Recommended app architecture
- UI layer:
