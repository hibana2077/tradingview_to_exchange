<!--
 * @Author: hibana2077 hibana2077@gmail.com
 * @Date: 2023-05-12 17:19:31
 * @LastEditors: hibana2077 hibana2077@gmail.com
 * @LastEditTime: 2023-05-12 17:43:48
 * @FilePath: \tradingview_to_exchange\src\tv2ex\pages\login.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
<div class="flex justify-content-center align-items-center" style="height: 100vh">
    <div class="surface-card p-4 shadow-2 border-round w-full lg:w-6">
        <div class="text-center mb-5">
            <img src="../assets/blocks/logos/hyper.svg" alt="Image" height="50" class="mb-3">
            <div class="text-900 text-3xl font-medium mb-3">Welcome Back</div>
            <span class="text-600 font-medium line-height-3">Don't have an account?</span>
            <a class="font-medium no-underline ml-2 text-blue-500 cursor-pointer">Create today!</a>
        </div>

        <div>
            <label for="email1" class="block text-900 font-medium mb-2">Email</label>
            <InputText id="email1" type="text" placeholder="Email address" class="w-full mb-3" />

            <label for="password1" class="block text-900 font-medium mb-2">Password</label>
            <InputText id="password1" type="password" placeholder="Password" class="w-full mb-3" />

            <div class="flex align-items-center justify-content-between mb-6">
                <div class="flex align-items-center">
                    <Checkbox id="rememberme1" :binary="true" v-model="checked1" class="mr-2"></Checkbox>
                    <label for="rememberme1">Remember me</label>
                </div>
                <a class="font-medium no-underline ml-2 text-blue-500 text-right cursor-pointer">Forgot password?</a>
            </div>

            <Button label="Sign In" icon="pi pi-user" class="w-full"></Button>
        </div>
    </div>
</div>
</template>

<script setup>

const checked1 = ref(false);

</script>

<style scoped>
.background {
    background-color: #fff;
}
</style>