#!/bin/bash

echo "🚀 Hướng dẫn push code lên GitHub"
echo "=================================="

echo ""
echo "1️⃣ Đảm bảo bạn đã tạo repository trên GitHub:"
echo "   - Vào https://github.com/Quynhdz19/lock_id"
echo "   - Hoặc tạo repository mới: https://github.com/new"
echo ""

echo "2️⃣ Kiểm tra git status:"
git status

echo ""
echo "3️⃣ Nếu repository chưa tồn tại, tạo mới:"
echo "   git remote add origin https://github.com/Quynhdz19/lock_id.git"
echo ""

echo "4️⃣ Push code lên GitHub:"
echo "   git push -u origin main"
echo ""

echo "5️⃣ Nếu gặp lỗi permission, thử:"
echo "   - Sử dụng Personal Access Token"
echo "   - Hoặc sử dụng SSH: git remote set-url origin git@github.com:Quynhdz19/lock_id.git"
echo ""

echo "6️⃣ Hoặc tạo repository mới với tên khác:"
echo "   git remote set-url origin https://github.com/Quynhdz19/smart-locker-system.git"
echo ""

echo "📝 Lưu ý:"
echo "- Đảm bảo bạn có quyền write vào repository"
echo "- Kiểm tra GitHub token nếu sử dụng HTTPS"
echo "- Repository sẽ chứa toàn bộ code Smart Locker System"
echo ""

echo "🎯 Repository sẽ bao gồm:"
echo "✅ Backend API (FastAPI)"
echo "✅ Flutter Mobile App"
echo "✅ Face Recognition System"
echo "✅ Documentation và README"
echo "✅ Test scripts"
echo ""

echo "🔗 Sau khi push thành công, repository sẽ có:"
echo "   - README.md với hướng dẫn chi tiết"
echo "   - Backend code với API endpoints"
echo "   - Flutter app với camera integration"
echo "   - Test scripts để verify functionality"
echo ""

echo "✨ Chúc bạn thành công!" 