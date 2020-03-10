from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from users.models import *
from django.forms import formset_factory

def current_year():
    return datetime.date.today().year

def year_choices():
	return [(r,r) for r in range(2020, datetime.date.today().year+1)]

class StudentCreateForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = ('name','gender','date_of_birth','religion','photo')

class ClassInformationCreateForm(forms.ModelForm):
	year_of_registration = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year)
	class Meta:
		model = ClassInformation
		fields = ('year_of_registration','current_class','stream',)

class StaffCreateForm(forms.ModelForm):
	class Meta:
		model = Staff
		fields = ('name','nin','gender','dob','nationality','district','address','email','phone','status','photo')

class ParentCreateForm(forms.ModelForm):
	class Meta:
		model = Parent
		fields = ('name','nin','gender','occupation','relation','district','address','email','phone','photo')

class HealthInformationCreateForm(forms.ModelForm):
	class Meta:
		model = HealthInformation
		fields = ('sickness','date_started','date_admitted','hospital_admitted','medication_given','admission_duration',)

class ClassroomReportCreateForm(forms.ModelForm):
	class Meta:
		model = ClassRoomReport
		fields = ('social_skills','sports','hygiene_level','reading_level','participation_level','leadership_kills','smartness_level',)

class NextofkinCreateForm(forms.ModelForm):
	class Meta:
		model = NextOfKin
		fields = ('name','gender','occupation','relation','district','address','email','phone','photo')

class TeacherSubjectCreateForm(forms.ModelForm):
	year = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year)
	class Meta:
		model = TeacherSubject
		fields = ('subject','subject_class','stream','term','year','role',)

class ClassTeacherCreateForm(forms.ModelForm):
	year_from = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year)
	year_to = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year)
	class Meta:
		model = ClassTeacher
		fields = ('teacher_class','stream','year_from','year_to','role',)

class DesignationCreateForm(forms.ModelForm):
	class Meta:
		model = Designation
		fields = ('position','date_appointed','scale','appointment_letter',)

class AcademicInformationCreateForm(forms.ModelForm):
	year = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year)
	class Meta:
		model = AcademicInformation
		fields = ('qualification','institution','year','document',)

class LeaveCreateForm(forms.ModelForm):
	class Meta:
		model = Leave
		fields = ('reason','date_from','date_to',)

class TrackRecordCreateForm(forms.ModelForm):
	class Meta:
		model = TrackRecord
		fields = ('action','date','comment',)

class MeetingCreateForm(forms.ModelForm):
	class Meta:
		model = Meeting
		fields = ('topic','membership','agenda','date','comment',)

class MeetingUpdateForm(forms.ModelForm):
	class Meta:
		model = Meeting
		fields = ('topic','membership','agenda','minutes','date','comment',)
		

class IncomeCreateForm(forms.ModelForm):
	class Meta:
		model = Income
		fields = ('source','received_from','amount','date','uploads','comment',)

class ExpenseCreateForm(forms.ModelForm):
	class Meta:
		model = Expense
		fields = ('item','quantity','unit_cost','unit_measure','date','uploads','comment',)

class BillCreateForm(forms.ModelForm):
	class Meta:
		model = Bill
		fields = ('item','quantity','unit_cost','unit_measure','date','uploads','comment',)

class UseItemCreateForm(forms.ModelForm):
	class Meta:
		model = UseItem
		fields = ('quantity_used','received_by','date','uploads','comment',)

class SchoolRequirementCreateForm(forms.ModelForm):
	class Meta:
		model = SchoolRequirement
		fields = ('item','quantity','unit_measure',)

class GatePassCreateForm(forms.ModelForm):
	class Meta:
		model = GatePass
		fields = ('reason','duration','return_date','picked_by','authorized_by',)

class DisciplinaryRecordCreateForm(forms.ModelForm):
	class Meta:
		model = DisciplinaryRecord
		fields = ('category','comment',)

class ChooseForm(forms.ModelForm):
	year = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year)
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		super(ChooseForm,self).__init__(*args,**kwargs)
		if user is not None:
			self.fields['subject'].queryset = TeacherSubject.objects.filter(staff=user.userprofile.staff).order_by('-id')
	class Meta:
		model = Choose
		fields = ('subject','year','term','exam_set',)

class ChooseRevForm(forms.ModelForm):
	year = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year)
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		super(ChooseRevForm,self).__init__(*args,**kwargs)
		if user is not None:
			self.fields['subject'].queryset = TeacherSubject.objects.filter(staff=user.userprofile.staff).order_by('-id')
	class Meta:
		model = Choose
		fields = ('subject','year','term',)

class ChooseReportCardForm(forms.ModelForm):
	year = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year)
	class Meta:
		model = Choose
		fields = ('marks_class','stream','year','term',)

class ChooseClassReviewForm(forms.ModelForm):
	year = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year)
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		super(ChooseClassReviewForm,self).__init__(*args,**kwargs)
		if user is not None:
			self.fields['marks_class'].queryset = ClassTeacher.objects.filter(staff=user.userprofile.staff).order_by('-id')
	class Meta:
		model = Choose
		fields = ('marks_class','stream','year','term',)

class MarkCreateForm(forms.ModelForm):
	class Meta:
		model = Mark
		fields = ('child','marks',)

class AttendanceCreateForm(forms.ModelForm):
	class Meta:
		model = TrackAttendance
		fields = ('child','attendance',)


class RemarkCreateForm(forms.ModelForm):
	class Meta:
		model = Remark
		fields = ('child','remark',)

class SubjectTeacherRemarkCreateForm(forms.ModelForm):
	class Meta:
		model = SubjectTeacherRemark
		fields = ('child','remark',)

class ClassTeacherRemarkCreateForm(forms.ModelForm):
	class Meta:
		model = ClassTeacherRemark
		fields = ('child','remark',)

class FeesCreateForm(forms.ModelForm):
	year = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year)
	class Meta:
		model = Fees
		fields = ('fees_class','term','year','amount','date','uploads',)

class SetFeesCreateForm(forms.ModelForm):
	year = forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year)
	class Meta:
		model = SetFees
		fields = ('fees_class','term','year','amount',)

class BookCreateForm(forms.ModelForm):
	class Meta:
		model = Book
		fields = ('number','auther','title','uploads',)

class LendBookChildCreateForm(forms.ModelForm):
	class Meta:
		model = LendBookChild
		fields = ('book','date_borrowed','return_date',)

class LendBookStaffCreateForm(forms.ModelForm):
	class Meta:
		model = LendBookStaff
		fields = ('book','date_borrowed','return_date',)

class ReturnBookChildCreateForm(forms.ModelForm):
	class Meta:
		model = LendBookChild
		fields = ('status',)

class ReturnBookStaffCreateForm(forms.ModelForm):
	class Meta:
		model = LendBookStaff
		fields = ('status',)

class MessageCreateForm(forms.ModelForm):
	class Meta:
		model = Message
		fields = ('receiver','subject','message_body','uploads',)

class ReplyCreateForm(forms.ModelForm):
	class Meta:
		model = Reply
		fields = ('reply_body','uploads',)

class StreamCreateForm(forms.ModelForm):
	class Meta:
		model = Stream
		fields = ('name',)

class ClassCreateForm(forms.ModelForm):
	class Meta:
		model = Classe
		fields = ('name',)

class SubjectCreateForm(forms.ModelForm):
	class Meta:
		model = Subject
		fields = ('code','name','subject_class','short_form')

class RegionCreateForm(forms.ModelForm):
	class Meta:
		model = Region
		fields = ('reg_name',)

class StaffStatusCreateForm(forms.ModelForm):
	class Meta:
		model = StaffStatus
		fields = ('name',)

class StaffCategoryCreateForm(forms.ModelForm):
	class Meta:
		model = StaffCategory
		fields = ('name',)

class PositionCreateForm(forms.ModelForm):
	class Meta:
		model = Position
		fields = ('name','category')

class DistrictCreateForm(forms.ModelForm):
	class Meta:
		model = District
		fields = ('dis_name','region')

class SocialSkillCreateForm(forms.ModelForm):
	class Meta:
		model = SocialSkill
		fields = ('name',)

class SportCreateForm(forms.ModelForm):
	class Meta:
		model = Sport
		fields = ('name',)

class MembershipCreateForm(forms.ModelForm):
	class Meta:
		model = Membership
		fields = ('name',)

class HygieneCreateForm(forms.ModelForm):
	class Meta:
		model = Hygiene
		fields = ('level',)

class ReadingCreateForm(forms.ModelForm):
	class Meta:
		model = Reading
		fields = ('level',)

class ParticipationCreateForm(forms.ModelForm):
	class Meta:
		model = Participation
		fields = ('level',)

class SmartnessCreateForm(forms.ModelForm):
	class Meta:
		model = Smartness
		fields = ('level',)

class LeadershipCreateForm(forms.ModelForm):
	class Meta:
		model = Leadership
		fields = ('level',)

class IncomeSourceCreateForm(forms.ModelForm):
	class Meta:
		model = IncomeSource
		fields = ('source',)

class ExpenseItemCreateForm(forms.ModelForm):
	class Meta:
		model = ExpenseItem
		fields = ('item',)

class BillItemCreateForm(forms.ModelForm):
	class Meta:
		model = BillItem
		fields = ('item',)

class SchoolItemCreateForm(forms.ModelForm):
	class Meta:
		model = SchoolItem
		fields = ('item',)

class CountryCreateForm(forms.ModelForm):
	class Meta:
		model = Country
		fields = ('name',)

class ReligionCreateForm(forms.ModelForm):
	class Meta:
		model = Religion
		fields = ('name',)

class ChildStatusCreateForm(forms.ModelForm):
	class Meta:
		model = ChildStatus
		fields = ('name',)

class DisciplinaryCategoryCreateForm(forms.ModelForm):
	class Meta:
		model = DisciplinaryCategory
		fields = ('name',)

class ScaleCreateForm(forms.ModelForm):
	class Meta:
		model = Scale
		fields = ('name',)

class SubjectTeacherRoleCreateForm(forms.ModelForm):
	class Meta:
		model = SubjectTeacherRole
		fields = ('name',)

class ClassTeacherRoleCreateForm(forms.ModelForm):
	class Meta:
		model = ClassTeacherRole
		fields = ('name',)

class TermCreateForm(forms.ModelForm):
	class Meta:
		model = Term
		fields = ('name',)

class UnitMeasureCreateForm(forms.ModelForm):
	class Meta:
		model = UnitMeasure
		fields = ('name',)

class ExamSetCreateForm(forms.ModelForm):
	class Meta:
		model = ExamSet
		fields = ('name','set_class','short_form',)

class GradeCreateForm(forms.ModelForm):
	class Meta:
		model = Grade
		fields = ('name','value',)