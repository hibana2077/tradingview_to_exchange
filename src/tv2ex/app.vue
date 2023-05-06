<template>
  <NuxtLayout :name="header">
  </NuxtLayout>
  <NuxtPage />
</template>

<script setup>
const header = 1 ? 'header' : 'header_hero'
</script>