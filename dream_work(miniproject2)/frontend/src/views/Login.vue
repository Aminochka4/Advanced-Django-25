<template>
  <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; background-color: #ffffff; padding: 30px;">
    <div style="background-color: #fff; padding: 50px; border-radius: 12px; box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15); width: 400px; max-width: 100%;">
      <h2 style="font-size: 32px; font-weight: 700; color: #cc0000; margin-bottom: 40px; text-align: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Login</h2>
      <form @submit.prevent="login">
        <div style="margin-bottom: 25px;">
          <label for="email" style="display: block; margin-bottom: 8px; color: #cc0000; font-size: 16px; font-weight: 500; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Email Address</label>
          <input
            type="email"
            id="email"
            v-model="loginForm.email"
            required
            style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; box-sizing: border-box; background-color: #FFF1F1;"
          />
        </div>
        <div style="margin-bottom: 35px;">
          <label for="password" style="display: block; margin-bottom: 8px; color: #cc0000; font-size: 16px; font-weight: 500; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Password</label>
          <input
            type="password"
            id="password"
            v-model="loginForm.password"
            required
            style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; box-sizing: border-box; background-color: #ffffff;"
          />
        </div>
        <button
          type="submit"
          style="background-color: #cc0000; color: #fff; padding: 16px 24px; border: none; border-radius: 8px; cursor: pointer; font-size: 18px; font-weight: 600; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; width: 100%; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); text-align: center;"
        >
          Login
        </button>
      </form>
      <p style="margin-top: 30px; font-size: 15px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center;">
        Don't have an account?
        <router-link to="/register" style="color: #ff3333; font-weight: 600; text-decoration: none;">Sign up</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import apiClient from '../api'
import { useAuth } from '../composables/useAuth'

export default {
  name: 'Login',
  setup() {
    const { resetForms } = useAuth()
    return { resetForms }
  },
  data() {
    return {
      loginForm: {
        email: '',
        password: '',
      },
      error: null,
    }
  },
  methods: {
    async login() {
      try {
        this.error = null
        const response = await apiClient.post('/auth/login/', this.loginForm)
        console.log('Login response:', response.data) // Debug log to inspect backend response

        const { access, refresh, role } = response.data
        if (!role) {
          throw new Error('Role not provided in login response')
        }

        localStorage.setItem('access_token', access)
        localStorage.setItem('refresh_token', refresh)
        localStorage.setItem('user_role', role)

        this.resetForms()
        this.$router.push('/jobs')
      } catch (err) {
        this.error = err.response?.data?.error || err.message || 'Login failed.'
      }
    },
  },
}
</script>