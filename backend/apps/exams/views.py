from rest_framework import generics, views, status, permissions
from rest_framework.response import Response
from .models import Exam, ExamResult
from .serializers import ExamSerializer, ExamResultSerializer, BulkResultEntrySerializer
from apps.notifications.whatsapp import send_result_notification
from apps.students.models import Student
from django.http import HttpResponse
from .utils import generate_marksheet_pdf
from django.shortcuts import get_object_or_404
from django.db.models import Sum

class ExamListCreateView(generics.ListCreateAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

class ExamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

class ExamPublishView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        if request.user.role not in ['principal', 'vice_principal', 'managing_director']:
            return Response(status=status.HTTP_403_FORBIDDEN)
            
        exam = get_object_or_404(Exam, pk=pk)
        exam.is_published = True
        exam.save()
        
        students = Student.objects.filter(exam_results__exam=exam).distinct()
        count = 0
        for student in students:
            results = ExamResult.objects.filter(exam=exam, student=student)
            gpas = [r.gpa for r in results if r.gpa is not None]
            avg_gpa = float(sum(gpas) / len(gpas)) if gpas else 0.0
            send_result_notification(student, exam.name_bn or exam.name, avg_gpa)
            count += 1
            
        return Response({'status': 'published', 'notifications_sent': count})

class ResultEntryView(views.APIView):
    def post(self, request, pk):
        exam = get_object_or_404(Exam, pk=pk)
        serializer = BulkResultEntrySerializer(data=request.data)
        if serializer.is_valid():
            results_data = serializer.validated_data.get('results', [])
            for r_data in results_data:
                ExamResult.objects.update_or_create(
                    exam=exam,
                    student=r_data['student'],
                    subject=r_data['subject'],
                    defaults={
                        'marks_obtained': r_data['marks_obtained'],
                        'total_marks': r_data.get('total_marks', 100),
                        'grade': r_data.get('grade', ''),
                        'gpa': r_data.get('gpa')
                    }
                )
            return Response({'status': 'saved'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentMarksheetView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, student_id, exam_id):
        student = get_object_or_404(Student, student_id=student_id)
        exam = get_object_or_404(Exam, pk=exam_id)
        
        # Access control
        if not exam.is_published:
            if request.user.role not in ['principal', 'vice_principal', 'managing_director', 'teacher']:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            if request.user.role == 'student' and getattr(student, 'user', None) != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            if request.user.role == 'guardian' and getattr(student, 'guardian_phone', None) != getattr(request.user, 'phone', None):
                return Response(status=status.HTTP_403_FORBIDDEN)
                
        results = ExamResult.objects.filter(exam=exam, student=student).select_related('subject')
        
        subject_results = []
        total_marks_obtained = 0
        total_gpa = 0
        valid_subjects = 0
        
        for r in results:
            subject_results.append({
                "subject_name": r.subject.name,
                "subject_name_bn": r.subject.name_bn,
                "marks_obtained": r.marks_obtained,
                "total_marks": r.total_marks,
                "grade": r.grade,
                "gpa": r.gpa
            })
            total_marks_obtained += r.marks_obtained
            if r.gpa is not None:
                total_gpa += r.gpa
                valid_subjects += 1
                
        average = float(total_marks_obtained / valid_subjects) if valid_subjects else 0.0
        overall_gpa = float(total_gpa / valid_subjects) if valid_subjects else 0.0
        
        # Calculate rank
        all_students_results = ExamResult.objects.filter(exam=exam).values('student').annotate(total=Sum('marks_obtained'))
        
        student_total = next((x['total'] for x in all_students_results if x['student'] == student.id), 0)
        higher_scores = [x['total'] for x in all_students_results if x['total'] > student_total]
        
        class_rank = len(higher_scores) + 1
        highest_total = max([x['total'] for x in all_students_results] + [0])
        gap_from_first = highest_total - student_total
        
        return Response({
            "student_id": student.student_id,
            "name": student.name,
            "exam_name": exam.name,
            "subject_results": subject_results,
            "total_marks_obtained": total_marks_obtained,
            "average": average,
            "overall_gpa": overall_gpa,
            "class_rank": class_rank,
            "gap_from_first": gap_from_first
        })

class ClassRankingView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk):
        exam = get_object_or_404(Exam, pk=pk)
        
        all_students_results = ExamResult.objects.filter(exam=exam).values('student').annotate(total=Sum('marks_obtained'))
        student_ids = [x['student'] for x in all_students_results]
        
        students = Student.objects.filter(id__in=student_ids)
        student_dict = {s.id: s for s in students}
        
        ranking_data = []
        for x in all_students_results:
            s_id = x['student']
            student = student_dict.get(s_id)
            if not student: continue
            
            # calculate gpa for this student
            gpas = [r.gpa for r in ExamResult.objects.filter(exam=exam, student=student) if r.gpa is not None]
            avg_gpa = float(sum(gpas) / len(gpas)) if gpas else 0.0
            
            is_current_user = False
            if request.user.role == 'student' and getattr(student, 'user', None) == request.user:
                is_current_user = True
            
            ranking_data.append({
                "student_id": student.student_id,
                "name": student.name,
                "name_bn": student.name_bn,
                "total_marks": x['total'],
                "gpa": avg_gpa,
                "is_current_user": is_current_user
            })
            
        ranking_data.sort(key=lambda item: item['total_marks'], reverse=True)
        
        # Assign ranks
        current_rank = 1
        for i in range(len(ranking_data)):
            if i > 0 and ranking_data[i]['total_marks'] < ranking_data[i-1]['total_marks']:
                current_rank = i + 1
            ranking_data[i]['rank'] = current_rank
            
        return Response(ranking_data)

class MarksheetPDFView(views.APIView):
    def get(self, request, student_id, exam_id):
        student = get_object_or_404(Student, student_id=student_id)
        exam = get_object_or_404(Exam, pk=exam_id)
        results = ExamResult.objects.filter(exam=exam, student=student).select_related('subject')
        pdf = generate_marksheet_pdf(student, exam, results)
        return HttpResponse(pdf, content_type='application/pdf')
