<!-- Source: https://kotlinlang.org/docs/ksp-overview.html -->
<!-- Type: official -->
<!-- Priority: high -->
<!-- Topic: kotlin-ksp -->
<!-- Extracted: 2026-03-24 -->
<!-- Verified: — -->

# Kotlin Symbol Processing API

## Decision Tables
### Supported libraries
| Library | Status |
| --- | --- |
| Room | Officially supported |
| Moshi | Officially supported |
| RxHttp | Officially supported |
| Kotshi | Officially supported |
| Lyricist | Officially supported |
| Lich SavedState | Officially supported |
| gRPC Dekorator | Officially supported |
| EasyAdapter | Officially supported |
| Koin Annotations | Officially supported |
| Glide | Officially supported |
| Micronaut | Officially supported |
| Epoxy | Officially supported |
| Paris | Officially supported |
| Auto Dagger | Officially supported |
| SealedX | Officially supported |
| Ktorfit | Officially supported |
| Mockative | Officially supported |
| DeeplinkDispatch | Supported via airbnb/DeepLinkDispatch#323 |
| Dagger | Alpha |
| Motif | Alpha |
| Hilt | In progress |
| Auto Factory | Not yet supported |

## Guidelines
- KSP aims to simplify the creation of lightweight compiler plugins. Its well-defined API hides compiler changes, so you don't need to spend much effort maintaining your processors. However, this approach comes with trade-offs. For example, KSP-based processors can't examine expressions or statements, and they can't modify the source code.
- Typical use cases for KSP-based plugins include:

## Core Concepts

1. **Kotlin Symbol Processing API (KSP)**
   - Evidence: Entire document focuses on KSP, listed under "Guidelines".
   - Explanation: The Kotlin Symbol Processing API provides a stable interface for developing compiler plugins that process Kotlin source code without needing to handle internal compiler changes manually.

2. **Supported Libraries and Their Status**
   - Evidence: Detailed in the "Decision Tables" section.
   - Explanation: KSP supports various libraries with different levels of support, ranging from officially supported (with full integration) to alpha or not yet supported, ensuring developers can use stable APIs without worrying about underlying compiler details.

3. **Typical Use Cases for KSP-Based Plugins**
   - Evidence: Mentioned in the guidelines section.
   - Explanation: Common applications include creating plugins that generate code based on annotations, validate types and perform other compile-time analyses, all while leveraging KSP's stable APIs to avoid maintenance overhead due to compiler changes.

## Mental Model
- **The Problem**: Developers struggle to maintain compiler plugins due to frequent changes in Kotlin language features and underlying compiler structures.
- **Core Insight**: KSP solves this issue by providing a stable API that allows developers to focus on plugin logic without dealing with internal compiler intricacies, making development and maintenance easier and more reliable.

## How It Works Internally
Kotlin Symbol Processing API = Lightweight Compiler Plugin Interface + Stable Symbol Definitions
- **Mechanism**: Developers create plugins using KSP's well-defined APIs, which handle the complexities of interacting with the Kotlin compiler.
- **Benefits**: This approach ensures that plugins remain stable and maintainable over time as Kotlin evolves.

## Common Mistakes
**Not Using Supported Libraries with KSP**
- **Looks like**: Attempting to integrate unsupported libraries directly without considering KSP's support status, leading to manual handling of compiler changes.
  ```kotlin
  // Incorrect approach: Using an unsupported library without KSP integration
  val annotation = element.annotationMirrors.first()
  ```
- **Why it breaks**: Without official support from KSP, developers must manually manage compiler changes and intricacies, which can lead to unstable plugins over time due to incompatibilities.
- **Correct Approach**: Utilize officially supported libraries listed with KSP for seamless integration by leveraging their stability and ease of use.

## Concepts (for graph)
- Kotlin Help
- Kotlin Symbol Processing API
- How KSP looks at source files
- SymbolProcessorProvider: the entry point
- Resources
- Supported libraries
- Typical → cases (uses)

<!-- Quality Report
## Quality Report

| Section | Score | Issue (if < 4) |
| --- | --- | --- |
| Core Concepts | 5 | None |
| Mental Model | 5 | None |
| Decision Framework | 3 | Missing detailed explanation of how KSP supports different libraries and their statuses. |
| Common Mistakes | 5 | None |
| Key Relationships | 4 | Could be more specific about the relationships between KSP and supported libraries, including any limitations or dependencies. |

## Verdict: NEEDS_FIX

## Fixes (only if NEEDS_FIX)
Decision Framework: Add a detailed explanation of how KSP supports different libraries based on their status in the Decision Tables section.
-->
