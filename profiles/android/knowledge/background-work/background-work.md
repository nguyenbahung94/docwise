<!-- Source: https://developer.android.com/develop/background-work/background-tasks -->
<!-- Source: https://developer.android.com/develop/background-work/services -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/bg-work-restrictions -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/data-transfer-options -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/uidt -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/persistent -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/persistent/getting-started -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/persistent/getting-started/define-work -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/persistent/how-to/states -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/persistent/how-to/manage-work -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/persistent/how-to/chain-work -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/persistent/how-to/long-running -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/persistent/how-to/observe -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/persistent/how-to/update-work -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/persistent/threading -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/persistent/threading/worker -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/persistent/threading/coroutineworker -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/persistent/threading/rxworker -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/persistent/threading/listenableworker -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/persistent/configuration/custom-configuration -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/testing/persistent/debug -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/testing/persistent/integration-testing -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/testing/persistent/worker-impl -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/persistent/migrate-from-legacy/firebase -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/persistent/migrate-from-legacy/gcm -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/optimize-battery -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/awake -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/awake/screen-on -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/awake/wakelock -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/awake/wakelock/set -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/awake/wakelock/release -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/awake/wakelock/best-practices -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/awake/wakelock/debug-locally -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/awake/wakelock/identify-wls -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/asynchronous -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/asynchronous/java-threads -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/asynchronous/listenablefuture -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/broadcasts -->
<!-- Source: https://developer.android.com/develop/background-work/background-tasks/broadcasts/broadcast-exceptions -->
<!-- Source: https://developer.android.com/develop/background-work/services/bound-services -->
<!-- Source: https://developer.android.com/develop/background-work/services/aidl -->
<!-- Source: https://developer.android.com/develop/background-work/services/fgs -->
<!-- Source: https://developer.android.com/develop/background-work/services/fgs/declare -->
<!-- Source: https://developer.android.com/develop/background-work/services/fgs/launch -->
<!-- Source: https://developer.android.com/develop/background-work/services/fgs/stop-fgs -->
<!-- Source: https://developer.android.com/develop/background-work/services/fgs/handle-user-stopping -->
<!-- Source: https://developer.android.com/develop/background-work/services/fgs/restrictions-bg-start -->
<!-- Source: https://developer.android.com/develop/background-work/services/fgs/timeout -->
<!-- Source: https://developer.android.com/develop/background-work/services/fgs/service-types -->
<!-- Source: https://developer.android.com/develop/background-work/services/fgs/troubleshooting -->
<!-- Source: https://developer.android.com/develop/background-work/services/fgs/changes -->
<!-- Source: https://developer.android.com/develop/background-work/services/alarms -->
<!-- Type: official -->
<!-- Priority: high -->
<!-- Topic: background-work -->
<!-- Extracted: 2026-03-24 -->
<!-- Verified: — -->

# Background tasks overview

## Rules
- DO: Use if one exists for that particular operation. Can yield benefits
 such as optimized performance and improved system integration.
- DO: You should define work constraints to specify the right
circumstances to run your job. For example, if your app needs to download
non-urgent resources, you might specify that the job should run while the
device is charging and connected to an unmetered network. WorkManager can
then run your job at a
- DO: Use a specific API if one is available (like the companion device
manager ); otherwise, use a connectedDevice foreground
service .
- DO: Call the setUserInitiated() method when building a
 JobInfo object. (This method is available beginning with
Android 14.) We also recommend that you offer a payload size
estimate by calling setEstimatedNetworkBytes() 
while creating your job. 

 
 Kotlin 
 val networkRequestBuilder = NetworkRequest
- DO: While the job is being executed, call
 setNotification() on the JobService object. Calling
 setNotification() makes the user aware that the job is running, both in
the Task Manager and in the status bar notification area. 

 When execution is complete, call jobFinished() to signal to the system
that
- DO: Clearly define network constraints and job execution constraints to specify
when the job should be executed.
- DON'T: Execute the task asynchronously in onStartJob() ; for example, you can do
this by using a coroutine . If you don't run the task asynchronously, the
work runs on the main thread and might block it, which can cause an ANR.
- DON'T: To avoid running the job longer than necessary, call
 jobFinished() when the transfer finishes, whether it
succeeds or fails. That way, the job doesn't run longer than necessary. To
discover why a job was stopped, implement the
 onStopJob() callback method and call
 JobParameters.getStopReason() .
- DO: Result.retry() : The work failed and should be tried at another time
according to its
 retry policy .
- DO: Backoff policy defines how the backoff delay should increase over time for
subsequent retry attempts. WorkManager supports 2 backoff policies,
 LINEAR and
 EXPONENTIAL .
- DO: RxWorker is the recommended
implementation for RxJava users. RxWorkers should be used if a lot of your
existing asynchronous code is modelled in RxJava. As with all RxJava concepts,
you are free to choose the threading strategy of your choice. Read more about
threading in RxWorker instances in Threa
- DON'T: As we mentioned, you do not set the constraints or tags when you define the
 Worker ; instead, you do this in the next step, when you create the
 WorkRequest .
- DO: Create a OneTimeWorkRequest 
or PeriodicWorkRequest , and
set any desired constraints specifying when the task should run, as well as
any tags to identify your work.
- DON'T: Is your app running a foreground service, and you need to keep the device
awake when screen is off while the service is running?
 
 If No , you do not need to keep the device awake. If the user is
actively interacting with the app, the device will stay awake. If the
user is not interacting with your
- DON'T: Would it be detrimental to the user experience if the device suspends while
the foreground service is running and the device screen is off? (For
example, if you're using a foreground service to update notifications, it
wouldn't be a bad user experience if the device is suspended.)
 
 If No , do not
- DO: If Yes , you might need to use a wake lock . However, you
should still check to see if you're already using an API or doing an
action that declares a wake lock on your behalf, as discussed in
 Actions that keep the device awake .
- DON'T: If you're playing audio, the audio system sets and manages a wake lock for
you; you don't need to do it yourself.
- DO: When the code creates the wake lock object, it uses the class's name as part
of the wake lock tag. We recommend including your package, class, or method
name as part of the wake lock tag. That way, if an error occurs, it's easier
to locate the wake lock in your source code. For more information, see
- DON'T: It's best to acquire the wake lock with
 WakeLock.acquire(long timeout) , which
automatically releases the wake lock after the specified timeout period.
However, you should still release the wake lock explicitly when you no
longer need it, so you don't hold the wake lock for longer than necessary.
- DON'T: Don't get the class or method name programmatically, for example by
calling getName() . If you try to get the name programmatically, it
might get obfuscated by tools like Proguard. Instead use a hard-coded
string.
- DON'T: Don't add a counter or unique identifiers to wake lock tags. The code
that creates a wake lock should use the same tag every time it runs.
This practice enables the system to aggregate each method's wake lock
usage.
- DON'T: Avoid doing lengthy work in the onReceive() method and
schedule workers if additional processing is required after the alarm.
- DON'T: AudioUnknown : Used when the other situations don't apply.
- DON'T: Don't declare wake lock names that begin with Audio .
- DO: Use Companion Device pairing to pair Bluetooth devices to
avoid acquiring a manual wake lock during Bluetooth pairing.
- DON'T: If your app requires both location and sensor data, synchronize their event
retrieval and processing. By coalescing sensor readings onto the brief
wake lock the system holds for location updates, you avoid needing a wake
lock to keep the CPU awake. Use a worker or a short-duration wake lock to
handl
- DON'T: Don't use high-priority FCM unless the message actually
needs to be delivered immediately.
- DON'T: Don't acquire a manual wake lock for user initiated download/ upload use
cases. Instead, use the User-Initiated Data Transfer (UIDT) API.
This is the designated path for long running data transfer tasks initiated
by the user.
- DON'T: Avoid acquiring a separate, continuous wake lock for caching location data,
as this is redundant and should be removed.
When requesting location updates using the
 FusedLocationProvider or LocationManager APIs, the system automatically
triggers a device wake-up during the location event callback.
In
- DO: For example, if you're using ktor-network to listen for
data packets on a network socket, you should only acquire a wake lock when
packets have been delivered to the client.
- DON'T: Choose whether the broadcast receiver should be exported and visible to
other apps on the device. If this receiver is listening for broadcasts sent
from the system or from other apps—even other apps that you own—use the
 RECEIVER_EXPORTED flag. If instead this receiver is listening only for
broadcas
- DON'T: If many apps have registered to receive the same broadcast in their
manifest, it can cause the system to launch a lot of apps, causing a
substantial impact on both device performance and user experience. To avoid
this, prefer using context registration over manifest declaration. Sometimes,
the Andro
- DON'T: Don't broadcast sensitive information using an implicit intent. Any app can
read the information if it registers to receive the broadcast.
There are three ways to control who can receive your broadcasts: 

 
 You can specify a permission when sending a broadcast.
- DON'T: Because a receiver's onReceive(Context, Intent) method runs on the
main thread, it should execute
and return quickly. If you need to perform long-running work, be careful
about spawning threads or starting background services because the system
can kill the entire process after onReceive() returns.
- DON'T: Don't start activities from broadcast receivers because the user experience
is jarring; especially if there is more than one receiver. Instead, consider
displaying a notification .
- DON'T: The first parameter of bindService() is an
 Intent that explicitly names the service to bind.
 Caution: If you use an intent to bind to a
 Service , make sure your app is secure by using an explicit 
intent. Using an implicit intent to start a service is a
security hazard because you can't be certai
- DO: Always trap DeadObjectException exceptions, which are thrown
when the connection has broken. This is the only exception thrown by remote methods.
- DON'T: Calls made from the local process execute in the same thread that is making the call. If
this is your main UI thread, that thread continues to execute in the AIDL interface. If it is
another thread, that is the one that executes your code in the service. Thus, if only local
threads are accessing the
- DO: List 
 All elements in the List must be one of the supported data types in this
list or one of the other AIDL-generated interfaces or parcelables you declare. A
 List can optionally be used as a parameterized type class, such as
 List<String> .
The actual concrete class that the other side receives
- DO: Map 
 All elements in the Map must be one of the supported data types in this
list or one of the other AIDL-generated interfaces or parcelables you declare. Parameterized type maps,
such as those of the form
 Map<String,Integer> , aren't supported. The actual concrete class that the other side
recei
- DON'T: All non-primitive parameters require a directional tag indicating which way the data goes:
 in , out , or inout (see the example below).
 Primitives, String , IBinder , and AIDL-generated
 interfaces are in by default and can't be otherwise. 
 Caution: Limit the direction to what is truly
needed, be
  WHY: marshalling parameters is expensive
- DON'T: By default, IPC calls are synchronous. If you know that the service takes more than a few
milliseconds to complete a request, don't call it from the activity's main thread.
It might hang the application, resulting in Android displaying an "Application is Not Responding"
dialog. Call it from a separa
- DON'T: Finally, create an .aidl file that declares your parcelable class, as shown for the following
 Rect.aidl file.
 If you are using a custom build process, do not add the .aidl file to your
build. Similar to a header file in the C language, this .aidl file isn't compiled.
- DO: Call the methods that you defined on your interface. Always trap
 DeadObjectException exceptions, which are thrown when
 the connection breaks. Also, trap SecurityException exceptions, which are thrown when the two processes involved in the IPC method call have conflicting AIDL definitions.
- DO: Depending on what API level your app targets, you may be
 required to declare foreground services in the app
manifest. The requirements for specific API levels are described in
 Changes to foreground services . 

 If you try to create a foreground service and its type isn't declared
in the manifest,
- DO: The app has already declared in the manifest that it needs the CAMERA 
permission. However, the app also has to check at runtime to make sure the
user granted that permission. If the app does not actually have the correct
permissions, it should let the user know about the problem.
- DON'T: Have your service implement the new Service.onTimeout(int, int) method.
When your app receives the callback, make sure to call stopSelf() within a
few seconds. (If you don't stop the app right away, the system generates a
failure.)
- DON'T: Make sure your app's dataSync and mediaProcessing services don't run for
more than a total of
6 hours in any 24-hour period (unless the user interacts with the app,
resetting the timer).
- DO: Use this method to set exact alarms, unless your app's work is
time-critical for the user.
- DO: Apps should confirm that the permission has not been revoked
- DO: Reschedules any exact alarms that your app needs, based on its current state.
This logic should be similar to what your app does when it receives the
 ACTION_BOOT_COMPLETED 
broadcast.
- DON'T: Avoid using exact alarms if possible. However, for the rare app that has rigid
time requirements, you can set an exact alarm by calling
 setRepeating() .
- DO: Use the WorkManager API, which is built to perform
background work. You can indicate that the system should expedite your work so
that the work finishes as soon as possible. For more information, see
 Schedule tasks with WorkManager
  WHY: the work finishes as soon as possible
- DO: Do any local work when the alarm triggers. "Local work" means anything that
doesn't hit a server or require the data from the server.
- DON'T: Don't wake up the device unnecessarily (this behavior is determined by the
alarm type, as described in Choose an alarm type ).
- DON'T: Don't make your alarm's trigger time any more precise than it has to be. 

 Use
 setInexactRepeating() 
instead of
 setRepeating() .
When you use setInexactRepeating() ,
Android synchronizes repeating alarms from multiple apps and fires
them at the same time. This reduces the total number of times t
- DON'T: Don't make your alarm's trigger time any more precise than it has to be.
- DO: Use
 setInexactRepeating() 
instead of
 setRepeating() .
When you use setInexactRepeating() ,
Android synchronizes repeating alarms from multiple apps and fires
them at the same time. This reduces the total number of times the system must wake the
device, thus reducing drain on the battery. As of An
- DON'T: Avoid basing your alarm on clock time if possible. 

 Repeating alarms that are based on a precise trigger time don't scale well. Use
 ELAPSED_REALTIME if
you can. The different alarm
types are described in more detail in the following section.
- DON'T: Avoid basing your alarm on clock time if possible.

## Code Patterns
### Declaring a service in the manifest
```xml
<manifest ... >
  ...
  <application ... >
      <service android:name=".ExampleService" />
      ...
  </application>
</manifest>
```

### Extending the Service class
```kotlin
class HelloService : Service() {

    private var serviceLooper: Looper? = null
    private var serviceHandler: ServiceHandler? = null

    // Handler that receives messages from the thread
    private inner class ServiceHandler(looper: Looper) : Handler(looper) {

        override fun handleMessage(msg: Message) {
            // Normally we would do some work here, like download a file.
            // For our sample, we just sleep for 5 seconds.
            try {
                Thread.sleep(5000)
            } catch (e: InterruptedException) {
                // Restore interrupt status.
                Thread.currentThread().interrupt()
            }

            // Stop the service using the startId, so that we don't stop
            // the service in the middle of handling another job
            stopSelf(msg.arg1)
        }
    }

    override fun onCreate() {
        // Start up the thread running the service.  Note that we create a
        // separate thread because the service normally runs in the process's
        // main thread, which we don't want to block.  We also make it
        // background priority so CPU-intensive work will not disrupt our UI.
        HandlerThread("ServiceStartArguments", Process.THREAD_PRIORITY_BACKGROUND).apply {
            start()

            // Get the HandlerThread's Looper and use it for our Handler
            serviceLooper = looper
            serviceHandler = ServiceHandler(looper)
        }
    }

    override fun onStartCommand(intent: Intent, flags: Int, startId: Int): Int {
        Toast.makeText(this, "service starting", Toast.LENGTH_SHORT).show()

        // For each start request, send a message to start a job and deliver the
        // start ID so we know which request we're stopping when we finish the job
        serviceHandler?.obtainMessage()?.also { msg ->
            msg.arg1 = startId
            serviceHandler?.sendMessage(msg)
        }

        // If we get killed, after returning from here, restart
        return START_STICKY
    }

    override fun onBind(intent: Intent): IBinder? {
        // We don't provide binding, so return null
        return null
    }

    override fun onDestroy() {
        Toast.makeText(this, "service done", Toast.LENGTH_SHORT).show()
    }
}
```

### Starting a service
```
startService(Intent(this, HelloService::class.java))
```

### Implementing the lifecycle callbacks
```kotlin
class ExampleService : Service() {
    private var startMode: Int = 0             // indicates how to behave if the service is killed
    private var binder: IBinder? = null        // interface for clients that bind
    private var allowRebind: Boolean = false   // indicates whether onRebind should be used

    override fun onCreate() {
        // The service is being created
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        // The service is starting, due to a call to startService()
        return startMode
    }

    override fun onBind(intent: Intent): IBinder? {
        // A client is binding to the service with bindService()
        return binder
    }

    override fun onUnbind(intent: Intent): Boolean {
        // All clients have unbound with unbindService()
        return allowRebind
    }

    override fun onRebind(intent: Intent) {
        // A client is binding to the service with bindService(),
        // after onUnbind() has already been called
    }

    override fun onDestroy() {
        // The service is no longer used and is being destroyed
    }
}
```

### Schedule work on unmetered connections
```kotlin
fun scheduleWork(context: Context) {
    val workManager = WorkManager.getInstance(context)
    val workRequest = OneTimeWorkRequestBuilder<MyWorker>()
       .setConstraints(
           Constraints.Builder()
               .setRequiredNetworkType(NetworkType.UNMETERED)
               .build()
           )
       .build()

    workManager.enqueue(workRequest)
}
```

### Determine which content authorities triggered work
```kotlin
class MyWorker(
    appContext: Context,
    params: WorkerParameters
): CoroutineWorker(appContext, params)
    override suspend fun doWork(): Result {
        StringBuilder().apply {
            append("Media content has changed:\n")
            params.triggeredContentAuthorities
                .takeIf { it.isNotEmpty() }
                ?.let { authorities ->
                    append("Authorities: ${authorities.joinToString(", ")}\n")
                    append(params.triggeredContentUris.joinToString("\n"))
                } ?: append("(No content)")
            Log.i(TAG, toString())
        }
        return Result.success()
    }
}
```

### Identify use-case specific APIs
```
I want to transfer data from an Android mobile device to [device_type]. Is there a specific API available?
```

### Schedule user-initiated data transfer jobs
```xml
<service android:name="com.example.app.CustomTransferService"
        android:permission="android.permission.BIND_JOB_SERVICE"
        android:exported="false">
        ...
</service>
```

### Schedule user-initiated data transfer jobs
```
class CustomTransferService : JobService() {
  ...
}
```

### Schedule user-initiated data transfer jobs
```xml
<manifest ...>
    <uses-permission android:name="android.permission.RUN_USER_INITIATED_JOBS" />
    <application ...>
        ...
    </application>
</manifest>
```

### Schedule user-initiated data transfer jobs
```kotlin
val networkRequestBuilder = NetworkRequest.Builder()
        // Add or remove capabilities based on your requirements.
        // For example, this code specifies that the job won't run
        // unless there's a connection to the internet (not just a local
        // network), and the connection doesn't charge per-byte.
        .addCapability(NET_CAPABILITY_INTERNET)
        .addCapability(NET_CAPABILITY_NOT_METERED)
        .build()

val jobInfo = JobInfo.Builder(jobId,
              ComponentName(mContext, CustomTransferService::class.java))
        // ...
        .setUserInitiated(true)
        .setRequiredNetwork(networkRequestBuilder)
        // Provide your estimate of the network traffic here
        .setEstimatedNetworkBytes(1024 * 1024 * 1024, 1024 * 1024 * 1024)
        // ...
        .build()
```

### Schedule user-initiated data transfer jobs
```kotlin
class CustomTransferService: JobService() {
    private val scope = CoroutineScope(Dispatchers.IO)

    @RequiresApi(Build.VERSION_CODES.UPSIDE_DOWN_CAKE)
    override fun onStartJob(params: JobParameters): Boolean {
        val notification = Notification.Builder(applicationContext,
                              NOTIFICATION_CHANNEL_ID)
            .setContentTitle("My user-initiated data transfer job")
            .setSmallIcon(android.R.mipmap.myicon)
            .setContentText("Job is running")
            .build()

        setNotification(params, notification.id, notification,
                JobService.JOB_END_NOTIFICATION_POLICY_DETACH)
        // Execute the work associated with this job asynchronously.
        scope.launch {
            doDownload(params)
        }
        return true
    }

    private suspend fun doDownload(params: JobParameters) {
        // Run the relevant async download task, then call
        // jobFinished once the task is completed.
        jobFinished(params, false)
    }

    // Called when the system stops the job.
    override fun onStopJob(params: JobParameters?): Boolean {
        // Asynchronously record job-related data, such as the
        // stop reason.
        return true // or return false if job should end entirely
    }
}
```

### Backward compatibility
```kotlin
fun beginTask() {
    if (Build.VERSION.SDK_INT  Build.VERSION_CODES.UPSIDE_DOWN_CAKE) {
        scheduleDownloadFGSWorker(context)
    } else {
        scheduleDownloadUIDTJob(context)
    }
}

private fun scheduleDownloadUIDTJob(context: Context) {
    // build jobInfo
    val jobScheduler: JobScheduler =
        context.getSystemService(Context.JOB_SCHEDULER_SERVICE) as JobScheduler
    jobScheduler.schedule(jobInfo)
}

private fun scheduleDownloadFGSWorker(context: Context) {
    val myWorkRequest = OneTimeWorkRequest.from(DownloadWorker::class.java)
    WorkManager.getInstance(context).enqueue(myWorkRequest)
}
```

### Testing
```
adb shell cmd jobscheduler run -f APP_PACKAGE_NAME JOB_ID
```

### Testing
```
adb shell cmd jobscheduler timeout TEST_APP_PACKAGE TEST_JOB_ID
```

### Work chaining
```kotlin
val continuation = WorkManager.getInstance(context)
    .beginUniqueWork(
        Constants.IMAGE_MANIPULATION_WORK_NAME,
        ExistingWorkPolicy.REPLACE,
        OneTimeWorkRequest.from(CleanupWorker::class.java)
    ).then(OneTimeWorkRequest.from(WaterColorFilterWorker::class.java))
    .then(OneTimeWorkRequest.from(GrayScaleFilterWorker::class.java))
    .then(OneTimeWorkRequest.from(BlurEffectFilterWorker::class.java))
    .then(
        if (save) {
            workRequest<SaveImageToGalleryWorker>(tag = Constants.TAG_OUTPUT)
        } else /* upload */ {
            workRequest<UploadWorker>(tag = Constants.TAG_OUTPUT)
        }
    )
```

### Getting started with WorkManager 

 
 
 
 

 
 
 Stay organized with collections
```kotlin
dependencies {
    val work_version = "2.11.1"

    // (Java only)
    implementation("androidx.work:work-runtime:$work_version")

    // Kotlin + coroutines
    implementation("androidx.work:work-runtime-ktx:$work_version")

    // optional - RxJava2 support
    implementation("androidx.work:work-rxjava2:$work_version")

    // optional - GCMNetworkManager support
    implementation("androidx.work:work-gcm:$work_version")

    // optional - Test helpers
    androidTestImplementation("androidx.work:work-testing:$work_version")

    // optional - Multiprocess support
    implementation("androidx.work:work-multiprocess:$work_version")
}
```

### Define the work
```kotlin
class UploadWorker(appContext: Context, workerParams: WorkerParameters):
       Worker(appContext, workerParams) {
   override fun doWork(): Result {

       // Do the work here--in this case, upload the images.
       uploadImages()

       // Indicate whether the work finished successfully with the Result
       return Result.success()
   }
}
```

### Create a WorkRequest
```kotlin
val uploadWorkRequest: WorkRequest =
   OneTimeWorkRequestBuilder<UploadWorker>()
       .build()
```

### Submit the WorkRequest to the system
```
WorkManager
    .getInstance(myContext)
    .enqueue(uploadWorkRequest)
```

### Overview
```kotlin
val myWorkRequest = ...
WorkManager.getInstance(myContext).enqueue(myWorkRequest)
```

### Schedule one-time work
```kotlin
val myWorkRequest = OneTimeWorkRequest.from(MyWork::class.java)
```

### Execute expedited work
```kotlin
val request = OneTimeWorkRequestBuilder<SyncWorker>()
    <b>.setExpedited(OutOfQuotaPolicy.RUN_AS_NON_EXPEDITED_WORK_REQUEST)</b>
    .build()

WorkManager.getInstance(context)
    .enqueue(request)
```

### CoroutineWorker
```kotlin
class ExpeditedWorker(appContext: Context, workerParams: WorkerParameters):
   CoroutineWorker(appContext, workerParams) {

   override suspend fun getForegroundInfo(): ForegroundInfo {
       return ForegroundInfo(
           NOTIFICATION_ID, createNotification()
       )
   }

   override suspend fun doWork(): Result {
       TODO()
   }

    private fun createNotification() : Notification {
       TODO()
    }

}
```

### Schedule periodic work
```kotlin
val saveRequest =
       PeriodicWorkRequestBuilder<SaveImageToFileWorker>(1, TimeUnit.HOURS)
    // Additional configuration
           .build()
```

### Flexible run intervals
```kotlin
val myUploadWork = PeriodicWorkRequestBuilder<SaveImageToFileWorker>(
       1, TimeUnit.HOURS, // repeatInterval (the period cycle)
       15, TimeUnit.MINUTES) // flexInterval
    .build()
```

### Work constraints
```kotlin
val constraints = Constraints.Builder()
   .setRequiredNetworkType(NetworkType.UNMETERED)
   .setRequiresCharging(true)
   .build()

val myWorkRequest: WorkRequest =
   OneTimeWorkRequestBuilder<MyWork>()
       .setConstraints(constraints)
       .build()
```

### Delayed Work
```kotlin
val myWorkRequest = OneTimeWorkRequestBuilder<MyWork>()
   .setInitialDelay(10, TimeUnit.MINUTES)
   .build()
```

### Assign input data
```kotlin
// Define the Worker requiring input
class UploadWork(appContext: Context, workerParams: WorkerParameters)
   : Worker(appContext, workerParams) {

   override fun doWork(): Result {
       val imageUriInput =
           inputData.getString("IMAGE_URI") ?: return Result.failure()

       uploadFile(imageUriInput)
       return Result.success()
   }
   ...
}

// Create a WorkRequest for your Worker and sending it input
val myUploadWork = OneTimeWorkRequestBuilder<UploadWork>()
   .setInputData(workDataOf(
       "IMAGE_URI" to "http://..."
   ))
   .build()
```

### Managing work 

 
 
 
 

 
 
 Stay organized with collections
 
 
 
 Save and ca
```kotlin
val myWork: WorkRequest = // ... OneTime or PeriodicWork
WorkManager.getInstance(requireContext()).enqueue(myWork)
```

### Unique Work
```kotlin
val sendLogsWorkRequest =
       PeriodicWorkRequestBuilder<SendLogsWorker>(24, TimeUnit.HOURS)
           .setConstraints(Constraints.Builder()
               .setRequiresCharging(true)
               .build()
            )
           .build()
WorkManager.getInstance(this).enqueueUniquePeriodicWork(
           "sendLogs",
           ExistingPeriodicWorkPolicy.KEEP,
           sendLogsWorkRequest
)
```

### Observing your work
```
// by id
workManager.getWorkInfoById(syncWorker.id) // ListenableFuture<WorkInfo>

// by name
workManager.getWorkInfosForUniqueWork("sync") // ListenableFuture<List<WorkInfo>>

// by tag
workManager.getWorkInfosByTag("syncTag") // ListenableFuture<List<WorkInfo>>
```

### Observing your work
```kotlin
workManager.getWorkInfoByIdFlow(syncWorker.id)
          .collect{ workInfo ->
              if(workInfo?.state == WorkInfo.State.SUCCEEDED) {
                  Snackbar.make(requireView(),
                      R.string.work_completed, Snackbar.LENGTH_SHORT)
                      .show()
              }
          }
```

### Complex work queries
```kotlin
val workQuery = WorkQuery.Builder
       .fromTags(listOf("syncTag"))
       .addStates(listOf(WorkInfo.State.FAILED, WorkInfo.State.CANCELLED))
       .addUniqueWorkNames(listOf("preProcess", "sync")
    )
   .build()

val workInfos: ListenableFuture<List<WorkInfo>> = workManager.getWorkInfos(workQuery)
```

### Cancelling and stopping work
```
// by id
workManager.cancelWorkById(syncWorker.id)

// by name
workManager.cancelUniqueWork("sync")

// by tag
workManager.cancelAllWorkByTag("syncTag")
```

### Chaining work 

 
 
 
 

 
 
 Stay organized with collections
 
 
 
 Save and ca
```
WorkManager.getInstance(myContext)
   // Candidates to run in parallel
   .beginWith(listOf(plantName1, plantName2, plantName3))
   // Dependent work (only runs after all previous work in chain)
   .then(cache)
   .then(upload)
   // Call enqueue to kick things off
   .enqueue()
```

### ArrayCreatingInputMerger
```kotlin
val cache: OneTimeWorkRequest = OneTimeWorkRequestBuilder<PlantWorker>()
   .setInputMerger(ArrayCreatingInputMerger::class)
   .setConstraints(constraints)
   .build()
```

### Creating and managing long-running workers
```kotlin
class DownloadWorker(context: Context, parameters: WorkerParameters) :
   CoroutineWorker(context, parameters) {

   private val notificationManager =
       context.getSystemService(Context.NOTIFICATION_SERVICE) as
               NotificationManager

   override suspend fun doWork(): Result {
       val inputUrl = inputData.getString(KEY_INPUT_URL)
                      ?: return Result.failure()
       val outputFile = inputData.getString(KEY_OUTPUT_FILE_NAME)
                      ?: return Result.failure()
       // Mark the Worker as important
       val progress = "Starting Download"
       setForeground(createForegroundInfo(progress))
       download(inputUrl, outputFile)
       return Result.success()
   }

   private fun download(inputUrl: String, outputFile: String) {
       // Downloads a file and updates bytes read
       // Calls setForeground() periodically when it needs to update
       // the ongoing Notification
   }
   // Creates an instance of ForegroundInfo which can be used to update the
   // ongoing notification.
   private fun createForegroundInfo(progress: String): ForegroundInfo {
       val id = applicationContext.getString(R.string.notification_channel_id)
       val title = applicationContext.getString(R.string.notification_title)
       val cancel = applicationContext.getString(R.string.cancel_download)
       // This PendingIntent can be used to cancel the worker
       val intent = WorkManager.getInstance(applicationContext)
               .createCancelPendingIntent(getId())

       // Create a Notification channel if necessary
       if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
           createChannel()
       }

       val notification = NotificationCompat.Builder(applicationContext, id)
           .setContentTitle(title)
           .setTicker(title)
           .setContentText(progress)
           .setSmallIcon(R.drawable.ic_work_notification)
           .setOngoing(true)
           // Add the cancel action to the notification which can
           // be used to cancel the worker
           .addAction(android.R.drawable.ic_delete, cancel, intent)
           .build()

       return ForegroundInfo(notificationId, notification)
   }

   @RequiresApi(Build.VERSION_CODES.O)
   private fun createChannel() {
       // Create a Notification channel
   }

   companion object {
       const val KEY_INPUT_URL = "KEY_INPUT_URL"
       const val KEY_OUTPUT_FILE_NAME = "KEY_OUTPUT_FILE_NAME"
   }
}
```

### Declare foreground service types in app manifest
```xml
<service
   android:name="androidx.work.impl.foreground.SystemForegroundService"
   android:foregroundServiceType="location|microphone"
   tools:node="merge" />
```

### Specify foreground service types at runtime
```kotlin
private fun createForegroundInfo(progress: String): ForegroundInfo {
   // ...
   return ForegroundInfo(NOTIFICATION_ID, notification,
           FOREGROUND_SERVICE_TYPE_LOCATION or
FOREGROUND_SERVICE_TYPE_MICROPHONE) }
```

### Update progress
```kotlin
import android.content.Context
import androidx.work.CoroutineWorker
import androidx.work.Data
import androidx.work.WorkerParameters
import kotlinx.coroutines.delay

class ProgressWorker(context: Context, parameters: WorkerParameters) :
    CoroutineWorker(context, parameters) {

    companion object {
        const val Progress = "Progress"
        private const val delayDuration = 1L
    }

    override suspend fun doWork(): Result {
        val firstUpdate = workDataOf(Progress to 0)
        val lastUpdate = workDataOf(Progress to 100)
        setProgress(firstUpdate)
        delay(delayDuration)
        setProgress(lastUpdate)
        return Result.success()
    }
}
```

### Update progress
```kotlin
import android.content.Context;
import androidx.annotation.NonNull;
import androidx.work.Data;
import androidx.work.Worker;
import androidx.work.WorkerParameters;

public class ProgressWorker extends Worker {

    private static final String PROGRESS = "PROGRESS";
    private static final long DELAY = 1000L;

    public ProgressWorker(
        @NonNull Context context,
        @NonNull WorkerParameters parameters) {
        super(context, parameters);
        // Set initial progress to 0
        setProgressAsync(new Data.Builder().putInt(PROGRESS, 0).build());
    }

    @NonNull
    @Override
    public Result doWork() {
        try {
            // Doing work.
            Thread.sleep(DELAY);
        } catch (InterruptedException exception) {
            // ... handle exception
        }
        // Set progress to 100 after you are done doing your work.
        setProgressAsync(new Data.Builder().putInt(PROGRESS, 100).build());
        return Result.success();
    }
}
```

### Observe progress
```kotlin
WorkManager.getInstance(applicationContext)
      // requestId is the WorkRequest id
      .getWorkInfoByIdFlow(requestId)
      .collect { workInfo: WorkInfo? ->
          if (workInfo != null) {
              val progress = workInfo.progress
              val value = progress.getInt("Progress", 0)
              // Do something with progress information
          }
      }
```

### Observe stop reason state
```kotlin
workManager.getWorkInfoByIdFlow(syncWorker.id)
  .collect { workInfo ->
      if (workInfo != null) {
        val stopReason = workInfo.stopReason
        logStopReason(syncWorker.id, stopReason)
      }
  }
```

### Update work example
```kotlin
suspend fun updatePhotoUploadWork() {
    // Get instance of WorkManager.
    val workManager = WorkManager.getInstance(context)

    // Retrieve the work request ID. In this example, the work being updated is unique
    // work so we can retrieve the ID using the unique work name.
    val photoUploadWorkInfoList = workManager.getWorkInfosForUniqueWork(
        PHOTO_UPLOAD_WORK_NAME
    ).await()

    val existingWorkRequestId = photoUploadWorkInfoList.firstOrNull()?.id ?: return

    // Update the constraints of the WorkRequest to not require a charging device.
    val newConstraints = Constraints.Builder()
        // Add other constraints as required here.
        .setRequiresCharging(false)
        .build()

    // Create new WorkRequest from existing Worker, new constraints, and the id of the old WorkRequest.
    val updatedWorkRequest: WorkRequest =
        OneTimeWorkRequestBuilder<MyWorker>()
            .setConstraints(newConstraints)
            .setId(existingWorkRequestId)
            .build()

    // Pass the new WorkRequest to updateWork().
    workManager.updateWork(updatedWorkRequest)
}
```

### Track generation example
```kotlin
// Get instance of WorkManager.
val workManager = WorkManager.getInstance(context)

// Retrieve WorkInfo instance.
val workInfo = workManager.getWorkInfoById(oldWorkRequestId)

// Call getGeneration to retrieve the generation.
val generation = workInfo.getGeneration()
```

### Threading in Worker 

 
 
 
 

 
 
 Stay organized with collections
 
 
 
 Save 
```
WorkManager.initialize(
    context,
    Configuration.Builder()
         // Uses a fixed thread pool of size 8 threads.
        .setExecutor(Executors.newFixedThreadPool(8))
        .build())
```

### Threading in Worker 

 
 
 
 

 
 
 Stay organized with collections
 
 
 
 Save 
```kotlin
class DownloadWorker(context: Context, params: WorkerParameters) : Worker(context, params) {

    override fun doWork(): ListenableWorker.Result {
        repeat(100) {
            try {
                downloadSynchronously("https://www.google.com")
            } catch (e: IOException) {
                return ListenableWorker.Result.failure()
            }
        }

        return ListenableWorker.Result.success()
    }
}
```

### Threading in CoroutineWorker 

 
 
 
 

 
 
 Stay organized with collections
 
 
```kotlin
class CoroutineDownloadWorker(
    context: Context,
    params: WorkerParameters
) : CoroutineWorker(context, params) {

    override suspend fun doWork(): Result {
        val data = downloadSynchronously("https://www.google.com")
        saveData(data)
        return Result.success()
    }
}
```

### Running a CoroutineWorker in a different process
```kotlin
val PACKAGE_NAME = "com.example.background.multiprocess"

val serviceName = RemoteWorkerService::class.java.name
val componentName = ComponentName(PACKAGE_NAME, serviceName)

val data: Data = Data.Builder()
   .putString(ARGUMENT_PACKAGE_NAME, componentName.packageName)
   .putString(ARGUMENT_CLASS_NAME, componentName.className)
   .build()

return OneTimeWorkRequest.Builder(ExampleRemoteCoroutineWorker::class.java)
   .setInputData(data)
   .build()
```

### Running a CoroutineWorker in a different process
```xml
<manifest ... >
    <service
            android:name="androidx.work.multiprocess.RemoteWorkerService"
            android:exported="false"
            android:process=":worker1" />

        <service
            android:name=".RemoteWorkerService2"
            android:exported="false"
            android:process=":worker2" />
    ...
</manifest>
```

### Threading in RxWorker 

 
 
 
 

 
 
 Stay organized with collections
 
 
 
 Sav
```kotlin
class RxDownloadWorker(
        context: Context,
        params: WorkerParameters
) : RxWorker(context, params) {
    override fun createWork(): Single<Result> {
        return Observable.range(0, 100)
                .flatMap { download("https://www.example.com") }
                .toList()
                .map { Result.success() }
    }
}
```

### Threading in ListenableWorker 

 
 
 
 

 
 
 Stay organized with collections
 

```kotlin
class CallbackWorker(
        context: Context,
        params: WorkerParameters
) : ListenableWorker(context, params) {
    override fun startWork(): ListenableFuture<Result> {
        return CallbackToFutureAdapter.getFuture { completer ->
            val callback = object : Callback {
                var successes = 0

                override fun onFailure(call: Call, e: IOException) {
                    completer.setException(e)
                }

                override fun onResponse(call: Call, response: Response) {
                    successes++
                    if (successes == 100) {
                        completer.set(Result.success())
                    }
                }
            }

            repeat(100) {
                downloadAsynchronously("https://example.com", callback)
            }

            callback
        }
    }
}
```

### Remove the default initializer
```xml
<!-- If you want to disable android.startup completely. -->
 <provider
    android:name="androidx.startup.InitializationProvider"
    android:authorities="${applicationId}.androidx-startup"
    tools:node="remove">
 </provider>
```

### Remove the default initializer
```xml
<provider
    android:name="androidx.startup.InitializationProvider"
    android:authorities="${applicationId}.androidx-startup"
    android:exported="false"
    tools:node="merge">
    <!-- If you are using androidx.startup to initialize other components -->
    <meta-data
        android:name="androidx.work.WorkManagerInitializer"
        android:value="androidx.startup"
        tools:node="remove" />
 </provider>
```

### Remove the default initializer
```xml
<provider
    android:name="androidx.work.impl.WorkManagerInitializer"
    android:authorities="${applicationId}.workmanager-init"
    tools:node="remove" />
```

### Implement Configuration.Provider
```kotlin
class MyApplication() : Application(), Configuration.Provider {
     override fun getWorkManagerConfiguration() =
           Configuration.Builder()
                .setMinimumLoggingLevel(android.util.Log.INFO)
                .build()
}
```

### Custom initialization
```kotlin
// provide custom configuration
val myConfig = Configuration.Builder()
    .setMinimumLoggingLevel(android.util.Log.INFO)
    .build()

// initialize WorkManager
WorkManager.initialize(this, myConfig)
```

### Use adb shell dumpsys jobscheduler
```
adb shell dumpsys jobscheduler
```

### Use adb shell dumpsys jobscheduler
```
JOB #u0a172/4: 6412553 com.google.android.youtube/androidx.work.impl.background.systemjob.SystemJobService
  u0a172 tag=*job*/com.google.android.youtube/androidx.work.impl.background.systemjob.SystemJobService
  Source: uid=u0a172 user=0 pkg=com.google.android.youtube
  JobInfo:
    Service: com.google.android.youtube/androidx.work.impl.background.systemjob.SystemJobService
    Requires: charging=false batteryNotLow=false deviceIdle=false
    Extras: mParcelledData.dataSize=180
    Network type: NetworkRequest [ NONE id=0, [ Capabilities: NOT_METERED&INTERNET&NOT_RESTRICTED&TRUSTED&VALIDATED Uid: 10172] ]
    Minimum latency: +1h29m59s687ms
    Backoff: policy=1 initial=+30s0ms
    Has early constraint
  Required constraints: TIMING_DELAY CONNECTIVITY [0x90000000]
  Satisfied constraints: DEVICE_NOT_DOZING BACKGROUND_NOT_RESTRICTED WITHIN_QUOTA [0x3400000]
  Unsatisfied constraints: TIMING_DELAY CONNECTIVITY [0x90000000]
  Tracking: CONNECTIVITY TIME QUOTA
  Implicit constraints:
    readyNotDozing: true
    readyNotRestrictedInBg: true
  Standby bucket: RARE
  Base heartbeat: 0
  Enqueue time: -51m29s853ms
  Run time: earliest=+38m29s834ms, latest=none, original latest=none
  Last run heartbeat: 0
  Ready: false (job=false user=true !pending=true !active=true !backingup=true comp=true)
```

### Use adb shell dumpsys jobscheduler
```
Job history:
     -1h35m26s440ms   START: #u0a107/9008 com.google.android.youtube/androidx.work.impl.background.systemjob.SystemJobService
     -1h35m26s362ms  STOP-P: #u0a107/9008 com.google.android.youtube/androidx.work.impl.background.systemjob.SystemJobService app called jobFinished
```

### Request diagnostic information from WorkManager 2.4.0+
```
adb shell am broadcast -a "androidx.work.diagnostics.REQUEST_DIAGNOSTICS" -p "<your_app_package_name>"
```

### Setup
```kotlin
dependencies {
    val work_version = "2.4.0"

    ...

    // optional - Test helpers
    androidTestImplementation("androidx.work:work-testing:$work_version")
}
```

### Concepts
```kotlin
@RunWith(AndroidJUnit4::class)
class BasicInstrumentationTest {
    @Before
    fun setup() {
        val context = InstrumentationRegistry.getTargetContext()
        val config = Configuration.Builder()
            .setMinimumLoggingLevel(Log.DEBUG)
            .setExecutor(SynchronousExecutor())
            .build()

        // Initialize WorkManager for instrumentation tests.
        WorkManagerTestInitHelper.initializeTestWorkManager(context, config)
    }
}
```

### Structuring Tests
```kotlin
class EchoWorker(context: Context, parameters: WorkerParameters)
   : Worker(context, parameters) {
   override fun doWork(): Result {
       return when(inputData.size()) {
           0 -> Result.failure()
           else -> Result.success(inputData)
       }
   }
}
```

### Basic Tests
```kotlin
@Test
@Throws(Exception::class)
fun testSimpleEchoWorker() {
    // Define input data
    val input = workDataOf(KEY_1 to 1, KEY_2 to 2)

    // Create request
    val request = OneTimeWorkRequestBuilder<EchoWorker>()
        .setInputData(input)
        .build()

    val workManager = WorkManager.getInstance(applicationContext)
    // Enqueue and wait for result. This also runs the Worker synchronously
    // because we are using a SynchronousExecutor.
    workManager.enqueue(request).result.get()
    // Get WorkInfo and outputData
    val workInfo = workManager.getWorkInfoById(request.id).get()
    val outputData = workInfo.outputData

    // Assert
    assertThat(workInfo.state, `is`(WorkInfo.State.SUCCEEDED))
    assertThat(outputData, `is`(input))
}
```

### Basic Tests
```kotlin
@Test
@Throws(Exception::class)
fun testEchoWorkerNoInput() {
   // Create request
   val request = OneTimeWorkRequestBuilder<EchoWorker>()
       .build()

   val workManager = WorkManager.getInstance(applicationContext)
   // Enqueue and wait for result. This also runs the Worker synchronously
   // because we are using a SynchronousExecutor.
   workManager.enqueue(request).result.get()
   // Get WorkInfo
   val workInfo = workManager.getWorkInfoById(request.id).get()

   // Assert
   assertThat(workInfo.state, `is`(WorkInfo.State.FAILED))
}
```

### Test Initial Delays
```kotlin
@Test
@Throws(Exception::class)
fun testWithInitialDelay() {
    // Define input data
    val input = workDataOf(KEY_1 to 1, KEY_2 to 2)

    // Create request
    val request = OneTimeWorkRequestBuilder<EchoWorker>()
        .setInputData(input)
        .setInitialDelay(10, TimeUnit.SECONDS)
        .build()

    val workManager = WorkManager.getInstance(getApplicationContext())
    // Get the TestDriver
    val testDriver = WorkManagerTestInitHelper.getTestDriver()
    // Enqueue
    workManager.enqueue(request).result.get()
    // Tells the WorkManager test framework that initial delays are now met.
    testDriver.setInitialDelayMet(request.id)
    // Get WorkInfo and outputData
    val workInfo = workManager.getWorkInfoById(request.id).get()
    val outputData = workInfo.outputData

    // Assert
    assertThat(workInfo.state, `is`(WorkInfo.State.SUCCEEDED))
    assertThat(outputData, `is`(input))
}
```

### Testing Constraints
```kotlin
@Test
@Throws(Exception::class)
fun testWithConstraints() {
    // Define input data
    val input = workDataOf(KEY_1 to 1, KEY_2 to 2)

    val constraints = Constraints.Builder()
        .setRequiredNetworkType(NetworkType.CONNECTED)
        .build()

    // Create request
    val request = OneTimeWorkRequestBuilder<EchoWorker>()
        .setInputData(input)
        .setConstraints(constraints)
        .build()

    val workManager = WorkManager.getInstance(myContext)
    val testDriver = WorkManagerTestInitHelper.getTestDriver()
    // Enqueue
    workManager.enqueue(request).result.get()
    // Tells the testing framework that all constraints are met.
    testDriver.setAllConstraintsMet(request.id)
    // Get WorkInfo and outputData
    val workInfo = workManager.getWorkInfoById(request.id).get()
    val outputData = workInfo.outputData

    // Assert
    assertThat(workInfo.state, `is`(WorkInfo.State.SUCCEEDED))
    assertThat(outputData, `is`(input))
}
```

### Testing Periodic Work
```kotlin
@Test
@Throws(Exception::class)
fun testPeriodicWork() {
    // Define input data
    val input = workDataOf(KEY_1 to 1, KEY_2 to 2)

    // Create request
    val request = PeriodicWorkRequestBuilder<EchoWorker>(15, MINUTES)
        .setInputData(input)
        .build()

    val workManager = WorkManager.getInstance(myContext)
    val testDriver = WorkManagerTestInitHelper.getTestDriver()
    // Enqueue and wait for result.
    workManager.enqueue(request).result.get()
    // Tells the testing framework the period delay is met
    testDriver.setPeriodDelayMet(request.id)
    // Get WorkInfo and outputData
    val workInfo = workManager.getWorkInfoById(request.id).get()

    // Assert
    assertThat(workInfo.state, `is`(WorkInfo.State.ENQUEUED))
}
```

### Testing Workers
```kotlin
class SleepWorker(context: Context, parameters: WorkerParameters) :
    Worker(context, parameters) {

    override fun doWork(): Result {
        // Sleep on a background thread.
        Thread.sleep(1000)
        return Result.success()
    }
}
```

### Testing Workers
```kotlin
// Kotlin code uses the TestWorkerBuilder extension to build
// the Worker
@RunWith(AndroidJUnit4::class)
class SleepWorkerTest {
    private lateinit var context: Context
    private lateinit var executor: Executor

    @Before
    fun setUp() {
        context = ApplicationProvider.getApplicationContext()
        executor = Executors.newSingleThreadExecutor()
    }

    @Test
    fun testSleepWorker() {
        val worker = TestWorkerBuilder<SleepWorker>(
            context = context,
            executor = executor
        ).build()

        val result = worker.doWork()
        assertThat(result, `is`(Result.success()))
    }
}
```

### Testing ListenableWorker and its variants
```kotlin
@RunWith(AndroidJUnit4::class)
class SleepWorkerTest {
    private lateinit var context: Context

    @Before
    fun setUp() {
        context = ApplicationProvider.getApplicationContext()
    }

    @Test
    fun testSleepWorker() {
        val worker = TestListenableWorkerBuilder<SleepWorker>(context).build()
        runBlocking {
            val result = worker.doWork()
            assertThat(result, `is`(Result.success()))
        }
    }
}
```

### Testing ListenableWorker and its variants
```kotlin
class SleepWorker(
    context: Context,
    parameters: WorkerParameters
) : RxWorker(context, parameters) {
    override fun createWork(): Single<Result> {
        return Single.just(Result.success())
            .delay(1000L, TimeUnit.MILLISECONDS)
    }
}
```

### From JobService to workers
```kotlin
import com.firebase.jobdispatcher.JobParameters
import com.firebase.jobdispatcher.JobService

class MyJobService : JobService() {
    override fun onStartJob(job: JobParameters): Boolean {
        // Do some work here
        return false // Answers the question: "Is there still work going on?"
    }
    override fun onStopJob(job: JobParameters): Boolean {
        return false // Answers the question: "Should this job be retried?"
    }
}
```

### From JobService to workers
```kotlin
import com.firebase.jobdispatcher.JobParameters;
import com.firebase.jobdispatcher.JobService;

public class MyJobService extends JobService {
    @Override
    public boolean onStartJob(JobParameters job) {
        // Do some work here

        return false; // Answers the question: "Is there still work going on?"
    }

    @Override
    public boolean onStopJob(JobParameters job) {
        return false; // Answers the question: "Should this job be retried?"
    }
}
```

### JobService maps to a ListenableWorker
```kotlin
import android.content.Context
import androidx.work.ListenableWorker
import androidx.work.ListenableWorker.Result
import androidx.work.WorkerParameters
import com.google.common.util.concurrent.ListenableFuture

class MyWorker(appContext: Context, params: WorkerParameters) :
    ListenableWorker(appContext, params) {

    override fun startWork(): ListenableFuture<ListenableWorker.Result> {
        // Do your work here.
        TODO("Return a ListenableFuture<Result>")
    }

    override fun onStopped() {
        // Cleanup because you are being stopped.
    }
}
```

### JobService maps to a ListenableWorker
```kotlin
import android.content.Context;
import androidx.work.ListenableWorker;
import androidx.work.ListenableWorker.Result;
import androidx.work.WorkerParameters;
import com.google.common.util.concurrent.ListenableFuture;

class MyWorker extends ListenableWorker {

  public MyWorker(@NonNull Context appContext, @NonNull WorkerParameters params) {
    super(appContext, params);
  }

  @Override
  public ListenableFuture<ListenableWorker.Result> startWork() {
    // Do your work here.
    Data input = getInputData();

    // Return a ListenableFuture<>
  }

  @Override
  public void onStopped() {
    // Cleanup because you are being stopped.
  }
}
```

### SimpleJobService maps to a Worker
```kotlin
import android.content.Context;
import androidx.work.Data;
import androidx.work.ListenableWorker.Result;
import androidx.work.Worker;
import androidx.work.WorkerParameters;


class MyWorker(context: Context, params: WorkerParameters) : Worker(context, params) {
    override fun doWork(): Result {
        TODO("Return a Result")
    }

    override fun onStopped() {
        super.onStopped()
        TODO("Cleanup, because you are being stopped")
    }
}
```

### JobBuilder maps to WorkRequest
```kotlin
val input: Bundle = Bundle().apply {
    putString("some_key", "some_value")
}

val job = dispatcher.newJobBuilder()
    // the JobService that will be called
    .setService(MyService::class.java)
    // uniquely identifies the job
    .setTag("my-unique-tag")
    // one-off job
    .setRecurring(false)
    // don't persist past a device reboot
    .setLifetime(Lifetime.UNTIL_NEXT_BOOT)
    // start between 0 and 60 seconds from now
    .setTrigger(Trigger.executionWindow(0, 60))
    // don't overwrite an existing job with the same tag
    .setReplaceCurrent(false)
    // retry with exponential backoff
    .setRetryStrategy(RetryStrategy.DEFAULT_EXPONENTIAL)

    .setConstraints(
        // only run on an unmetered network
        Constraint.ON_UNMETERED_NETWORK,
        // // only run when the device is charging
        Constraint.DEVICE_CHARGING
    )
    .setExtras(input)
    .build()

dispatcher.mustSchedule(job)
```

### Setting up inputs for the Worker
```kotlin
import androidx.work.workDataOf
val data = workDataOf("some_key" to "some_val")
```

### Setting up inputs for the Worker
```kotlin
import androidx.work.Data;
Data input = new Data.Builder()
    .putString("some_key", "some_value")
    .build();
```

### Setting up Constraints for the Worker
```kotlin
import androidx.work.*

val constraints: Constraints = Constraints.Builder().apply {
    setRequiredNetworkType(NetworkType.CONNECTED)
    setRequiresCharging(true)
}.build()
```

### Setting up Constraints for the Worker
```kotlin
import androidx.work.Constraints;
import androidx.work.Constraints.Builder;
import androidx.work.NetworkType;

Constraints constraints = new Constraints.Builder()
    // The Worker needs Network connectivity
    .setRequiredNetworkType(NetworkType.CONNECTED)
    // Needs the device to be charging
    .setRequiresCharging(true)
    .build();
```

### Creating the WorkRequest (OneTime or Periodic)
```kotlin
import androidx.work.*
import java.util.concurrent.TimeUnit

val constraints: Constraints = TODO("Define constraints as above")
val request: OneTimeWorkRequest =
     // Tell which work to execute
     OneTimeWorkRequestBuilder<MyWorker>()
         // Sets the input data for the ListenableWorker
        .setInputData(input)
        // If you want to delay the start of work by 60 seconds
        .setInitialDelay(60, TimeUnit.SECONDS)
        // Set a backoff criteria to be used when retry-ing
        .setBackoffCriteria(BackoffPolicy.EXPONENTIAL, 30000, TimeUnit.MILLISECONDS)
        // Set additional constraints
        .setConstraints(constraints)
        .build()
```

### Creating the WorkRequest (OneTime or Periodic)
```kotlin
import androidx.work.BackoffCriteria;
import androidx.work.Constraints;
import androidx.work.Constraints.Builder;
import androidx.work.NetworkType;
import androidx.work.OneTimeWorkRequest;
import androidx.work.OneTimeWorkRequest.Builder;
import androidx.work.Data;

// Define constraints (as above)
Constraints constraints = ...
OneTimeWorkRequest request =
    // Tell which work to execute
    new OneTimeWorkRequest.Builder(MyWorker.class)
        // Sets the input data for the ListenableWorker
        .setInputData(inputData)
        // If you want to delay the start of work by 60 seconds
        .setInitialDelay(60, TimeUnit.SECONDS)
        // Set a backoff criteria to be used when retry-ing
        .setBackoffCriteria(BackoffCriteria.EXPONENTIAL, 30000, TimeUnit.MILLISECONDS)
        // Set additional constraints
        .setConstraints(constraints)
        .build();
```

### Creating the WorkRequest (OneTime or Periodic)
```kotlin
val constraints: Constraints = TODO("Define constraints as above")
val request: PeriodicWorkRequest =
PeriodicWorkRequestBuilder<MyWorker>(15, TimeUnit.MINUTES)
    // Sets the input data for the ListenableWorker
    .setInputData(input)
    // Other setters
    .build()
```

### Scheduling work
```kotlin
val job = dispatcher.newJobBuilder()
    // the JobService that will be called
    .setService(MyService::class.java)
    // uniquely identifies the job
    .setTag("my-unique-tag")
    // don't overwrite an existing job with the same tag
    .setRecurring(false)
    // Other setters...
    .build()
```

### Scheduling work
```kotlin
import androidx.work.*

val request: OneTimeWorkRequest = TODO("A WorkRequest")
WorkManager.getInstance(myContext)
    .enqueueUniqueWork("my-unique-name", ExistingWorkPolicy.KEEP, request)
```

### Scheduling work
```kotlin
import androidx.work.ExistingWorkPolicy;
import androidx.work.OneTimeWorkRequest;
import androidx.work.WorkManager;

OneTimeWorkRequest workRequest = // a WorkRequest;
WorkManager.getInstance(myContext)
    // Use ExistingWorkPolicy.REPLACE to cancel and delete any existing pending
    // (uncompleted) work with the same unique name. Then, insert the newly-specified
    // work.
    .enqueueUniqueWork("my-unique-name", ExistingWorkPolicy.KEEP, workRequest);
```

### Cancelling work
```
dispatcher.cancel("my-unique-tag")
```

### Cancelling work
```kotlin
import androidx.work.WorkManager
WorkManager.getInstance(myContext).cancelUniqueWork("my-unique-name")
```

### Cancelling work
```kotlin
import androidx.work.WorkManager;
WorkManager.getInstance(myContext).cancelUniqueWork("my-unique-name");
```

### Migrate to WorkManager
```kotlin
val myTask = OneoffTask.Builder()
    // setService() says what class does the work
    .setService(MyUploadService::class.java)
    // Don't run the task unless device is charging
    .setRequiresCharging(true)
    // Run the task between 5 & 15 minutes from now
    .setExecutionWindow(5 * DateUtil.MINUTE_IN_SECONDS,
            15 * DateUtil.MINUTE_IN_SECONDS)
    // Define a unique tag for the task
    .setTag("test-upload")
    // ...finally, build the task and assign its value to myTask
    .build()
GcmNetworkManager.getInstance(this).schedule(myTask)
```

### Migrate to WorkManager
```kotlin
class MyUploadService : GcmTaskService() {
    fun onRunTask(params: TaskParams): Int {
        // Do some upload work
        return GcmNetworkManager.RESULT_SUCCESS
    }
}
```

### Define the Worker
```kotlin
class UploadWorker(context: Context, params: WorkerParameters)
                        : Worker(context, params) {
    override fun doWork() : Result {
        // Do the upload operation ...
        myUploadOperation()

        // Indicate whether the task finished successfully with the Result
        return Result.success()
    }
}
```

### Schedule the work request
```kotlin
val uploadConstraints = Constraints.Builder()
    .setRequiredNetworkType(NetworkType.CONNECTED)
    .setRequiresCharging(true).build()

val uploadTask = OneTimeWorkRequestBuilder&lt;UploadWorker>()
    .setConstraints(uploadConstraints)
    .build()
WorkManager.getInstance().enqueue(uploadTask)
```

### Manually keep the screen on
```kotlin
class MainActivity : Activity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
    }
}
```

### Manually keep the screen on
```xml
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:keepScreenOn="true">
    ...
</RelativeLayout>
```

### Dependencies
```xml
<uses-permission android:name="android.permission.WAKE_LOCK" />
```

### Create and acquire a wake lock
```kotlin
val wakeLock: PowerManager.WakeLock =
    (getSystemService(POWER_SERVICE) as PowerManager).run {
        newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "MyClassName::MyWakelockTag").apply {
            acquire(WAKELOCK_TIMEOUT)
        }
    }WakeLockSnippetsKotlin.kt
```

### Release an active wake lock
```kotlin
@Throws(MyException::class)
fun doSomethingAndRelease() {
    wakeLock.apply {
        try {
            acquire(WAKELOCK_TIMEOUT)
            doTheWork()
        } finally {
            release()
        }
    }
}WakeLockSnippetsKotlin.kt
```

### Android 15 and lower
```
*job*u/@<name_space>@/<package_name>/<classname>
```

### Android 15 and lower
```
*job*/@<name_space>@/<package_name>/<classname>
```

### Android 16 QPR2 and higher
```
*job*u/@<name_space>@/#<trace_tag>#/<package_name>/<classname>
```

### Android 16 QPR2 and higher
```
*job*e/@<name_space>@/#<trace_tag>#/<package_name>/<classname>
```

### Android 16 QPR2 and higher
```
*job*r/@<name_space>@/#<trace_tag>#/<package_name>/<classname>
```

### Example
```
*job*/@backup@/com.example.app/com.backup.BackupFileService
```

### Example
```
*job*e/@backup@/#started#/com.example.app/com.backup.BackupFileService
```

### Android 15 and lower
```
*job*/<package_name>/androidx.work.impl.background.systemjob.SystemJobService
```

### Android 16 QPR2 and higher
```
*job*e/#<trace_tag>#/<package_name>/androidx.work.impl.background.systemjob.SystemJobService
```

### Android 16 QPR2 and higher
```
*job*r/#<trace_tag>#/<package_name>/androidx.work.impl.background.systemjob.SystemJobService
```

### Example
```
*job*/com.example.app/androidx.work.impl.background.systemjob.SystemJobService
```

### Example
```
*job*e/#BackupFileWorker#/com.example.app/androidx.work.impl.background.systemjob.SystemJobService
```

### Required libraries
```kotlin
dependencies {
    implementation("com.google.guava:guava:31.0.1-android")

    // To use CallbackToFutureAdapter
    implementation("androidx.concurrent:concurrent-futures:1.3.0")

    // Kotlin
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-guava:1.6.0")
}
```

### Adding a callback
```kotlin
val future: ListenableFuture<QueryResult> = ...
Futures.addCallback(
    future,
    object : FutureCallback<QueryResult> {
        override fun onSuccess(result: QueryResult) {
            // handle success
        }

        override fun onFailure(t: Throwable) {
            // handle failure
        }
    },
    // causes the callbacks to be executed on the main (UI) thread
    context.mainExecutor
)
```

### Suspending in Kotlin
```kotlin
import kotlinx.coroutines.guava.await

...

val future: ListenableFuture<QueryResult> = ...
val queryResult = future.await() // suspends awaiting success
```

### Interop with RxJava
```kotlin
val future: ListenableFuture<QueryResult> = ...
val single = Single.create<QueryResult> {
    Futures.addCallback(future, object : FutureCallback<QueryResult> {
        override fun onSuccess(result: QueryResult) {
            it.onSuccess(result)
        }

        override fun onFailure(t: Throwable) {
            it.onError(t)
        }
    }, executor)
}
```

### Creating an immediate future
```kotlin
fun getResult(): ListenableFuture<QueryResult> {
    try {
        val queryResult = getQueryResult()
        return Futures.immediateFuture(queryResult)
    } catch (e: Exception) {
        return Futures.immediateFailedFuture(e)
    }
}
```

### Using a coroutine
```kotlin
import kotlinx.coroutines.guava.future

suspend fun getResultAsync(): QueryResult { ... }

fun getResultFuture(): ListenableFuture<QueryResult> {
    return coroutineScope.future{
        getResultAsync()
    }
}
```

### Converting from RxJava Single
```kotlin
fun getResult(): ListenableFuture<QueryResult> {
    val single: Single<QueryResult> = ...

    val future = SettableFuture.create<QueryResult>()
    single.subscribe(future::set, future::setException)
    return future
}
```

### Context-registered receivers
```kotlin
dependencies {
    val core_version = "1.18.0"

    // Java language implementation
    implementation("androidx.core:core:$core_version")
    // Kotlin
    implementation("androidx.core:core-ktx:$core_version")

    // To use RoleManagerCompat
    implementation("androidx.core:core-role:1.1.0")

    // To use the Animator APIs
    implementation("androidx.core:core-animation:1.0.0")
    // To test the Animator APIs
    androidTestImplementation("androidx.core:core-animation-testing:1.0.0")

    // Optional - To enable APIs that query the performance characteristics of GMS devices.
    implementation("androidx.core:core-performance:1.0.0")

    // Optional - to use ShortcutManagerCompat to donate shortcuts to be used by Google
    implementation("androidx.core:core-google-shortcuts:1.1.0")

    // Optional - to support backwards compatibility of RemoteViews
    implementation("androidx.core:core-remoteviews:1.1.0")

    // Optional - APIs for SplashScreen, including compatibility helpers on devices prior Android 12
    implementation("androidx.core:core-splashscreen:1.2.0")
}
```

### Context-registered receivers
```kotlin
val myBroadcastReceiver = MyBroadcastReceiver()
```

### Context-registered receivers
```kotlin
val filter = IntentFilter("com.example.snippets.ACTION_UPDATE_DATA")
```

### Context-registered receivers
```kotlin
val listenToBroadcastsFromOtherApps = false
val receiverFlags = if (listenToBroadcastsFromOtherApps) {
    ContextCompat.RECEIVER_EXPORTED
} else {
    ContextCompat.RECEIVER_NOT_EXPORTED
}BroadcastReceiverSnippets.kt
```

### Context-registered receivers
```
ContextCompat.registerReceiver(context, myBroadcastReceiver, filter, receiverFlags)
```

### Unregister your broadcast receiver
```kotlin
class MyActivity : ComponentActivity() {
    private val myBroadcastReceiver = MyBroadcastReceiver()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // ...
        ContextCompat.registerReceiver(this, myBroadcastReceiver, filter, receiverFlags)
        setContent { MyApp() }
    }

    override fun onDestroy() {
        super.onDestroy()
        // When you forget to unregister your receiver here, you're causing a leak!
        this.unregisterReceiver(myBroadcastReceiver)
    }
}BroadcastReceiverSnippets.kt
```

### Create stateful and stateless composable
```kotlin
@Composable
fun MyStatefulScreen() {
    val myBroadcastReceiver = remember { MyBroadcastReceiver() }
    val context = LocalContext.current
    LifecycleStartEffect(true) {
        // ...
        ContextCompat.registerReceiver(context, myBroadcastReceiver, filter, flags)
        onStopOrDispose { context.unregisterReceiver(myBroadcastReceiver) }
    }
    MyStatelessScreen()
}

@Composable
fun MyStatelessScreen() {
    // Implement your screen
}BroadcastReceiverSnippets.kt
```

### Manifest-declared receivers
```xml
<!-- If this receiver listens for broadcasts sent from the system or from
     other apps, even other apps that you own, set android:exported to "true". -->
<receiver android:name=".MyBroadcastReceiver" android:exported="false">
    <intent-filter>
        <action android:name="com.example.snippets.ACTION_UPDATE_DATA" />
    </intent-filter>
</receiver>AndroidManifest.xml
```

### Manifest-declared receivers
```kotlin
class MyBroadcastReceiver : BroadcastReceiver() {

    @Inject
    lateinit var dataRepository: DataRepository

    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action == "com.example.snippets.ACTION_UPDATE_DATA") {
            val data = intent.getStringExtra("com.example.snippets.DATA") ?: "No data"
            // Do something with the data, for example send it to a data repository:
            dataRepository.updateData(data)
        }
    }
}BroadcastReceiverSnippets.kt
```

### Manifest-declared receivers
```kotlin
public static class MyBroadcastReceiver extends BroadcastReceiver {

    @Inject
    DataRepository dataRepository;

    @Override
    public void onReceive(Context context, Intent intent) {
        if (Objects.equals(intent.getAction(), "com.example.snippets.ACTION_UPDATE_DATA")) {
            String data = intent.getStringExtra("com.example.snippets.DATA");
            // Do something with the data, for example send it to a data repository:
            if (data != null) { dataRepository.updateData(data); }
        }
    }
}BroadcastReceiverJavaSnippets.java
```

### Send broadcasts
```kotlin
val intent = Intent("com.example.snippets.ACTION_UPDATE_DATA").apply {
    putExtra("com.example.snippets.DATA", newData)
    setPackage("com.example.snippets")
}
context.sendBroadcast(intent)BroadcastReceiverSnippets.kt
```

### Send broadcasts
```
Intent intent = new Intent("com.example.snippets.ACTION_UPDATE_DATA");
intent.putExtra("com.example.snippets.DATA", newData);
intent.setPackage("com.example.snippets");
context.sendBroadcast(intent);BroadcastReceiverJavaSnippets.java
```

### Send broadcasts with permissions
```
context.sendBroadcast(intent, android.Manifest.permission.ACCESS_COARSE_LOCATION)
```

### Send broadcasts with permissions
```xml
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
```

### Receive broadcasts with permissions
```
ContextCompat.registerReceiver(
    context, myBroadcastReceiver, filter,
    android.Manifest.permission.ACCESS_COARSE_LOCATION,
    null, // scheduler that defines thread, null means run on main thread
    receiverFlags
)BroadcastReceiverSnippets.kt
```

### Extend the Binder class
```kotlin
class LocalService : Service() {
    // Binder given to clients.
    private val binder = LocalBinder()

    // Random number generator.
    private val mGenerator = Random()

    /** Method for clients.  */
    val randomNumber: Int
        get() = mGenerator.nextInt(100)

    /**
     * Class used for the client Binder. Because we know this service always
     * runs in the same process as its clients, we don't need to deal with IPC.
     */
    inner class LocalBinder : Binder() {
        // Return this instance of LocalService so clients can call public methods.
        fun getService(): LocalService = this@LocalService
    }

    override fun onBind(intent: Intent): IBinder {
        return binder
    }
}
```

### Extend the Binder class
```kotlin
class BindingActivity : Activity() {
    private lateinit var mService: LocalService
    private var mBound: Boolean = false

    /** Defines callbacks for service binding, passed to bindService().  */
    private val connection = object : ServiceConnection {

        override fun onServiceConnected(className: ComponentName, service: IBinder) {
            // We've bound to LocalService, cast the IBinder and get LocalService instance.
            val binder = service as LocalService.LocalBinder
            mService = binder.getService()
            mBound = true
        }

        override fun onServiceDisconnected(arg0: ComponentName) {
            mBound = false
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.main)
    }

    override fun onStart() {
        super.onStart()
        // Bind to LocalService.
        Intent(this, LocalService::class.java).also { intent ->
            bindService(intent, connection, Context.BIND_AUTO_CREATE)
        }
    }

    override fun onStop() {
        super.onStop()
        unbindService(connection)
        mBound = false
    }

    /** Called when a button is clicked (the button in the layout file attaches to
     * this method with the android:onClick attribute).  */
    fun onButtonClick(v: View) {
        if (mBound) {
            // Call a method from the LocalService.
            // However, if this call is something that might hang, then put this request
            // in a separate thread to avoid slowing down the activity performance.
            val num: Int = mService.randomNumber
            Toast.makeText(this, "number: $num", Toast.LENGTH_SHORT).show()
        }
    }
}
```

### Use a Messenger
```kotlin
/** Command to the service to display a message.  */
private const val MSG_SAY_HELLO = 1

class MessengerService : Service() {

    /**
     * Target we publish for clients to send messages to IncomingHandler.
     */
    private lateinit var mMessenger: Messenger

    /**
     * Handler of incoming messages from clients.
     */
    internal class IncomingHandler(
            context: Context,
            private val applicationContext: Context = context.applicationContext
    ) : Handler() {
        override fun handleMessage(msg: Message) {
            when (msg.what) {
                MSG_SAY_HELLO ->
                    Toast.makeText(applicationContext, "hello!", Toast.LENGTH_SHORT).show()
                else -> super.handleMessage(msg)
            }
        }
    }

    /**
     * When binding to the service, we return an interface to our messenger
     * for sending messages to the service.
     */
    override fun onBind(intent: Intent): IBinder? {
        Toast.makeText(applicationContext, "binding", Toast.LENGTH_SHORT).show()
        mMessenger = Messenger(IncomingHandler(this))
        return mMessenger.binder
    }
}
```

### Use a Messenger
```kotlin
class ActivityMessenger : Activity() {
    /** Messenger for communicating with the service.  */
    private var mService: Messenger? = null

    /** Flag indicating whether we have called bind on the service.  */
    private var bound: Boolean = false

    /**
     * Class for interacting with the main interface of the service.
     */
    private val mConnection = object : ServiceConnection {

        override fun onServiceConnected(className: ComponentName, service: IBinder) {
            // This is called when the connection with the service has been
            // established, giving us the object we can use to
            // interact with the service.  We are communicating with the
            // service using a Messenger, so here we get a client-side
            // representation of that from the raw IBinder object.
            mService = Messenger(service)
            bound = true
        }

        override fun onServiceDisconnected(className: ComponentName) {
            // This is called when the connection with the service has been
            // unexpectedly disconnected&mdash;that is, its process crashed.
            mService = null
            bound = false
        }
    }

    fun sayHello(v: View) {
        if (!bound) return
        // Create and send a message to the service, using a supported 'what' value.
        val msg: Message = Message.obtain(null, MSG_SAY_HELLO, 0, 0)
        try {
            mService?.send(msg)
        } catch (e: RemoteException) {
            e.printStackTrace()
        }

    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.main)
    }

    override fun onStart() {
        super.onStart()
        // Bind to the service.
        Intent(this, MessengerService::class.java).also { intent ->
            bindService(intent, mConnection, Context.BIND_AUTO_CREATE)
        }
    }

    override fun onStop() {
        super.onStop()
        // Unbind from the service.
        if (bound) {
            unbindService(mConnection)
            bound = false
        }
    }
}
```

### Bind to a service
```kotlin
var mService: LocalService

val mConnection = object : ServiceConnection {
    // Called when the connection with the service is established.
    override fun onServiceConnected(className: ComponentName, service: IBinder) {
        // Because we have bound to an explicit
        // service that is running in our own process, we can
        // cast its IBinder to a concrete class and directly access it.
        val binder = service as LocalService.LocalBinder
        mService = binder.getService()
        mBound = true
    }

    // Called when the connection with the service disconnects unexpectedly.
    override fun onServiceDisconnected(className: ComponentName) {
        Log.e(TAG, "onServiceDisconnected")
        mBound = false
    }
}
```

### Bind to a service
```
Intent(this, LocalService::class.java).also { intent ->
    bindService(intent, connection, Context.BIND_AUTO_CREATE)
}
```

### Create the .aidl file
```
// IRemoteService.aidl
package com.example.android;

// Declare any non-default types here with import statements.

/** Example service interface */
interface IRemoteService {
    /** Request the process ID of this service. */
    int getPid();

    /** Demonstrates some basic types that you can use as parameters
     * and return values in AIDL.
     */
    void basicTypes(int anInt, long aLong, boolean aBoolean, float aFloat,
            double aDouble, String aString);
}
```

### Implement the interface
```kotlin
private val binder = object : IRemoteService.Stub() {

    override fun getPid(): Int =
            Process.myPid()

    override fun basicTypes(
            anInt: Int,
            aLong: Long,
            aBoolean: Boolean,
            aFloat: Float,
            aDouble: Double,
            aString: String
    ) {
        // Does nothing.
    }
}
```

### Expose the interface to clients
```kotlin
class RemoteService : Service() {

    override fun onCreate() {
        super.onCreate()
    }

    override fun onBind(intent: Intent): IBinder {
        // Return the interface.
        return binder
    }


    private val binder = object : IRemoteService.Stub() {
        override fun getPid(): Int {
            return Process.myPid()
        }

        override fun basicTypes(
                anInt: Int,
                aLong: Long,
                aBoolean: Boolean,
                aFloat: Float,
                aDouble: Double,
                aString: String
        ) {
            // Does nothing.
        }
    }
}
```

### Expose the interface to clients
```kotlin
var iRemoteService: IRemoteService? = null

val mConnection = object : ServiceConnection {

    // Called when the connection with the service is established.
    override fun onServiceConnected(className: ComponentName, service: IBinder) {
        // Following the preceding example for an AIDL interface,
        // this gets an instance of the IRemoteInterface, which we can use to call on the service.
        iRemoteService = IRemoteService.Stub.asInterface(service)
    }

    // Called when the connection with the service disconnects unexpectedly.
    override fun onServiceDisconnected(className: ComponentName) {
        Log.e(TAG, "Service has unexpectedly disconnected")
        iRemoteService = null
    }
}
```

### Passing objects over IPC
```
package android.graphics;

// Declare Rect so AIDL can find it and knows that it implements
// the parcelable protocol.
parcelable Rect {
    int left;
    int top;
    int right;
    int bottom;
}
```

### Passing objects over IPC
```kotlin
import android.os.Parcel
import android.os.Parcelable

class Rect() : Parcelable {
    var left: Int = 0
    var top: Int = 0
    var right: Int = 0
    var bottom: Int = 0

    companion object CREATOR : Parcelable.Creator<Rect> {
        override fun createFromParcel(parcel: Parcel): Rect {
            return Rect(parcel)
        }

        override fun newArray(size: Int): Array<Rect?> {
            return Array(size) { null }
        }
    }

    private constructor(inParcel: Parcel) : this() {
        readFromParcel(inParcel)
    }

    override fun writeToParcel(outParcel: Parcel, flags: Int) {
        outParcel.writeInt(left)
        outParcel.writeInt(top)
        outParcel.writeInt(right)
        outParcel.writeInt(bottom)
    }

    private fun readFromParcel(inParcel: Parcel) {
        left = inParcel.readInt()
        top = inParcel.readInt()
        right = inParcel.readInt()
        bottom = inParcel.readInt()
    }

    override fun describeContents(): Int {
        return 0
    }
}
```

### Passing objects over IPC
```kotlin
import android.os.Parcel;
import android.os.Parcelable;

public final class Rect implements Parcelable {
    public int left;
    public int top;
    public int right;
    public int bottom;

    public static final Parcelable.Creator<Rect> CREATOR = new Parcelable.Creator<Rect>() {
        public Rect createFromParcel(Parcel in) {
            return new Rect(in);
        }

        public Rect[] newArray(int size) {
            return new Rect[size];
        }
    };

    public Rect() {
    }

    private Rect(Parcel in) {
        readFromParcel(in);
    }

    public void writeToParcel(Parcel out, int flags) {
        out.writeInt(left);
        out.writeInt(top);
        out.writeInt(right);
        out.writeInt(bottom);
    }

    public void readFromParcel(Parcel in) {
        left = in.readInt();
        top = in.readInt();
        right = in.readInt();
        bottom = in.readInt();
    }

    public int describeContents() {
        return 0;
    }
}
```

### Methods with Bundle arguments containing Parcelables
```
// IRectInsideBundle.aidl
package com.example.android;

/** Example service interface */
interface IRectInsideBundle {
    /** Rect parcelable is stored in the bundle with key "rect". */
    void saveRect(in Bundle bundle);
}
```

### Methods with Bundle arguments containing Parcelables
```kotlin
private val binder = object : IRectInsideBundle.Stub() {
    override fun saveRect(bundle: Bundle) {
      bundle.classLoader = classLoader
      val rect = bundle.getParcelable<Rect>("rect")
      process(rect) // Do more with the parcelable.
    }
}
```

### Calling an IPC method
```kotlin
private const val BUMP_MSG = 1

class Binding : Activity() {

    /** The primary interface you call on the service.  */
    private var mService: IRemoteService? = null

    /** Another interface you use on the service.  */
    internal var secondaryService: ISecondary? = null

    private lateinit var killButton: Button
    private lateinit var callbackText: TextView
    private lateinit var handler: InternalHandler

    private var isBound: Boolean = false

    /**
     * Class for interacting with the main interface of the service.
     */
    private val mConnection = object : ServiceConnection {

        override fun onServiceConnected(className: ComponentName, service: IBinder) {
            // This is called when the connection with the service is
            // established, giving us the service object we can use to
            // interact with the service.  We are communicating with our
            // service through an IDL interface, so get a client-side
            // representation of that from the raw service object.
            mService = IRemoteService.Stub.asInterface(service)
            killButton.isEnabled = true
            callbackText.text = "Attached."

            // We want to monitor the service for as long as we are
            // connected to it.
            try {
                mService?.registerCallback(mCallback)
            } catch (e: RemoteException) {
                // In this case, the service crashes before we can
                // do anything with it. We can count on soon being
                // disconnected (and then reconnected if it can be restarted)
                // so there is no need to do anything here.
            }

            // As part of the sample, tell the user what happened.
            Toast.makeText(
                    this@Binding,
                    R.string.remote_service_connected,
                    Toast.LENGTH_SHORT
            ).show()
        }

        override fun onServiceDisconnected(className: ComponentName) {
            // This is called when the connection with the service is
            // unexpectedly disconnected&mdash;that is, its process crashed.
            mService = null
            killButton.isEnabled = false
            callbackText.text = "Disconnected."

            // As part of the sample, tell the user what happened.
            Toast.makeText(
                    this@Binding,
                    R.string.remote_service_disconnected,
                    Toast.LENGTH_SHORT
            ).show()
        }
    }

    /**
     * Class for interacting with the secondary interface of the service.
     */
    private val secondaryConnection = object : ServiceConnection {

        override fun onServiceConnected(className: ComponentName, service: IBinder) {
            // Connecting to a secondary interface is the same as any
            // other interface.
            secondaryService = ISecondary.Stub.asInterface(service)
            killButton.isEnabled = true
        }

        override fun onServiceDisconnected(className: ComponentName) {
            secondaryService = null
            killButton.isEnabled = false
        }
    }

    private val mBindListener = View.OnClickListener {
        // Establish a couple connections with the service, binding
        // by interface names. This lets other applications be
        // installed that replace the remote service by implementing
        // the same interface.
        val intent = Intent(this@Binding, RemoteService::class.java)
        intent.action = IRemoteService::class.java.name
        bindService(intent, mConnection, Context.BIND_AUTO_CREATE)
        intent.action = ISecondary::class.java.name
        bindService(intent, secondaryConnection, Context.BIND_AUTO_CREATE)
        isBound = true
        callbackText.text = "Binding."
    }

    private val unbindListener = View.OnClickListener {
        if (isBound) {
            // If we have received the service, and hence registered with
            // it, then now is the time to unregister.
            try {
                mService?.unregisterCallback(mCallback)
            } catch (e: RemoteException) {
                // There is nothing special we need to do if the service
                // crashes.
            }

            // Detach our existing connection.
            unbindService(mConnection)
            unbindService(secondaryConnection)
            killButton.isEnabled = false
            isBound = false
            callbackText.text = "Unbinding."
        }
    }

    private val killListener = View.OnClickListener {
        // To kill the process hosting the service, we need to know its
        // PID.  Conveniently, the service has a call that returns
        // that information.
        try {
            secondaryService?.pid?.also { pid ->
                // Note that, though this API lets us request to
                // kill any process based on its PID, the kernel
                // still imposes standard restrictions on which PIDs you
                // can actually kill. Typically this means only
                // the process running your application and any additional
                // processes created by that app, as shown here. Packages
                // sharing a common UID are also able to kill each
                // other's processes.
                Process.killProcess(pid)
                callbackText.text = "Killed service process."
            }
        } catch (ex: RemoteException) {
            // Recover gracefully from the process hosting the
            // server dying.
            // For purposes of this sample, put up a notification.
            Toast.makeText(this@Binding, R.string.remote_call_failed, Toast.LENGTH_SHORT).show()
        }
    }

    // ----------------------------------------------------------------------
    // Code showing how to deal with callbacks.
    // ----------------------------------------------------------------------

    /**
     * This implementation is used to receive callbacks from the remote
     * service.
     */
    private val mCallback = object : IRemoteServiceCallback.Stub() {
        /**
         * This is called by the remote service regularly to tell us about
         * new values.  Note that IPC calls are dispatched through a thread
         * pool running in each process, so the code executing here is
         * NOT running in our main thread like most other things. So,
         * to update the UI, we need to use a Handler to hop over there.
         */
        override fun valueChanged(value: Int) {
            handler.sendMessage(handler.obtainMessage(BUMP_MSG, value, 0))
        }
    }

    /**
     * Standard initialization of this activity.  Set up the UI, then wait
     * for the user to interact with it before doing anything.
     */
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContentView(R.layout.remote_service_binding)

        // Watch for button taps.
        var button: Button = findViewById(R.id.bind)
        button.setOnClickListener(mBindListener)
        button = findViewById(R.id.unbind)
        button.setOnClickListener(unbindListener)
        killButton = findViewById(R.id.kill)
        killButton.setOnClickListener(killListener)
        killButton.isEnabled = false

        callbackText = findViewById(R.id.callback)
        callbackText.text = "Not attached."
        handler = InternalHandler(callbackText)
    }

    private class InternalHandler(
            textView: TextView,
            private val weakTextView: WeakReference<TextView> = WeakReference(textView)
    ) : Handler() {
        override fun handleMessage(msg: Message) {
            when (msg.what) {
                BUMP_MSG -> weakTextView.get()?.text = "Received from service: ${msg.arg1}"
                else -> super.handleMessage(msg)
            }
        }
    }
}
```

### Declare foreground services in the app manifest
```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android" ...>
  <application ...>

    <service
        android:name=".MyMediaPlaybackService"
        android:foregroundServiceType="mediaPlayback"
        android:exported="false">
    </service>
  </application>
</manifest>
```

### Key points about the code
```xml
android:foregroundServiceType="camera|microphone"
```

### Launch a service
```kotlin
val intent = Intent(...) // Build the intent for the service
context.startForegroundService(intent)
```

### Promote a service to the foreground
```kotlin
class MyCameraService: Service() {

  private fun startForeground() {
    // Before starting the service as foreground check that the app has the
    // appropriate runtime permissions. In this case, verify that the user has
    // granted the CAMERA permission.
    val cameraPermission =
            PermissionChecker.checkSelfPermission(this, Manifest.permission.CAMERA)
    if (cameraPermission != PermissionChecker.PERMISSION_GRANTED) {
        // Without camera permissions the service cannot run in the foreground
        // Consider informing user or updating your app UI if visible.
        stopSelf()
        return
    }

    try {
        val notification = NotificationCompat.Builder(this, "CHANNEL_ID")
            // Create the notification to display while the service is running
            .build()
        ServiceCompat.startForeground(
            /* service = */ this,
            /* id = */ 100, // Cannot be 0
            /* notification = */ notification,
            /* foregroundServiceType = */
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
                ServiceInfo.FOREGROUND_SERVICE_TYPE_CAMERA
            } else {
                0
            },
        )
    } catch (e: Exception) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S
                && e is ForegroundServiceStartNotAllowedException) {
            // App not in a valid state to start foreground service
            // (e.g. started from bg)
        }
        // ...
    }
  }
}
```

### Handle user-initiated stopping of apps running foreground services 

 
 
 
 

 

```
adb shell cmd activity stop-app PACKAGE_NAME
```

### Determine which services are affected in your app
```
Foreground service started from background can not have \
location/camera/microphone access: service SERVICE_NAME
```

### Timeout behavior
```
Fatal Exception: android.app.RemoteServiceException: "A foreground service of
type [service type] did not stop within its timeout: [component name]"
```

### Testing
```
adb shell am compat enable FGS_INTRODUCE_TIME_LIMITS your-package-name
```

### Testing
```
adb shell device_config put activity_manager data_sync_fgs_timeout_duration duration-in-milliseconds
```

### Testing
```
adb shell device_config put activity_manager media_processing_fgs_timeout_duration duration-in-milliseconds
```

### Special use
```xml
<service android:name="fooService" android:foregroundServiceType="specialUse">
  <property android:name="android.app.PROPERTY_SPECIAL_USE_FGS_SUBTYPE"
      android:value="explanation_for_special_use"/>
</service>
```

### Internal exception: ForegroundServiceDidNotStartInTimeException
```
android.app.RemoteServiceException$ForegroundServiceDidNotStartInTimeException:
Context.startForegroundService() did not then call Service.startForeground()
```

### Internal exception: ForegroundServiceDidNotStartInTimeException
```
Re-initializing SystemForegroundService after a request to shut-down
```

### Set a repeating alarm
```kotlin
val alarmManager =
    context.getSystemService(Context.ALARM_SERVICE) as? AlarmManager
val pendingIntent =
    PendingIntent.getService(context, requestId, intent,
                                PendingIntent.FLAG_NO_CREATE)
if (pendingIntent != null && alarmManager != null) {
  alarmManager.cancel(pendingIntent)
}
```

### Examples of elapsed real time alarms
```
// Hopefully your alarm will have a lower frequency than this!
alarmMgr?.setInexactRepeating(
        AlarmManager.ELAPSED_REALTIME_WAKEUP,
        SystemClock.elapsedRealtime() + AlarmManager.INTERVAL_HALF_HOUR,
        AlarmManager.INTERVAL_HALF_HOUR,
        alarmIntent
)
```

### Examples of elapsed real time alarms
```
private var alarmMgr: AlarmManager? = null
private lateinit var alarmIntent: PendingIntent
...
alarmMgr = context.getSystemService(Context.ALARM_SERVICE) as AlarmManager
alarmIntent = Intent(context, AlarmReceiver::class.java).let { intent ->
    PendingIntent.getBroadcast(context, 0, intent, 0)
}

alarmMgr?.set(
        AlarmManager.ELAPSED_REALTIME_WAKEUP,
        SystemClock.elapsedRealtime() + 60 * 1000,
        alarmIntent
)
```

### Examples of real time clock alarms
```kotlin
// Set the alarm to start at approximately 2:00 p.m.
val calendar: Calendar = Calendar.getInstance().apply {
    timeInMillis = System.currentTimeMillis()
    set(Calendar.HOUR_OF_DAY, 14)
}

// With setInexactRepeating(), you have to use one of the AlarmManager interval
// constants--in this case, AlarmManager.INTERVAL_DAY.
alarmMgr?.setInexactRepeating(
        AlarmManager.RTC_WAKEUP,
        calendar.timeInMillis,
        AlarmManager.INTERVAL_DAY,
        alarmIntent
)
```

### Cancel an alarm
```
// If the alarm has been set, cancel it.
alarmMgr?.cancel(alarmIntent)
```

### Start an alarm when the device restarts
```xml
<uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED"/>
```

### Start an alarm when the device restarts
```kotlin
class SampleBootReceiver : BroadcastReceiver() {

    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action == "android.intent.action.BOOT_COMPLETED") {
            // Set the alarm here.
        }
    }
}
```

### Start an alarm when the device restarts
```xml
<receiver android:name=".SampleBootReceiver"
        android:enabled="false">
    <intent-filter>
        <action android:name="android.intent.action.BOOT_COMPLETED"></action>
    </intent-filter>
</receiver>
```

### Start an alarm when the device restarts
```kotlin
val receiver = ComponentName(context, SampleBootReceiver::class.java)

context.packageManager.setComponentEnabledSetting(
        receiver,
        PackageManager.COMPONENT_ENABLED_STATE_ENABLED,
        PackageManager.DONT_KILL_APP
)
```

## Pitfalls
- Note: If a background work task takes longer than 10 minutes to complete, it's
highly likely to be interrupted. You should try to find ways to break tasks like
that into smaller sub-tasks. If you need to create a long-running task and you
can't break it into subtasks, and you don't want the task to
- Note: Beginning with Android 12, most foreground services do not show
notifications to the user until they've been running for 10
seconds.
- Note: To avoid these limitations and their associated warnings, you should use
WorkManager to schedule your background tasks.
- Caution: Failing to implement the corresponding getForegroundInfo method can
lead to runtime crashes when calling setExpedited on older platform versions.
- Caution: setForeground() can throw runtime exceptions on Android 12, and might
throw an exception if the launch was restricted .
- Note: Backoff delays are inexact and could vary by several seconds between
retries but will never be less than the initial backoff delay specified in your
configuration.
- Caution: It is not possible to use updateWork() to change the type of Worker 
in a WorkRequest . For example, if you have enqueued a OneTimeWorkRequest and
you would like for it to run periodically, you must cancel the request and
schedule a new PeriodicWorkRequest .
- Note: If you call the deprecated no-parameter WorkManager.getInstance() method
before WorkManager has been initialized, the method throws an exception. You
should always use the WorkManager.getInstance(Context) method, even if you're
not customizing WorkManager.
- Note: GCMNetworkManager requires you to define an execution window, but
WorkManager does not require this. Instead, WorkManager runs the job as soon as
possible after the constraints are met. In this example, we assume you don't
actually need to set a specific time for the job to run.
- Note: Some APIs acquire wake locks that are attributed to your app .
This means your app
might be using wake locks even though you aren't writing that code explicitly.
If your app has mysterious performance issues, it can be helpful to check if
there are misbehaving wake locks.
If your app is holdin
- Warning: This sample code is only recommended when the result is available
 immediately . ImmediateFuture shouldn't be used in synchronous APIs, such as
when getQueryResult() is a long-running blocking call.
- Some system broadcasts come from highly privileged
apps, such as Bluetooth and telephony, that are part of the Android
framework but don't run under the system's unique process ID (UID). To
receive all system broadcasts, including broadcasts from highly privileged
apps, flag your receiver with RECEI
- Caution: If you export the broadcast receiver, other apps could send
unprotected broadcasts to your app.
- Note: If your app targets API level 26 or higher, you cannot use the manifest to
declare a receiver for implicit broadcasts, except for a few implicit
broadcasts that are exempted from that restriction . Implicit broadcasts
are broadcasts that don't target your app specifically. In most cases, you c
- Note: Even though these implicit broadcasts still work in the
background, avoid registering listeners for them.
- Caution: When your app schedules an exact alarm using this method, the
invocation of the alarm can significantly affect the device's resources,
such as battery life.

## Decision Tables
### Common background data transfer scenarios
| WorkManager | For scheduling tasks with duration less than 10 minutes that should
 execute when the app is not visible. | Deferrable: Can also be adjusted by constraints Immediate: Use
 
 setExpedited if the work needs to run immediately | Periodically syncing data with a server Downloading or
 uploading media while on the network Background-initiated (not by the user) |
| --- | --- | --- | --- |
| User-Initiated Data Transfer Job | When the data transfer is triggered by the user and you need to keep
 the user informed about the transfer's progress. | Initiated by the user (i.e. button click) - starts immediately | Uploading a photo, downloading a file |
| Foreground Service | For short, critical tasks, or when WorkManager is not an option. A
 notification informs the user of the transfer's progress. | Starts immediately | connectedDevice : Syncing data with a connected device 
 
 shortService : File processing under 3 minutes 
 
 mediaProcessing : Encoding or decoding a media file |
| Specific API | Use if one exists for that particular operation. Can yield benefits
 such as optimized performance and improved system integration. | Varies | Syncing data with a connected device |

### Types of work
| Type | Periodicity | How to access |
| --- | --- | --- |
| Immediate | One time | OneTimeWorkRequest and Worker . For expedited work, call setExpedited() on your OneTimeWorkRequest. |
| Long Running | One time or periodic | Any WorkRequest or Worker . Call setForeground() in the Worker to handle the notification. |
| Deferrable | One time or periodic | PeriodicWorkRequest and Worker . |

### Relationship to other APIs
| API | Recommended for | Relationship to WorkManager |
| --- | --- | --- |
| Coroutines | All asynchronous work that doesn't need to persist if the app
 leaves the visible state. | Coroutines are the standard means of leaving the main thread in Kotlin.
 However, they stop as soon as the app closes. For work that should persist
 even after the app closes, use WorkManager. |
| AlarmManager | Alarms only. | Unlike WorkManager's regular workers, AlarmManager's exact alarms wake a
 device from Doze mode. It is therefore not efficient in terms of power and
 resource management. Only use it for precise alarms or notifications such as
 calendar events, not for recurring background work. |

### Work constraints
| NetworkType | Constrains the type of network required for your work to run.
For example, Wi-Fi ( UNMETERED ). |
| --- | --- |
| BatteryNotLow | When set to true, your work will not run if the device is in low battery mode. |
| RequiresCharging | When set to true, your work will only run when the device is charging. |
| DeviceIdle | When set to true, this requires the user's device to be idle before the work will run. This can be useful for running batched operations that might otherwise have a negative performance impact on other apps running actively on the user's device. |
| StorageNotLow | When set to true, your work won't run if the user's storage space on the device is too low. |

### Constraint mappings
| GCMNetworkManager constraint | WorkManager equivalent | Notes |
| --- | --- | --- |
| setPersisted() | (not required) | All WorkManager jobs are persisted across device reboots |
| setRequiredNetwork() | setRequiredNetworkType() | By default GCMNetworkManager requires network access. WorkManager does not require network access by default. If your job requires network access, you must use setRequiredNetworkType(CONNECTED) , or set some more specific network type. |
| setRequiresCharging() |  |  |

### Java and Kotlin
|  | Kotlin | Java |
| --- | --- | --- |
| Solution | Coroutines. | Java threads. |
| Further reading | For a full overview of Coroutines, see the Coroutines guide . | See the Java Threads page for more information. |

## Guidelines
- For the purposes of this document, we'll use the term "task" to mean an
operation an app is doing outside its main workflow. To ensure alignment in
understanding, we've put this into three main categories of types of tasks:
 asynchronous work , the
 task scheduling APIs ,
and foreground services .
- In most scenarios, you can figure out the right APIs to use for your task by
figuring out the category ( asynchronous work , the
 task scheduling APIs , or
 foreground services ) the
task falls under.
- If you're still unsure, you can use the flow charts we provide which add more
nuance to the decision. Each of these options is described in more detail later
in this document.
- Note: In most cases, your best option for running background tasks is to use
WorkManager.
However, there are a few situations where another option is better. This page
will help you understand which solution fits your needs best.
- There are two main scenarios to consider for background tasks:
- In many cases, an app just needs to do concurrent operations while it's running
in the foreground. For example, an app might need to do a time-consuming
calculation. If it did the calculation on the UI thread, the user wouldn't be
able to interact with the app until the calculation finished; this might result
in an ANR error. In a case like this, the app should use an asynchronous work 
option.
- The task scheduling APIs are a more flexible option when you need to do tasks
that need to
continue even if the user leaves the app. In most cases, the best option for
running background tasks is to use WorkManager ,
though in some cases it may be appropriate to use the platform
 JobScheduler API.
- WorkManager is a powerful library that lets you set up simple or complicated
jobs as you need. You can use WorkManager to schedule tasks to run at specific
times, or specify the conditions when the task should run. You can even set up
chains of tasks, so each task runs in turn, passing its results to the next one.
To understand all the options available, read through the WorkManager feature
list .
- Getting periodic location data (you must be granted
 ACCESS_BACKGROUND_LOCATION permission on Android 10 or
higher)
- The system offers alternative APIs which are designed to perform better for more
specific use cases. If an alternative API exists for your use case, we recommend
using that API instead of a foreground service as it should help your app
perform better. The foreground service types documentation notes
when there's a good alternative API to use instead of a particular foreground
service type.
- It's important to consider whether the user experience would be harmed if a task
is postponed or canceled. For example, if an app needs to update its assets, the
user might not notice whether the operation happens right away, or in the middle
of the night while the device is recharging. In cases like this, you should use
the background work options.
- If the task cannot be delayed and it will complete quickly, you can use a
 foreground service with the type
 shortService . These
services are easier to create than other foreground services, and don't require
as many permissions. However, short services must complete within three minutes.
- If you can be sure that the task will finish in a few seconds, use asynchronous
work to perform the task. The system will allow your app a
few seconds to perform any such tasks, even if your app was in the background.
- If the task will take longer than a few seconds, use the
 task scheduling APIs .
- Caution: A service runs in the main thread of its hosting
process; the service does not create its own thread and does not 
run in a separate process unless you specify otherwise. You should run any blocking operations on
a separate thread within the service to avoid Application
Not Responding (ANR) errors.
- A foreground service performs some operation that is noticeable to the
 user. For example, an audio app would use a foreground service to play an
 audio track. Foreground services must display a Notification .
 Foreground services continue running even when the user isn't interacting
 with the app.
- When you use a foreground service, you must display a notification so that
 users are actively aware that the service is running. This notification cannot
 be dismissed unless the service is either stopped or removed from the
 foreground.
- A service is simply a component that can run in the background, even when the user is not
interacting with your application, so you should create a service only if that is what you
need.
- Remember that if you do use a service, it still runs in your application's main thread by
default, so you should still create a new thread within the service if it performs intensive or
blocking operations.
- To create a service, you must create a subclass of Service or use one
of its existing subclasses. In your implementation, you must override some callback methods that
handle key aspects of the service lifecycle and provide a mechanism that allows the components to
bind to the service, if appropriate. These are the most important callback methods that you should
override:

## Concepts (for graph)
- Terminology
- Key Term:
- Choose the right option
- Asynchronous work
- Task scheduling APIs
- Foreground services
- Alternative APIs
- Tasks initiated by the user
- Figure 1
- Does the task need to continue running while the app is in the background?
- Will there be a bad user experience if the task is deferred or interrupted?
- Is it a short, critical task?
