<template>
    <navbar />

    <section class="w-full flex justify-center">
        <div class="relative w-full max-w-6xl">
            <img class="object-cover w-full rounded-xl h-96" src="@/assets/images/exposure.png">
            <div class="absolute w-full py-2 bottom-1/3 inset-x-20 flex flex-col space-y-4">
                <h1 class="text-6xl text-white filter drop-shadow-xl">Take control of <br>your money</h1>
                <div>
                    <router-link to="/register" class="rounded py-2 px-4 bg-green-400 text-white mt-4">Get Started</router-link>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
import Navbar from "@/components/Navbar.vue";

export default {
    name: 'Home',
    components: {
        Navbar,
    },
}
</script>
