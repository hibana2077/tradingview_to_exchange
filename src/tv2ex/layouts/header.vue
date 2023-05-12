<!--
 * @Author: hibana2077 hibana2077@gmail.com
 * @Date: 2023-05-06 15:49:45
 * @LastEditors: hibana2077 hibana2077@gmail.com
 * @LastEditTime: 2023-05-12 08:26:44
 * @FilePath: \tradingview_to_exchange\src\tv2ex\layouts\header.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->

<template>
    <MegaMenu :model="items" orientation="horizontal">
    <template #start>
        <span class="flex align-items-center">
            <img alt="logo" src="../assets/logo.svg" height="48" class="mr-2" />
        </span>
    </template>
    <template #item="{ item }">
        <span class="flex align-items-center justify-content-start">
            <NuxtLink :to="item.url" class="flex align-items-center justify-content-start" style="color: black; text-decoration: none">
                <i :class="item.icon" class="mr-2"></i>
                {{ item.label }} &nbsp;
            </NuxtLink>
        </span>
    </template>
    <template #end>
        <Avatar label="L" class="mr-2" style="background-color:#9c27b0; color: #ffffff" shape="circle" />
    </template>
  </MegaMenu>
  <slot />
</template>
  
  <script setup>
  
  const items = ref([
    {
        label: 'Pricing',
        icon: 'pi pi-fw pi-money-bill',
        url: '/pricing'
    },
    {
        label: 'Contacts',
        icon: 'pi pi-fw pi-users',
        url: '/contacts'
    },
    {
        label: 'Events',
        icon: 'pi pi-fw pi-calendar',
        url: '/events'
    }
  ]);
  </script>