<template>
  <div style="max-width: 1200px; margin: 0 auto; padding: 20px;">
    <h1 style="font-size: 2.5rem; font-weight: bold; margin-bottom: 1.5rem; color: #cc0000; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Applications for Your Jobs</h1>
    <div v-if="error" style="background-color: #ffe6e6; color: #cc0000; padding: 15px; border-radius: 6px; margin-bottom: 1rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
      {{ error }}
    </div>
    <div style="margin-bottom: 1.5rem;">
      <label for="jobFilter" style="display: block; margin-bottom: 0.5rem; color: #333; font-weight: 500; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Filter by Job</label>
      <select
        id="jobFilter"
        v-model="selectedJobTitle"
        @change="filterApplicationsByJobTitle"
        style="display: block; width: 100%; max-width: 300px; border: 1px solid #ddd; border-radius: 6px; padding: 0.75rem 1rem; font-size: 1rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; outline: none; transition: border-color 0.2s ease-in-out;"
      >
        <option value="">All Jobs</option>
        <option v-for="title in jobTitles" :key="title" :value="title">{{ title }}</option>
      </select>
    </div>
    <div v-if="filteredApplications.length" style="display: flex; flex-direction: column; gap: 1.5rem;">
      <div v-for="app in filteredApplications" :key="app.created_at" style="background-color: #fff; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); border-radius: 8px; padding: 1.5rem; border: 1px solid #f0f0f0;">
        <h2 style="font-size: 1.5rem; font-weight: bold; margin-bottom: 0.75rem; color: #cc0000; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">{{ app.job_title }}</h2>
        <p style="color: #333; margin-bottom: 0.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;"><strong>Applicant:</strong> {{ app.user_email }}</p>
        <p style="color: #555; margin-bottom: 0.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;"><strong>Match Score:</strong> {{ app.match_score }}/10</p>
        <p style="color: #555; margin-bottom: 0.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;"><strong>Feedback:</strong> {{ app.feedback_text }}</p>
        <div style="color: #666; margin-bottom: 0.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
          <strong>Resume:</strong>
          <pre style="background-color: #f9f9f9; padding: 1rem; border-radius: 6px; margin-top: 0.5rem; max-height: 150px; overflow-y: auto; font-family: 'Consolas', 'Monaco', monospace; font-size: 0.8rem; white-space: pre-wrap;">{{ app.resume_text }}</pre>
        </div>
        <p style="color: #777; font-size: 0.9rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Applied on {{ formatDate(app.created_at) }}</p>
      </div>
    </div>
    <div v-else style="color: #777; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
      No applications found.
    </div>
  </div>
</template>

<script>
import apiClient from '../api'

export default {
  name: 'RecruiterApplicationsPage',
  data() {
    return {
      applications: [],
      jobTitles: [],
      selectedJobTitle: '',
      error: null,
      filteredApplications: []
    }
  },
  async created() {
    await this.fetchApplications();
  },
  methods: {
    async fetchApplications() {
      try {
        this.error = null;
        const response = await apiClient.get('/jobs/applications/');
        this.applications = response.data;
        this.filteredApplications = [...this.applications]; // Изначально показываем все заявки
        this.jobTitles = [...new Set(this.applications.map(app => app.job_title))]; // Получаем уникальные названия вакансий
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to load applications.';
      }
    },
    filterApplicationsByJobTitle() {
      if (!this.selectedJobTitle) {
        this.filteredApplications = [...this.applications]; // Если выбрано "All Jobs", показываем все
      } else {
        this.filteredApplications = this.applications.filter(app => app.job_title === this.selectedJobTitle);
      }
    },
    formatDate(value) {
      if (!value) return '';
      return new Date(value).toLocaleString();
    }
  }
}
</script>