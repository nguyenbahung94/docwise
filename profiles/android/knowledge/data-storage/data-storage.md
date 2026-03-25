<!-- Source: https://developer.android.com/training/data-storage -->
<!-- Source: https://developer.android.com/training/data-storage/app-specific -->
<!-- Source: https://developer.android.com/training/data-storage/shared -->
<!-- Source: https://developer.android.com/training/data-storage/shared/media -->
<!-- Source: https://developer.android.com/training/data-storage/shared/photo-picker -->
<!-- Source: https://developer.android.com/training/data-storage/shared/documents-files -->
<!-- Source: https://developer.android.com/training/data-storage/manage-all-files -->
<!-- Source: https://developer.android.com/training/data-storage/shared-preferences -->
<!-- Source: https://developer.android.com/training/data-storage/sqlite -->
<!-- Source: https://developer.android.com/training/data-storage/use-cases -->
<!-- Source: https://developer.android.com/training/data-storage/app-specific -->
<!-- Source: https://developer.android.com/training/data-storage/shared -->
<!-- Source: https://developer.android.com/training/data-storage/shared/media -->
<!-- Source: https://developer.android.com/training/data-storage/shared/photo-picker -->
<!-- Source: https://developer.android.com/training/data-storage/shared/photo-picker/embedded -->
<!-- Source: https://developer.android.com/training/data-storage/shared/documents-files -->
<!-- Source: https://developer.android.com/training/data-storage/shared/datasets -->
<!-- Source: https://developer.android.com/training/data-storage/manage-all-files -->
<!-- Source: https://developer.android.com/training/data-storage/shared-preferences -->
<!-- Source: https://developer.android.com/training/data-storage/room -->
<!-- Source: https://developer.android.com/training/data-storage/room/defining-data -->
<!-- Source: https://developer.android.com/training/data-storage/room/accessing-data -->
<!-- Source: https://developer.android.com/training/data-storage/room/relationships -->
<!-- Source: https://developer.android.com/training/data-storage/room/relationships/one-to-one -->
<!-- Source: https://developer.android.com/training/data-storage/room/relationships/one-to-many -->
<!-- Source: https://developer.android.com/training/data-storage/room/relationships/many-to-many -->
<!-- Source: https://developer.android.com/training/data-storage/room/relationships/nested -->
<!-- Source: https://developer.android.com/training/data-storage/room/async-queries -->
<!-- Source: https://developer.android.com/training/data-storage/room/creating-views -->
<!-- Source: https://developer.android.com/training/data-storage/room/prepopulate -->
<!-- Source: https://developer.android.com/training/data-storage/room/migrating-db-versions -->
<!-- Source: https://developer.android.com/training/data-storage/room/testing-db -->
<!-- Source: https://developer.android.com/training/data-storage/room/referencing-data -->
<!-- Source: https://developer.android.com/training/data-storage/room/sqlite-room-migration -->
<!-- Source: https://developer.android.com/training/data-storage/sqlite -->
<!-- Source: https://developer.android.com/training/data-storage/use-cases -->
<!-- Type: official -->
<!-- Priority: high -->
<!-- Topic: data-storage -->
<!-- Extracted: 2026-03-24 -->
<!-- Verified: — -->

# Data and file storage overview

## Rules
- DON'T: The exact location of where your files can be saved might vary across
devices. For this reason, don't use hard-coded file paths.
- DON'T: To avoid accidental disclosure of information, don't use predictable
 patterns to filenames in ways that could reveal the kinds of information
 found within a file.
- DO: Use scoped storage unless your app needs access to a file that's stored outside
of an app-specific directory and outside
of a directory that the MediaStore 
APIs can access. If you store app-specific files on external storage, you can
make it easier to adopt scoped storage by placing these files in
- DO: External storage directories: These directories include both a dedicated
location for storing persistent files, and another location for storing
cache data. Although it's possible for another app to access these directories
if that app has the proper permissions, the files stored in these directorie
- DO: Use shared storage for user data that can or should be accessible to other apps
and saved even if the user uninstalls your app.
- DON'T: If scoped storage is enabled, the collection shows only the photos, videos,
and audio files that your app has created. Most developers don't need to use
 MediaStore.Files to view media files from other apps, but if you have a
specific requirement to do so, you can declare the READ_EXTERNAL_STORAGE
- DON'T: Don't assume any implementation details regarding the version number.
- DON'T: Cache the column indices so that you don't need to call
 getColumnIndexOrThrow() 
each time you process a row from the query result.
- DON'T: From your MediaStore object, get the exact bytes of the photograph by
calling
 setRequireOriginal() 
and passing in the URI of the photograph, as shown in the following code snippet: 

 
 Kotlin 
 val photoUri : Uri = Uri . withAppendedPath ( 
 MediaStore . Images . Media . EXTERNAL_CONTENT_URI ,
- DO: Use the following activity result contracts to launch the photo picker:
- DO: Use the
 ACTION_CREATE_DOCUMENT 
intent action to load the system file picker and allow the user to choose a
location where to write the contents of a file. This process is similar to the
one used in the "save as" dialogs that other operating systems use.
- DO: Use the
 ACTION_MANAGE_ALL_FILES_ACCESS_PERMISSION 
intent action to direct users to a system settings page where they can enable
the following option for your app: Allow access to manage all files .
- DON'T: getPreferences() : Use this from an Activity if you need
to use only one shared preference file for the activity. Because this
retrieves a default shared preference file that belongs to the activity, you
don't need to supply a name.
- DO: Use the MediaStore API to modify
or delete the media files.
- DO: Use the query() 
API to query a media collection .
- DO: Use the ACTION_GET_CONTENT 
intent, which asks the user to pick an image to import.
- DO: Use the
 insert() 
method to add records directly into the MediaStore. For more information, see
the Add an item section of the
media storage guide.
- DO: Use the Android FileProvider component, as described in the Setting up file
sharing guide.
- DO: Use the ACTION_OPEN_DOCUMENT 
intent to ask the user to pick a file to open using the system picker. If you
want to filter the types of files that the system picker will present to the
user to choose from, you can use
 setType() 
or EXTRA_MIME_TYPES .
- DO: Use the scoped storage model.
- DO: Use the Storage Access
Framework , which allows users to
select the location on a secondary storage volume where your app can write the
file.
- DON'T: Large files or files that do not contain sensitive information : Use
 Context#getExternalCacheDir() .
- DO: Use gutter actions to quickly run queries from your DAO
classes .
- DO: Annotate the class declaration with
 @Entity to indicate that it is a
Room entity. You can optionally use the
 tableName property to
indicate that the resulting table should have a name that is different from
the class name.
- DO: If any of the columns in the resulting table should have a name that is
different from the name of the corresponding field, annotate the field with
 @ColumnInfo and set the
 name property to the
correct column name.
- DON'T: If the class has fields that you do not want to persist in the database,
annotate those fields with
 @Ignore to indicate that Room
should not create columns for them in the corresponding table.
- DO: If the class has more than one constructor method, indicate which constructor
Room should use by annotating all of the other constructors with @Ignore .

## Code Patterns
### Categories of storage locations
```xml
<manifest ...
  android:installLocation="preferExternal">
  ...
</manifest>
```

### Access and store files
```kotlin
val file = File(context.filesDir, filename)
```

### Store a file using a stream
```kotlin
val filename = "myfile"
val fileContents = "Hello world!"
context.openFileOutput(filename, Context.MODE_PRIVATE).use {
        it.write(fileContents.toByteArray())
}
```

### Access a file using a stream
```
context.openFileInput(filename).bufferedReader().useLines { lines ->
    lines.fold("") { some, text ->
        "$some\n$text"
    }
}
```

### View list of files
```
var files: Array<String> = context.fileList()
```

### Create nested directories
```
context.getDir(dirName, Context.MODE_PRIVATE)
```

### Create cache files
```
File.createTempFile(filename, null, context.cacheDir)
```

### Create cache files
```kotlin
val cacheFile = File(context.cacheDir, filename)
```

### Remove cache files
```
cacheFile.delete()
```

### Remove cache files
```
context.deleteFile(cacheFileName)
```

### Verify that storage is available
```kotlin
// Checks if a volume containing external storage is available
// for read and write.
fun isExternalStorageWritable(): Boolean {
    return Environment.getExternalStorageState() == Environment.MEDIA_MOUNTED
}

// Checks if a volume containing external storage is available to at least read.
fun isExternalStorageReadable(): Boolean {
     return Environment.getExternalStorageState() in
        setOf(Environment.MEDIA_MOUNTED, Environment.MEDIA_MOUNTED_READ_ONLY)
}
```

### Verify that storage is available
```
adb shell sm set-virtual-disk true
```

### Select a physical storage location
```kotlin
val externalStorageVolumes: Array<out File> =
        ContextCompat.getExternalFilesDirs(applicationContext, null)
val primaryExternalStorage = externalStorageVolumes[0]
```

### Access persistent files
```kotlin
val appSpecificExternalDir = File(context.getExternalFilesDir(null), filename)
```

### Create cache files
```kotlin
val externalCacheFile = File(context.externalCacheDir, filename)
```

### Remove cache files
```
externalCacheFile.delete()
```

### Media content
```kotlin
fun getAppSpecificAlbumStorageDir(context: Context, albumName: String): File? {
    // Get the pictures directory that's inside the app-specific directory on
    // external storage.
    val file = File(context.getExternalFilesDir(
            Environment.DIRECTORY_PICTURES), albumName)
    if (!file?.mkdirs()) {
        Log.e(LOG_TAG, "Directory not created")
    }
    return file
}
```

### Query free space
```kotlin
// App needs 10 MB within internal storage.
const val NUM_BYTES_NEEDED_FOR_MY_APP = 1024 * 1024 * 10L;

val storageManager = applicationContext.getSystemService<StorageManager>()!!
val appSpecificInternalDirUuid: UUID = storageManager.getUuidForPath(filesDir)
val availableBytes: Long =
        storageManager.getAllocatableBytes(appSpecificInternalDirUuid)
if (availableBytes >= NUM_BYTES_NEEDED_FOR_MY_APP) {
    storageManager.allocateBytes(
        appSpecificInternalDirUuid, NUM_BYTES_NEEDED_FOR_MY_APP)
} else {
    val storageIntent = Intent().apply {
        // To request that the user remove all app cache files instead, set
        // "action" to ACTION_CLEAR_APP_CACHE.
        action = ACTION_MANAGE_STORAGE
    }
}
```

### Ask user to remove some device files
```
StorageStatsManager.getFreeBytes() / StorageStatsManager.getTotalBytes()
```

### Media store
```kotlin
val projection = arrayOf(media-database-columns-to-retrieve)
val selection = sql-where-clause-with-placeholder-variables
val selectionArgs = values-of-placeholder-variables
val sortOrder = sql-order-by-clause

applicationContext.contentResolver.query(
    MediaStore.media-type.Media.EXTERNAL_CONTENT_URI,
    projection,
    selection,
    selectionArgs,
    sortOrder
)?.use { cursor ->
    while (cursor.moveToNext()) {
        // Use an ID column from the projection to get
        // a URI representing the media item itself.
    }
}
```

### Access other apps' media files
```xml
<!-- Required only if your app needs to access images or photos
     that other apps created. -->
<uses-permission android:name="android.permission.READ_MEDIA_IMAGES" />

<!-- Required only if your app needs to access videos
     that other apps created. -->
<uses-permission android:name="android.permission.READ_MEDIA_VIDEO" />

<!-- Required only if your app needs to access audio files
     that other apps created. -->
<uses-permission android:name="android.permission.READ_MEDIA_AUDIO" />

<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>

<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"
                 android:maxSdkVersion="29" />
```

### Query a media collection
```kotlin
// Need the READ_EXTERNAL_STORAGE permission if accessing video files that your
// app didn't create.

// Container for information about each video.
data class Video(val uri: Uri,
    val name: String,
    val duration: Int,
    val size: Int
)
val videoList = mutableListOf<Video>()

val collection =
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
        MediaStore.Video.Media.getContentUri(
            MediaStore.VOLUME_EXTERNAL
        )
    } else {
        MediaStore.Video.Media.EXTERNAL_CONTENT_URI
    }

val projection = arrayOf(
    MediaStore.Video.Media._ID,
    MediaStore.Video.Media.DISPLAY_NAME,
    MediaStore.Video.Media.DURATION,
    MediaStore.Video.Media.SIZE
)

// Show only videos that are at least 5 minutes in duration.
val selection = "${MediaStore.Video.Media.DURATION} >= ?"
val selectionArgs = arrayOf(
    TimeUnit.MILLISECONDS.convert(5, TimeUnit.MINUTES).toString()
)

// Display videos in alphabetical order based on their display name.
val sortOrder = "${MediaStore.Video.Media.DISPLAY_NAME} ASC"

val query = ContentResolver.query(
    collection,
    projection,
    selection,
    selectionArgs,
    sortOrder
)
query?.use { cursor ->
    // Cache column indices.
    val idColumn = cursor.getColumnIndexOrThrow(MediaStore.Video.Media._ID)
    val nameColumn =
            cursor.getColumnIndexOrThrow(MediaStore.Video.Media.DISPLAY_NAME)
    val durationColumn =
            cursor.getColumnIndexOrThrow(MediaStore.Video.Media.DURATION)
    val sizeColumn = cursor.getColumnIndexOrThrow(MediaStore.Video.Media.SIZE)

    while (cursor.moveToNext()) {
        // Get values of columns for a given video.
        val id = cursor.getLong(idColumn)
        val name = cursor.getString(nameColumn)
        val duration = cursor.getInt(durationColumn)
        val size = cursor.getInt(sizeColumn)

        val contentUri: Uri = ContentUris.withAppendedId(
            MediaStore.Video.Media.EXTERNAL_CONTENT_URI,
            id
        )

        // Stores column values and the contentUri in a local object
        // that represents the media file.
        videoList += Video(contentUri, name, duration, size)
    }
}
```

### Load file thumbnails
```kotlin
// Load thumbnail of a specific media item.
val thumbnail: Bitmap =
        applicationContext.contentResolver.loadThumbnail(
        content-uri, Size(640, 480), null)
```

### File descriptor
```kotlin
// Open a specific media item using ParcelFileDescriptor.
val resolver = applicationContext.contentResolver

// "rw" for read-and-write.
// "rwt" for truncating or overwriting existing file contents.
val readOnlyMode = "r"
resolver.openFileDescriptor(content-uri, readOnlyMode).use { pfd ->
    // Perform operations on "pfd".
}
```

### File stream
```kotlin
// Open a specific media item using InputStream.
val resolver = applicationContext.contentResolver
resolver.openInputStream(content-uri).use { stream ->
    // Perform operations on "stream".
}
```

### Storage volumes
```kotlin
val volumeNames: Set<String> = MediaStore.getExternalVolumeNames(context)
val firstVolumeName = volumeNames.iterator().next()
```

### Photographs
```kotlin
val photoUri: Uri = Uri.withAppendedPath(
        MediaStore.Images.Media.EXTERNAL_CONTENT_URI,
        cursor.getString(idColumnIndex)
)

// Get location data using the Exifinterface library.
// Exception occurs if ACCESS_MEDIA_LOCATION permission isn't granted.
photoUri = MediaStore.setRequireOriginal(photoUri)
contentResolver.openInputStream(photoUri)?.use { stream ->
    ExifInterface(stream).run {
        // If lat/long is null, fall back to the coordinates (0, 0).
        val latLong = latLong ?: doubleArrayOf(0.0, 0.0)
    }
}
```

### Videos
```kotlin
val retriever = MediaMetadataRetriever()
val context = applicationContext

// Find the videos that are stored on a device by querying the video collection.
val query = ContentResolver.query(
    collection,
    projection,
    selection,
    selectionArgs,
    sortOrder
)
query?.use { cursor ->
    val idColumn = cursor.getColumnIndexOrThrow(MediaStore.Video.Media._ID)
    while (cursor.moveToNext()) {
        val id = cursor.getLong(idColumn)
        val videoUri: Uri = ContentUris.withAppendedId(
            MediaStore.Video.Media.EXTERNAL_CONTENT_URI,
            id
        )
        extractVideoLocationInfo(videoUri)
    }
}

private fun extractVideoLocationInfo(videoUri: Uri) {
    try {
        retriever.setDataSource(context, videoUri)
    } catch (e: RuntimeException) {
        Log.e(APP_TAG, "Cannot retrieve video file", e)
    }
    // Metadata uses a standardized format.
    val locationMetadata: String? =
            retriever.extractMetadata(MediaMetadataRetriever.METADATA_KEY_LOCATION)
}
```

### Add an item
```kotlin
// Add a specific media item.
val resolver = applicationContext.contentResolver

// Find all audio files on the primary external storage device.
val audioCollection =
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
        MediaStore.Audio.Media.getContentUri(
            MediaStore.VOLUME_EXTERNAL_PRIMARY
        )
    } else {
        MediaStore.Audio.Media.EXTERNAL_CONTENT_URI
    }

// Publish a new song.
val newSongDetails = ContentValues().apply {
    put(MediaStore.Audio.Media.DISPLAY_NAME, "My Song.mp3")
}

// Keep a handle to the new song's URI in case you need to modify it
// later.
val myFavoriteSongUri = resolver
        .insert(audioCollection, newSongDetails)
```

### Toggle pending status for media files
```kotlin
// Add a media item that other apps don't see until the item is
// fully written to the media store.
val resolver = applicationContext.contentResolver

// Find all audio files on the primary external storage device.
val audioCollection =
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
        MediaStore.Audio.Media.getContentUri(
            MediaStore.VOLUME_EXTERNAL_PRIMARY
        )
    } else {
        MediaStore.Audio.Media.EXTERNAL_CONTENT_URI
    }

val songDetails = ContentValues().apply {
    put(MediaStore.Audio.Media.DISPLAY_NAME, "My Workout Playlist.mp3")
    put(MediaStore.Audio.Media.IS_PENDING, 1)
}

val songContentUri = resolver.insert(audioCollection, songDetails)

// "w" for write.
resolver.openFileDescriptor(songContentUri, "w", null).use { pfd ->
    // Write data into the pending audio file.
}

// Now that you're finished, release the "pending" status and let other apps
// play the audio track.
songDetails.clear()
songDetails.put(MediaStore.Audio.Media.IS_PENDING, 0)
resolver.update(songContentUri, songDetails, null, null)
```

### Update an item
```kotlin
// Updates an existing media item.
val mediaId = // MediaStore.Audio.Media._ID of item to update.
val resolver = applicationContext.contentResolver

// When performing a single item update, prefer using the ID.
val selection = "${MediaStore.Audio.Media._ID} = ?"

// By using selection + args you protect against improper escaping of // values.
val selectionArgs = arrayOf(mediaId.toString())

// Update an existing song.
val updatedSongDetails = ContentValues().apply {
    put(MediaStore.Audio.Media.DISPLAY_NAME, "My Favorite Song.mp3")
}

// Use the individual song's URI to represent the collection that's
// updated.
val numSongsUpdated = resolver.update(
        myFavoriteSongUri,
        updatedSongDetails,
        selection,
        selectionArgs)
```

### Update in native code
```kotlin
val contentUri: Uri = ContentUris.withAppendedId(
        MediaStore.Audio.Media.EXTERNAL_CONTENT_URI,
        cursor.getLong(BaseColumns._ID))
val fileOpenMode = "r"
val parcelFd = resolver.openFileDescriptor(contentUri, fileOpenMode)
val fd = parcelFd?.detachFd()
// Pass the integer value "fd" into your native code. Remember to call
// close(2) on the file descriptor when you're done using it.
```

### Update other apps' media files
```kotlin
// Apply a grayscale filter to the image at the given content URI.
try {
    // "w" for write.
    contentResolver.openFileDescriptor(image-content-uri, "w")?.use {
        setGrayscaleFilter(it)
    }
} catch (securityException: SecurityException) {
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
        val recoverableSecurityException = securityException as?
            RecoverableSecurityException ?:
            throw RuntimeException(securityException.message, securityException)

        val intentSender =
            recoverableSecurityException.userAction.actionIntent.intentSender
        intentSender?.let {
            startIntentSenderForResult(intentSender, image-request-code,
                    null, 0, 0, 0, null)
        }
    } else {
        throw RuntimeException(securityException.message, securityException)
    }
}
```

### Remove an item
```kotlin
// Remove a specific media item.
val resolver = applicationContext.contentResolver

// URI of the image to remove.
val imageUri = "..."

// WHERE clause.
val selection = "..."
val selectionArgs = "..."

// Perform the actual removal.
val numImagesRemoved = resolver.delete(
        imageUri,
        selection,
        selectionArgs)
```

### Manage groups of media files
```kotlin
val urisToModify = /* A collection of content URIs to modify. */
val editPendingIntent = MediaStore.createWriteRequest(contentResolver,
        urisToModify)

// Launch a system prompt requesting user permission for the operation.
startIntentSenderForResult(editPendingIntent.intentSender, EDIT_REQUEST_CODE,
    null, 0, 0, 0)
```

### Manage groups of media files
```kotlin
override fun onActivityResult(requestCode: Int, resultCode: Int,
                 data: Intent?) {
    ...
    when (requestCode) {
        EDIT_REQUEST_CODE ->
            if (resultCode == Activity.RESULT_OK) {
                /* Edit request granted; proceed. */
            } else {
                /* Edit request not granted; explain to the user. */
            }
    }
}
```

### Views
```kotlin
// Registers a photo picker activity launcher in single-select mode.
val pickMedia = registerForActivityResult(PickVisualMedia()) { uri ->
    // Callback is invoked after the user selects a media item or closes the
    // photo picker.
    if (uri != null) {
        Log.d("PhotoPicker", "Selected URI: $uri")
    } else {
        Log.d("PhotoPicker", "No media selected")
    }
}

// Include only one of the following calls to launch(), depending on the types
// of media that you want to let the user choose from.

// Launch the photo picker and let the user choose images and videos.
pickMedia.launch(PickVisualMediaRequest(PickVisualMedia.ImageAndVideo))

// Launch the photo picker and let the user choose only images.
pickMedia.launch(PickVisualMediaRequest(PickVisualMedia.ImageOnly))

// Launch the photo picker and let the user choose only videos.
pickMedia.launch(PickVisualMediaRequest(PickVisualMedia.VideoOnly))

// Launch the photo picker and let the user choose only images/videos of a
// specific MIME type, such as GIFs.
val mimeType = "image/gif"
pickMedia.launch(PickVisualMediaRequest(PickVisualMedia.SingleMimeType(mimeType)))
```

### Views
```kotlin
// Registers a photo picker activity launcher in multi-select mode.
// In this example, the app lets the user select up to 5 media files.
val pickMultipleMedia =
        registerForActivityResult(PickMultipleVisualMedia(5)) { uris ->
    // Callback is invoked after the user selects media items or closes the
    // photo picker.
    if (uris.isNotEmpty()) {
        Log.d("PhotoPicker", "Number of items selected: ${uris.size}")
    } else {
        Log.d("PhotoPicker", "No media selected")
    }
}

// For this example, launch the photo picker and let the user choose images
// and videos. If you want the user to select a specific type of media file,
// use the overloaded versions of launch(), as shown in the section about how
// to select a single media item.
pickMultipleMedia.launch(PickVisualMediaRequest(PickVisualMedia.ImageAndVideo))
```

### Device availability
```xml
<!-- Trigger Google Play services to install the backported photo picker module. -->
<service android:name="com.google.android.gms.metadata.ModuleDependencies"
         android:enabled="false"
         android:exported="false"
         tools:ignore="MissingClass">
    <intent-filter>
        <action android:name="com.google.android.gms.metadata.MODULE_DEPENDENCIES" />
    </intent-filter>
    <meta-data android:name="photopicker_activity:0:required" android:value="" />
</service>
```

### Persist media file access
```kotlin
val flag = Intent.FLAG_GRANT_READ_URI_PERMISSION
context.contentResolver.takePersistableUriPermission(uri, flag)
```

### How photo picker transcoding works
```kotlin
import androidx.activity.result.PickVisualMediaRequest
import androidx.activity.result.contract.ActivityResultContracts.PickVisualMedia
import androidx.annotation.RequiresApi
import android.os.Build
import android.util.Log
import android.provider.MediaStore

// Registers a photo picker activity launcher.
val pickMedia = registerForActivityResult(PickVisualMedia()) { uri ->
    // Callback invoked after media selected or picker activity closed.
    if (uri != null) {
        Log.d("photo picker", "Selected URI: $uri")
    } else {
        Log.d("photo picker", "No media selected")
    }
}

@RequiresApi(Build.VERSION_CODES.TIRAMISU)
fun launchPhotoPickerWithTranscodingSupport() {
    val mediaCapabilities = MediaCapabilities.Builder()
        .addSupportedHdrType(MediaCapabilities.HdrType.TYPE_HLG10)
        .build()

    // Launch the photo picker and let the user choose only videos with
    // transcoding enabled.
    pickMedia.launch(PickVisualMediaRequest.Builder()
        .setMediaType(PickVisualMedia.VideoOnly)
        .setMediaCapabilitiesForTranscoding(mediaCapabilities)
        .build())
}
```

### Create a new file
```kotlin
// Request code for creating a PDF document.
const val CREATE_FILE = 1

private fun createFile(pickerInitialUri: Uri) {
    val intent = Intent(Intent.ACTION_CREATE_DOCUMENT).apply {
        addCategory(Intent.CATEGORY_OPENABLE)
        type = "application/pdf"
        putExtra(Intent.EXTRA_TITLE, "invoice.pdf")

        // Optionally, specify a URI for the directory that should be opened in
        // the system file picker before your app creates the document.
        putExtra(DocumentsContract.EXTRA_INITIAL_URI, pickerInitialUri)
    }
    startActivityForResult(intent, CREATE_FILE)
}
```

### Open a file
```kotlin
// Request code for selecting a PDF document.
const val PICK_PDF_FILE = 2

fun openFile(pickerInitialUri: Uri) {
    val intent = Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
        addCategory(Intent.CATEGORY_OPENABLE)
        type = "application/pdf"

        // Optionally, specify a URI for the file that should appear in the
        // system file picker when it loads.
        putExtra(DocumentsContract.EXTRA_INITIAL_URI, pickerInitialUri)
    }

    startActivityForResult(intent, PICK_PDF_FILE)
}
```

### Grant access to a directory's contents
```kotlin
fun openDirectory(pickerInitialUri: Uri) {
    // Choose a directory using the system's file picker.
    val intent = Intent(Intent.ACTION_OPEN_DOCUMENT_TREE).apply {
        // Optionally, specify a URI for the directory that should be opened in
        // the system file picker when it loads.
        putExtra(DocumentsContract.EXTRA_INITIAL_URI, pickerInitialUri)
    }

    startActivityForResult(intent, your-request-code)
}
```

### Perform operations on chosen location
```kotlin
override fun onActivityResult(
        requestCode: Int, resultCode: Int, resultData: Intent?) {
    if (requestCode == your-request-code
            && resultCode == Activity.RESULT_OK) {
        // The result data contains a URI for the document or directory that
        // the user selected.
        resultData?.data?.also { uri ->
            // Perform operations on the document using its URI.
        }
    }
}
```

### Persist permissions
```kotlin
val contentResolver = applicationContext.contentResolver

val takeFlags: Int = Intent.FLAG_GRANT_READ_URI_PERMISSION or
        Intent.FLAG_GRANT_WRITE_URI_PERMISSION
// Check for the freshest data.
contentResolver.takePersistableUriPermission(uri, takeFlags)
```

### Examine document metadata
```kotlin
val contentResolver = applicationContext.contentResolver

fun dumpImageMetaData(uri: Uri) {

    // The query, because it only applies to a single document, returns only
    // one row. There's no need to filter, sort, or select fields,
    // because we want all fields for one document.
    val cursor: Cursor? = contentResolver.query(
            uri, null, null, null, null, null)

    cursor?.use {
        // moveToFirst() returns false if the cursor has 0 rows. Very handy for
        // "if there's anything to look at, look at it" conditionals.
        if (it.moveToFirst()) {

            // Note it's called "Display Name". This is
            // provider-specific, and might not necessarily be the file name.
            val displayName: String =
                    it.getString(it.getColumnIndex(OpenableColumns.DISPLAY_NAME))
            Log.i(TAG, "Display Name: $displayName")

            val sizeIndex: Int = it.getColumnIndex(OpenableColumns.SIZE)
            // If the size is unknown, the value stored is null. But because an
            // int can't be null, the behavior is implementation-specific,
            // and unpredictable. So as
            // a rule, check if it's null before assigning to an int. This will
            // happen often: The storage API allows for remote files, whose
            // size might not be locally known.
            val size: String = if (!it.isNull(sizeIndex)) {
                // Technically the column stores an int, but cursor.getString()
                // will do the conversion automatically.
                it.getString(sizeIndex)
            } else {
                "Unknown"
            }
            Log.i(TAG, "Size: $size")
        }
    }
}
```

### Bitmap
```kotlin
val contentResolver = applicationContext.contentResolver

@Throws(IOException::class)
private fun getBitmapFromUri(uri: Uri): Bitmap {
    val parcelFileDescriptor: ParcelFileDescriptor =
            contentResolver.openFileDescriptor(uri, "r")
    val fileDescriptor: FileDescriptor = parcelFileDescriptor.fileDescriptor
    val image: Bitmap = BitmapFactory.decodeFileDescriptor(fileDescriptor)
    parcelFileDescriptor.close()
    return image
}
```

### Edit a document
```kotlin
val contentResolver = applicationContext.contentResolver

private fun alterDocument(uri: Uri) {
    try {
        contentResolver.openFileDescriptor(uri, "w")?.use {
            FileOutputStream(it.fileDescriptor).use {
                it.write(
                    ("Overwritten at ${System.currentTimeMillis()}\n")
                        .toByteArray()
                )
            }
        }
    } catch (e: FileNotFoundException) {
        e.printStackTrace()
    } catch (e: IOException) {
        e.printStackTrace()
    }
}
```

### Delete a document
```
DocumentsContract.deleteDocument(applicationContext.contentResolver, uri)
```

### Open a virtual file
```kotlin
private fun isVirtualFile(uri: Uri): Boolean {
    if (!DocumentsContract.isDocumentUri(this, uri)) {
        return false
    }

    val cursor: Cursor? = contentResolver.query(
            uri,
            arrayOf(DocumentsContract.Document.COLUMN_FLAGS),
            null,
            null,
            null
    )

    val flags: Int = cursor?.use {
        if (cursor.moveToFirst()) {
            cursor.getInt(0)
        } else {
            0
        }
    } ?: 0

    return flags and DocumentsContract.Document.FLAG_VIRTUAL_DOCUMENT != 0
}
```

### Open a virtual file
```kotlin
@Throws(IOException::class)
private fun getInputStreamForVirtualFile(
        uri: Uri, mimeTypeFilter: String): InputStream {

    val openableMimeTypes: Array<String>? =
            contentResolver.getStreamTypes(uri, mimeTypeFilter)

    return if (openableMimeTypes?.isNotEmpty() == true) {
        contentResolver
                .openTypedAssetFileDescriptor(uri, openableMimeTypes[0], null)
                .createInputStream()
    } else {
        throw FileNotFoundException()
    }
}
```

### Enable MANAGE_EXTERNAL_STORAGE for testing
```
adb shell appops set --uid PACKAGE_NAME MANAGE_EXTERNAL_STORAGE allow
```

### Get a handle to shared preferences
```kotlin
val sharedPref = activity?.getSharedPreferences(
        getString(R.string.preference_file_key), Context.MODE_PRIVATE)
```

### Get a handle to shared preferences
```kotlin
val sharedPref = activity?.getPreferences(Context.MODE_PRIVATE)
```

### Define a schema and contract
```kotlin
object FeedReaderContract {
    // Table contents are grouped together in an anonymous object.
    object FeedEntry : BaseColumns {
        const val TABLE_NAME = "entry"
        const val COLUMN_NAME_TITLE = "title"
        const val COLUMN_NAME_SUBTITLE = "subtitle"
    }
}
```

### Create a database using an SQL helper
```kotlin
private const val SQL_CREATE_ENTRIES =
        "CREATE TABLE ${FeedEntry.TABLE_NAME} (" +
                "${BaseColumns._ID} INTEGER PRIMARY KEY," +
                "${FeedEntry.COLUMN_NAME_TITLE} TEXT," +
                "${FeedEntry.COLUMN_NAME_SUBTITLE} TEXT)"

private const val SQL_DELETE_ENTRIES = "DROP TABLE IF EXISTS ${FeedEntry.TABLE_NAME}"
```

### Create a database using an SQL helper
```kotlin
class FeedReaderDbHelper(context: Context) : SQLiteOpenHelper(context, DATABASE_NAME, null, DATABASE_VERSION) {
    override fun onCreate(db: SQLiteDatabase) {
        db.execSQL(SQL_CREATE_ENTRIES)
    }
    override fun onUpgrade(db: SQLiteDatabase, oldVersion: Int, newVersion: Int) {
        // This database is only a cache for online data, so its upgrade policy is
        // to simply to discard the data and start over
        db.execSQL(SQL_DELETE_ENTRIES)
        onCreate(db)
    }
    override fun onDowngrade(db: SQLiteDatabase, oldVersion: Int, newVersion: Int) {
        onUpgrade(db, oldVersion, newVersion)
    }
    companion object {
        // If you change the database schema, you must increment the database version.
        const val DATABASE_VERSION = 1
        const val DATABASE_NAME = "FeedReader.db"
    }
}
```

### Create a database using an SQL helper
```kotlin
val dbHelper = FeedReaderDbHelper(context)
```

### Put information into a database
```kotlin
// Gets the data repository in write mode
val db = dbHelper.writableDatabase

// Create a new map of values, where column names are the keys
val values = ContentValues().apply {
    put(FeedEntry.COLUMN_NAME_TITLE, title)
    put(FeedEntry.COLUMN_NAME_SUBTITLE, subtitle)
}

// Insert the new row, returning the primary key value of the new row
val newRowId = db?.insert(FeedEntry.TABLE_NAME, null, values)
```

### Read information from a database
```kotlin
val db = dbHelper.readableDatabase

// Define a projection that specifies which columns from the database
// you will actually use after this query.
val projection = arrayOf(BaseColumns._ID, FeedEntry.COLUMN_NAME_TITLE, FeedEntry.COLUMN_NAME_SUBTITLE)

// Filter results WHERE "title" = 'My Title'
val selection = "${FeedEntry.COLUMN_NAME_TITLE} = ?"
val selectionArgs = arrayOf("My Title")

// How you want the results sorted in the resulting Cursor
val sortOrder = "${FeedEntry.COLUMN_NAME_SUBTITLE} DESC"

val cursor = db.query(
        FeedEntry.TABLE_NAME,   // The table to query
        projection,             // The array of columns to return (pass null to get all)
        selection,              // The columns for the WHERE clause
        selectionArgs,          // The values for the WHERE clause
        null,                   // don't group the rows
        null,                   // don't filter by row groups
        sortOrder               // The sort order
)
```

### Read information from a database
```kotlin
val itemIds = mutableListOf<Long>()
with(cursor) {
    while (moveToNext()) {
        val itemId = getLong(getColumnIndexOrThrow(BaseColumns._ID))
        itemIds.add(itemId)
    }
}
cursor.close()
```

### Delete information from a database
```kotlin
// Define 'where' part of query.
val selection = "${FeedEntry.COLUMN_NAME_TITLE} LIKE ?"
// Specify arguments in placeholder order.
val selectionArgs = arrayOf("MyTitle")
// Issue SQL statement.
val deletedRows = db.delete(FeedEntry.TABLE_NAME, selection, selectionArgs)
```

### Update a database
```kotlin
val db = dbHelper.writableDatabase

// New value for one column
val title = "MyNewTitle"
val values = ContentValues().apply {
    put(FeedEntry.COLUMN_NAME_TITLE, title)
}

// Which row to update, based on the title
val selection = "${FeedEntry.COLUMN_NAME_TITLE} LIKE ?"
val selectionArgs = arrayOf("MyOldTitle")
val count = db.update(
        FeedEntry.TABLE_NAME,
        values,
        selection,
        selectionArgs)
```

### Persisting database connection
```kotlin
override fun onDestroy() {
    dbHelper.close()
    super.onDestroy()
}
```

### Open a document file
```
startActivityForResult(
        Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
            addCategory(Intent.CATEGORY_OPENABLE)
            type = "*/*"
            putExtra(Intent.EXTRA_MIME_TYPES, arrayOf(
                    "application/pdf", // .pdf
                    "application/vnd.oasis.opendocument.text", // .odt
                    "text/plain" // .txt
            ))
        },
        REQUEST_CODE
      )
```

### Opt out in your tests
```
-e no-isolated-storage 1
```

### Opt out in your production app
```xml
<manifest ... >
  <!-- This attribute is "false" by default on apps targeting
       Android 10. -->
  <application android:requestLegacyExternalStorage="true" ... >
    ...
  </application>
</manifest>
```

### Jetpack library dependency
```kotlin
// For apps using Jetpack Compose
implementation("androidx.photopicker:photopicker-compose:1.0.0-alpha01")

// For apps using Views
implementation("androidx.photopicker:photopicker:1.0.0-alpha01")
```

### Jetpack Compose integration
```kotlin
val coroutineScope = rememberCoroutineScope()
val pickerState = rememberEmbeddedPhotoPickerState()

EmbeddedPhotoPicker(
    state = pickerState,
    onUriPermissionGranted = { uris ->
        _attachments.value += uris
    },
    onUriPermissionRevoked = { uris ->
        _attachments.value -= uris
    },
    onSelectionComplete = {
        // Hide the embedded photo picker as the user is done with the
        // photo/video selection
    },
)
```

### Continuous selection
```kotlin
coroutineScope.launch {
    // Signal unselected media to the picker
    pickerState.deselectUris(uris)
    // Remove them from the list of selected media to be reflected in the app's UI
    _attachments.value -= uris
}
```

### Accent color
```kotlin
val info = EmbeddedPhotoPickerFeatureInfo.Builder().setAccentColor(0xFF0000).build()

EmbeddedPhotoPicker(
    embeddedPhotoPickerFeatureInfo = info,
    ...
)
```

### Dimensions
```
EmbeddedPhotoPicker(
    modifier = Modifier.height(500.dp),
    ...
)
```

### Views integration
```xml
<view class="androidx.photopicker.EmbeddedPhotoPickerView"
    android:id="@+id/photopicker"
    android:layout_width="match_parent"
    android:layout_height="match_parent" />
```

### Views integration
```kotlin
// Keep track of the selected media
private val _attachments = MutableStateFlow(emptyList<Uri>())
val attachments = _attachments.asStateFlow()

private lateinit var picker: EmbeddedPhotoPickerView
private var openSession: EmbeddedPhotoPickerSession? = null

val pickerListener = object : EmbeddedPhotoPickerStateChangeListener {
    override fun onSessionOpened(newSession: EmbeddedPhotoPickerSession) {
        // Keep reference to the session to notify the embedded picker of user
        // interactions on the calling app
        openSession = newSession
    }

    override fun onSessionError(throwable: Throwable) {}

    override fun onUriPermissionGranted(uris: List<Uri>) {
        // Add newly selected media to our tracked list
        _attachments += uris
    }

    override fun onUriPermissionRevoked(uris: List<Uri>) {
        // Remove newly unselected media from our tracked list
        _attachments -= uris
    }

    override fun onSelectionComplete() {
        // Hide the embedded photo picker as the user is done with the
        // photo/video selection
    }
}

override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)

    setContentView(R.layout.main_view)
    picker = findViewById(R.id.photopicker)

    // Attach the embedded picker event listener to update the app's UI
    picker.addEmbeddedPhotoPickerStateChangeListener(pickerListener)

    // Customize embedded picker's features: accent color, max selectable items,
    // pre-selected URIs, filter out mime types
    picker.setEmbeddedPhotoPickerFeatureInfo(
        // Set a custom accent color
        EmbeddedPhotoPickerFeatureInfo.Builder().setAccentColor(0xFF0000).build()
    )
}
```

### Views integration
```
// Notify the embedded picker of a configuration change
openSession.notifyConfigurationChanged(newConfig)

// Update the embedded picker to expand following a user interaction
openSession.notifyPhotoPickerExpanded(/* expanded: */ true)

// Resize the embedded picker
openSession.notifyResized(/* width: */ 512, /* height: */ 256)

// Show/hide the embedded picker (after a form has been submitted)
openSession.notifyVisibilityChanged(/* visible: */ false)

// Remove unselected media from the embedded picker after they have been
// unselected from the host app's UI
openSession.requestRevokeUriPermission(removedUris)
```

### Dataset available
```kotlin
val blobStoreManager =
        getSystemService(Context.BLOB_STORE_SERVICE) as BlobStoreManager
// The label "Sample photos" is visible to the user.
val blobHandle = BlobHandle.createWithSha256(sha256DigestBytes,
        "Sample photos",
        System.currentTimeMillis() + TimeUnit.DAYS.toMillis(1),
        "photoTrainingDataset")
try {
    val input = ParcelFileDescriptor.AutoCloseInputStream(
            blobStoreManager.openBlob(blobHandle))
    useDataset(input)
}
```

### Dataset unavailable
```kotlin
val sessionId = blobStoreManager.createSession(blobHandle)
try {
    val session = blobStoreManager.openSession(sessionId)
    try {
        // For this example, write 200 MiB at the beginning of the file.
        val output = ParcelFileDescriptor.AutoCloseOutputStream(
                session.openWrite(0, 1024 * 1024 * 200))
        writeDataset(output)

        session.apply {
            allowSameSignatureAccess()
            allowPackageAccess(your-app-package,
                    app-certificate)
            allowPackageAccess(some-other-app-package,
                    app-certificate)
            commit(mainExecutor, callback)
        }
    }
}
```

### Setup
```kotlin
dependencies {
    val room_version = "2.8.4"

    implementation("androidx.room:room-runtime:$room_version")

    // If this project uses any Kotlin source, use Kotlin Symbol Processing (KSP)
    // See Add the KSP plugin to your project
    ksp("androidx.room:room-compiler:$room_version")

    // If this project only uses Java source, use the Java annotationProcessor
    // No additional plugins are necessary
    annotationProcessor("androidx.room:room-compiler:$room_version")

    // optional - Kotlin Extensions and Coroutines support for Room
    implementation("androidx.room:room-ktx:$room_version")

    // optional - RxJava2 support for Room
    implementation("androidx.room:room-rxjava2:$room_version")

    // optional - RxJava3 support for Room
    implementation("androidx.room:room-rxjava3:$room_version")

    // optional - Guava support for Room, including Optional and ListenableFuture
    implementation("androidx.room:room-guava:$room_version")

    // optional - Test helpers
    testImplementation("androidx.room:room-testing:$room_version")

    // optional - Paging 3 Integration
    implementation("androidx.room:room-paging:$room_version")
}
```

### Data entity
```kotlin
@Entity
data class User(
    @PrimaryKey val uid: Int,
    @ColumnInfo(name = "first_name") val firstName: String?,
    @ColumnInfo(name = "last_name") val lastName: String?
)
```

### Data access object (DAO)
```kotlin
@Dao
interface UserDao {
    @Query("SELECT * FROM user")
    fun getAll(): List<User>

    @Query("SELECT * FROM user WHERE uid IN (:userIds)")
    fun loadAllByIds(userIds: IntArray): List<User>

    @Query("SELECT * FROM user WHERE first_name LIKE :first AND " +
           "last_name LIKE :last LIMIT 1")
    fun findByName(first: String, last: String): User

    @Insert
    fun insertAll(vararg users: User)

    @Delete
    fun delete(user: User)
}
```

### Database
```kotlin
@Database(entities = [User::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao
}
```

### Usage
```kotlin
val db = Room.databaseBuilder(
            applicationContext,
            AppDatabase::class.java, "database-name"
        ).build()
```

### Usage
```kotlin
val userDao = db.userDao()
val users: List<User> = userDao.getAll()
```

### Anatomy of an entity
```kotlin
@Entity
data class User(
    @PrimaryKey val id: Int,

    val firstName: String?,
    val lastName: String?
)
```

### Anatomy of an entity
```kotlin
@Entity(tableName = "users")
data class User (
    @PrimaryKey val id: Int,
    @ColumnInfo(name = "first_name") val firstName: String?,
    @ColumnInfo(name = "last_name") val lastName: String?
)
```

### Define a primary key
```kotlin
@PrimaryKey val id: Int
```

### Define a composite primary key
```kotlin
@Entity(primaryKeys = ["firstName", "lastName"])
data class User(
    val firstName: String?,
    val lastName: String?
)
```

### Ignore fields
```kotlin
@Entity
data class User(
    @PrimaryKey val id: Int,
    val firstName: String?,
    val lastName: String?,
    @Ignore val picture: Bitmap?
)
```

### Ignore fields
```kotlin
open class User {
    var picture: Bitmap? = null
}

@Entity(ignoredColumns = ["picture"])
data class RemoteUser(
    @PrimaryKey val id: Int,
    val hasVpn: Boolean
) : User()
```

### Support full-text search
```kotlin
// Use `@Fts3` only if your app has strict disk space requirements or if you
// require compatibility with an older SQLite version.
@Fts4
@Entity(tableName = "users")
data class User(
    /* Specifying a primary key for an FTS-table-backed entity is optional, but
       if you include one, it must use this type and column name. */
    @PrimaryKey @ColumnInfo(name = "rowid") val id: Int,
    @ColumnInfo(name = "first_name") val firstName: String?
)
```

### Support full-text search
```kotlin
@Fts4(languageId = "lid")
@Entity(tableName = "users")
data class User(
    // ...
    @ColumnInfo(name = "lid") val languageId: Int
)
```

### Index specific columns
```kotlin
@Entity(indices = [Index(value = ["last_name", "address"])])
data class User(
    @PrimaryKey val id: Int,
    val firstName: String?,
    val address: String?,
    @ColumnInfo(name = "last_name") val lastName: String?,
    @Ignore val picture: Bitmap?
)
```

### Index specific columns
```kotlin
@Entity(indices = [Index(value = ["first_name", "last_name"],
        unique = true)])
data class User(
    @PrimaryKey val id: Int,
    @ColumnInfo(name = "first_name") val firstName: String?,
    @ColumnInfo(name = "last_name") val lastName: String?,
    @Ignore var picture: Bitmap?
)
```

### Include AutoValue-based objects
```
@AutoValue
@Entity
public abstract class User {
    // Supported annotations must include `@CopyAnnotations`.
    @CopyAnnotations
    @PrimaryKey
    public abstract long getId();

    public abstract String getFirstName();
    public abstract String getLastName();

    // Room uses this factory method to create User objects.
    public static User create(long id, String firstName, String lastName) {
        return new AutoValue_User(id, firstName, lastName);
    }
}
```

### Anatomy of a DAO
```kotlin
@Dao
interface UserDao {
    @Insert
    fun insertAll(vararg users: User)

    @Delete
    fun delete(user: User)

    @Query("SELECT * FROM user")
    fun getAll(): List<User>
}
```

### Insert
```kotlin
@Dao
interface UserDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    fun insertUsers(vararg users: User)

    @Insert
    fun insertBothUsers(user1: User, user2: User)

    @Insert
    fun insertUsersAndFriends(user: User, friends: List<User>)
}
```

### Update
```kotlin
@Dao
interface UserDao {
    @Update
    fun updateUsers(vararg users: User)
}
```

### Delete
```kotlin
@Dao
interface UserDao {
    @Delete
    fun deleteUsers(vararg users: User)
}
```

### Simple queries
```kotlin
@Query("SELECT * FROM user")
fun loadAllUsers(): Array<User>
```

### Return a subset of a table's columns
```kotlin
data class NameTuple(
    @ColumnInfo(name = "first_name") val firstName: String?,
    @ColumnInfo(name = "last_name") val lastName: String?
)
```

### Return a subset of a table's columns
```kotlin
@Query("SELECT first_name, last_name FROM user")
fun loadFullName(): List<NameTuple>
```

### Pass simple parameters to a query
```kotlin
@Query("SELECT * FROM user WHERE age > :minAge")
fun loadAllUsersOlderThan(minAge: Int): Array<User>
```

### Pass simple parameters to a query
```kotlin
@Query("SELECT * FROM user WHERE age BETWEEN :minAge AND :maxAge")
fun loadAllUsersBetweenAges(minAge: Int, maxAge: Int): Array<User>

@Query("SELECT * FROM user WHERE first_name LIKE :search " +
       "OR last_name LIKE :search")
fun findUserWithName(search: String): List<User>
```

### Pass a collection of parameters to a query
```kotlin
@Query("SELECT * FROM user WHERE region IN (:regions)")
fun loadUsersFromRegions(regions: List<String>): List<User>
```

### Query multiple tables
```kotlin
@Query(
    "SELECT * FROM book " +
    "INNER JOIN loan ON loan.book_id = book.id " +
    "INNER JOIN user ON user.id = loan.user_id " +
    "WHERE user.name LIKE :userName"
)
fun findBooksBorrowedByNameSync(userName: String): List<Book>
```

### Query multiple tables
```kotlin
interface UserBookDao {
    @Query(
        "SELECT user.name AS userName, book.name AS bookName " +
        "FROM user, book " +
        "WHERE user.id = book.user_id"
    )
    fun loadUserAndBookNames(): LiveData<List<UserBook>>

    // You can also define this class in a separate file.
    data class UserBook(val userName: String?, val bookName: String?)
}
```

### Return a multimap
```kotlin
@Query(
    "SELECT * FROM user" +
    "JOIN book ON user.id = book.user_id"
)
fun loadUserAndBookNames(): Map<User, List<Book>>
```

### Return a multimap
```kotlin
@MapInfo(keyColumn = "userName", valueColumn = "bookName")
@Query(
    "SELECT user.name AS username, book.name AS bookname FROM user" +
    "JOIN book ON user.id = book.user_id"
)
fun loadUserAndBookNames(): Map<String, List<String>>
```

### Paginated queries with the Paging library
```kotlin
@Dao
interface UserDao {
  @Query("SELECT * FROM users WHERE label LIKE :query")
  fun pagingSource(query: String): PagingSource<Int, User>
}
```

### Direct cursor access
```kotlin
@Dao
interface UserDao {
    @Query("SELECT * FROM user WHERE age > :minAge LIMIT 5")
    fun loadRawUsersOlderThan(minAge: Int): Cursor
}
```

### Use the intermediate data class approach
```kotlin
@Dao
interface UserBookDao {
    @Query(
        "SELECT user.name AS userName, book.name AS bookName " +
        "FROM user, book " +
        "WHERE user.id = book.user_id"
    )
    fun loadUserAndBookNames(): LiveData<List<UserBook>>
}

data class UserBook(val userName: String?, val bookName: String?)
```

### Create embedded objects
```kotlin
data class Address(
    val street: String?,
    val state: String?,
    val city: String?,
    @ColumnInfo(name = "post_code") val postCode: Int
)

@Entity
data class User(
    @PrimaryKey val id: Int,
    val firstName: String?,
    @Embedded val address: Address?
)
```

### Define the relationship
```kotlin
@Entity
data class User(
    @PrimaryKey val userId: Long,
    val name: String,
    val age: Int
)

@Entity
data class Library(
    @PrimaryKey val libraryId: Long,
    val userOwnerId: Long
)
```

### Query the entities
```kotlin
data class UserAndLibrary(
    @Embedded val user: User,
    @Relation(
         parentColumn = "userId",
         entityColumn = "userOwnerId"
    )
    val library: Library
)
```

### Query the entities
```kotlin
@Transaction
@Query("SELECT * FROM User")
fun getUsersAndLibraries(): List<UserAndLibrary>
```

### Query the entities
```kotlin
data class UserWithPlaylists(
    @Embedded val user: User,
    @Relation(
          parentColumn = "userId",
          entityColumn = "userCreatorId"
    )
    val playlists: List<Playlist>
)
```

### Query the entities
```kotlin
@Transaction
@Query("SELECT * FROM User")
fun getUsersWithPlaylists(): List<UserWithPlaylists>
```

### Define the relationship
```kotlin
@Entity
data class Playlist(
    @PrimaryKey val playlistId: Long,
    val playlistName: String
)

@Entity
data class Song(
    @PrimaryKey val songId: Long,
    val songName: String,
    val artist: String
)

@Entity(primaryKeys = ["playlistId", "songId"])
data class PlaylistSongCrossRef(
    val playlistId: Long,
    val songId: Long
)
```

### Query the entities
```kotlin
data class PlaylistWithSongs(
    @Embedded val playlist: Playlist,
    @Relation(
         parentColumn = "playlistId",
         entityColumn = "songId",
         associateBy = Junction(PlaylistSongCrossRef::class)
    )
    val songs: List<Song>
)

data class SongWithPlaylists(
    @Embedded val song: Song,
    @Relation(
         parentColumn = "songId",
         entityColumn = "playlistId",
         associateBy = Junction(PlaylistSongCrossRef::class)
    )
    val playlists: List<Playlist>
)
```

### Query the entities
```kotlin
@Transaction
@Query("SELECT * FROM Playlist")
fun getPlaylistsWithSongs(): List<PlaylistWithSongs>

@Transaction
@Query("SELECT * FROM Song")
fun getSongsWithPlaylists(): List<SongWithPlaylists>
```

### Define and query nested relationships 

 
 
 
 

 
 
 Stay organized with collec
```kotlin
data class UserWithPlaylistsAndSongs(
    @Embedded val user: User
    @Relation(
        entity = Playlist::class,
        parentColumn = "userId",
        entityColumn = "userCreatorId"
    )
    val playlists: List<PlaylistWithSongs>
)
```

### Create a view
```kotlin
@DatabaseView("SELECT user.id, user.name, user.departmentId," +
        "department.name AS departmentName FROM user " +
        "INNER JOIN department ON user.departmentId = department.id")
data class UserDetail(
    val id: Long,
    val name: String?,
    val departmentId: Long,
    val departmentName: String?
)
```

### Associate a view with your database
```kotlin
@Database(entities = [User::class],
          views =[UserDetail::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao
}
```

### Prepopulate from an app asset
```
Room.databaseBuilder(appContext, AppDatabase::class.java, "Sample.db")
    .createFromAsset("database/myapp.db")
    .build()
```

### Example: Fallback migration with a prepackaged database
```
// Database class definition declaring version 3.
@Database(version = 3)
abstract class AppDatabase : RoomDatabase() {
    ...
}

// Destructive migrations are enabled and a prepackaged database
// is provided.
Room.databaseBuilder(appContext, AppDatabase::class.java, "Sample.db")
    .createFromAsset("database/myapp.db")
    .fallbackToDestructiveMigration()
    .build()
```

### Example: Multi-step migration with a prepackaged database
```kotlin
// Database class definition declaring version 4.
@Database(version = 4)
abstract class AppDatabase : RoomDatabase() {
    ...
}

// Migration path definition from version 3 to version 4.
val MIGRATION_3_4 = object : Migration(3, 4) {
    override fun migrate(database: SupportSQLiteDatabase) {
        ...
    }
}

// Destructive migrations are enabled and a prepackaged database is
// provided.
Room.databaseBuilder(appContext, AppDatabase::class.java, "Sample.db")
    .createFromAsset("database/myapp.db")
    .addMigrations(MIGRATION_3_4)
    .fallbackToDestructiveMigration()
    .build()
```

### Automated migrations
```
// Database class before the version update.
@Database(
  version = 1,
  entities = [User::class]
)
abstract class AppDatabase : RoomDatabase() {
  ...
}

// Database class after the version update.
@Database(
  version = 2,
  entities = [User::class],
  autoMigrations = [
    AutoMigration (from = 1, to = 2)
  ]
)
abstract class AppDatabase : RoomDatabase() {
  ...
}
```

### Automatic migration specifications
```
@Database(
  version = 2,
  entities = [User::class],
  autoMigrations = [
    AutoMigration (
      from = 1,
      to = 2,
      spec = AppDatabase.MyAutoMigration::class
    )
  ]
)
abstract class AppDatabase : RoomDatabase() {
  @RenameTable(fromTableName = "User", toTableName = "AppUser")
  class MyAutoMigration : AutoMigrationSpec
  ...
}
```

### Manual migrations
```kotlin
val MIGRATION_1_2 = object : Migration(1, 2) {
  override fun migrate(database: SupportSQLiteDatabase) {
    database.execSQL("CREATE TABLE `Fruit` (`id` INTEGER, `name` TEXT, " +
      "PRIMARY KEY(`id`))")
  }
}

val MIGRATION_2_3 = object : Migration(2, 3) {
  override fun migrate(database: SupportSQLiteDatabase) {
    database.execSQL("ALTER TABLE Book ADD COLUMN pub_year INTEGER")
  }
}

Room.databaseBuilder(applicationContext, MyDb::class.java, "database-name")
  .addMigrations(MIGRATION_1_2, MIGRATION_2_3).build()
```

### Set schema location using Room Gradle Plugin
```
plugins {
  id("androidx.room")
}

room {
  schemaDirectory("$projectDir/schemas")
}
```

### Set schema location using Room Gradle Plugin
```
room {
  // Applies to 'demoDebug' only
  schemaDirectory("demoDebug", "$projectDir/schemas/demoDebug")

  // Applies to 'demoDebug' and 'demoRelease'
  schemaDirectory("demo", "$projectDir/schemas/demo")

  // Applies to 'demoDebug' and 'fullDebug'
  schemaDirectory("debug", "$projectDir/schemas/debug")

  // Applies to variants that aren't matched by other configurations.
  schemaDirectory("$projectDir/schemas")
}
```

### Set schema location using annotation processor option
```kotlin
class RoomSchemaArgProvider(
  @get:InputDirectory
  @get:PathSensitive(PathSensitivity.RELATIVE)
  val schemaDir: File
) : CommandLineArgumentProvider {

  override fun asArguments(): Iterable<String> {
    // Note: If you're using KAPT and javac, change the line below to
    // return listOf("-Aroom.schemaLocation=${schemaDir.path}").
    return listOf("room.schemaLocation=${schemaDir.path}")
  }
}
```

### Set schema location using annotation processor option
```
// For KSP, configure using KSP extension:
ksp {
  arg(RoomSchemaArgProvider(File(projectDir, "schemas")))
}

// For javac or KAPT, configure using android DSL:
android {
  ...
  defaultConfig {
    javaCompileOptions {
      annotationProcessorOptions {
        compilerArgumentProviders(
          RoomSchemaArgProvider(File(projectDir, "schemas"))
        )
      }
    }
  }
}
```

### Test a single migration
```
android {
    ...
    sourceSets {
        // Adds exported schema location as test app assets.
        getByName("androidTest").assets.srcDir("$projectDir/schemas")
    }
}

dependencies {
    ...
    testImplementation("androidx.room:room-testing:2.8.4")
}
```

### Test a single migration
```kotlin
@RunWith(AndroidJUnit4::class)
class MigrationTest {
    private val TEST_DB = "migration-test"

    @get:Rule
    val helper: MigrationTestHelper = MigrationTestHelper(
            InstrumentationRegistry.getInstrumentation(),
            MigrationDb::class.java.canonicalName,
            FrameworkSQLiteOpenHelperFactory()
    )

    @Test
    @Throws(IOException::class)
    fun migrate1To2() {
        var db = helper.createDatabase(TEST_DB, 1).apply {
            // Database has schema version 1. Insert some data using SQL queries.
            // You can't use DAO classes because they expect the latest schema.
            execSQL(...)

            // Prepare for the next version.
            close()
        }

        // Re-open the database with version 2 and provide
        // MIGRATION_1_2 as the migration process.
        db = helper.runMigrationsAndValidate(TEST_DB, 2, true, MIGRATION_1_2)

        // MigrationTestHelper automatically verifies the schema changes,
        // but you need to validate that the data was migrated properly.
    }
}
```

### Gracefully handle missing migration paths
```
Room.databaseBuilder(applicationContext, MyDb::class.java, "database-name")
        .fallbackToDestructiveMigration()
        .build()
```

### Handle column default values when upgrading to Room 2.2.0
```kotlin
// Song entity, database version 1, Room 2.1.0.
@Entity
data class Song(
    @PrimaryKey
    val id: Long,
    val title: String
)
```

### Handle column default values when upgrading to Room 2.2.0
```kotlin
// Song entity, database version 2, Room 2.1.0.
@Entity
data class Song(
    @PrimaryKey
    val id: Long,
    val title: String,
    val tag: String // Added in version 2.
)

// Migration from 1 to 2, Room 2.1.0.
val MIGRATION_1_2 = object : Migration(1, 2) {
    override fun migrate(database: SupportSQLiteDatabase) {
        database.execSQL(
            "ALTER TABLE Song ADD COLUMN tag TEXT NOT NULL DEFAULT ''")
    }
}
```

### Handle column default values when upgrading to Room 2.2.0
```kotlin
// Migration from 2 to 3, Room 2.2.0.
val MIGRATION_2_3 = object : Migration(2, 3) {
    override fun migrate(database: SupportSQLiteDatabase) {
        database.execSQL("""
                CREATE TABLE new_Song (
                    id INTEGER PRIMARY KEY NOT NULL,
                    name TEXT,
                    tag TEXT NOT NULL DEFAULT ''
                )
                """.trimIndent())
        database.execSQL("""
                INSERT INTO new_Song (id, name, tag)
                SELECT id, name, tag FROM Song
                """.trimIndent())
        database.execSQL("DROP TABLE Song")
        database.execSQL("ALTER TABLE new_Song RENAME TO Song")
    }
}
```

### Test on an Android device
```kotlin
@RunWith(AndroidJUnit4::class)
class SimpleEntityReadWriteTest {
    private lateinit var userDao: UserDao
    private lateinit var db: TestDatabase

    @Before
    fun createDb() {
        val context = ApplicationProvider.getApplicationContext<Context>()
        db = Room.inMemoryDatabaseBuilder(
                context, TestDatabase::class.java).build()
        userDao = db.getUserDao()
    }

    @After
    @Throws(IOException::class)
    fun closeDb() {
        db.close()
    }

    @Test
    @Throws(Exception::class)
    fun writeUserAndReadInList() {
        val user: User = TestUtil.createUser(3).apply {
            setName("george")
        }
        userDao.insert(user)
        val byName = userDao.findUsersByName("george")
        assertThat(byName.get(0), equalTo(user))
    }
}
```

### Dump data from the command line
```
adb -s emulator-5554 shell
sqlite3 /data/data/your-app-package/databases/rssitems.db
```

### Use type converters
```kotlin
class Converters {
  @TypeConverter
  fun fromTimestamp(value: Long?): Date? {
    return value?.let { Date(it) }
  }

  @TypeConverter
  fun dateToTimestamp(date: Date?): Long? {
    return date?.time?.toLong()
  }
}
```

### Use type converters
```kotlin
@Database(entities = [User::class], version = 1)
@TypeConverters(Converters::class)
abstract class AppDatabase : RoomDatabase() {
  abstract fun userDao(): UserDao
}
```

### Use type converters
```kotlin
@Entity
data class User(private val birthday: Date?)

@Dao
interface UserDao {
  @Query("SELECT * FROM user WHERE birthday = :targetDate")
  fun findUsersBornOnDate(targetDate: Date): List<User>
}
```

### Control type converter initialization
```kotlin
@ProvidedTypeConverter
class ExampleConverter {
  @TypeConverter
  fun StringToExample(string: String?): ExampleType? {
    ...
  }

  @TypeConverter
  fun ExampleToString(example: ExampleType?): String? {
    ...
  }
}
```

### Control type converter initialization
```kotlin
val db = Room.databaseBuilder(...)
  .addTypeConverter(exampleConverterInstance)
  .build()
```

### Understand why Room doesn't allow object references
```
authorNameTextView.text = book.author.name
```

### Update model classes to data entities
```kotlin
@Entity(tableName = "users")
data class User(
  @PrimaryKey
  @ColumnInfo(name = "userid") val mId: String,
  @ColumnInfo(name = "username") val mUserName: String?,
  @ColumnInfo(name = "last_update") val mDate: Date?,
)
```

### Create a database class
```kotlin
@Database(entities = [User::class], version = 2)
@TypeConverters(DateConverter::class)
abstract class UsersDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao
}
```

### Update the database instantiation
```kotlin
val db = Room.databaseBuilder(
          applicationContext,
          AppDatabase::class.java, "database-name"
        )
          .addMigrations(MIGRATION_1_2).build()
```

## Pitfalls
- Caution: 
 
 The exact location of where your files can be saved might vary across
devices. For this reason, don't use hard-coded file paths. 
 To avoid accidental disclosure of information, don't use predictable
 patterns to filenames in ways that could reveal the kinds of information
 found within
- Caution: On devices that run Android 7.0 (API level 24) or higher, unless you
pass the Context.MODE_PRIVATE file mode into openFileOutput() , a
 SecurityException occurs.
- Caution: When the device is low on internal storage space, Android may delete
these cache files to recover space. So check for the existence of your cache
files before reading them.
- Caution: The files in these directories aren't guaranteed to be accessible, such
as when a removable SD card is taken out of the device. If your app's
functionality depends on these files, you should instead store the files within
 internal storage .
- Note: You aren't required to check the amount of available space before you save
your file. You can instead try writing the file right away, then catch an
 IOException if one occurs. You may need to
do this if you don't know exactly how much space you need. For example, if you
change the file's enco
- Caution: The ACTION_CLEAR_APP_CACHE intent action can substantially affect
device battery life and might remove a large number of files from the device.
- Caution: Because you request the ACCESS_MEDIA_LOCATION permission at runtime,
there is no guarantee that your app has access to unredacted EXIF metadata from
photos. Your app requires explicit user consent to gain access to this
information.
- Caution: Before you rely on the value of getGeneration() , check the media
store for updates . If the media store version has changed,
perform a full synchronization pass.
- Caution: If you iterate through a large number of files within the directory
that's accessed using ACTION_OPEN_DOCUMENT_TREE , your app's performance might
be reduced.
- Caution: Even after calling takePersistableUriPermission() , your app doesn't
retain access to the URI if the associated document is moved or deleted. In
those cases, you need to ask permission again to regain access to the URI.
- Note: Because an app cannot directly open a virtual file by using the
 openInputStream() 
method, don't use the
 CATEGORY_OPENABLE 
category when creating the intent that contains the ACTION_OPEN_DOCUMENT or
 ACTION_OPEN_DOCUMENT_TREE action.
- Caution: DataStore is a modern data storage solution that you should use
instead of SharedPreferences . It builds on Kotlin coroutines and Flow, and
overcomes many of the drawbacks of SharedPreferences .
 Read the DataStore guide for more information.
- Caution: The MODE_WORLD_READABLE and MODE_WORLD_WRITEABLE modes
have been deprecated since API level 17.
 Starting with Android 7.0 (API level 24), Android throws a
 SecurityException if you use them. If your app needs to share private
files with other apps, it may use a FileProvider with the
 FLAG_
  WHY: API level 17
- Note: To avoid cluttering, use generally accessible locations like externalStoragePublicDirectory() or externalMediaDirs() .
- Note: The files in app-scoped storage don't persist after your app is
uninstalled.
- Caution: After you update your app to target Android 11 (API level 30), the
system ignores the requestLegacyExternalStorage 
attribute when your app is
running on Android 11 devices, so your app must be ready
to support scoped storage and to migrate app data 
for users on those devices.
- Note: Choose only one of ksp or annotationProcessor . Don't include both.
- Caution: We don't recommend using the Cursor API, because it doesn't
guarantee that the rows exist or what values the rows contain. Only use this
functionality if you already have code that expects a cursor and that you can't
refactor easily.
- Caution: Querying data with nested relationships requires Room to manipulate a
large volume of data and can affect performance. Use as few nested relationships
as possible in your queries.
- Note: In-memory Room databases don't support prepopulating the database
using createFromAsset() or createFromFile() .
- Caution: To keep your migration logic functioning as expected, use full queries
instead of referencing constants that represent the queries.
- Warning: Setting this option in your app's database builder means that Room
 permanently deletes all data from the tables in the user's database when it
attempts to perform a migration and there is no defined migration path.
- Note: When running tests for your app, Room allows you to create mock instances
of your DAO classes. That way,
you don't need to create a full database if you aren't testing the database
itself. This functionality is possible because your DAOs don't leak any details
of your database.
- Note: Room 2.3 and higher includes a default type converter for persisting
enums. Existing type converters take precedence over the default, but if you
have not already defined a type converter for enums then you don't need to
define one.

## Decision Tables
### Data and file storage overview 

 
 
 
 

 
 
 Stay organized with collections
 
 
 
 Save and categorize content based on your preferences.
|  | Type of content | Access method | Permissions needed | Can other apps access? | Files removed on app uninstall? |
| --- | --- | --- | --- | --- | --- |
| App-specific
 files | Files meant for your app's use only | From internal storage, getFilesDir() or
 getCacheDir() From external storage,
 getExternalFilesDir() or
 getExternalCacheDir() | Never needed for internal storage Not needed for external
 storage when your app is used on devices that run Android 4.4 (API level 19)
 or higher | No | Yes |
| Media | Shareable media files (images, audio files, videos) | MediaStore API | READ_EXTERNAL_STORAGE when accessing other apps' files on
 Android 11 (API level 30) or higher 
 READ_EXTERNAL_STORAGE or WRITE_EXTERNAL_STORAGE 
 when accessing other apps' files on Android 10 (API level 29) 
 Permissions are required for all files on Android 9 (API level 28) or
 lower | Yes, though the other app needs the READ_EXTERNAL_STORAGE 
 permission | No |
| Documents and
 other files | Other types of shareable content, including downloaded files | Storage Access Framework | None | Yes, through the system file picker | No |
| App
 preferences | Key-value pairs | Jetpack
 Preferences library | None | No | Yes |
| Database | Structured data | Room persistence library | None | No | Yes |

### Handle media files
| Use case | Summary |
| --- | --- |
| Show all image or video files | Use the same approach for all versions of Android. |
| Show images or videos from a particular
 folder | Use the same approach for all versions of Android. |
| Access location information from
 photos | Use one approach if your app uses scoped storage. Use a different
 approach if your app opts out of scoped storage. |
| Define storage location for new downloads | Use one approach if your app uses scoped storage. Use a different
 approach if your app opts out of scoped storage. |
| Export user media files to a device | Use the same approach for all versions of Android. |
| Modify or delete multiple media files in
 a single operation | Use one approach for Android 11. For Android 10, opt out of scoped
 storage and use the approach for Android 9 and lower instead. |
| Import a single image that already
 exists | Use the same approach for all versions of Android. |
| Capture a single image | Use the same approach for all versions of Android. |
| Share media files with other apps | Use the same approach for all versions of Android. |
| Share media files with a specific app | Use the same approach for all versions of Android. |
| Access files from code or libraries
 that use direct file paths | Use one approach for Android 11. For Android 10, opt out of scoped
 storage and use the approach for Android 9 and lower instead. |

### Handle non-media files
| Use case | Summary |
| --- | --- |
| Open a document file | Use the same approach for all versions of Android. |
| Write to files on
 secondary storage volumes | Use one approach for Android 11. Use a different approach for earlier
 versions of Android. |
| Migrate existing files from a legacy
 storage location | Migrate your files to scoped storage when possible. Opt out of scoped
 storage for Android 10 when necessary. |
| Share content with other
 apps | Use the same approach for all versions of Android. |
| Cache non-media files | Use the same approach for all versions of Android. |
| Export non-media files to a device | Use one approach if your app uses scoped storage. Use a different
 approach if your app opts out of scoped storage. |

### Accent color
| Without setting accent color | With accent color (peak) | With accent color (expanded) |
| --- | --- | --- |
|  |  |  |

### Dimensions
| Without limit (expanded) | With 500 dp limit (expanded) |
| --- | --- |
|  |  |

### Language and framework options
| Query type | Kotlin language features | RxJava | Guava | Jetpack Lifecycle |
| --- | --- | --- | --- | --- |
| One-shot write | Coroutines ( suspend ) | Single<T> , Maybe<T> ,
 Completable | ListenableFuture<T> | N/A |
| One-shot read | Coroutines ( suspend ) | Single<T> , Maybe<T> | ListenableFuture<T> | N/A |
| Observable read | Flow<T> | Flowable<T> , Publisher<T> ,
 Observable<T> | N/A | LiveData<T> |

## Guidelines
- App-specific storage: Store files that are meant for your app's use only,
either in dedicated directories within an internal storage volume or different
dedicated directories within external storage. Use the directories within
internal storage to save sensitive information that other apps shouldn't access.
- Android provides two types of physical storage locations: internal storage and
 external storage . On most devices, internal storage is smaller than external
storage. However, internal storage is always available on all devices, making it
a more reliable place to put data on which your app depends.
- Android 11 introduces the MANAGE_EXTERNAL_STORAGE permission, which provides
write access to files outside the app-specific directory and MediaStore . To
learn more about this permission, and why most apps don't need to declare it to
fulfill their use cases, see the guide on how to manage all
files on a storage device.
- To prepare your app for scoped storage, view the storage use cases and best
practices guide. If your app has another use
case that isn't covered by scoped storage, file a feature
request . You can
 temporarily opt-out of using scoped
storage .
- To view the files stored on a device, use Android Studio's Device File
Explorer .
- In many cases, your app creates files that other apps don't need to access, or
shouldn't access. The system provides the following locations for storing such
 app-specific files:
- Keep in mind, however, that these directories tend to be small. Before writing
app-specific files to internal storage, your app should query the free
space on the device.
- You can use the File API to access and store files.
- To help maintain your app's performance, don't open and close the same
file multiple times.
- The following code snippet demonstrates how to use the File API:
- To read a file as a stream, use
 openFileInput() :
- Note: If you need to access a file as a stream at install time, save the file in
your project's /res/raw directory. You can open these files with
 openRawResource() ,
passing in the filename prefixed with R.raw as the resource ID. This method
returns an InputStream that you can use to
read the file. You cannot write to the original file.
- Note: dataDir 
is always an ancestor directory of this new directory.
- To remove a file from the cache directory within internal storage, use one of
the following methods:
- adb shell sm set-virtual-disk true
 

 Select a physical storage location 

 Sometimes, a device that allocates a partition of its internal memory as
external storage also provides an SD card slot. This means that the device has
multiple physical volumes that could contain external storage, so you need to
select which one to use for your app-specific storage.
- To access the different locations, call
 ContextCompat.getExternalFilesDirs() .
As shown in the code snippet, the first element in the returned array is
considered the primary external storage volume. Use this volume unless it's full
or unavailable.
- val externalCacheFile = File ( context . externalCacheDir , filename ) 
 Java 
 File externalCacheFile = new File ( context . getExternalCacheDir (), filename ); 
 
 

 Remove cache files 

 To remove a file from the external cache directory, use the
 delete() method on a File object that
represents the file:
- Many users don't have much storage space available on their devices, so your app
should consume space thoughtfully.
- To request that the user choose files on the device to remove, invoke an intent
that includes the
 ACTION_MANAGE_STORAGE 
action. This intent displays a prompt to the user. If desired, this prompt can
show the amount of free space available on the device. To show this
user-friendly information, use the result of the following calculation:
- Documents and other files: The system has a special directory for
containing other file types, such as PDF documents and books that use the EPUB
format. Your app can access these files using the platform's Storage Access
Framework.

## Concepts (for graph)
- App-specific storage:
- Shared storage:
- Preferences:
- Databases:
- Categories of storage locations
- Permissions and access to external storage
- Scoped storage
- View files on a device
- Additional resources
- Videos
- Internal storage directories:
- External storage directories:
