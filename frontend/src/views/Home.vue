<template>
    <navbar />

    <section class="w-full flex justify-center">
        <div class="relative w-full max-w-screen-5xl">
            <img class="object-cover w-full rounded-xl" style="height: 710px" src="@/assets/images/cta.jpg">
            <h1 class="absolute w-full py-2 bottom-2/3 inset-x-20 text-6xl text-white filter drop-shadow-xl">Take control of <br>your money</h1>
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
