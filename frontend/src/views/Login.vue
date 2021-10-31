<template>
    <main class="flex flex-col h-screen">
        <navbar />

        <div class="flex flex-col justify-center items-center flex-grow space-y-6">
            <div class="flex flex-col justify-center space-y-2">
                <img src="@/assets/logo.svg" class="h-20">
                <p class="tracking-widest">Finance Friend</p>
            </div>
            <form @submit="submitLogin" class="flex flex-col space-y-4 w-1/4">
                <input v-model.trim='username' class="p-2 border rounded" type="text" id="username" placeholder="Username" />
                <input v-model.trim='password' class="p-2 border rounded" type="password" id="password" placeholder="Password" />
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
    },

    data() {
        return {
            username: '',
            password: '',
            token: '',
        }
    },

    methods: {
        submitLogin(event) {
            event.preventDefault();

            const payload = new FormData();
            payload.append('username', this.username);
            payload.append('password', this.password);

            this.$axios.post('/token', payload)
            .then((response) => {
                this.token = response.data;
                this.$axios.get('/users/me', {params: {token: localStorage.token}, headers: {Authorization: `Bearer ${this.token.access_token}`}})
                .then((response) => {
                    localStorage.user_id = response.data.user_id;
                    this.$router.push('/insights');
                })
            })
            .catch((error) => {
                alert('an unexpected error occurred');
            })

        },
    }
}
</script>
