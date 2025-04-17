<template>
  <div style="max-width: 1200px; margin: 0 auto; padding: 20px;">
    <h1 style="font-size: 2.5rem; font-weight: bold; margin-bottom: 1.5rem; color: #cc0000; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Job Listings</h1>
    <div v-if="error" style="background-color: #ffe6e6; color: #cc0000; padding: 15px; border-radius: 6px; margin-bottom: 1rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
      {{ error }}
    </div>
    <div style="margin-bottom: 1.5rem;">
      <div style="display: flex; gap: 1rem; align-items: center;">
        <input
          v-model="filters.location"
          type="text"
          placeholder="Filter by location"
          style="padding: 0.75rem 1rem; border: 1px solid #ddd; border-radius: 6px; font-size: 1rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; flex-grow: 1; min-width: 150px; outline: none; transition: border-color 0.2s ease-in-out;"
        />
        <select v-model="filters.employment_type" style="padding: 0.75rem 1rem; border: 1px solid #ddd; border-radius: 6px; font-size: 1rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; min-width: 120px; outline: none; transition: border-color 0.2s ease-in-out;">
          <option value="">All Types</option>
          <option value="remote">Remote</option>
          <option value="hybrid">Hybrid</option>
          <option value="onsite">Office</option>
        </select>
        <input
          v-model="filters.skill"
          type="text"
          placeholder="Filter by skill"
          style="padding: 0.75rem 1rem; border: 1px solid #ddd; border-radius: 6px; font-size: 1rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; flex-grow: 1; min-width: 150px; outline: none; transition: border-color 0.2s ease-in-out;"
        />
        <select v-model="sortBy" style="padding: 0.75rem 1rem; border: 1px solid #ddd; border-radius: 6px; font-size: 1rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; min-width: 180px; outline: none; transition: border-color 0.2s ease-in-out;">
          <option value="created_at">New</option>
          <option value="required_experience">By experience</option>
        </select>
      </div>
    </div>
    <div v-if="filteredJobs.length === 0" style="color: #777; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
      No jobs match your filters.
    </div>
    <div v-else style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem;">
      <router-link
        v-for="job in filteredJobs"
        :key="job.id"
        :to="'/jobs/' + job.id"
        style="background-color: #fff; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); border-radius: 8px; padding: 1.5rem; transition: box-shadow 0.3s ease-in-out; border: 1px solid #f0f0f0;"
        @mouseover="event => { event.currentTarget.style.boxShadow = '0 8px 16px rgba(0, 0, 0, 0.2)'; event.currentTarget.style.borderColor = '#cc0000'; }"
        @mouseleave="event => { event.currentTarget.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.1)'; event.currentTarget.style.borderColor = '#f0f0f0'; }"
      >
        <h2 style="font-size: 1.5rem; font-weight: bold; margin-bottom: 0.75rem; color: #cc0000; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">{{ job.title }}</h2>
        <p style="color: #333; margin-bottom: 0.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;"><strong>Company:</strong> {{ job.company_name }}</p>
        <p style="color: #555; margin-bottom: 0.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;"><strong>Location:</strong> {{ job.location }}</p>
        <p style="color: #555; margin-bottom: 0.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;"><strong>Type:</strong> {{ capitalize(job.employment_type) }}</p>
        <p style="color: #555; margin-bottom: 0.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;"><strong>Experience:</strong> {{ job.required_experience }} years</p>
        <p style="color: #555; margin-bottom: 0.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
          <strong>Skills:</strong> {{ job.required_skills_data.map(s => s.name).join(', ') }}
        </p>
        <p style="color: #666; margin-top: 0.75rem; font-size: 0.9rem; line-height: 1.4; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">{{ truncate(job.description, 200) }}</p>
      </router-link>
    </div>
  </div>
</template>

<script>
import apiClient from '../api'

export default {
  name: 'JobListPage',
  data() {
    return {
      jobs: [],
      filters: {
        location: '',
        employment_type: '',
        skill: ''
      },
      sortBy: 'created_at',
      error: null
    }
  },
  computed: {
    filteredJobs() {
      let filtered = this.jobs
      if (this.filters.location) {
        filtered = filtered.filter(job =>
          job.location.toLowerCase().includes(this.filters.location.toLowerCase())
        )
      }
      if (this.filters.employment_type) {
        filtered = filtered.filter(job => job.employment_type === this.filters.employment_type)
      }
      if (this.filters.skill) {
        const skillLower = this.filters.skill.toLowerCase()
        filtered = filtered.filter(job =>
          job.required_skills_data.some(skill => skill.name.toLowerCase().includes(skillLower))
        )
      }
      if (this.sortBy === 'required_experience') {
        filtered = [...filtered].sort((a, b) => a.required_experience - b.required_experience)
      } else {
        filtered = [...filtered].sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
      }
      return filtered
    }
  },
  async created() {
    await this.fetchJobs()
  },
  methods: {
    async fetchJobs() {
      try {
        this.error = null
        const response = await apiClient.get('/jobs/')
        this.jobs = response.data
      } catch (err) {
        this.error = 'Failed to load jobs.'
      }
    },
    capitalize(value) {
      if (!value) return ''
      return value.charAt(0).toUpperCase() + value.slice(1)
    },
    truncate(value, length) {
      if (!value) return ''
      return value.length > length ? value.substring(0, length) + '...' : value
    }
  }
}
</script>