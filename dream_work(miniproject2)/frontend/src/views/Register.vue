<template>
  <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; background-color: #ffffff; padding: 30px;">
    <div style="background-color: #fff; padding: 50px; border-radius: 12px; box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15); width: 400px; max-width: 100%;">
      <h2 style="font-size: 32px; font-weight: 700; color: #cc0000; margin-bottom: 40px; text-align: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Create Account</h2>
      <div v-if="error" style="margin-bottom: 20px; padding: 15px; background-color: #ffdddd; color: #cc0000; border-radius: 6px; font-size: 16px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        {{ error }}
      </div>
      <form @submit.prevent="register">
        <div style="margin-bottom: 25px;">
          <label for="email" style="display: block; margin-bottom: 8px; color: #cc0000; font-size: 16px; font-weight: 500; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Email</label>
          <input
            v-model="registerForm.email"
            type="email"
            id="email"
            style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; box-sizing: border-box; background-color: #f9f9f9;"
            placeholder="Enter your email"
            required
          />
        </div>
        <div style="margin-bottom: 25px;">
          <label for="password" style="display: block; margin-bottom: 8px; color: #cc0000; font-size: 16px; font-weight: 500; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Password</label>
          <input
            v-model="registerForm.password"
            type="password"
            id="password"
            style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; box-sizing: border-box; background-color: #f9f9f9;"
            placeholder="Enter your password"
            required
          />
        </div>
        <div style="margin-bottom: 35px;">
          <label for="role" style="display: block; margin-bottom: 8px; color: #cc0000; font-size: 16px; font-weight: 500; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Role</label>
          <select
            v-model="registerForm.role"
            id="role"
            style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; box-sizing: border-box; background-color: #f9f9f9;"
            required
          >
            <option value="job_seeker">Job Seeker</option>
            <option value="recruiter">Recruiter</option>
          </select>
        </div>
        <button
          type="submit"
          style="background-color: #cc0000; color: #fff; padding: 16px 24px; border: none; border-radius: 8px; cursor: pointer; font-size: 18px; font-weight: 600; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; width: 100%; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);"
        >
          Sign Up
        </button>
      </form>
      <p style="margin-top: 30px; font-size: 15px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center;">
        Already have an account?
        <router-link to="/login" style="color: #ff3333; font-weight: 600; text-decoration: none;">Log in</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import { useAuth } from '../composables/useAuth'

export default {
  name: 'RegisterPage',
  setup() {
    const { registerForm, error, register } = useAuth()
    return { registerForm, error, register }
  },
}
</script>