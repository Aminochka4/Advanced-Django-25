<template>
  <div style="max-width: 1200px; margin: 0 auto; padding: 20px;">
    <h1 style="font-size: 2.5rem; font-weight: bold; margin-bottom: 1.5rem; color: #cc0000; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Create Job Listing</h1>
    <div v-if="error" style="background-color: #ffe6e6; color: #cc0000; padding: 15px; border-radius: 6px; margin-bottom: 1rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
      {{ error }}
    </div>
    <div v-if="success" style="background-color: #e6ffe6; color: #008000; padding: 15px; border-radius: 6px; margin-bottom: 1rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
      {{ success }}
    </div>
    <form @submit.prevent="createJob" style="max-width: 800px;">
      <div style="margin-bottom: 1.5rem;">
        <label for="title" style="display: block; margin-bottom: 0.5rem; color: #333; font-weight: 500; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Job Title</label>
        <input
          v-model="form.title"
          type="text"
          id="title"
          style="display: block; width: calc(100% - 24px); border: 1px solid #ddd; border-radius: 6px; padding: 0.75rem 1rem; font-size: 1rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; outline: none; transition: border-color 0.2s ease-in-out;"
          required
          maxlength="100"
        />
      </div>
      <div style="margin-bottom: 1.5rem;">
        <label for="company_name" style="display: block; margin-bottom: 0.5rem; color: #333; font-weight: 500; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Company Name</label>
        <input
          v-model="form.company_name"
          type="text"
          id="company_name"
          style="display: block; width: calc(100% - 24px); border: 1px solid #ddd; border-radius: 6px; padding: 0.75rem 1rem; font-size: 1rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; outline: none; transition: border-color 0.2s ease-in-out;"
          required
          maxlength="100"
        />
      </div>
      <div style="margin-bottom: 1.5rem;">
        <label for="location" style="display: block; margin-bottom: 0.5rem; color: #333; font-weight: 500; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Location</label>
        <input
          v-model="form.location"
          type="text"
          id="location"
          style="display: block; width: calc(100% - 24px); border: 1px solid #ddd; border-radius: 6px; padding: 0.75rem 1rem; font-size: 1rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; outline: none; transition: border-color 0.2s ease-in-out;"
          required
          maxlength="100"
        />
      </div>
      <div style="margin-bottom: 1.5rem;">
        <label for="employment_type" style="display: block; margin-bottom: 0.5rem; color: #333; font-weight: 500; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Employment Type</label>
        <select
          v-model="form.employment_type"
          id="employment_type"
          style="display: block; width: calc(100% - 24px); border: 1px solid #ddd; border-radius: 6px; padding: 0.75rem 1rem; font-size: 1rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; outline: none; transition: border-color 0.2s ease-in-out;"
          required
        >
          <option value="remote">Remote</option>
          <option value="hybrid">Hybrid</option>
          <option value="onsite">Onsite</option>
        </select>
      </div>
      <div style="margin-bottom: 1.5rem;">
        <label for="required_experience" style="display: block; margin-bottom: 0.5rem; color: #333; font-weight: 500; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Required Experience (in years)</label>
        <input
          v-model.number="form.required_experience"
          type="number"
          id="required_experience"
          style="display: block; width: calc(100% - 24px); border: 1px solid #ddd; border-radius: 6px; padding: 0.75rem 1rem; font-size: 1rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; outline: none; transition: border-color 0.2s ease-in-out;"
          required
          min="0"
        />
      </div>
      <div style="margin-bottom: 1.5rem;">
        <label for="required_skills" style="display: block; margin-bottom: 0.5rem; color: #333; font-weight: 500; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Required Skills</label>
        <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.5rem;">
          <span
            v-for="skill in form.required_skills"
            :key="skill"
            style="background-color: #e0f7fa; color: #00838f; padding: 0.5rem 0.75rem; border-radius: 1rem; display: flex; align-items: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 0.9rem;"
          >
            {{ skill }}
            <button
              type="button"
              @click="removeSkill(skill)"
              style="margin-left: 0.5rem; color: #d32f2f; cursor: pointer; border: none; background: none; padding: 0;"
            >
              &times;
            </button>
          </span>
        </div>
        <input
          v-model="newSkill"
          type="text"
          id="required_skills"
          style="display: block; width: calc(100% - 24px); border: 1px solid #ddd; border-radius: 6px; padding: 0.75rem 1rem; font-size: 1rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; outline: none; transition: border-color 0.2s ease-in-out;"
          placeholder="Add required skills"
          @keydown.enter.prevent="addSkill"
          maxlength="50"
        />
      </div>
      <div style="margin-bottom: 2rem;">
        <label for="description" style="display: block; margin-bottom: 0.5rem; color: #333; font-weight: 500; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Description</label>
        <textarea
          v-model="form.description"
          id="description"
          style="display: block; width: calc(100% - 24px); border: 1px solid #ddd; border-radius: 6px; padding: 0.75rem 1rem; font-size: 1rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; outline: none; transition: border-color 0.2s ease-in-out; min-height: 150px;"
        ></textarea>
      </div>
      <button
        type="submit"
        style="background-color: #cc0000; color: #fff; padding: 10px 15px; border: none; border-radius: 6px; cursor: pointer; font-size: 1rem; transition-colors 0.2s ease-in-out; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-weight: 500;"
      >
        Create Job
      </button>
    </form>
  </div>
</template>

<script>
import apiClient from '../api'

export default {
  name: 'JobCreatePage',
  data() {
    return {
      form: {
        title: '',
        company_name: '',
        location: '',
        employment_type: 'remote',
        required_experience: 0,
        required_skills: [],
        description: ''
      },
      newSkill: '',
      error: null,
      success: null
    }
  },
  methods: {
    addSkill() {
      const skill = this.newSkill.trim()
      if (skill && !this.form.required_skills.includes(skill) && skill.length <= 50) {
        this.form.required_skills.push(skill)
        this.newSkill = ''
      }
    },
    removeSkill(skill) {
      this.form.required_skills = this.form.required_skills.filter(s => s !== skill)
    },
    async createJob() {
      try {
        this.error = null
        this.success = null
        const response = await apiClient.post('/jobs/create/', {
          title: this.form.title,
          company_name: this.form.company_name,
          location: this.form.location,
          employment_type: this.form.employment_type,
          required_experience: this.form.required_experience,
          required_skills: this.form.required_skills,
          description: this.form.description
        })
        this.success = response.data.message
        this.form = {
          title: '',
          company_name: '',
          location: '',
          employment_type: 'remote',
          required_experience: 0,
          required_skills: [],
          description: ''
        }
        this.$router.push('/jobs')
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to create job.'
      }
    }
  }
}
</script>