<!--
 * @Author: hibana2077 hibana2077@gmail.com
 * @Date: 2023-05-12 08:32:27
 * @LastEditors: hibana2077 hibana2077@gmail.com
 * @LastEditTime: 2023-05-12 09:37:30
 * @FilePath: \tradingview_to_exchange\src\tv2ex\pages\[...slug].vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE"
-->
<template>
  
<div class="surface-section px-8 py-8 md:px-8 lg:px-8 flex justify-content-center align-items-center">
    <div class="flex flex-column lg:flex-row justify-content-center align-items-center gap-8">
        <div class="text-center lg:text-right">
            <div class="mt-6 mb-3 font-bold text-6xl text-900">Are you lost?</div>
            <p class="text-700 text-3xl mt-0 mb-6">Sorry, we couldn't find the page.</p>
            <NuxtLink to="/" class="p-button-outlined">
              <Button type="button" label="Go back to home page" class="p-button-outlined"></Button>
            </NuxtLink>
        </div>
        <div>
            <img src="../assets/images/404-rocket.png" alt="Image" class="w-full md:w-28rem" />
        </div>
    </div>
</div>
</template>
  
<script setup>
  setResponseStatus(404)
</script>