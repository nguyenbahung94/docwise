<!-- Source: https://developer.android.com/guide/navigation -->
<!-- Source: https://developer.android.com/guide/navigation/use-graph/navigate -->
<!-- Source: https://developer.android.com/guide/navigation/navigation-principles -->
<!-- Source: https://developer.android.com/guide/navigation/principles -->
<!-- Source: https://developer.android.com/guide/navigation/navcontroller -->
<!-- Source: https://developer.android.com/guide/navigation/design -->
<!-- Source: https://developer.android.com/guide/navigation/design/dialog-destinations -->
<!-- Source: https://developer.android.com/guide/navigation/design/activity-destinations -->
<!-- Source: https://developer.android.com/guide/navigation/design/nested-graphs -->
<!-- Source: https://developer.android.com/guide/navigation/design/deep-link -->
<!-- Source: https://developer.android.com/guide/navigation/design/add-new -->
<!-- Source: https://developer.android.com/guide/navigation/design/type-safety -->
<!-- Source: https://developer.android.com/guide/navigation/design/encapsulate -->
<!-- Source: https://developer.android.com/guide/navigation/design/actions -->
<!-- Source: https://developer.android.com/guide/navigation/design/kotlin-dsl -->
<!-- Source: https://developer.android.com/guide/navigation/design/editor -->
<!-- Source: https://developer.android.com/guide/navigation/use-graph/navigate -->
<!-- Source: https://developer.android.com/guide/navigation/use-graph/navoptions -->
<!-- Source: https://developer.android.com/guide/navigation/use-graph/safe-args -->
<!-- Source: https://developer.android.com/guide/navigation/use-graph/pass-data -->
<!-- Source: https://developer.android.com/guide/navigation/use-graph/animate-transitions -->
<!-- Source: https://developer.android.com/guide/navigation/use-graph/conditional -->
<!-- Source: https://developer.android.com/guide/navigation/use-graph/programmatic -->
<!-- Source: https://developer.android.com/guide/navigation/backstack -->
<!-- Source: https://developer.android.com/guide/navigation/backstack/dialog -->
<!-- Source: https://developer.android.com/guide/navigation/backstack/circular -->
<!-- Source: https://developer.android.com/guide/navigation/backstack/multi-back-stacks -->
<!-- Source: https://developer.android.com/guide/navigation/integrations/feature-modules -->
<!-- Source: https://developer.android.com/guide/navigation/integrations/multi-module -->
<!-- Source: https://developer.android.com/guide/navigation/integrations/ui -->
<!-- Source: https://developer.android.com/guide/navigation/migrate -->
<!-- Source: https://developer.android.com/guide/navigation/testing -->
<!-- Source: https://developer.android.com/guide/navigation/custom-back -->
<!-- Source: https://developer.android.com/guide/navigation/custom-back/predictive-back-gesture -->
<!-- Source: https://developer.android.com/guide/navigation/custom-back/support-animations -->
<!-- Source: https://developer.android.com/guide/navigation/custom-back/support-animations-views -->
<!-- Source: https://developer.android.com/guide/navigation/navigation-event -->
<!-- Source: https://developer.android.com/guide/navigation/navigation-event/setup -->
<!-- Source: https://developer.android.com/guide/navigation/navigation-event/handle-back -->
<!-- Source: https://developer.android.com/guide/navigation/navigation-event/dispatcher -->
<!-- Source: https://developer.android.com/guide/navigation/responsive/config-changes -->
<!-- Source: https://developer.android.com/guide/navigation/responsive/form-factors -->
<!-- Source: https://developer.android.com/guide/navigation/advanced/swipe-view-2 -->
<!-- Source: https://developer.android.com/guide/navigation/advanced/swipe-view -->
<!-- Source: https://developer.android.com/guide/navigation/navigation-3 -->
<!-- Source: https://developer.android.com/guide/navigation/navigation-3/get-started -->
<!-- Source: https://developer.android.com/guide/navigation/navigation-3/basics -->
<!-- Source: https://developer.android.com/guide/navigation/navigation-3/save-state -->
<!-- Source: https://developer.android.com/guide/navigation/navigation-3/metadata -->
<!-- Source: https://developer.android.com/guide/navigation/navigation-3/modularize -->
<!-- Source: https://developer.android.com/guide/navigation/navigation-3/scenes -->
<!-- Source: https://developer.android.com/guide/navigation/navigation-3/scenes/scene-decorators -->
<!-- Source: https://developer.android.com/guide/navigation/navigation-3/animate-destinations -->
<!-- Source: https://developer.android.com/guide/navigation/navigation-3/naventrydecorators -->
<!-- Source: https://developer.android.com/guide/navigation/navigation-3/migration-guide -->
<!-- Source: https://developer.android.com/guide/navigation/navigation-pass-data -->
<!-- Type: official -->
<!-- Priority: high -->
<!-- Topic: navigation -->
<!-- Extracted: 2026-03-24 -->
<!-- Verified: — -->

# Navigation

## Rules
- DO: Accordingly, calls to navigate() should occur there and not in a lower
composable like ProfileScreen .
- DO: Use the @Serializable annotation to automatically create the necessary
serialization and deserialization methods for your route types. This annotation
is provided by the Kotlin Serialization
plugin . Follow these
instructions to add this plugin .
- DON'T: Extraneous query parameters do not affect deep link URI matching. For
example, http://www.example.com/users/{id} matches
 http://www.example.com/users/4?extraneousParam=7 , even though
 extraneousParam is not defined in the URI pattern.
- DO: Use the following rules to decide what type to use for your route:
- DON'T: KClass<T> : Use if you don't need to pass arguments, such as a class
without parameters, or a class where all parameters have default values
 
 For example: Profile::class
- DO: Use your navigation graph
- DO: Use internal to keep screens and route types private
- DO: Navigation options : Navigation options, represented as
 NavOptions . This class contains all of the special configuration for
transitioning to and back from the target destination, including animation
resource configuration, pop behavior, and whether the destination should be
launched in single top
- DON'T: Arrays support a single default value, "@null". Arrays don't support any
other default value.
- DO: Use the graph itself: navController.setGraph(navGraph, args)
- DO: Use @Keep annotations.
- DO: Use keepnames rules.
- DO: In the Navigation editor, click on the action where the animation should
occur.
- DO: The initial case, where the user is not logged in and should be asked to
login.
- DON'T: Don't use the app:navGraph element when adding the
 NavHostFragment in XML.
- DON'T: Don't call NavHostFragment.create(@NavigationRes int) .
- DON'T: Don't use any other APIs that rely solely on the
 R.navigation ID to inflate and set your graph.
- DON'T: Circular navigation : Learn how you can avoid an overstuffed back
stack in cases where navigation flows are circular.
- DON'T: If the value is false , you're navigating to a normal destination and don't
need to do anything else.
- DO: If the value is true , you should start observing the LiveData object that
is now in installMonitor.status . This LiveData object emits
 SplitInstallSessionState 
updates from the Play Core library. These updates contain installation
progress events that you can use to update the UI. Remember to han
- DO: Use <include-dynamic/> instead of <include/> , as shown in the following
example: 
 <include-dynamic
 android:id="@+id/includedGraph"
 app:moduleName="includedgraphfeature"
 app:graphResName="included_feature_nav"
 app:graphPackage="com.google.android.samples.dynamic_navigator.included_graph_feature
- DON'T: Dynamically-included graphs don't currently support deep links.
- DON'T: Dynamically-loaded nested graphs (that is, a <navigation> element with an
 app:moduleName ) don't currently support deep links.
- DO: Make sure to upgrade to
 AndroidX Activity 1.6.0-alpha05 . 
 // In your build.gradle file:
dependencies {

// Add this in addition to your other dependencies
implementation "androidx.activity:activity:1.6.0-alpha05"
 Note: OnBackPressedCallback is always called regardless of the value of
 android:en
- DO: Use the following approaches if your app must run business logic or log when the
user swipes back:
- DO: Use OnBackInvokedCallback with PRIORITY_SYSTEM_NAVIGATION_OBSERVER 
on devices running Android 16 and higher. This creates an observer-callback that doesn't
consume the back event. For example, you may register this callback when the
user swipes back from the root activity, or in other words, when t
- DO: Use TransitionManager#controlDelayedTransition instead of
 beginDelayedTransition to play transitions as
the user swipes back.
- DO: Use isSeekingSupported to check if the transition supports Predictive Back.
- DO: Use a NavDisplay to display your app's back stack. Whenever the back
stack changes, it updates the UI to display relevant content. See Display
the back stack .
- DO: Your back stack - this should be of type SnapshotStateList<T> , where T is
the type of your back stack keys. It is an observable List so that it
triggers recomposition of NavDisplay when it changes.
- DO: previousEntries: List<NavEntry<T>> : This property defines the
 NavEntry s that would result if a "back" action occurs from the current
 Scene . It's essential for calculating the proper predictive back state,
allowing the NavDisplay to anticipate and transition to the correct previous
state, which
- DO: If so, how should I arrange those entries into the Scene? Once a
 SceneStrategy commits to handling the entries, it takes on the
responsibility of constructing a Scene and defining how the specified
 NavEntry s will be displayed within that Scene .
- DO: Use rememberListDetailSceneStrategy (): This composable function
provides a pre-configured ListDetailSceneStrategy that can be used by a
 NavDisplay .
- DO: If it should decorate the input scene, it returns a new Scene . In
general, the returned scene takes the input scene as a parameter and calls
the input scene's content method within its own content 
method.
- DO: decorate - A composable lambda that is called for each NavEntry in your
back stack. It receives the NavEntry as a parameter. This lets you to
create state objects that are keyed to the entry's contentKey . You can
use CompositionLocalProvider to provide dependencies to the entry's content.
You can a
- DO: Use rememberDecoratedNavEntries . This function is useful when you
have multiple back stacks, each with its own set of decorators (see
 this code recipe for more details). The function returns
a decorated list of NavEntry s that you can use with NavDisplay .
- DON'T: Don't use a decorator to:
- DO: You should be familiar with navigation terminology .
- DO: You always exit the app through the Home screen, which is the first
screen displayed when the app launches.
- DO: Use the Get started page to add the Navigation 3 dependencies to your
project. The core dependencies are provided for you to copy.
- DO: Use NavigationState.topLevelRoute to determine the item that is currently
selected in a navigation bar.
- DO: bottomSheet : Follow the bottom sheet recipe here .
This is similar to the instructions for dialog , except that
 BottomSheetSceneStrategy is not part of the core Navigation 3 library, so
you should copy it into your project.

## Code Patterns
### Set up your environment
```kotlin
plugins {
  // Kotlin serialization plugin for type safe routes and navigation arguments
  kotlin("plugin.serialization") version "2.0.21"
}

dependencies {
  val nav_version = "2.9.7"

  // Jetpack Compose integration
  implementation("androidx.navigation:navigation-compose:$nav_version")

  // Views/Fragments integration
  implementation("androidx.navigation:navigation-fragment:$nav_version")
  implementation("androidx.navigation:navigation-ui:$nav_version")

  // Feature module support for Fragments
  implementation("androidx.navigation:navigation-dynamic-features-fragment:$nav_version")

  // Testing Navigation
  androidTestImplementation("androidx.navigation:navigation-testing:$nav_version")

  // JSON serialization library, works with the Kotlin serialization plugin
  implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.7.3")
}
```

### Navigate to a composable
```
@Serializable
object FriendsList

navController.navigate(route = FriendsList)
```

### Example
```kotlin
@Serializable
object Profile
@Serializable
object FriendsList

@Composable
fun MyAppNavHost(
    modifier: Modifier = Modifier,
    navController: NavHostController = rememberNavController(),
) {
    NavHost(
        modifier = modifier,
        navController = navController,
        startDestination = Profile
    ) {
        composable<Profile> {
            ProfileScreen(
                onNavigateToFriends = { navController.navigate(route = FriendsList) },
                /*...*/
            )
        }
        composable<FriendsList> { FriendsListScreen(/*...*/) }
    }
}

@Composable
fun ProfileScreen(
    onNavigateToFriends: () -> Unit,
    /*...*/
) {
    /*...*/
    Button(onClick = onNavigateToFriends) {
        Text(text = "See friends list")
    }
}
```

### Navigate using integer ID
```
viewTransactionsButton.setOnClickListener { view ->
  view.findNavController().navigate(R.id.viewTransactionsAction)
}
```

### Navigate using NavDeepLinkRequest
```kotlin
val request = NavDeepLinkRequest.Builder
  .fromUri("android-app://androidx.navigation.app/profile".toUri())
  .build()
findNavController().navigate(request)
```

### Compose
```kotlin
val navController = rememberNavController()
```

### Views
```kotlin
val navHostFragment =
    supportFragmentManager.findFragmentById(R.id.nav_host_fragment) as NavHostFragment
val navController = navHostFragment.navController
```

### Understand the lambda
```kotlin
val navGraph by remember(navController) {
  navController.createGraph(startDestination = Profile)) {
    composable<Profile> { ProfileScreen( /* ... */ ) }
    composable<FriendsList> { FriendsListScreen( /* ... */ ) }
  }
}
NavHost(navController, navGraph)
```

### Pass arguments
```kotlin
@Serializable
data class Profile(val name: String)
```

### Pass arguments
```kotlin
@Serializable
data class Profile(val nickname: String? = null)
```

### Obtain route instance
```kotlin
@Serializable
data class Profile(val name: String)

val navController = rememberNavController()

NavHost(navController = navController, startDestination = Profile(name="John Smith")) {
    composable<Profile> { backStackEntry ->
        val profile: Profile = backStackEntry.toRoute()
        ProfileScreen(name = profile.name) }
}
```

### Minimal example
```kotlin
@Serializable
data class Profile(val name: String)

@Serializable
object FriendsList

// Define the ProfileScreen composable.
@Composable
fun ProfileScreen(
    profile: Profile
    onNavigateToFriendsList: () -> Unit,
  ) {
  Text("Profile for ${profile.name}")
  Button(onClick = { onNavigateToFriendsList() }) {
    Text("Go to Friends List")
  }
}

// Define the FriendsListScreen composable.
@Composable
fun FriendsListScreen(onNavigateToProfile: () -> Unit) {
  Text("Friends List")
  Button(onClick = { onNavigateToProfile() }) {
    Text("Go to Profile")
  }
}

// Define the MyApp composable, including the `NavController` and `NavHost`.
@Composable
fun MyApp() {
  val navController = rememberNavController()
  NavHost(navController, startDestination = Profile(name = "John Smith")) {
    composable<Profile> { backStackEntry ->
        val profile: Profile = backStackEntry.toRoute()
        ProfileScreen(
            profile = profile,
            onNavigateToFriendsList = {
                navController.navigate(route = FriendsList)
            }
        )
    }
    composable<FriendsList> {
      FriendsListScreen(
        onNavigateToProfile = {
          navController.navigate(
            route = Profile(name = "Aisha Devi")
          )
        }
      )
    }
  }
}
```

### Programmatically
```xml
<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <androidx.fragment.app.FragmentContainerView
        android:id="@+id/nav_host_fragment"
        android:name="androidx.navigation.fragment.NavHostFragment"
        android:layout_width="match_parent"
        android:layout_height="match_parent" />
</FrameLayout>
```

### XML
```xml
<navigation xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:id="@+id/nav_graph"
    app:startDestination="@id/profile">

    <fragment
        android:id="@+id/profile"
        android:name="com.example.ProfileFragment"
        android:label="Profile">

        <!-- Action to navigate from Profile to Friends List. -->
        <action
            android:id="@+id/action_profile_to_friendslist"
            app:destination="@id/friendslist" />
    </fragment>

    <fragment
        android:id="@+id/friendslist"
        android:name="com.example.FriendsListFragment"
        android:label="Friends List" />

    <!-- Add other fragment destinations similarly. -->
</navigation>
```

### Dialog composable
```kotlin
@Serializable
object Home
@Serializable
object Settings
@Composable
fun HomeScreen(onNavigateToSettings: () -> Unit){
    Column {
        Text("Home")
        Button(onClick = onNavigateToSettings){
            Text("Open settings")
        }
    }
}

// This screen will be displayed as a dialog
@Composable
fun SettingsScreen(){
    Text("Settings")
    // ...
}

@Composable
fun MyApp() {
    val navController = rememberNavController()
    NavHost(navController, startDestination = Home) {
        composable<Home> { HomeScreen(onNavigateToSettings = { navController.navigate(route = Settings) }) }
        dialog<Settings> { SettingsScreen() }
    }
}
```

### Kotlin DSL
```
// Define destinations with serializable classes or objects
@Serializable
object Home
@Serializable
object Settings

// Add the graph to the NavController with `createGraph()`.
navController.graph = navController.createGraph(
    startDestination = Home
) {
    // Associate the home route with the HomeFragment.
    fragment<HomeFragment, Home> {
        label = "Home"
    }

    // Define the settings destination as a dialog using DialogFragment.
    dialog<SettingsFragment, Settings> {
        label = "Settings"
    }
}
```

### XML
```xml
<?xml version="1.0" encoding="utf-8"?>
<navigation xmlns:android="http://schemas.android.com/apk/res/android"
            xmlns:app="http://schemas.android.com/apk/res-auto"
            android:id="@+id/nav_graph">

...

<dialog
    android:id="@+id/my_dialog_fragment"
    android:name="androidx.navigation.myapp.MyDialogFragment">
    <argument android:name="myarg" android:defaultValue="@null" />
        <action
            android:id="@+id/myaction"
            app:destination="@+id/another_destination"/>
</dialog>

...

</navigation>
```

### XML
```
startActivity(Intent(context, DestinationActivity::class.java))
```

### XML
```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.android.navigation.activity">
    <application>
        <activity android:name=".DestinationActivity">
            <intent-filter>
                <action android:name="android.intent.action.VIEW" />
                <data
                    android:host="example.com"
                    android:scheme="https" />
                <category android:name="android.intent.category.BROWSABLE" />
                <category android:name="android.intent.category.DEFAULT" />
            </intent-filter>
        </activity>
    </application>
</manifest>
```

### Dynamic arguments
```
navController.navigate(
    R.id.localDestinationActivity,
    bundleOf("userId" to "someUser")
)
```

### Compose
```
// Routes
@Serializable object Title
@Serializable object Register

// Route for nested graph
@Serializable object Game

// Routes inside nested graph
@Serializable object Match
@Serializable object InGame
@Serializable object ResultsWinner
@Serializable object GameOver

NavHost(navController, startDestination = Title) {
   composable<Title> {
       TitleScreen(
           onPlayClicked = { navController.navigate(route = Register) },
           onLeaderboardsClicked = { /* Navigate to leaderboards */ }
       )
   }
   composable<Register> {
       RegisterScreen(
           onSignUpComplete = { navController.navigate(route = Game) }
       )
   }
   navigation<Game>(startDestination = Match) {
       composable<Match> {
           MatchScreen(
               onStartGame = { navController.navigate(route = InGame) }
           )
       }
       composable<InGame> {
           InGameScreen(
               onGameWin = { navController.navigate(route = ResultsWinner) },
               onGameLose = { navController.navigate(route = GameOver) }
           )
       }
       composable<ResultsWinner> {
           ResultsWinnerScreen(
               onNextMatchClicked = {
                   navController.navigate(route = Match) {
                       popUpTo(route = Match) { inclusive = true }
                   }
               },
               onLeaderboardsClicked = { /* Navigate to leaderboards */ }
           )
       }
       composable<GameOver> {
           GameOverScreen(
               onTryAgainClicked = {
                   navController.navigate(route = Match) {
                       popUpTo(route = Match) { inclusive = true }
                   }
               }
           )
       }
   }
}
```

### Compose
```
navController.navigate(route = Match)
```

### XML
```xml
<?xml version="1.0" encoding="utf-8"?>
<navigation xmlns:app="http://schemas.android.com/apk/res-auto"
   xmlns:tools="http://schemas.android.com/tools"
   xmlns:android="http://schemas.android.com/apk/res/android"
   app:startDestination="@id/mainFragment">
   <fragment
       android:id="@+id/mainFragment"
       android:name="com.example.cashdog.cashdog.MainFragment"
       android:label="fragment_main"
       tools:layout="@layout/fragment_main" >
       <action
           android:id="@+id/action_mainFragment_to_sendMoneyGraph"
           app:destination="@id/sendMoneyGraph" />
       <action
           android:id="@+id/action_mainFragment_to_viewBalanceFragment"
           app:destination="@id/viewBalanceFragment" />
   </fragment>
   <fragment
       android:id="@+id/viewBalanceFragment"
       android:name="com.example.cashdog.cashdog.ViewBalanceFragment"
       android:label="fragment_view_balance"
       tools:layout="@layout/fragment_view_balance" />
   <navigation android:id="@+id/sendMoneyGraph" app:startDestination="@id/chooseRecipient">
       <fragment
           android:id="@+id/chooseRecipient"
           android:name="com.example.cashdog.cashdog.ChooseRecipient"
           android:label="fragment_choose_recipient"
           tools:layout="@layout/fragment_choose_recipient">
           <action
               android:id="@+id/action_chooseRecipient_to_chooseAmountFragment"
               app:destination="@id/chooseAmountFragment" />
       </fragment>
       <fragment
           android:id="@+id/chooseAmountFragment"
           android:name="com.example.cashdog.cashdog.ChooseAmountFragment"
           android:label="fragment_choose_amount"
           tools:layout="@layout/fragment_choose_amount" />
   </navigation>
</navigation>
```

### XML
```
view.findNavController().navigate(R.id.action_mainFragment_to_sendMoneyGraph)
```

### Reference other navigation graphs with include
```xml
<!-- (root) nav_graph.xml -->
<?xml version="1.0" encoding="utf-8"?>
<navigation xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:id="@+id/nav_graph"
    app:startDestination="@id/fragment">

    <include app:graph="@navigation/included_graph" />

    <fragment
        android:id="@+id/fragment"
        android:name="com.example.myapplication.BlankFragment"
        android:label="Fragment in Root Graph"
        tools:layout="@layout/fragment_blank">
        <action
            android:id="@+id/action_fragment_to_second_graph"
            app:destination="@id/second_graph" />
    </fragment>

    ...
</navigation>
```

### Reference other navigation graphs with include
```xml
<!-- included_graph.xml -->
<?xml version="1.0" encoding="utf-8"?>
<navigation xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:id="@+id/second_graph"
    app:startDestination="@id/includedStart">

    <fragment
        android:id="@+id/includedStart"
        android:name="com.example.myapplication.IncludedStart"
        android:label="fragment_included_start"
        tools:layout="@layout/fragment_included_start" />
</navigation>
```

### Create an explicit deep link
```kotlin
val pendingIntent = NavDeepLinkBuilder(context)
    .setGraph(R.navigation.nav_graph)
    .setDestination(R.id.android)
    .setArguments(args)
    .createPendingIntent()
```

### Create an explicit deep link
```kotlin
val componentName = ...

val pendingIntent = NavDeepLinkBuilder(context)
    .setGraph(R.navigation.nav_graph)
    .setDestination(R.id.android)
    .setArguments(args)
    .setComponentName(componentName)
    .createPendingIntent()
```

### Create an implicit deep link
```xml
<fragment android:id="@+id/a"
          android:name="com.example.myapplication.FragmentA"
          tools:layout="@layout/a">
        <deepLink app:uri="www.example.com"
                app:action="android.intent.action.MY_ACTION"
                app:mimeType="type/subtype"/>
</fragment>
```

### Create an implicit deep link
```
<deepLink app:uri="https://www.google.com" />
```

### Handling deep links
```kotlin
override fun onNewIntent(intent: Intent?) {
    super.onNewIntent(intent)
    navController.handleDeepLink(intent)
}
```

### Add support for new destination types 

 
 
 
 

 
 
 Stay organized with collec
```kotlin
val customNavigator = CustomNavigator()
navController.navigatorProvider += customNavigator
```

### Define routes
```kotlin
// Define a home route that doesn't take any arguments
@Serializable
object Home

// Define a profile route that takes an ID
@Serializable
data class Profile(val id: String)
```

### Build your graph
```kotlin
NavHost(navController, startDestination = Home) {
     composable<Home> {
         HomeScreen(onNavigateToProfile = { id ->
             navController.navigate(Profile(id))
         })
     }
     composable<Profile> { backStackEntry ->
         val profile: Profile = backStackEntry.toRoute()
         ProfileScreen(profile.id)
     }
}
```

### Navigate to type safe route
```
navController.navigate(Profile(id = 123))
```

### Extract destinations
```kotlin
// MyApp.kt

@Serializable
object Contacts

@Composable
fun MyApp() {
  ...
  NavHost(navController, startDestination = Contacts) {
    composable<Contacts> { ContactsScreen( /* ... */ ) }
  }
}
```

### Extract destinations
```kotlin
// ContactsNavigation.kt

@Serializable
object Contacts

fun NavGraphBuilder.contactsDestination() {
    composable<Contacts> { ContactsScreen( /* ... */ ) }
}

// MyApp.kt

@Composable
fun MyApp() {
  ...
  NavHost(navController, startDestination = Contacts) {
     contactsDestination()
  }
}
```

### Example
```kotlin
// ContactScreens.kt

// Displays a list of contacts
@Composable
internal fun ContactsScreen(
  uiState: ContactsUiState,
  onNavigateToContactDetails: (contactId: String) -> Unit
) { ... }

// Displays the details for an individual contact
@Composable
internal fun ContactDetailsScreen(contact: ContactDetails) { ... }
```

### Create destinations
```kotlin
// ContactsNavigation.kt

@Serializable
object Contacts

// Adds contacts destination to `this` NavGraphBuilder
fun NavGraphBuilder.contactsDestination(
  // Navigation events are exposed to the caller to be handled at a higher level
  onNavigateToContactDetails: (contactId: String) -> Unit
) {
  composable<Contacts> {
    // The ViewModel as a screen level state holder produces the screen
    // UI state and handles business logic for the ConversationScreen
    val viewModel: ContactsViewModel = hiltViewModel()
    val uiState = viewModel.uiState.collectAsStateWithLifecycle()
    ContactsScreen(
      uiState,
      onNavigateToContactDetails
    )
  }
}
```

### Create destinations
```kotlin
// ContactsNavigation.kt

@Serializable
internal data class ContactDetails(val id: String)

fun NavGraphBuilder.contactDetailsScreen() {
  composable<ContactDetails> { navBackStackEntry ->
    ContactDetailsScreen(contact = navBackStackEntry.toRoute())
  }
}
```

### Encapsulate navigation events
```kotlin
// ContactsNavigation.kt

fun NavController.navigateToContactDetails(id: String) {
  navigate(route = ContactDetails(id = id))
}
```

### Bring it together
```kotlin
// MyApp.kt

@Composable
fun MyApp() {
  ...
  NavHost(navController, startDestination = Contacts) {
     contactsDestination(onNavigateToContactDetails = { contactId ->
        navController.navigateToContactDetails(id = contactId)
     })
     contactDetailsDestination()
  }
}
```

### Examples
```xml
<fragment
    android:id="@+id/fragmentA"
    android:name="com.example.FragmentA">
    <action
        android:id="@+id/action_fragmentA_to_fragmentB"
        app:destination="@id/fragmentB" />
</fragment>
```

### Navigate using an action
```
navController.navigate(R.id.action_fragmentA_to_fragmentB)
```

### Dependencies
```kotlin
dependencies {
    val nav_version = "2.9.7"

    api("androidx.navigation:navigation-fragment-ktx:$nav_version")
}
```

### Hosting a Kotlin DSL Nav Graph
```xml
<!-- activity_garden.xml -->
<FrameLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto">
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <androidx.fragment.app.FragmentContainerView
        android:id="@+id/nav_host"
        android:name="androidx.navigation.fragment.NavHostFragment"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        app:defaultNavHost="true" />

</FrameLayout>
```

### Create routes for your graph
```kotlin
@Serializable data object Home
@Serializable data class Plant(val id: String)
```

### Build a graph with the NavGraphBuilder DSL
```kotlin
val navController = findNavController(R.id.nav_host_fragment)
navController.graph = navController.createGraph(
    startDestination = Home
) {
    fragment<HomeFragment, Home> {
        label = resources.getString(R.string.home_title)
    }
    fragment<PlantDetailFragment, PlantDetail> {
        label = resources.getString(R.string.plant_detail_title)
    }
}
```

### Navigating with your Kotlin DSL graph
```kotlin
private fun navigateToPlant(plantId: String) {
   findNavController().navigate(route = PlantDetail(id = plantId))
}
```

### Navigating with your Kotlin DSL graph
```kotlin
val plantDetailRoute = findNavController().getBackStackEntry<PlantDetail>().toRoute<PlantDetail>()
val plantId = plantDetailRoute.id
```

### Navigating with your Kotlin DSL graph
```kotlin
val plantDetailRoute = savedStateHandle.toRoute<PlantDetail>()
val plantId = plantDetailRoute.id
```

### Fragment destinations
```
fragment<MyFragment, MyRoute> {
   label = getString(R.string.fragment_title)
   // custom argument types, deepLinks
}
```

### Activity destination
```
activity<MyRoute> {
   label = getString(R.string.activity_title)
   // custom argument types, deepLinks...

   activityClass = MyActivity::class
}
```

### Navigation graph destination
```
@Serializable data object HomeGraph
@Serializable data object Home

navigation<HomeGraph>(startDestination = Home) {
   // label, other destinations, deep links
}
```

### Supporting custom destinations
```kotlin
// The NavigatorProvider is retrieved from the NavController
val customDestination = navigatorProvider[CustomNavigator::class].createDestination().apply {
    route = Graph.CustomDestination.route
}
addDestination(customDestination)
```

### Providing destination arguments
```kotlin
@Serializable
data class MyRoute(
  val id: String,
  val myList: List<Int>,
  val optionalArg: String? = null
)

fragment<MyFragment, MyRoute>
```

### Providing custom types
```kotlin
@Serializable
data class SearchRoute(val parameters: SearchParameters)

@Serializable
@Parcelize
data class SearchParameters(
  val searchQuery: String,
  val filters: List<String>
)
```

### Providing custom types
```kotlin
val SearchParametersType = object : NavType<SearchParameters>(
  isNullableAllowed = false
) {
  override fun put(bundle: Bundle, key: String, value: SearchParameters) {
    bundle.putParcelable(key, value)
  }
  override fun get(bundle: Bundle, key: String): SearchParameters {
    return bundle.getParcelable(key) as SearchParameters
  }

  override fun serializeAsValue(value: SearchParameters): String {
    // Serialized values must always be Uri encoded
    return Uri.encode(Json.encodeToString(value))
  }

  override fun parseValue(value: String): SearchParameters {
    // Navigation takes care of decoding the string
    // before passing it to parseValue()
    return Json.decodeFromString<SearchParameters>(value)
  }
}
```

### Providing custom types
```
fragment<SearchFragment, SearchRoute>(
    typeMap = mapOf(typeOf<SearchParameters>() to SearchParametersType)
) {
    label = getString(R.string.plant_search_title)
}
```

### Providing custom types
```kotlin
val params = SearchParameters("rose", listOf("available"))
navController.navigate(route = SearchRoute(params))
```

### Providing custom types
```kotlin
val searchRoute = navController().getBackStackEntry<SearchRoute>().toRoute<SearchRoute>()
val params = searchRoute.parameters
```

### Deep links
```
@Serializable data object Home

fragment<HomeFragment, Home>{
  deepLink<Home>(basePath = "www.example.com/home"){
    // Optionally, specify the action and/or mime type that this destination
    // supports
    action = "android.intent.action.MY_ACTION"
    mimeType = "image/*"
  }
}
```

### URI format
```kotlin
@Serializable data class PlantDetail(
  val id: String,
  val name: String,
  val colors: List<String>,
  val latinName: String? = null,
)
```

### Options with XML
```
navController.navigate(R.id.action_b_to_a)
```

### Apply options programmatically
```
findNavController().navigate(
R.id.action_fragmentOne_to_fragmentTwo,
null,
navOptions { // Use the Kotlin DSL for building NavOptions
    anim {
        enter = android.R.animator.fade_in
        exit = android.R.animator.fade_out
    }
  }
)
```

### Apply options programmatically
```
findNavController().navigate(
    deepLinkUri,
    navOptions { // Use the Kotlin DSL for building NavOptions
        anim {
            enter = android.R.animator.fade_in
            exit = android.R.animator.fade_out
        }
    }
)
```

### Enable Safe Args
```kotlin
buildscript {
    repositories {
        google()
    }
    dependencies {
        val nav_version = "2.9.7"
        classpath("androidx.navigation:navigation-safe-args-gradle-plugin:$nav_version")
    }
}
```

### Enable Safe Args
```
plugins {
    id("androidx.navigation.safeargs")
}
```

### Enable Safe Args
```
plugins {
    id("androidx.navigation.safeargs.kotlin")
}
```

### Safe Args example
```kotlin
override fun onClick(v: View) {
    val amount: Float = ...
    val action =
        SpecifyAmountFragmentDirections
            .actionSpecifyAmountFragmentToConfirmationFragment(amount)
    v.findNavController().navigate(action)
}
```

### Ensure type safety by using Safe Args
```kotlin
override fun onClick(view: View) {
    val action =
        SpecifyAmountFragmentDirections
            .actionSpecifyAmountFragmentToConfirmationFragment()
    view.findNavController().navigate(action)
}
```

### Define destination arguments
```xml
<fragment android:id="@+id/myFragment" >
     <argument
         android:name="myArg"
         app:argType="integer"
         android:defaultValue="0" />
 </fragment>
```

### Override a destination argument in an action
```xml
<action android:id="@+id/startMyFragment"
    app:destination="@+id/myFragment">
    <argument
        android:name="myArg"
        app:argType="integer"
        android:defaultValue="1" />
</action>
```

### Use Safe Args to pass data with type safety
```kotlin
override fun onClick(v: View) {
   val amountTv: EditText = view!!.findViewById(R.id.editTextAmount)
   val amount = amountTv.text.toString().toInt()
   val action = SpecifyAmountFragmentDirections.confirmationAction(amount)
   v.findNavController().navigate(action)
}
```

### Use Safe Args to pass data with type safety
```kotlin
val args: ConfirmationFragmentArgs by navArgs()

override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
    val tv: TextView = view.findViewById(R.id.textViewAmount)
    val amount = args.amount
    tv.text = amount.toString()
}
```

### Pass data between destinations with Bundle objects
```kotlin
val bundle = bundleOf("amount" to amount)
view.findNavController().navigate(R.id.confirmationAction, bundle)
```

### Pass data between destinations with Bundle objects
```kotlin
val tv = view.findViewById<TextView>(R.id.textViewAmount)
tv.text = arguments?.getString("amount")
```

### Use @Keep annotations
```
@Keep class ParcelableArg : Parcelable { ... }

@Keep class SerializableArg : Serializable { ... }

@Keep enum class EnumArg { ... }
```

### Use keepnames rules
```
...

-keepnames class com.path.to.your.ParcelableArg
-keepnames class com.path.to.your.SerializableArg
-keepnames class com.path.to.your.EnumArg

...
```

### Animate transitions between destinations 

 
 
 
 

 
 
 Stay organized with col
```xml
<fragment
    android:id="@+id/specifyAmountFragment"
    android:name="com.example.buybuddy.buybuddy.SpecifyAmountFragment"
    android:label="fragment_specify_amount"
    tools:layout="@layout/fragment_specify_amount">
    <action
        android:id="@+id/confirmationAction"
        app:destination="@id/confirmationFragment"
        app:enterAnim="@anim/slide_in_right"
        app:exitAnim="@anim/slide_out_left"
        app:popEnterAnim="@anim/slide_in_left"
        app:popExitAnim="@anim/slide_out_right" />
</fragment>
```

### Shared element transitions to a fragment destination
```kotlin
val extras = FragmentNavigatorExtras(view1 to "hero_image")

view.findNavController().navigate(
    R.id.confirmationAction,
    null, // Bundle of args
    null, // NavOptions
    extras)
```

### Shared element transitions to an activity destination
```kotlin
// Rename the Pair class from the Android framework to avoid a name clash
import android.util.Pair as UtilPair
...
val options = ActivityOptionsCompat.makeSceneTransitionAnimation(activity,
        UtilPair.create(view1, "hero_image"))
val extras = ActivityNavigatorExtras(options)
view.findNavController().navigate(
    R.id.details,
    null, // Bundle of args
    null, // NavOptions
    extras)
```

### Apply pop animations to activity transitions
```kotlin
override fun finish() {
    super.finish()
    ActivityNavigator.applyPopAnimationsToPendingTransition(this)
}
```

### User login
```kotlin
class ProfileFragment : Fragment() {
    private val userViewModel: UserViewModel by activityViewModels()
    ...
}
```

### User login
```kotlin
class LoginFragment : Fragment() {
    companion object {
        const val LOGIN_SUCCESSFUL: String = "LOGIN_SUCCESSFUL"
    }

    private val userViewModel: UserViewModel by activityViewModels()
    private lateinit var savedStateHandle: SavedStateHandle

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        savedStateHandle = findNavController().previousBackStackEntry!!.savedStateHandle
        savedStateHandle.set(LOGIN_SUCCESSFUL, false)
    }
}
```

### User login
```kotlin
class ProfileFragment : Fragment() {
    ...

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val navController = findNavController()

        val currentBackStackEntry = navController.currentBackStackEntry!!
        val savedStateHandle = currentBackStackEntry.savedStateHandle
        savedStateHandle.getLiveData<Boolean>(LoginFragment.LOGIN_SUCCESSFUL)
                .observe(currentBackStackEntry, Observer { success ->
                    if (!success) {
                        val startDestination = navController.graph.startDestination
                        val navOptions = NavOptions.Builder()
                                .setPopUpTo(startDestination, true)
                                .build()
                        navController.navigate(startDestination, null, navOptions)
                    }
                })
    }

    ...
}
```

### Create a NavHostFragment
```kotlin
val finalHost = NavHostFragment.create(R.navigation.example_graph)
supportFragmentManager.beginTransaction()
    .replace(R.id.nav_host, finalHost)
    .setPrimaryNavigationFragment(finalHost) // equivalent to app:defaultNavHost="true"
    .commit()
```

### Reference a destination using NavBackStackEntry
```
myViewModel.liveData.observe(backStackEntry, Observer { myData ->
    // react to live data update
})
```

### Returning a result to the previous Destination
```kotlin
override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
    val navController = findNavController();
    // We use a String here, but any type that can be put in a Bundle is supported
    navController.currentBackStackEntry?.savedStateHandle?.getLiveData<String>("key")?.observe(
        viewLifecycleOwner) { result ->
        // Do something with the result.
    }
}
```

### Returning a result to the previous Destination
```
navController.previousBackStackEntry?.savedStateHandle?.set("key", result)
```

### Share UI-related data between destinations with ViewModel
```kotlin
val viewModel: MyViewModel
        by navGraphViewModels(R.id.my_graph)
```

### Share UI-related data between destinations with ViewModel
```kotlin
val viewModel: MyViewModel by navGraphViewModels(R.id.my_graph) {
    SavedStateViewModelFactory(requireActivity().application, requireParentFragment())
}
```

### Modifying inflated navigation graphs
```kotlin
val navHostFragment =
        supportFragmentManager.findFragmentById(R.id.nav_host_fragment) as NavHostFragment

val navController = navHostFragment.navController
val navGraph = navController.navInflater.inflate(R.navigation.bottom_nav_graph)
navGraph.startDestination = R.id.shop
navController.graph = navGraph
binding.bottomNavView.setupWithNavController(navController)
```

### Pop back to a particular destination
```
navController.popBackStack(R.id.destinationId, true)
```

### Handle a failed pop back
```
...

if (!navController.popBackStack()) {
    // Call finish() on your Activity
    finish()
}
```

### Save state when popping up
```
navController.navigate(
    route = route,
    navOptions =  navOptions {
        popUpTo<A>{ saveState = true }
        restoreState = true
    }
)
```

### XML example
```xml
<action
  android:id="@+id/action_a_to_b"
  app:destination="@id/b"
  app:popUpTo="@+id/a"
  app:popUpToInclusive="true"
  app:restoreState=”true”
  app:popUpToSaveState="true"/>
```

### Compose example
```kotlin
@Composable
fun MyAppNavHost(
    modifier: Modifier = Modifier,
    navController: NavHostController = rememberNavController(),
    startDestination: Any = A
) {
    NavHost(
        modifier = modifier,
        navController = navController,
        startDestination = startDestination
    ) {
        composable<A> {
            DestinationA(
                onNavigateToB = {
                // Pop everything up to, and including, the A destination off
                // the back stack, saving the back stack and the state of its
                // destinations.
                // Then restore any previous back stack state associated with
                // the B destination.
                // Finally navigate to the B destination.
                    navController.navigate(route = B) {
                        popUpTo<A> {
                            inclusive = true
                            saveState = true
                        }
                        restoreState = true
                    }
                },
            )
        }
        composable<B> { DestinationB(/* ... */) }
    }
}

@Composable
fun DestinationA(onNavigateToB: () -> Unit) {
    Button(onClick = onNavigateToB) {
        Text("Go to A")
    }
}
```

### Compose example
```
// Pop everything up to the destination_a destination off the back stack before
// navigating to the "destination_b" destination
navController.navigate("destination_b") {
    popUpTo("destination_a")
}

// Pop everything up to and including the "destination_a" destination off
// the back stack before navigating to the "destination_b" destination
navController.navigate("destination_b") {
    popUpTo("destination_a") { inclusive = true }
}

// Navigate to the "search” destination only if we’re not already on
// the "search" destination, avoiding multiple copies on the top of the
// back stack
navController.navigate("search") {
    launchSingleTop = true
}
```

### Compose implementation
```
// When creating your `NavGraph` in your `NavHost`.
composable("c") {
    DestinationC(
        onNavigateToA = {
          navController.navigate("a") {
            popUpTo("a") {
              inclusive = true
            }
          }
        },
    )
}
```

### Views implementation
```xml
<fragment
    android:id="@+id/c"
    android:name="com.example.myapplication.C"
    android:label="fragment_c"
    tools:layout="@layout/fragment_c">

    <action
        android:id="@+id/action_c_to_a"
        app:destination="@id/a"
        app:popUpTo="@+id/a"
        app:popUpToInclusive="true"/>
</fragment>
```

### Navigation XML
```xml
<action
  android:id=”@+id/swap_stack”
  app:destination=”@id/second_stack”
  app:restoreState=”true”
  app:popUpTo=”@id/first_stack_start_destination”
  app:popUpToSaveState=”true” />
```

### NavOptions
```
// Use the navigate() method that takes a navOptions DSL Builder
navController.navigate(selectedBottomNavRoute) {
  launchSingleTop = true
  restoreState = true
  popUpTo(navController.graph.findStartDestination().id) {
    saveState = true
  }
}
```

### Basic usage
```xml
<androidx.fragment.app.FragmentContainerView
    android:id="@+id/nav_host_fragment"
    android:name="androidx.navigation.dynamicfeatures.fragment.DynamicNavHostFragment"
    app:navGraph="@navigation/nav_graph"
    ... />
```

### Basic usage
```xml
<fragment
    app:moduleName="myDynamicFeature"
    android:id="@+id/featureFragment"
    android:name="com.google.android.samples.feature.FeatureFragment"
    ... />
```

### Monitor the request state
```kotlin
val navController = ...
val installMonitor = DynamicInstallMonitor()

navController.navigate(
    destinationId,
    null,
    null,
    DynamicExtras(installMonitor)
)
```

### Included graphs
```xml
<include-dynamic
    android:id="@+id/includedGraph"
    app:moduleName="includedgraphfeature"
    app:graphResName="included_feature_nav"
    app:graphPackage="com.google.android.samples.dynamic_navigator.included_graph_feature" />
```

### [After] Use the correct graphPackage
```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:dist="http://schemas.android.com/apk/distribution"
    featureSplit="DynamicFeatureModule"
    package="com.example.dynamicfeatureapp"
    android:versionCode="1"
    android:versionName="1.0" >

    <uses-sdk
        android:minSdkVersion="21"
        android:targetSdkVersion="30" />

    <dist:module
        dist:instant="false"
        dist:title="@string/title_dynamicfeaturemodule" >
        <dist:delivery>
            <dist:install-time />
        </dist:delivery>

        <dist:fusing dist:include="true" />
    </dist:module>

    <application />

</manifest>
```

### Navigation best practices for multi-module projects 

 
 
 
 

 
 
 Stay organiz
```kotlin
dependencies {
    ...
    implementation(project(":feature:home"))
    implementation(project(":feature:favorites"))
    implementation(project(":feature:settings"))
```

### Top-level navigation in app module
```xml
<?xml version="1.0" encoding="utf-8"?>
<menu xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto">

    <item
        android:id="@id/home_nav_graph"
        android:icon="@drawable/ic_home"
        android:title="Home"
        app:showAsAction="ifRoom"/>

    <item
        android:id="@id/favorites_nav_graph"
        android:icon="@drawable/ic_favorite"
        android:title="Favorites"
        app:showAsAction="ifRoom"/>

    <item
        android:id="@id/settings_nav_graph"
        android:icon="@drawable/ic_settings"
        android:title="Settings"
        app:showAsAction="ifRoom" />
</menu>
```

### Top-level navigation in app module
```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    setContentView(R.layout.activity_main)
    val navHostFragment =
        supportFragmentManager.findFragmentById(R.id.nav_host_fragment) as NavHostFragment
    val navController = navHostFragment.navController

    findViewById<BottomNavigationView>(R.id.bottom_nav)
            .setupWithNavController(navController)
}
```

### Navigating across feature modules
```kotlin
button.setOnClickListener {
    val request = NavDeepLinkRequest.Builder
        .fromUri("android-app://example.google.app/settings_fragment_two".toUri())
        .build()
    findNavController().navigate(request)
}
```

### Top app bar
```xml
<navigation>
    <fragment ...
              android:label="Page title">
      ...
    </fragment>
</navigation>
```

### AppBarConfiguration
```kotlin
val appBarConfiguration = AppBarConfiguration(navController.graph)
```

### AppBarConfiguration
```kotlin
val appBarConfiguration = AppBarConfiguration(setOf(R.id.main, R.id.profile))
```

### Create a Toolbar
```xml
<LinearLayout>
    <androidx.appcompat.widget.Toolbar
        android:id="@+id/toolbar" />
    <androidx.fragment.app.FragmentContainerView
        android:id="@+id/nav_host_fragment"
        ... />
    ...
</LinearLayout>
```

### Create a Toolbar
```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
    setContentView(R.layout.activity_main)

    ...

    val navController = findNavController(R.id.nav_host_fragment)
    val appBarConfiguration = AppBarConfiguration(navController.graph)
    findViewById<Toolbar>(R.id.toolbar)
        .setupWithNavController(navController, appBarConfiguration)
}
```

### Create a Toolbar
```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
    ...

    val navHostFragment =
        supportFragmentManager.findFragmentById(R.id.nav_host_fragment) as NavHostFragment
    val navController = navHostFragment.navController
    val appBarConfiguration = AppBarConfiguration(
        topLevelDestinationIds = setOf(),
        fallbackOnNavigateUpListener = ::onSupportNavigateUp
    )
    findViewById<Toolbar>(R.id.toolbar)
        .setupWithNavController(navController, appBarConfiguration)
}
```

### Include CollapsingToolbarLayout
```xml
<LinearLayout>
    <com.google.android.material.appbar.AppBarLayout
        android:layout_width="match_parent"
        android:layout_height="@dimen/tall_toolbar_height">

        <com.google.android.material.appbar.CollapsingToolbarLayout
            android:id="@+id/collapsing_toolbar_layout"
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            app:contentScrim="?attr/colorPrimary"
            app:expandedTitleGravity="top"
            app:layout_scrollFlags="scroll|exitUntilCollapsed|snap">

            <androidx.appcompat.widget.Toolbar
                android:id="@+id/toolbar"
                android:layout_width="match_parent"
                android:layout_height="?attr/actionBarSize"
                app:layout_collapseMode="pin"/>
        </com.google.android.material.appbar.CollapsingToolbarLayout>
    </com.google.android.material.appbar.AppBarLayout>

    <androidx.fragment.app.FragmentContainerView
        android:id="@+id/nav_host_fragment"
        ... />
    ...
</LinearLayout>
```

### Action bar
```kotlin
private lateinit var appBarConfiguration: AppBarConfiguration

...

override fun onCreate(savedInstanceState: Bundle?) {
    ...

    val navHostFragment =
        supportFragmentManager.findFragmentById(R.id.nav_host_fragment) as NavHostFragment
    val navController = navHostFragment.navController
    appBarConfiguration = AppBarConfiguration(navController.graph)
    setupActionBarWithNavController(navController, appBarConfiguration)
}
```

### Action bar
```kotlin
override fun onSupportNavigateUp(): Boolean {
    val navController = findNavController(R.id.nav_host_fragment)
    return navController.navigateUp(appBarConfiguration)
            || super.onSupportNavigateUp()
}
```

### Tie destinations to menu items
```xml
<menu xmlns:android="http://schemas.android.com/apk/res/android">

    ...

    <item
        android:id="@+id/details_page_fragment"
        android:icon="@drawable/ic_details"
        android:title="@string/details" />
</menu>
```

### Tie destinations to menu items
```kotlin
override fun onOptionsItemSelected(item: MenuItem): Boolean {
    val navController = findNavController(R.id.nav_host_fragment)
    return item.onNavDestinationSelected(navController) || super.onOptionsItemSelected(item)
}
```

### Add a navigation drawer
```xml
<?xml version="1.0" encoding="utf-8"?>
<!-- Use DrawerLayout as root container for activity -->
<androidx.drawerlayout.widget.DrawerLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:id="@+id/drawer_layout"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:fitsSystemWindows="true">

    <!-- Layout to contain contents of main body of screen (drawer will slide over this) -->
    <androidx.fragment.app.FragmentContainerView
        android:name="androidx.navigation.fragment.NavHostFragment"
        android:id="@+id/nav_host_fragment"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        app:defaultNavHost="true"
        app:navGraph="@navigation/nav_graph" />

    <!-- Container for contents of drawer - use NavigationView to make configuration easier -->
    <com.google.android.material.navigation.NavigationView
        android:id="@+id/nav_view"
        android:layout_width="wrap_content"
        android:layout_height="match_parent"
        android:layout_gravity="start"
        android:fitsSystemWindows="true" />

</androidx.drawerlayout.widget.DrawerLayout>
```

### Bottom navigation
```xml
<LinearLayout>
    ...
    <androidx.fragment.app.FragmentContainerView
        android:id="@+id/nav_host_fragment"
        ... />
    <com.google.android.material.bottomnavigation.BottomNavigationView
        android:id="@+id/bottom_nav"
        app:menu="@menu/menu_bottom_nav" />
</LinearLayout>
```

### Listen for navigation events
```
navController.addOnDestinationChangedListener { _, destination, _ ->
   if(destination.id == R.id.full_screen_destination) {
       toolbar.visibility = View.GONE
       bottomNavigationView.visibility = View.GONE
   } else {
       toolbar.visibility = View.VISIBLE
       bottomNavigationView.visibility = View.VISIBLE
   }
}
```

### Argument-based listeners
```
navController.addOnDestinationChangedListener { _, _, arguments ->
    appBar.isVisible = arguments?.getBoolean("ShowAppBar", false) == true
}
```

### Create a New Layout to Host the UI
```xml
<FrameLayout
   xmlns:app="http://schemas.android.com/apk/res-auto"
   xmlns:android="http://schemas.android.com/apk/res/android"
   android:id="@+id/main_content"
   android:layout_height="match_parent"
   android:layout_width="match_parent" />
```

### Create a New Layout to Host the UI
```kotlin
class ProductListActivity : AppCompatActivity() {
    ...
    override fun onCreate(savedInstanceState: Bundle?) {
        ...
        // Replace setContentView(R.layout.product_list) with the line below
        setContentView(R.layout.product_list_host)
        ...
    }
}
```

### Create a fragment
```
class ProductListFragment : Fragment() {
    // Leave empty for now.
}
```

### Move activity logic into a fragment
```kotlin
class ProductListActivity : AppCompatActivity() {

    // Views and/or ViewDataBinding references, Adapters...
    private lateinit var productAdapter: ProductAdapter
    private lateinit var binding: ProductListActivityBinding

    ...

    // ViewModels, System Services, other Dependencies...
    private val viewModel: ProductListViewModel by viewModels()

    ...

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // View initialization logic
        DataBindingUtil.setContentView(this, R.layout.product_list_activity)

        // Post view initialization logic
        // Connect adapters
        productAdapter = ProductAdapter(productClickCallback)
        binding.productsList.setAdapter(productAdapter)

        // Initialize view properties, set click listeners, etc.
        binding.productsSearchBtn.setOnClickListener {...}

        // Subscribe to state
        viewModel.products.observe(this, Observer { myProducts ->
            ...
        })

        // ...and so on
    }
   ...
}
```

### Move activity logic into a fragment
```kotlin
// Provided to ProductAdapter in ProductListActivity snippet.
    private val productClickCallback = ProductClickCallback { product ->
        show(product)
    }

    fun show(product: Product) {
        val intent = Intent(this, ProductActivity::class.java)
        intent.putExtra(ProductActivity.KEY_PRODUCT_ID, product.id)
        startActivity(intent)
    }
```

### Move activity logic into a fragment
```kotlin
class ProductListFragment : Fragment() {

    private lateinit var binding: ProductListFragmentBinding
    private val viewModel: ProductListViewModel by viewModels()

     // View initialization logic
    override fun onCreateView(inflater: LayoutInflater,
            container: ViewGroup?,
            savedInstanceState: Bundle?): View? {
        binding = DataBindingUtil.inflate(
                inflater,
                R.layout.product_list,
                container,
                false
        )
        return binding.root
    }

    // Post view initialization logic
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        // Connect adapters
        productAdapter = ProductAdapter(productClickCallback)
        binding.productsList.setAdapter(productAdapter)

        // Initialize view properties, set click listeners, etc.
        binding.productsSearchBtn.setOnClickListener {...}

        // Subscribe to state
        viewModel.products.observe(this, Observer { myProducts ->
            ...
        })

        // ...and so on
    }

    // Provided to ProductAdapter
    private val productClickCallback = ProductClickCallback { product ->
        if (lifecycle.currentState.isAtLeast(Lifecycle.State.STARTED)) {
            (requireActivity() as ProductListActivity).show(product)
        }
    }
    ...
}
```

### Initialize the fragment in the host activity
```kotlin
class ProductListActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.product_list_host)
    }

    fun show(product: Product) {
        val intent = Intent(this, ProductActivity::class.java)
        intent.putExtra(ProductActivity.KEY_PRODUCT_ID, product.id)
        startActivity(intent)
    }
}
```

### Pass intent extras to the fragment
```kotlin
...

if (savedInstanceState == null) {
    val fragment = ProductDetailsFragment()

    // Intent extras and Fragment Args are both of type android.os.Bundle.
    fragment.arguments = intent.extras

    supportFragmentManager
            .beginTransaction()
            .add(R.id.main_content, fragment)
            .commit()
}

...
```

### Create a navigation graph
```xml
<androidx.fragment.app.FragmentContainerView
   android:name="androidx.navigation.fragment.NavHostFragment"
   app:navGraph="@navigation/product_list_graph"
   app:defaultNavHost="true"
   android:id="@+id/main_content"
   android:layout_width="match_parent"
   android:layout_height="match_parent" />
```

### Single activity managing multiple fragments
```kotlin
class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Logic to load the starting destination
        //  when the Activity is first created
        if (savedInstanceState == null) {
            val fragment = ProductListFragment()
            supportFragmentManager.beginTransaction()
                    .add(R.id.fragment_container, fragment, ProductListFragment.TAG)
                    .commit()
        }
    }

    // Logic to navigate the user to another destination.
    // This may include logic to initialize and set arguments on the destination
    // fragment or even transition animations between the fragments (not shown here).
    fun navigateToProductDetail(productId: String) {
        val fragment = new ProductDetailsFragment()
        val args = Bundle().apply {
            putInt(KEY_PRODUCT_ID, productId)
        }
        fragment.arguments = args

        supportFragmentManager.beginTransaction()
                .addToBackStack(ProductDetailsFragment.TAG)
                .replace(R.id.fragment_container, fragment, ProductDetailsFragment.TAG)
                .commit()
    }
}
```

### Single activity managing multiple fragments
```kotlin
public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Logic to load the starting destination when the activity is first created.
        if (savedInstanceState == null) {
            val fragment = ProductListFragment()
            supportFragmentManager.beginTransaction()
                    .add(R.id.fragment_container, fragment, ProductListFragment.TAG)
                    .commit();
        }
    }

    // Logic to navigate the user to another destination.
    // This may include logic to initialize and set arguments on the destination
    // fragment or even transition animations between the fragments (not shown here).
    public void navigateToProductDetail(String productId) {
        Fragment fragment = new ProductDetailsFragment();
        Bundle args = new Bundle();
        args.putInt(KEY_PRODUCT_ID, productId);
        fragment.setArguments(args);

        getSupportFragmentManager().beginTransaction()
                .addToBackStack(ProductDetailsFragment.TAG)
                .replace(R.id.fragment_container, fragment, ProductDetailsFragment.TAG)
                .commit();
    }
}
```

### Single activity managing multiple fragments
```kotlin
class ProductListFragment : Fragment() {
    ...
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        // In this example a callback is passed to respond to an item clicked
        //  in a RecyclerView
        productAdapter = ProductAdapter(productClickCallback)
        binding.productsList.setAdapter(productAdapter)
    }
    ...

    // The callback makes the call to the activity to make the transition.
    private val productClickCallback = ProductClickCallback { product ->
            (requireActivity() as MainActivity).navigateToProductDetail(product.id)
    }
}
```

### Single activity managing multiple fragments
```kotlin
class MainActivity : AppCompatActivity() {

    // No need to load the start destination, handled automatically by the Navigation component
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }
}
```

### Pass arguments safely
```kotlin
class ProductListFragment : Fragment() {

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        // In this example a callback is passed to respond to an item clicked in a RecyclerView
        productAdapter = ProductAdapter(productClickCallback)
        binding.productsList.setAdapter(productAdapter)
    }
    ...

    // The callback makes the call to the NavController to make the transition.
    private val productClickCallback = ProductClickCallback { product ->
        val directions = ProductListDirections.navigateToProductDetail(product.id)
        findNavController().navigate(directions)
    }
}
```

### Top-Level Navigation
```kotlin
class MainActivity : AppCompatActivity(),
    NavigationView.OnNavigationItemSelectedListener {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val toolbar: Toolbar = findViewById(R.id.toolbar)
        setSupportActionBar(toolbar)

        val drawerLayout: DrawerLayout = findViewById(R.id.drawer_layout)
        val navView: NavigationView = findViewById(R.id.nav_view)
        val toggle = ActionBarDrawerToggle(
                this,
                drawerLayout,
                toolbar,
                R.string.navigation_drawer_open, 
                R.string.navigation_drawer_close
        )
        drawerLayout.addDrawerListener(toggle)
        toggle.syncState()

        navView.setNavigationItemSelectedListener(this)
    }

    override fun onBackPressed() {
        val drawerLayout: DrawerLayout = findViewById(R.id.drawer_layout)
        if (drawerLayout.isDrawerOpen(GravityCompat.START)) {
            drawerLayout.closeDrawer(GravityCompat.START)
        } else {
            super.onBackPressed()
        }
    }

    override fun onNavigationItemSelected(item: MenuItem): Boolean {
        // Handle navigation view item clicks here.
        when (item.itemId) {
            R.id.home -> {
                val homeFragment = HomeFragment()
                show(homeFragment)
            }
            R.id.gallery -> {
                val galleryFragment = GalleryFragment()
                show(galleryFragment)
            }
            R.id.slide_show -> {
                val slideShowFragment = SlideShowFragment()
                show(slideShowFragment)
            }
            R.id.tools -> {
                val toolsFragment = ToolsFragment()
                show(toolsFragment)
            }
        }
        val drawerLayout: DrawerLayout = findViewById(R.id.drawer_layout)
        drawerLayout.closeDrawer(GravityCompat.START)
        return true
    }
}

private fun show(fragment: Fragment) {

    val drawerLayout = drawer_layout as DrawerLayout
    val fragmentManager = supportFragmentManager

    fragmentManager
            .beginTransaction()
            .replace(R.id.main_content, fragment)
            .commit()

    drawerLayout.closeDrawer(GravityCompat.START)
}
```

### Top-Level Navigation
```xml
<!-- activity_main_drawer.xml -->
<menu xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    tools:showIn="navigation_view">

    <group android:checkableBehavior="single">
        <item
            android:id="@+id/home"
            android:icon="@drawable/ic_menu_camera"
            android:title="@string/menu_home" />
        <item
            android:id="@+id/gallery"
            android:icon="@drawable/ic_menu_gallery"
            android:title="@string/menu_gallery" />
        <item
            android:id="@+id/slide_show"
            android:icon="@drawable/ic_menu_slideshow"
            android:title="@string/menu_slideshow" />
        <item
            android:id="@+id/tools"
            android:icon="@drawable/ic_menu_manage"
            android:title="@string/menu_tools" />
    </group>
</menu>
```

### Top-Level Navigation
```xml
<!-- activity_main_graph.xml -->
<navigation xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:id="@+id/main_graph"
    app:startDestination="@id/home">

    <fragment
        android:id="@+id/home"
        android:name="com.example.HomeFragment"
        android:label="Home"
        tools:layout="@layout/home" />

    <fragment
        android:id="@+id/gallery"
        android:name="com.example.GalleryFragment"
        android:label="Gallery"
        tools:layout="@layout/gallery" />

    <fragment
        android:id="@+id/slide_show"
        android:name="com.example.SlideShowFragment"
        android:label="Slide Show"
        tools:layout="@layout/slide_show" />

    <fragment
        android:id="@+id/tools"
        android:name="com.example.ToolsFragment"
        android:label="Tools"
        tools:layout="@layout/tools" />

</navigation>
```

### Top-Level Navigation
```kotlin
class MainActivity : AppCompatActivity()  {

    val drawerLayout by lazy { findViewById<DrawerLayout>(R.id.drawer_layout) }
    val navController by lazy {
      (supportFragmentManager.findFragmentById(R.id.main_content) as NavHostFragment).navController
    }
    val navigationView by lazy { findViewById<NavigationView>(R.id.nav_view) }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val toolbar = findViewById<Toolbar>(R.id.toolbar)
        setSupportActionBar(toolbar)

        // Show and Manage the Drawer and Back Icon
        setupActionBarWithNavController(navController, drawerLayout)

        // Handle Navigation item clicks
        // This works with no further action on your part if the menu and destination id’s match.
        navigationView.setupWithNavController(navController)

    }

    override fun onSupportNavigateUp(): Boolean {
        // Allows NavigationUI to support proper up navigation or the drawer layout
        // drawer menu, depending on the situation
        return navController.navigateUp(drawerLayout)
    }
}
```

### Add activity destinations
```kotlin
fun navigateToProductDetails(productId: String) {
    val intent = Intent(this, ProductDetailsActivity::class.java)
    intent.putExtra(KEY_PRODUCT_ID, productId)
    startActivity(intent)
}
```

### Add activity destinations
```xml
<!-- Graph A -->
<navigation xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:id="@+id/product_list_graph"
    app:startDestination="@id/product_list">

    <fragment
        android:id="@+id/product_list"
        android:name="com.example.android.persistence.ui.ProductListFragment"
        android:label="Product List"
        tools:layout="@layout/product_list_fragment">
        <action
            android:id="@+id/navigate_to_product_detail"
            app:destination="@id/product_details_activity" />
    </fragment>

    <activity
        android:id="@+id/product_details_activity"
        android:name="com.example.android.persistence.ui.ProductDetailsActivity"
        android:label="Product Details"
        tools:layout="@layout/product_details_host">

        <argument
            android:name="product_id"
            app:argType="integer" />

    </activity>

</navigation>
```

### Add activity destinations
```xml
<!-- Graph B -->
<navigation xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    app:startDestination="@id/product_details">

    <fragment
        android:id="@+id/product_details"
        android:name="com.example.android.persistence.ui.ProductDetailsFragment"
        android:label="Product Details"
        tools:layout="@layout/product_details_fragment">
        <argument
            android:name="product_id"
            app:argType="integer" />
    </fragment>

</navigation>
```

### Add activity destinations
```kotlin
fun navigateToProductDetails(productId: String) {
    val directions = ProductListDirections.navigateToProductDetail(productId)
    findNavController().navigate(directions)
}
```

### Pass activity destination args to a start destination fragment
```kotlin
class ProductDetailsActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.product_details_host)
        val navHostFragment = supportFragmentManager.findFragmentById(R.id.main_content) as NavHostFragment
        val navController = navHostFragment.navController
        navController
                .setGraph(R.navigation.product_detail_graph, intent.extras)
    }

}
```

### Pass activity destination args to a start destination fragment
```kotlin
class ProductDetailsFragment : Fragment() {

    val args by navArgs<ProductDetailsArgs>()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        val productId = args.productId
        ...
    }
    ...
```

### Combine activities
```xml
<!-- Combined Graph A and B -->
<navigation xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:id="@+id/product_list_graph"
    app:startDestination="@id/product_list">

    <fragment
        android:id="@+id/product_list"
        android:name="com.example.android.persistence.ui.ProductListFragment"
        android:label="Product List Fragment"
        tools:layout="@layout/product_list">
        <action
            android:id="@+id/navigate_to_product_detail"
            app:destination="@id/product_details" />
    </fragment>

    <fragment
        android:id="@+id/product_details"
        android:name="com.example.android.persistence.ui.ProductDetailsFragment"
        android:label="Product Details"
        tools:layout="@layout/product_details">
        <argument
            android:name="product_id"
            app:argType="integer" />
    </fragment>

</navigation>
```

### Test fragment navigation
```kotlin
dependencies {
  val nav_version = "2.9.7"

  androidTestImplementation("androidx.navigation:navigation-testing:$nav_version")
}
```

### Test fragment navigation
```kotlin
class TitleScreen : Fragment() {
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ) = inflater.inflate(R.layout.fragment_title_screen, container, false)

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        view.findViewById<Button>(R.id.play_btn).setOnClickListener {
            view.findNavController().navigate(R.id.action_title_screen_to_in_game)
        }
    }
}
```

### Test fragment navigation
```kotlin
@RunWith(AndroidJUnit4::class)
class TitleScreenTest {

    @Test
    fun testNavigationToInGameScreen() {
        // Create a TestNavHostController
        val navController = TestNavHostController(
            ApplicationProvider.getApplicationContext())

        // Create a graphical FragmentScenario for the TitleScreen
        val titleScenario = launchFragmentInContainer<TitleScreen>()

        titleScenario.onFragment { fragment ->
            // Set the graph on the TestNavHostController
            navController.setGraph(R.navigation.trivia)

            // Make the NavController available via the findNavController() APIs
            Navigation.setViewNavController(fragment.requireView(), navController)
        }

        // Verify that performing a click changes the NavController’s state
        onView(ViewMatchers.withId(R.id.play_btn)).perform(ViewActions.click())
        assertThat(navController.currentDestination?.id).isEqualTo(R.id.in_game)
    }
}
```

### Test NavigationUI with FragmentScenario
```kotlin
class TitleScreen : Fragment(R.layout.fragment_title_screen) {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        val navController = view.findNavController()
        view.findViewById<Toolbar>(R.id.toolbar).setupWithNavController(navController)
    }
}
```

### Test NavigationUI with FragmentScenario
```kotlin
val scenario = launchFragmentInContainer {
    TitleScreen().also { fragment ->

        // In addition to returning a new instance of our Fragment,
        // get a callback whenever the fragment’s view is created
        // or destroyed so that we can set the NavController
        fragment.viewLifecycleOwnerLiveData.observeForever { viewLifecycleOwner ->
            if (viewLifecycleOwner != null) {
                // The fragment’s view has just been created
                navController.setGraph(R.navigation.trivia)
                Navigation.setViewNavController(fragment.requireView(), navController)
            }
        }
    }
}
```

### Testing interactions with back stack entries
```kotlin
val navController = TestNavHostController(ApplicationProvider.getApplicationContext())

// This allows fragments to use by navGraphViewModels()
navController.setViewModelStore(ViewModelStore())
```

### Implement custom back navigation with Views
```kotlin
class MyFragment : Fragment() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // This callback will only be called when MyFragment is at least Started.
        val callback = requireActivity().onBackPressedDispatcher.addCallback(this) {
            // Handle the back button event
        }

        // The callback can be enabled or disabled here or in the lambda
    }
    ...
}
```

### Handle custom back gestures in Compose
```kotlin
PredictiveBackHandler(enabled = isBackHandlerEnabled) { progress: Flow<BackEventCompat> ->
    try {
        progress.collect { backEvent ->
            // Update your UI or animation based on backEvent.progress
        }
        // Handle the final back action (e.g., navigate back)
    } catch (e: CancellationException) {
        // Back gesture was cancelled, reset your UI
    }
}
```

### Opt out of predictive back
```xml
<application
    ...
    android:enableOnBackInvokedCallback="false"
    ... >
...
</application>
```

### Opt out at an activity level
```xml
<manifest ...>
    <application . . .

        android:enableOnBackInvokedCallback="false">

        <activity
            android:name=".MainActivity"
            android:enableOnBackInvokedCallback="true"
            ...
        </activity>
        <activity
            android:name=".SecondActivity"
            android:enableOnBackInvokedCallback="false"
            ...
        </activity>
    </application>
</manifest>
```

### Add custom transitions in Jetpack Compose
```kotlin
@Composable
fun DetailScreen(onBack: () -> Unit) {
    var scale by remember { mutableFloatStateOf(1f) }
    var xOffset by remember { mutableFloatStateOf(0f) }
    val scope = rememberCoroutineScope()

    PredictiveBackHandler { progressFlow ->
        try {
            progressFlow.collectLatest { backEvent ->
                scale = 1f - backEvent.progress
                xOffset = backEvent.progress * 100f
            }
            // User completed gesture
            onBack()
        } catch (e: CancellationException) {
            // User cancelled gesture
            // Animate scale and xOffset back to 1f and 0f respectively
            scope.launch {
                animate(scale, 1f) { value, _ -> scale = value }
            }
            scope.launch {
                animate(xOffset, 0f) { value, _ -> xOffset = value }
            }
        }
    }
    Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        Surface(
            modifier = Modifier
                .size(200.dp)
                .scale(scale)
                .offset(x = xOffset.dp, y = 0.dp),
            color = Color.Blue
        ) {}
    }
}
```

### Use the Progress APIs with AndroidX Transitions
```kotlin
class MyFragment : Fragment() {

    val transitionSet = TransitionSet().apply {
        addTransition(Fade(Fade.MODE_OUT))
        addTransition(ChangeBounds())
        addTransition(Fade(Fade.MODE_IN))
    }
    ...
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val callback = object : OnBackPressedCallback(enabled = false) {

            var controller: TransitionSeekController? = null

            @RequiresApi(34)
            override fun handleOnBackStarted(backEvent: BackEvent) {
                // Create the transition
                controller = TransitionManager.controlDelayedTransition(
                    binding.card,
                    transitionSet
                )
                changeTextVisibility(ShowText.SHORT)
            }

            @RequiresApi(34)
            override fun handleOnBackProgressed(backEvent: BackEvent) {
                // Play the transition as the user swipes back
                if (controller?.isReady == true) {
                    controller?.currentFraction = backEvent.progress
                }
            }

            override fun handleOnBackPressed() {
                // Finish playing the transition when the user commits back
                controller?.animateToEnd()
                this.isEnabled = false
            }

            @RequiresApi(34)
            override fun handleOnBackCancelled() {
                // If the user cancels the back gesture, reset the state
                transition(ShowText.LONG)
            }
        }

        binding.shortText.setOnClickListener {
            transition(ShowText.LONG)
            callback.isEnabled = true
        }

        this.requireActivity().onBackPressedDispatcher.addCallback(callback)
    }

    private fun transition(showText: ShowText) {
        TransitionManager.beginDelayedTransition(
            binding.card,
            transitionSet
        )
        changeTextVisibility(showText)
    }

    enum class ShowText { SHORT, LONG }
    private fun changeTextVisibility(showText: ShowText) {
        when (showText) {
            ShowText.SHORT -> {
                binding.shortText.isVisible = true
                binding.longText.isVisible = false
            }
            ShowText.LONG -> {
                binding.shortText.isVisible = false
                binding.longText.isVisible = true
            }
        }
    }
}
```

### Use the Progress APIs with AndroidX Transitions
```xml
<?xml version="1.0" encoding="utf-8"?>
...
    <androidx.constraintlayout.widget.ConstraintLayout
        android:id="@+id/card"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        ...>

        <TextView
            android:id="@+id/short_text"
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            ... />

        <TextView
            android:id="@+id/long_text"
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:visibility="gone"
            .../>

    </androidx.constraintlayout.widget.ConstraintLayout>
```

### Declare dependencies
```
[versions]
navigationevent = "1.0.0"

[libraries]
# NavigationEvent libraries
androidx-navigationevent = { module = "androidx.navigationevent:navigationevent", version.ref = "navigationevent" }
androidx-navigationevent-compose = { module = "androidx.navigationevent:navigationevent-compose", version.ref = "navigationevent" }
```

### Declare dependencies
```
[versions]
compileSdk = "36"
```

### Declare dependencies
```kotlin
dependencies {
  ...
  implementation(libs.androidx.navigationevent)
  implementation(libs.androidx.navigationevent.compose)
}
```

### Handle back gestures and predictive back animations 

 
 
 
 

 
 
 Stay organiz
```kotlin
val myHandler = object: NavigationEventHandler<NavigationEventInfo>(
    initialInfo = NavigationEventInfo.None,
    isBackEnabled = true
) {
    override fun onBackStarted(event: NavigationEvent) {
        // Prepare for the back event
    }

    override fun onBackProgressed(event: NavigationEvent) {
        // Use event.progress for predictive animations
    }

    // This is the required method for final event handling
    override fun onBackCompleted() {
        // Complete the back event
    }

    override fun onBackCancelled() {
        // Cancel the back event
    }
}NavEventSnippets.kt
```

### Handle back gestures and predictive back animations 

 
 
 
 

 
 
 Stay organiz
```
navigationEventDispatcher.addHandler(myHandler)NavEventSnippets.kt
```

### Handle back gestures and predictive back animations 

 
 
 
 

 
 
 Stay organiz
```
myHandler.remove()NavEventSnippets.kt
```

### Intercept back with Jetpack Compose
```kotlin
@Composable
public fun NavigationBackHandler(
    state: NavigationEventState<out NavigationEventInfo>,
    isBackEnabled: Boolean = true,
    onBackCancelled: () -> Unit = {},
    onBackCompleted: () -> Unit,
){

}NavEventSnippets.kt
```

### Intercept back with Jetpack Compose
```kotlin
@Composable
fun HandlingBackWithTransitionState(
    onNavigateUp: () -> Unit
) {
    val navigationState = rememberNavigationEventState(
        currentInfo = NavigationEventInfo.None
    )
    val transitionState = navigationState.transitionState
    // React to predictive back transition updates
    when (transitionState) {
        is NavigationEventTransitionState.InProgress -> {
            val progress = transitionState.latestEvent.progress
            // Use progress (0f..1f) to update UI during the gesture
        }
        is NavigationEventTransitionState.Idle -> {
            // Reset any temporary UI state if the gesture is cancelled
        }
    }
    NavigationBackHandler(
        state = navigationState,
        onBackCancelled = {
            // Called if the back gesture is cancelled
        },
        onBackCompleted = {
            // Called when the back gesture fully completes
            onNavigateUp()
        }
    )
}NavEventSnippets.kt
```

### Access the back gesture or swipe edge in Compose
```kotlin
object Routes {
    const val SCREEN_A = "Screen A"
    const val SCREEN_B = "Screen B"
}

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            var state by remember { mutableStateOf(Routes.SCREEN_A) }
            val backEventState = rememberNavigationEventState<NavigationEventInfo>(currentInfo = NavigationEventInfo.None)
            when (state) {
                Routes.SCREEN_A -> {
                    ScreenA(onNavigate = { state = Routes.SCREEN_B })
                }
                else -> {
                    if (backEventState.transitionState is NavigationEventTransitionState.InProgress) {
                        ScreenA(onNavigate = { })
                    }
                    ScreenB(
                        backEventState = backEventState,
                        onBackCompleted = { state = Routes.SCREEN_A }
                    )
                }
            }
        }
    }
}

@Composable
fun ScreenB(
    backEventState: NavigationEventState<NavigationEventInfo>,
    onBackCompleted: () -> Unit = {},
) {
    val transitionState = backEventState.transitionState
    val latestEvent =
        (transitionState as? NavigationEventTransitionState.InProgress)
            ?.latestEvent
    val backProgress = latestEvent?.progress ?: 0f
    val swipeEdge = latestEvent?.swipeEdge ?: NavigationEvent.EDGE_LEFT
    if (transitionState is NavigationEventTransitionState.InProgress) {
        Log.d("BackGesture", "Progress: ${transitionState.latestEvent.progress}")
    } else if (transitionState is NavigationEventTransitionState.Idle) {
        Log.d("BackGesture", "Idle")
    }
    val animatedScale by animateFloatAsState(
        targetValue = 1f - (backProgress * 0.1f),
        label = "ScaleAnimation"
    )
    val windowInfo = LocalWindowInfo.current
    val density = LocalDensity.current
    val maxShift = remember(windowInfo, density) {
        val widthDp = with(density) { windowInfo.containerSize.width.toDp() }
        (widthDp.value / 20f) - 8
    }
    val offsetX = when (swipeEdge) {
        EDGE_LEFT -> (backProgress * maxShift).dp
        EDGE_RIGHT -> (-backProgress * maxShift).dp
        else -> 0.dp
    }
    NavigationBackHandler(
        state = backEventState,
        onBackCompleted = onBackCompleted,
        isBackEnabled = true
    )
    Box(
        modifier = Modifier
            .offset(x = offsetX)
            .scale(animatedScale)
    ){
        // Rest of UI
    }
}NavEventSnippets.kt
```

### Declare a NavigationEventDispatcher
```kotlin
class MyComponent: NavigationEventDispatcherOwner {
    override val navigationEventDispatcher: NavigationEventDispatcher =
        NavigationEventDispatcher()
}NavEventSnippets.kt
```

### Declare a NavigationEventDispatcher
```kotlin
class MyCustomActivity : ComponentActivity() {
    fun addMyHandler() {
        // navigationEventDispatcher provided by the ComponentActivity
        navigationEventDispatcher.addHandler(myNavigationEventHandler)
    }
}NavEventSnippets.kt
```

### Add a NavigationEventInput
```kotlin
public class MyInput : NavigationEventInput() {
    @MainThread
    public fun backStarted(event: NavigationEvent) {
        dispatchOnBackStarted(event)
    }

    @MainThread
    public fun backProgressed(event: NavigationEvent) {
        dispatchOnBackProgressed(event)
    }

    @MainThread
    public fun backCancelled() {
        dispatchOnBackCancelled()
    }

    @MainThread
    public fun backCompleted() {
        dispatchOnBackCompleted()
    }
}NavEventSnippets.kt
```

### Add a NavigationEventInput
```
navigationEventDispatcher.addInput(MyInput())NavEventSnippets.kt
```

### Clean up resources with dispose()
```
navigationEventDispatcher.dispose()NavEventSnippets.kt
```

### Implementing global navigation in a responsive UI
```xml
<!-- res/layout-w960dp/navigation_activity.xml -->
<RelativeLayout
   xmlns:android="http://schemas.android.com/apk/res/android"
   xmlns:app="http://schemas.android.com/apk/res-auto"
   xmlns:tools="http://schemas.android.com/tools"
   android:layout_width="match_parent"
   android:layout_height="match_parent"
   tools:context="com.example.android.codelabs.navigation.MainActivity">

   <com.google.android.material.navigation.NavigationView
       android:id="@+id/nav_view"
       android:layout_width="wrap_content"
       android:layout_height="match_parent"
       android:layout_alignParentStart="true"
       app:elevation="0dp"
       app:headerLayout="@layout/nav_view_header"
       app:menu="@menu/nav_drawer_menu" />

   <View
       android:layout_width="1dp"
       android:layout_height="match_parent"
       android:layout_toEndOf="@id/nav_view"
       android:background="?android:attr/listDivider" />

   <androidx.appcompat.widget.Toolbar
       android:id="@+id/toolbar"
       android:layout_width="match_parent"
       android:layout_height="wrap_content"
       android:layout_alignParentTop="true"
       android:layout_toEndOf="@id/nav_view"
       android:background="@color/colorPrimary"
       android:theme="@style/ThemeOverlay.MaterialComponents.Dark.ActionBar" />

   <androidx.fragment.app.FragmentContainerView
       android:id="@+id/my_nav_host_fragment"
       android:name="androidx.navigation.fragment.NavHostFragment"
       android:layout_width="match_parent"
       android:layout_height="match_parent"
       android:layout_below="@id/toolbar"
       android:layout_toEndOf="@id/nav_view"
       app:defaultNavHost="true"
       app:navGraph="@navigation/mobile_navigation" />
</RelativeLayout>
```

### Implementing global navigation in a responsive UI
```xml
<!-- res/layout-h470dp/navigation_activity.xml -->
<LinearLayout
   xmlns:android="http://schemas.android.com/apk/res/android"
   xmlns:app="http://schemas.android.com/apk/res-auto"
   xmlns:tools="http://schemas.android.com/tools"
   android:layout_width="match_parent"
   android:layout_height="match_parent"
   android:orientation="vertical"
   tools:context="com.example.android.codelabs.navigation.MainActivity">

   <androidx.appcompat.widget.Toolbar
       android:id="@+id/toolbar"
       android:layout_width="match_parent"
       android:layout_height="wrap_content"
       android:background="@color/colorPrimary"
       android:theme="@style/ThemeOverlay.MaterialComponents.Dark.ActionBar" />

   <androidx.fragment.app.FragmentContainerView
       android:id="@+id/my_nav_host_fragment"
       android:name="androidx.navigation.fragment.NavHostFragment"
       android:layout_width="match_parent"
       android:layout_height="0dp"
       android:layout_weight="1"
       app:defaultNavHost="true"
       app:navGraph="@navigation/mobile_navigation" />

   <com.google.android.material.bottomnavigation.BottomNavigationView
       android:id="@+id/bottom_nav_view"
       android:layout_width="match_parent"
       android:layout_height="wrap_content"
       app:menu="@menu/bottom_nav_menu" />
</LinearLayout>
```

### Implementing global navigation in a responsive UI
```xml
<!-- res/layout/navigation_activity.xml -->
<androidx.drawerlayout.widget.DrawerLayout
   xmlns:android="http://schemas.android.com/apk/res/android"
   xmlns:app="http://schemas.android.com/apk/res-auto"
   xmlns:tools="http://schemas.android.com/tools"
   android:id="@+id/drawer_layout"
   android:layout_width="match_parent"
   android:layout_height="match_parent"
   tools:context="com.example.android.codelabs.navigation.MainActivity">

   <LinearLayout
       android:layout_width="match_parent"
       android:layout_height="match_parent"
       android:orientation="vertical">

       <androidx.appcompat.widget.Toolbar
           android:id="@+id/toolbar"
           android:layout_width="match_parent"
           android:layout_height="wrap_content"
           android:background="@color/colorPrimary"
           android:theme="@style/ThemeOverlay.MaterialComponents.Dark.ActionBar" />

       <androidx.fragment.app.FragmentContainerView
           android:id="@+id/my_nav_host_fragment"
           android:name="androidx.navigation.fragment.NavHostFragment"
           android:layout_width="match_parent"
           android:layout_height="match_parent"
           app:defaultNavHost="true"
           app:navGraph="@navigation/mobile_navigation" />
   </LinearLayout>

   <com.google.android.material.navigation.NavigationView
       android:id="@+id/nav_view"
       android:layout_width="wrap_content"
       android:layout_height="match_parent"
       android:layout_gravity="start"
       app:menu="@menu/nav_drawer_menu" />
</androidx.drawerlayout.widget.DrawerLayout>
```

### Implementing global navigation in a responsive UI
```kotlin
class MainActivity : AppCompatActivity() {

   private lateinit var appBarConfiguration : AppBarConfiguration

   override fun onCreate(savedInstanceState: Bundle?) {
      super.onCreate(savedInstanceState)
      setContentView(R.layout.navigation_activity)
      val drawerLayout : DrawerLayout? = findViewById(R.id.drawer_layout)
      appBarConfiguration = AppBarConfiguration(
                  setOf(R.id.home_dest, R.id.deeplink_dest),
                  drawerLayout)

      ...

      // Initialize the app bar with the navigation drawer if present.
      // If the drawerLayout is not null here, a Navigation button will be added
      // to the app bar whenever the user is on a top-level destination.
      setupActionBarWithNavController(navController, appBarConfig)

      // Initialize the NavigationView if it is present,
      // so that clicking an item takes
      // the user to the appropriate destination.
      val sideNavView = findViewById<NavigationView>(R.id.nav_view)
      sideNavView?.setupWithNavController(navController)

      // Initialize the BottomNavigationView if it is present,
      // so that clicking an item takes
      // the user to the appropriate destination.
      val bottomNav = findViewById<BottomNavigationView>(R.id.bottom_nav_view)
      bottomNav?.setupWithNavController(navController)

      ...
    }

    ...
}
```

### Destination names
```xml
<navigation ...>
    <fragment
        android:id="@+id/my_dest"
        android:name="com.example.MyFragment"
        android:label="@string/my_dest_label"
        tools:layout="@layout/my_fragment" />
    ...
```

### Implement Swipe Views
```xml
<androidx.viewpager2.widget.ViewPager2
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/pager"
    android:layout_width="match_parent"
    android:layout_height="match_parent" />
```

### Implement Swipe Views
```kotlin
class CollectionDemoFragment : Fragment() {
    // When requested, this adapter returns a DemoObjectFragment,
    // representing an object in the collection.
    private lateinit var demoCollectionAdapter: DemoCollectionAdapter
    private lateinit var viewPager: ViewPager2

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.collection_demo, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        demoCollectionAdapter = DemoCollectionAdapter(this)
        viewPager = view.findViewById(R.id.pager)
        viewPager.adapter = demoCollectionAdapter
    }
}

class DemoCollectionAdapter(fragment: Fragment) : FragmentStateAdapter(fragment) {

    override fun getItemCount(): Int = 100

    override fun createFragment(position: Int): Fragment {
        // Return a NEW fragment instance in createFragment(int)
        val fragment = DemoObjectFragment()
        fragment.arguments = Bundle().apply {
            // Our object is just an integer :-P
            putInt(ARG_OBJECT, position + 1)
        }
        return fragment
    }
}

private const val ARG_OBJECT = "object"

// Instances of this class are fragments representing a single
// object in our collection.
class DemoObjectFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        return inflater.inflate(R.layout.fragment_collection_object, container, false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        arguments?.takeIf { it.containsKey(ARG_OBJECT) }?.apply {
            val textView: TextView = view.findViewById(android.R.id.text1)
            textView.text = getInt(ARG_OBJECT).toString()
        }
    }
}
```

### Add Tabs Using a TabLayout
```xml
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical">

    <com.google.android.material.tabs.TabLayout
        android:id="@+id/tab_layout"
        android:layout_width="match_parent"
        android:layout_height="wrap_content" />

    <androidx.viewpager2.widget.ViewPager2
        android:id="@+id/pager"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1" />

</LinearLayout>
```

### Add Tabs Using a TabLayout
```kotlin
class CollectionDemoFragment : Fragment() {
    ...
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        val tabLayout = view.findViewById(R.id.tab_layout)
        TabLayoutMediator(tabLayout, viewPager) { tab, position ->
            tab.text = "OBJECT ${(position + 1)}"
        }.attach()
    }
    ...
}
```

### Implement swipe views
```xml
<androidx.viewpager.widget.ViewPager
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/pager"
    android:layout_width="match_parent"
    android:layout_height="match_parent" />
```

### Project setup
```
[versions]
nav3Core = "1.0.1"
lifecycleViewmodelNav3 = "2.11.0-alpha02"
kotlinSerialization = "2.2.21"
kotlinxSerializationCore = "1.9.0"
material3AdaptiveNav3 = "1.3.0-alpha09"

[libraries]
# Core Navigation 3 libraries
androidx-navigation3-runtime = { module = "androidx.navigation3:navigation3-runtime", version.ref = "nav3Core" }
androidx-navigation3-ui = { module = "androidx.navigation3:navigation3-ui", version.ref = "nav3Core" }

# Optional add-on libraries
androidx-lifecycle-viewmodel-navigation3 = { module = "androidx.lifecycle:lifecycle-viewmodel-navigation3", version.ref = "lifecycleViewmodelNav3" }
kotlinx-serialization-core = { module = "org.jetbrains.kotlinx:kotlinx-serialization-core", version.ref = "kotlinxSerializationCore" }
androidx-material3-adaptive-navigation3 = { group = "androidx.compose.material3.adaptive", name = "adaptive-navigation3", version.ref = "material3AdaptiveNav3" }

[plugins]
# Optional plugins
jetbrains-kotlin-serialization = { id = "org.jetbrains.kotlin.plugin.serialization", version.ref = "kotlinSerialization"}
```

### Project setup
```kotlin
plugins {
    ...
    // Optional, provides the @Serialize annotation for autogeneration of Serializers.
    alias(libs.plugins.jetbrains.kotlin.serialization)
}

dependencies {
    ...
    implementation(libs.androidx.navigation3.ui)
    implementation(libs.androidx.navigation3.runtime)
    implementation(libs.androidx.lifecycle.viewmodel.navigation3)
    implementation(libs.androidx.material3.adaptive.navigation3)
    implementation(libs.kotlinx.serialization.core)
}
```

### Create a back stack
```kotlin
// Define keys that will identify content
data object ProductList
data class ProductDetail(val id: String)

@Composable
fun MyApp() {

    // Create a back stack, specifying the key the app should start with
    val backStack = remember { mutableStateListOf<Any>(ProductList) }

    // Supply your back stack to a NavDisplay so it can reflect changes in the UI
    // ...more on this below...

    // Push a key onto the back stack (navigate forward), the navigation library will reflect the change in state
    backStack.add(ProductDetail(id = "ABC"))

    // Pop a key off the back stack (navigate back), the navigation library will reflect the change in state
    backStack.removeLastOrNull()
}BasicSnippets.kt
```

### Create an Entry Provider function directly
```
entryProvider = { key ->
    when (key) {
        is ProductList -> NavEntry(key) { Text("Product List") }
        is ProductDetail -> NavEntry(
            key,
            metadata = mapOf("extraDataKey" to "extraDataValue")
        ) { Text("Product ${key.id} ") }

        else -> {
            NavEntry(Unit) { Text(text = "Invalid Key: $it") }
        }
    }
}BasicSnippets.kt
```

### Use the entryProvider DSL
```
entryProvider = entryProvider {
    entry<ProductList> { Text("Product List") }
    entry<ProductDetail>(
        metadata = mapOf("extraDataKey" to "extraDataValue")
    ) { key -> Text("Product ${key.id} ") }
}BasicSnippets.kt
```

### Display the back stack
```kotlin
data object Home
data class Product(val id: String)

@Composable
fun NavExample() {

    val backStack = remember { mutableStateListOf<Any>(Home) }

    NavDisplay(
        backStack = backStack,
        onBack = { backStack.removeLastOrNull() },
        entryProvider = { key ->
            when (key) {
                is Home -> NavEntry(key) {
                    ContentGreen("Welcome to Nav3") {
                        Button(onClick = {
                            backStack.add(Product("123"))
                        }) {
                            Text("Click to navigate")
                        }
                    }
                }

                is Product -> NavEntry(key) {
                    ContentBlue("Product ${key.id} ")
                }

                else -> NavEntry(Unit) { Text("Unknown route") }
            }
        }
    )
}BasicSnippets.kt
```

### Use rememberNavBackStack
```kotlin
@Serializable
data object Home : NavKey

@Composable
fun NavBackStack() {
    val backStack = rememberNavBackStack(Home)
}SavingStateSnippets.kt
```

### Scoping ViewModel s to NavEntry s
```
NavDisplay(
    entryDecorators = listOf(
        // Add the default decorators for managing scenes and saving state
        rememberSaveableStateHolderNavEntryDecorator(),
        // Then add the view model store decorator
        rememberViewModelStoreNavEntryDecorator()
    ),
    backStack = backStack,
    entryProvider = entryProvider { },
)SavingStateSnippets.kt
```

### Provide NavEntry metadata
```
when (key) {
    is Home -> NavEntry(key, metadata = mapOf("key" to "value")) {}
}MetadataSnippets.kt
```

### Provide NavEntry metadata
```
entry<Home>(metadata = mapOf("key" to "value")) { /* ... */ }
entry<Conversation>(metadata = { key: Conversation ->
    mapOf("key" to "value: ${key.id})")
}) { /* ... */ }MetadataSnippets.kt
```

### Define metadata keys
```
// For classes such as scene strategies or nav entry decorators, you can define the keys
// as nested object.
class MySceneStrategy<T : Any> : SceneStrategy<T> {

    // ...

    object MyStringMetadataKey : NavMetadataKey<String>
}

// An example from NavDisplay.
// Because NavDisplay is a function, the metadata keys are defined in an object with the same name.
public object NavDisplay {

    public object TransitionKey :
        NavMetadataKey<AnimatedContentTransitionScope<Scene<*>>.() -> ContentTransform>
}MetadataSnippets.kt
```

### Build metadata using the DSL
```
entry<Home>(
    metadata = metadata {
        put(NavDisplay.TransitionKey) { fadeIn() togetherWith fadeOut() }
        // An additional benefit of the metadata DSL is the ability to use conditional logic
        if (condition) {
            put(MySceneStrategy.MyStringMetadataKey, "Hello, world!")
        }
    }
) {
    // ...
}MetadataSnippets.kt
```

### Read metadata using metadata keys
```kotlin
// import androidx.navigation3.runtime.contains
// import androidx.navigation3.runtime.get

val hasMyString: Boolean = metadata.contains(MySceneStrategy.MyStringMetadataKey)
val myString: String? = metadata[MySceneStrategy.MyStringMetadataKey]MetadataSnippets.kt
```

### Separate navigation entries using extension functions
```kotlin
// import androidx.navigation3.runtime.EntryProviderScope
// import androidx.navigation3.runtime.NavKey

fun EntryProviderScope<NavKey>.featureAEntryBuilder() {
    entry<KeyA> {
        ContentRed("Screen A") {
            // Content for screen A
        }
    }
    entry<KeyA2> {
        ContentGreen("Screen A2") {
            // Content for screen A2
        }
    }
}ModularizationSnippets.kt
```

### Separate navigation entries using extension functions
```kotlin
// import androidx.navigation3.runtime.entryProvider
// import androidx.navigation3.ui.NavDisplay
NavDisplay(
    entryProvider = entryProvider {
        featureAEntryBuilder()
    },
    // ...
)ModularizationSnippets.kt
```

### Use dependency injection to add entries to the main app
```kotlin
// import dagger.Module
// import dagger.Provides
// import dagger.hilt.InstallIn
// import dagger.hilt.android.components.ActivityRetainedComponent
// import dagger.multibindings.IntoSet

@Module
@InstallIn(ActivityRetainedComponent::class)
object FeatureAModule {

    @IntoSet
    @Provides
    fun provideFeatureAEntryBuilder() : EntryProviderScope<NavKey>.() -> Unit = {
        featureAEntryBuilder()
    }
}ModularizationSnippets.kt
```

### Use dependency injection to add entries to the main app
```kotlin
// import android.os.Bundle
// import androidx.activity.ComponentActivity
// import androidx.activity.compose.setContent
// import androidx.navigation3.runtime.EntryProviderScope
// import androidx.navigation3.runtime.NavKey
// import androidx.navigation3.runtime.entryProvider
// import androidx.navigation3.ui.NavDisplay
// import javax.inject.Inject

class MainActivity : ComponentActivity() {

    @Inject
    lateinit var entryBuilders: Set<@JvmSuppressWildcards EntryProviderScope<NavKey>.() -> Unit>

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            NavDisplay(
                entryProvider = entryProvider {
                    entryBuilders.forEach { builder -> this.builder() }
                },
                // ...
            )
        }
    }
}ModularizationSnippets.kt
```

### Understand scene strategies
```kotlin
@Composable
public fun calculateScene(
    entries: List<NavEntry<T>>,
    onBack: (count: Int) -> Unit,
): Scene<T>?ScenesSnippets.kt
```

### Example: Single pane layout (default behavior)
```kotlin
data class SinglePaneScene<T : Any>(
    override val key: Any,
    val entry: NavEntry<T>,
    override val previousEntries: List<NavEntry<T>>,
) : Scene<T> {
    override val entries: List<NavEntry<T>> = listOf(entry)
    override val content: @Composable () -> Unit = { entry.Content() }
}

/**
 * A [SceneStrategy] that always creates a 1-entry [Scene] simply displaying the last entry in the
 * list.
 */
public class SinglePaneSceneStrategy<T : Any> : SceneStrategy<T> {
    override fun SceneStrategyScope<T>.calculateScene(entries: List<NavEntry<T>>): Scene<T>? =
        SinglePaneScene(
            key = entries.last().contentKey,
            entry = entries.last(),
            previousEntries = entries.dropLast(1)
        )
}ScenesSnippets.kt
```

### Example: Basic list-detail layout (custom Scene and strategy)
```kotlin
// --- ListDetailScene ---
/**
 * A [Scene] that displays a list and a detail [NavEntry] side-by-side in a 40/60 split.
 *
 */
class ListDetailScene<T : Any>(
    override val key: Any,
    override val previousEntries: List<NavEntry<T>>,
    val listEntry: NavEntry<T>,
    val detailEntry: NavEntry<T>,
) : Scene<T> {
    override val entries: List<NavEntry<T>> = listOf(listEntry, detailEntry)
    override val content: @Composable (() -> Unit) = {
        Row(modifier = Modifier.fillMaxSize()) {
            Column(modifier = Modifier.weight(0.4f)) {
                listEntry.Content()
            }
            Column(modifier = Modifier.weight(0.6f)) {
                detailEntry.Content()
            }
        }
    }
}

@Composable
fun <T : Any> rememberListDetailSceneStrategy(): ListDetailSceneStrategy<T> {
    val windowSizeClass = currentWindowAdaptiveInfo().windowSizeClass

    return remember(windowSizeClass) {
        ListDetailSceneStrategy(windowSizeClass)
    }
}

// --- ListDetailSceneStrategy ---
/**
 * A [SceneStrategy] that returns a [ListDetailScene] if the window is wide enough, the last item
 * is the backstack is a detail, and before it, at any point in the backstack is a list.
 */
class ListDetailSceneStrategy<T : Any>(val windowSizeClass: WindowSizeClass) : SceneStrategy<T> {

    override fun SceneStrategyScope<T>.calculateScene(entries: List<NavEntry<T>>): Scene<T>? {

        if (!windowSizeClass.isWidthAtLeastBreakpoint(WIDTH_DP_MEDIUM_LOWER_BOUND)) {
            return null
        }

        val detailEntry =
            entries.lastOrNull()?.takeIf { it.metadata.contains(DetailKey) } ?: return null
        val listEntry = entries.findLast { it.metadata.contains(ListKey) } ?: return null

        // We use the list's contentKey to uniquely identify the scene.
        // This allows the detail panes to be displayed instantly through recomposition, rather than
        // having NavDisplay animate the whole scene out when the selected detail item changes.
        val sceneKey = listEntry.contentKey

        return ListDetailScene(
            key = sceneKey,
            previousEntries = entries.dropLast(1),
            listEntry = listEntry,
            detailEntry = detailEntry
        )
    }

    object ListKey : NavMetadataKey<Boolean>
    object DetailKey : NavMetadataKey<Boolean>
    companion object {

        /**
         * Helper function to add metadata to a [NavEntry] indicating it can be displayed
         * as a list in the [ListDetailScene].
         */
        fun listPane() = metadata {
            put(ListKey, true)
        }

        /**
         * Helper function to add metadata to a [NavEntry] indicating it can be displayed
         * as a list in the [ListDetailScene].
         */
        fun detailPane() = metadata {
            put(DetailKey, true)
        }
    }
}ScenesSnippets.kt
```

### Example: Basic list-detail layout (custom Scene and strategy)
```kotlin
// Define your navigation keys
@Serializable
data object ConversationList : NavKey

@Serializable
data class ConversationDetail(val id: String) : NavKey

@Composable
fun MyAppContent() {
    val backStack = rememberNavBackStack(ConversationList)
    val listDetailStrategy = rememberListDetailSceneStrategy<NavKey>()

    NavDisplay(
        backStack = backStack,
        onBack = { backStack.removeLastOrNull() },
        sceneStrategies = listOf(listDetailStrategy),
        entryProvider = entryProvider {
            entry<ConversationList>(
                metadata = ListDetailSceneStrategy.listPane()
            ) {
                Column(modifier = Modifier.fillMaxSize()) {
                    Text(text = "I'm a Conversation List")
                    Button(onClick = { backStack.addDetail(ConversationDetail("123")) }) {
                        Text(text = "Open detail")
                    }
                }
            }
            entry<ConversationDetail>(
                metadata = ListDetailSceneStrategy.detailPane()
            ) {
                Text(text = "I'm a Conversation Detail")
            }
        }
    )
}

private fun NavBackStack<NavKey>.addDetail(detailRoute: ConversationDetail) {

    // Remove any existing detail routes, then add the new detail route
    removeIf { it is ConversationDetail }
    add(detailRoute)
}ScenesSnippets.kt
```

### Display list-detail content in a Material Adaptive Scene
```kotlin
@Serializable
object ProductList : NavKey

@Serializable
data class ProductDetail(val id: String) : NavKey

@Serializable
data object Profile : NavKey

class MaterialListDetailActivity : ComponentActivity() {

    @OptIn(ExperimentalMaterial3AdaptiveApi::class)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContent {
            Scaffold { paddingValues ->
                val backStack = rememberNavBackStack(ProductList)
                val listDetailStrategy = rememberListDetailSceneStrategy<NavKey>()

                NavDisplay(
                    backStack = backStack,
                    modifier = Modifier.padding(paddingValues),
                    onBack = { backStack.removeLastOrNull() },
                    sceneStrategies = listOf(listDetailStrategy),
                    entryProvider = entryProvider {
                        entry<ProductList>(
                            metadata = ListDetailSceneStrategy.listPane(
                                detailPlaceholder = {
                                    ContentYellow("Choose a product from the list")
                                }
                            )
                        ) {
                            ContentRed("Welcome to Nav3") {
                                Button(onClick = {
                                    backStack.add(ProductDetail("ABC"))
                                }) {
                                    Text("View product")
                                }
                            }
                        }
                        entry<ProductDetail>(
                            metadata = ListDetailSceneStrategy.detailPane()
                        ) { product ->
                            ContentBlue("Product ${product.id} ", Modifier.background(PastelBlue)) {
                                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                    Button(onClick = {
                                        backStack.add(Profile)
                                    }) {
                                        Text("View profile")
                                    }
                                }
                            }
                        }
                        entry<Profile>(
                            metadata = ListDetailSceneStrategy.extraPane()
                        ) {
                            ContentGreen("Profile")
                        }
                    }
                )
            }
        }
    }
}MaterialScenesSnippets.kt
```

### Create a scene decorator strategy
```kotlin
class MySceneDecoratorStrategy<T : Any> : SceneDecoratorStrategy<T> {


    override fun SceneDecoratorStrategyScope<T>.decorateScene(scene: Scene<T>): Scene<T> {
        // `shouldDecorate` determines if the scene should be decorated based on scene.metadata,
        // scene.entries.metadata, or any other relevant state.
        return if (shouldDecorate(scene)) {
            MyDecoratingScene(scene)
        } else {
            scene
        }
    }

}

class MyDecoratingScene<T : Any>(scene: Scene<T>) : Scene<T> {

    // ...

    override val content = @Composable {
        scene.content()
    }
}SceneDecoratorSnippets.kt
```

### Use scene decorator strategies
```
NavDisplay(
    // ...
    sceneDecoratorStrategies = listOf(firstSceneDecoratorStrategy, secondSceneDecoratorStrategy)
)SceneDecoratorSnippets.kt
```

### Copy properties
```kotlin
class CopyingScene<T : Any>(scene: Scene<T>) : Scene<T> {
    override val entries = scene.entries
    override val previousEntries = scene.previousEntries
    override val metadata = scene.metadata

    // ...
}SceneDecoratorSnippets.kt
```

### Maintain animations
```kotlin
class DerivedKeyScene<T : Any>(scene: Scene<T>) : Scene<T> {
    override val key = scene::class to scene.key

    // ...
}SceneDecoratorSnippets.kt
```

### Override transitions at the Scene level
```kotlin
@Serializable
data object ScreenA : NavKey

@Serializable
data object ScreenB : NavKey

@Serializable
data object ScreenC : NavKey

class AnimatedNavDisplayActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {

            Scaffold { paddingValues ->

                val backStack = rememberNavBackStack(ScreenA)

                NavDisplay(
                    backStack = backStack,
                    onBack = { backStack.removeLastOrNull() },
                    entryProvider = entryProvider {
                        entry<ScreenA> {
                            ContentOrange("This is Screen A") {
                                Button(onClick = { backStack.add(ScreenB) }) {
                                    Text("Go to Screen B")
                                }
                            }
                        }
                        entry<ScreenB> {
                            ContentMauve("This is Screen B") {
                                Button(onClick = { backStack.add(ScreenC) }) {
                                    Text("Go to Screen C")
                                }
                            }
                        }
                        entry<ScreenC>(
                            metadata = metadata {
                                put(NavDisplay.TransitionKey) {
                                    // Slide new content up, keeping the old content in place underneath
                                    slideInVertically(
                                        initialOffsetY = { it },
                                        animationSpec = tween(1000)
                                    ) togetherWith ExitTransition.KeepUntilTransitionsFinished
                                }
                                put(NavDisplay.PopTransitionKey) {
                                    // Slide old content down, revealing the new content in place underneath
                                    EnterTransition.None togetherWith
                                            slideOutVertically(
                                                targetOffsetY = { it },
                                                animationSpec = tween(1000)
                                            )
                                }
                                put(NavDisplay.PredictivePopTransitionKey) {
                                    // Slide old content down, revealing the new content in place underneath
                                    EnterTransition.None togetherWith
                                            slideOutVertically(
                                                targetOffsetY = { it },
                                                animationSpec = tween(1000)
                                            )
                                }
                            }
                        ) {
                            ContentGreen("This is Screen C")
                        }
                    },
                    transitionSpec = {
                        // Slide in from right when navigating forward
                        slideInHorizontally(initialOffsetX = { it }) togetherWith
                            slideOutHorizontally(targetOffsetX = { -it })
                    },
                    popTransitionSpec = {
                        // Slide in from left when navigating back
                        slideInHorizontally(initialOffsetX = { -it }) togetherWith
                            slideOutHorizontally(targetOffsetX = { it })
                    },
                    predictivePopTransitionSpec = {
                        // Slide in from left when navigating back
                        slideInHorizontally(initialOffsetX = { -it }) togetherWith
                            slideOutHorizontally(targetOffsetX = { it })
                    },
                    modifier = Modifier.padding(paddingValues)
                )
            }
        }
    }
}AnimationSnippets.kt
```

### Transition nav entries between scenes
```
SharedTransitionLayout {
    NavDisplay(
        // ...
        sharedTransitionScope = this
    )
}AnimationSnippets.kt
```

### Create a custom decorator
```kotlin
// import androidx.navigation3.runtime.NavEntryDecorator
class CustomNavEntryDecorator<T : Any> : NavEntryDecorator<T>(
    decorate = { entry ->
        Log.d("CustomNavEntryDecorator", "entry with ${entry.contentKey} entered composition and was decorated")
        entry.Content()
    },
    onPop = { contentKey -> Log.d("CustomNavEntryDecorator", "entry with $contentKey was popped") }
)DecoratorSnippets.kt
```

### Include the default decorator
```kotlin
// import androidx.navigation3.runtime.rememberSaveableStateHolderNavEntryDecorator
NavDisplay(
    entryDecorators = listOf(
        rememberSaveableStateHolderNavEntryDecorator(),
        remember { CustomNavEntryDecorator() }
    ),
    // ...
)DecoratorSnippets.kt
```

### Migrate from Navigation 2 to Navigation 3
```
Migrate from Navigation 2 to Navigation 3 using the official
migration guide.
```

### Step 1: Add Navigation 3 dependencies
```
[versions]
nav3Core = "1.0.0"

# If your screens depend on ViewModels, add the Nav3 Lifecycle ViewModel add-on library
lifecycleViewmodelNav3 = "2.10.0-rc01"

[libraries]
# Core Navigation 3 libraries
androidx-navigation3-runtime = { module = "androidx.navigation3:navigation3-runtime", version.ref = "nav3Core" }
androidx-navigation3-ui = { module = "androidx.navigation3:navigation3-ui", version.ref = "nav3Core" }

# Add-on libraries (only add if you need them)
androidx-lifecycle-viewmodel-navigation3 = { module = "androidx.lifecycle:lifecycle-viewmodel-navigation3", version.ref = "lifecycleViewmodelNav3" }
```

### Step 1: Add Navigation 3 dependencies
```kotlin
dependencies {
    implementation(libs.androidx.navigation3.ui)
    implementation(libs.androidx.navigation3.runtime)

    // If using the ViewModel add-on library
    implementation(libs.androidx.lifecycle.viewmodel.navigation3)
}
```

### Step 2: Update navigation routes to implement the NavKey interface
```
@Serializable data object RouteA
```

### Step 2: Update navigation routes to implement the NavKey interface
```
@Serializable data object RouteA : NavKey
```

### Step 3.1: Create a navigation state holder
```kotlin
// package com.example.project

import androidx.compose.runtime.Composable
import androidx.compose.runtime.MutableState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSerializable
import androidx.compose.runtime.setValue
import androidx.compose.runtime.snapshots.SnapshotStateList
import androidx.compose.runtime.toMutableStateList
import androidx.navigation3.runtime.NavBackStack
import androidx.navigation3.runtime.NavEntry
import androidx.navigation3.runtime.NavKey
import androidx.navigation3.runtime.rememberDecoratedNavEntries
import androidx.navigation3.runtime.rememberNavBackStack
import androidx.navigation3.runtime.rememberSaveableStateHolderNavEntryDecorator
import androidx.navigation3.runtime.serialization.NavKeySerializer
import androidx.savedstate.compose.serialization.serializers.MutableStateSerializer

/**
 * Create a navigation state that persists config changes and process death.
 */
@Composable
fun rememberNavigationState(
    startRoute: NavKey,
    topLevelRoutes: Set<NavKey>
): NavigationState {

    val topLevelRoute = rememberSerializable(
        startRoute, topLevelRoutes,
        serializer = MutableStateSerializer(NavKeySerializer())
    ) {
        mutableStateOf(startRoute)
    }

    val backStacks = topLevelRoutes.associateWith { key -> rememberNavBackStack(key) }

    return remember(startRoute, topLevelRoutes) {
        NavigationState(
            startRoute = startRoute,
            topLevelRoute = topLevelRoute,
            backStacks = backStacks
        )
    }
}

/**
 * State holder for navigation state.
 *
 * @param startRoute - the start route. The user will exit the app through this route.
 * @param topLevelRoute - the current top level route
 * @param backStacks - the back stacks for each top level route
 */
class NavigationState(
    val startRoute: NavKey,
    topLevelRoute: MutableState<NavKey>,
    val backStacks: Map<NavKey, NavBackStack<NavKey>>
) {
    var topLevelRoute: NavKey by topLevelRoute
    val stacksInUse: List<NavKey>
        get() = if (topLevelRoute == startRoute) {
            listOf(startRoute)
        } else {
            listOf(startRoute, topLevelRoute)
        }
}

/**
 * Convert NavigationState into NavEntries.
 */
@Composable
fun NavigationState.toEntries(
    entryProvider: (NavKey) -> NavEntry<NavKey>
): SnapshotStateList<NavEntry<NavKey>> {

    val decoratedEntries = backStacks.mapValues { (_, stack) ->
        val decorators = listOf(
            rememberSaveableStateHolderNavEntryDecorator<NavKey>(),
        )
        rememberDecoratedNavEntries(
            backStack = stack,
            entryDecorators = decorators,
            entryProvider = entryProvider
        )
    }

    return stacksInUse
        .flatMap { decoratedEntries[it] ?: emptyList() }
        .toMutableStateList()
}
```

### Step 3.2: Create an object that modifies navigation state in response to events
```kotlin
// package com.example.project

import androidx.navigation3.runtime.NavKey

/**
 * Handles navigation events (forward and back) by updating the navigation state.
 */
class Navigator(val state: NavigationState){
    fun navigate(route: NavKey){
        if (route in state.backStacks.keys){
            // This is a top level route, just switch to it.
            state.topLevelRoute = route
        } else {
            state.backStacks[state.topLevelRoute]?.add(route)
        }
    }

    fun goBack(){
        val currentStack = state.backStacks[state.topLevelRoute] ?:
        error("Stack for ${state.topLevelRoute} not found")
        val currentRoute = currentStack.last()

        // If we're at the base of the current route, go back to the start route stack.
        if (currentRoute == state.topLevelRoute){
            state.topLevelRoute = state.startRoute
        } else {
            currentStack.removeLastOrNull()
        }
    }
}
```

### Step 3.3: Create the NavigationState and Navigator
```kotlin
val navigationState = rememberNavigationState(
    startRoute = <Insert your starting route>,
    topLevelRoutes = <Insert your set of top level routes>
)

val navigator = remember { Navigator(navigationState) }
```

### Step 4: Replace NavController
```kotlin
val isSelected = navController.currentBackStackEntryAsState().value?.destination.isRouteInHierarchy(key::class)

fun NavDestination?.isRouteInHierarchy(route: KClass<*>) =
    this?.hierarchy?.any {
        it.hasRoute(route)
    } ?: false
```

### Step 4: Replace NavController
```kotlin
val isSelected = key == navigationState.topLevelRoute
```

### Step 5.1: Create an entryProvider
```kotlin
val entryProvider = entryProvider {

}
```

### Step 5.2: Move destinations into the entryProvider
```kotlin
import androidx.navigation.NavDestination
import androidx.navigation.NavDestination.Companion.hasRoute
import androidx.navigation.NavDestination.Companion.hierarchy
import androidx.navigation.NavGraphBuilder
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.dialog
import androidx.navigation.compose.navigation
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navOptions
import androidx.navigation.toRoute

@Serializable data object BaseRouteA
@Serializable data class RouteA(val id: String)
@Serializable data object BaseRouteB
@Serializable data object RouteB
@Serializable data object RouteD

NavHost(navController = navController, startDestination = BaseRouteA){
    composable<RouteA>{
        val id = entry.toRoute<RouteA>().id
        ScreenA(title = "Screen has ID: $id")
    }
    featureBSection()
    dialog<RouteD>{ ScreenD() }
}

fun NavGraphBuilder.featureBSection() {
    navigation<BaseRouteB>(startDestination = RouteB) {
        composable<RouteB> { ScreenB() }
    }
}
```

### Step 5.2: Move destinations into the entryProvider
```kotlin
import androidx.navigation3.runtime.EntryProviderScope
import androidx.navigation3.runtime.NavKey
import androidx.navigation3.runtime.entryProvider
import androidx.navigation3.scene.DialogSceneStrategy

@Serializable data class RouteA(val id: String) : NavKey
@Serializable data object RouteB : NavKey
@Serializable data object RouteD : NavKey

val entryProvider = entryProvider {
    entry<RouteA>{ key -> ScreenA(title = "Screen has ID: ${key.id}") }
    featureBSection()
    entry<RouteD>(metadata = DialogSceneStrategy.dialog()){ ScreenD() }
}

fun EntryProviderScope<NavKey>.featureBSection() {
    entry<RouteB> { ScreenB() }
}
```

### Step 6: Replace NavHost with NavDisplay
```kotlin
import androidx.navigation3.ui.NavDisplay

NavDisplay(
    entries = navigationState.toEntries(entryProvider),
    onBack = { navigator.goBack() },
    sceneStrategies = remember { listOf(DialogSceneStrategy()) }
)
```

## Pitfalls
- Warning: Don't pass your NavController to your composables. Expose an event as
described here.
- Warning: You should only call navigate() as part of a callback and not as part
of your composable itself. This avoids calling navigate() on every
recomposition.
- Caution: When navigating using NavDeepLinkRequest , the back stack does not 
reset. This behavior is unlike other forms of deep link navigation .
However, popUpTo() and popUpToInclusive() still remove destinations from the
back stack just as though you had navigated using an ID.
- Warning: You can encounter problems when creating the NavHostFragment using
 FragmentContainerView or when manually adding the NavHostFragment to your
activity using a FragmentTransaction . If you do so, you can cause
 Navigation.findNavController(Activity, @IdRes int) to fail if you attempt to
retr
- Caution: Instead of passing a type to composable() , you can pass a route 
string or an integer id . However, this makes it much more difficult to manage
passing additional arguments to the destination.
- Note: The DSL example does not define actions because they don't apply in that
context. When using the DSL, use NavController.navigate() directly .
- Caution: An ActivityNotFoundException is thrown if you attempt to navigate to
this destination and either the specified app is not installed on the device
or the destination app does not have an Activity defined in its manifest with
a matching intent-filter .
- Caution: An exception is thrown if any required arguments are missing from the
navigation request.
- Warning: The navigation actions API is available only when using the views UI
framework.
- Caution: You can't use the Navigation Editor for your app if you are using
Compose or if you have built your navigation graph programmatically using the
Kotlin DSL.
- Note: You must change the Class attribute of your placeholders to existing
destinations before running your app. Placeholders don't cause compilation
errors, and if you attempt to navigate to a placeholder destination, the app
throws a runtime exception.
- Warning: Safe Args is only available for Android views and fragments. If you are
using Compose, see the guide on type safe navigation .
- Caution: Passing complex data structures over arguments is considered an
poor practice. Each destination should be responsible for loading UI data based
on the minimum necessary information, such as item IDs. This simplifies
process recreation and avoids potential data inconsistencies.
- Note: when manually calling setGraph() with arguments, you must not use
the app:navGraph attribute when creating the NavHostFragment in XML as that
internally calls setGraph() without any arguments, resulting in your graph and
start destination being created twice.
- Caution: When manually calling
 setGraph() , note the following: 
 
 Don't use the app:navGraph element when adding the
 NavHostFragment in XML. 
 Don't call NavHostFragment.create(@NavigationRes int) . 
 Don't use any other APIs that rely solely on the
 R.navigation ID to inflate and set your graph
- Caution: The package name of the dynamic feature module is generated
automatically by the build toolchain, and any values in the
 AndroidManifest.xml or build.gradle in your dynamic module will be ignored.
- Note: Safe Args don't support cross-module navigation, as there isn't
direct action to the destination. In the previous example, although a
 Directions class would be generated for the target destination in settings,
you aren't able to access the generated class from the classpath of the
home module
- Caution: If you pass a Toolbar as the argument to setSupportActionBar() ,
the ActionBar assumes complete ownership of that Toolbar and you must not
use any Toolbar APIs after that call. You can use the support for the
 ActionBar to connect the ActionBar to NavController .
- Note: When using a Toolbar , Navigation automatically handles click events for
the Navigation button, so you do not need to override
 onSupportNavigateUp() .
- Note: When using NavigationUI , the top app bar helpers
automatically transition between the drawer icon and the Up icon as the current
destination changes. You don't need to use
 ActionBarDrawerToggle .
- Important: To ensure success, approach migration as an iterative process,
thoroughly testing your app with each step. While a single-activity architecture
allows you to take full advantage of the Navigation component, you do not need
to fully migrate your app to benefit from Navigation.
- Note: In this case, you should avoid setting the app:NavGraph attribute in the
 NavHostFragment definition, because doing so results in inflating and setting
the navigation graph twice.
- Note: KeyEvent.KEYCODE_BACK is not deprecated as there are some supported use
cases of KeyEvent.KEYCODE_BACK ; however, intercepting back events from
 KeyEvent.KEYCODE_BACK is no longer supported.
- Note: The Web platform has unique navigation handling, where the browser
controls the back stack state. This requires synchronization between the browser
window and the application's navigation stack. The question mark represents
behavior that is inconsistent because web browsers don't have a single
- Warning: NavDisplay doesn't decorate Scene instances that implement
 OverlayScene . This is because the content of an OverlayScene is
expected to be rendered in a separate window, so any wrapping content would
never be rendered.

## Decision Tables
### Key concepts
| Concept | Purpose | Type |
| --- | --- | --- |
| Host | A UI element that contains the current navigation destination. That is, when a user navigates through an app, the app essentially swaps destinations in and out of the navigation host. | Compose : NavHost 
 Fragments : NavHostFragment |
| Graph | A data structure that defines all the navigation destinations within the app and how they connect together. | NavGraph |
| Controller | The central coordinator for managing navigation between destinations. The controller offers methods for navigating between destinations, handling deep links, managing the back stack, and more. | NavController |
| Destination | A node in the navigation graph. When the user navigates to this node, the host displays its content. | NavDestination Typically created when constructing the navigation graph. |
| Route | Uniquely identifies a destination and any data required by it. You can navigate using routes. Routes take you to destinations. | Any serializable data type. |

### Destination types
| Type | Description | Use cases |
| --- | --- | --- |
| Hosted | Fills the entire navigation host. That is, the size of a hosted destination is the same as the size of the navigation host and previous destinations are not visible. | Main and detail screens. |
| Dialog | Presents overlay UI components. This UI is not tied to the location of the navigation host or its size. Previous destinations are visible underneath the destination. | Alerts, selections, forms. |
| Activity | Represents unique screens or features within the app. | Serve as an exit point to the navigation graph that starts a new Android activity that is managed separately from the Navigation component. 
 In modern Android development, an app consists of a single activity. Activity destinations are therefore best used when interacting with third party activities or as part of the migration process . |

### Supported argument types
| Type | app:argType syntax | Support for default values | Handled by routes | Nullable |
| --- | --- | --- | --- | --- |
| Integer | app:argType="integer" | Yes | Yes | No |
| Float | app:argType="float" | Yes | Yes | No |
| Long | app:argType="long" | Yes - Default values must always end with an 'L' suffix (e.g. "123L"). | Yes | No |
| Boolean | app:argType="boolean" | Yes - "true" or "false" | Yes | No |
| String | app:argType="string" | Yes | Yes | Yes |
| Resource Reference | app:argType="reference" | Yes - Default values must be in the form of "@resourceType/resourceName" (e.g. "@style/myCustomStyle") or "0" | Yes | No |
| Custom Parcelable | app:argType="<type>", where <type> is the fully-qualified class name of the Parcelable | Supports a default value of "@null". Does not support other default values. | No | Yes |
| Custom Serializable | app:argType="<type>", where <type> is the fully-qualified class name of the Serializable | Supports a default value of "@null". Does not support other default values. | No | Yes |
| Custom Enum | app:argType="<type>", where <type> is the fully-qualified name of the enum | Yes - Default values must match the unqualified name (e.g. "SUCCESS" to match MyEnum.SUCCESS). | No | No |

### Update an app that uses custom back navigation
| How your app handles back navigation | Recommended migration path (link on this page) |
| --- | --- |
| AndroidX APIs | Migrate an existing AndroidX back implementation |
| Unsupported platform APIs | Migrate an AndroidX app containing unsupported back navigation APIs to AndroidX APIs |

### Supported directions
| Platform | Back | Up | Forward | Home |
| --- | --- | --- | --- | --- |
| Android phone | ✅ | ✅ | 🚫 | ✅ |
| Android tablet | ✅ | ✅ | 🚫 | ✅ |
| Web (Browser) | ✅ | ✅ | ✅ | 🚫 |
| iOS (iPhone/iPad) | ✅ | 🚫 | ✅ | ✅ |

### Supported triggers
| Trigger | Android Phone | Web (Browser) | iOS (iPhone/iPad) |
| --- | --- | --- | --- |
| Keyboard back button | ✅ Back | ❓ | ✅ Back |
| Software back button | 🚫 | ✅ Back | ✅ Back |
| Software up button | ✅ Up | 🚫 | 🚫 |
| Gesture from left | ✅ Back | ❓ | ✅ Back |
| Gesture from right | ✅ Back | ❓ | ✅ Forward |
| Gesture from bottom | ✅ Home | 🚫 | ✅ Home |

### Artifacts
| Name | What it does | Artifact |
| --- | --- | --- |
| Navigation 3 runtime library | Core Navigation 3 API. Includes NavEntry , EntryProvider and the associated DSL. | androidx.navigation3:navigation3-runtime |
| Navigation 3 UI library | Provides classes to display content, including NavDisplay and Scene . | androidx.navigation3:navigation3-ui |
| ViewModel Lifecycle for Navigation 3 | Allows ViewModels to be scoped to entries in the back stack. | androidx.lifecycle:lifecycle-viewmodel-navigation3 |
| Material 3 adaptive layouts for Navigation 3 | Provides adaptive layouts (SceneStrategies, Scenes and metadata definitions) for use with NavDisplay. | androidx.compose.material3.adaptive:adaptive-navigation3 |
| KotlinX Serialization | Allows navigation keys to be serialized. | Plugin: org.jetbrains.kotlin.plugin.serialization Library: org.jetbrains.kotlinx:kotlinx-serialization-core |

### Separate features into api and implementation submodules
| Module name | Contains |
| --- | --- |
| api | navigation keys |
| impl | Content for that feature, including definitions for
 NavEntry s and the entryProvider . See also
 resolve keys to content . |

### Step 4: Replace NavController
| NavController field or method | Navigator equivalent |
| --- | --- |
| navigate() | navigate() |
| popBackStack() | goBack() |

## Guidelines
- Android Jetpack's Navigation component includes the Navigation
library , Safe Args Gradle plug-in ,
and tooling to help you implement app navigation. The Navigation component
handles diverse navigation use cases, from straightforward button clicks to more
complex patterns, such as app bars and the navigation drawer.
- The following table provides an overview of the key concepts in
navigation and the main types that you use to implement them.
- Important: Whether you are using Compose, views, or a custom UI framework, these
concepts always apply when implementing navigation. However, the specific ways
in which you use them can differ.
- Note: If you are using XML for your navigation graphs, use Android Studio's
 Navigation Editor to view and edit your graphs.
- Navigate to a destination : Demonstrates how to use a NavController to
move between the destinations in your graph.
- The Navigation component provides a straightforward and generic way of
navigating to a destination. This interface supports a range of contexts and UI
frameworks. For example, you can use the Navigation component with Compose,
views, fragments, activities, and even custom UI frameworks.
- This guide describes how you can use the Navigation component to navigate to a
destination in various contexts.
- The key type you use to move between destinations is the NavController .
See Create a navigation controller for more information on the class itself
and how to create an instance of it. This guide details how to use it.
- Regardless of which UI framework you use, there is a single function you can use
to navigate to a destination: NavController.navigate() .
- There are many overloads available for navigate() . The overload you should
choose corresponds to your exact context. For example, you should use one
overload when navigating to a composable and another when navigating to a view.
- The following sections outline some of the key navigate() overloads you can
use.
- To navigate to a composable, you should use NavController.navigate<T> .
With this overload, navigate() takes a single route argument for which you
pass a type. It serves as the key to a destination.
- When a composable function needs to navigate to a new screen, you shouldn't pass
it a reference to the NavController so that it can call navigate() directly.
According to Unidirectional Data Flow (UDF) principles, the composable
should instead expose an event that the NavController handles.
- Note: For buttons, there are three variants of
 Navigation.createNavigateOnClickListener() . These variants are useful if
you're using the Java programming language. If you're using Kotlin,
 OnClickListener is a SAM interface, so you can use a trailing lambda. This
approach can be shorter and easier to read than calling
 createNavigateOnClickListener() directly.
- To navigate to an implicit deep link destination , use the
 navigate(NavDeepLinkRequest) overload. The follow snippet provides an
implementation of this method:
- Note: For convenience, you can also use navigate(Uri) , which wraps a
 Uri in a DeepLinkRequest .
- In addition to Uri , NavDeepLinkRequest also supports deep links with
actions and MIME types. To add an action to the request, use
 fromAction() or setAction() . To add a MIME type to a request,
use fromMimeType() or setMimeType() .
- For a NavDeepLinkRequest to properly match an implicit deep link destination,
the URI, action, and MIME type must all match the NavDeepLink in the
destination. URIs must match the pattern, the actions must be an exact match,
and the MIME types must be related. For example, image/jpg matches with
 image/\*
- This document covers how to use NavController.navigate() in the most
common use cases. However, the function has a range of overloads that you can
use in different contexts, and in tandem with any Ui framework. See the
reference documentation for more detail on these overloads.
- Note: Even if you aren't using the Navigation component in your project, your
app should follow these design principles.

## Concepts (for graph)
- Important:
- Key concepts
- Compose
- Fragments
- Benefits and features
- Animations and transitions:
- Deep linking:
- UI patterns:
- Type safety:
- ViewModel support:
- Fragment transactions:
- Back and up:
