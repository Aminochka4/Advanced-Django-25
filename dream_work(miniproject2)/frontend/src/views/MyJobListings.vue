<template>
    <div style="max-width: 1200px; margin: 0 auto; padding: 20px;">
      <h1 style="font-size: 2.5rem; font-weight: bold; margin-bottom: 1.5rem; color: #cc0000; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">My Job Listings</h1>
      <div v-if="error" style="background-color: #ffe6e6; color: #cc0000; padding: 15px; border-radius: 6px; margin-bottom: 1rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        {{ error }}
      </div>
      <div v-if="jobs.length" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem;">
        <div v-for="job in jobs" :key="job.id" style="background-color: #fff; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); border-radius: 8px; padding: 1.5rem; border: 1px solid #f0f0f0; display: flex; flex-direction: column; justify-content: space-between;">
          <div>
            <h2 style="font-size: 1.5rem; font-weight: bold; margin-bottom: 0.75rem; color: #cc0000; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">{{ job.title }}</h2>
            <p style="color: #333; margin-bottom: 0.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;"><strong>Company:</strong> {{ job.company_name }}</p>
            <p style="color: #555; margin-bottom: 0.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;"><strong>Location:</strong> {{ job.location }}</p>
            <p style="color: #555; margin-bottom: 0.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;"><strong>Type:</strong> {{ capitalize(job.employment_type) }}</p>
            <p style="color: #555; margin-bottom: 0.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;"><strong>Experience:</strong> {{ job.required_experience }} years</p>
            <p style="color: #555; margin-bottom: 0.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
              <strong>Skills:</strong> {{ job.required_skills_data.map(s => s.name).join(', ') }}
            </p>
            <p style="color: #666; margin-top: 0.75rem; font-size: 0.9rem; line-height: 1.4; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">{{ truncate(job.description, 200) }}</p>
          </div>
          <div style="margin-top: 1rem;">
            <p style="color: #A9A9A9; margin-bottom: 0.5rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">* If the vacancy is no longer relevant, you can delete it</p>
            <button @click="deleteJob(job.id)" style="padding: 0.5rem 1rem; border: 1px solid #ddd; border-radius: 4px; cursor: pointer; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f44336; color: white;">Delete</button>
          </div>
        </div>
      </div>
      <div v-else-if="!loading" style="color: #777; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        No job listings created yet.
      </div>
      <div v-else style="color: #777; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        Loading job listings...
      </div>
    </div>
  </template>
  
  <script>
  import apiClient from '../api'
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router'; // Import useRouter for navigation
  
  export default {
    name: 'MyJobListings',
    setup() {
      const jobs = ref([]);
      const error = ref(null);
      const loading = ref(true);
      const router = useRouter(); // Initialize router
  
      const fetchMyJobs = async () => {
        try {
          const response = await apiClient.get('/jobs/my-jobs/'); // Assuming this endpoint returns the recruiter's jobs
          jobs.value = response.data;
        } catch (err) {
          error.value = 'Failed to load your job listings.';
          console.error('Error loading recruiter jobs:', err);
        } finally {
          loading.value = false;
        }
      };
  
      const deleteJob = async (jobId) => {
        if (confirm('Are you sure you want to delete this job listing?')) {
          try {
            await apiClient.delete(`/jobs/${jobId}/`); // Assuming this endpoint deletes a job by ID
            jobs.value = jobs.value.filter(job => job.id !== jobId); // Remove deleted job from the list
          } catch (err) {
            error.value = 'Failed to delete the job listing.';
            console.error('Error deleting job:', err);
          }
        }
      };
  
      const editJob = (jobId) => {
        router.push(`/recruiter/edit-job/${jobId}`); // Navigate to the edit page with job ID
      };
  
      const capitalize = (value) => {
        if (!value) return '';
        return value.charAt(0).toUpperCase() + value.slice(1);
      };
  
      const truncate = (value, length) => {
        if (!value) return '';
        return value.length > length ? value.substring(0, length) + '...' : value;
      };
  
      onMounted(fetchMyJobs);
  
      return { jobs, error, loading, capitalize, truncate, deleteJob, editJob };
    },
  };
  </script>
  
  <style scoped>
  /* Add any specific styles for this component here */
  </style>