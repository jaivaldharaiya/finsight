<!-- src/views/LoginView.vue -->
<template>
  <div class="background-blur"></div>
  <v-container class="fill-height content-on-bg" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>FinsightAI Login</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="handleLogin">
              <v-text-field
                label="Phone Number"
                v-model="phone"
                prepend-icon="mdi-phone"
                type="tel"
                required
              ></v-text-field>
              <v-text-field
                label="Password"
                v-model="password"
                prepend-icon="mdi-lock"
                :type="showPassword ? 'text' : 'password'"
                :append-inner-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                @click:append-inner="showPassword = !showPassword"
                required
              ></v-text-field>
              <v-card-actions class="px-0">
                <v-btn text color="primary" to="/register">Don't have an account?</v-btn>
                <v-spacer></v-spacer>
                <v-btn type="submit" color="primary" :loading="loading">Login</v-btn>
              </v-card-actions>
              <v-alert v-if="error" type="error" dismissible>
                {{ error }}
              </v-alert>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/composables/auth'

const router = useRouter()
const { login } = useAuth()

const phone = ref('')
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''
  try {
    await login({ phone: phone.value, password: password.value })
    router.push('/dashboard')
  } catch (e) {
    error.value = e.message || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.background-blur {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 0;
  background: url('/bg-login.jpg') center center / cover no-repeat;
  filter: blur(8px) brightness(0.7);
}
.content-on-bg {
  position: relative;
  z-index: 1;
}
.fill-height {
  min-height: 100vh;
}
</style>