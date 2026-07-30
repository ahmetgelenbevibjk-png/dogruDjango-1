import {createI18n} from 'vue-i18n'
import tr from './locales/tr'
import en from './locales/en'

const messages= {
    tr,
    en
}

const i18n=createI18n({
    legacy: false,
    locale:'tr',
    fallbackLocale:'tr',
    messages
})

export default i18n