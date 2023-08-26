import Vue from 'vue';

import VueFeather from 'vue-feather';
Vue.use(VueFeather);

import { IconDefinition, library } from '@fortawesome/fontawesome-svg-core'
import {
  faQuestion,
  faServer,
  faPuzzlePiece,
  faVolumeOff,
  faHome,
  faPlayCircle,
  faStopCircle,
  faPauseCircle,
  faSlidersH,
  faMagic,
  faEdit,
  faLeaf,
  faFireAlt,
  faUserSecret,
  faSnowflake,
  faUser,
  faUserAltSlash,
  faDoorOpen,
  faDoorClosed,
  faInbox,
  faCopy,
  faFolderPlus,
  faPlay,
  faLockOpen,
  faUnlock,
  faLock,
  faSave,
  faTint,
  faThermometerFull,
  faThermometerThreeQuarters,
  faThermometerHalf,
  faThermometerQuarter,
  faThermometerEmpty,
  faCloud,
  faChartArea,
  faCheck,
  faBan,
  faEye,
  faEyeSlash,
  faTrashAlt,
  faBatteryFull,
  faBatteryThreeQuarters,
  faBatteryHalf,
  faBatteryQuarter,
  faBatteryEmpty,
  faDatabase,
  faLink,
  faWarehouse,
  faVideo,
  faAngleDoubleRight,
  faLightbulb,
  faToggleOn,
  faPlug,
  faPlugCircleMinus,
  faPlugCircleXmark,
  faExclamationTriangle,
  faSun,
  faCode,
  faBolt,
  faExclamation,
  faTrash,
  faBell,
  faUnlockAlt,
  faKey,
  faTv,
  faVolumeUp,
  faQuestionCircle,
  faFan,
  faFaucet,
  faExternalLinkAlt,
  faSortDown,
  faCodeBranch,
  faHdd,
  faTimes,
  faHistory,
  faCalendarAlt,
  faShieldAlt,
  faWrench,
  faVideoCamera,
  faTimeline,
  faMobile,
  faBoltLightning,
  faFileText,
} from '@fortawesome/free-solid-svg-icons'

import {
  faChrome,
  faGithub,
} from '@fortawesome/free-brands-svg-icons'

const icons: IconDefinition[] =[
  faHistory,
  faQuestion,
  faServer,
  faPuzzlePiece,
  faVolumeOff,
  faHome,
  faPlayCircle,
  faStopCircle,
  faPauseCircle,
  faSlidersH,
  faMagic,
  faEdit,
  faLeaf,
  faFireAlt,
  faUserSecret,
  faChrome,
  faSnowflake,
  faUser,
  faUserAltSlash,
  faDoorOpen,
  faDoorClosed,
  faInbox,
  faCopy,
  faFolderPlus,
  faPlay,
  faUnlockAlt,
  faLockOpen,
  faUnlock,
  faLock,
  faSave,
  faTint,
  faThermometerFull,
  faThermometerThreeQuarters,
  faThermometerHalf,
  faThermometerQuarter,
  faThermometerEmpty,
  faCloud,
  faChartArea,
  faCheck,
  faBan,
  faEye,
  faEyeSlash,
  faTrashAlt,
  faBatteryFull,
  faBatteryThreeQuarters,
  faBatteryHalf,
  faBatteryQuarter,
  faBatteryEmpty,
  faDatabase,
  faLink,
  faWarehouse,
  faGithub,
  faVideo,
  faAngleDoubleRight,
  faLightbulb,
  faToggleOn,
  faPlug,
  faPlugCircleMinus,
  faPlugCircleXmark,
  faExclamationTriangle,
  faSun,
  faCode,
  faBolt,
  faExclamation,
  faTrash,
  faBell,
  faUnlockAlt,
  faKey,
  faTv,
  faVolumeUp,
  faQuestionCircle,
  faFan,
  faFaucet,
  faExternalLinkAlt,
  faSortDown,
  faCodeBranch,
  faHdd,
  faTimes,
  faCalendarAlt,
  faShieldAlt,
  faWrench,
  faVideoCamera,
  faTimeline,
  faMobile,
  faBoltLightning,
  faFileText,
];

for (var icon in icons) {
  library.add(icons[icon])
}

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
Vue.component('font-awesome-icon', FontAwesomeIcon)
