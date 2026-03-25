<!-- Source: https://kotlinlang.org/docs/flow.html -->
<!-- Type: official -->
<!-- Priority: high -->
<!-- Topic: kotlin-flow -->
<!-- Extracted: 2026-03-24 -->
<!-- Verified: — -->

# Asynchronous Flow

## Guidelines
- Using the List<Int> result type, means we can only return all the values at once. To represent the stream of values that are being computed asynchronously, we can use a Flow<Int> type just like we would use a Sequence<Int> type for synchronously computed values:
- Size-limiting intermediate operators like take cancel the execution of the flow when the corresponding limit is reached. Cancellation in coroutines is always performed by throwing an exception, so that all the resource-management functions (like try { ... } finally { ... } blocks) operate normally in case of cancellation:
- Operators to get the first value and to ensure that a flow emits a single value.
- Collection of a flow always happens in the context of the calling coroutine. For example, if there is a simple flow, then the following code runs in the context specified by the author of this code, regardless of the implementation details of the simple flow:
- So, by default, code in the flow { ... } builder runs in the context that is provided by a collector of the corresponding flow. For example, consider the implementation of a simple function that prints the thread it is called on and emits three numbers:
- We can use a buffer operator on a flow to run emitting code of the simple flow concurrently with collecting code, as opposed to running them sequentially:
- We use a onEach intermediate operator in this example to delay each element and make the code that emits sample flows more declarative and shorter.
- Note that flatMapLatest cancels all the code in its block ( { requestFlow(it) } in this example) when a new value is received. It makes no difference in this particular example, because the call to requestFlow itself is fast, not-suspending, and cannot be cancelled. However, a differnce in output would be visible if we were to use suspending functions like delay in requestFlow .
- A collector can use Kotlin's try/catch block to handle exceptions:
- Flows must be transparent to exceptions and it is a violation of the exception transparency to emit values in the flow { ... } builder from inside of a try/catch block. This guarantees that a collector throwing an exception can always catch it using try/catch as in the previous example.
- The emitter can use a catch operator that preserves this exception transparency and allows encapsulation of its exception handling. The body of the catch operator can analyze an exception and react to it in different ways depending on which exception was caught:
- The output of the example is the same, even though we do not have try/catch around the code anymore.
- We can combine the declarative nature of the catch operator with a desire to handle all the exceptions, by moving the body of the collect operator into onEach and putting it before the catch operator. Collection of this flow must be triggered by a call to collect() without parameters:
- In addition to try / catch , a collector can also use a finally block to execute an action upon collect completion.
- Now we know how to collect flow, and handle its completion and exceptions in both imperative and declarative ways. The natural question here is, which approach is preferred and why? As a library, we do not advocate for any particular approach and believe that both options are valid and should be selected according to your own preferences and code style.
- If we use the collect terminal operator after onEach , then the code after it will wait until the flow is collected:
- The required parameter to launchIn must specify a CoroutineScope in which the coroutine to collect the flow is launched. In the above example this scope comes from the runBlocking coroutine builder, so while the flow is running, this runBlocking scope waits for completion of its child coroutine and keeps the main function from returning and terminating this example.
- However, most other flow operators do not do additional cancellation checks on their own for performance reasons. For example, if you use IntRange.asFlow extension to write the same busy loop and don't suspend anywhere, then there are no checks for cancellation:
- In the case where you have a busy loop with coroutines you must explicitly check for cancellation. You can add .onEach { currentCoroutineContext().ensureActive() } , but there is a ready-to-use cancellable operator provided to do that:

## Core Concepts

1. **Flows and Asynchronous Data Streams**: Flows are used to represent asynchronous data streams that emit values sequentially over time rather than returning all values at once like `List<Int>`. For example, using `Flow<Int>` enables us to handle sequential asynchronous operations efficiently.
   - Evidence: "Using the List result type, means we can only return all the values at once. To represent the stream of values that are being computed asynchronously..."

2. **Cancellation and Resource Management**: When a flow is cancelled by an intermediate operator like `take`, it throws exceptions to allow proper resource cleanup through try-finally blocks.
   - Evidence: "Size-limiting intermediate operators like take cancel the execution of the flow when the corresponding limit is reached."

3. **Declarative Exception Handling with `catch` Operator**: This operator ensures exception transparency and encapsulates error handling within flows without breaking the declarative style by moving exception handling out of the main flow logic.
   - Evidence: "Flows must be transparent to exceptions... The emitter can use a catch operator that preserves this exception transparency..."

4. **Imperative vs Declarative Approaches**: Both imperative and declarative approaches are valid for collecting flows and handling their completion and exceptions, with choices based on preferences and code style.
   - Evidence: "Now we know how to collect flow, and handle its completion and exceptions in both imperative and declarative ways. The natural question here is, which approach is preferred and why? As a library, we do not advocate for any particular approach and believe that both options are valid..."

## Mental Model

- **The Problem**: Without proper mechanisms like cancellation through exceptions and robust exception handling, asynchronous operations in Kotlin can lead to resource leaks or unexpected application crashes.
- **Core Insight**: Utilizing flows and their operators effectively manages asynchronous data streams while ensuring clean resource management and transparent error handling.
- **How concepts connect**:
  - Asynchronous Data Streams → Cancellation → Exception Transparency
  - Using `Flow<Int>` allows for sequential, non-blocking data emission. When using size-limiting operators like `take`, cancellation occurs through exceptions that are caught by try-finally blocks, ensuring proper resource cleanup.

## Decision Framework

| I need to... | Use | NOT | Because |
| --- | --- | --- | --- |
| Handle asynchronous data streams in Kotlin | `Flow<Int>` | `List<Int>` | To represent sequential emission of values over time rather than immediate return |

## How It Works Internally

- **Cancellation**: Cancellation in coroutines is performed by throwing exceptions, which allows the execution to be properly cleaned up through resource management blocks (try-finally).

## Common Mistakes

**Name:** Incorrect Use of `catch` Operator

- **Looks like**:
```kotlin
flow {
    emit(1)
}.catch { e ->
    println("Caught exception: $e")
}
```

- **Why it breaks**: The code inside the try-catch block does not follow the cancellation protocol correctly, leading to potential resource leaks or unexpected behavior.

- **Correct**:
```kotlin
flow {
    emit(1)
}.catch { e ->
    println("Caught exception: $e")
}

// Correct usage of catch operator outside try/catch block inside flow builder.
```

## Key Relationships

- `Flow` requires proper cancellation and resource management to avoid leaks or unexpected behavior.

## Concepts (for graph)
- Kotlin Help
- Asynchronous Flow
- Representing multiple values
- Sequences
- Suspending functions
- Flows
- Flows are cold
- Flow cancellation basics
- Flow builders
- Intermediate flow operators
- Transform operator
- Size-limiting operators

<!-- Quality Report
## Quality Report

| Section | Score | Issue (if < 4) |
| --- | --- | --- |
| Core Concepts | 5 | None |
| Mental Model | 4 | Missing a connection between cancellation and the catch operator. |
| Decision Framework | 4 | The table should clarify that `List<Int>` is used for synchronous operations whereas `Flow<Int>` is for asynchronous ones. |
| Common Mistakes | 4 | Example lacks context on why it's incorrect, misses explanation of proper use inside try-catch block outside flow builder. |
| Key Relationships | 5 | None |

## Verdict: NEEDS_FIX

## Fixes (only if NEEDS_FIX)
Mental Model: Add insight about how the catch operator integrates with cancellation protocol.
Decision Framework: Clarify distinction between synchronous and asynchronous data handling.
Common Mistakes: Explain proper use of `catch` outside try-catch block inside flow builder.
-->
