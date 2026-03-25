<!-- Source: https://developer.android.com/develop/ui/compose/designsystems/material3 -->
<!-- Type: official -->
<!-- Priority: high -->
<!-- Topic: material-design-3 -->
<!-- Extracted: 2026-03-24 -->
<!-- Verified: — -->

# Material Design 3 in Compose

## Rules
- DO: Use on-primary on top of primary, and on-primary-container on top of
primary-container, and the same for other accent and neutral colors to provide
accessible contrast to the user.

## Code Patterns
### Experimental APIs
```kotlin
// import androidx.compose.material3.ExperimentalMaterial3Api
@Composable
fun AppComposable() {
    // M3 composables
}
Material3Snippets.kt
```

### Material theming
```
MaterialTheme(
    colorScheme = /* ...
    typography = /* ...
    shapes = /* ...
) {
    // M3 app content
}Material3Snippets.kt
```

### Generate color schemes
```kotlin
val md_theme_light_primary = Color(0xFF476810)
val md_theme_light_onPrimary = Color(0xFFFFFFFF)
val md_theme_light_primaryContainer = Color(0xFFC7F089)
// ..
// ..

val md_theme_dark_primary = Color(0xFFACD370)
val md_theme_dark_onPrimary = Color(0xFF213600)
val md_theme_dark_primaryContainer = Color(0xFF324F00)
// ..
// ..Material3Snippets.kt
```

### Generate color schemes
```kotlin
private val LightColorScheme = lightColorScheme(
    primary = md_theme_light_primary,
    onPrimary = md_theme_light_onPrimary,
    primaryContainer = md_theme_light_primaryContainer,
    // ..
)
private val DarkColorScheme = darkColorScheme(
    primary = md_theme_dark_primary,
    onPrimary = md_theme_dark_onPrimary,
    primaryContainer = md_theme_dark_primaryContainer,
    // ..
)

@Composable
fun ReplyTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme =
        if (!darkTheme) {
            LightColorScheme
        } else {
            DarkColorScheme
        }
    MaterialTheme(
        colorScheme = colorScheme,
        content = content
    )
}Material3Snippets.kt
```

### Dynamic color schemes
```kotlin
// Dynamic color is available on Android 12+
val dynamicColor = Build.VERSION.SDK_INT >= Build.VERSION_CODES.S
val colors = when {
    dynamicColor && darkTheme -> dynamicDarkColorScheme(LocalContext.current)
    dynamicColor && !darkTheme -> dynamicLightColorScheme(LocalContext.current)
    darkTheme -> DarkColorScheme
    else -> LightColorScheme
}Material3Snippets.kt
```

### Color usage
```
Text(
    text = "Hello theming",
    color = MaterialTheme.colorScheme.primary
)Material3Snippets.kt
```

### Color usage
```
Card(
    colors = CardDefaults.cardColors(
        containerColor =
        if (isSelected) MaterialTheme.colorScheme.primaryContainer
        else
            MaterialTheme.colorScheme.surfaceVariant
    )
) {
    Text(
        text = "Dinner club",
        style = MaterialTheme.typography.bodyLarge,
        color =
        if (isSelected) MaterialTheme.colorScheme.onPrimaryContainer
        else MaterialTheme.colorScheme.onSurface,
    )
}
Material3Snippets.kt
```

### Define typography
```kotlin
val replyTypography = Typography(
    titleLarge = TextStyle(
        fontWeight = FontWeight.SemiBold,
        fontSize = 22.sp,
        lineHeight = 28.sp,
        letterSpacing = 0.sp
    ),
    titleMedium = TextStyle(
        fontWeight = FontWeight.SemiBold,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.15.sp
    ),
    // ..
)
// ..Material3Snippets.kt
```

### Define typography
```
bodyLarge = TextStyle(
    fontWeight = FontWeight.Normal,
    fontFamily = FontFamily.SansSerif,
    fontStyle = FontStyle.Italic,
    fontSize = 16.sp,
    lineHeight = 24.sp,
    letterSpacing = 0.15.sp,
    baselineShift = BaselineShift.Subscript
),Material3Snippets.kt
```

### Define typography
```
MaterialTheme(
    typography = replyTypography,
) {
    // M3 app Content
}Material3Snippets.kt
```

### Use text styles
```
Text(
    text = "Hello M3 theming",
    style = MaterialTheme.typography.titleLarge
)
Text(
    text = "you are learning typography",
    style = MaterialTheme.typography.bodyMedium
)Material3Snippets.kt
```

### Define shapes
```kotlin
val replyShapes = Shapes(
    extraSmall = RoundedCornerShape(4.dp),
    small = RoundedCornerShape(8.dp),
    medium = RoundedCornerShape(12.dp),
    large = RoundedCornerShape(16.dp),
    extraLarge = RoundedCornerShape(24.dp)
)Material3Snippets.kt
```

### Define shapes
```
MaterialTheme(
    shapes = replyShapes,
) {
    // M3 app Content
}Material3Snippets.kt
```

### Use shapes
```
Card(shape = MaterialTheme.shapes.medium) { /* card content */ }
FloatingActionButton(
    shape = MaterialTheme.shapes.large,
    onClick = {
    }
) {
    /* fab content */
}Material3Snippets.kt
```

### Use shapes
```
Card(shape = RectangleShape) { /* card content */ }
Card(shape = CircleShape) { /* card content */ }Material3Snippets.kt
```

### Emphasis
```
bodyLarge = TextStyle(
    fontWeight = FontWeight.Bold
),
bodyMedium = TextStyle(
    fontWeight = FontWeight.Normal
)Material3Snippets.kt
```

### Elevation
```
Surface(
    modifier = Modifier,
    tonalElevation = /*...
    shadowElevation = /*...
) {
    Column(content = content)
}Material3Snippets.kt
```

### Material components
```
Button(onClick = { /*..*/ }) {
    Text(text = "My Button")
}Material3Snippets.kt
```

### Material components
```
ExtendedFloatingActionButton(
    onClick = { /*..*/ },
    modifier = Modifier
) {
    Icon(
        imageVector = Icons.Default.Edit,
        contentDescription = stringResource(id = R.string.edit),
    )
    Text(
        text = stringResource(id = R.string.add_entry),
    )
}Material3Snippets.kt
```

### Material components
```
Button(onClick = { /*..*/ }) {
    Text(text = stringResource(id = R.string.view_entry))
}Material3Snippets.kt
```

### Material components
```
TextButton(onClick = { /*..*/ }) {
    Text(text = stringResource(id = R.string.replated_articles))
}Material3Snippets.kt
```

### Navigation components
```
NavigationBar(modifier = Modifier.fillMaxWidth()) {
    Destinations.entries.forEach { replyDestination ->
        NavigationBarItem(
            selected = selectedDestination == replyDestination,
            onClick = { },
            icon = { }
        )
    }
}Material3Snippets.kt
```

### Navigation components
```
NavigationRail(
    modifier = Modifier.fillMaxHeight(),
) {
    Destinations.entries.forEach { replyDestination ->
        NavigationRailItem(
            selected = selectedDestination == replyDestination,
            onClick = { },
            icon = { }
        )
    }
}Material3Snippets.kt
```

### Navigation components
```
PermanentNavigationDrawer(modifier = Modifier.fillMaxHeight(), drawerContent = {
    Destinations.entries.forEach { replyDestination ->
        NavigationRailItem(
            selected = selectedDestination == replyDestination,
            onClick = { },
            icon = { },
            label = { }
        )
    }
}) {
}Material3Snippets.kt
```

### Customize a component's theming
```kotlin
val customCardColors = CardDefaults.cardColors(
    contentColor = MaterialTheme.colorScheme.primary,
    containerColor = MaterialTheme.colorScheme.primaryContainer,
    disabledContentColor = MaterialTheme.colorScheme.surface,
    disabledContainerColor = MaterialTheme.colorScheme.onSurface,
)
val customCardElevation = CardDefaults.cardElevation(
    defaultElevation = 8.dp,
    pressedElevation = 2.dp,
    focusedElevation = 4.dp
)
Card(
    colors = customCardColors,
    elevation = customCardElevation
) {
    // m3 card content
}Material3Snippets.kt
```

### Color accessibility
```
// ✅ Button with sufficient contrast ratio
Button(
    onClick = { },
    colors = ButtonDefaults.buttonColors(
        containerColor = MaterialTheme.colorScheme.primary,
        contentColor = MaterialTheme.colorScheme.onPrimary
    )
) {
}

// ❌ Button with poor contrast ratio
Button(
    onClick = { },
    colors = ButtonDefaults.buttonColors(
        containerColor = MaterialTheme.colorScheme.tertiaryContainer,
        contentColor = MaterialTheme.colorScheme.primaryContainer
    )
) {
}Material3Snippets.kt
```

## Decision Tables
### Typography
| M3 | Default Font Size/Line Height |
| --- | --- |
| displayLarge | Roboto 57/64 |
| displayMedium | Roboto 45/52 |
| displaySmall | Roboto 36/44 |
| headlineLarge | Roboto 32/40 |
| headlineMedium | Roboto 28/36 |
| headlineSmall | Roboto 24/32 |
| titleLarge | New- Roboto Medium 22/28 |
| titleMedium | Roboto Medium 16/24 |
| titleSmall | Roboto Medium 14/20 |
| bodyLarge | Roboto 16/24 |
| bodyMedium | Roboto 14/20 |
| bodySmall | Roboto 12/16 |
| labelLarge | Roboto Medium 14/20 |
| labelMedium | Roboto Medium 12/16 |
| labelSmall | New Roboto Medium, 11/16 |

## Guidelines
- An M3 theme contains the following subsystems: color scheme ,
 typography and shapes . When you customize
these values, your changes are automatically reflected in the M3 components you
use to build your app.
- To support light and dark themes, use isSystemInDarkTheme() . Based on the
system setting, define which color scheme to use: light or dark.
- Dynamic color is available on Android 12 and above. If dynamic color is
available, you can set up a dynamic ColorScheme . If not, you should fall back
to using a custom light or dark ColorScheme .
- Note: Unlike the M2 Typography class, the M3 Typography class doesn’t
currently include a defaultFontFamily parameter. You’ll need to use the
 fontFamily parameter in each of the individual TextStyles instead.
- Compose provides the M3 Typography class — along with the existing
 TextStyle and font-related classes — to model the Material 3 type
scale. The Typography constructor offers defaults for each style so you can omit
any parameters you do not want to customize:
- Note: For disabled states in M3, it’s still acceptable to use “on-x” (where x
can be primary, secondary, surface etc.) colors with alpha values.
- You can read more about Material buttons and other components .
Material 3 provides a wide variety of component suites such as Buttons, App
bars, Navigation components that are specifically designed for different use
cases and screen sizes.
- NavigationDrawer is used for medium-to-large size tablets where you have
enough space to show detail. You can use both PermanentNavigationDrawer or
 ModalNavigationDrawer along with NavigationRail .
- All Material components and dynamic theming already use the above color roles
from a set of tonal palettes , selected to meet accessibility
requirements. However, if you are customizing components, make sure to use
appropriate color roles and avoid mismatch.
- The use of a tertiary container on top of primary gives the user a poor
contrast button:

## Core Concepts

1. **Material Theming**
   - Evidence: Sections such as Experimental APIs and Material theming emphasize the importance of setting up a consistent theme across an app using `MaterialTheme`. The mechanism involves defining color schemes, typography, and shapes within `MaterialTheme` to ensure uniform styling throughout the application.
2. **Color Schemes and Accessibility**
   - Evidence: Guidelines explicitly mention providing accessible contrast for users with guidelines like DOs, which include specific instructions on how colors should be used to maintain adequate contrast ratios across light and dark themes.
3. **Typography Customization**
   - Evidence: Sections on typography usage, definition, and customization illustrate the prominence of Material 3's Typography class in customizing font styles, sizes, and line heights for different text elements, ensuring a readable and aesthetically pleasing UI.

## Mental Model

- **The Problem**: The lack of consistent theming can result in UI elements like buttons or cards appearing with insufficient contrast ratios between background colors and text when switching from light to dark mode. This inconsistency can lead to readability problems for users.
- **Core Insight**: `MaterialTheme` serves as a central hub for defining the visual identity of an app by providing pre-defined or custom color schemes, typography, and shapes. This ensures that all UI elements follow a unified design language throughout the application.
- **How concepts connect**:
  - Material Theming → Color Schemes: The theme provides a cohesive set of colors and typography rules that can be dynamically adjusted to fit different modes (light, dark).
  - Color Schemes → Accessibility: Properly defined color schemes meet accessibility standards by ensuring sufficient contrast ratios for all users.
  - Typography Customization → UI Appearance: Using the right font sizes and styles enhances readability and aesthetic appeal across various screen sizes and content types.

## Common Mistakes

### Using Inappropriate Color Contrasts
- **Name**: Poor Contrast Ratios in Buttons
- **Looks like**:
  ```kotlin
  Button(
      onClick = { },
      colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.tertiaryContainer, contentColor = MaterialTheme.colorScheme.primaryContainer)
  ) {
  }
  ```
- **Why it breaks**: The selected color combination may not meet WCAG (Web Content Accessibility Guidelines) contrast standards, making the text or icons hard to read for users with visual impairments.
- **Correct**:
  ```kotlin
  Button(
      onClick = { },
      colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary, contentColor = MaterialTheme.colorScheme.onPrimary)
  ) {
  }
  ```

## Key Relationships

- Material Theming enables consistent UI and ensures that all navigation components maintain a unified look across different modes by providing pre-defined or custom color schemes.
- Color Schemes ensure accessible and visually appealing designs by adhering to WCAG guidelines, ensuring sufficient contrast ratios for text against backgrounds in both light and dark themes.
- Typography Customization enhances readability and aesthetic appeal through proper use of font sizes, styles, and line heights, making the UI more user-friendly regardless of screen size or content type.

## Concepts (for graph)
- Figure 1
- Dependency
- Experimental APIs
- Material theming
- Figure 2
- Color scheme
- Figure 3
- Figure 4
- Figure 5
- Figure 6
- Typography
- Figure 7

<!-- Quality Report
## Quality Report

| Section | Score | Issue (if < 4) |
| --- | --- | --- |
| Core Concepts | 5 | N/A |
| Mental Model | 5 | N/A |
| Decision Framework | 3 | Missing depth and precision in the description of how concepts connect. |
| Common Mistakes | 5 | N/A |
| Key Relationships | 5 | N/A |

## Verdict: NEEDS_FIX

## Fixes (only if NEEDS_FIX)
Decision Framework: Provide more specific examples to illustrate the connections between Material Theming, Color Schemes, and Typography Customization.
-->
