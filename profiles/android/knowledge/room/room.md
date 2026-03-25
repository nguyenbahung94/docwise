<!-- Source: https://developer.android.com/training/data-storage/room -->
<!-- Source: https://developer.android.com/training/data-storage/room/defining-data -->
<!-- Source: https://developer.android.com/training/data-storage/room/accessing-data -->
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
<!-- Type: official -->
<!-- Priority: high -->
<!-- Topic: room -->
<!-- Extracted: 2026-03-24 -->
<!-- Verified: — -->

# Save data in a local database using Room

## Rules
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

## Pitfalls
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
### Language and framework options
| Query type | Kotlin language features | RxJava | Guava | Jetpack Lifecycle |
| --- | --- | --- | --- | --- |
| One-shot write | Coroutines ( suspend ) | Single<T> , Maybe<T> ,
 Completable | ListenableFuture<T> | N/A |
| One-shot read | Coroutines ( suspend ) | Single<T> , Maybe<T> | ListenableFuture<T> | N/A |
| Observable read | Flow<T> | Flowable<T> , Publisher<T> ,
 Observable<T> | N/A | LiveData<T> |

## Guidelines
- Apps that handle non-trivial amounts of structured data can benefit greatly from
persisting that data locally. The most common use case is to cache relevant
pieces of data so that when the device cannot access the network, the user can
still browse that content while they are offline.
- Because of these considerations, we highly recommend that you use Room instead
of using the SQLite APIs directly .
- To use Room in your app, add the following dependencies to your app's
 build.gradle file.
- Data access objects (DAOs) that
provide methods that your app can use to query, update, insert, and delete
data in the database.
- The following code defines an AppDatabase class to hold the database.
 AppDatabase defines the database configuration and serves as the app's main
access point to the persisted data. The database class must satisfy the
following conditions:
- The class must be annotated with a
 @Database annotation that
includes an entities 
array that lists all of the data entities associated with the database.
- The class must be an abstract class that extends
 RoomDatabase .
- For each DAO class that is associated with the database, the database class
must define an abstract method that has zero arguments and returns an instance
of the DAO class.
- After you have defined the data entity, the DAO, and the database object, you
can use the following code to create an instance of the database:
- When you use the Room persistence library to
store your app's data, you define entities to represent the objects that you
want to store. Each entity corresponds to a table in the associated Room
database, and each instance of an entity represents a row of data in the
corresponding table.
- That means that you can use Room entities to define your database
schema without
writing any SQL code.
- Note: To persist a field, Room must have access to it. You can make sure Room
has access to a field either by making it public or by providing getter and
setter methods for it.
- If your app requires very quick access to database information through full-text
search (FTS), have your entities backed by a virtual table that uses either
the FTS3 or FTS4 SQLite extension
module . To use this capability,
available in Room 2.1.0 and higher, add the
 @Fts3 or
 @Fts4 annotation to a given entity, as shown
in the following code snippet:
- Note: FTS-enabled tables always use a primary key of type INTEGER and with the
column name "rowid" . If your FTS-table-backed entity defines a primary key, it
 must use that type and column name.
- Note: This capability is designed for use only in Java-based entities. To
achieve the same functionality in Kotlin-based entities, it's better to use
 data
classes 
instead.
- When using classes annotated with @AutoValue as entities, you can annotate the
class's abstract methods using @PrimaryKey , @ColumnInfo , @Embedded , and
 @Relation . When using these annotations, however, you must include the
 @CopyAnnotations annotation each time so that Room can interpret the methods'
auto-generated implementations properly.
- When you use the Room persistence library to store your app's data, you interact
with the stored data by defining data access objects , or DAOs. Each DAO
includes methods that offer abstract access to your app's database. At compile
time, Room automatically generates implementations of the DAOs that you define.
- You can define each DAO as either an interface or an abstract class. For basic
use cases, you usually use an interface. In either case, you must always
annotate your DAOs with @Dao . DAOs
don't have properties, but they do define one or more methods for interacting
with the data in your app's database.
- The following sections demonstrate how to use both types of DAO methods to
define the database interactions that your app needs.
- If you need to define more complex insertions, updates, or deletions, or if you need
to query the data in the database, use a query method instead.

## Core Concepts

1. **Data Access Objects (DAOs)**
   - Data access objects (DAOs) provide methods that your app can use to interact with data in the database, such as querying, updating, inserting, and deleting records. These methods are defined as abstract functions within a DAO interface or class.
     - **Entity → DAO**: Entities define the structure of tables; DAOs are used to interact with these entities via methods like `@Insert`, `@Update`, `@Delete`, and `@Query`.
     - **DAO → Database**: Methods in DAO classes are utilized by the database class to perform data operations such as inserting or querying. The database class, which extends `RoomDatabase` and is annotated with `@Database`, serves as a central access point for database interactions.

2. **Room Entity Management**
   - Room entity management involves defining entities that represent tables in your database. Entities define table schemas without requiring raw SQL and include annotations like `@Entity`, `@PrimaryKey`, `@ColumnInfo`, and `@Ignore`.
     - **Annotations**: These annotations are crucial for describing how the fields of an entity should be mapped to columns in a database.
       - `@Entity`: Marks a class as an entity, which is a table in your database.
       - `@PrimaryKey`: Indicates the primary key column that uniquely identifies each record in the table.
       - `@ColumnInfo`: Used for specifying custom column names if they differ from the property name or to add metadata like index or default values.
       - `@Ignore`: Fields annotated with `@Ignore` are not persisted and are excluded from table creation, which is useful for transient fields that don't need to be saved in the database.
     - **Primary Keys & Composite Keys**: Primary keys uniquely identify records within a table. When a single column cannot guarantee uniqueness, you can use composite primary keys by specifying multiple columns as part of `@Entity`.
     - **Ignored Fields**: Fields annotated with `@Ignore` are not persisted and are excluded from table creation.

3. **Database Migrations**
   - Database migrations ensure schema consistency across different app versions by managing changes to entities. They include automated migrations for simple schema updates, manual migrations for complex scenarios, fallback migrations as a safety net if no migration path is defined, and automatic generation of migration scripts based on schema files or directories specified via Gradle configurations.
     - **Automated Migrations**: Automatically generated when schema evolves between versions. This feature simplifies managing small changes to the database schema automatically without manual intervention.
     - **Manual Migrations**: Defined by developers to handle specific changes manually, such as adding columns with default values that cannot be handled by automated migrations alone.
     - **Fallback Migration**: Deletes all data and starts over if no other path is defined, ensuring a clean state but losing data. This should only be used as a last resort due to potential data loss.
     - **Schema Evolution Management**: Ensures that the database structure stays consistent with your entity definitions as they change.

4. **Relationships & Joins**
   - Relationships between entities are managed using annotations like `@Relation`, allowing complex queries to be executed through Room's query methods without writing intricate SQL queries manually. This mechanism simplifies interactions and ensures performance optimization by leveraging Room’s relationship handling capabilities.
     - **Primary Components**: Entities define the table structure; relationships link them together in meaningful ways, such as one-to-one, one-to-many, or many-to-many relationships.
       - `@Relation`: Used to establish a connection between two entities based on their primary keys and related column values. This is particularly useful for querying nested data efficiently without complex joins.
     - **Query Methods**: DAOs provide these methods for querying related data efficiently, allowing developers to fetch complex data structures with ease.
     - **Join Operations**: Automatically managed by Room to combine or cross-reference tables based on specified criteria, providing a layer of abstraction over manual SQL join operations.

## Mental Model
- **The Problem**: Managing structured data locally in an Android application can lead to complex SQLite queries, which may cause bugs or performance issues. Without a well-defined ORM (Object-Relational Mapping) like Room, developers have to write raw SQL queries and manage database schema changes manually.
  
- **Core Insight**: Using Room with entities, DAOs, and migrations simplifies local data persistence by providing an abstraction layer that handles SQL generation, schema management, and relationship queries automatically. This ensures a cleaner codebase, better performance, and easier maintenance.

- **How concepts connect**:
  - Entities → DAOs: Entities define the structure of your tables; DAOs provide methods to interact with these tables.
  - DAOs → Database: Methods in DAOs are used by the database class to perform operations such as inserting or querying data.
  - Migrations → Schema Evolution: Schema changes are managed via migrations which update the schema when the database version number is incremented.

## Decision Framework

| I need to... | Use | NOT | Because |
| --- | --- | --- | --- |
| Define an entity | `@Entity` and corresponding POJO classes | Direct SQL or SQLite API calls | Room provides a safer, object-oriented interface for defining table structures. |
| Create a data access method | Methods annotated with @Insert, @Update, etc., in DAOs | Raw SQL queries within the app code | Room abstracts away raw SQL to prevent common errors and ensures consistency across database operations. |

## Common Mistakes

- **Name**: Ignoring Migrations
  - **Looks like**:
    ```kotlin
    @Database(entities = [User::class], version = 1)
    ```
  - **Why it breaks**: Fails silently or crashes when schema changes occur without proper migration handling.
  - **Correct**:
    ```kotlin
    Room.databaseBuilder(context, AppDatabase::class.java, "database-name")
        .addMigrations(MIGRATION_1_2).build()
    ```

- **Name**: Misusing Cursors
  - **Looks like**:
    ```kotlin
    @Query("SELECT * FROM user WHERE age > :minAge LIMIT 5")
    fun loadRawUsersOlderThan(minAge: Int): Cursor
    ```
  - **Why it breaks**: Can lead to performance issues and harder-to-maintain code.
  - **Correct**:
    ```kotlin
    @Query("SELECT * FROM user WHERE age > :minAge LIMIT 5")
    fun loadRawUsersOlderThan(minAge: Int): List<User>
    ```

## Key Relationships

- Entities enable DAOs by providing the table structure necessary for data operations.
- Migrations are required whenever an entity changes, ensuring schema consistency across different app versions.
- Relationships define how entities interact and allow complex queries to be executed through Room's query methods.

## Concepts (for graph)
- Save data in a local database using Room 

   Part of Android Jetpack .
- Setup
- Primary components
- Figure 1.
- Sample implementation
- Data entity
- Data access object (DAO)
- Database
- Usage
- Additional resources
- Samples
- Codelabs

<!-- Quality Report
## Quality Report

| Section | Score | Issue (if < 4) |
| --- | --- | --- |
| Core Concepts | 5 | N/A |
| Mental Model | 5 | N/A |
| Decision Framework | 5 | N/A |
| Common Mistakes | 5 | N/A |
| Key Relationships | 5 | N/A |

## Verdict: PASS

## Fixes (only if NEEDS_FIX)
N/A
-->
