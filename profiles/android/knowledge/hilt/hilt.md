<!-- Source: https://developer.android.com/training/dependency-injection/hilt-android -->
<!-- Type: official -->
<!-- Priority: high -->
<!-- Topic: hilt -->
<!-- Extracted: 2026-03-24 -->
<!-- Verified: — -->

# Dependency injection with Hilt

## Code Patterns
### Adding dependencies
```
plugins {
  ...
  id("com.google.dagger.hilt.android") version "2.57.1" apply false
}
```

### Adding dependencies
```kotlin
plugins {
  id("com.google.devtools.ksp")
  id("com.google.dagger.hilt.android")
}

android {
  ...
}

dependencies {
  implementation("com.google.dagger:hilt-android:2.57.1")
  ksp("com.google.dagger:hilt-android-compiler:2.57.1")
}
```

### Adding dependencies
```
android {
  ...
  compileOptions {
    sourceCompatibility = JavaVersion.VERSION_1_8
    targetCompatibility = JavaVersion.VERSION_1_8
  }
}
```

### Hilt application class
```
@HiltAndroidApp
class ExampleApplication : Application() { ... }
```

### Inject dependencies into Android classes
```
@AndroidEntryPoint
class ExampleActivity : AppCompatActivity() { ... }
```

### Inject dependencies into Android classes
```kotlin
@AndroidEntryPoint
public class ExampleActivity extends AppCompatActivity {

  @Inject
  AnalyticsAdapter analytics;
  ...
}
```

### Define Hilt bindings
```kotlin
class AnalyticsAdapter @Inject constructor(
  private val service: AnalyticsService
) { ... }
```

### Define Hilt bindings
```kotlin
public class AnalyticsAdapter {

  private final AnalyticsService service;

  @Inject
  AnalyticsAdapter(AnalyticsService service) {
    this.service = service;
  }
  ...
}
```

### Inject interface instances with @Binds
```kotlin
interface AnalyticsService {
  fun analyticsMethods()
}

// Constructor-injected, because Hilt needs to know how to
// provide instances of AnalyticsServiceImpl, too.
class AnalyticsServiceImpl @Inject constructor(
  ...
) : AnalyticsService { ... }

@Module
@InstallIn(ActivityComponent::class)
abstract class AnalyticsModule {

  @Binds
  abstract fun bindAnalyticsService(
    analyticsServiceImpl: AnalyticsServiceImpl
  ): AnalyticsService
}
```

### Inject interface instances with @Binds
```kotlin
public interface AnalyticsService {
  void analyticsMethods();
}

// Constructor-injected, because Hilt needs to know how to
// provide instances of AnalyticsServiceImpl, too.
public class AnalyticsServiceImpl implements AnalyticsService {
  ...
  @Inject
  AnalyticsServiceImpl(...) {
    ...
  }
}

@Module
@InstallIn(ActivityComponent.class)
public abstract class AnalyticsModule {

  @Binds
  public abstract AnalyticsService bindAnalyticsService(
    AnalyticsServiceImpl analyticsServiceImpl
  );
}
```

### Inject instances with @Provides
```kotlin
@Module
@InstallIn(ActivityComponent::class)
object AnalyticsModule {

  @Provides
  fun provideAnalyticsService(
    // Potential dependencies of this type
  ): AnalyticsService {
      return Retrofit.Builder()
               .baseUrl("https://example.com")
               .build()
               .create(AnalyticsService::class.java)
  }
}
```

### Inject instances with @Provides
```kotlin
@Module
@InstallIn(ActivityComponent.class)
public class AnalyticsModule {

  @Provides
  public static AnalyticsService provideAnalyticsService(
    // Potential dependencies of this type
  ) {
      return new Retrofit.Builder()
               .baseUrl("https://example.com")
               .build()
               .create(AnalyticsService.class);
  }
}
```

### Provide multiple bindings for the same type
```
@Qualifier
@Retention(AnnotationRetention.BINARY)
annotation class AuthInterceptorOkHttpClient

@Qualifier
@Retention(AnnotationRetention.BINARY)
annotation class OtherInterceptorOkHttpClient
```

### Provide multiple bindings for the same type
```kotlin
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {

  @AuthInterceptorOkHttpClient
  @Provides
  fun provideAuthInterceptorOkHttpClient(
    authInterceptor: AuthInterceptor
  ): OkHttpClient {
      return OkHttpClient.Builder()
               .addInterceptor(authInterceptor)
               .build()
  }

  @OtherInterceptorOkHttpClient
  @Provides
  fun provideOtherInterceptorOkHttpClient(
    otherInterceptor: OtherInterceptor
  ): OkHttpClient {
      return OkHttpClient.Builder()
               .addInterceptor(otherInterceptor)
               .build()
  }
}
```

### Provide multiple bindings for the same type
```kotlin
@Module
@InstallIn(ActivityComponent.class)
public class NetworkModule {

  @AuthInterceptorOkHttpClient
  @Provides
  public static OkHttpClient provideAuthInterceptorOkHttpClient(
    AuthInterceptor authInterceptor
  ) {
      return new OkHttpClient.Builder()
                   .addInterceptor(authInterceptor)
                   .build();
  }

  @OtherInterceptorOkHttpClient
  @Provides
  public static OkHttpClient provideOtherInterceptorOkHttpClient(
    OtherInterceptor otherInterceptor
  ) {
      return new OkHttpClient.Builder()
                   .addInterceptor(otherInterceptor)
                   .build();
  }
}
```

### Provide multiple bindings for the same type
```kotlin
// As a dependency of another class.
@Module
@InstallIn(ActivityComponent::class)
object AnalyticsModule {

  @Provides
  fun provideAnalyticsService(
    @AuthInterceptorOkHttpClient okHttpClient: OkHttpClient
  ): AnalyticsService {
      return Retrofit.Builder()
               .baseUrl("https://example.com")
               .client(okHttpClient)
               .build()
               .create(AnalyticsService::class.java)
  }
}

// As a dependency of a constructor-injected class.
class ExampleServiceImpl @Inject constructor(
  @AuthInterceptorOkHttpClient private val okHttpClient: OkHttpClient
) : ...

// At field injection.
@AndroidEntryPoint
class ExampleActivity: AppCompatActivity() {

  @AuthInterceptorOkHttpClient
  @Inject lateinit var okHttpClient: OkHttpClient
}
```

### Predefined qualifiers in Hilt
```kotlin
class AnalyticsAdapter @Inject constructor(
    @ActivityContext private val context: Context,
    private val service: AnalyticsService
) { ... }
```

### Predefined qualifiers in Hilt
```kotlin
public class AnalyticsAdapter {

  private final Context context;
  private final AnalyticsService service;

  @Inject
  AnalyticsAdapter(
    @ActivityContext Context context,
    AnalyticsService service
  ) {
    this.context = context;
    this.service = service;
  }
}
```

### Component scopes
```kotlin
@ActivityScoped
class AnalyticsAdapter @Inject constructor(
  private val service: AnalyticsService
) { ... }
```

### Component scopes
```kotlin
@ActivityScoped
public class AnalyticsAdapter {

  private final AnalyticsService service;

  @Inject
  AnalyticsAdapter(AnalyticsService service) {
    this.service = service;
  }
  ...
}
```

### Component scopes
```kotlin
// If AnalyticsService is an interface.
@Module
@InstallIn(SingletonComponent::class)
abstract class AnalyticsModule {

  @Singleton
  @Binds
  abstract fun bindAnalyticsService(
    analyticsServiceImpl: AnalyticsServiceImpl
  ): AnalyticsService
}

// If you don't own AnalyticsService.
@Module
@InstallIn(SingletonComponent::class)
object AnalyticsModule {

  @Singleton
  @Provides
  fun provideAnalyticsService(): AnalyticsService {
      return Retrofit.Builder()
               .baseUrl("https://example.com")
               .build()
               .create(AnalyticsService::class.java)
  }
}
```

### Component default bindings
```kotlin
class AnalyticsServiceImpl @Inject constructor(
  @ApplicationContext context: Context
) : AnalyticsService { ... }

// The Application binding is available without qualifiers.
class AnalyticsServiceImpl @Inject constructor(
  application: Application
) : AnalyticsService { ... }
```

### Component default bindings
```kotlin
public class AnalyticsServiceImpl implements AnalyticsService {

  private final Context context;

  @Inject
  AnalyticsAdapter(@ApplicationContext Context context) {
    this.context = context;
  }
}

// The Application binding is available without qualifiers.
public class AnalyticsServiceImpl implements AnalyticsService {

  private final Application application;

  @Inject
  AnalyticsAdapter(Application application) {
    this.application = application;
  }
}
```

### Component default bindings
```kotlin
class AnalyticsAdapter @Inject constructor(
  @ActivityContext context: Context
) { ... }

// The Activity binding is available without qualifiers.
class AnalyticsAdapter @Inject constructor(
  activity: FragmentActivity
) { ... }
```

### Inject dependencies in classes not supported by Hilt
```kotlin
class ExampleContentProvider : ContentProvider() {

  @EntryPoint
  @InstallIn(SingletonComponent::class)
  interface ExampleContentProviderEntryPoint {
    fun analyticsService(): AnalyticsService
  }

  ...
}
```

### Inject dependencies in classes not supported by Hilt
```kotlin
class ExampleContentProvider: ContentProvider() {
    ...

  override fun query(...): Cursor {
    val appContext = context?.applicationContext ?: throw IllegalStateException()
    val hiltEntryPoint =
      EntryPointAccessors.fromApplication(appContext, ExampleContentProviderEntryPoint::class.java)

    val analyticsService = hiltEntryPoint.analyticsService()
    ...
  }
}
```

## Decision Tables
### Generated components for Android classes
| Hilt component | Injector for |
| --- | --- |
| SingletonComponent | Application |
| ActivityRetainedComponent | N/A |
| ViewModelComponent | ViewModel |
| ActivityComponent | Activity |
| FragmentComponent | Fragment |
| ViewComponent | View |
| ViewWithFragmentComponent | View annotated with @WithFragmentBindings |
| ServiceComponent | Service |

### Component lifetimes
| Generated component | Created at | Destroyed at |
| --- | --- | --- |
| SingletonComponent | Application#onCreate() | Application destroyed |
| ActivityRetainedComponent | Activity#onCreate() | Activity#onDestroy() |
| ViewModelComponent | ViewModel created | ViewModel destroyed |
| ActivityComponent | Activity#onCreate() | Activity#onDestroy() |
| FragmentComponent | Fragment#onAttach() | Fragment#onDestroy() |
| ViewComponent | View#super() | View destroyed |
| ViewWithFragmentComponent | View#super() | View destroyed |
| ServiceComponent | Service#onCreate() | Service#onDestroy() |

### Component scopes
| Android class | Generated component | Scope |
| --- | --- | --- |
| Application | SingletonComponent | @Singleton |
| Activity | ActivityRetainedComponent | @ActivityRetainedScoped |
| ViewModel | ViewModelComponent | @ViewModelScoped |
| Activity | ActivityComponent | @ActivityScoped |
| Fragment | FragmentComponent | @FragmentScoped |
| View | ViewComponent | @ViewScoped |
| View annotated with @WithFragmentBindings | ViewWithFragmentComponent | @ViewScoped |
| Service | ServiceComponent | @ServiceScoped |

### Component default bindings
| Android component | Default bindings |
| --- | --- |
| SingletonComponent | Application |
| ActivityRetainedComponent | Application |
| ViewModelComponent | SavedStateHandle |
| ActivityComponent | Application , Activity |
| FragmentComponent | Application , Activity , Fragment |
| ViewComponent | Application , Activity , View |
| ViewWithFragmentComponent | Application , Activity , Fragment , View |
| ServiceComponent | Application , Service |

## Guidelines
- Hilt is a dependency injection library for Android that reduces the boilerplate
of doing manual dependency injection in your project. Doing manual dependency
injection requires you to construct
every class and its dependencies by hand, and to use containers to reuse and
manage dependencies.
- Hilt provides a standard way to use DI in your application by providing
containers for every Android class in your project and managing their lifecycles
automatically. Hilt is built on top of the popular DI library
 Dagger to benefit from the
compile-time correctness, runtime performance, scalability, and Android Studio
support 
that Dagger provides. For more information, see Hilt and
Dagger .
- This guide explains the basic concepts of Hilt and its generated containers. It
also includes a demonstration of how to bootstrap an existing app to use Hilt.
- Note: Projects that use both Hilt and data
binding require Android Studio 4.0 or higher.
- If you annotate an Android class with @AndroidEntryPoint , then you also must
annotate Android classes that depend on it. For example, if you annotate a
fragment, then you must also annotate any activities where you use that
fragment.
- To obtain dependencies from a component, use the @Inject annotation to perform
field injection:
- One way to provide binding information to Hilt is constructor injection . Use
the @Inject annotation on the constructor of a class to tell Hilt how to
provide instances of that class:
- Sometimes a type cannot be constructor-injected. This can happen for multiple
reasons. For example, you cannot constructor-inject an interface. You also
cannot constructor-inject a type that you do not own, such as a class from an
external library. In these cases, you can provide Hilt with binding information
by using Hilt modules .
- A Hilt module is a class that is annotated with @Module . Like a Dagger
module , it
informs Hilt how to provide instances of certain types. Unlike Dagger modules,
you must annotate Hilt modules with @InstallIn to tell Hilt which Android
class each module will be used or installed in.
- Note: Because Hilt's code generation needs access to all of the Gradle modules
that use Hilt, the Gradle module that compiles your Application class also
needs to have all of your Hilt modules and constructor-injected classes in its
transitive dependencies.
- Consider the AnalyticsService example. If AnalyticsService is an interface,
then you cannot constructor-inject it. Instead, provide Hilt with the binding
information by creating an abstract function annotated with @Binds inside a
Hilt module.
- The @Binds annotation tells Hilt which implementation to use when it needs to
provide an instance of an interface.
- Interfaces are not the only case where you cannot constructor-inject a type.
Constructor injection is also not possible if you don't own the class because it
comes from an external library (classes like
 Retrofit ,
 OkHttpClient ,
or Room databases ), or if instances must
be created with the builder
pattern .
- Consider the previous example. If you don't directly own the AnalyticsService 
class, you can tell Hilt how to provide instances of this type by creating a
function inside a Hilt module and annotating that function with @Provides .
- A qualifier is an annotation that you use to identify a specific binding for a
type when that type has multiple bindings defined.
- Consider the example. If you need to intercept calls to AnalyticsService , you
could use an OkHttpClient object with an
 interceptor . For
other services, you might need to intercept calls in a different way. In that
case, you need to tell Hilt how to provide two different implementations of
 OkHttpClient .
- First, define the qualifiers that you will use to annotate the @Binds or
 @Provides methods:
- The previous examples demonstrated the use of ActivityComponent in Hilt
modules.
- The following example demonstrates how to scope a binding to a component in a
Hilt module. A binding's scope must match the scope of the component where it is
installed, so in this example you must install AnalyticsService in
 SingletonComponent instead of ActivityComponent :
- Note: By default, if you perform field injection in a view, ViewComponent can
use bindings that are defined in the ActivityComponent . If you also need to
use bindings that are defined in FragmentComponent and the view is part of a
fragment, use the @WithFragmentBindings annotation with @AndroidEntryPoint .

## Core Concepts

### Dependency Injection (DI) with Hilt

Dependency injection is a design pattern that allows you to manage dependencies by making them explicit through constructor or field injection. In Android applications, Hilt simplifies this process by automatically handling lifecycle-aware components and their scopes.

1. **Component Scopes and Lifetimes**
   - Components like SingletonComponent, ActivityRetainedComponent, ViewModelComponent, etc., are generated for different parts of the application (such as Application, ViewModels, Activities, Fragments) to manage dependencies that should be available throughout a specific lifecycle.
   - Example:
     ```kotlin
     @Singleton
     class AnalyticsServiceImpl : AnalyticsService {
         private val service: AnalyticsService

         @Inject
         constructor(service: AnalyticsService) { this.service = service }
     }

     @Module
     @InstallIn(SingletonComponent::class)
     abstract class AnalyticsModule {

       @Binds
       abstract fun bindAnalyticsService(
         analyticsServiceImpl: AnalyticsServiceImpl
       ): AnalyticsService
     }
     ```

2. **Providing Dependency Bindings with Hilt Modules**
   - You can provide dependency bindings using modules by either binding interfaces to implementations or providing instances of complex types like Retrofit services.
   (See the "Define Hilt bindings" and "Inject interface instances with @Binds" sections for examples.)

### Mental Model

- **The Problem**: Manually managing dependencies in Android projects leads to boilerplate code, difficult maintenance, and potential errors.
- **Core Insight**: Hilt simplifies dependency management by automatically handling lifecycle-aware components and their scopes, thus reducing manual effort and minimizing mistakes.
- **How concepts connect**:
   - Dependency Injection → Component Scopes: DI relies on properly scoped components to ensure that dependencies are correctly managed according to the component's lifecycle (e.g., ActivityComponent for activities).
   - Hilt Application Class → Lifecycle Management: The application class annotated with `@HiltAndroidApp` ensures that global dependencies are properly initialized and available across different components.

### Component Scopes and Lifetimes

Components like SingletonComponent, ActivityRetainedComponent, ViewModelComponent manage their lifecycles according to specific lifecycle events:

- **SingletonComponent**: Created at `Application#onCreate()` and destroyed when the application is destroyed.
- **ActivityRetainedComponent**: Created at `Activity#onCreate()` and destroyed at `Activity#onDestroy()`.
- **ViewModelComponent**: Created when the ViewModel is created and destroyed when the ViewModel is destroyed.

### Decision Framework

| I need to... | Use | NOT | Because |
| --- | --- | --- | --- |
| Inject an interface instance with Hilt | Use @Binds or constructor injection for owned classes | Use @Provides function within a module | When you don't own the class, like from Retrofit or third-party libraries |

### How It Works Internally

- **X = Y + Z**: Components (Y) + Scopes (Z) create the binding graph that Hilt uses to manage dependency lifecycles.
  - Example:
    ```kotlin
    @Singleton
    class AnalyticsServiceImpl : AnalyticsService {
        private val service: AnalyticsService

        @Inject
        constructor(service: AnalyticsService) { this.service = service }
    }

    @Module
    @InstallIn(SingletonComponent::class)
    abstract class AnalyticsModule {

      @Binds
      abstract fun bindAnalyticsService(
        analyticsServiceImpl: AnalyticsServiceImpl
      ): AnalyticsService
    }
    ```

### Common Mistakes

**Incorrect Dependency Injection**

- **Name**: Misusing `@Inject`
  - **Looks like**:
    ```kotlin
    class ExampleActivity {
        lateinit var analyticsService: AnalyticsService // No injection here
    }
    ```
  - **Why it breaks**: The `analyticsService` field will not be automatically provided and initialized, leading to a runtime exception or undefined behavior.
  - **Correct**:
    ```kotlin
    @AndroidEntryPoint
    class ExampleActivity : AppCompatActivity() {
        @Inject lateinit var analyticsService: AnalyticsService // Correct injection here
    }
    ```

## Key Relationships

- Dependency Injection requires Component Scopes for lifecycle management.
- Hilt modules provide necessary bindings for components, ensuring that dependencies are available at the right times in their lifecycles.

## Concepts (for graph)
- Adding dependencies
- Hilt application class
- Inject dependencies into Android classes
- Define Hilt bindings
- Hilt modules
- Inject interface instances with @Binds
- Inject instances with @Provides
- Provide multiple bindings for the same type
- Predefined qualifiers in Hilt
- Generated components for Android classes
- Component lifetimes
- Component scopes

<!-- Quality Report
## Quality Report

| Section | Score | Issue (if < 4) |
| --- | --- | --- |
| Core Concepts | 5 | - |
| Mental Model | 5 | - |
| Decision Framework | 4 | Inconsistent table format and minor wording issues. |
| Common Mistakes | 4 | Minor wording improvements can be made for clarity. |
| Key Relationships | 4 | Missing some direct relationships between concepts, could be more explicit about how components and scopes interact. |

## Verdict: NEEDS_FIX

## Fixes (only if NEEDS_FIX)
Decision Framework: Standardize table format and improve minor inconsistencies.
Common Mistakes: Refine wording for clearer explanations.
Key Relationships: Explicitly describe the interaction between components and scopes in dependency management.
-->
