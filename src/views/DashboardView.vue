<!-- src/views/DashboardView.vue -->
<template>
  <v-container fluid class="pa-4 pa-md-6 dashboard-bg">
    <!-- Row 1: Welcome Header -->
    <v-row>
      <v-col>
        <h1 class="text-h4 font-weight-bold">Welcome back, {{ user.name }}!</h1>
        <p class="text-grey-darken-1">Here is your financial summary for this month.</p>
      </v-col>
    </v-row>

    <!-- Row 2: Key Metrics -->
    <v-row>
      <v-col v-for="metric in keyMetrics" :key="metric.title" cols="12" md="4">
        <v-card class="elevation-2 fill-height">
          <v-card-text>
            <div class="d-flex align-center">
              <v-icon :color="metric.color" size="x-large" class="mr-4">{{ metric.icon }}</v-icon>
              <div>
                <div class="text-caption text-grey">{{ metric.title }}</div>
                <div class="text-h4 font-weight-bold">{{ metric.value }}</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <!-- Column 1: Spending Overview & Recent Transactions -->
      <v-col cols="12" lg="7">
        <!-- Spending Chart -->
        <v-card class="elevation-2 mb-6">
          <v-card-title>Spending Overview</v-card-title>
          <v-card-text>
            <!-- Chart.js Donut Chart will be rendered here -->
            <Doughnut :data="chartData" :options="chartOptions" style="max-height: 300px;"/>
          </v-card-text>
        </v-card>

        <!-- Recent Transactions -->
        <v-card class="elevation-2">
          <v-card-title>Recent Transactions</v-card-title>
          <v-list lines="two">
            <v-list-item
              v-for="item in transactions"
              :key="item.id"
              class="transaction-item"
            >
              <template v-slot:prepend>
                <v-avatar :color="item.type === 'credit' ? 'green-lighten-4' : 'blue-lighten-5'">
                  <v-icon :color="item.type === 'credit' ? 'success' : 'primary'">{{ item.icon }}</v-icon>
                </v-avatar>
              </template>

              <v-list-item-title class="font-weight-bold">{{ item.title }}</v-list-item-title>
              <v-list-item-subtitle>{{ item.date }}</v-list-item-subtitle>
              
              <template v-slot:append>
                <span :class="item.type === 'credit' ? 'text-success' : 'text-body-1'" class="font-weight-medium">
                  {{ item.type === 'credit' ? '+' : '-' }}${{ item.amount }}
                </span>
              </template>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>

      <!-- Column 2: Persona & Goals -->
      <v-col cols="12" lg="5">
        <!-- Persona Card -->
        <v-card class="elevation-2 mb-6 text-center">
          <v-card-text class="pa-5">
            <div class="text-overline mb-2">Your Financial Persona</div>
            <v-icon size="70" color="accent">mdi-account-star-outline</v-icon>
            <h3 class="text-h5 mt-3">The Balanced Achiever</h3>
            <p class="mt-2 text-body-2">You are good at managing your day-to-day expenses while saving for future goals.</p>
          </v-card-text>
        </v-card>

        <!-- Aspirational Goals -->
        <v-card class="elevation-2">
          <v-card-title>Aspirational Goals</v-card-title>
          <v-card-text>
            <div v-for="goal in goals" :key="goal.title" class="mb-4">
              <div class="d-flex justify-space-between mb-1">
                <span class="font-weight-medium">{{ goal.title }}</span>
                <span class="text-grey">${{ goal.current }} / ${{ goal.total }}</span>
              </div>
              <v-progress-linear
                :model-value="(goal.current / goal.total) * 100"
                color="success"
                height="8"
                rounded
              ></v-progress-linear>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import { Doughnut } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, CategoryScale } from 'chart.js';

// IMPORTANT: Register the components you need from Chart.js
ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale);

// --- Dummy Data (Replace with API calls) ---

const user = ref({ name: 'Alex' }); // This would come from your /api/profile

const keyMetrics = ref([
  { title: 'Monthly Spending', value: '$1,845', icon: 'mdi-credit-card-outline', color: 'primary' },
  { title: 'Monthly Income', value: '$4,500', icon: 'mdi-cash-plus', color: 'success' },
  { title: 'Net Savings', value: '$2,655', icon: 'mdi-piggy-bank-outline', color: 'accent' },
]);

const transactions = ref([
  { id: 1, title: 'Spotify Subscription', date: 'Jul 24, 2025', amount: 10, type: 'debit', icon: 'mdi-spotify' },
  { id: 2, title: 'Salary Deposit', date: 'Jul 21, 2025', amount: 2250, type: 'credit', icon: 'mdi-cash' },
  { id: 3, title: 'Groceries from Whole Foods', date: 'Jul 20, 2025', amount: 154, type: 'debit', icon: 'mdi-cart-outline' },
  { id: 4, title: 'Dinner at The Italian Place', date: 'Jul 19, 2025', amount: 88, type: 'debit', icon: 'mdi-silverware-fork-knife' },
]);

const goals = ref([
  { title: 'Vacation to Hawaii', current: 3500, total: 5000 },
  { title: 'New Laptop', current: 1200, total: 1800 },
  { title: 'Emergency Fund', current: 8500, total: 10000 },
]);

// --- Chart.js Configuration ---

const chartData = ref({
  labels: ['Food & Dining', 'Shopping', 'Utilities', 'Entertainment', 'Transport'],
  datasets: [{
    backgroundColor: ['#1976D2', '#42A5F5', '#82B1FF', '#FFB74D', '#FB8C00'],
    data: [40, 20, 15, 15, 10], // Percentages or amounts
  }]
});

const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right', // Display legend on the side
    }
  }
});
</script>

<style scoped>
.dashboard-bg {
  background-color: #f8f9fa; /* A very light grey for a clean look */
}

.transaction-item {
  transition: background-color 0.2s ease-in-out;
}

.transaction-item:hover {
  background-color: #f1f1f1;
}
</style>