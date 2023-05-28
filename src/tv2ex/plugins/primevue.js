/*
 * @Author: hibana2077 hibana2077@gmail.com
 * @Date: 2023-05-06 14:12:30
 * @LastEditors: hibana2077 hibana2077@gmail.com
 * @LastEditTime: 2023-05-28 20:27:57
 * @FilePath: \tradingview_to_exchange\src\tv2ex\plugins\primevue.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
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
import Ripple from 'primevue/ripple';
import Checkbox from 'primevue/checkbox';
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
    nuxtApp.vueApp.component('Checkbox', Checkbox)
    nuxtApp.vueApp.directive('ripple', Ripple)
    //other components that you need
})