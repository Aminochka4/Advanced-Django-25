# Video Demonstration
link to the video - [here]()

## Implemented API Endpoints
`http://localhost:8000/api/auth/register/` - register page
`http://localhost:8000/api/auth/login/` - login page
`http://localhost:8000/api/auth/verify/<uuid:uuid>/` - verification of the registered account
`http://localhost:8000/api/auth/profiles/` - registered account page

`http://localhost:8000/api/jobs/create/` - creating a job by recruiter
`http://localhost:8000/api/jobs/job<int:job_id>/apply/` - applying to a job by job seeker
`http://localhost:8000/api/jobs/<int:job_id>/` - each created job page
`http://localhost:8000/api/jobs/applications/` - all applications page in recruiter mode
`http://localhost:8000/api/jobs/my-jobs/` - all created jobs by certain recruiter
`http://localhost:8000/api/jobs/my-applications/` - all applications of the job seeker page

`http://localhost:8000/api/resumes/upload/` - uploading the resume by job seeker page