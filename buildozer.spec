
[app]
title = 4-7-8 Breathing
package.name = breathing478
package.domain = com.breathing
version = 1.0.0
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
requirements = python3, kivy==2.3.0
orientation = portrait
fullscreen = 0

# تنظیمات ضروری و به‌روز اندروید
android.api = 33
android.minapi = 21
# حذف خط android.sdk (منسوخ شده است)
android.ndk = 25b # استفاده از نسخه‌ی NDK جدیدتر و پایدارتر
android.ndk_api = 21
# مهاجرت از arch به archs (برای جلوگیری از هشدار)
android.archs = arm64-v8a, armeabi-v7a
android.permissions = INTERNET
android.accept_sdk_license = true
android.wakelock = True

# تنظیمات پشتیبان برای سازگاری (اختیاری)
p4a.branch = develop
