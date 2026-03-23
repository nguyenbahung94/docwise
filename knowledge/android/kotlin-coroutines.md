<!-- Source: https://kotlinlang.org/docs/coroutines-guide.html -->
<!-- Type: official -->
<!-- Priority: high -->
<!-- Topic: concurrency -->
<!-- Extracted: 2026-03-23 -->
<!-- Verified: — -->

# Kotlin Coroutines — Official Guide

## Rules

- DO: Always rethrow `CancellationException` after catching it.
  WHY: Swallowing it breaks cancellation propagation through the coroutine hierarchy, preventing cleanup of parent and sibling coroutines.

- DO: Use `ensureActive()` or `isActive` checks in tight computation loops.
  WHY: Coroutine cancellation is cooperative — CPU-bound code without suspension points never checks for cancellation.

- DO: Use `flowOn()` to change a Flow's upstream dispatcher.
  WHY: Using `withContext` inside `flow {}` violates the flow context preservation invariant and throws an exception.

- DO: Use `Mutex.withLock` instead of `synchronized` in coroutines.
  WHY: `synchronized` blocks the thread; `Mutex` suspends, allowing other coroutines to run on the same thread.

- DO: Use coarse-grained thread confinement over fine-grained.
  WHY: Fine-grained `withContext(singleThread)` on every access causes excessive context switching and severe performance degradation.

- DO: Use `withContext(NonCancellable)` only in `finally` blocks for essential cleanup.
  WHY: Using it with `launch`/`async` breaks parent-child relationships and structured concurrency.

- DO: Use `cancelAndJoin()` instead of separate `cancel()` + `join()`.
  WHY: Combines both into a single call, preventing race conditions between cancel and subsequent code.

- DON'T: Use `runBlocking` inside suspending functions.
  WHY: Defeats the purpose of coroutines by blocking the thread; causes deadlocks if called on a limited dispatcher.
  EXCEPTION: Bridging non-suspend interfaces to suspend code (e.g., legacy callback APIs).

- DON'T: Use `GlobalScope.async` for structured concurrent work.
  WHY: No structured concurrency — coroutines continue running even if calling code fails, causing memory and resource leaks.

- DON'T: Use `@Volatile` for compound operations like `counter++`.
  WHY: Volatile guarantees atomic reads/writes but NOT atomicity of read-modify-write sequences. Use `AtomicInteger` or `Mutex`.

- DON'T: Catch downstream exceptions with `catch` operator on Flow.
  WHY: `catch` only handles upstream exceptions. Move logic to `onEach` before `catch` to handle all exceptions.

- DON'T: Use `Dispatchers.Unconfined` in general application code.
  WHY: After first suspension, it resumes on whatever thread the suspending function used — unpredictable and unsafe for shared state.
  EXCEPTION: Coroutines that don't consume CPU time or update shared data.

## Before/After

Old way — withContext in flow builder:
```kotlin
fun simple(): Flow<Int> = flow {
    withContext(Dispatchers.Default) { // WRONG — throws exception
        emit(i)
    }
}
```

New way — flowOn operator:
```kotlin
fun simple(): Flow<Int> = flow {
    emit(i)
}.flowOn(Dispatchers.Default) // Correct — changes upstream context
```

Old way — fine-grained confinement:
```kotlin
repeat(100_000) {
    withContext(counterContext) { counter++ } // Slow: context switch per operation
}
```

New way — coarse-grained confinement:
```kotlin
withContext(counterContext) {
    repeat(100_000) { counter++ } // Fast: single context switch
}
```

## Decision Tables

| Need | Use | Not |
|---|---|---|
| Fire-and-forget task | `launch` | `async` |
| Need return value | `async` + `await` | `launch` |
| Sequential dependent calls | Sequential suspend calls | `async` |
| Parallel independent calls | `async` + `await` | Sequential calls |
| Child failure isolation | `SupervisorJob` / `supervisorScope` | Regular `Job` |
| Change Flow dispatcher | `flowOn()` | `withContext` in flow |
| Slow collector, only want latest | `conflate()` or `collectLatest` | `buffer()` |
| Pipeline emitter+collector | `buffer()` | Default sequential |
| Search-as-you-type | `flatMapLatest` | `flatMapConcat` |
| Simple atomic counter | `AtomicInteger` | `Mutex` or `@Volatile` |
| Complex shared state | `Mutex.withLock` | `synchronized` |
| UI-bound state updates | Coarse thread confinement | Fine-grained confinement |
| Root-level error logging | `CoroutineExceptionHandler` | try-catch |
| Per-call error handling | try-catch around `await()` | `CoroutineExceptionHandler` |

## Pitfalls

- Calling `await()` on lazy async without `start()` runs sequentially.
  WHY: `await()` starts AND waits; without prior `start()` on all deferreds, they execute one at a time.

- `CoroutineExceptionHandler` on child coroutines is ignored.
  WHY: Children delegate exceptions to parent. Handler only works on root coroutines or inside `supervisorScope`.

- `CancellationException` from `withTimeout` can be caught by outer try-catch.
  WHY: `TimeoutCancellationException` is a subclass of `CancellationException`. Use `withTimeoutOrNull` for graceful handling.

- Flow built with `asFlow()` doesn't check cancellation automatically.
  WHY: Performance optimization. Add `.cancellable()` operator for busy loops.

- `launch` propagates exceptions immediately; `async` defers until `await()`.
  WHY: Different design: launch is fire-and-forget, async holds result/exception in Deferred. Forgetting to await loses the error.

## Concepts (for graph)

- CoroutineScope -> Job (manages lifecycle via)
- launch -> Job (returns)
- async -> Deferred (returns)
- Flow -> flowOn (changes upstream dispatcher via)
- Flow -> StateFlow (cold-to-hot conversion via stateIn)
- SupervisorJob -> Job (replaces for child-failure isolation)
- supervisorScope -> coroutineScope (replaces for child-failure isolation)
- Mutex -> synchronized (replaces in coroutine context)
- CancellationException -> structured concurrency (enables cooperative cancellation for)
- withContext -> Dispatchers (switches thread pool via)
- flatMapLatest -> Flow (cancels previous inner flow in)
