<template>
    <main class="flex flex-col h-screen">
        <navbar />

        <component :is="activeComponent"></component>
    </main>
</template>

<script>
import Navbar from "@/components/Navbar.vue";
import InputDetails from "@/components/InputDetails.vue";

export default {
    components: {
        Navbar,
        InputDetails,
    },

    data() {
        return {
            activeComponent: 'input-details',
        }
    }
}
</script>
