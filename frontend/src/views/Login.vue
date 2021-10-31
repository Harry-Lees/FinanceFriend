<template>
    <main class="flex flex-col h-screen">
        <navbar />

        <div class="flex flex-col justify-center items-center flex-grow space-y-6">
            <div class="flex flex-col justify-center space-y-2">
                <img src="@/assets/logo.svg" class="h-20">
                <p class="tracking-widest">Finance Friend</p>
            </div>
            <form class="flex flex-col space-y-4 w-1/4">
                <input class="p-2 border rounded" type="text" id="username" placeholder="Username" />
                <input class="p-2 border rounded" type="password" id="password" placeholder="Password" />
                <input class="p-2 border rounded cursor-pointer hover:bg-green-500 hover:text-white duration-200" type="submit" id="submit" value="Login" />
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
