[app]
title = 4-7-8 Breathing
package.name = breathing478
package.domain = com.yourname
version = 1.0.0
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
requirements = python3,kivy==2.3.0,android
orientation = portrait
fullscreen = 0
android.api = 33
android.minapi = 21
android.sdk = 24
android.ndk = 23b
android.ndk_api = 21
android.gradle_dependencies = 'com.google.android.material:material:1.8.0'
p4a.branch = master
android.arch = armeabi-v7a,arm64-v8a
android.permissions = INTERNET
android.wakelock = True
android.meta_data = android.max_aspect=2.1

# آیکون‌ها (اختیاری)
# icon.filename = assets/icon.png
# presplash.filename = assets/presplash.png

# تنظیمات بهینه‌سازی
android.allow_backup = true
android.usesCleartextTraffic = true

# امضای دیباگ
android.release_artifact = .apk
