<template>
   <div v-if="chartData.length" class="h-96">
        <vue3-chart-js :type="chartType" :data="barChart" id="bar" :options='chartOptions' />
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
            chartType: "line",
            chartOptions: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }

                },
            }
        }
    },

    mounted() {
        this.getChartData();
    },

    methods: {
        getChartData() {
            this.$axios.get('/spending_by_day', {params: { account_id: 28 }})
            .then((response) => {
                this.chartData = response.data;
            })
        },
    },

    computed: {
        labels() {
            return this.chartData.map(row => row.date_trunc)
        },

        data() {
            return this.chartData.map(row => row.sum)
        },

        barChart() {
            return {
                labels: this.labels,
                datasets: [
                    {
                        data: this.data,
                        backgroundColor: ['#94D2BD', '#69D6CB', '#34D5EB', '#249AD4', '#2A88F7'],
                        borderColor: ['#94D2BD', '#69D6CB', '#34D5EB', '#249AD4', '#2A88F7'],
                    },
                ],
            }
        },
    }
};
</script>

