// MAIN COLORS - VUESAX THEME COLORS
let colors = {
  primary: '#191948', // Primary
  secondary: '#64728F', // Secondary
  success: '#0243EC', // Action
  danger: '#ED1D24', // Danger
  warning: '#e15759', // Warning
  dark: '#1E1E1E',
  tertiary: '#E6EEFF', // Selection
  info: '#002583', // Action/shape hover
  outline: '#B8C4E5', // Outline
};

import Vue from 'vue';
import Vuesax from 'vuesax';

Vue.use(Vuesax, { theme: { colors } });


// CONFIGS
const themeConfig = {
  disableCustomizer: true, // options[Boolean] : true, false(default)
  disableThemeTour: false, // options[Boolean] : true, false(default)
  footerType: 'static', // options[String]  : static(default) / sticky / hidden
  hideScrollToTop: false, // options[Boolean] : true, false(default)
  mainLayoutType: 'vertical', // options[String]  : vertical(default) / horizontal
  navbarColor: '#fff', // options[String]  : HEX color / rgb / rgba / Valid HTML Color name - (default: #fff)
  navbarType: 'floating', // options[String]  : floating(default) / static / sticky / hidden
  routerTransition: 'zoom-fade', // options[String]  : zoom-fade / slide-fade / fade-bottom / fade / zoom-out
  sidebarCollapsed: false, // options[Boolean] : true, false(default)
  theme: 'light', // options[String]  : "light"(default), "dark", "semi-dark"

  // Not required yet - WIP
  userInfoLocalStorageKey: 'userInfo',

  // NOTE: themeTour will be disabled in screens < 1200. Please refer docs for more info.
};

export default themeConfig;
