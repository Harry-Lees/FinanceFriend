<template>
    <section class="flex justify-center w-full">
        <div class="flex-flex-col w-full max-w-6xl space-y-6">
            <div class="card">
                <h1 class="text-3xl font-bold">Where you spend your money</h1>
                <div class="rounded mt-4">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead>
                            <tr class="text-left">
                                <th class="px-6 py-4">Merchant</th>
                                <th class="px-6 py-4">Net Spend</th>
                                <th class="px-6 py-4">Num. Visits</th>
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

            <div class="card cursor-pointer">
                <a class="flex" href="https://www.savethestudent.org/make-money/how-where-to-invest-money.html">
                    <div>
                        <h1 class="text-3xl font-bold">How to Grow your wealth through investments</h1>
                        <small>External Article</small>
                    </div>

                    <img src="https://www.savethestudent.org/uploads/Stock-market-shares-investing-tracking-prices.jpg" class="rounded-xl">
                </a>
            </div>

            <div class="card">
                <h1 class="text-3xl font-bold mb-2">What you spend money on</h1>
                <doughnut-chart />
            </div>
          
            <div class="card cursor-pointer">
                <a class="flex justify-between" href="https://medium.com/@victoria_h/a-simple-guide-to-weekly-meal-prep-meal-planning-e0d962062618">
                    <img class="rounded-xl h-96" src="https://miro.medium.com/max/1400/1*SyURL-68M-_PQY1Ht22rIA.jpeg">
                
                    <div>
                        <h1 class="text-3xl font-bold">A simple guide to weekly meal prep</h1>
                        <small>External Article</small>
                    </div>
                </a>
            </div>

            <div class="card">
                <h1 class="text-3xl font-bold mb-2">When you spend money</h1> 
                <bar-chart />
            </div>

            <div class="card">
                <h1 class="text-3xl font-bold mb-2">Your spending habits around food</h1>
                <table class="w-full">
                    <thead>
                        <tr class="text-left">
                            <th class="px-6 py-4">Meal</th>
                            <th class="px-6 py-4">Number of purchases</th>
                            <th class="px-6 py-4">Net Spend</th>
                        </tr>
                    </thead>
 
                    <tbody class="bg-white divide-y divide-gray-200 p-2">
                        <tr v-for="row in foodSpending" :key="row.meal">
                            <td class="px-6 py-4 whitespace-nowrap">{{ row.meal }}</td>
                            <td class="px-6 py-4 whitespace-nowrap">{{ row.count }}</td>
                            <td class="px-6 py-4 whitespace-nowrap">£{{ row.spend }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </section>
</template>

<script>
import DoughnutChart from "@/components/DoughnutChart.vue";
import BarChart from "@/components/BarChart.vue";

export default {
    components: {
        DoughnutChart,
        BarChart,
    },

    data() {
        return {
            topMerchants: [],
            roundedSavings: 0,
            foodSpending: {},
        }
    },

    mounted() {
        this.getTopMerchants();
        this.getRoundedSavings();
        this.getFoodSpending();
        console.log('here');
    },

    methods: {
        getTopMerchants() {
            this.$axios.get('/top_merchants', {params: {account_id: localStorage.user_id}})
            .then((result) => {
                this.topMerchants = result.data;
            })
        },

        getRoundedSavings() {
            this.$axios.get('/tip_jar', { params: { account_id: localStorage.user_id } })
            .then((result) => {
                this.roundedSavings = result.data;
            })
        },

        getFoodSpending() {
            this.$axios.get('/dinner_food_spend', { params: { account_id: localStorage.user_id } })
            .then((result) => {
                this.foodSpending = result.data;
            })
        },
    }
}
</script>

<style scoped>
.card {
    @apply rounded-xl border w-full p-12 shadow-md
}

.title {
    @apply text-3xl font-semibold
}
</style>
