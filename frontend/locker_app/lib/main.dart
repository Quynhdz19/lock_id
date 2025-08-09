import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:http/http.dart' as http;
import 'package:permission_handler/permission_handler.dart';
import 'dart:io';
import 'dart:convert';
import 'package:http_parser/http_parser.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_database/firebase_database.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize Firebase
  await Firebase.initializeApp();
  // Enable verbose logging for Realtime Database troubleshooting
  FirebaseDatabase.instance.setLoggingEnabled(true);
  
  runApp(MyLockerApp());
}

class MyLockerApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'My Locker',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF2196F3),
          brightness: Brightness.light,
        ),
        useMaterial3: true,
      ),
      home: LockerPage(),
    );
  }
}

class LockerPage extends StatefulWidget {
  @override
  _LockerPageState createState() => _LockerPageState();
}

class _LockerPageState extends State<LockerPage> with TickerProviderStateMixin {
  CameraController? _controller;
  bool _isInitialized = false;
  bool _isUnlocking = false;
  int _cameraIndex = 0;
  List<CameraDescription> _cameras = [];
  late AnimationController _scanAnimationController;
  
  // Thông tin tủ của bạn - thay đổi theo tủ thực tế
  final String myLockerNumber = "A12"; // Thay đổi số tủ của bạn ở đây
  final String myLockerId = "12"; // ID tủ trong database
  
  // API Configuration
  final String baseUrl = "http://192.168.1.11:8000/api/face"; // Update to your backend URL
  
  // Firebase Database
  // Use explicit databaseURL to ensure we write to the correct instance/region
  static const String _databaseUrl =
      'https://lock-id-46378-default-rtdb.asia-southeast1.firebasedatabase.app';
  late FirebaseDatabase _database;
  late DatabaseReference _lockerRef;
  late DatabaseReference _rootStateRef;

  @override
  void initState() {
    super.initState();
    _scanAnimationController = AnimationController(
      duration: Duration(seconds: 2),
      vsync: this,
    )..repeat();
    
    // Initialize Firebase Database references
    _database = FirebaseDatabase.instanceFor(databaseURL: _databaseUrl);
    _lockerRef = _database.ref().child('lockers').child(myLockerId);
    // Root-level state key that your hardware/UI might be observing
    _rootStateRef = _database.ref().child('state');
    
    // Start listening to locker state changes
    _listenToLockerState();
    
    _requestCameraPermission();
  }

  Future<void> _requestCameraPermission() async {
    try {
      // Kiểm tra quyền camera
      PermissionStatus status = await Permission.camera.status;
      
      print('Camera permission status: $status');
      
      if (status.isDenied) {
        // Yêu cầu quyền camera
        print('Requesting camera permission...');
        status = await Permission.camera.request();
        print('Camera permission after request: $status');
      }
      
      if (status.isPermanentlyDenied) {
        // Quyền bị từ chối vĩnh viễn, hướng dẫn user mở settings
        print('Camera permission permanently denied');
        _showPermissionDialog();
        return;
      }
      
      if (status.isGranted) {
        // Có quyền, khởi tạo camera
        print('Camera permission granted, initializing camera...');
        _initializeCamera();
      } else {
        // Quyền bị từ chối
        print('Camera permission denied');
        _showMessage('Cần quyền truy cập camera để sử dụng tính năng này', isError: true);
      }
    } catch (e) {
      print('Error requesting camera permission: $e');
      _showMessage('Lỗi khi yêu cầu quyền camera: $e', isError: true);
    }
  }

  // Thêm hàm kiểm tra quyền camera trực tiếp
  Future<void> _checkCameraPermissionDirectly() async {
    try {
      // Thử khởi tạo camera trực tiếp
      _cameras = await availableCameras();
      if (_cameras.isNotEmpty) {
        _controller = CameraController(
          _cameras[_cameraIndex],
          ResolutionPreset.high,
        );
        
        await _controller!.initialize();
        setState(() {
          _isInitialized = true;
        });
        print('Camera initialized successfully');
      } else {
        print('No cameras found');
        _showMessage('No camera found on device', isError: true);
      }
    } catch (e) {
      print('Direct camera initialization error: $e');
      if (e.toString().contains('permission')) {
        _showMessage('Camera permission required. Please go to Settings > Privacy & Security > Camera and enable permission for this app.', isError: true);
      } else {
        _showMessage('Camera initialization error: $e', isError: true);
      }
    }
  }

  void _showPermissionDialog() {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Row(
            children: [
              Icon(Icons.camera_alt, color: Colors.blue),
              SizedBox(width: 8),
              Text('Camera Permission'),
            ],
          ),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'This app needs camera permission for face recognition and locker access.',
                style: TextStyle(fontSize: 16),
              ),
              SizedBox(height: 16),
              Text(
                'How to enable:',
                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
              ),
              SizedBox(height: 8),
              Text(
                '1. Open Settings\n'
                '2. Find "Locker App"\n'
                '3. Enable "Camera"\n'
                '4. Return to app',
                style: TextStyle(fontSize: 14, color: Colors.grey[700]),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
                _showMessage('Cannot use camera', isError: true);
              },
              child: Text('Cancel'),
            ),
            ElevatedButton(
              onPressed: () async {
                Navigator.of(context).pop();
                try {
                  await openAppSettings();
                } catch (e) {
                  _showMessage('Cannot open Settings: $e', isError: true);
                }
              },
              child: Text('Open Settings'),
            ),
          ],
        );
      },
    );
  }

  Future<void> _initializeCamera() async {
    try {
      _cameras = await availableCameras();
      if (_cameras.isNotEmpty) {
        _controller = CameraController(
          _cameras[_cameraIndex],
          ResolutionPreset.high,
        );
        
        await _controller!.initialize();
        setState(() {
          _isInitialized = true;
        });
      } else {
        _showMessage('No camera found', isError: true);
      }
    } catch (e) {
      _showMessage('Camera initialization error: $e', isError: true);
    }
  }

  Future<void> _switchCamera() async {
    if (_cameras.length < 2) return;
    
    try {
      await _controller?.dispose();
      
      _cameraIndex = (_cameraIndex + 1) % _cameras.length;
      _controller = CameraController(
        _cameras[_cameraIndex],
        ResolutionPreset.high,
      );
      
      await _controller!.initialize();
      setState(() {});
    } catch (e) {
      _showMessage('Error switching camera: $e', isError: true);
    }
  }

  @override
  void dispose() {
    _controller?.dispose();
    _scanAnimationController.dispose();
    super.dispose();
  }

  Future<void> _unlockWithFace() async {
    if (!_isInitialized || _controller == null) {
      _showMessage('Camera not ready', isError: true);
      return;
    }

    setState(() {
      _isUnlocking = true;
    });

    try {
      // Take a photo
      final image = await _controller!.takePicture();
      
      // Read the image file
      final imageFile = File(image.path);
      final imageBytes = await imageFile.readAsBytes();

      // Create multipart request
      var request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl/unlock-locker'),
      );

      // Add image file
      request.files.add(
        http.MultipartFile.fromBytes(
          'file',
          imageBytes,
          filename: 'face.jpg',
          contentType: MediaType('image', 'jpeg'),
        ),
      );

      // Add locker ID and user ID
      request.fields['locker_id'] = myLockerId;
      request.fields['user_id'] = 'owner';

      // Send request
      final response = await request.send();
      final responseData = await response.stream.bytesToString();
      final jsonResponse = json.decode(responseData);

      print('🔍 Face verification response: $jsonResponse');

      if (response.statusCode == 200 && jsonResponse['success']) {
        // Unlock function with Firebase Realtime Database
        await _unlockLocker();
      } else {
        print('❌ Face verification failed: ${jsonResponse['message']}');
        _showMessage('❌ Face verification failed', isError: true);
      }
    } catch (e) {
      print('❌ Error unlocking with face: $e');
      _showMessage('Error: $e', isError: true);
    } finally {
      setState(() {
        _isUnlocking = false;
      });
    }
  }

  // Firebase Realtime Database unlock function
  Future<void> _unlockLocker() async {
    try {
      // Update the state field to 'unlocked' in Firebase
      await _lockerRef.update({
        'state': 'unlocked',
        'lastUnlockTime': DateTime.now().toIso8601String(),
        'status': 'active',
        'lockerNumber': myLockerNumber,
      });
      // Also mirror the state at the root key if external systems read it there
      await _rootStateRef.set('unlocked');
      
      print('✅ FACE MATCH DETECTED - Locker unlocked successfully!');
      print('✅ Firebase updated: Locker $myLockerId state changed to unlocked');
      _showMessage('🔓 Locker unlocked successfully!', isError: false);
      
      // Optional: Add sound or vibration here
      // You can add HapticFeedback.mediumImpact() for vibration
      
    } catch (e) {
      print('❌ Error updating Firebase: $e');
      _showMessage('🔓 Locker unlocked but failed to update database', isError: false);
    }
  }

  // Function to read current locker state from Firebase
  Future<Map<String, dynamic>?> _getLockerState() async {
    try {
      final snapshot = await _lockerRef.get();
      if (snapshot.exists) {
        return Map<String, dynamic>.from(snapshot.value as Map);
      }
      return null;
    } catch (e) {
      print('❌ Error reading locker state: $e');
      return null;
    }
  }

  // Function to listen to locker state changes
  void _listenToLockerState() {
    _lockerRef.onValue.listen((event) {
      if (event.snapshot.exists) {
        final data = Map<String, dynamic>.from(event.snapshot.value as Map);
        print('📡 Locker state changed: ${data['state']}');
        
        // You can add UI updates here based on state changes
        if (data['state'] == 'locked') {
          print('🔒 Locker is now locked');
        } else if (data['state'] == 'unlocked') {
          print('🔓 Locker is now unlocked');
        }
      }
    });
  }

  // New method to register face
  Future<void> _registerFace() async {
    if (!_isInitialized || _controller == null) {
      _showMessage('Camera not ready', isError: true);
      return;
    }

    setState(() {
      _isUnlocking = true;
    });

    try {
      // Take a photo
      final image = await _controller!.takePicture();
      
      // Read the image file
      final imageFile = File(image.path);
      final imageBytes = await imageFile.readAsBytes();

      // Create multipart request for registration
      var request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl/register'),
      );

      // Add image file
      request.files.add(
        http.MultipartFile.fromBytes(
          'file',
          imageBytes,
          filename: 'face.jpg',
          contentType: MediaType('image', 'jpeg'),
        ),
      );

      // Add user ID
      request.fields['user_id'] = 'owner';

      // Send request
      final response = await request.send();
      final responseData = await response.stream.bytesToString();
      final jsonResponse = json.decode(responseData);

      print('🔍 Face registration response: $jsonResponse');

      if (response.statusCode == 200 && jsonResponse['success']) {
        print('✅ Face registered successfully!');
        _showMessage('✅ Face registered successfully!', isError: false);
      } else {
        print('❌ Face registration failed: ${jsonResponse['message']}');
        _showMessage('❌ Face registration failed: ${jsonResponse['message']}', isError: true);
      }
    } catch (e) {
      print('❌ Error registering face: $e');
      _showMessage('Error: $e', isError: true);
    } finally {
      setState(() {
        _isUnlocking = false;
      });
    }
  }

  Future<bool> _sendFaceToServer(File imageFile) async {
    try {
      // Tạo request để gửi ảnh lên server
      final request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl/unlock-locker'),
      );

      // Thêm ảnh vào request
      request.files.add(
        await http.MultipartFile.fromPath('file', imageFile.path),
      );
      
      // Thêm ID tủ và user ID
      request.fields['locker_id'] = myLockerId;
      request.fields['user_id'] = 'owner';

      // Gửi request
      final response = await request.send();
      final responseData = await response.stream.bytesToString();
      final data = json.decode(responseData);

      return response.statusCode == 200 && data['success'] == true;
    } catch (e) {
      print('Error sending face to server: $e');
      return false;
    }
  }

  void _showMessage(String message, {required bool isError}) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: isError ? Colors.red : Colors.green,
        duration: Duration(seconds: 3),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('My Locker'),
        backgroundColor: Theme.of(context).colorScheme.primary,
        foregroundColor: Colors.white,
        centerTitle: true,
        elevation: 0,
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [
              Theme.of(context).colorScheme.primary.withOpacity(0.1),
              Colors.white,
            ],
          ),
        ),
        child: SafeArea(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                // Thông tin tủ
                Card(
                  elevation: 8,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(20),
                    child: Column(
                      children: [
                        Icon(
                          Icons.lock_outline,
                          size: 60,
                          color: Theme.of(context).colorScheme.primary,
                        ),
                        SizedBox(height: 16),
                        Text(
                          'Your Locker',
                          style: TextStyle(
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                            color: Theme.of(context).colorScheme.primary,
                          ),
                        ),
                        SizedBox(height: 8),
                        Text(
                          'Locker: $myLockerNumber',
                          style: TextStyle(
                            fontSize: 28,
                            fontWeight: FontWeight.bold,
                            color: Colors.black87,
                          ),
                        ),
                        SizedBox(height: 16),
                        Container(
                          padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                          decoration: BoxDecoration(
                            color: Colors.green.withOpacity(0.1),
                            borderRadius: BorderRadius.circular(16),
                            border: Border.all(color: Colors.green),
                          ),
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Icon(Icons.check_circle, color: Colors.green, size: 18),
                              SizedBox(width: 6),
                              Text(
                                'Ready to unlock',
                                style: TextStyle(
                                  color: Colors.green,
                                  fontWeight: FontWeight.bold,
                                  fontSize: 12,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                
                SizedBox(height: 24),
                
                // Camera preview with face scanning effect
                if (_isInitialized)
                  Stack(
                    children: [
                      Container(
                        height: 600,
                        width: 350,
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(20),
                          border: Border.all(
                            color: Theme.of(context).colorScheme.primary,
                            width: 3,
                          ),
                        ),
                        clipBehavior: Clip.antiAlias,
                        child: CameraPreview(_controller!),
                      ),
                      // Face scanning overlay
                      Positioned.fill(
                        child: Container(
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: AnimatedBuilder(
                            animation: _scanAnimationController,
                            builder: (context, child) {
                              return CustomPaint(
                                painter: FaceScanningPainter(_scanAnimationController.value),
                              );
                            },
                          ),
                        ),
                      ),
                      // Camera switch button
                      if (_cameras.length > 1)
                        Positioned(
                          top: 16,
                          right: 16,
                          child: Container(
                            decoration: BoxDecoration(
                              color: Colors.black.withOpacity(0.6),
                              borderRadius: BorderRadius.circular(25),
                            ),
                            child: IconButton(
                              onPressed: _switchCamera,
                              icon: Icon(Icons.flip_camera_ios, color: Colors.white),
                              iconSize: 24,
                            ),
                          ),
                        ),
                    ],
                  )
                else
                  Container(
                    height: 350,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(20),
                      color: Colors.grey[200],
                    ),
                    child: Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.camera_alt, size: 48, color: Colors.grey[400]),
                          SizedBox(height: 16),
                          Text('Camera not ready', style: TextStyle(fontSize: 16, color: Colors.grey[600])),
                          SizedBox(height: 8),
                          Column(
                            children: [
                              ElevatedButton(
                                onPressed: () {
                                  _requestCameraPermission();
                                },
                                child: Text('Request Permission'),
                              ),
                              SizedBox(height: 8),
                              TextButton(
                                onPressed: () {
                                  _checkCameraPermissionDirectly();
                                },
                                child: Text('Try Direct Init'),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ),
                
                SizedBox(height: 24),
                
                // Register Face Button
                SizedBox(
                  width: double.infinity,
                  height: 50,
                  child: OutlinedButton(
                    onPressed: _isUnlocking ? null : _registerFace,
                    style: OutlinedButton.styleFrom(
                      foregroundColor: Colors.blue,
                      side: BorderSide(color: Colors.blue),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(16),
                      ),
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.person_add, size: 20),
                        SizedBox(width: 8),
                        Text(
                          'Register Face',
                          style: TextStyle(fontSize: 14, fontWeight: FontWeight.w500),
                        ),
                      ],
                    ),
                  ),
                ),
                
                SizedBox(height: 16),
                
                // Unlock button
                SizedBox(
                  width: double.infinity,
                  height: 70,
                  child: ElevatedButton(
                    onPressed: _isUnlocking ? null : _unlockWithFace,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Theme.of(context).colorScheme.primary,
                      foregroundColor: Colors.white,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(16),
                      ),
                      elevation: 8,
                    ),
                    child: _isUnlocking
                        ? Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              SizedBox(
                                width: 18,
                                height: 18,
                                child: CircularProgressIndicator(
                                  strokeWidth: 2,
                                  valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                                ),
                              ),
                              SizedBox(width: 10),
                              Text(
                                'Verifying...',
                                style: TextStyle(fontSize: 16),
                              ),
                            ],
                          )
                        : Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(Icons.face, size: 24),
                              SizedBox(width: 10),
                              Text(
                                'Unlock with Face Recognition',
                                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                              ),
                            ],
                          ),
                  ),
                ),
                
                SizedBox(height: 16),
                
                // Instructions
                Container(
                  padding: EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.blue.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.blue.withOpacity(0.3)),
                  ),
                  child: Row(
                    children: [
                      Icon(Icons.info_outline, color: Colors.blue, size: 20),
                      SizedBox(width: 10),
                      Expanded(
                        child: Text(
                          'First register your face, then position it in the camera frame to unlock',
                          style: TextStyle(
                            color: Colors.blue[800],
                            fontSize: 13,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                
                SizedBox(height: 20),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

// Face scanning effect painter
class FaceScanningPainter extends CustomPainter {
  final double animationValue;
  
  FaceScanningPainter(this.animationValue);
  
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.blue.withOpacity(0.3)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.0;

    final center = Offset(size.width / 2, size.height / 2);
    final radius = size.width * 0.3;
    
    // Draw scanning circle
    canvas.drawCircle(center, radius, paint);
    
    // Draw scanning line
    final scanPaint = Paint()
      ..color = Colors.blue.withOpacity(0.8)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 3.0;
    
    final scanY = center.dy - radius + animationValue * (radius * 2);
    canvas.drawLine(
      Offset(center.dx - radius, scanY),
      Offset(center.dx + radius, scanY),
      scanPaint,
    );
    
    // Draw corner indicators
    final cornerPaint = Paint()
      ..color = Colors.blue
      ..style = PaintingStyle.stroke
      ..strokeWidth = 4.0;
    
    final cornerLength = 20.0;
    final cornerOffset = radius - cornerLength;
    
    // Top left corner
    canvas.drawLine(
      Offset(center.dx - cornerOffset, center.dy - radius),
      Offset(center.dx - cornerOffset + cornerLength, center.dy - radius),
      cornerPaint,
    );
    canvas.drawLine(
      Offset(center.dx - radius, center.dy - cornerOffset),
      Offset(center.dx - radius, center.dy - cornerOffset + cornerLength),
      cornerPaint,
    );
    
    // Top right corner
    canvas.drawLine(
      Offset(center.dx + cornerOffset - cornerLength, center.dy - radius),
      Offset(center.dx + cornerOffset, center.dy - radius),
      cornerPaint,
    );
    canvas.drawLine(
      Offset(center.dx + radius - cornerLength, center.dy - cornerOffset),
      Offset(center.dx + radius, center.dy - cornerOffset),
      cornerPaint,
    );
    
    // Bottom left corner
    canvas.drawLine(
      Offset(center.dx - cornerOffset, center.dy + radius - cornerLength),
      Offset(center.dx - cornerOffset + cornerLength, center.dy + radius),
      cornerPaint,
    );
    canvas.drawLine(
      Offset(center.dx - radius, center.dy + cornerOffset - cornerLength),
      Offset(center.dx - radius, center.dy + cornerOffset),
      cornerPaint,
    );
    
    // Bottom right corner
    canvas.drawLine(
      Offset(center.dx + cornerOffset - cornerLength, center.dy + radius),
      Offset(center.dx + cornerOffset, center.dy + radius),
      cornerPaint,
    );
    canvas.drawLine(
      Offset(center.dx + radius - cornerLength, center.dy + cornerOffset),
      Offset(center.dx + radius, center.dy + cornerOffset),
      cornerPaint,
    );
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) {
    return oldDelegate is FaceScanningPainter && 
           oldDelegate.animationValue != animationValue;
  }
}
