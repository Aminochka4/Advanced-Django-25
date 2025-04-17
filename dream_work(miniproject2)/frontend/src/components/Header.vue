<template>
  <header style="background-color: #ffe6e6; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);">
    <div style="width: 100%; margin-left: auto; margin-right: auto; padding-left: 1.5rem; padding-right: 1.5rem; padding-top: 0.75rem; padding-bottom: 0.75rem; display: flex; align-items: center; justify-content: space-between; background-color: #D40000;">
      <router-link to="/" style="font-size: 1.25rem; font-weight: 600; letter-spacing: -0.025em; color: #FFFFFF; transition-property: color, background-color, border-color, outline-color, text-decoration-color, fill, stroke, --tw-gradient-from, --tw-gradient-via, --tw-gradient-to; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 150ms; text-decoration: none;">
        <span style="font-size: 1.5rem; display: inline-block;">Dream Job</span>
      </router-link>

      <div v-if="$route.path === '/login' || $route.path === '/register'" style="display: flex; align-items: center;">
        <router-link to="/login" style="font-size: 1.125rem; font-weight: 500; color: #FFFFFF; transition-property: color, background-color, border-color, outline-color, text-decoration-color, fill, stroke, --tw-gradient-from, --tw-gradient-via, --tw-gradient-to; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 150ms; margin-left: 1.5rem; text-decoration: none;">
          Login
        </router-link>
        <router-link to="/register" style="font-size: 1.125rem; font-weight: 500; color: #FFFFFF; transition-property: color, background-color, border-color, outline-color, text-decoration-color, fill, stroke, --tw-gradient-from, --tw-gradient-via, --tw-gradient-to; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 150ms; margin-left: 1.5rem; text-decoration: none;">
          Register
        </router-link>
      </div>

      <button v-else @click="toggleMenu" style="display: block; padding: 0; border: none; background-color: transparent; outline: none;" class="md:hidden focus:outline-none">
        <svg style="height: 1.5rem; width: 1.5rem; color: #FFFFFF; transition-property: color, background-color, border-color, outline-color, text-decoration-color, fill, stroke, --tw-gradient-from, --tw-gradient-via, --tw-gradient-to; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 150ms; cursor: pointer;" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="isMenuOpen ? 'M6 18L18 6M6 6l12 12' : 'M4 6h16M4 12h16M4 18h16'"></path>
        </svg>
      </button>
    </div>

    <div v-if="isMenuOpen && $route.path !== '/login' && $route.path !== '/register'" style="display: none;" class="md:hidden" :style="isMenuOpen ? 'display: block; background-color: #FFFFFF; transition-property: all; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 300ms;' : 'display: none;'">
      <div style="width: 100%; margin-left: auto; margin-right: auto; padding-left: 1.5rem; padding-right: 1.5rem; padding-top: 1rem; padding-bottom: 1rem; display: flex; flex-direction: column; gap: 0.75rem;">
        <template v-if="isAuthenticated">
          <router-link to="/jobs" @click="toggleMenu" style="font-size: 1.125rem; font-weight: 500; color: #D40000; transition-property: color, background-color, border-color, outline-color, text-decoration-color, fill, stroke, --tw-gradient-from, --tw-gradient-via, --tw-gradient-to; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 150ms; padding-top: 0.5rem; padding-bottom: 0.5rem; border-radius: 0.25rem; text-decoration: none;">
            Job Listings
          </router-link>
          <router-link v-if="userRole?.toLowerCase() === 'job_seeker'" to="/upload-resume" @click="toggleMenu" style="font-size: 1.125rem; font-weight: 500; color: #D40000; transition-property: color, background-color, border-color, outline-color, text-decoration-color, fill, stroke, --tw-gradient-from, --tw-gradient-via, --tw-gradient-to; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 150ms; padding-top: 0.5rem; padding-bottom: 0.5rem; border-radius: 0.25rem; text-decoration: none;">
            Add Resume
          </router-link>
          <router-link v-if="userRole?.toLowerCase() === 'recruiter'" to="/create-job" @click="toggleMenu" style="font-size: 1.125rem; font-weight: 500; color: #D40000; transition-property: color, background-color, border-color, outline-color, text-decoration-color, fill, stroke, --tw-gradient-from, --tw-gradient-via, --tw-gradient-to; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 150ms; padding-top: 0.5rem; padding-bottom: 0.5rem; border-radius: 0.25rem; text-decoration: none;">
            Create Vacancy
          </router-link>
          <router-link v-if="userRole?.toLowerCase() === 'recruiter'" to="/my-listings" @click="toggleMenu" style="font-size: 1.125rem; font-weight: 500; color: #D40000; transition-property: color, background-color, border-color, outline-color, text-decoration-color, fill, stroke, --tw-gradient-from, --tw-gradient-via, --tw-gradient-to; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 150ms; padding-top: 0.5rem; padding-bottom: 0.5rem; border-radius: 0.25rem; text-decoration: none;">
            My Listings
          </router-link>
          <router-link v-if="userRole?.toLowerCase() === 'recruiter'" to="/recruiter-applications" @click="toggleMenu" style="font-size: 1.125rem; font-weight: 500; color: #D40000; transition-property: color, background-color, border-color, outline-color, text-decoration-color, fill, stroke, --tw-gradient-from, --tw-gradient-via, --tw-gradient-to; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 150ms; padding-top: 0.5rem; padding-bottom: 0.5rem; border-radius: 0.25rem; text-decoration: none;">
            All Applications
          </router-link>
          <router-link v-if="userRole?.toLowerCase() === 'job_seeker'" to="/my-applications" @click="toggleMenu" style="font-size: 1.125rem; font-weight: 500; color: #D40000; transition-property: color, background-color, border-color, outline-color, text-decoration-color, fill, stroke, --tw-gradient-from, --tw-gradient-via, --tw-gradient-to; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 150ms; padding-top: 0.5rem; padding-bottom: 0.5rem; border-radius: 0.25rem; text-decoration: none;">
            My Applications
          </router-link>
          <button @click="logout" style="font-size: 1.125rem; font-weight: 500; color: #D40000; transition-property: color, background-color, border-color, outline-color, text-decoration-color, fill, stroke, --tw-gradient-from, --tw-gradient-via, --tw-gradient-to; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 150ms; text-align: left; padding-top: 0.5rem; padding-bottom: 0.5rem; border-radius: 0.25rem; border: none; background: transparent; cursor: pointer;">
            Logout
          </button>
        </template>
      </div>
    </div>
  </header>
</template>

<script>
import { useAuth } from '../composables/useAuth'

export default {
  name: 'Header',
  data() {
    return {
      isMenuOpen: false,
      isAuthenticated: false,
      userRole: null,
      isDesktopNavVisible: true,
    }
  },
  setup() {
    const { resetForms } = useAuth()
    return { resetForms }
  },
  methods: {
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen
    },
    logout() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user_role')
      this.isAuthenticated = false
      this.userRole = null
      this.resetForms()
      this.$router.push('/login')
    },
    checkAuth() {
      const token = localStorage.getItem('access_token')
      this.isAuthenticated = !!token
      this.userRole = localStorage.getItem('user_role')
      console.log('User Role:', this.userRole)
    },
    updateDesktopNavVisibility() {
      this.isDesktopNavVisible = window.innerWidth >= 768;
    },
  },
  created() {
    this.checkAuth()
    this.updateDesktopNavVisibility();
    window.addEventListener('resize', this.updateDesktopNavVisibility);
    this.$router.afterEach(() => {
      this.checkAuth()
    })
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.updateDesktopNavVisibility);
  },
}
</script>