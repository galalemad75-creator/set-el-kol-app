import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.setelkol.recipes',
  appName: 'ست الكل - Set El Kol',
  webDir: 'www',
  server: {
    androidScheme: 'https',
    allowNavigation: ['www.themealdb.com', 'themealdb.com']
  },
  plugins: {
    SplashScreen: {
      launchShowDuration: 2000,
      launchAutoHide: true,
      backgroundColor: '#FFF9F2',
      androidSplashResourceName: 'splash',
      androidScaleType: 'CENTER_CROP',
      showSpinner: false
    },
    StatusBar: {
      style: 'default',
      backgroundColor: '#E8553A',
      overlaysWebView: false
    },
    App: {
      launchUrl: ''
    }
  },
  android: {
    allowMixedContent: false,
    captureInput: false,
    webContentsDebuggingEnabled: false
  },
  ios: {
    contentInset: 'automatic',
    scheme: 'set-el-kol'
  }
};

export default config;
