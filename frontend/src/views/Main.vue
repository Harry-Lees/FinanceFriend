<template>
    <main class="flex flex-col h-screen">
        <navbar />

        <component :is="activeComponent"></component>
    </main>
</template>

<script>
import Navbar from "@/components/Navbar.vue";
import InputDetails from "@/components/InputDetails.vue";
import Insights from "@/components/Insights.vue";

export default {
    components: {
        Navbar,
        InputDetails,
        Insights,
    },

    data() {
        return {
            activeComponent: 'insights',
        }
    }
}
</script>
