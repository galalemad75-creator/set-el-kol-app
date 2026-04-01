# 👩‍🍳 ست الكل - Set El Kol

تطبيق ذكي للوصفات — ابحث عن ألذ الوصفات حسب المكونات المتاحة في مطبخك!

## ✨ المميزات

- 🔍 **بحث بالمكونات** — أدخل المكونات المتاحة واحصل على وصفات مطابقة
- 🌍 **21 مطبخ عالمي** — مصري، هندي، إيطالي، ياباني، فرنسي، تركي، صيني، مكسيكي، مغربي، تايلاندي، إسباني، بريطاني، أمريكي، يوناني، فيتنامي، كندي، هولندي، أيرلندي، جامايكي، كيني
- 🍽️ **تصنيفات متعددة** — لحوم، دجاج، حلويات، بحري، نباتي، معكرونة، إفطار
- 🌐 **دعم 3 لغات** — العربية، الإنجليزية، الفرنسية
- ❤️ **المفضلة** — احفظ الوصفات المحبوبة
- 📤 **مشاركة** — شارك الوصفات مع أصدقائك
- 📴 **عمل بدون إنترنت** — Service Worker للوصول بدون اتصال
- 🎨 **تصميم أنيق** — واجهة عربية RTL مع ألوان دافئة

## 🛠️ التقنية

- **Frontend:** Pure HTML5 + CSS3 + Vanilla JS (ES6+)
- **Native Wrapper:** Capacitor (Android + iOS)
- **API:** [TheMealDB](https://www.themealdb.com/api.php) (مجاني)
- **Offline:** Service Worker caching
- **Storage:** localStorage للمفضلة والإعدادات

## 📱 بناء التطبيق

### متطلبات
- Node.js 18+
- Android Studio (لبناء Android)
- Xcode (لبناء iOS - macOS فقط)

### الخطوات

```bash
# تثبيت التبعيات
npm install

# إضافة منصات الأصلية
npx cap add android
npx cap add ios

# بناء Android
cd android && ./gradlew assembleRelease

# بناء iOS
open ios/App/App.xcworkspace
```

📖 دليل كامل في `store/DEVELOPER_GUIDE.md`

## 🏪 نشر المتجر

- **Google Play:** `store/play-store-listing.md`
- **App Store:** `store/app-store-listing.md`
- **سياسة الخصوصية:** `store/privacy-policy.html`
- **شروط الاستخدام:** `store/terms-of-service.html`

## 📄 الترخيص

© 2026 ست الكل - Set El Kol. جميع الحقوق محفوظة.

البيانات مقدمة من [TheMealDB](https://www.themealdb.com/api.php).
