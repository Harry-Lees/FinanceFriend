<template>
    <main class="flex flex-col h-screen">
        <navbar />

        <div class="flex flex-col justify-center items-center flex-grow space-y-6">
            <div class="flex flex-col justify-center space-x-2">
                <img src="@/assets/logo.svg" class="h-20">
                <p class="tracking-widest">Finance Friend</p>
            </div>
            <form @submit="submitRegistration" class="flex flex-col space-y-4 w-1/4">
                <input v-model.trim="username" required class="p-2 border rounded" type="text" id="username" placeholder="Username" />
                <input v-model.trim="password" required class="p-2 border rounded" type="password" id="password" placeholder="Password" />
                <input required class="p-2 border rounded" type="password" id="confirm-password" placeholder="Confirm Password" />
                <input class="p-2 border rounded cursor-pointer hover:bg-green-500 hover:text-white duration-100" type="submit" id="submit" value="Register" />
            </form>
            <small class="w-1/4 text-left mt-2 text-gray-500">Already have an account? Click <router-link class="text-blue-500" to="/login">Here</router-link> to login</small>
        </div>
    </main>
</template>

<script>
import Navbar from "@/components/Navbar.vue";

export default {
    components: {
        Navbar,
    },

    methods: {
        submitRegistration(event) {
            event.preventDefault();
            let params = {
                username: this.username,
                password: this.password,
            }

            this.$axios.put('/user', {}, { params: params })
            .then(() => {
                alert('successfully created account');
                this.$router.push('/login');
            })
            .catch(() => {
                alert('an unexpected error occurred');
            })
        },
    }
}
</script>
