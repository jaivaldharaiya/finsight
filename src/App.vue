<!-- src/App.vue -->
<<template>
  <v-app>
    <!-- Conditionally render navigation based on the current route -->
    <template v-if="shouldShowNavigation">
      <!-- Navigation Drawer for Desktop -->
      <v-navigation-drawer v-if="!isMobile" app color="primary">
        <v-list dark>
          <v-list-item prepend-icon="mdi-finance" title="Finsight" class="font-weight-bold text-h6"></v-list-item>
          <v-divider></v-divider>
          <v-list-item link to="/dashboard" prepend-icon="mdi-view-dashboard" title="Dashboard"></v-list-item>
          <v-list-item link to="/Agents" prepend-icon="mdi-view-dashboard" title="Agents"></v-list-item>

          <v-spacer></v-spacer>
          <v-list-item @click="handleLogout" prepend-icon="mdi-logout" title="Logout"></v-list-item>
        </v-list>
      </v-navigation-drawer>
    </template>

    <!-- Main Content Area -->
    <v-main>
      <router-view />
    </v-main>

    <!-- Conditionally render bottom navigation -->
    <template v-if="shouldShowNavigation">
      <!-- Bottom Navigation for Mobile -->
      <v-bottom-navigation v-if="isMobile" app color="primary" grow>
         <v-btn to="/">
            <v-icon>mdi-account-question</v-icon>
            <span>Questions</span>
          </v-btn>
        <v-btn to="/dashboard">
          <v-icon>mdi-view-dashboard</v-icon>
          <span>Dashboard</span>
        </v-btn>
         <v-btn @click="handleLogout">
          <v-icon>mdi-logout</v-icon>
          <span>Logout</span>
        </v-btn>
      </v-bottom-navigation>
    </template>
  </v-app>
</template>

<script setup>
import { computed } from 'vue'
import { useDisplay } from 'vuetify'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '@/composables/auth'

const { name } = useDisplay()
const route = useRoute()
const router = useRouter()
const { user, logout } = useAuth()

const isMobile = computed(() => ['xs', 'sm'].includes(name.value))

// Show navigation only if user is logged in and not on Login/Register page
const shouldShowNavigation = computed(() => {
  return user.value && route.name !== 'Login' && route.name !== 'Register';
})

const handleLogout = () => {
  logout()
  router.push('/login')
}
</script>


<style>
/* Global styles */
.v-btn span {
  font-size: 0.75rem;
  margin-top: 2px;
}
.v-list-item {
  cursor: pointer;
}
</style>