# Firebase Configuration for Locker App

## 1. Firebase Project Setup

You need to set up Firebase for your Flutter app. Follow these steps:

### Step 1: Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or use existing project
3. Enable Realtime Database

### Step 2: Add Android App
1. In Firebase Console, go to Project Settings
2. Add Android app with package name: `com.example.locker_app`
3. Download `google-services.json` and place it in `android/app/`

### Step 3: Add iOS App (if needed)
1. Add iOS app with bundle ID: `com.example.lockerApp`
2. Download `GoogleService-Info.plist` and place it in `ios/Runner/`

### Step 4: Configure Realtime Database
1. Go to Realtime Database in Firebase Console
2. Create database with URL: `https://lock-id-46378-default-rtdb.asia-southeast1.firebasedatabase.app/`
3. Set security rules to allow read/write:

```json
{
  "rules": {
    "lockers": {
      "$lockerId": {
        ".read": true,
        ".write": true
      }
    }
  }
}
```

## 2. Database Structure

The app expects this structure in Firebase Realtime Database:

```json
{
  "lockers": {
    "12": {
      "state": "locked",
      "status": "active",
      "lockerNumber": "A12",
      "lastUnlockTime": "2024-01-01T12:00:00.000Z"
    }
  }
}
```

## 3. Install Dependencies

Run this command to install Firebase dependencies:

```bash
flutter pub get
```

## 4. Test the Implementation

The app will now:
- Update Firebase when face verification succeeds (status 200)
- Set `state` to "unlocked"
- Add timestamp and status information
- Listen to real-time state changes

## 5. Firebase Security Rules (Recommended)

For production, use more secure rules:

```json
{
  "rules": {
    "lockers": {
      "$lockerId": {
        ".read": "auth != null",
        ".write": "auth != null && data.child('state').val() != 'unlocked'"
      }
    }
  }
}
```

## 6. Troubleshooting

If you get Firebase connection errors:
1. Check if `google-services.json` is in the correct location
2. Verify Firebase project settings
3. Check internet connection
4. Verify database URL in Firebase Console
