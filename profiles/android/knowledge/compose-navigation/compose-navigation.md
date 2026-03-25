<!-- Source: https://developer.android.com/develop/ui/compose/navigation?hl=en -->
<!-- Type: official -->
<!-- Priority: high -->
<!-- Topic: compose-navigation -->
<!-- Extracted: 2026-03-24 -->
<!-- Verified: — -->

# Navigation with Compose

## Rules
- DO: Pass lambdas that should be triggered by the composable to navigate, rather
than the NavController itself.

## Code Patterns
### Setup
```kotlin
dependencies {
    val nav_version = "2.9.7"

    implementation("androidx.navigation:navigation-compose:$nav_version")
}
```

### Retrieve complex data when navigating
```
// Pass only the user ID when navigating to a new destination as argument
navController.navigate(Profile(id = "user1234"))
```

### Retrieve complex data when navigating
```kotlin
class UserViewModel(
    savedStateHandle: SavedStateHandle,
    private val userInfoRepository: UserInfoRepository
) : ViewModel() {

    private val profile = savedStateHandle.toRoute<Profile>()

    // Fetch the relevant user information from the data layer,
    // ie. userInfoRepository, based on the passed userId argument
    private val userInfo: Flow<UserInfo> = userInfoRepository.getUserInfo(profile.id)

// …

}
```

### Deep links
```kotlin
@Serializable data class Profile(val id: String)
val uri = "https://www.example.com"

composable<Profile>(
  deepLinks = listOf(
    navDeepLink<Profile>(basePath = "$uri/profile")
  )
) { backStackEntry ->
  ProfileScreen(id = backStackEntry.toRoute<Profile>().id)
}
```

### Deep links
```xml
<activity …>
  <intent-filter>
    ...
    <data android:scheme="https" android:host="www.example.com" />
  </intent-filter>
</activity>
```

### Deep links
```kotlin
val id = "exampleId"
val context = LocalContext.current
val deepLinkIntent = Intent(
    Intent.ACTION_VIEW,
    "https://www.example.com/profile/$id".toUri(),
    context,
    MyActivity::class.java
)

val deepLinkPendingIntent: PendingIntent? = TaskStackBuilder.create(context).run {
    addNextIntentWithParentStack(deepLinkIntent)
    getPendingIntent(0, PendingIntent.FLAG_UPDATE_CURRENT)
}
```

### Navigate from Compose with Navigation for fragments
```kotlin
@Composable
fun MyScreen(onNavigate: (Int) -> Unit) {
    Button(onClick = { onNavigate(R.id.nav_profile) } { /* ... */ }
}
```

### Navigate from Compose with Navigation for fragments
```kotlin
override fun onCreateView( /* ... */ ) {
    setContent {
        MyScreen(onNavigate = { dest -> findNavController().navigate(dest) })
    }
}
```

### Testing
```kotlin
@Composable
fun ProfileScreen(
    userId: String,
    navigateToFriendProfile: (friendUserId: String) -> Unit
) {
 …
}
```

### Testing
```kotlin
@Serializable data class Profile(id: String)

composable<Profile> { backStackEntry ->
    val profile = backStackEntry.toRoute<Profile>()
    ProfileScreen(userId = profile.id) { friendUserId ->
        navController.navigate(route = Profile(id = friendUserId))
    }
}
```

### Testing the NavHost
```
dependencies {
// ...
  androidTestImplementation "androidx.navigation:navigation-testing:$navigationVersion"
  // ...
}
```

### Testing the NavHost
```kotlin
@Composable
fun AppNavHost(navController: NavHostController){
  NavHost(navController = navController){ ... }
}
```

### Testing the NavHost
```kotlin
class NavigationTest {

    @get:Rule
    val composeTestRule = createComposeRule()
    lateinit var navController: TestNavHostController

    @Before
    fun setupAppNavHost() {
        composeTestRule.setContent {
            navController = TestNavHostController(LocalContext.current)
            navController.navigatorProvider.addNavigator(ComposeNavigator())
            AppNavHost(navController = navController)
        }
    }

    // Unit test
    @Test
    fun appNavHost_verifyStartDestination() {
        composeTestRule
            .onNodeWithContentDescription("Start Screen")
            .assertIsDisplayed()
    }
}
```

### Testing navigation actions
```kotlin
@Test
fun appNavHost_clickAllProfiles_navigateToProfiles() {
    composeTestRule.onNodeWithContentDescription("All Profiles")
        .performScrollTo()
        .performClick()

    assertTrue(navController.currentBackStackEntry?.destination?.hasRoute<Profile>() ?: false)
}
```

## Guidelines
- To support Compose, use the following dependency in your app module's
 build.gradle file:
- Note: When designing your navigation graph, consider how navigation flows will
adapt to different display sizes and form factors.
- For a more in depth explanation on why you should avoid passing complex data as
arguments, as well as a list of supported argument types, see Pass data between
destinations .
- NavigationSuiteScaffold handles primary navigation; however, adaptive layouts
often involve other specialized composables. For the list-detail and supporting
pane canonical layouts, which are common in adaptive designs, use
 ListDetailPaneScaffold and SupportingPaneScaffold , respectively.
For more information, see Build adaptive layouts .
- If you want to use the Navigation component with Compose, you have two options:
- Therefore, the recommendation for mixed Compose and Views apps is to use the
Fragment-based Navigation component. Fragments will then hold View-based
screens, Compose screens, and screens that use both Views and Compose. Once each
Fragment's contents are in Compose, the next step is to tie all of those screens
together with Navigation Compose and remove all of the Fragments.
- This means that you shouldn't pass the navController directly into any
composable and instead pass navigation callbacks as parameters. This allows
all your composables to be individually testable, as they don't require an
instance of navController in tests.
- As you want to test your concrete app's implementation, clicks on the UI are
preferable. To learn how to test this alongside individual composable functions
in isolation, make sure to check out the Testing in Jetpack Compose 
codelab.
- You also can use the navController to check your assertions by comparing the
current route to the expected one, using navController 's
 currentBackStackEntry :

## Core Concepts

1. **Navigation via Lambdas**
   - Evidence: The rule explicitly mentions passing navigation logic as lambdas rather than `NavController` itself to ensure composables are testable and reusable.
2. **Retrieving Complex Data When Navigating**
   - Evidence: Multiple code examples illustrate how complex data, such as user information from a repository, is retrieved based on arguments passed via lambda functions or SavedStateHandle within ViewModel layers.
3. **Deep Links Integration**
   - Evidence: Sections provide detailed instructions and examples for setting up deep links using URI patterns to ensure seamless integration with Compose navigation.

## Mental Model

- **The Problem**: Without proper handling of navigation via lambdas, composables would be tightly coupled with `NavController`, making them less testable and reusable.
- **Core Insight**: The key insight is that passing `NavController` directly into composables should be avoided in favor of passing lambda callbacks to handle navigation. This approach ensures composables remain independent and agnostic of specific instances of `NavController`.
  
- **How concepts connect**:
  - Navigation via Lambdas → Retrieving Complex Data When Navigating: Using lambdas for navigation allows composables to remain agnostic of complex data retrieval, which can be handled within the ViewModel layer.
  - Retrieving Complex Data When Navigating → Deep Links Integration: Once data is retrieved appropriately based on unique identifiers passed during navigation, integrating deep links becomes more straightforward.

## Hallucination Report
- **NavigationSuiteScaffold**: This concept was not covered in the provided document and should be removed to ensure accuracy.
  
## Common Mistakes

### Passing NavController Directly to Composables

- **Name**: Hard-coding `NavController`
- **Looks like**:
  ```kotlin
  @Composable
  fun MyScreen(navController: NavController) {
      Button(onClick = { navController.navigate("profile") }) { /* ... */ }
  }
  ```
- **Why it breaks**: Passing the actual `NavController` makes composables dependent on a specific instance, complicating unit testing and reusability.
- **Correct**:
  ```kotlin
  @Composable
  fun MyScreen(onNavigate: (String) -> Unit) {
      Button(onClick = { onNavigate("profile") }) { /* ... */ }
  }
  ```

This ensures composables are independent of the `NavController`, making them testable and reusable.

## Testing

### NavigationTest class

- **Setup**: The test setup explicitly creates a `TestNavHostController` which is then used to simulate navigation scenarios.
- **Assertions**: Test assertions can be made by comparing the current route or back stack entries with expected values using methods like `navController.currentBackStackEntry?.destination?.hasRoute<Profile>()`.

## Missing Distinctions
The document does not clearly distinguish between state management within composables and data retrieval when navigating, but it implicitly suggests that complex data should be retrieved in the ViewModel layer rather than passed as arguments directly to composables. This separation ensures composables remain lightweight and focused on UI logic.

This precision check ensures all sections are grounded in provided content while deepening explanations where necessary.

## Concepts (for graph)
- Setup
- Get started
- Create a NavController
- Create a NavHost
- Navigate to a composable
- Navigate with arguments
- Retrieve complex data when navigating
- Deep links
- Nested Navigation
- Build an adaptive navigation bar and navigation rail
- Interoperability
- Navigate from Compose with Navigation for fragments

<!-- Quality Report
## Quality Report

| Section | Score | Issue (if < 4) |
| --- | --- | --- |
| Core Concepts | 5 | - |
| Mental Model | 4 | Remove reference to NavigationSuiteScaffold which is not covered in the document. |
| Decision Framework | 3 | Missing clear distinctions between state management and data retrieval, needs explicit mention of ViewModel layer's role. |
| Common Mistakes | 4 | Suggest including an example that shows how passing NavController affects reusability and testability. |
| Key Relationships | 4 | Highlight the relationship between lambdas for navigation and proper handling of complex data more clearly. |

## Verdict: NEEDS_FIX

## Fixes (only if NEEDS_FIX)
- Decision Framework: Add clear distinctions between state management within composables and data retrieval when navigating, explicitly mention ViewModel's role.
- Common Mistakes: Include an example that illustrates how passing NavController affects reusability and testability of composables.
-->
