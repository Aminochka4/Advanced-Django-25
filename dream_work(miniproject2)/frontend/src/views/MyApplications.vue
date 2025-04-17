<template>
    <div style="max-width: 1200px; margin: 0 auto; padding: 20px;">
      <h1 style="font-size: 2.5rem; font-weight: bold; margin-bottom: 1.5rem; color: #cc0000; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">My Applications</h1>
      <div v-if="error" style="background-color: #ffe6e6; color: #cc0000; padding: 15px; border-radius: 6px; margin-bottom: 1rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        {{ error }}
      </div>
      <div v-if="applications.length" style="display: flex; flex-direction: column; gap: 1.5rem;">
        <div v-for="app in applications" :key="app.applied_on" style="background-color: #fff; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); border-radius: 8px; padding: 1.5rem; border: 1px solid #f0f0f0;">
          <h2 style="font-size: 1.5rem; font-weight: bold; margin-bottom: 0.75rem; color: #cc0000; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">{{ app.job_title }}</h2>
          <p style="color: #333; margin-bottom: 0.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;"><strong>Company:</strong> {{ app.company }}</p>
          <p style="color: #555; margin-bottom: 0.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;"><strong>Resume:</strong> {{ app.resume_filename || 'N/A' }}</p>
          <!-- You might want to display the resume text in a more user-friendly way, perhaps with a toggle -->
          <!-- <div v-if="showResume[app.applied_on]" style="color: #666; margin-bottom: 0.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
            <strong>Resume Text:</strong>
            <pre style="background-color: #f9f9f9; padding: 1rem; border-radius: 6px; margin-top: 0.5rem; max-height: 150px; overflow-y: auto; font-family: 'Consolas', 'Monaco', monospace; font-size: 0.8rem; white-space: pre-wrap;">{{ app.resume_text }}</pre>
          </div>
          <button @click="toggleResume(app.applied_on)" style="padding: 0.5rem 1rem; border: 1px solid #ddd; border-radius: 4px; cursor: pointer; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 0.9rem;">
            {{ showResume[app.applied_on] ? 'Hide Resume' : 'Show Resume' }}
          </button> -->
          <p style="color: #555; margin-bottom: 0.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;"><strong>Match Score:</strong> {{ app.match_score }}/10</p>
          <p style="color: #555; margin-bottom: 0.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;"><strong>Feedback:</strong> {{ app.feedback_text || 'No feedback yet' }}</p>
          <p style="color: #777; font-size: 0.9rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Applied on {{ formatDate(app.applied_on) }}</p>
        </div>
      </div>
      <div v-else-if="!loading" style="color: #777; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        You haven't applied to any jobs yet.
      </div>
      <div v-else style="color: #777; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        Loading your applications...
      </div>
    </div>
  </template>
  
  <script>
  import apiClient from '../api'
  import { ref, onMounted } from 'vue';
  
  export default {
    name: 'MyApplications',
    setup() {
      const applications = ref([]);
      const error = ref(null);
      const loading = ref(true);
      // const showResume = ref({}); // If you want to implement resume toggle
  
      const fetchMyApplications = async () => {
        try {
          const response = await apiClient.get('/jobs/my-applications/');
          applications.value = response.data;
          // applications.value.forEach(app => {
          //   showResume.value[app.applied_on] = false; // Initialize resume visibility
          // });
        } catch (err) {
          error.value = 'Failed to load your applications.';
          console.error('Error loading job seeker applications:', err);
        } finally {
          loading.value = false;
        }
      };
  
      const formatDate = (value) => {
        if (!value) return '';
        return new Date(value).toLocaleString();
      };
  
      // const toggleResume = (appliedOn) => {
      //   showResume.value[appliedOn] = !showResume.value[appliedOn];
      // };
  
      onMounted(fetchMyApplications);
  
      return { applications, error, loading, formatDate, /*toggleResume, showResume*/ };
    },
  };
  </script>
  
  <style scoped>
  /* Add any specific styles here */
  </style>