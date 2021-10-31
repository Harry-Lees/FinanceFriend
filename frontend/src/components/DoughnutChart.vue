<template>
    <div v-if="chartData.length">
        <vue3-chart-js :type="chartType" :data="doughnutChart" :options="chartOptions" id="doughnut" />
    </div>
</template>

<script>
import Vue3ChartJs from "@j-t-mcc/vue3-chartjs";

export default {
    name: "App",

    components: {
        Vue3ChartJs,
    },

    data() {
        return {
            chartData: [],
            chartType: "doughnut",
            chartOptions: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'left',
                    },
                }
            }
        }
    },

    mounted() {
        this.getChartData();
    },

    methods: {
        getChartData() {
            this.$axios.get('/spending_by_category', {params: { account_id: localStorage.user_id }})
            .then((response) => {
                this.chartData = response.data;
            })
        },
    },

    computed: {
        labels() {
            return this.chartData.map(row => row.category)
        },

        data() {
            return this.chartData.map(row => row.round)
        },

        doughnutChart() {
            return {
                labels: this.labels,
                datasets: [
                    {
                        data: this.data,
                        backgroundColor: ['#94D2BD', '#69D6CB', '#34D5EB', '#249AD4', '#2A88F7'],
                    },
                ],
            }
        }
    }
};
</script>

