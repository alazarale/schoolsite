import datetime
import random
import string
from django.templatetags.static import static
from urllib import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from adminpanel.models import Attendance, ClassSchedule, FinalScore, Result, SPGradeAssociation, ScheduleTimes, StudentResult, Homework, Assignment
from course.models import Course, CourseGradeAssociation, Module
from exam.models import Exam, ExamGradeAssociation, ExamQuestion
from .serializers import (
                        AllResultSerializer,
                        AttendaceStudentSerializers,
                        FinalScoreHRSerializer,
                        FinalScoreSerializer,
                        HomeRoomSingleSerializers,
                        SchoolPaymentSerializer,
                        StudentClassScheduleSerializer,
                        StudentExamQuestionSerializer,
                        StudentExamSerializer,
                        StudentScheduleTimesSerializer,
                        StudentSerializers, 
                        HomeRoomSerializers,
                        TeacherCourseModuleSerializer, 
                        TeacherHomeSerializer, 
                        AttendaceSerializers,
                        MyTokenObtainPairSerializer,
                        StudentParentSerializer,
                        StudentShortSerializer,
                        GradeSubjectSerializers,
                        TeachingSingleSerializers,
                        ResultSerializers,
                        ResultStudentSerializers,
                        MainStudentSerializers,
                        StudentProfileSerializers,
                        HomeworkSerializers,
                        TeacherCourseSerializer,
                        )
from .permissions import HasTeacherPermission, HasParentPermission, HasStudentPermission
from acctype.models import Student, Teacher, Parent, StudentParent
from accyear.models import GradeStudent, GradeSubject, HomeRoomTeacher, GrSubTeacher, Subject
from collections import namedtuple
from datetime import date, timedelta

from api import serializers


TeacherHome = namedtuple('TeacherHome', ('home_room', 'teaching'))


class StudentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasTeacherPermission]
    def get(self, request, *args, **kwargs):
        studs = Student.objects.all()
        serializer = StudentSerializers(studs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeacherAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasTeacherPermission]
    
    def get(self, request, *args, **kwargs):
        teacher = Teacher.objects.get(user=request.user)
        home_room = HomeRoomTeacher.objects.filter(teacher=teacher)
        teaching = GrSubTeacher.objects.filter(teacher=teacher)
        teacher_home = TeacherHome(home_room=home_room, teaching=teaching)
        serializer = TeacherHomeSerializer(teacher_home)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TeacherHRAttendaceAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasTeacherPermission]

    def get(self, request, pk):
        today = date.today()
        grade = HomeRoomTeacher.objects.get(id=pk).grade
        attendances = Attendance.objects.filter(student__grade__grade=grade, att_date=today)
        serializer = AttendaceSerializers(attendances, many=True)
        final = {'day': today, 'att': serializer.data}
        return Response(final, status=status.HTTP_200_OK)


class TeacherHRAttendaceTakeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasTeacherPermission]

    def get(self, request, pk):
        today = date.today()
        grade = HomeRoomTeacher.objects.get(id=pk).grade
        students = Student.objects.filter(grade__grade=grade).reverse()
        serializer = AttendaceStudentSerializers(students, many=True)
        final = {'day': today, 'att': serializer.data}
        return Response(final, status=status.HTTP_200_OK)


class TeacherHR(APIView):
    permission_classes = [permissions.IsAuthenticated, HasTeacherPermission]

    def get(self, request, pk):
        homeroom = HomeRoomTeacher.objects.get(id=pk)
        serializer = HomeRoomSingleSerializers(homeroom)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeacherHRAttTaken(APIView):
    permission_classes = [permissions.IsAuthenticated, HasTeacherPermission]

    def get(self, request, pk):
        today = date.today()
        homeroom = HomeRoomTeacher.objects.get(id=pk)
        
        att = Attendance.objects.filter(student__grade__grade=homeroom.grade, att_date=today)
        
        if att.count() > 0: 
            return Response({'stat': True}, status=status.HTTP_200_OK)
        else: 
            return Response({'stat': False}, status=status.HTTP_200_OK)


class TeacherHRAttendance(APIView):
    permission_classes = [permissions.IsAuthenticated, HasTeacherPermission]

    def get(self, request, pk):
        today = date.today()
        homeroom = HomeRoomTeacher.objects.get(id=pk)
        
        att = Attendance.objects.filter(student__grade__grade=homeroom.grade, att_date=today)
        print(att)
        
        return Response({'stat': True}, status=status.HTTP_200_OK)
        


class TeacherTeaching(APIView):
    permission_classes = [permissions.IsAuthenticated, HasTeacherPermission]

    def get(self, request, pk):
        homeroom = GrSubTeacher.objects.get(id=pk)
        serializer = TeachingSingleSerializers(homeroom)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ParentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasParentPermission]
    
    def get(self, request, *args, **kwargs):
        parent = Parent.objects.get(user=request.user)
        parent_stud = StudentParent.objects.filter(parent=parent)
        
        serializer = StudentParentSerializer(parent_stud, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ParentStudAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasParentPermission]

    def get(self, request, pk):
        parent = Parent.objects.get(user=request.user)
        parent_stud = StudentParent.objects.get(id=pk)
        if parent_stud.parent == parent:    
            serializer = StudentParentSerializer(parent_stud)
        else:
            return Response()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ParentStudSubAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasParentPermission]

    def get(self, request, pk):
        parent = Parent.objects.get(user=request.user)
        parent_stud = StudentParent.objects.get(id=pk)
        if parent_stud.parent == parent:
            stud = parent_stud.student
            subs = stud.grade.all()[0].grade.subjects.all()
            print(subs)    
            serializer = GradeSubjectSerializers(subs, many=True)
        else:
            return Response()

        return Response(serializer.data, status=status.HTTP_200_OK)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ResultAddAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasTeacherPermission]

    def post(self, request, pk):
        serializer = ResultSerializers(data=request.data)
        if serializer.is_valid():
            gr_sub = GrSubTeacher.objects.get(id=pk)
            new_result = Result.objects.create(gr_sub=gr_sub.gr_sub, description=serializer['description'].value, out_of=serializer['out_of'].value, privacy=serializer['privacy'].value)
            students = gr_sub.gr_sub.grade.students.all()
            students = list(sorted(students, key=lambda obj: obj.student.user.first_name+'     '+obj.student.user.last_name))
            send_serializer = ResultStudentSerializers(students, many=True)
            print(type(new_result.out_of))
            return Response({'id': new_result.id, 'max_value': new_result.out_of, 'students': send_serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResultSumitAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasTeacherPermission]

    def post(self, request, pk):
        try:
            data = request.data
            result = Result.objects.get(id=data['res_id'])
            del data['res_id']
            for k in data.keys():
                rcvd = data[k]
                gr_stud = GradeStudent.objects.get(id=rcvd['grStud'])
                studRes = StudentResult.objects.create(student=gr_stud.student, result=result, score=float(rcvd['value']))
            return Response({'stat': 'success'}, status=status.HTTP_201_CREATED)
        except:
            return Response({'stat': 'failed'})


class TeacherStudsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasTeacherPermission]

    def get(self, request, pk):
        gr_sub = GrSubTeacher.objects.get(id=pk)
        print(gr_sub.gr_sub.grade)
        studs = Student.objects.filter(grade__grade=gr_sub.gr_sub.grade)
        studs = list(sorted(studs, key=lambda obj: obj.user.first_name+'     '+obj.user.last_name))
        serializer = MainStudentSerializers(studs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeacherHRStudsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasTeacherPermission]

    def get(self, request, pk):
        homeroom = HomeRoomTeacher.objects.get(id=pk)
        
        studs = Student.objects.filter(grade__grade=homeroom.grade)
        studs = list(sorted(studs, key=lambda obj: obj.user.first_name+'     '+obj.user.last_name))
        serializer = MainStudentSerializers(studs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasTeacherPermission]

    def get(self, request, pk):
        stud = Student.objects.get(id=pk)
        
        serializer = StudentProfileSerializers(stud)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeacherHomeworkAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasTeacherPermission]

    def get(self, request, pk):
        today = date.today()
        gr_sub = GrSubTeacher.objects.get(id=pk).gr_sub
        hw_today = Homework.objects.filter(gr_sub=gr_sub, due_date=today)
        hw_all = Homework.objects.filter(gr_sub=gr_sub)
        hw_future = []
        hw_past = []
        for hw in hw_all:
            if hw.due_date > today:
                hw_future.append(hw)
            elif hw.due_date < today and len(hw_past) < 10:
                hw_past.append(hw)

        today_serializer = HomeworkSerializers(hw_today, many=True)
        future_serializer = HomeworkSerializers(hw_future, many=True)
        past_serializer = HomeworkSerializers(hw_past, many=True)
        
        return Response({'today': today_serializer.data, 'future': future_serializer.data, 'past': past_serializer.data}, status=status.HTTP_200_OK)


class TeacherHomeworkAddAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasTeacherPermission]

    def post(self, request, pk):
        try:
       
            data = request.data
            files = request.FILES['file']
        
            gr_sub = GrSubTeacher.objects.get(id=pk).gr_sub

            homework = Homework.objects.create(gr_sub=gr_sub, for_who="All Class", title=data['title'], description=data['description'], desc_file=files, due_date=datetime.datetime.strptime(data['due_date'].split(' ')[0], '%Y-%m-%d'))
        
            return Response({'stat': 'success'}, status=status.HTTP_201_CREATED)
        except:
            
            return Response({'stat': 'failed'})


class TeacherSubmittedAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasTeacherPermission]

    def get(self, request, pk):
        gr_sub = GrSubTeacher.objects.get(id=pk).gr_sub
        subject = gr_sub.subject
        studs = GradeStudent.objects.filter(grade=gr_sub.grade)
        final_colect = []
        for i in studs:
            if FinalScore.objects.filter(gr_stud=i, subject=subject).count() > 0:
                res = FinalScore.objects.filter(gr_stud=i, subject=subject)[0]
                final_colect.append(res)
            else:
                res = FinalScore.objects.create(gr_stud=i, subject=subject)
                final_colect.append(res)
        final_colect = list(sorted(final_colect, key=lambda obj: obj.gr_stud.student.user.first_name+'     '+obj.gr_stud.student.user.last_name))
        serializers = FinalScoreSerializer(final_colect, many=True)
        
        return Response(serializers.data, status=status.HTTP_200_OK)


class TeacherSubmittedAddAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasTeacherPermission]

    def post(self, request, pk):
        try:
            gr_sub = GrSubTeacher.objects.get(id=pk).gr_sub
            subject = gr_sub.subject
            w_list = ['Add 1st Sem 1st 50%', 'Add 1st Sem 2nd 50%', 'Add 2nd Sem 1st 50%', 'Add 2nd Sem 2nd 50%']
            data = request.data
            wt = data['wt']
            stud_data = data['data']
            print(w_list.index(wt))
            for i in stud_data.keys():
                gr_stud = GradeStudent.objects.get(id=i)
                final_score = FinalScore.objects.filter(gr_stud=gr_stud, subject=subject)[0]
                if w_list.index(wt) == 0:
                    final_score.first_50 = float(stud_data[i])
                    final_score.save()
                elif w_list.index(wt) == 1:
                    final_score.second_50 = float(stud_data[i])
                    final_score.save()
                elif w_list.index(wt) == 2:
                    final_score.third_50 = float(stud_data[i])
                    final_score.save() 
                elif w_list.index(wt) == 3:
                    final_score.forth_50 = float(stud_data[i])
                    final_score.save()         

            
            return Response({'stat': 'success'}, status=status.HTTP_201_CREATED)
        except:
            return Response({'stat': 'failed'})


class TeacherHRAttTake(APIView):
    permission_classes = [permissions.IsAuthenticated, HasTeacherPermission]

    def post(self, request, pk):
        try:
            data = request.data
            today = date.today()
            for i in data.keys():
                stud = Student.objects.get(stud_id=i)
                if data[i] == 'P':
                    att = Attendance.objects.create(student=stud, stat='Present', att_date=today)
                elif data[i] == 'A':
                    att = Attendance.objects.create(student=stud, stat='Absent', att_date=today)
                elif data[i] == 'L':
                    att = Attendance.objects.create(student=stud, stat='Leave', att_date=today)

            return Response({'stat': 'success'}, status=status.HTTP_201_CREATED)
        except:
            
            return Response({'stat': 'failed'})


class TeacherHRClassScoreAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasTeacherPermission]

    def get(self, request, pk):
        homeroom = HomeRoomTeacher.objects.get(id=pk)
        g_subjects = GradeSubject.objects.filter(grade=homeroom.grade)
        gr_studs = GradeStudent.objects.filter(grade=homeroom.grade)
        gr_studs = list(sorted(gr_studs, key=lambda obj: obj.student.user.first_name+'     '+obj.student.user.last_name))
        final_data = []
        for stud in gr_studs:
            f_d = {}
            f_d['studName'] = stud.student.user.first_name + ' ' + stud.student.user.last_name
            f_d['studId'] = stud.student.stud_id
            if stud.student.profile_pic:
                f_d['studPp'] = stud.student.profile_pic.url
            else: 
                f_d['studPp'] = static('noprofile.png')
            all_subs = []
            for sub in g_subjects:
                if FinalScore.objects.filter(gr_stud=stud, subject=sub.subject).count() > 0:
                    final_score = FinalScore.objects.filter(gr_stud=stud, subject=sub.subject)[0]
                    
                else:
                    final_score = FinalScore.objects.create(gr_stud=stud, subject=sub.subject)
                sub_serializer = FinalScoreHRSerializer(final_score)
                all_subs.append(sub_serializer.data)
            f_d['subs'] = all_subs
            final_data.append(f_d)
        
        return Response(final_data, status=status.HTTP_200_OK)


class TeacherCourseAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasTeacherPermission]

    def post(self, request, pk):
        try:
            data = request.data
            gr_sub = GrSubTeacher.objects.get(id=pk)
            grade = gr_sub.gr_sub.grade
            subject = gr_sub.gr_sub.subject
            title = data['title']
            overview = data['overview']
            slug = title + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            slug = slug.strip(' ')
            print(slug)
            course = Course.objects.create(owner=gr_sub.teacher.user, subject=subject, title=title, slug=slug, overview=overview)
            c_g_ass = CourseGradeAssociation.objects.create(grades=grade, course=course)
    
            return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        except:
            return Response({'status': 'fail'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TeacherCourseSeeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasTeacherPermission]

    def get(self, request, pk):
        gr_sub = GrSubTeacher.objects.get(id=pk)
        subject = gr_sub.gr_sub.subject
        grade = gr_sub.gr_sub.grade
        c_g = CourseGradeAssociation.objects.filter(grades=grade, course__subject=subject, course__owner=gr_sub.teacher.user)
        courses = []
        for i in c_g:
            courses.append(i.course)

        serializers = TeacherCourseSerializer(courses, many=True)
        
        return Response(serializers.data, status=status.HTTP_200_OK)



class TeacherCourseModuleSeeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasTeacherPermission]

    def get(self, request, pk, mpk):
        gr_sub = GrSubTeacher.objects.get(id=pk)
        course = Course.objects.get(id=mpk)
        course_title = course.title
        modules = Module.objects.filter(course=course)
        serializers = TeacherCourseModuleSerializer(modules, many=True)
        
        return Response({'course_title': course_title, 'modules': serializers.data}, status=status.HTTP_200_OK)


class TeacherCourseModuleAddAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasTeacherPermission]

    def post(self, request, pk, mpk):
        data = request.data
        gr_sub = GrSubTeacher.objects.get(id=pk)
        course = Course.objects.get(id=mpk)
        title = data['title']
        desc = data['description']
        new_module = Module.objects.create(course=course, title=title, description=desc)
   
        return Response('sdf', status=status.HTTP_201_CREATED)


class StudentSubjectAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasStudentPermission]

    def get(self, request):
        student = Student.objects.get(user=request.user)
        subs = student.grade.all()[0].grade.subjects
       
        serializer = GradeSubjectSerializers(subs, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentHomeworkAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasStudentPermission]

    def get(self, request):
        today = date.today()
        gr_subs = request.user.student.all()[0].grade.all()[0].grade.subjects.all()
        today_serializer = []
        future_serializer = []
        past_serializer = []
        for gr_sub in gr_subs:
            hw_today = Homework.objects.filter(gr_sub=gr_sub, due_date=today)
            hw_all = Homework.objects.filter(gr_sub=gr_sub)
            hw_future = []
            hw_past = []
            for hw in hw_all:
                if hw.due_date > today:
                    hw_future.append(hw)
                elif hw.due_date < today and len(hw_past) < 10:
                    hw_past.append(hw)
            
            for i in HomeworkSerializers(hw_today, many=True).data:
                today_serializer.append(i)
            for i in HomeworkSerializers(hw_future, many=True).data:
                future_serializer.append(i)
            for i in HomeworkSerializers(hw_past, many=True).data:
                past_serializer.append(i)
            

       
        return Response({'today': today_serializer, 'future': future_serializer, 'past': past_serializer}, status=status.HTTP_200_OK)


class StudentGradeReportAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasStudentPermission]

    def get(self, request):
        grade = request.user.student.all()[0].grade.all()[0].grade
        stud = request.user.student.all()[0]
        g_subjects = GradeSubject.objects.filter(grade=grade)
        
        f_d = {}
        f_d['studName'] = stud.user.first_name + ' ' + stud.user.last_name
        f_d['studId'] = stud.stud_id
        if stud.profile_pic:
            f_d['studPp'] = stud.profile_pic.url
        else: 
            f_d['studPp'] = static('noprofile.png')
        all_subs = []
        for sub in g_subjects:
            if FinalScore.objects.filter(gr_stud=stud.grade.all()[0], subject=sub.subject).count() > 0:
                final_score = FinalScore.objects.filter(gr_stud=stud.grade.all()[0], subject=sub.subject)[0]
                
            else:
                final_score = FinalScore.objects.create(gr_stud=stud.grade.all()[0], subject=sub.subject)
            sub_serializer = FinalScoreHRSerializer(final_score)
            all_subs.append(sub_serializer.data)
        f_d['subs'] = all_subs
        
        return Response(f_d, status=status.HTTP_200_OK)


class StudentAttendanceAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasStudentPermission]

    def get(self, request):
        grade = request.user.student.all()[0].grade.all()[0].grade
        stud = request.user.student.all()[0]
        attendances = Attendance.objects.filter(student=stud)
        print(attendances)
        serialized_data = AttendaceSerializers(attendances, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)


class StudentSubjectHomeworkAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasStudentPermission]

    def get(self, request, pk):
        today = date.today()
        sub = Subject.objects.get(id=pk)
        gr_sub = request.user.student.all()[0].grade.all()[0].grade.subjects.filter(subject=sub)[0]
        today_serializer = []
        future_serializer = []
        past_serializer = []
        
        hw_today = Homework.objects.filter(gr_sub=gr_sub, due_date=today)
        hw_all = Homework.objects.filter(gr_sub=gr_sub)
        hw_future = []
        hw_past = []
        for hw in hw_all:
            if hw.due_date > today:
                hw_future.append(hw)
            elif hw.due_date < today and len(hw_past) < 10:
                hw_past.append(hw)
        
        for i in HomeworkSerializers(hw_today, many=True).data:
            today_serializer.append(i)
        for i in HomeworkSerializers(hw_future, many=True).data:
            future_serializer.append(i)
        for i in HomeworkSerializers(hw_past, many=True).data:
            past_serializer.append(i)
            

       
        return Response({'today': today_serializer, 'future': future_serializer, 'past': past_serializer}, status=status.HTTP_200_OK)


class StudentSubjectResultsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasStudentPermission]

    def get(self, request, pk):
        sub = Subject.objects.get(id=pk)
        
        grade = request.user.student.all()[0].grade.all()[0].grade
        gr_sub = GradeSubject.objects.filter(grade=grade, subject=sub)[0]
        
        stud_results = StudentResult.objects.filter(result__gr_sub= gr_sub,student=request.user.student.all()[0])
        
        serializers = AllResultSerializer(stud_results, many=True)
       
        return Response(serializers.data, status=status.HTTP_200_OK)


class StudentSubjectReportAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasStudentPermission]

    def get(self, request, pk):
        sub = Subject.objects.get(id=pk)
        grade_s = request.user.student.all()[0].grade.all()[0]

        if FinalScore.objects.filter(gr_stud=grade_s, subject=sub).count() > 0:
            final_score = FinalScore.objects.filter(gr_stud=grade_s, subject=sub)[0] 
        else:
            final_score = FinalScore.objects.create(gr_stud=grade_s, subject=sub)
        sub_serializer = FinalScoreSerializer(final_score)
        
        return Response(sub_serializer.data, status=status.HTTP_200_OK)


class StudentTimetableAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasStudentPermission]

    def get(self, request):
        final_data = {}
        grade = request.user.student.all()[0].grade.all()[0].grade
        times = ScheduleTimes.objects.all()
        time_serializer = StudentScheduleTimesSerializer(times, many=True)
        final_data['times'] = time_serializer.data

        class_schedules = ClassSchedule.objects.filter(grade=grade)
        cl_serializer = StudentClassScheduleSerializer(class_schedules, many=True)
        
        final_data['schedules'] = cl_serializer.data
        
        return Response(final_data, status=status.HTTP_200_OK)


class StudentExamAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasStudentPermission]

    def get(self, request, pk):
        sub = Subject.objects.get(id=pk)
        stud = request.user.student.all()[0]
        grade = request.user.student.all()[0].grade.all()[0].grade
        exam_grade = ExamGradeAssociation.objects.filter(grade=grade, exam__subject=sub, exam__status="active")
        serializer = StudentExamSerializer(exam_grade, many=True, context={'request': stud})
    
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentExamSeeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasStudentPermission]

    def get(self, request, pk, pk2):
        sub = Subject.objects.get(id=pk)
        stud = request.user.student.all()[0]
        
        exam = ExamGradeAssociation.objects.get(id=pk2)
        
        final_data = {}
        if exam.exam.subject == sub and exam.grade == stud.grade.all()[0].grade:
            questions = exam.exam.exam_questions.all()
            serializer = StudentExamQuestionSerializer(questions, many=True)
            final_data['questions'] = serializer.data
        
        final_data['title'] = exam.exam.title 
        final_data['time'] = exam.exam.time
        
    
        return Response(final_data, status=status.HTTP_200_OK)


class SchoolPaymentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasStudentPermission]

    def get(self, request):
        grade = request.user.student.all()[0].grade.all()[0].grade
        payments = SPGradeAssociation.objects.filter(grade=grade)
        
        serializer = SchoolPaymentSerializer(payments, many=True, context={'request': request})
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class ParentStudSubResultAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasParentPermission]

    def get(self, request, pk, pk2):
        parent = Parent.objects.get(user=request.user)
        parent_stud = StudentParent.objects.get(id=pk)
        if parent_stud.parent == parent:
            stud = parent_stud.student
            sub = Subject.objects.get(id=pk2)
            gr_sub = stud.grade.all()[0].grade.subjects.all().filter(subject=sub)[0]
            results = StudentResult.objects.filter(student=stud, result__gr_sub=gr_sub, result__privacy='All')
            print(results)
            serializers = AllResultSerializer(results, many=True)
            
        else:
            return Response()

        return Response(serializers.data, status=status.HTTP_200_OK)


class ParentSubmittedSubResultAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasParentPermission]

    def get(self, request, pk, pk2):
        parent = Parent.objects.get(user=request.user)
        parent_stud = StudentParent.objects.get(id=pk)
        if parent_stud.parent == parent:
            stud = parent_stud.student
            grade_s = stud.grade.all()[0]
            sub = Subject.objects.get(id=pk2)

            if FinalScore.objects.filter(gr_stud=grade_s, subject=sub).count() > 0:
                final_score = FinalScore.objects.filter(gr_stud=grade_s, subject=sub)[0] 
            else:
                final_score = FinalScore.objects.create(gr_stud=grade_s, subject=sub)
            sub_serializer = FinalScoreSerializer(final_score)
        
        return Response(sub_serializer.data, status=status.HTTP_200_OK)


class ParentGradeReportAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasParentPermission]

    def get(self, request, pk):
        parent = Parent.objects.get(user=request.user)
        parent_stud = StudentParent.objects.get(id=pk)
        if parent_stud.parent == parent:
            stud = parent_stud.student
            grade = stud.grade.all()[0].grade
            g_subjects = GradeSubject.objects.filter(grade=grade)
            
            f_d = {}
            f_d['studName'] = stud.user.first_name + ' ' + stud.user.last_name
            f_d['studId'] = stud.stud_id
            if stud.profile_pic:
                f_d['studPp'] = stud.profile_pic.url
            else: 
                f_d['studPp'] = static('noprofile.png')
            all_subs = []
            clac = True
            tot = 0
            for sub in g_subjects:

                if FinalScore.objects.filter(gr_stud=stud.grade.all()[0], subject=sub.subject).count() > 0:
                    final_score = FinalScore.objects.filter(gr_stud=stud.grade.all()[0], subject=sub.subject)[0]
                    
                else:
                    final_score = FinalScore.objects.create(gr_stud=stud.grade.all()[0], subject=sub.subject)
                sub_serializer = FinalScoreHRSerializer(final_score)
                all_subs.append(sub_serializer.data)
            f_d['subs'] = all_subs
        
        return Response(f_d, status=status.HTTP_200_OK)


class ParentAttendanceAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasParentPermission]

    def get(self, request, pk):
        parent = Parent.objects.get(user=request.user)
        parent_stud = StudentParent.objects.get(id=pk)
        if parent_stud.parent == parent:
            stud = parent_stud.student
            grade = stud.grade.all()[0].grade
            
            attendances = Attendance.objects.filter(student=stud)
            
            serialized_data = AttendaceSerializers(attendances, many=True)
            
        return Response(serialized_data.data, status=status.HTTP_200_OK)


class ParentSubjectHomeworkAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasParentPermission]

    def get(self, request, pk, pk2):
        parent = Parent.objects.get(user=request.user)
        parent_stud = StudentParent.objects.get(id=pk)
        today = date.today()
        if parent_stud.parent == parent:
            print(pk, pk2)
            sub = Subject.objects.get(id=pk2)
            stud = parent_stud.student
            grade = stud.grade.all()[0].grade
            gr_sub = GradeSubject.objects.filter(grade=grade, subject=sub)[0]
            today_serializer = []
            future_serializer = []
            past_serializer = []
            
            hw_today = Homework.objects.filter(gr_sub=gr_sub, due_date=today)
            hw_all = Homework.objects.filter(gr_sub=gr_sub)
            hw_future = []
            hw_past = []
            print(hw_all)
            for hw in hw_all:
                if hw.due_date > today:
                    hw_future.append(hw)
                elif hw.due_date < today and len(hw_past) < 10:
                    hw_past.append(hw)
            
            for i in HomeworkSerializers(hw_today, many=True).data:
                today_serializer.append(i)
            for i in HomeworkSerializers(hw_future, many=True).data:
                future_serializer.append(i)
            for i in HomeworkSerializers(hw_past, many=True).data:
                past_serializer.append(i)
            

       
        return Response({'today': today_serializer, 'future': future_serializer, 'past': past_serializer}, status=status.HTTP_200_OK)


class ParentHomeworkAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasParentPermission]

    def get(self, request, pk):
        
        parent = Parent.objects.get(user=request.user)
        parent_stud = StudentParent.objects.get(id=pk)
        today = date.today()
        if parent_stud.parent == parent:

            gr_subs = parent_stud.student.grade.all()[0].grade.subjects.all()
            today_serializer = []
            future_serializer = []
            past_serializer = []
            for gr_sub in gr_subs:
                hw_today = Homework.objects.filter(gr_sub=gr_sub, due_date=today)
                hw_all = Homework.objects.filter(gr_sub=gr_sub)
                hw_future = []
                hw_past = []
                for hw in hw_all:
                    if hw.due_date > today:
                        hw_future.append(hw)
                    elif hw.due_date < today and len(hw_past) < 10:
                        hw_past.append(hw)
                
                for i in HomeworkSerializers(hw_today, many=True).data:
                    today_serializer.append(i)
                for i in HomeworkSerializers(hw_future, many=True).data:
                    future_serializer.append(i)
                for i in HomeworkSerializers(hw_past, many=True).data:
                    past_serializer.append(i)
            

       
        return Response({'today': today_serializer, 'future': future_serializer, 'past': past_serializer}, status=status.HTTP_200_OK)


class ParentTimetableAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasParentPermission]

    def get(self, request, pk):
        parent = Parent.objects.get(user=request.user)
        parent_stud = StudentParent.objects.get(id=pk)
        today = date.today()
        if parent_stud.parent == parent:
            stud = parent_stud.student
            grade = stud.grade.all()[0].grade

            final_data = {}
            
            times = ScheduleTimes.objects.all()
            time_serializer = StudentScheduleTimesSerializer(times, many=True)
            final_data['times'] = time_serializer.data

            class_schedules = ClassSchedule.objects.filter(grade=grade)
            cl_serializer = StudentClassScheduleSerializer(class_schedules, many=True)
            
            final_data['schedules'] = cl_serializer.data
        
        return Response(final_data, status=status.HTTP_200_OK)

class ParentPaymentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasParentPermission]

    def get(self, request, pk):
        parent = Parent.objects.get(user=request.user)
        parent_stud = StudentParent.objects.get(id=pk)
        
        if parent_stud.parent == parent:
            stud = parent_stud.student
            grade = stud.grade.all()[0].grade
        
            payments = SPGradeAssociation.objects.filter(grade=grade)
            
            serializer = SchoolPaymentSerializer(payments, many=True, context={'request': stud})
        
        return Response(serializer.data, status=status.HTTP_200_OK)