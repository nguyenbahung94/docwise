<!-- Source: https://kotlinlang.org/docs/coroutines-guide.html -->
<!-- Source: https://kotlinlang.org/docs/coroutines-basics.html -->
<!-- Source: https://kotlinlang.org/docs/cancellation-and-timeouts.html -->
<!-- Source: https://kotlinlang.org/docs/composing-suspending-functions.html -->
<!-- Source: https://kotlinlang.org/docs/coroutine-context-and-dispatchers.html -->
<!-- Source: https://kotlinlang.org/docs/flow.html -->
<!-- Source: https://kotlinlang.org/docs/channels.html -->
<!-- Source: https://kotlinlang.org/docs/coroutines-and-channels.html -->
<!-- Source: https://kotlinlang.org/docs/exception-handling.html -->
<!-- Source: https://kotlinlang.org/docs/shared-mutable-state-and-concurrency.html -->
<!-- Type: official -->
<!-- Priority: high -->
<!-- Topic: kotlin-coroutines -->
<!-- Extracted: 2026-03-24 -->
<!-- Verified: — -->

# Coroutines guide

## Rules
- DO: Use withContext(Dispatchers.Default) to define an entry point for multithreaded concurrent code that runs on a shared thread pool: 
suspend fun main() {
 withContext(Dispatchers.Default) {
 // Add the coroutine builders here
 }
}
 The suspending withContext() function is typically used for context s
- DO: Use a coroutine builder function like CoroutineScope.launch() to start the coroutine: 
suspend fun main() {
 withContext(Dispatchers.Default) { // this: CoroutineScope
 // Starts a coroutine inside the scope with CoroutineScope.launch()
 this.launch { greet() }
 println("The withContext() on the thr
- DO: Use CoroutineScope.launch() to run a task alongside other work when the result isn't needed or you don't want to wait for it:
- DO: Use runBlocking() only when there is no other option to call suspending code from non-suspending code:
- DO: Use the isActive property in long-running computations to periodically check for cancellation. This property is false when the coroutine is no longer active, which you can use to gracefully stop the coroutine when it no longer needs to continue the operation:
- DO: Use the ensureActive() function to check for cancellation and stop the current computation by throwing CancellationException if the coroutine is canceled:
- DO: Use yield to allow other coroutines to run on the same thread or thread pool before one of them finishes:
- DON'T: Do not select any scopes. Click Generate token at the bottom of the page.
- DO: Click Load contributors . The UI should freeze for some time and then show the list of contributors.
- DON'T: To avoid repeating .body() ?: emptyList() , an extension function bodyList() is declared: 
fun <T> Response<List<T>>.bodyList(): List<T> {
 return body() ?: emptyList()
}
- DO: Run the program again and take a look at the system output in IntelliJ IDEA. It should have something like this: 
1770 [AWT-EventQueue-0] INFO Contributors - kotlin: loaded 40 repos
2025 [AWT-EventQueue-0] INFO Contributors - kotlin-examples: loaded 23 contributors
2229 [AWT-EventQueue-0] INFO Contr
  WHY: the program started, then the thread name in square brackets
- DO: updateResults() updates the UI, so it must always be called from the UI thread.
- DO: loadContributorsSuspend() should be defined as a suspend function.
- DON'T: To change this code to run "contributors" coroutines on different threads from the common thread pool, specify Dispatchers.Default as the context argument for the async function: 
async(Dispatchers.Default) { }
 CoroutineDispatcher determines what thread or threads the corresponding coroutine should
- DO: To specify the dispatcher on the caller side, apply the following change to the project while letting loadContributorsConcurrent start coroutines in the inherited context: 
launch(Dispatchers.Default) {
 val users = loadContributorsConcurrent(service, req)
 withContext(Dispatchers.Main) {
 updateRes
- DO: The coroutine context stores additional technical information used to run a given coroutine, like the coroutine custom name, or the dispatcher specifying the threads the coroutine should be scheduled on.
- DO: launch and async are declared as extensions to CoroutineScope , so an implicit or explicit receiver must always be passed when you call them.
- DO: Use a simple version without concurrency; you'll add it later in the next section.
- DO: The intermediate list of contributors should be shown in an "aggregated" state, not just the list of users loaded for each repository.
- DO: The total number of contributions for each user should be increased when the data for each new repository is loaded.
- DO: Use the previous functions, loadContributorsConcurrent() from Request5Concurrent.kt and loadContributorsProgress() from Request6Progress.kt .
- DO: You can't rely on the exact time the solution runs because it still takes additional time to prepare and run the code. You could add a constant, but then the time would differ from machine to machine. The mock service delays should be higher than this constant so you can see a difference. If the con
  WHY: it still takes additional time to prepare and run the code
- DON'T: Don't forget to add @UseExperimental(ExperimentalCoroutinesApi::class) .

## Pitfalls
- You don't have to specify a dispatcher for every coroutine. By default, coroutines inherit the dispatcher from their parent scope. You can specify a dispatcher to run a coroutine in a different context. If the coroutine context doesn't include a dispatcher, coroutine builders use Dispatchers.Default
- All suspending functions in the kotlinx.coroutines library cooperate with cancellation because they use suspendCancellableCoroutine() internally, which checks for cancellation when the coroutine suspends. In contrast, custom suspending functions that use suspendCoroutine() don't react to cancellatio
  WHY: they use suspendCancellableCoroutine() internally, which checks for cancellation when the coroutine suspends
- Avoid using NonCancellable with other coroutine builders like .launch() or .async() . Doing so disrupts structured concurrency by breaking the parent-child relationship.
- All functions that create coroutines are defined as extensions on CoroutineScope , so that we can rely on structured concurrency to make sure that we don't have lingering global coroutines in our application.
  WHY: we can rely on structured concurrency to make sure that we don't have lingering global coroutines in our application
- Coroutines running in supervision scope do not propagate exceptions to their parent and are excluded from this rule. A further Supervision section of this document gives more details.

## Guidelines
- In order to use coroutines as well as follow the examples in this guide, you need to add a dependency on the kotlinx-coroutines-core module as explained in the project README .
- To declare a suspending function, use the suspend keyword:
- This example doesn't use concurrency yet, but by marking the functions with the suspend keyword, you allow them to call other suspending functions and run concurrent code inside.
- The examples on this page use the explicit this expression with the coroutine builder functions CoroutineScope.launch() and CoroutineScope.async() . These coroutine builders are extension functions on CoroutineScope , and the this expression refers to the current CoroutineScope as the receiver. For a practical example, see Extract coroutine builders from the coroutine scope .
- While you can mark the main() function as suspend in some projects, it may not be possible when integrating with existing code or using a framework. In that case, check the framework's documentation to see if it supports calling suspending functions. If not, use runBlocking() to call them by blocking the current thread.
- Consider the following example:
- You can also write this.launch without the explicit this expression, as launch . These examples use explicit this expressions to highlight that it's an extension function on CoroutineScope . For more information on how lambdas with receivers work in Kotlin, see Function literals with receiver .
- To extract the coroutine builders into another function, that function must declare a CoroutineScope receiver, otherwise a compilation error occurs:
- The CoroutineScope.launch() function returns a Job handle. Use this handle to wait for the launched coroutine to complete. For more information, see Cancellation and timeouts .
- The CoroutineScope.async() coroutine builder function is an extension function on CoroutineScope . It starts a concurrent computation inside an existing coroutine scope and returns a Deferred handle that represents an eventual result. Use the .await() function to suspend the code until the result is ready:
- A coroutine dispatcher controls which thread or thread pool coroutines use for their execution. Coroutines aren't always tied to a single thread. They can pause on one thread and resume on another, depending on the dispatcher. This lets you run many coroutines at the same time without allocating a separate thread for every coroutine.
- If the coroutine context doesn't include a dispatcher, coroutine builders use Dispatchers.Default .
- The kotlinx.coroutines library includes different dispatchers for different use cases. For example, Dispatchers.Default runs coroutines on a shared pool of threads, performing work in the background, separate from the main thread. This makes it an ideal choice for CPU-intensive operations like data processing.
- Alternatively, you can use a withContext() block to run all code in it on a specified dispatcher:
- Depending on your operating system, JDK version, and settings, the JVM thread version may throw an out-of-memory error or slow down thread creation to avoid running too many threads at once.
- Cancellation lets you stop a coroutine before it completes. It stops work that's no longer needed, such as when a user closes a window or navigates away in a user interface while a coroutine is still running. You can also use it to release resources early and to stop a coroutine from accessing objects past their disposal.
- You can use cancellation to stop long-running coroutines that keep producing values even after other coroutines no longer need them, for example, in pipelines .
- You can use the awaitCancellation() function to suspend a coroutine until it's canceled.
- Catching CancellationException can break the cancellation propagation. If you must catch it, rethrow it to let the cancellation propagate correctly through the coroutine hierarchy. For more information, see Coroutine exceptions handling .
- A call to a suspend function is a suspension point, but it doesn't always suspend. For example, when awaiting a Deferred result, the coroutine only suspends if that Deferred isn't completed yet.

## Core Concepts

1. **Coroutine Scopes and Structured Concurrency**
   - Explanation: Coroutine scopes manage the lifecycle of coroutines launched from them, ensuring that each coroutine is properly contained within its parent scope. This helps avoid lingering global coroutines and ensures better control over the concurrency model.
   
2. **Coroutine Dispatchers and Thread Management**
   - Explanation: Dispatchers determine how coroutines are executed on different threads or thread pools. Common dispatchers like `Dispatchers.Default` handle background computations, while `Dispatchers.Main` is used for UI updates to maintain responsiveness in applications.

3. **Cancellation Mechanisms in Coroutines**
   - Explanation: Proper cancellation mechanisms allow stopping unneeded coroutines efficiently, freeing up resources and preventing unnecessary computation or data access after a coroutine's work is no longer required.

4. **Suspending Functions and Their Cooperation with Cancellation**
   - Explanation: Suspend functions provided by kotlinx.coroutines support internal cancellation checks, ensuring that they can halt operation when requested, unlike custom suspending functions which might not behave similarly without explicit handling.
   
5. **Coroutine Builders (launch vs async)**
   - Explanation: `CoroutineScope.launch()` is used to run tasks concurrently and does not return a result, making it suitable for side effects or operations where the outcome isn't necessary. Conversely, `async` starts concurrent computations that produce a deferred result, which can be awaited using `.await()`.

## Mental Model
- **The Problem**: Efficiently managing multiple asynchronous tasks in an application without causing issues like uncontrolled coroutine lifecycle or incorrect UI updates.
- **Core Insight**: Understanding how `CoroutineScope` and dispatchers manage concurrency ensures clean code that avoids common pitfalls of multithreading, such as leaking coroutines or failing to properly update the user interface.

## Hallucination Report
- The section "Observable State Triggers Recomposition" has been removed since it introduces concepts not covered in the provided documentation on Kotlin coroutines.

## Concepts (for graph)
- Kotlin Help
- Coroutines guide
- Table of contents
- Additional references
- Coroutines basics
- Suspending functions
- Add the kotlinx.coroutines library to your project
- Create your first coroutines
- Coroutine scope and structured concurrency
- Create a coroutine scope with the coroutineScope() function
- Extract coroutine builders from the coroutine scope
- Coroutine builder functions

<!-- Quality Report
## Quality Report

| Section | Score | Issue (if < 4) |
| --- | --- | --- |
| Core Concepts | 5 | - |
| Mental Model | 4 | Missing a brief explanation or example of observable state triggers in UI context |
| Decision Framework | N/A | Not present in the provided content |
| Common Mistakes | 3 | Needs specific examples or details on common mistakes related to coroutines and structured concurrency |
| Key Relationships | 5 | - |

## Verdict: NEEDS_FIX

## Fixes (only if NEEDS_FIX)
Mental Model: Include a brief explanation of how observable state triggers recomposition in the UI context.
Common Mistakes: Add specific examples or details on common mistakes related to coroutines and structured concurrency.
-->
