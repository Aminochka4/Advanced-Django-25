<template>
  <div style="max-width: 1200px; margin: 0 auto; padding: 20px;">
    <div v-if="error" style="background-color: #ffe6e6; color: #cc0000; padding: 15px; border-radius: 6px; margin-bottom: 1rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
      {{ error }}
    </div>
    <div v-if="success" style="background-color: #e6ffe6; color: #008000; padding: 15px; border-radius: 6px; margin-bottom: 1rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
      {{ success }}
      <div v-if="match_score !== null" style="margin-top: 10px;">
        <p style="font-weight: bold; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;"><strong>Match Score:</strong> {{ match_score }}/10</p>
        <p style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;"><strong>Feedback:</strong> {{ feedback_text }}</p>
      </div>
    </div>
    <div v-if="job" style="background-color: #fff; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); border-radius: 8px; padding: 20px; border: 1px solid #f0f0f0;">
      <h1 style="font-size: 2.5rem; font-weight: bold; margin-bottom: 1rem; color: #cc0000; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">{{ job.title }}</h1>
      <p style="color: #333; margin-bottom: 0.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;"><strong>Company:</strong> {{ job.company_name }}</p>
      <p style="color: #555; margin-bottom: 0.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;"><strong>Location:</strong> {{ job.location }}</p>
      <p style="color: #555; margin-bottom: 0.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;"><strong>Type:</strong> {{ capitalize(job.employment_type) }}</p>
      <p style="color: #555; margin-bottom: 0.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;"><strong>Experience:</strong> {{ job.required_experience }} years</p>
      <p style="color: #555; margin-bottom: 0.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        <strong>Skills:</strong> {{ job.required_skills_data.map(s => s.name).join(', ') }}
      </p>
      <p style="color: #666; margin-bottom: 1.5rem; white-space: pre-wrap; line-height: 1.6; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">{{ job.description }}</p>
      <p style="color: #777; font-size: 0.9rem; margin-bottom: 1.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Posted on {{ formatDate(job.created_at) }}</p>
      <button
        v-if="isJobSeeker"
        @click="applyJob"
        style="background-color: #cc0000; color: #fff; padding: 10px 15px; border: none; border-radius: 6px; cursor: pointer; font-size: 1rem; transition-colors 0.2s ease-in-out; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;"
        :disabled="applying"
        :style="{ backgroundColor: applying ? '#800000' : '#cc0000' }"
      >
        {{ applying ? 'Applying...' : 'Apply Now' }}
      </button>
    </div>
    <div v-else style="color: #777; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
      Loading job details...
    </div>
  </div>
</template>

<script>
import apiClient from '../api'

export default {
  name: 'JobDetailPage',
  data() {
    return {
      job: null,
      error: null,
      success: null,
      applying: false,
      match_score: null,
      feedback_text: null
    }
  },
  computed: {
    isJobSeeker() {
      return localStorage.getItem('user_role') === 'job_seeker'
    }
  },
  async created() {
    await this.fetchJob()
  },
  methods: {
    async fetchJob() {
      try {
        this.error = null
        const jobId = this.$route.params.id
        this.job = (await apiClient.get(`/jobs/${jobId}/`)).data
      } catch (err) {
        this.error = 'Failed to load job details.'
      }
    },
    async applyJob() {
      if (this.applying) return
      this.applying = true
      try {
        this.error = null
        this.success = null
        const jobId = this.$route.params.id
        const response = await apiClient.post(`/jobs/${jobId}/apply/`)
        this.success = 'Application submitted successfully!'
        this.match_score = response.data.match_score
        this.feedback_text = response.data.feedback_text
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to apply.'
      } finally {
        this.applying = false
      }
    },
    capitalize(value) {
      if (!value) return ''
      return value.charAt(0).toUpperCase() + value.slice(1)
    },
    formatDate(value) {
      if (!value) return ''
      return new Date(value).toLocaleDateString()
    }
  }
}
</script>