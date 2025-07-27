<!-- src/views/HomeView.vue -->
<template>
  <div class="home-wrapper">
    <!-- Section 1: Hero Section -->
    <section class="hero-section">
      <v-container class="fill-height">
        <v-row align="center" class="text-center text-md-left">
          <!-- Left Column: Animated Text Content -->
          <v-col cols="12" md="6">
            <v-slide-y-transition appear>
              <h1 class="text-h3 text-md-h2 font-weight-black mb-6 text-white" style="line-height: 1.2;">
                Gain True Clarity on Your Finances.
              </h1>
            </v-slide-y-transition>

            <v-slide-y-transition appear>
              <h2 class="text-h6 font-weight-light mb-8 text-grey-lighten-2" style="max-width: 500px;">
                FinsightAI uses powerful AI agents to analyze your spending, plan investments, and help you achieve your financial goals faster.
              </h2>
            </v-slide-y-transition>

            <v-slide-y-transition appear>
              <v-btn
                to="/register"
                size="x-large"
                color="success"
                class="elevation-6 font-weight-bold"
                append-icon="mdi-arrow-right-circle-outline"
              >
                Get Started for Free
              </v-btn>
            </v-slide-y-transition>
          </v-col>
          
          <!-- Right Column: Animated Image -->
          <v-col cols="12" md="6">
            <v-fade-transition appear>
              <v-img 
                src="@/assets/hero-illustration.svg" 
                max-height="500"
                contain
                alt="Financial analysis illustration"
              />
            </v-fade-transition>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Section 2: Features Section -->
    <section class="features-section py-15">
      <v-container>
        <div class="text-center">
          <v-chip color="primary" variant="elevated" class="mb-4">Our Agents</v-chip>
          <h2 class="text-h3 font-weight-bold mb-4">Your Personal AI Finance Team</h2>
          <p class="text-h6 font-weight-light text-grey-darken-1 mx-auto mb-12" style="max-width: 700px;">
            Unlock the power of specialized agents working just for you, 24/7. Each one is an expert in its domain.
          </p>
        </div>
        <v-row>
          <v-col
            v-for="(feature, i) in features"
            :key="i"
            cols="12"
            sm="6"
            md="3"
          >
            <!-- Using d-flex and flex-column ensures cards are truly the same height -->
            <v-card class="text-center pa-5 fill-height d-flex flex-column elevation-2 card-hover">
              <div class="flex-grow-1">
                <v-icon size="64" :color="feature.color" class="my-4">{{ feature.icon }}</v-icon>
                <v-card-title class="font-weight-bold justify-center">{{ feature.title }}</v-card-title>
                <v-card-text class="text-body-1">{{ feature.text }}</v-card-text>
              </div>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Section 3: Footer -->
    <v-footer color="grey-darken-4" class="py-5">
      <v-container class="text-center">
        <span class="text-white">© {{ new Date().getFullYear() }} Finsight. All Rights Reserved.</span>
      </v-container>
    </v-footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const features = ref([
  {
    icon: 'mdi-chart-pie',
    color: 'primary',
    title: 'Spend Analyzer',
    text: 'Get a crystal-clear visual breakdown of where your money goes every month.'
  },
  {
    icon: 'mdi-rocket-launch-outline',
    color: 'success',
    title: 'Goal Achiever',
    text: 'Set your biggest goals and get a clear, actionable plan to make them a reality.'
  },
  {
    icon: 'mdi-chart-line',
    color: 'info',
    title: 'Investment Planner',
    text: 'Discover investment opportunities tailored to your financial persona and risk tolerance.'
  },
  {
    icon: 'mdi-file-document-edit-outline',
    color: 'warning',
    title: 'ITR Return Planner',
    text: 'Simplify tax season with an agent that helps you prepare and plan for your returns.'
  }
])
</script>

<style scoped>
.home-wrapper {
  width: 100%;
}

.hero-section {
  /* A richer, more modern gradient */
  background: linear-gradient(45deg, #1A237E 0%, #1565C0 100%);
  background-size: 200% 200%;
  min-height: 95vh;
  display: flex;
  align-items: center;
  /* Subtle background pan animation */
  animation: gradient-pan 15s ease infinite;
}

@keyframes gradient-pan {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.features-section {
  background-color: #f8f9fa; /* A clean, light grey */
}

.card-hover {
  transition: all 0.3s ease-in-out !important;
  border: 1px solid transparent;
}

.card-hover:hover {
  transform: translateY(-8px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.1) !important;
  border-color: #d3c800; /* Add a subtle border on hover */
}
</style>