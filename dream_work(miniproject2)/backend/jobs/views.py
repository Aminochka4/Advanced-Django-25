from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import JobListing, Application
from .serializers import JobListingSerializer, ApplicationSerializer
from accounts.models import JobSeekerProfile
from resumes.models import ParsedResume
import spacy
from spacy.matcher import PhraseMatcher
from rest_framework.permissions import IsAuthenticatedOrReadOnly

nlp = spacy.load("en_core_web_md")

class JobCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'recruiter':
            return Response({"error": "Only recruiters can create jobs"}, status=status.HTTP_403_FORBIDDEN)
        serializer = JobListingSerializer(data=request.data)
        if serializer.is_valid():
            job = serializer.save(recruiter=request.user)
            return Response({"message": "Job created successfully", "job": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class JobListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        jobs = JobListing.objects.all()
        serializer = JobListingSerializer(jobs, many=True)
        return Response(serializer.data)

class JobDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, job_id):
        try:
            job = JobListing.objects.get(id=job_id)
            serializer = JobListingSerializer(job)
            return Response(serializer.data)
        except JobListing.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, job_id):
        try:
            job = JobListing.objects.get(id=job_id)
        except JobListing.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Только рекрутер, создавший эту вакансию, может её удалить
        if request.user != job.recruiter:
            return Response({"error": "You do not have permission to delete this job"}, status=status.HTTP_403_FORBIDDEN)
        
        job.delete()
        return Response({"message": "Job deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class ApplyJobView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, job_id):
        if request.user.role != 'job_seeker':
            return Response({"error": "Only job seekers can apply"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            job = JobListing.objects.get(id=job_id)
        except JobListing.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            profile = JobSeekerProfile.objects.filter(user=request.user).latest('id')
        except JobSeekerProfile.DoesNotExist:
            return Response({"error": "Job seeker profile not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            parsed_resume = ParsedResume.objects.filter(user=request.user).order_by('-created_at').first()
            if not parsed_resume:
                raise ParsedResume.DoesNotExist
        except ParsedResume.DoesNotExist:
            return Response({"error": "Parsed resume not found"}, status=status.HTTP_404_NOT_FOUND)

        # Initialize spaCy matcher for skills
        matcher = PhraseMatcher(nlp.vocab)
        required_skills = [skill.name for skill in job.required_skills.all()]
        patterns = [nlp(skill.lower()) for skill in required_skills]
        matcher.add("SKILLS", patterns)

        # Process resume and job
        resume_doc = nlp(parsed_resume.text.lower())
        job_text = f"{job.title} {job.description} {' '.join(required_skills)}".lower()
        job_doc = nlp(job_text)

        # Find skill matches
        matches = matcher(resume_doc)
        matched_skills = set(resume_doc[start:end].text.title() for _, start, end in matches)

        # Calculate match score: 70% skills, 30% general similarity
        skill_score = (len(matched_skills) / max(len(required_skills), 1)) * 7.0
        general_score = resume_doc.similarity(job_doc) * 3.0
        match_score = round(skill_score + general_score, 1)
        match_score = min(match_score, 9.5)

        # Feedback
        feedback_parts = []
        if matched_skills:
            feedback_parts.append(f"Strong match in: {', '.join(matched_skills)}.")
        missing_skills = [s.title() for s in required_skills if s.lower() not in [m.lower() for m in matched_skills]]
        if missing_skills:
            feedback_parts.append(f"Consider developing: {', '.join(missing_skills)}.")
        if match_score < 6.0:
            feedback_parts.append("Your experience may not fully align; highlight relevant projects.")
        feedback = " ".join(feedback_parts) or "Your resume shows some alignment with the role."

        # Create application
        application = Application.objects.create(
            job_seeker=profile,
            job_listing=job,
            resume_used=profile.resume,
            feedback_text=feedback,
            match_score=match_score
        )

        serializer = ApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RecruiterApplicationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'recruiter':
            return Response({"error": "Only recruiters can view applications"}, status=status.HTTP_403_FORBIDDEN)
        
        job_id = request.query_params.get('job_id')
        applications = Application.objects.filter(job_listing__recruiter=request.user)
        if job_id:
            applications = applications.filter(job_listing__id=job_id)
        
        applications = applications.order_by('-match_score')
        data = [
            {
                'job_title': app.job_listing.title,
                'user_email': app.job_seeker.user.email,
                'resume_text': ParsedResume.objects.filter(user_id=str(app.job_seeker.user.id)).order_by('-created_at').first().text,
                'match_score': app.match_score,
                'feedback_text': app.feedback_text,
                'created_at': app.created_at
            }
            for app in applications
        ]
        return Response(data)
    
class RecruiterJobListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'recruiter':
            return Response({"error": "Only recruiters can view their job listings"}, status=status.HTTP_403_FORBIDDEN)
        
        jobs = JobListing.objects.filter(recruiter=request.user).order_by('-created_at')
        serializer = JobListingSerializer(jobs, many=True)
        return Response(serializer.data)

class JobSeekerApplicationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'job_seeker':
            return Response({"error": "Only job seekers can view their applications"}, status=status.HTTP_403_FORBIDDEN)
        
        applications = Application.objects.filter(job_seeker__user=request.user).order_by('-created_at')

        data = [
            {
                'job_title': app.job_listing.title,
                'company': app.job_listing.company_name,  # если у тебя есть поле company_name
                'resume_filename': app.resume_used.name if app.resume_used else None,
                'resume_text': ParsedResume.objects.filter(user=request.user).order_by('-created_at').first().text,
                'match_score': app.match_score,
                'feedback_text': app.feedback_text,
                'applied_on': app.created_at
            }
            for app in applications
        ]
        return Response(data)
