<!-- Source: https://developer.android.com/guide/app-compatibility -->
<!-- Source: https://developer.android.com/guide/app-compatibility/test-debug -->
<!-- Source: https://developer.android.com/guide/app-compatibility/restrictions-non-sdk-interfaces -->
<!-- Type: official -->
<!-- Priority: high -->
<!-- Topic: app-compatibility -->
<!-- Extracted: 2026-03-24 -->
<!-- Verified: — -->

# App compatibility in Android

## Rules
- DO: Use the developer options to toggle changes on or off. To find the developer
options, follow these steps:
- DON'T: Deprecated: blacklist
- DON'T: Deprecated: greylist-max-x
- DON'T: Deprecated: greylist
- DON'T: Deprecated: Both public-api and whitelist

## Code Patterns
### Identify enabled changes using logcat
```
D CompatibilityChangeReporter: Compat change id reported: 194833441; UID 10265; state: ENABLED
```

### Identify enabled changes using ADB
```
adb shell dumpsys platform_compat
```

### Identify enabled changes using ADB
```
packageOverrides={com.my.package=false}
```

### Identify enabled changes using ADB
```
packageOverrides={com.my.package=true, com.another.package=false}
```

### Toggle changes using ADB
```
adb shell am compat enable (CHANGE_ID|CHANGE_NAME) PACKAGE_NAME
adb shell am compat disable (CHANGE_ID|CHANGE_NAME) PACKAGE_NAME
```

### Toggle changes using ADB
```
adb shell am compat reset (CHANGE_ID|CHANGE_NAME) PACKAGE_NAME
```

### Generate lists from AOSP
```
m out/soong/hiddenapi/hiddenapi-flags.csv
```

### Generate lists from AOSP
```
out/soong/hiddenapi/hiddenapi-flags.csv
```

### Test using a debuggable app
```
Accessing hidden field Landroid/os/Message;->flags:I (light greylist, JNI)
```

### How can I enable access to non-SDK interfaces?
```
adb shell settings put global hidden_api_policy  1
```

### How can I enable access to non-SDK interfaces?
```
adb shell settings delete global hidden_api_policy
```

### How can I enable access to non-SDK interfaces?
```
adb shell settings put global hidden_api_policy_pre_p_apps  1
adb shell settings put global hidden_api_policy_p_apps 1
```

### How can I enable access to non-SDK interfaces?
```
adb shell settings delete global hidden_api_policy_pre_p_apps
adb shell settings delete global hidden_api_policy_p_apps
```

## Decision Tables
### Identify enabled changes using logcat
| State | Meaning |
| --- | --- |
| ENABLED | The change is enabled and will affect the app's behavior if
 the app uses the APIs that were changed. |
| DISABLED | The change is disabled and won't affect the app. 
 Note: If this change is disabled because the app's
 targetSDKVersion is below the required threshold, the
 change will be enabled by default when the app increases its
 targetSDKVersion to target a higher version. |
| LOGGED | The change is being logged through the compatibility framework but
 can't be toggled on or off. Although this change can't be toggled, it
 might still affect your app's behavior. See the description of the
 change in the compatibility framework list for
 that Android version for more information. In many cases, these
 types of changes are experimental and can be ignored. |

### Restrictions on toggling changes
| Build type | Non-debuggable app | Debuggable app |
| --- | --- | --- |
| All changes | Changes gated by targetSDKVersion | All other changes |
| Developer Preview or Beta build | Can't toggle | Can toggle |
| Public user build | Can't toggle | Can toggle |

### Non-SDK API lists
| List | Code tags | Description |
| --- | --- | --- |
| Blocklist | blocked 
 Deprecated: blacklist | Non-SDK interfaces that you cannot use regardless of your app's
 target API level .
 If your app attempts to access one of these interfaces, the system
 throws an error . |
| Conditionally blocked | max-target-x 
 Deprecated: greylist-max-x | Starting with Android 9 (API level 28), each API level has non-SDK
 interfaces that are restricted when an app targets that API level. 
 These lists are labelled by the maximum API level
 ( max-target-x ) that an app can target before the app can no
 longer access the non-SDK interfaces in that list. For example, a
 non-SDK interface that was not blocked in Android Pie but is now blocked
 in Android 10 is part of the max-target-p 
 ( greylist-max-p ) list, where "p" stands for Pie or Android
 9 (API level 28). 
 If your app attempts to access an interface that is restricted for your
 target API level, the system
 behaves as if the API is part of
 the blocklist . |
| Unsupported | unsupported 
 Deprecated: greylist | Non-SDK interfaces that are unrestricted and your app can use. Note
 however, that these interfaces are unsupported and
 subject to change without notice. Expect these interfaces to be
 conditionally blocked in future Android versions in a
 max-target-x list. |
| SDK | Both public-api and sdk 
 Deprecated: Both public-api and whitelist | Interfaces that can be freely used and are now supported as part of the
 officially documented Android framework
 Package Index . |
| Test APIs | test-api | Interfaces that are used for internal system testing, such as APIs that
 facilitate testing through the Compatibility Test Suite (CTS).
 Test APIs are not part of the SDK.
 Starting in
 Android 11 (API level 30) , test APIs are included in the blocklist, so
 apps aren't allowed to use them regardless of their target API level. All
 test APIs are unsupported and subject to change without notice, regardless
 of the platform API level. |

### Expected behavior when restricted non-SDK interfaces are accessed
| Means of access | Result |
| --- | --- |
| Dalvik instruction referencing a field | NoSuchFieldError thrown |
| Dalvik instruction referencing a method | NoSuchMethodError thrown |
| Reflection using Class.getDeclaredField() or Class.getField() | NoSuchFieldException thrown |
| Reflection using Class.getDeclaredMethod() , Class.getMethod() | NoSuchMethodException thrown |
| Reflection using Class.getDeclaredFields() , Class.getFields() | Non-SDK members not in results |
| Reflection using Class.getDeclaredMethods() , Class.getMethods() | Non-SDK members not in results |
| JNI using env->GetFieldID() | NULL returned, NoSuchFieldError thrown |
| JNI using env->GetMethodID() | NULL returned, NoSuchMethodError thrown |

## Guidelines
- App compatibility starts to affect your users immediately when they update to
the latest version of Android, whether they've purchased a new device or
installed an update on their current device. They're excited to explore the
latest version of Android, and they want to experience it with their favorite
apps. If their apps don't work properly, it can cause major issues both for them
and for you.
- As part of our ongoing effort to gradually move developers away from non-SDK
APIs, we update the lists of restricted non-SDK interfaces in each Android
release. As always, your feedback and requests for public API equivalents 
are welcome.
- Select your app from the list. 
 Note: You must use a debuggable build variant of your app to toggle
changes on and off.
- Note: You must use a debuggable build variant of your app to toggle
changes on and off.
- Note: During the Android 15 preview until the API level is finalized, some
changes that are only enabled when targeting Android 15 use a value of
 10000 for the API level instead of the eventual, presumed API level of
 35 .
- D CompatibilityChangeReporter: Compat change id reported: 194833441; UID 10265; state: ENABLED
 Note: Each change is only logged, at most, once per process. Force stop and
restart your app's process to ensure that you see all relevant logcat messages. 
 Each logcat message includes the following information:
- Note: Each change is only logged, at most, once per process. Force stop and
restart your app's process to ensure that you see all relevant logcat messages.
- The main purpose of the compatibility framework is to provide you with control
and flexibility as you test your app with newer versions of Android. This
section describes some strategies you can use to determine when to toggle
changes on or off as you test and debug your app.
- Because these changes can affect all apps regardless of targetSDKVersion ,
you should usually test and update your app for these changes before changes
that are gated by targetSDKVersion . This helps ensure that your users
won't have a degraded app experience when they update their device to a new
platform version.
- You should also prioritize testing these changes because you can't toggle
these changes off when using a public release build of Android .
Ideally, you should perform testing on these changes for each version of
Android while that version is in preview .
- Note: Whenever you toggle a change for an app using either the developer options
or ADB commands, the app will be killed to ensure that your override takes
effect immediately.
- You can also use the following command to reset a change back to its default
state, removing any override that you've set using ADB or the developer options:
- To avoid crashes and unexpected behavior, apps should only use the officially
documented parts of the classes in the SDK. This also means that you shouldn't
access methods or fields that are not listed in the SDK when you interact with a
class using mechanisms such as reflection.
- With each release of Android, additional non-SDK interfaces are restricted. We
know these restrictions can impact your release workflow, and we want to make
sure you have the tools to detect usage of non-SDK interfaces, an opportunity to
 give us feedback , and time to plan and adjust to the new policies.
- To minimize the impact of non-SDK restrictions on your development workflow, the
non-SDK interfaces are divided into lists that define how tightly their use is
restricted, depending on which API level is being targeted. The following table
describes each of these lists:
- There are several methods that you can use to test for non-SDK interfaces in
your app.
- You can test for non-SDK interfaces by building and running a
 debuggable app on a device or emulator running Android 9 (API level 28) or
higher. Make sure that the device or emulator that you are using matches the
 target API level of your app.
- You can use adb logcat to access these log messages, which appear under the
PID of the running app. For example, an entry in the log might read as follows:
- For more information, see the Android Compatibility section in Use pre-launch
reports to identify issues .
- Why you need to use these APIs, including details about the high-level
feature that the API is necessary for, not just low level details.

## Core Concepts

**App Compatibility Testing and Debugging**
- **Explanation**: Developers can use tools like `adb`, logcat, and the compatibility framework's developer settings to identify which changes are enabled or disabled based on their current build settings. This is crucial for ensuring that apps function correctly across different Android versions.
- **Failure Mode**: Not testing compatibility changes can lead to unexpected behavior in newer Android versions due to restricted non-SDK interfaces.

**Non-SDK Interface Restrictions**
- **Explanation**: Non-SDK interface usage is restricted based on the target SDK version, affecting how apps behave when they try to access unsupported or blocked interfaces. This is crucial for maintaining app stability and preventing runtime errors.
- **Failure Mode**: Accessing non-SDK interfaces can cause runtime errors (e.g., `NoSuchFieldError`, `NoSuchMethodError`) due to their lack of guaranteed stability.

**Logging Compatibility Changes**
- **Explanation**: Developers can track the status and impact of platform behavior changes by analyzing logs generated by the `CompatibilityChangeReporter`. This helps in identifying which compatibility changes are enabled or disabled for a specific app.
- **Failure Mode**: Incorrect interpretation or oversight of logged changes can result in missed updates or improper app behavior.

**Changing App Behavior via ADB Commands**
- **Explanation**: Using `adb shell am compat` commands, developers can enable, disable, or reset specific compatibility changes to test and debug their apps. This is important for ensuring that apps behave as expected across different Android versions.
- **Failure Mode**: Enabling non-SDK interfaces in production builds through these commands can lead to instability due to the unreliability of non-SDK interface usage.

**Target API Levels and Non-SDK Interfaces**
- **Explanation**: The availability of certain APIs is governed by the Android version and target SDK level, impacting compatibility when moving to newer platform releases. Developers must adhere to restrictions based on their app's target SDK version.
- **Failure Mode**: Ignoring these guidelines can result in app crashes or degraded performance due to unsupported API usage.

**Automatic Toggling of Compatibility Changes**
- **Explanation**: Some compatibility changes are automatically enabled or disabled based on the app’s target SDK version. For example, if an app targets a lower SDK version than required for a change, that change will be enabled by default when the app increases its target SDK version.
- **Failure Mode**: Ignoring automatic toggling rules can lead to unexpected behavior in newer Android versions due to untested or improperly configured compatibility settings.

## Mental Model

**The Problem**: App compatibility issues arise when developers fail to adapt their applications to new Android platform changes without proper testing or adherence to API restrictions. This can lead to unexpected behavior, crashes, and degraded user experience.

**Core Insight**: Developers must proactively test for non-SDK interface usage in their apps using debuggable builds and tools like ADB commands and logcat logs. Understanding the restrictions across different SDK versions is crucial to maintain app stability and compatibility.

**How concepts connect**:
- **App Compatibility Testing → Identifying Changes**: Using ADB commands and developer options allows developers to identify which changes are enabled or disabled based on their current build settings.
- **Non-SDK Interface Restrictions → Logging Behavior**: Developers must monitor the logs for any non-compliance issues that arise due to restricted interfaces, ensuring they understand how these restrictions affect app behavior.

## Guidelines
- App compatibility starts affecting users immediately when they update to the latest version of Android. This means apps need to be tested thoroughly before release.
- Gradual updates to the lists of restricted non-SDK APIs help developers adapt their applications incrementally without major disruptions.
- Using debuggable builds is essential for testing and toggling changes effectively.
- Non-SDK interface restrictions may vary across different Android versions, requiring careful consideration during app development.

## Decision Tables
| I need to... | Use | NOT | Because |
| --- | --- | --- | --- |
| Test compatibility changes | ADB commands | Developer options | For non-debuggable builds, only ADB can be used. Debuggable builds allow both methods. |

---

## Common Mistakes

### Enabling Non-SDK Interfaces in Production Builds
- **Looks like**: 
  ```java
  adb shell settings put global hidden_api_policy 1
  ```
- **Why it breaks**: This command enables access to non-SDK interfaces, leading to instability and unexpected behavior as these interfaces may change or be removed in future Android versions.
- **Correct**: Use debuggable builds and test environments to toggle changes via ADB or logcat. Avoid making such settings permanent for release builds.

### Misinterpreting Log Output
- **Looks like**:
  ```log
  D CompatibilityChangeReporter: Compat change id reported: 194833441; UID 10265; state: ENABLED
  ```
- **Why it breaks**: Incorrect interpretation of the log output can lead to overlooking critical changes that need testing or adjustment.
- **Correct**: Ensure developers understand how to interpret these logs accurately, identifying enabled and logged states correctly.

---

## Key Relationships

**App Compatibility Testing requires ADB Commands / ADB Commands enable testing for compatibility issues**
- Developers must use tools like `adb` and logcat to test their apps' behavior in different Android versions.

**Non-SDK Interface Restrictions affect App Behavior / Monitoring with Logcat helps identify Non-SDK Interface Usage**
- Restricted non-SDK interfaces can cause runtime errors, while monitoring logs allows developers to detect such issues early.

## Concepts (for graph)
- Why app compatibility is important
- Types of platform behavior changes
- Changes for all apps
- Targeted changes
- Compatibility framework tools
- Restrictions on non-SDK interfaces
- Platform releases
- How to identify which changes are enabled
- Identify enabled changes using developer options
- Figure 1.
- Default Enabled Changes
- Enabled for targetSdkVersion >=33

<!-- Quality Report
## Quality Report

| Section | Score | Issue (if < 4) |
| --- | --- | --- |
| Core Concepts | 5 | N/A |
| Mental Model | 4 | Minor improvements possible for clarity. |
| Decision Framework | 5 | N/A |
| Common Mistakes | 5 | N/A |
| Key Relationships | 5 | N/A |

## Verdict: PASS

No sections scored below 4, indicating that the knowledge base entry is precise and actionable with no hallucinations or vague claims.
-->
