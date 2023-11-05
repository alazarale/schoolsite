from django.templatetags.static import static
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.decorators import api_view
from acctype.models import Student, StudentParent
from accyear.models import AccadamicYear, HomeRoomTeacher, GrSubTeacher, GradeStudent, GradeSubject
from adminpanel.models import ClassSchedule, FinalScore, Result, Homework, Assignment, Attendance, SPGradeAssociation, ScheduleTimes, StudentResult
from course.models import Course, Module
from exam.models import Exam, ExamGradeAssociation, ExamQuestion
from django.contrib.auth.models import User
from datetime import date, timedelta

class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['stud_id', 'gender', 'birth_date', 'created', 'updated']
    

class UserSerializers(serializers.ModelSerializer):
 
    class Meta:
        model = User
        fields =  '__all__'


class HomeRoomSerializers(serializers.ModelSerializer):
    grade_name = serializers.SerializerMethodField(read_only=True)
    stud_no = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = HomeRoomTeacher
        fields = [
            'id',
            'teacher',
            'grade_name',
            'stud_no'
            ]
    
    def get_grade_name(self, obj):
        return str(obj.grade.grade_num) + obj.grade.section

    def get_stud_no(self, obj):
        grade = obj.grade
        studs = GradeStudent.objects.filter(grade=grade)
        return len(studs)

class GrSubTeacherSerializer(serializers.ModelSerializer):
    grade_name = serializers.SerializerMethodField(read_only=True)
    subject = serializers.SerializerMethodField(read_only=True)
    stud_no = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = GrSubTeacher
        fields = [
            'id',
            'grade_name',
            'subject',
            'stud_no'
        ]
    
    def get_grade_name(self, obj):
        return str(obj.gr_sub.grade.grade_num) + obj.gr_sub.grade.section
    
    def get_subject(self, obj):
        return obj.gr_sub.subject.name
    
    def get_stud_no(self, obj):
        grade = obj.gr_sub.grade
        studs = GradeStudent.objects.filter(grade=grade)
        return len(studs)
    

class TeacherHomeSerializer(serializers.Serializer):
    home_room = HomeRoomSerializers(many=True)
    teaching = GrSubTeacherSerializer(many=True)


class HomeRoomSingleSerializers(serializers.ModelSerializer):
    grade = serializers.SerializerMethodField(read_only=True)
    students = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = HomeRoomTeacher
        fields = ['grade', 'students', 'id']

    def get_grade(self, obj):
        return str(obj.grade.grade_num) + obj.grade.section

    def get_students(self, obj):
        return len(obj.grade.students.all()) 
      

class TeachingSingleSerializers(serializers.ModelSerializer):
    grade = serializers.SerializerMethodField(read_only=True)
    students = serializers.SerializerMethodField(read_only=True)
    subject = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = GrSubTeacher
        fields = ['grade', 'students', 'subject', 'id']

    def get_grade(self, obj):
        return str(obj.gr_sub.grade.grade_num) + obj.gr_sub.grade.section

    def get_students(self, obj):
        return len(obj.gr_sub.grade.students.all()) 
    
    def get_subject(self, obj):
        return obj.gr_sub.subject.name


class AttendaceSerializers(serializers.ModelSerializer):
    stud_pp = serializers.SerializerMethodField(read_only=True)
    stud_name = serializers.SerializerMethodField(read_only=True)
    stud_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Attendance
        fields = ['stud_pp', 'stud_name', 'stud_id', 'stat', 'att_date']

    def get_stud_pp(self, obj):
        try:
            return obj.student.profile_pic.url
        except:
            return static('noprofile.png')

    def get_stud_name(self, obj):
        return obj.student.user.first_name + ' ' + obj.student.user.last_name
    
    def get_stud_id(self, obj):
        return obj.student.stud_id

class AttendaceStudentSerializers(serializers.ModelSerializer):
    stud_pp = serializers.SerializerMethodField(read_only=True)
    stud_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Student
        fields = ['stud_pp', 'stud_name', 'stud_id']
    
    def get_stud_pp(self, obj):
        try:
            return obj.profile_pic.url
        except:
            return static('noprofile.png')

    def get_stud_name(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name


class StudentParentSerializer(serializers.ModelSerializer):
    stud_name = serializers.SerializerMethodField(read_only=True)
    stud_pp = serializers.SerializerMethodField(read_only=True)
    stud_grade = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StudentParent
        fields = ['stud_name', 'stud_pp', 'stud_grade', 'id']

    def get_id(self, obj):
        return str(obj.id)

    def get_stud_name(self, obj):
        return obj.student.user.first_name + ' ' + (obj.student.user.last_name).split(' ')[-1]
    
    def get_stud_pp(self, obj):
        try:
            return obj.student.profile_pic.url
        except:
            return static('noprofile.png')
    
    def get_stud_grade(self, obj):
        return str(obj.student.grade.all()[0].grade.grade_num) + obj.student.grade.all()[0].grade.section


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        name = self.user.first_name

        if len(self.user.student.all()) > 0:
            stat = 'student'
        elif len(self.user.parent.all()) > 0:
            stat = 'parent'
        elif len(self.user.teacher.all()) > 0:
            stat = 'teacher'
        else:
            stat = 'unknown'
            name = self.user.username

        data.update({'stat': stat, 'name': name})
        # and everything else you want to send in the response
        return data


class StudentShortSerializer(serializers.ModelSerializer):
    stud_name = serializers.SerializerMethodField(read_only=True)
    stud_id = serializers.SerializerMethodField(read_only=True)
    stud_pp = serializers.SerializerMethodField(read_only=True)
    stud_grade = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StudentParent
        fields = ['stud_name', 'stud_id', 'stud_pp', 'stud_grade']

    def get_stud_name(self, obj):
        return obj.student.user.first_name + ' ' + (obj.student.user.last_name).split(' ')[1]

    def get_stud_id(self, obj):
        return str(obj.student.stud_id)
    
    def get_stud_pp(self, obj):
        try:
            return obj.student.profile_pic.url
        except:
            return static('noprofile.png')
    
    def get_stud_grade(self, obj):
        return str(obj.student.grade.all()[0].grade.grade_num) + obj.student.grade.all()[0].grade.section


class GradeSubjectSerializers(serializers.ModelSerializer):
    sub_name = serializers.SerializerMethodField(read_only=True)
    sub_id = serializers.SerializerMethodField(read_only=True)
    

    class Meta:
        model = GradeSubject
        fields = ['sub_name', 'sub_id']


    def get_sub_name(self, obj):
        return obj.subject.name

    def get_sub_id(self, obj):
        return obj.subject.id


class ResultSerializers(serializers.ModelSerializer):
 
    class Meta:
        model = Result
        fields =  ['description', 'out_of', 'privacy']
    

class ResultStudentSerializers(serializers.ModelSerializer):
    stud_pp = serializers.SerializerMethodField(read_only=True)
    stud_name = serializers.SerializerMethodField(read_only=True)
    stud_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = GradeStudent
        fields = ['stud_pp', 'stud_name', 'stud_id', 'id']
    
    def get_stud_pp(self, obj):
        try:
            return obj.student.profile_pic.url
        except:
            return static('noprofile.png')

    def get_stud_name(self, obj):
        return obj.student.user.first_name + ' ' + obj.student.user.last_name

    def get_stud_id(self, obj):
        return obj.student.stud_id


class MainStudentSerializers(serializers.ModelSerializer):
    stud_pp = serializers.SerializerMethodField(read_only=True)
    stud_name = serializers.SerializerMethodField(read_only=True)
    stud_id = serializers.SerializerMethodField(read_only=True)
    prev_grade = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Student
        fields = ['stud_pp', 'stud_name', 'stud_id', 'id', 'prev_grade']
    
    def get_stud_pp(self, obj):
        try:
            return obj.profile_pic.url
        except:
            return static('noprofile.png')

    def get_stud_name(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name

    def get_stud_id(self, obj):
        return obj.stud_id

    def get_prev_grade(self, obj):
        return obj.previous_score.all()[0].score


class StudentProfileSerializers(serializers.ModelSerializer):
    stud_pp = serializers.SerializerMethodField(read_only=True)
    stud_name = serializers.SerializerMethodField(read_only=True)
    prev_grade = serializers.SerializerMethodField(read_only=True)
    stud_grade = serializers.SerializerMethodField(read_only=True)
    parent = serializers.SerializerMethodField(read_only=True)
    parent_id = serializers.SerializerMethodField(read_only=True)
    homeroom_t = serializers.SerializerMethodField(read_only=True)
    homeroom_t_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Student
        fields = ['stud_pp', 'stud_name', 'stud_id', 'id', 'prev_grade', 'stud_grade', 'phone', 'parent', 'parent_id', 'homeroom_t', 'homeroom_t_id']
    
    def get_stud_pp(self, obj):
        try:
            return obj.profile_pic.url
        except:
            return static('noprofile.png')

    def get_stud_grade(self, obj):
        try:
            yr = AccadamicYear.objects.filter(status="Active")[0]
            return str(obj.grade.filter(grade__acc_yr=yr)[0].grade.grade_num) + ' ' + obj.grade.filter(grade__acc_yr=yr)[0].grade.section 
        except:
            return ''

    def get_stud_name(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name
    
    def get_parent(self, obj):
        try:
            return obj.parent.all()[0].parent.user.first_name + ' ' + obj.parent.all()[0].parent.user.last_name
        except:
            return 'NOT SET'

    def get_parent_id(self, obj):
        try:
            return obj.parent.all()[0].parent.id
        except:
            return None
    
    def get_homeroom_t(self, obj):
        try:
            yr = AccadamicYear.objects.filter(status="Active")[0]
            return obj.grade.filter(grade__acc_yr=yr)[0].grade.home_room.all()[0].teacher.user.first_name + ' ' + obj.grade.filter(grade__acc_yr=yr)[0].grade.home_room.all()[0].teacher.user.last_name
        except:
            return 'NOT SET'

    def get_homeroom_t_id(self, obj):
        try:
            yr = AccadamicYear.objects.filter(status="Active")[0]
            return obj.grade.filter(grade__acc_yr=yr)[0].grade.home_room.all()[0].teacher.id
        except:
            return None

    def get_prev_grade(self, obj):
        return obj.previous_score.all()[0].score


class HomeworkSerializers(serializers.ModelSerializer):
    stud_name = serializers.SerializerMethodField(read_only=True)
    grade = serializers.SerializerMethodField(read_only=True)
    d_file = serializers.SerializerMethodField(read_only=True)
    due_date = serializers.SerializerMethodField(read_only=True)
    created = serializers.SerializerMethodField(read_only=True)
    subject = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Homework
        fields = ['id', 'title', 'description', 'created', 'due_date', 'd_file', 'for_who', 'grade', 'stud_name', 'subject']
    
    def get_due_date(self, obj):
        return obj.due_date.strftime("%b %d")
    
    def get_created(self, obj):
        return obj.created.strftime("%b %d")

    def get_grade(self, obj):
        return str(obj.gr_sub.grade.grade_num) + obj.gr_sub.grade.section

    def get_stud_name(self, obj):
        try:
            return obj.student.user.first_name + ' ' + obj.student.user.last_name
        except:
            return "None"

    def get_d_file(self, obj):
        try:
            return obj.desc_file.url
        except:
            return "None" 
    
    def get_subject(self, obj):
        return obj.gr_sub.subject.name


class FinalScoreSerializer(serializers.ModelSerializer):
    stud_id = serializers.SerializerMethodField(read_only=True)
    stud_pp = serializers.SerializerMethodField(read_only=True)
    stud_name = serializers.SerializerMethodField(read_only=True)
    gr_stud_id = serializers.SerializerMethodField(read_only=True)
    first_per = serializers.SerializerMethodField(read_only=True)
    second_per = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FinalScore
        fields = ['stud_id', 'stud_name', 'stud_pp', 'first_desc', 'first_per', 'second_per', 'first_50', 'second_desc', 'second_50', 'third_desc', 'third_50', 'forth_desc', 'forth_50', 'gr_stud_id']

    def get_stud_id(self, obj):
        return obj.gr_stud.student.stud_id
    
    def get_first_per(self, obj):
        all_res = FinalScore.objects.filter(subject=obj.subject, gr_stud__grade=obj.gr_stud.grade)
        print(all_res)
        count = 0
        if obj.first_50 != None and obj.second_50 != None:
            for i in all_res:
                if i.first_50 + i.second_50 <= obj.first_50 + obj.second_50:
                    count+=1
        elif obj.first_50 != None:
            for i in all_res:
                if i.first_50 <= obj.first_50:
                    count+=1
        else:
            return '-'

        perc_val = (count/len(all_res)) * 100

        return str(round(perc_val))
    
    def get_second_per(self, obj):
        all_res = FinalScore.objects.filter(subject=obj.subject, gr_stud__grade=obj.gr_stud.grade)
        print(all_res)
        count = 0
        if obj.third_50 != None and obj.forth_50 != None:
            for i in all_res:
                if i.third_50 + i.forth_50 <= obj.third_50 + obj.forth_50:
                    count+=1
        elif obj.third_50 != None:
            for i in all_res:
                if i.third_50 <= obj.third_50:
                    count+=1
        else:
            return '-'

        perc_val = (count/len(all_res)) * 100

        return str(round(perc_val))

    def get_gr_stud_id(self, obj):
        return obj.gr_stud.id
    
    def get_stud_pp(self, obj):
        try:
            return obj.gr_stud.student.profile_pic.url
        except:
            return static('noprofile.png')
        
    
    def get_stud_name(self, obj):
        return obj.gr_stud.student.user.first_name + ' ' + obj.gr_stud.student.user.last_name


class FinalScoreHRSerializer(serializers.ModelSerializer):
    sub_name = serializers.SerializerMethodField(read_only=True)
    first_100 = serializers.SerializerMethodField(read_only=True)
    second_100 = serializers.SerializerMethodField(read_only=True)
    avg = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FinalScore
        fields = ['sub_name', 'first_100', 'second_100', 'avg']

    def get_sub_name(self, obj):
        return obj.subject.name
    
    def get_first_100(self, obj):
        if obj.first_50 != None and obj.second_50 != None:
            return obj.first_50 + obj.second_50
        else:
            return None
    
    def get_second_100(self, obj):
        if obj.third_50 != None and obj.forth_50 != None:
            return obj.third_50 + obj.forth_50
        else:
            return None
    
    def get_avg(self, obj):
        if obj.third_50 != None and obj.forth_50 != None:
            return (obj.third_50 + obj.forth_50 + obj.third_50 + obj.forth_50) / 2
        else:
            return None


class TeacherCourseSerializer(serializers.ModelSerializer):
    module_no = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'overview', 'module_no']
    
    def get_module_no(self, obj):
        return obj.modules.all().count()


class TeacherCourseModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Module
        fields = ['id', 'title', 'description']


class AllResultSerializer(serializers.ModelSerializer):
    out_of = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    perc = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StudentResult
        fields = ['id', 'name', 'out_of', 'score', 'perc']
    
    def get_out_of(self, obj):
        return obj.result.out_of

    def get_name(self, obj):
        return obj.result.description

    def get_perc(self, obj):
        all_results = StudentResult.objects.filter(result=obj.result)
        count = 0
        for i in all_results:
            if i.score <= obj.score:
                count+=1
        perc_val = (count/len(all_results)) * 100
        return round(perc_val)


class StudentScheduleTimesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScheduleTimes
        fields = ['start', 'end']
    

class StudentClassScheduleSerializer(serializers.ModelSerializer):
    start = serializers.SerializerMethodField(read_only=True)
    end = serializers.SerializerMethodField(read_only=True)
    subject_name = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = ClassSchedule
        fields = ['start', 'end', 'subject_name', 'sc_day', 'rest']    
    
    def get_start(self, obj):
        return obj.schedule_time.start
    
    def get_end(self, obj):
        return obj.schedule_time.end
    
    def get_subject_name(self, obj):
        if obj.subject != None:
            return obj.subject.name
        else:
            return 'Break'


class SchoolPaymentSerializer(serializers.ModelSerializer):
    start = serializers.SerializerMethodField(read_only=True)
    end = serializers.SerializerMethodField(read_only=True)
    title = serializers.SerializerMethodField(read_only=True)
    desc = serializers.SerializerMethodField(read_only=True)
    paid_on = serializers.SerializerMethodField(read_only=True)
    paid = serializers.SerializerMethodField(read_only=True)
    stat = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = SPGradeAssociation
        fields = ['start', 'end', 'title', 'desc', 'paid', 'amount', 'paid_on', 'stat']    
    
    def get_start(self, obj):
        return obj.sp.payment_starts.strftime('%b %d')
    
    def get_end(self, obj):
        return obj.sp.payment_ends.strftime('%b %d')
    
    def get_title(self, obj):
        return obj.sp.title
    
    def get_desc(self, obj):
        return obj.sp.description
    
    def get_paid(self, obj):
        request = self.context.get('request', None)
        print(request)
        if request:
            print('sfs')
            usr = request.user
            print(usr)
            if obj.sp.paid.all().filter(stud=usr.student.all()[0]).count() > 0:
                return 'yes'
            else:
                return 'no'
        return 'no'

    def get_paid_on(self, obj):
        request = self.context.get('request', None)
        if request:
            usr = request.user
            if obj.sp.paid.all().filter(stud=usr.student.all()[0]).count() > 0:
                return obj.sp.paid.all().filter(stud=usr.student.all()[0])[0].paid_on.strftime('%b %d')
            else:
                return None
        return None
    
    def get_stat(self, obj):
        today = date.today()
        if obj.sp.payment_starts > today:
            return 'ny'
        elif obj.sp.payment_starts <= today and obj.sp.payment_ends >= today:
            return 'on'
        else:
            return 'p'
    

class StudentExamSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField(read_only=True)
    taken = serializers.SerializerMethodField(read_only=True)
    ques_no = serializers.SerializerMethodField(read_only=True)
    time = serializers.SerializerMethodField(read_only=True)
    created = serializers.SerializerMethodField(read_only=True)
    desc = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = ExamGradeAssociation
        fields = ['title', 'taken', 'ques_no', 'time', 'created', 'id', 'desc']    
    
    def get_title(self, obj):
        return obj.exam.title
    
    def get_taken(self, obj):
        request = self.context.get('request', None)
        usr = request.user
        if obj.exam.taken.all().filter(user=usr).count() > 0:
            return 'yes'
        return 'no'
    
    def get_ques_no(self, obj):
        return obj.exam.exam_questions.all().count()
    
    def get_time(self, obj):
        return obj.exam.time
    
    def get_created(self, obj):
        return obj.exam.created

    def get_desc(self, obj):
        return obj.exam.description

class StudentExamQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExamQuestion
        fields = ['question', 'choice_a', 'choice_b', 'choice_c', 'choice_d', 'answer', 'id']    
    
    