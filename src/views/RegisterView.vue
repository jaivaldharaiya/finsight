<!-- src/views/RegisterView.vue -->
<template>
  <div class="background-blur"></div>
  <v-container class="fill-height content-on-bg" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Create Your FinsightAI Account</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="handleRegister">
               <v-text-field
                label="Full Name"
                v-model="form.name"
                prepend-icon="mdi-account"
                type="text"
                required
              ></v-text-field>
              <v-text-field
                label="Email"
                v-model="form.email"
                prepend-icon="mdi-email"
                type="email"
                required
              ></v-text-field>
              <v-text-field
                label="Phone Number"
                v-model="form.phone"
                prepend-icon="mdi-phone"
                type="tel"
                required
              ></v-text-field>
              <v-text-field
                label="Password"
                v-model="form.password"
                prepend-icon="mdi-lock"
                type="password"
                required
              ></v-text-field>
              <v-card-actions class="px-0">
                <v-btn text color="primary" to="/login">Already have an account?</v-btn>
                <v-spacer></v-spacer>
                <v-btn type="submit" color="success" :loading="loading">Register</v-btn>
              </v-card-actions>
            </v-form>
            <v-alert v-if="error" type="error" dismissible>{{ error }}</v-alert>
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
const { register, login } = useAuth()

const form = ref({
  name: '',
  email: '',
  phone: '',
  password: ''
})

const loading = ref(false)
const error = ref('')

async function handleRegister() {
  loading.value = true
  error.value = ''

  // Basic validation
  if (!form.value.name || !form.value.email || !form.value.phone || !form.value.password) {
    error.value = 'All fields are required.'
    loading.value = false
    return
  }
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailPattern.test(form.value.email)) {
    error.value = 'Please enter a valid email address.'
    loading.value = false
    return
  }
  const phonePattern = /^\d{10}$/
  if (!phonePattern.test(form.value.phone)) {
    error.value = 'Please enter a valid 10-digit phone number.'
    loading.value = false
    return
  }
  if (form.value.password.length < 6) {
    error.value = 'Password must be at least 6 characters.'
    loading.value = false
    return
  }

  try {
    await register(form.value)
    // Only use phone and password for login, as per backend API
    await login({ phone: form.value.phone, password: form.value.password })
    router.push('/Questionnaire')
  } catch (e) {
    error.value = e.message || 'Registration failed'
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