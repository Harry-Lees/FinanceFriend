<template>
    <nav>
        <div class="px-8 py-2">
            <div class="relative flex items-center justify-between h-14">

                <div class="flex-1 flex items-center justify-center sm:items-stretch sm:justify-start">
                    <div class="flex-shrink-0 flex items-center text-lg text-gray-800"><router-link to="/">Finance Friend</router-link></div>
                </div>

                <router-link v-if="loggedIn" to="/logout" class="hover:text-green-500">logout</router-link>
                <div v-else class="flex items-center space-x-12 text-s">
                    <router-link to="/login" class="hover:text-green-500">login</router-link>
                    <router-link to="/register" class="hover:text-green-500">register</router-link>
                </div>
            </div>
        </div>
    </nav>
</template>

<script>
export default {
    data() {
        return {
            dropdownOpen: false,
        }
    },

    computed: {
        loggedIn() {
            if (localStorage.user_id) {
                return true
            }
            return false
        }
    }
}
</script>
