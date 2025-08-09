import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_database/firebase_database.dart';

// Test function to verify Firebase connection
Future<void> testFirebaseConnection() async {
  try {
    // Initialize Firebase
    await Firebase.initializeApp();
    
    // Test database connection
    final database = FirebaseDatabase.instance;
    final ref = database.ref();
    
    // Test write operation
    await ref.child('test').child('connection').set({
      'timestamp': DateTime.now().toIso8601String(),
      'status': 'connected',
    });
    
    print('✅ Firebase connection test successful!');
    
    // Test read operation
    final snapshot = await ref.child('test').child('connection').get();
    if (snapshot.exists) {
      print('✅ Firebase read test successful!');
      print('Data: ${snapshot.value}');
    }
    
    // Clean up test data
    await ref.child('test').remove();
    
  } catch (e) {
    print('❌ Firebase connection test failed: $e');
  }
}

// Test locker unlock function
Future<void> testLockerUnlock(String lockerId) async {
  try {
    final database = FirebaseDatabase.instance;
    final ref = database.ref().child('lockers').child(lockerId);
    
    // Update locker state
    await ref.update({
      'state': 'unlocked',
      'lastUnlockTime': DateTime.now().toIso8601String(),
      'status': 'active',
      'lockerNumber': 'A$lockerId',
    });
    
    print('✅ Locker unlock test successful for locker $lockerId!');
    
    // Read back the data
    final snapshot = await ref.get();
    if (snapshot.exists) {
      final data = Map<String, dynamic>.from(snapshot.value as Map);
      print('Locker state: ${data['state']}');
      print('Last unlock time: ${data['lastUnlockTime']}');
    }
    
  } catch (e) {
    print('❌ Locker unlock test failed: $e');
  }
}
