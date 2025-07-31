#!/bin/bash

echo "🔧 Installing Face Recognition Dependencies..."

# Install basic requirements
pip3 install fastapi uvicorn python-multipart

# Install OpenCV
pip3 install opencv-python

# Install face_recognition (this might take a while)
echo "📦 Installing face_recognition library..."
pip3 install face-recognition

# Install numpy if not already installed
pip3 install numpy

echo "✅ Dependencies installed successfully!"
echo ""
echo "🚀 To start the server, run:"
echo "python3 main.py"
echo ""
echo "📱 API will be available at:"
echo "http://localhost:8000/docs" 