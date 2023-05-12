<!--
 * @Author: hibana2077 hibana2077@gmail.com
 * @Date: 2023-05-06 16:04:00
 * @LastEditors: hibana2077 hibana2077@gmail.com
 * @LastEditTime: 2023-05-12 17:11:57
 * @FilePath: \tradingview_to_exchange\src\tv2ex\pages\index.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
 
<div class="bg-gray-900 py-3 px-6 shadow-2 flex align-items-center justify-content-between relative">
    <img src="../assets/blocks/logos/hyper-light.svg" alt="Image" height="50">
    <a class="cursor-pointer block lg:hidden text-gray-400"
        v-styleclass="{ selector: '@next', enterClass: 'hidden', leaveToClass: 'hidden', hideOnOutsideClick: true }">
        <i class="pi pi-bars text-4xl"></i>
    </a>
    <div class="align-items-center flex-grow-1 justify-content-between hidden lg:flex absolute lg:static w-full bg-gray-900 left-0 top-100 px-6 lg:px-0 shadow-2 lg:shadow-none z-2">
        <section></section>
        <ul class="list-none p-0 m-0 flex lg:align-items-center text-gray-400 select-none flex-column lg:flex-row cursor-pointer">
            <li>
                <a v-ripple class="flex px-0 lg:px-5 py-3 text-gray-200 hover:text-blue-600 font-medium transition-colors transition-duration-150 p-ripple" href="#Features"  style="text-decoration: none ">
                    <span>Features</span>
                </a>
            </li>
            <li>
                <a v-ripple class="flex px-0 lg:px-5 py-3 text-gray-200 hover:text-blue-600 font-medium transition-colors transition-duration-150 p-ripple">
                    <span>Corporate</span>
                </a>
            </li>
            <li>
                <a v-ripple class="flex px-0 lg:px-5 py-3 text-gray-200 hover:text-blue-600 font-medium transition-colors transition-duration-150 p-ripple">
                    <span>Resources</span>
                </a>
            </li>
            <li>
                <a v-ripple class="flex px-0 lg:px-5 py-3 text-gray-200 hover:text-blue-600 font-medium transition-colors transition-duration-150 p-ripple" href="#pricing"  style="text-decoration: none ">
                    <span>Pricing</span>
                </a>
            </li>
        </ul>
        <div class="flex justify-content-between lg:block border-top-1 lg:border-top-none border-gray-800 py-3 lg:py-0 mt-3 lg:mt-0">
            <Button label="Login" class="p-button-text font-bold"></Button>
            <Button label="Register" class="ml-3 font-bold"></Button>
        </div>
    </div>
</div>
<div class="bg-gray-900 px-4 py-8 md:px-6 lg:px-8">
    <div class="flex flex-wrap">
        <div class="w-12 lg:w-6 p-4">
            <h1 class="text-6xl font-bold text-white mt-0 mb-3">Social CRM that helps you grow faster <span class="text-yellow-500 underline">for free</span></h1>
            <p class="text-3xl text-gray-400 mt-0 mb-5">Arcu cursus euismod quis viverra nibh cras. Amet justo donec enim diam vulputate ut.</p>
            <ul class="list-none p-0 m-0">
                <li class="mb-3 flex align-items-center"><i class="pi pi-compass text-yellow-500 text-xl mr-2"></i><span class="text-gray-400 line-height-3">Senectus et netus et malesuada fames.</span></li>
                <li class="mb-3 flex align-items-center"><i class="pi pi-map text-yellow-500 text-xl mr-2"></i><span class="text-gray-400 line-height-3">Orci a scelerisque purus semper eget.</span></li>
                <li class="mb-3 flex align-items-center"><i class="pi pi-calendar text-yellow-500 text-xl mr-2"></i><span class="text-gray-400 line-height-3">Aenean sed adipiscing diam donec adipiscing tristique.</span></li>
            </ul>
            <Button type="button" label="Claim Your Account" class="block mt-7 mb-7 lg:mb-0 p-button-rounded p-button-success p-button-lg font-medium"></Button>
        </div>
        <div class="w-12 lg:w-6 text-center lg:text-right overflow-hidden">
            <img src="../assets/blocks/hero/hero-illustration.svg" alt="Image" class="w-full lg:w-auto">
        </div>
    </div>
</div>
<div class="surface-section px-4 py-8 md:px-6 lg:px-8">
    <div class="flex justify-content-evenly flex-wrap">
        <div class="p-3">
            <img src="../assets/blocks/logos/peak-500.svg" alt="Image" height="50">
        </div>
        <div class="p-3">
            <img src="../assets/blocks/logos/charot-500.svg" alt="Image" height="50">
        </div>
        <div class="p-3">
            <img src="../assets/blocks/logos/hyper-500.svg" alt="Image" height="50">
        </div>
        <div class="p-3">
            <img src="../assets/blocks/logos/hodly-500.svg" alt="Image" height="50">
        </div>
        <div class="p-3">
            <img src="../assets/blocks/logos/franki-500.svg" alt="Image" height="50">
        </div>
    </div>
</div>
<div class="surface-section px-4 py-8 md:px-6 lg:px-8">
    <div class="font-bold text-900 text-3xl mb-3 text-center">Build The Way You Want</div>
    <div class="text-700 text-center mb-3">Risus feugiat in ante metus. Lacus suspendisse faucibus interdum posuere lorem.</div>
    <div class="flex flex-wrap">
        <div class="w-full lg:w-6 xl:w-3 p-5">
            <img src="../assets/blocks/feature/feature-illustration-1.svg" alt="Image" class="w-full">
            <div class="mt-3 mb-2 font-medium text-900 text-xl">Ornare Arcu Odio</div>
            <span class="text-700 line-height-3">Quisque sagittis purus sit amet volutpat consequat mauris nunc. Scelerisque eleifend.</span>
            <a tabindex="0" class="text-blue-500 font-medium flex align-items-center mt-2">
                <span>Explore</span>
                <i class="pi pi-arrow-right ml-3"></i>
            </a>
        </div>
        <div class="w-full lg:w-6 xl:w-3 p-5">
            <img src="../assets/blocks/feature/feature-illustration-2.svg" alt="Image" class="w-full">
            <div class="mt-3 mb-2 font-medium text-900 text-xl">Sem Nulla Pharetra</div>
            <span class="text-700 line-height-3">Quisque sagittis purus sit amet volutpat consequat mauris nunc. Scelerisque eleifend.</span>
            <a tabindex="0" class="text-blue-500 font-medium flex align-items-center mt-2">
                <span>Explore</span>
                <i class="pi pi-arrow-right ml-3"></i>
            </a>
        </div>
        <div class="w-full lg:w-6 xl:w-3 p-5">
            <img src="../assets/blocks/feature/feature-illustration-3.svg" alt="Image" class="w-full">
            <div class="mt-3 mb-2 font-medium text-900 text-xl">Facilisi Etiam Dignissim</div>
            <span class="text-700 line-height-3">Quisque sagittis purus sit amet volutpat consequat mauris nunc. Scelerisque eleifend.</span>
            <a tabindex="0" class="text-blue-500 font-medium flex align-items-center mt-2">
                <span>Explore</span>
                <i class="pi pi-arrow-right ml-3"></i>
            </a>
        </div>
        <div class="w-full lg:w-6 xl:w-3 p-5">
            <img src="../assets/blocks/feature/feature-illustration-4.svg" alt="Image" class="w-full">
            <div class="mt-3 mb-2 font-medium text-900 text-xl">Risus Feugiat In Ante</div>
            <span class="text-700 line-height-3">Quisque sagittis purus sit amet volutpat consequat mauris nunc. Scelerisque eleifend.</span>
            <a tabindex="0" class="text-blue-500 font-medium flex align-items-center mt-2">
                <span>Explore</span>
                <i class="pi pi-arrow-right ml-3"></i>
            </a>
        </div>
    </div>
</div>
<div class="surface-section px-4 py-8 md:px-6 lg:px-8 overflow-hidden">
    <div class="font-bold text-900 text-3xl mb-3 text-center" id="Features">Explore The Features</div>
    <div class="text-700 text-center mb-5 line-height-3">Libero justo laoreet sit amet cursus sit amet dictum. Auctor neque vitae tempus quam pellentesque nec nam.</div>
    <div class="flex lg:justify-content-center mb-5">
        <div class="py-3 pr-8 pl-3 w-30rem hidden lg:block">
            <img src="../assets/blocks/feature/feature-timeline-1.png" alt="Image" class="w-full mr-8">
        </div>
        <div class="flex flex-column align-items-center w-2rem">
            <span class="bg-blue-500 text-0 flex align-items-center justify-content-center border-circle" style="min-width:2.5rem; min-height: 2.5rem">1</span>
            <div class="h-full bg-blue-500" style="width: 2px; min-height: 4rem"></div>
        </div>
        <div class="py-3 pl-5 lg:pl-8 pl-3 lg:w-30rem">
            <div class="text-900 text-xl mb-2 font-medium">Ornare Arcu Odio</div>
            <span class="block text-700 line-height-3 mb-3">Quisque sagittis purus sit amet volutpat consequat mauris nunc. Scelerisque eleifend.</span>
            <div class="pt-3 border-top-1 border-300">
                <div class="mb-2 line-height-3"><span class="text-900 font-medium">Sed lectus vestibulum</span> mattis ullamcorper velit. Laoreet sit amet cursus sit.</div>
                <div class="line-height-3"><span class="text-900 font-medium">Fames ac turpis</span> egestas sed tempus urna et. Cursus turpis massa.</div>
            </div>
            <img src="../assets/blocks/feature/feature-timeline-1.png" alt="Image" class="w-full mt-3 block lg:hidden">
        </div>
    </div>
    <div class="flex justify-content-center mb-5">
        <div class="py-3 pl-5 pr-3 lg:pr-8 lg:pl-3 lg:w-30rem flex-order-1 lg:flex-order-0">
            <div class="text-900 text-xl mb-2 font-medium">A diam maecenas</div>
            <span class="block text-700 line-height-3 mb-3">Amet minim mollit non deserunt ullamco est sit aliqua dolor do amet sint. Velit officia consequat duis enim velit mollit.</span>
            <div class="pt-3 border-top-1 border-300">
                <div class="mb-2 line-height-3"><span class="text-900 font-medium">Quis hendrerit dolor</span> magna eget est. Pellentesque pulvinar pellentesque.</div>
                <div class="line-height-3"><span class="text-900 font-medium">Lectus urna duis</span> convallis convallis tellus id interdum velit laoreet.</div>
            </div>
            <img src="../assets/blocks/feature/feature-timeline-2.png" alt="Image" class="w-full mt-3 block lg:hidden">
        </div>
        <div class="flex flex-column align-items-center w-2rem flex-order-0 lg:flex-order-1">
            <span class="bg-yellow-500 text-0 flex align-items-center justify-content-center border-circle" style="min-width:2.5rem; min-height: 2.5rem">2</span>
            <div class="h-full bg-yellow-500" style="width: 2px; min-height: 4rem"></div>
        </div>
        <div class="py-3 pl-8 pr-3 w-30rem hidden lg:block flex-order-2">
            <img src="../assets/blocks/feature/feature-timeline-2.png" alt="Image" class="w-full mr-8">
        </div>
    </div>
    <div class="flex justify-content-center">
        <div class="py-3 pr-8 pl-3 w-30rem hidden lg:block">
            <img src="../assets/blocks/feature/feature-timeline-3.png" alt="Image" class="w-full mr-8">
        </div>
        <div class="flex flex-column align-items-center w-2rem">
            <span class="bg-cyan-500 text-0 flex align-items-center justify-content-center border-circle" style="min-width:2.5rem; min-height: 2.5rem">3</span>
            <div class="h-full bg-cyan-500" style="width: 2px; min-height: 4rem"></div>
        </div>
        <div class="py-3 pl-5 lg:pl-8 pl-3 lg:w-30rem">
            <div class="text-900 text-xl mb-2 font-medium">Pharetra et ultrices neque</div>
            <span class="block text-700 line-height-3 mb-3">Id interdum velit laoreet id. A iaculis at erat pellentesque adipiscing commodo elit at imperdiet.</span>
            <div class="pt-3 border-top-1 border-300">
                <div class="mb-2 line-height-3"><span class="text-900 font-medium">Egestas dui id</span> ornare arcu odio ut. Mi bibendum neque egestas congue.</div>
                <div class="line-height-3"><span class="text-900 font-medium">Sed velit dignissim</span> sodales ut eu. Massa placerat duis ultricies lacus.</div>
            </div>
            <img src="../assets/blocks/feature/feature-timeline-3.png" alt="Image" class="w-full mt-3 block lg:hidden">
        </div>
    </div>
</div>
<div class="surface-section px-4 py-8 md:px-6 lg:px-8">
    <div class="text-orange-500 text-center mb-3">VITAE TEMPUS QUAM</div>
    <div class="font-bold text-5xl text-900 text-center mb-6">Take your vision to the next level</div>
    <div class="grid grid-nogutter">
        <div class="col-12 md:col-6 lg:col-3 p-3">
            <div class="bg-blue-50 text-center p-5 border-round flex flex-column">
                <i class="text-blue-500 pi pi-play text-4xl block mb-4"></i>
                <span class="text-900 text-5xl">52000</span>
                <div class="text-blue-700 mt-3 font-medium">Streams</div>
            </div>
        </div>
        <div class="col-12 md:col-6 lg:col-3 p-3">
            <div class="bg-purple-50 text-center p-5 border-round flex flex-column">
                <i class="text-purple-500 pi pi-users text-4xl block mb-4"></i>
                <span class="text-900 text-5xl">21000</span>
                <div class="text-purple-700 mt-3 font-medium">Engagement</div>
            </div>
        </div>
        <div class="col-12 md:col-6 lg:col-3 p-3">
            <div class="bg-teal-50 text-center p-5 border-round flex flex-column">
                <i class="text-teal-500 pi pi-camera text-4xl block mb-4"></i>
                <span class="text-900 text-5xl">71.2h</span>
                <div class="text-teal-700 mt-3 font-medium">Watch Time</div>
            </div>
        </div>
        <div class="col-12 md:col-6 lg:col-3 p-3">
            <div class="bg-indigo-50 text-center p-5 border-round flex flex-column">
                <i class="text-indigo-500 pi pi-thumbs-up text-4xl block mb-4"></i>
                <span class="text-900 text-5xl">4500</span>
                <div class="text-indigo-700 mt-3 font-medium">Likes</div>
            </div>
        </div>
    </div>
</div>
<div class="surface-ground px-4 py-8 md:px-6 lg:px-8">
    <div class="flex flex-wrap relative overflow-hidden" style="border-radius:1rem; background:radial-gradient(100% 1126.49% at 100% 0%, rgba(106, 200, 212, 0.4) 0%, rgba(33, 33, 33, 0) 100%), #212121;">
        <div class="px-6 py-8">
            <span class="uppercase text-cyan-500 font-bold">BE THE FIRST ONE</span>
            <div class="text-white text-medium text-5xl mt-3 mb-5">Join the waitlist Today!</div>
            <button v-ripple class="appearance-none p-3 bg-cyan-500 hover:bg-cyan-300 cursor-pointer font-medium gray-900 border-none p-component transition-colors transition-duration-150 p-ripple" style="border-radius: 35px">Reserve Your Username</button>
        </div>
            
        <img src="../assets/blocks/cta/cta-browser.png" alt="Image" class="static lg:absolute block mx-auto" style="height: 400px; top: -2rem; right: -1rem">
    </div>
</div>
<div class="surface-section px-4 py-8 md:px-6 lg:px-8" id="pricing">
    <div class="overflow-x-auto">
        <table class="w-full white-space-nowrap" style="border-collapse: collapse; border-spacing: 0">
            <thead>
                <tr>
                    <td class="surface-100 p-3">
                        <div class="text-3xl text-900 mb-2">Pricing</div>
                        <span class="text-600 line-height-3">Fringilla est ullamcorper eget nulla facilisi etiam</span>
                    </td>
                    <td class="surface-100 p-3 text-center">
                        <div class="text-900 text-xl font-medium mb-3">Basic</div>
                        <div class="text-600 mb-3"><span class="text-3xl text-900">$5</span> /month</div>
                        <Button type="button" class="p-button-rounded" label="Free Trial"></Button>
                    </td>
                    <td class="surface-100 p-3 text-center">
                        <div class="text-900 text-xl font-medium mb-3">Premium</div>
                        <div class="text-600 mb-3"><span class="text-3xl text-900">$9</span> /month</div>
                        <Button type="button" class="p-button-rounded" label="Buy Now"></Button>
                    </td>
                    <td class="surface-100 p-3 text-center">
                        <div class="text-900 text-xl font-medium mb-3">Enterprise</div>
                        <div class="text-600 mb-3"><span class="text-3xl text-900">$12</span> /month</div>
                        <Button type="button" class="p-button-rounded p-button-outlined" label="Contact Us"></Button>
                    </td>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="p-3 text-900 font-medium border-bottom-1 border-200">Arcu purus</td>
                    <td class="text-center p-medium border-bottom-1 border-200"><i class="text-green-500 pi pi-check"></i></td>
                    <td class="text-center p-medium border-bottom-1 border-200"><i class="text-green-500 pi pi-check"></i></td>
                    <td class="text-center p-medium border-bottom-1 border-200"><i class="text-green-500 pi pi-check"></i></td>
                </tr>
                <tr>
                    <td class="p-3 text-900 font-medium border-bottom-1 border-200">Posuere felis</td>
                    <td class="text-center p-medium border-bottom-1 border-200"><i class="text-green-500 pi pi-check"></i></td>
                    <td class="text-center p-medium border-bottom-1 border-200"><i class="text-green-500 pi pi-check"></i></td>
                    <td class="text-center p-medium border-bottom-1 border-200"><i class="text-green-500 pi pi-check"></i></td>
                </tr>
                <tr>
                    <td class="p-3 text-900 font-medium border-bottom-1 border-200">Curabitur mollis</td>
                    <td class="text-center p-medium border-bottom-1 border-200"><i class="text-green-500 pi pi-check"></i></td>
                    <td class="text-center p-medium border-bottom-1 border-200"><i class="text-green-500 pi pi-check"></i></td>
                    <td class="text-center p-medium border-bottom-1 border-200"><i class="text-green-500 pi pi-check"></i></td>
                </tr>
                <tr>
                    <td class="p-3 text-900 font-medium border-bottom-1 border-200">Vitae odio</td>
                    <td class="text-center p-medium border-bottom-1 border-200"><i class="text-green-500 pi pi-check"></i></td>
                    <td class="text-center p-medium border-bottom-1 border-200"><i class="text-green-500 pi pi-check"></i></td>
                    <td class="text-center p-medium border-bottom-1 border-200"><i class="text-green-500 pi pi-check"></i></td>
                </tr>
                <tr>
                    <td class="p-3 text-900 font-medium border-bottom-1 border-200">Orci, mi</td>
                    <td class="text-center p-medium border-bottom-1 border-200"><i class="text-500 pi pi-times"></i></td>
                    <td class="text-center p-medium border-bottom-1 border-200"><i class="text-green-500 pi pi-check"></i></td>
                    <td class="text-center p-medium border-bottom-1 border-200"><i class="text-green-500 pi pi-check"></i></td>
                </tr>
                <tr>
                    <td class="p-3 text-900 font-medium border-bottom-1 border-200">Tincidunt vulputate</td>
                    <td class="text-center p-medium border-bottom-1 border-200"><i class="text-500 pi pi-times"></i></td>
                    <td class="text-center p-medium border-bottom-1 border-200"><i class="text-500 pi pi-times"></i></td>
                    <td class="text-center p-medium border-bottom-1 border-200"><i class="text-green-500 pi pi-check"></i></td>
                </tr>
                <tr>
                    <td class="p-3 text-900 font-medium border-bottom-1 border-200">Quis felis</td>
                    <td class="text-center p-medium border-bottom-1 border-200"><i class="text-500 pi pi-times"></i></td>
                    <td class="text-center p-medium border-bottom-1 border-200"><i class="text-500 pi pi-times"></i></td>
                    <td class="text-center p-medium border-bottom-1 border-200"><i class="text-green-500 pi pi-check"></i></td>
                </tr>
                <tr>
                    <td class="p-3 text-900 font-medium border-bottom-1 border-200">Dignissim vivamus</td>
                    <td class="text-center text-600 border-bottom-1 border-200">Up to <span class="text-900">5</span> files</td>
                    <td class="text-center text-600 border-bottom-1 border-200">Up to <span class="text-900">10</span> files</td>
                    <td class="text-center text-900 border-bottom-1 border-200">Unlimited</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
<div class="surface-section px-4 py-8 md:px-6 lg:px-8">
    <div class="flex align-items-start lg:align-items-center lg:justify-content-between pb-5 border-bottom-1 border-300 flex-column lg:flex-row">
        <div class="pr-0 lg:pr-8">
            <img src="../assets/blocks/logos/bastion-700.svg" alt="Image" height="50">
            <p class="text-600 line-height-3 text-xl mb-0 mt-5">Consequat nisl vel pretium lectus quam. Scelerisque eu ultrices vitae auctor eu augue ut lectus arcu. Integer quis auctor elit sed.</p>
        </div>
        <Button label="Get Started" class="mt-5 lg:mt-0 white-space-nowrap min-w-max"></Button>
    </div>
    <div class="py-5 border-bottom-1 border-300">
        <div class="grid">
            <div class="col-12 sm:col-6 md:col-4 lg:col-2">
                <span class="text-900 block font-bold line-height-3 mb-3">Company</span>
                <ul class="list-none p-0 m-0">
                    <li class="mb-2"><a class="text-700 cursor-pointer line-height-3">About Us</a></li>
                    <li class="mb-2"><a class="text-700 cursor-pointer line-height-3">News</a></li>
                    <li class="mb-2"><a class="text-700 cursor-pointer line-height-3">Investor Relations</a></li>
                    <li class="mb-2"><a class="text-700 cursor-pointer line-height-3">Careers</a></li>
                    <li class="mb-2"><a class="text-700 cursor-pointer line-height-3">Media Kit</a></li>
                </ul>
            </div>
            <div class="col-12 sm:col-6 md:col-4 lg:col-2">
                <span class="text-900 block font-bold line-height-3 mb-3">Resources</span>
                <ul class="list-none p-0 m-0">
                    <li class="mb-2"><a class="text-700 cursor-pointer line-height-3">Get Started</a></li>
                    <li class="mb-2"><a class="text-700 cursor-pointer line-height-3">Learn</a></li>
                    <li class="mb-2"><a class="text-700 cursor-pointer line-height-3">Case Studies</a></li>
                </ul>
            </div>
            <div class="col-12 sm:col-6 md:col-4 lg:col-2">
                <span class="text-900 block font-bold line-height-3 mb-3">Developer</span>
                <ul class="list-none p-0 m-0">
                    <li class="mb-2"><a class="text-700 cursor-pointer line-height-3">Courses</a></li>
                    <li class="mb-2"><a class="text-700 cursor-pointer line-height-3">Documentation</a></li>
                    <li class="mb-2"><a class="text-700 cursor-pointer line-height-3">API Reference</a></li>
                    <li class="mb-2"><a class="text-700 cursor-pointer line-height-3">Status</a></li>
                    <li class="mb-2"><a class="text-700 cursor-pointer line-height-3">Papers</a></li>
                    <li class="mb-2"><a class="text-700 cursor-pointer line-height-3">Development Blog</a></li>
                </ul>
            </div>
            <div class="col-12 sm:col-6 md:col-4 lg:col-2">
                <span class="text-900 block font-bold line-height-3 mb-3">Community</span>
                <ul class="list-none p-0 m-0">
                    <li class="mb-2"><a class="text-700 cursor-pointer line-height-3">Discord</a></li>
                    <li class="mb-2"><a class="text-700 cursor-pointer line-height-3">Events</a></li>
                    <li class="mb-2"><a class="text-700 cursor-pointer line-height-3">FAQ</a></li>
                    <li class="mb-2"><a class="text-700 cursor-pointer line-height-3">Blog</a></li>
                </ul>
            </div>
            <div class="col-12 sm:col-6 md:col-4 lg:col-2">
                <span class="text-900 block font-bold line-height-3 mb-3">Connect</span>
                <ul class="list-none p-0 m-0">
                    <li class="mb-2"><a class="text-700 cursor-pointer line-height-3">Newsletters</a></li>
                    <li class="mb-2"><a class="text-700 cursor-pointer line-height-3">Press</a></li>
                    <li class="mb-2"><a class="text-700 cursor-pointer line-height-3">Code of Conduct</a></li>
                    <li class="mb-2"><a class="text-700 cursor-pointer line-height-3">Security Guide</a></li>
                    <li class="mb-2"><a class="text-700 cursor-pointer line-height-3">Bug Bounty</a></li>
                </ul>
            </div>
            <div class="col-12 sm:col-6 md:col-4 lg:col-2">
                <span class="text-900 block font-bold line-height-3 mb-3">Legal</span>
                <ul class="list-none p-0 m-0">
                    <li class="mb-2"><a class="text-700 cursor-pointer line-height-3">Brand Policy</a></li>
                    <li class="mb-2"><a class="text-700 cursor-pointer line-height-3">Privacty Policy</a></li>
                    <li class="mb-2"><a class="text-700 cursor-pointer line-height-3">Terms of Service</a></li>
                </ul>
            </div>
        </div>
    </div>
    <div class="flex justify-content-between align-items-center py-5">
        <span>&copy; {{ year }} Bastion Tech</span>
        <div class="flex align-items-center justify-content-between">
            <a class="cursor-pointer text-500 md:ml-3 ml-2">
                <i class="pi pi-twitter text-xl"></i>
            </a>
            <a class="cursor-pointer text-500 md:ml-3 ml-2">
                <i class="pi pi-facebook text-xl"></i>
            </a>
            <a class="cursor-pointer text-500 md:ml-3 ml-2">
                <i class="pi pi-github text-xl"></i>
            </a>
        </div>
    </div>
</div>
</template>

<script setup>
const year = new Date().getFullYear();


</script>

<style>
body {
    font-family: var(--font-family);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}
</style>