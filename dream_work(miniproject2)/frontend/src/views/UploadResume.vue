<template>
  <div style="max-width: 1200px; margin: 0 auto; padding: 20px; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; min-height: 100vh;">
    <h1 style="font-size: 2.5rem; font-weight: bold; margin-bottom: 1.5rem; color: #cc0000; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Add Resume</h1>
    <div v-if="error" style="background-color: #ffe6e6; color: #cc0000; padding: 15px; border-radius: 6px; margin-bottom: 1rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
      {{ error }}
    </div>
    <div v-if="success" style="background-color: #e6ffe6; color: #008000; padding: 15px; border-radius: 6px; margin-bottom: 1rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
      {{ success }}
    </div>
    <form @submit.prevent="uploadResume" style="max-width: 600px; border: 1px solid #f0f0f0; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); width: 100%;">
      <div style="margin-bottom: 1.5rem;">
        <label for="resume" style="display: block; margin-bottom: 0.5rem; color: #333; font-weight: 500; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Choose Resume to analyze (in PDF/DOCX format)</label>
        <input
          type="file"
          id="resume"
          accept=".pdf,.docx"
          @change="handleFileChange"
          style="display: block; width: calc(100% - 24px); border: 1px solid #ddd; border-radius: 6px; padding: 0.75rem 1rem; font-size: 1rem; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; outline: none;"
        />
      </div>
      <button
        type="submit"
        style="background-color: #cc0000; color: #fff; padding: 10px 15px; border: none; border-radius: 6px; cursor: pointer; font-size: 1rem; transition-colors 0.2s ease-in-out; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-weight: 500; width: 100%;"
        :disabled="!file"
      >
        Add Resume
      </button>
    </form>
  </div>
</template>

<script>
import apiClient from '../api'

export default {
  name: 'UploadResumePage',
  data() {
    return {
      file: null,
      error: null,
      success: null,
    }
  },
  methods: {
    handleFileChange(event) {
      const selectedFile = event.target.files[0]
      if (selectedFile && ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'].includes(selectedFile.type)) {
        this.file = selectedFile
        this.error = null
      } else {
        this.file = null
        this.error = 'Please select a PDF or DOCX file.'
      }
    },
    async uploadResume() {
      if (!this.file) {
        this.error = 'Please select a file to upload.'
        return
      }

      const formData = new FormData()
      formData.append('resume', this.file)

      try {
        this.error = null
        this.success = null
        await apiClient.post('/resumes/upload/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        this.success = 'Resume uploaded successfully!'
        this.file = null
        document.getElementById('resume').value = '' // Reset file input
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to upload resume.'
      }
    },
  },
}
</script>