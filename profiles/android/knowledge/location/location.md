<!-- Source: https://developer.android.com/develop/sensors-and-location/location -->
<!-- Source: https://developer.android.com/develop/sensors-and-location/location/permissions -->
<!-- Source: https://developer.android.com/develop/sensors-and-location/location/permissions/runtime -->
<!-- Source: https://developer.android.com/develop/sensors-and-location/location/permissions/background -->
<!-- Source: https://developer.android.com/develop/sensors-and-location/location/retrieve-current -->
<!-- Source: https://developer.android.com/develop/sensors-and-location/location/change-location-settings -->
<!-- Source: https://developer.android.com/develop/sensors-and-location/location/request-updates -->
<!-- Source: https://developer.android.com/develop/sensors-and-location/location/background -->
<!-- Source: https://developer.android.com/develop/sensors-and-location/location/geofencing -->
<!-- Source: https://developer.android.com/develop/sensors-and-location/location/transitions -->
<!-- Source: https://developer.android.com/develop/sensors-and-location/location/battery -->
<!-- Source: https://developer.android.com/develop/sensors-and-location/location/battery/optimize -->
<!-- Source: https://developer.android.com/develop/sensors-and-location/location/battery/scenarios -->
<!-- Source: https://developer.android.com/develop/sensors-and-location/location/testing -->
<!-- Source: https://developer.android.com/develop/sensors-and-location/location/migration -->
<!-- Source: https://developer.android.com/develop/sensors-and-location/location/maps-and-places -->
<!-- Type: official -->
<!-- Priority: high -->
<!-- Topic: location -->
<!-- Extracted: 2026-03-24 -->
<!-- Verified: — -->

# Build location-aware apps

## Rules
- DO: Your app is running a foreground service. When a foreground service is
running, the system raises user awareness by showing a persistent
notification. Your app retains access when it's placed in the background,
such as when the user presses the Home button on their device or turns
their device's dis
- DO: At first, your app should guide users to the features that require
foreground location access, such as the "share location" feature in Figure 1
or the "show current location" feature in Figure 2. 

 It's recommended that you disable user access to features that require
background location access unt
- DO: An option for users to decline the permission. If users decline background
location access, they should be able to continue using your app.
- DON'T: The device never recorded its location, which could be the case of a new
 device or a device that has been restored to factory settings.
- DON'T: Google Play services on the device has restarted, and there is no active
 Fused Location Provider client that has requested location after the
 services restarted. To avoid this situation you can create a new client and
 request location updates yourself. For more information, see Request location
- DO: Use the following checklist to identify potential location access logic in the
background:
- DON'T: If you don't need location access in the background, remove it. 

 If your app targets Android 10 (API level 29) or higher, remove the
 ACCESS_BACKGROUND_LOCATION 
permission 
from your app's manifest. When you remove this permission, all-the-time
access to location isn't an option for the app on de
- DO: Use a larger geofence radius for locations where a user spends a significant amount of time,
such as home or work. While a larger radius doesn't directly reduce power consumption, it reduces
the frequency at which the app checks for entrance or exit, effectively lowering overall power
consumption.
- DO: The device is rebooted. The app should listen for the device's boot complete action, and then re-
register the geofences required.
- DON'T: Wi-Fi is turned off on the device. Having Wi-Fi on can significantly improve
the location accuracy, so if Wi-Fi is turned off, your application might never get geofence alerts
depending on several settings including the radius of the geofence, the device model, or the
Android version. Starting from
- DO: Use the balanced power or low power options to satisfy the location needs of
most apps. Reserve high accuracy for apps that run in the foreground and require
 real time location updates (for example, a mapping app).
- DO: Use the setIntervalMillis() method to specify the interval for
computing your app's location.
- DO: Use the setMinUpdateIntervalMillis() method to specify the interval
for receiving other apps' locations.
- DO: Recommendations : This guide lays out some concrete recommended
actions you can use to improve your app's impact on battery life.
- DO: Use cases : This guide provides several common use cases
where you might use location services and how you could optimise the impact
on battery life for those cases.
- DO: Use the setPriority() method with a value of
 PRIORITY_HIGH_ACCURACY or PRIORITY_BALANCED_POWER_ACCURACY .
- DO: Use the getLastLocation() method, which returns the most recently
available location (which in rare cases may be null). This method provides a
straightforward way of getting location and doesn't incur costs associated with
actively requesting location updates. Use in conjunction with the
 isLocation
- DO: Use geofencing in conjunction with fused location provider updates.
Request updates when the app receives a geofence entrance trigger, and remove
updates when the app receives a geofence exit trigger. This ensures that the app
gets more granular location updates only when the user has entered a defi
- DO: Use the Activity Recognition API in conjunction with fused location
provider updates. Request updates when the targeted activity is detected, and
remove updates when the user stops performing that activity.
- DO: Use the setNotificationResponsiveness() , passing a value of
approximately five minutes. However, consider using a value of approximately
ten minutes if your app can manage the extra delay in responsiveness.
- DO: Use the setPriority() method with the PRIORITY_NO_POWER option if
possible because it incurs almost no battery drain. If using PRIORITY_NO_POWER 
isn't possible, use PRIORITY_BALANCED_POWER_ACCURACY or
 PRIORITY_LOW_POWER , but avoid using PRIORITY_HIGH_ACCURACY for
sustained background work because
  WHY: it incurs almost no battery drain
- DO: Use a foreground service. If expensive work is potentially going to be done by
your app on behalf of the user, making the user aware of that work is a
recommended best practice. A foreground service requires a persistent
notification. For more information, see Notifications Overview .
- DO: Use the location settings API to validate the current location settings.
- DO: Use Google Play services for complex features like geofencing, activity
recognition, and awareness.
- DO: Use the location settings API to check the current settings.

## Code Patterns
### Foreground location
```xml
<!-- Recommended for Android 9 (API level 28) and lower. -->
<!-- Required for Android 10 (API level 29) and higher. -->
<service
    android:name="MyNavigationService"
    android:foregroundServiceType="location" ... >
    <!-- Any inner elements would go here. -->
</service>
```

### Foreground location
```xml
<manifest ... >
  <!-- Always include this permission -->
  <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />

  <!-- Include only if your app benefits from precise location access. -->
  <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
</manifest>
```

### Background location
```xml
<manifest ... >
  <!-- Required only when requesting background location access on
       Android 10 (API level 29) and higher. -->
  <uses-permission android:name="android.permission.ACCESS_BACKGROUND_LOCATION" />
</manifest>
```

### User can grant only approximate location
```
ACCESS_FINE_LOCATION must be requested with ACCESS_COARSE_LOCATION.
```

### User choice affects permission grants
```kotlin
@RequiresApi(Build.VERSION_CODES.N)
fun requestPermissions() {
    val locationPermissionRequest = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { permissions ->
        when {
            permissions.getOrDefault(Manifest.permission.ACCESS_FINE_LOCATION, false) -> {
                // Precise location access granted.
            }
            permissions.getOrDefault(Manifest.permission.ACCESS_COARSE_LOCATION, false) -> {
                // Only approximate location access granted.
            }
            else -> {
                // No location access granted.
            }
        }
    }

    // Before you perform the actual permission request, check whether your app
    // already has the permissions, and whether your app needs to show a permission
    // rationale dialog. For more details, see Request permissions:
    // https://developer.android.com/training/permissions/requesting#request-permission
    locationPermissionRequest.launch(
        arrayOf(
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.ACCESS_COARSE_LOCATION
        )
    )
}LocationPermissionsActivity.kt
```

### Create location services client
```kotlin
private lateinit var fusedLocationClient: FusedLocationProviderClient

override fun onCreate(savedInstanceState: Bundle?) {
    // ...

    fusedLocationClient = LocationServices.getFusedLocationProviderClient(this)
}
```

### Get the last known location
```
fusedLocationClient.lastLocation
        .addOnSuccessListener { location : Location? ->
            // Got last known location. In some rare situations this can be null.
        }
```

### Set up a location request
```kotlin
fun createLocationRequest() {
    val locationRequest = LocationRequest.Builder(Priority.PRIORITY_HIGH_ACCURACY, 10000)
        .setMinUpdateIntervalMillis(5000)
        .build()
}
```

### Get current location settings
```kotlin
val builder = LocationSettingsRequest.Builder()
        .addLocationRequest(locationRequest)
```

### Get current location settings
```kotlin
val builder = LocationSettingsRequest.Builder()

// ...

val client: SettingsClient = LocationServices.getSettingsClient(this)
val task: Task<LocationSettingsResponse> = client.checkLocationSettings(builder.build())
```

### Prompt the user to change location settings
```
task.addOnSuccessListener { locationSettingsResponse ->
    // All location settings are satisfied. The client can initialize
    // location requests here.
    // ...
}

task.addOnFailureListener { exception ->
    if (exception is ResolvableApiException){
        // Location settings are not satisfied, but this can be fixed
        // by showing the user a dialog.
        try {
            // Show the dialog by calling startResolutionForResult(),
            // and check the result in onActivityResult().
            exception.startResolutionForResult(this@MainActivity,
                    REQUEST_CHECK_SETTINGS)
        } catch (sendEx: IntentSender.SendIntentException) {
            // Ignore the error.
        }
    }
}
```

### Make a location request
```kotlin
override fun onResume() {
    super.onResume()
    if (requestingLocationUpdates) startLocationUpdates()
}

private fun startLocationUpdates() {
    fusedLocationClient.requestLocationUpdates(locationRequest,
            locationCallback,
            Looper.getMainLooper())
}
```

### Define the location update callback
```kotlin
private lateinit var locationCallback: LocationCallback

// ...

override fun onCreate(savedInstanceState: Bundle?) {
    // ...

    locationCallback = object : LocationCallback() {
        override fun onLocationResult(locationResult: LocationResult?) {
            locationResult ?: return
            for (location in locationResult.locations){
                // Update UI with location data
                // ...
            }
        }
    }
}
```

### Stop location updates
```kotlin
override fun onPause() {
    super.onPause()
    stopLocationUpdates()
}

private fun stopLocationUpdates() {
    fusedLocationClient.removeLocationUpdates(locationCallback)
}
```

### Save the state of the activity
```kotlin
override fun onSaveInstanceState(outState: Bundle?) {
    outState?.putBoolean(REQUESTING_LOCATION_UPDATES_KEY, requestingLocationUpdates)
    super.onSaveInstanceState(outState)
}
```

### Save the state of the activity
```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
    // ...
    updateValuesFromBundle(savedInstanceState)
}

private fun updateValuesFromBundle(savedInstanceState: Bundle?) {
    savedInstanceState ?: return

    // Update the value of requestingLocationUpdates from the Bundle.
    if (savedInstanceState.keySet().contains(REQUESTING_LOCATION_UPDATES_KEY)) {
        requestingLocationUpdates = savedInstanceState.getBoolean(
                REQUESTING_LOCATION_UPDATES_KEY)
    }

    // ...

    // Update UI to match restored state
    updateUI()
}
```

### Set up for geofence monitoring
```xml
<application
   android:allowBackup="true">
   ...
   <receiver android:name=".GeofenceBroadcastReceiver"/>
<application/>
```

### Set up for geofence monitoring
```kotlin
lateinit var geofencingClient: GeofencingClient

override fun onCreate(savedInstanceState: Bundle?) {
    // ...
    geofencingClient = LocationServices.getGeofencingClient(this)
}
```

### Create geofence objects
```
geofenceList.add(Geofence.Builder()
    // Set the request ID of the geofence. This is a string to identify this
    // geofence.
    .setRequestId(entry.key)

    // Set the circular region of this geofence.
    .setCircularRegion(
        entry.value.latitude,
        entry.value.longitude,
        Constants.GEOFENCE_RADIUS_IN_METERS
    )

    // Set the expiration duration of the geofence. This geofence gets automatically
    // removed after this period of time.
    .setExpirationDuration(Constants.GEOFENCE_EXPIRATION_IN_MILLISECONDS)

    // Set the transition types of interest. Alerts are only generated for these
    // transition. We track entry and exit transitions in this sample.
    .setTransitionTypes(Geofence.GEOFENCE_TRANSITION_ENTER or Geofence.GEOFENCE_TRANSITION_EXIT)

    // Create the geofence.
    .build())
```

### Specify geofences and initial triggers
```kotlin
private fun getGeofencingRequest(): GeofencingRequest {
    return GeofencingRequest.Builder().apply {
        setInitialTrigger(GeofencingRequest.INITIAL_TRIGGER_ENTER)
        addGeofences(geofenceList)
    }.build()
}
```

### Define a broadcast receiver for geofence transitions
```kotlin
class MainActivity : AppCompatActivity() {

    // ...

    private val geofencePendingIntent: PendingIntent by lazy {
        // We use FLAG_UPDATE_CURRENT so that we get the same pending intent back when calling
        // addGeofences() and removeGeofences().
        val flags = PendingIntent.FLAG_UPDATE_CURRENT
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.S) {
            // Starting on Android S+ the pending intent has to be mutable.
            flags or PendingIntent.FLAG_MUTABLE
        }
        val intent = Intent(this, GeofenceBroadcastReceiver::class.java)
        PendingIntent.getBroadcast(this, 0, intent, flags)
    }

}
```

### Add geofences
```
geofencingClient?.addGeofences(getGeofencingRequest(), geofencePendingIntent)?.run {
    addOnSuccessListener {
        // Geofences added
        // ...
    }
    addOnFailureListener {
        // Failed to add geofences
        // ...
    }
}
```

### Handle geofence transitions
```kotlin
class GeofenceBroadcastReceiver : BroadcastReceiver() {
    // ...
    override fun onReceive(context: Context?, intent: Intent?) {
        val geofencingEvent = GeofencingEvent.fromIntent(intent)
        if (geofencingEvent.hasError()) {
            val errorMessage = GeofenceStatusCodes
                    .getStatusCodeString(geofencingEvent.errorCode)
            Log.e(TAG, errorMessage)
            return
        }

        // Get the transition type.
        val geofenceTransition = geofencingEvent.geofenceTransition

        // Test that the reported transition was of interest.
        if (geofenceTransition == Geofence.GEOFENCE_TRANSITION_ENTER ||
                geofenceTransition == Geofence.GEOFENCE_TRANSITION_EXIT) {

            // Get the geofences that were triggered. A single event can trigger
            // multiple geofences.
            val triggeringGeofences = geofencingEvent.triggeringGeofences

            // Get the transition details as a String.
            val geofenceTransitionDetails = getGeofenceTransitionDetails(
                    this,
                    geofenceTransition,
                    triggeringGeofences
            )

            // Send notification and log the transition details.
            sendNotification(geofenceTransitionDetails)
            Log.i(TAG, geofenceTransitionDetails)
        } else {
            // Log the error.
            Log.e(TAG, getString(R.string.geofence_transition_invalid_type,
                    geofenceTransition))
        }
    }
}
```

### Stop geofence monitoring
```
geofencingClient?.removeGeofences(geofencePendingIntent)?.run {
    addOnSuccessListener {
        // Geofences removed
        // ...
    }
    addOnFailureListener {
        // Failed to remove geofences
        // ...
    }
}
```

### Set up your project
```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
         package="com.example.myapp">

   <uses-permission android:name="com.google.android.gms.permission.ACTIVITY_RECOGNITION" />
   …
 </manifest>
```

### Register for activity transition updates
```kotlin
val transitions = mutableListOf<ActivityTransition>()

transitions +=
        ActivityTransition.Builder()
          .setActivityType(DetectedActivity.IN_VEHICLE)
          .setActivityTransition(ActivityTransition.ACTIVITY_TRANSITION_ENTER)
          .build()

transitions +=
        ActivityTransition.Builder()
          .setActivityType(DetectedActivity.IN_VEHICLE)
          .setActivityTransition(ActivityTransition.ACTIVITY_TRANSITION_EXIT)
          .build()

transitions +=
        ActivityTransition.Builder()
          .setActivityType(DetectedActivity.WALKING)
          .setActivityTransition(ActivityTransition.ACTIVITY_TRANSITION_EXIT)
          .build()
```

### Register for activity transition updates
```kotlin
val request = ActivityTransitionRequest(transitions)
```

### Register for activity transition updates
```kotlin
// myPendingIntent is the instance of PendingIntent where the app receives callbacks.
val task = ActivityRecognition.getClient(context)
        .requestActivityTransitionUpdates(request, myPendingIntent)

task.addOnSuccessListener {
    // Handle success
}

task.addOnFailureListener { e: Exception ->
    // Handle error
}
```

### Process activity transition events
```kotlin
override fun onReceive(context: Context, intent: Intent) {
    if (ActivityTransitionResult.hasResult(intent)) {
        val result = ActivityTransitionResult.extractResult(intent)!!
        for (event in result.transitionEvents) {
            // chronological sequence of events....
        }
    }
}
```

### Batch requests
```kotlin
val request = LocationRequest.Builder(Priority.PRIORITY_HIGH_ACCURACY, 10 * 60 * 1000)
.setMaxUpdateDelayMillis(60 * 60 * 1000)
.build()
```

## Pitfalls
- Caution: If the user downgrades your app's location access from precise to
approximate, either from the permission dialog or in system settings, the system
restarts your app's process. For these reasons, it's especially important that
you follow best practices for requesting runtime permissions .
- Caution: If your app targets Android 11 (API level 30) or higher, the system
enforces this best practice. If you request a foreground location permission and
the background location permission at the same time, the system ignores the
request and doesn't grant your app either permission.

## Decision Tables
### User choice affects permission grants
|  | Precise | Approximate |
| --- | --- | --- |
| While using the app | ACCESS_FINE_LOCATION and 
 ACCESS_COARSE_LOCATION | ACCESS_COARSE_LOCATION |
| Only this time | ACCESS_FINE_LOCATION and 
 ACCESS_COARSE_LOCATION | ACCESS_COARSE_LOCATION |
| Deny | No location permissions | No location permissions |

## Guidelines
- Location
 in Android 10 with Kotlin : Learn how to request location on devices that run
 Android 10, including requesting location while the app is in use.
- To protect user privacy, apps that use location services must request location
permissions.
- Multiple permissions are related to location. Which permissions you request,
and how you request them,
depend on the location requirements for your app's use case.
- Additionally, you should declare a foreground service type of
 location , as shown in the following code snippet. On Android
10 (API level 29) and higher, you must declare this foreground service type.
- On Android 10 (API level 29) and higher, you must declare the
 ACCESS_BACKGROUND_LOCATION permission in your app's manifest in order to
 request background location access at runtime. On earlier versions of
Android, when your app receives foreground location access, it automatically
receives background location access as well.
- Your app should still work when the user grants only approximate location
access. If a feature in your app absolutely requires access to precise location
using the ACCESS_FINE_LOCATION permission, you can ask the user to allow your
app to access precise location .
- Sample app 
to demonstrate the use of location permissions.
- ACCESS_FINE_LOCATION must be requested with ACCESS_COARSE_LOCATION.
 Note: To better respect user privacy, it's recommended that you only request
 ACCESS_COARSE_LOCATION . You can fulfill most use cases even when you have
access to only approximate location information. Figure 2 shows the
user-facing dialog that appears when your app targets Android 12
and requests only ACCESS_COARSE_LOCATION .
- Note: To better respect user privacy, it's recommended that you only request
 ACCESS_COARSE_LOCATION . You can fulfill most use cases even when you have
access to only approximate location information. Figure 2 shows the
user-facing dialog that appears when your app targets Android 12
and requests only ACCESS_COARSE_LOCATION .
- To determine which permissions the system has granted to your app, check the
return value of your permissions request. You can use Jetpack libraries in code
that's similar to the following, or you can use platform libraries, where you
 manage the permission request code yourself .
- Figure 6 shows an example of an app that's designed to handle incremental
requests. Both the "show current location" and "recommend nearby places"
features require foreground location access. Only the "recommend nearby places"
feature, however, requires background location access.
- Note: If a feature in your app accesses location from the background, verify
that access is necessary. Consider getting the information that the feature
needs in other ways. To learn more about background location access, see the
 Access location in the background page.
- On Android 11 (API level 30) and higher, however, the system dialog doesn't
include the Allow all the time option. Instead, users must enable background
location on a settings page, as shown in figure 7.
- As long as your app already follows best practices for requesting location
permissions, you don't need to make any changes to support this behavior.
- Specifically, use the
 fused
 location provider to retrieve the device's last known location. The fused
 location provider is one of the location APIs in Google Play services. It
 manages the underlying location technology and provides a simple API so that
 you can specify requirements at a high level, like high accuracy or low power.
 It also optimizes the device's use of battery power.
- Note: When your app is running in the background,
 access to location should be
 critical to the core functionality of the app and is accompanied with proper
 disclosure to users.
- Apps whose features use location services must
 request location permissions ,
depending on the use cases of those features.
- The FusedLocationProviderClient provides several methods to retrieve device
location information. Choose from one of the following, depending on your app's
use case:
- This lesson shows you how to use the
 Settings Client 
 to check which settings are enabled, and present the Location Settings
 dialog for the user to update their settings with a single tap.
- In order to use the location services provided by Google Play Services and
 the fused location provider, connect your app using the
 Settings Client ,
 then check the current location settings and prompt the user to enable the
 required settings if needed.

 Apps whose features use location services must
 request location permissions ,
depending on the use cases of those features.

## Core Concepts

1. **Requesting Location Permissions**
   - Explanation: Proper handling of location access is crucial for respecting user privacy while providing necessary functionalities.
   - Failure Mode: Incorrectly requesting only `ACCESS_FINE_LOCATION` can violate user trust and potentially cause system-level restrictions on background services.

2. **Foreground Services for Continuous Background Operations**
   - Explanation: Declaring the proper service type ensures that the app can continue running in the background, but also mandates showing a persistent notification to inform users of continuous operations.
   - Failure Mode: Failing to declare this service type can result in the system terminating your app's process if it attempts to run continuously without user consent.

3. **Geofencing and Activity Recognition**
   - Explanation: Setting up geofences allows monitoring specific areas for location-based triggers, while activity recognition enhances these by providing context based on detected activities.
   - Failure Mode: Without proper setup or continuous updates, critical features relying on these services may fail to operate correctly.

4. **Battery Optimization Techniques**
   - Explanation: Optimizing battery usage is essential for maintaining app usability and user satisfaction over time.
   - Failure Mode: Failing to optimize can lead to excessive battery drain, prompting users to restrict background location access or uninstall the app entirely.


## Mental Model

- **The Problem**: Location-aware apps require proper handling of permissions, service types, and background operations to ensure user privacy while still providing essential features.
- **Core Insight**: Developers must carefully manage location access requests based on the app's requirements, ensuring that they follow best practices to respect user privacy and device battery life.
- **How concepts connect**:
   - Permissions → Services: Proper permissions are required for foreground services which in turn require a persistent notification for background operations.
   - Services → Geofencing: Foreground services allow continuous location monitoring necessary for geofence setup and activity recognition.

## Decision Framework
| I need to... | Use | NOT | Because |
| --- | --- | --- | --- |
| Request precise location access | `ACCESS_FINE_LOCATION` and `ACCESS_COARSE_LOCATION` | `ACCESS_FINE_LOCATION` alone | Requires both permissions for better accuracy while respecting user privacy. |

## How It Works Internally

- **Location Permissions**: Both `ACCESS_FINE_LOCATION` and `ACCESS_COARSE_LOCATION` must be requested to ensure proper permission handling and respect user preferences.
  - Practical Implication: Developers should request coarse location access as a baseline, offering fine-grained location only for specific high-accuracy use cases.

## Key Relationships

- Permissions require Services: To effectively utilize background location functionalities, an app must declare appropriate permissions and foreground service types to maintain continuous operation while respecting user privacy.
- Geofencing requires Activity Recognition: Setting up geofences combined with activity recognition enhances the functionality of location-based services in apps by providing context-aware triggers for actions.

## Concepts (for graph)
- Build location-aware apps
- Development resources
- Request the proper permissions
- Receive location updates
- Optimize power usage
- Add maps to your app
- Latest news
- Additional resources
- Codelabs
- Samples
- Location Permissions
- Current Location

<!-- Quality Report
## Quality Report

| Section | Score | Issue (if < 4) |
| --- | --- | --- |
| Core Concepts | 5 | None |
| Mental Model | 4 | Some details could be more concise |
| Decision Framework | 3 | Lacks clear distinction between 'Use' and 'NOT' actions |
| Common Mistakes | 1 | Missing section; no common mistakes listed |
| Key Relationships | 5 | None |

## Verdict: NEEDS_FIX

## Fixes (only if NEEDS_FIX)
Mental Model: Tighten explanations for better clarity.
Decision Framework: Clarify the distinction between permissions to use and not to use based on context.
-->
