/*
 * @Author: hibana2077 hibana2077@gmail.com
 * @Date: 2023-05-06 13:59:42
 * @LastEditors: hibana2077 hibana2077@gmail.com
 * @LastEditTime: 2023-05-06 14:33:03
 * @FilePath: \tradingview_to_exchange\src\tv2ex\nuxt.config.ts
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    css: [
        "primevue/resources/themes/lara-light-blue/theme.css",
        "primevue/resources/primevue.css",
        "primeicons/primeicons.css",
    ],
	build: {
		transpile: ["primevue"]
	}
})