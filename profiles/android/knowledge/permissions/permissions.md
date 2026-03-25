<!-- Source: https://developer.android.com/guide/topics/permissions/overview -->
<!-- Type: official -->
<!-- Priority: high -->
<!-- Topic: permissions -->
<!-- Extracted: 2026-03-24 -->
<!-- Verified: — -->

# Permissions on Android

## Guidelines
- If your app offers functionality that might require access to restricted data or
restricted actions, determine whether you can get the information or perform the
actions without needing to declare
permissions . You can fulfill many use cases
in your app, such as taking photos, pausing media playback, and displaying
relevant ads, without needing to declare any permissions.
- If you decide that your app must access restricted data or perform restricted
actions to fulfill a use case, declare the appropriate permissions. Some
permissions, known as install-time permissions , are
automatically granted when your app is installed. Other permissions, known as
 runtime permissions , require your app to go a step further and
request the permission at runtime.
- Applications that implement privileged services, such as autofill or VPN
services, also make use of signature permissions. These apps require
service-binding signature permissions so that only the system can bind
to the services.
- Note: Some signature permissions aren't for use by third-party apps.
- When the user requests a particular action in your app, your app should request
only the permissions that it needs to complete that action. Depending on how you
are using the permissions, there might be an alternative way to fulfill your
app's use case without relying on access to
sensitive information.
- Request permissions as late into the flow of your app's use cases as possible.
For example, if your app lets users send audio messages to others, wait
until the user has navigated to the messaging screen and has pressed the Send
audio message button. After the user presses the button, your app can then
request access to the microphone.

## Core Concepts

1. **Permissions Types**:
   - Permissions are categorized into install-time and runtime based on their impact on user experience and system security.
   - Install-time permissions: Automatically granted when your app is installed, typically for less sensitive functionalities.
   - Runtime permissions: Require your app to request permission at runtime before accessing restricted data or performing actions.

2. **Workflow for Using Permissions**:
   - Proper timing in requesting permissions ensures a smooth user experience and minimizes disruption.
   - Example: When sending audio messages, request microphone permission only after the Send button is pressed.

3. **Restricted Data/Actions**:
   - Identifying which data or actions are restricted helps determine appropriate permission types (install-time vs runtime) and usage strategies.

## Mental Model

- **The Problem**: Managing sensitive functionalities while ensuring user privacy and security.
- **Core Insight**: Properly declaring and requesting permissions ensures that apps only perform necessary actions, minimizing risks to users.
- **How concepts connect**:
  - Restricted Data/Actions → Permissions Types: Identifying restricted functionalities leads to determining the appropriate permission type (install-time or runtime).
  - Workflow for Using Permissions → Permissions Types: The timing of permission requests depends on their type, ensuring minimal disruption to user experience.

## Decision Framework

| I need to... | Use | NOT | Because |
| --- | --- | --- | --- |
| Request access to restricted functionalities | Runtime permissions | Install-time permissions | For features requiring sensitive data or actions, runtime permissions offer better security and a smoother user experience by delaying permission requests until necessary. |

## Common Mistakes

- **Name**: Premature Permission Requests
  - **Looks like**:
    ```java
    // In onCreate method of an Activity
    ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.CAMERA}, REQUEST_CAMERA);
    ```
  - **Why it breaks**: This disrupts user experience by interrupting the flow and blocking access to non-sensitive functionalities unnecessarily.
  - **Correct**:
    ```java
    // In a click listener for a button that triggers camera use
    Button takePictureButton = findViewById(R.id.take_picture_button);
    takePictureButton.setOnClickListener(new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest.permission.CAMERA}, REQUEST_CAMERA);
        }
    });
    ```

## Concepts (for graph)
- Restricted data
- Restricted actions
- Workflow for using permissions
- Figure 1.
- Types of permissions
- Install-time permissions
- Figure 2.
- Runtime permissions
- Figure 3.
- Special permissions
- Special app access
- Permission groups

<!-- Quality Report
## Quality Report

| Section | Score | Issue (if < 4) |
| --- | --- | --- |
| Core Concepts | 5 | None |
| Mental Model | 4 | Could be more specific about the connections between concepts. |
| Decision Framework | 5 | None |
| Common Mistakes | 5 | None |
| Key Relationships | 3 | Missing details on how different permission types relate to each other in terms of security and user experience. |

## Verdict: NEEDS_FIX

## Fixes (only if NEEDS_FIX)
Key Relationships: Provide more detailed connections between install-time, runtime permissions, and their impact on security and user experience.
-->
