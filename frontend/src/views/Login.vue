<template>
    <main class="flex flex-col h-screen">
        <navbar />

        <div class="flex flex-col justify-center items-center flex-grow">
            <form class="flex flex-col space-y-4 w-1/4">
                <input class="p-2 border rounded" type="text" id="username" placeholder="Username" />
                <input class="p-2 border rounded" type="password" id="password" placeholder="Password" />
                <input class="p-2 border rounded cursor-pointer" type="submit" id="submit" value="Login" />
            </form>
            <small class="w-1/4 text-left mt-2 text-gray-500">Don't have an account? Click <router-link class="text-blue-500" to="/register">Here</router-link> to register</small>
        </div>
    </main>
</template>

<script>
import Navbar from "@/components/Navbar.vue";

export default {
    components: {
        Navbar,
    }
}
</script>
