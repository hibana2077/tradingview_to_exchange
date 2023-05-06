import PrimeVue from 'primevue/config'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Toast from 'primevue/toast'
import ToastService from 'primevue/toastservice'
import Editor from 'primevue/editor';
import Card from 'primevue/card';
import Accordion from 'primevue/accordion';
import AccordionTab from 'primevue/accordiontab';
import MegaMenu from 'primevue/megamenu';
import Avatar from 'primevue/avatar';
import AvatarGroup from 'primevue/avatargroup';   //Optional for grouping
//ToastService is a virable name that you can change it to any name you want

export default defineNuxtPlugin(nuxtApp => {
    nuxtApp.vueApp.use(PrimeVue, { ripple: true })
    nuxtApp.vueApp.use(ToastService)
    nuxtApp.vueApp.component('Button', Button)
    nuxtApp.vueApp.component('InputText', InputText)
    nuxtApp.vueApp.component('Toast', Toast)
    nuxtApp.vueApp.component('Editor', Editor)
    nuxtApp.vueApp.component('Card', Card)
    nuxtApp.vueApp.component('Accordion', Accordion)
    nuxtApp.vueApp.component('AccordionTab', AccordionTab)
    nuxtApp.vueApp.component('MegaMenu', MegaMenu)
    nuxtApp.vueApp.component('Avatar', Avatar)
    nuxtApp.vueApp.component('AvatarGroup', AvatarGroup)
    //other components that you need
})