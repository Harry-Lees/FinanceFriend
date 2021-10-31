<template>
    <section class="flex justify-center w-full">
        <div class="flex-flex-col w-full max-w-6xl">
            <h1 class="text-3xl font-bold">Where you spend your money</h1>
            <div class="border shadow-md rounded mt-4">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr class="text-left">
                            <th class="px-6 py-4">Merchant</th>
                            <th class="px-6 py-4">Net Spend</th>
                            <th class="px-6 py-4">Num Visits</th>
                        </tr>
                    </thead>

                    <tbody class="bg-white divide-y divide-gray-200 p-2">
                        <tr v-for="merchant in topMerchants" :key="merchant.merchant">
                            <td class="px-6 py-4 whitespace-nowrap">{{ merchant.merchant }}</td>
                            <td class="px-6 py-4 whitespace-nowrap">£{{ merchant.net_spend }}</td>
                            <td class="px-6 py-4 whitespace-nowrap">{{ merchant.visits }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </section>
</template>

<script>
export default {
    data() {
        return {
            topMerchants: [],
            roundedSavings: 0,
        }
    },

    mounted() {
        this.getTopMerchants();
        this.getRoundedSavings();
        console.log('here');
    },

    methods: {
        getTopMerchants() {
            this.$axios.get('/top_merchants', {params: {account_id: 28}})
            .then((result) => {
                this.topMerchants = result.data;
            })
        },

        getRoundedSavings() {
            this.$axios.get('/tip_jar', { params: { account_id: 28 } })
            .then((result) => {
                this.roundedSavings = result.data;
            })
        },
    }
}
</script>

<style scoped>
.card {
    @apply rounded border w-full p-4
}

.title {
    @apply text-3xl font-semibold
}
</style>
