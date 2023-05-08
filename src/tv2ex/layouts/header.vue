<!--
 * @Author: hibana2077 hibana2077@gmail.com
 * @Date: 2023-05-06 15:49:45
 * @LastEditors: hibana2077 hibana2077@gmail.com
 * @LastEditTime: 2023-05-08 07:45:03
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
        items: []
    },
    {
        label: 'Contacts',
        icon: 'pi pi-fw pi-users',
        items: [
            [
                {
                    label: 'Discord'
                },
                {
                    label: 'Telegram'
                },
                {
                    label: 'Twitter'
                }

            ]
        ]
    },
    {
        label: 'Events',
        icon: 'pi pi-fw pi-calendar',
        items: [
            [
                {
                    label: 'Event 1',
                    items: [{ label: 'Event 1.1' }, { label: 'Event 1.2' }]
                },
                {
                    label: 'Event 2',
                    items: [{ label: 'Event 2.1' }, { label: 'Event 2.2' }]
                }
            ],
            [
                {
                    label: 'Event 3',
                    items: [{ label: 'Event 3.1' }, { label: 'Event 3.2' }]
                },
                {
                    label: 'Event 4',
                    items: [{ label: 'Event 4.1' }, { label: 'Event 4.2' }]
                }
            ]
        ]
    }
  ]);
  </script>