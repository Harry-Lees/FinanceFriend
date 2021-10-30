<template>
    <nav>
        <div class="px-8 py-2">
            <div class="relative flex items-center justify-between h-14">

                <div class="flex-1 flex items-center justify-center sm:items-stretch sm:justify-start">
                    <div class="flex-shrink-0 flex items-center text-lg text-gray-800"><router-link to="/">Finance Friends</router-link></div>
                </div>

                <div class="flex items-center space-x-16 text-s">
                    <p>about</p>
                    <router-link to="/login">login</router-link>
                    <router-link to="/register" class="py-2 px-4 bg-green-400 rounded-full">register</router-link>
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

    methods: {
        //documentClick(event) {
        //    let elem = this.$refs.dropdownMenu;
        //    let target = event.target;

        //   if ((elem !== target) && !elem.contains(target)) {
        //        this.dropdownOpen = false;
        //    }
        //},
        toggleDropdown() {
            this.dropdownOpen = !this.dropdownOpen;
        }
    },

    created() {
        document.addEventListener("click", this.documentClick);
    },

    unmounted() {
        document.removeEventListener("click", this.documentClick);
    }
}
</script>
