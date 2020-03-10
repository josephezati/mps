from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.utils.translation import gettext as _
from django import forms
import datetime

def current_year():
	return datetime.date.today().year

def max_value_current_year(value):
	return MaxValueValidator(current_year())(value)

class Gender(models.Model):
	name = models.CharField( unique=True, max_length=200)
	def __str__(self):
		return self.name

class Classe(models.Model):
	name = models.CharField( unique=True, max_length=200)
	def __str__(self):
		return self.name

class Subject(models.Model):
	name = models.CharField( unique=True, max_length=200)
	code = models.CharField( unique=True, max_length=200)
	subject_class = models.ManyToManyField(Classe,)
	short_form = models.CharField( max_length=6)
	def __str__(self):
		return self.name

class Stream(models.Model):
	name = models.CharField( unique=True, max_length=200)
	def __str__(self):
		return self.name

class Region(models.Model):
	reg_name = models.CharField(unique=True, max_length=45, verbose_name="Region")
	def __str__(self):
		return self.reg_name

class StaffStatus(models.Model):
	name = models.CharField(unique=True, max_length=45, verbose_name="Status")
	def __str__(self):
		return self.name

class StaffCategory(models.Model):
	name = models.CharField(unique=True, max_length=45, verbose_name="Category")
	def __str__(self):
		return self.name

class Position(models.Model):
	name = models.CharField(max_length=45, verbose_name="Position")
	category = models.ForeignKey(StaffCategory, on_delete = models.SET_NULL, blank=True, null=True, verbose_name="Category")
	def __str__(self):
		return self.name

class District(models.Model):
	dis_name = models.CharField(unique=True, max_length=45, verbose_name="District Name")
	region = models.ForeignKey(Region, on_delete = models.SET_NULL, blank=True, null=True, verbose_name="Region")
	def __str__(self):
		return self.dis_name

class SocialSkill(models.Model):
	name = models.CharField(unique=True, max_length=45, verbose_name="Skill Name")
	def __str__(self):
		return self.name

class Sport(models.Model):
	name = models.CharField(unique=True, max_length=45, verbose_name="Sport Name")
	def __str__(self):
		return self.name

class Membership(models.Model):
	name = models.CharField(unique=True, max_length=45,)
	def __str__(self):
		return self.name

class Hygiene(models.Model):
	level = models.CharField(unique=True, max_length=45,)
	def __str__(self):
		return self.level

class Reading(models.Model):
	level = models.CharField(unique=True, max_length=45,)
	def __str__(self):
		return self.level

class Participation(models.Model):
	level = models.CharField(unique=True, max_length=45,)
	def __str__(self):
		return self.level

class Smartness(models.Model):
	level = models.CharField(unique=True, max_length=45,)
	def __str__(self):
		return self.level

class Leadership(models.Model):
	level = models.CharField(unique=True, max_length=45,)
	def __str__(self):
		return self.level

class IncomeSource(models.Model):
	source = models.CharField(unique=True, max_length=45,)
	def __str__(self):
		return self.source

class ExpenseItem(models.Model):
	item = models.CharField(unique=True, max_length=45,)
	def __str__(self):
		return self.item

class BillItem(models.Model):
	item = models.CharField(unique=True, max_length=45,)
	def __str__(self):
		return self.item

class SchoolItem(models.Model):
	item = models.CharField(unique=True, max_length=45,)
	def __str__(self):
		return self.item

class Country(models.Model):
	name = models.CharField(unique=True, max_length=45,)
	def __str__(self):
		return self.name

class Religion(models.Model):
	name = models.CharField(unique=True, max_length=45,)
	def __str__(self):
		return self.name

class ChildStatus(models.Model):
	name = models.CharField(unique=True, max_length=45,)
	def __str__(self):
		return self.name

class DisciplinaryCategory(models.Model):
	name = models.CharField(unique=True, max_length=45,)
	def __str__(self):
		return self.name

class Scale(models.Model):
	name = models.CharField(unique=True, max_length=45,)
	def __str__(self):
		return self.name

class SubjectTeacherRole(models.Model):
	name = models.CharField(unique=True, max_length=45,)
	def __str__(self):
		return self.name

class ClassTeacherRole(models.Model):
	name = models.CharField(unique=True, max_length=45,)
	def __str__(self):
		return self.name

class Term(models.Model):
	name = models.CharField(unique=True, max_length=45,)
	def __str__(self):
		return self.name

class UnitMeasure(models.Model):
	name = models.CharField(unique=True, max_length=45,)
	def __str__(self):
		return self.name

class Student(models.Model):
	name = models.CharField(max_length=200, verbose_name='Child Name')
	photo = models.ImageField(default='child_photos/default.png', upload_to='child_photos', blank=True, null=True,)
	date_created = models.DateTimeField(default=timezone.now)
	date_of_birth = models.DateField(default=timezone.now)
	updated = models.DateTimeField(auto_now=True)
	gender = models.ForeignKey(Gender, blank=True, null=True, on_delete=models.SET_NULL)
	religion = models.ForeignKey(Religion, blank=True, null=True, on_delete=models.SET_NULL)
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
	def __str__(self):
		return self.name

class ClassInformation (models.Model):
	year_of_registration = models.IntegerField(validators=[MinValueValidator(2012), max_value_current_year])
	date_created = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now=True)
	current_class = models.ForeignKey(Classe, default=1, on_delete=models.CASCADE)
	stream = models.ForeignKey(Stream, default=1, blank=True, null=True, on_delete=models.SET_NULL)
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
	child = models.ForeignKey(Student, on_delete=models.CASCADE)
	def __str__(self):
		return f'{self.current_class} {self.stream} {self.year_of_registration}'

class Staff(models.Model):
	name = models.CharField(max_length=200, verbose_name="Full Name")
	nin = models.CharField(max_length=200, verbose_name="NIN", unique=True)
	email = models.EmailField(blank=True, null=True)
	address = models.CharField(max_length=200,)
	phone = models.CharField(max_length=200,)
	status = models.ForeignKey(StaffStatus, default=1, on_delete = models.SET_DEFAULT, verbose_name="Staff Status")
	gender = models.ForeignKey(Gender, on_delete = models.SET_NULL, blank=True, null=True,)
	dob = models.DateField(blank=True, null=True, verbose_name="Date of Birth")
	district = models.ForeignKey(District, on_delete = models.SET_NULL, blank=True, null=True,)
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	nationality = models.ForeignKey(Country, on_delete = models.SET_NULL, blank=True, null=True,)
	photo = models.ImageField(default='staff_photos/default.png', upload_to='staff_photos')
			
	def __str__(self):
		return self.name

class Designation(models.Model):
	staff = models.ForeignKey(Staff, on_delete = models.CASCADE,)
	position = models.ForeignKey(Position, on_delete = models.CASCADE,)
	scale = models.ForeignKey(Scale, on_delete = models.SET_NULL, blank=True, null=True,)
	date_appointed = models.DateField(default=timezone.now)
	date_created = models.DateTimeField(default=timezone.now)
	appointment_letter = models.FileField(blank=True, null=True)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	def __str__(self):
		return f'{self.staff} {self.position}'

class AcademicInformation (models.Model):
	qualification = models.CharField(max_length=200,)
	institution = models.CharField(max_length=200,)
	year = models.IntegerField(validators=[MinValueValidator(1900), max_value_current_year])
	staff = models.ForeignKey(Staff, on_delete = models.CASCADE,)
	date_created = models.DateTimeField(default=timezone.now)
	document = models.FileField(blank=True, null=True)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	def __str__(self):
		return f'{self.qualification} {self.institution}'

class Parent(models.Model):
	name = models.CharField(max_length=200, verbose_name="Full Name")
	nin = models.CharField(max_length=200, verbose_name="NIN", unique=True)
	relation = models.CharField(max_length=200,)
	email = models.EmailField(blank=True, null=True)
	address = models.CharField(max_length=200,)
	phone = models.CharField(max_length=200,)
	occupation = models.CharField(max_length=200,blank=True, null=True)
	gender = models.ForeignKey(Gender, on_delete = models.SET_NULL, blank=True, null=True,)
	district = models.ForeignKey(District, on_delete = models.SET_NULL, blank=True, null=True,)
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	photo = models.ImageField(default='staff_photos/default.png', upload_to='staff_photos')
	child = models.ForeignKey(Student, on_delete = models.CASCADE,)
			
	def __str__(self):
		return self.name

class HealthInformation(models.Model):
	sickness = models.CharField(max_length=200,)
	hospital_admitted = models.CharField(max_length=200, blank=True, null=True,)
	medication_given = models.CharField(max_length=200, blank=True, null=True,)
	admission_duration = models.IntegerField(blank=True, null=True,)
	date_started = models.DateField(default=timezone.now)
	date_admitted = models.DateField(default=timezone.now, blank=True, null=True,)
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	child = models.ForeignKey(Student, on_delete = models.CASCADE,)
			
	def __str__(self):
		return self.name

class ClassRoomReport(models.Model):
	social_skills = models.ManyToManyField(SocialSkill,)
	sports = models.ManyToManyField(Sport,)
	hygiene_level = models.ForeignKey(Hygiene, on_delete = models.SET_NULL, blank=True, null=True,)
	reading_level = models.ForeignKey(Reading, on_delete = models.SET_NULL, blank=True, null=True,)
	participation_level = models.ForeignKey(Participation, on_delete = models.SET_NULL, blank=True, null=True,)
	leadership_kills = models.ForeignKey(Leadership, on_delete = models.SET_NULL, blank=True, null=True,)
	smartness_level = models.ForeignKey(Smartness, on_delete = models.SET_NULL, blank=True, null=True,)
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	child = models.ForeignKey(Student, on_delete = models.CASCADE,)
			
	def __str__(self):
		return f'{self.child} on {self.date_created}'

class NextOfKin(models.Model):
	name = models.CharField(max_length=200, verbose_name="Full Name")
	email = models.EmailField(blank=True, null=True)
	relation = models.CharField(max_length=200,)
	address = models.CharField(max_length=200,)
	phone = models.CharField(max_length=200,)
	occupation = models.CharField(max_length=200,blank=True, null=True)
	gender = models.ForeignKey(Gender, on_delete = models.SET_NULL, blank=True, null=True,)
	district = models.ForeignKey(District, on_delete = models.SET_NULL, blank=True, null=True,)
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	photo = models.ImageField(default='nextofkin_photos/default.png', upload_to='nextofkin_photos')
	staff = models.ForeignKey(Staff, on_delete = models.CASCADE,)
			
	def __str__(self):
		return self.name

class TeacherSubject(models.Model):
	subject = models.ForeignKey(Subject, on_delete = models.CASCADE,)
	subject_class = models.ForeignKey(Classe, on_delete = models.CASCADE,)
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	staff = models.ForeignKey(Staff, on_delete = models.CASCADE,)
	term = models.ForeignKey(Term, on_delete = models.CASCADE,)
	stream = models.ForeignKey(Stream, on_delete = models.CASCADE,)
	role = models.ForeignKey(SubjectTeacherRole, models.SET_NULL, blank=True, null=True,)
	year = models.IntegerField(validators=[MinValueValidator(2012), max_value_current_year])
			
	def __str__(self):
		return f'{self.subject} {self.subject_class} {self.stream}'

	class Meta():
		unique_together=['subject','subject_class','term','stream','year']


class ClassTeacher(models.Model):
	teacher_class = models.ForeignKey(Classe, on_delete = models.CASCADE,)
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	staff = models.ForeignKey(Staff, on_delete = models.CASCADE,)
	stream = models.ForeignKey(Stream, on_delete = models.CASCADE,)
	role = models.ForeignKey(SubjectTeacherRole, models.SET_NULL, blank=True, null=True,)
	year_from = models.IntegerField(validators=[MinValueValidator(2012), max_value_current_year])
	year_to = models.IntegerField(validators=[MinValueValidator(2012), max_value_current_year])
			
	def __str__(self):
		return f'{self.staff} {self.teacher_class}'

class Leave(models.Model):
	reason = models.CharField(max_length=200,)
	date_created = models.DateTimeField(default=timezone.now)
	date_from = models.DateTimeField(default=timezone.now)
	date_to = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	staff = models.ForeignKey(Staff, on_delete = models.CASCADE,)
			
	def __str__(self):
		return f'{self.staff} {self.reason}'

class TrackRecord(models.Model):
	action = models.CharField(max_length=200,)
	comment = models.TextField()
	date = models.DateTimeField(default=timezone.now)
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	staff = models.ForeignKey(Staff, on_delete = models.CASCADE,)
			
	def __str__(self):
		return f'{self.staff} {self.action}'

class Meeting(models.Model):
	topic = models.CharField(max_length=200,)
	comment = models.TextField()
	minutes = models.FileField(blank=True, null=True, upload_to='minutes',)
	agenda = models.FileField(blank=True, null=True, upload_to='agenda',)
	date = models.DateTimeField(default=timezone.now)
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	membership = models.ForeignKey(Membership, on_delete = models.SET_NULL, blank=True, null=True,)
			
	def __str__(self):
		return self.topic

class Income(models.Model):
	amount = models.IntegerField()
	date = models.DateField(default=timezone.now)
	received_from = models.CharField(max_length=200,)
	comment = models.TextField()
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	uploads = models.FileField(blank=True, null=True, upload_to='income_docs',)
	source = models.ForeignKey(IncomeSource, on_delete = models.CASCADE)
			
	def __str__(self):
		return f'{self.source} {self.amount}'

class Expense(models.Model):
	unit_cost = models.IntegerField()
	total_cost = models.IntegerField()
	unit_measure = models.ForeignKey(UnitMeasure, default=1, on_delete = models.SET_DEFAULT,)
	quantity = models.IntegerField()
	comment = models.TextField()
	date = models.DateField(default=timezone.now)
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	item = models.ForeignKey(ExpenseItem, on_delete = models.CASCADE)
	uploads = models.FileField(blank=True, null=True, upload_to='expense_docs',)
			
	def __str__(self):
		return f'{self.item} {self.quantity} {self.unit_measure}'

class Bill(models.Model):
	unit_cost = models.IntegerField()
	total_cost = models.IntegerField()
	unit_measure = models.ForeignKey(UnitMeasure, default=1, on_delete = models.SET_DEFAULT,)
	quantity = models.IntegerField()
	comment = models.TextField()
	date = models.DateField(default=timezone.now)
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	item = models.ForeignKey(BillItem, on_delete = models.CASCADE)
	uploads = models.FileField(blank=True, null=True, upload_to='expense_docs',)
			
	def __str__(self):
		return f'{self.item} {self.quantity} {self.unit_measure}'

class UseItem(models.Model):
	quantity_used = models.IntegerField()
	comment = models.TextField()
	received_by = models.CharField(max_length=200,)
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	item = models.ForeignKey(Expense, on_delete = models.CASCADE)
	date = models.DateField(default=timezone.now)
	uploads = models.FileField(blank=True, null=True, upload_to='expense_docs',)
			
	def __str__(self):
		return f'{self.item} {self.quantity_used}'

class SchoolRequirement(models.Model):
	quantity = models.IntegerField()
	unit_measure = models.CharField(max_length=200,)
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	item = models.ForeignKey(SchoolItem, on_delete = models.CASCADE)
	child = models.ForeignKey(Student, on_delete = models.CASCADE,)
			
	def __str__(self):
		return f'{self.quantity} {self.unit_measure} of {self.item}'

class GatePass(models.Model):
	duration = models.IntegerField(verbose_name="Duration in Days")
	reason = models.CharField(max_length=200,)
	picked_by = models.CharField(max_length=200,)
	authorized_by = models.CharField(max_length=200,)
	date_created = models.DateTimeField(default=timezone.now)
	return_date = models.DateField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	child = models.ForeignKey(Student, on_delete = models.CASCADE,)
			
	def __str__(self):
		return f'{self.child} for {self.reason}'

class DisciplinaryRecord(models.Model):
	comment = models.TextField(max_length=200,)
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	child = models.ForeignKey(Student, on_delete = models.CASCADE,)
	category = models.ForeignKey(DisciplinaryCategory, on_delete = models.CASCADE,)
			
	def __str__(self):
		return f'{self.child} {self.category}'

class ExamSet(models.Model):
	name = models.CharField(max_length=200,)
	set_class = models.ManyToManyField(Classe,)	
	short_form = models.CharField(max_length=5, blank=True, null=True,)	
	def __str__(self):
		return self.name

class Grade(models.Model):
	name = models.CharField(max_length=200,)
	value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)])
	def __str__(self):
		return self.name

class Mark(models.Model):
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	child = models.ForeignKey(Student, on_delete = models.CASCADE,)
	subject = models.ForeignKey(Subject, on_delete = models.CASCADE,)
	marks_class = models.ForeignKey(Classe, on_delete = models.CASCADE,)
	stream = models.ForeignKey(Stream, on_delete = models.CASCADE,)
	term = models.ForeignKey(Term, on_delete = models.CASCADE,)
	exam_set = models.ForeignKey(ExamSet, on_delete = models.CASCADE,)
	grade = models.ForeignKey(Grade, on_delete = models.SET_NULL, blank=True, null=True,)
	year = models.IntegerField(default=current_year, validators=[MinValueValidator(2020), max_value_current_year])
	marks = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
			
	def __str__(self):
		return f'{self.child} {self.subject} {self.year} {self.term} {self.marks}'
	class Meta():
		unique_together=['child','subject','term','exam_set','year','marks_class']

class Remark(models.Model):
	remark = models.CharField(max_length=100)
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	child = models.ForeignKey(Student, on_delete = models.CASCADE,)
	stream = models.ForeignKey(Stream, on_delete = models.CASCADE,)
	term = models.ForeignKey(Term, on_delete = models.CASCADE,)
	marks_class = models.ForeignKey(Classe, on_delete = models.CASCADE,)
	year = models.IntegerField(default=current_year, validators=[MinValueValidator(2020), max_value_current_year])
			
	def __str__(self):
		return f'{self.child} {self.marks_class} {self.year} {self.term} {self.remark}'
	class Meta():
		unique_together=['child','term','year','marks_class']

class ClassTeacherRemark(models.Model):
	remark = models.CharField(max_length=100)
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	child = models.ForeignKey(Student, on_delete = models.CASCADE,)
	stream = models.ForeignKey(Stream, on_delete = models.CASCADE,)
	term = models.ForeignKey(Term, on_delete = models.CASCADE,)
	marks_class = models.ForeignKey(Classe, on_delete = models.CASCADE,)
	year = models.IntegerField(default=current_year, validators=[MinValueValidator(2020), max_value_current_year])
			
	def __str__(self):
		return f'{self.child} {self.marks_class} {self.year} {self.term} {self.remark}'
	class Meta():
		unique_together=['child','term','year','marks_class']

class SubjectTeacherRemark(models.Model):
	subject = models.ForeignKey(Subject, on_delete = models.CASCADE,)
	remark = models.CharField(max_length=100)
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	child = models.ForeignKey(Student, on_delete = models.CASCADE,)
	stream = models.ForeignKey(Stream, on_delete = models.CASCADE,)
	term = models.ForeignKey(Term, on_delete = models.CASCADE,)
	marks_class = models.ForeignKey(Classe, on_delete = models.CASCADE,)
	year = models.IntegerField(default=current_year, validators=[MinValueValidator(2020), max_value_current_year])
			
	def __str__(self):
		return f'{self.child} {self.subject} {self.marks_class} {self.year} {self.term} {self.remark}'
	class Meta():
		unique_together=['child','term','year','marks_class','subject']

class Attendance(models.Model):
	name = models.CharField(max_length=200,)
	def __str__(self):
		return self.name

class TrackAttendance(models.Model):
	attendance = models.ForeignKey(Attendance, default=1, on_delete=models.SET_DEFAULT)
	date_created = models.DateTimeField(default=timezone.now)
	date = models.DateField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	child = models.ForeignKey(Student, on_delete = models.CASCADE,)
	stream = models.ForeignKey(Stream, on_delete = models.CASCADE,)
	term = models.ForeignKey(Term, on_delete = models.CASCADE,)
	marks_class = models.ForeignKey(Classe, on_delete = models.CASCADE,)
	year = models.IntegerField(default=current_year, validators=[MinValueValidator(2020), max_value_current_year])
			
	def __str__(self):
		return f'{self.child} {self.marks_class} {self.date} {self.attendance}'
	class Meta():
		unique_together=['child','term','year','marks_class','date']

class Choose(models.Model):
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	child = models.ForeignKey(Student, on_delete = models.CASCADE,)
	subject = models.ForeignKey(TeacherSubject, on_delete = models.CASCADE,)
	marks_class = models.ForeignKey(Classe, on_delete = models.CASCADE, verbose_name="Class")
	stream = models.ForeignKey(Stream, on_delete = models.CASCADE,)
	term = models.ForeignKey(Term, on_delete = models.CASCADE,)
	exam_set = models.ForeignKey(ExamSet, on_delete = models.CASCADE,)
	year = models.IntegerField(default=current_year, validators=[MinValueValidator(2020), max_value_current_year])
	marks = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
			
	def __str__(self):
		return f'{self.child} {self.subject} {self.year} {self.marks}'

class Fees(models.Model):
	date_created = models.DateTimeField(default=timezone.now)
	date = models.DateField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	child = models.ForeignKey(Student, on_delete = models.CASCADE,)
	fees_class = models.ForeignKey(Classe, on_delete = models.CASCADE,)
	term = models.ForeignKey(Term, on_delete = models.CASCADE,)
	year = models.IntegerField(default=current_year, validators=[MinValueValidator(2020), max_value_current_year])
	amount = models.IntegerField(validators=[MinValueValidator(500)])
	uploads = models.FileField(blank=True, null=True, upload_to='fees_docs',)
			
	def __str__(self):
		return f'{self.child} {self.amount}'

class SetFees(models.Model):
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	fees_class = models.ForeignKey(Classe, on_delete = models.CASCADE,)
	term = models.ForeignKey(Term, on_delete = models.CASCADE,)
	year = models.IntegerField(default=current_year, validators=[MinValueValidator(2020), max_value_current_year])
	amount = models.IntegerField(validators=[MinValueValidator(500)])
			
	def __str__(self):
		return f'{self.fees_class} {self.term} {self.year}'

class BookStatus(models.Model):
	name = models.CharField(max_length=200,)	
	def __str__(self):
		return self.name

class Book(models.Model):
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	auther = models.CharField(max_length=200)
	title = models.CharField(max_length=200)
	number = models.CharField(max_length=200, unique=True)
	uploads = models.FileField(blank=True, null=True, upload_to='book_uploads',)
			
	def __str__(self):
		return f'{self.number} {self.title}'

class LendBookStaff(models.Model):
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	book = models.ForeignKey(Book, on_delete = models.CASCADE,)
	staff = models.ForeignKey(Staff, on_delete = models.CASCADE,)
	date_borrowed = models.DateTimeField(default=timezone.now)
	return_date = models.DateTimeField(default=timezone.now)
	status = models.ForeignKey(BookStatus, default=1, on_delete = models.SET_DEFAULT,)
			
	def __str__(self):
		return f'{self.staff} {self.book}'



class LendBookChild(models.Model):
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True,)
	book = models.ForeignKey(Book, on_delete = models.CASCADE,)
	child = models.ForeignKey(Student, on_delete = models.CASCADE,)
	date_borrowed = models.DateTimeField(default=timezone.now)
	return_date = models.DateTimeField(default=timezone.now)
	status = models.ForeignKey(BookStatus, default=1, on_delete = models.SET_DEFAULT,)
			
	def __str__(self):
		return f'{self.child} {self.book}'

class MessageStatus(models.Model):
	status = models.CharField(max_length=200)
			
	def __str__(self):
		return self.status

class Message(models.Model):
	subject = models.CharField(max_length=200)
	date_created = models.DateTimeField(default=timezone.now)
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
	status = models.ForeignKey(MessageStatus, on_delete=models.SET_DEFAULT, default=1,)
	receiver = models.ManyToManyField(User, related_name='receiver')
	message_body = models.TextField(blank=True, null=True,)
	uploads = models.FileField(blank=True, null=True, upload_to='email_uploads')
			
	def __str__(self):
		return f'{self.sender}, {self.subject}'

class Reply(models.Model):
	date_created = models.DateTimeField(default=timezone.now)
	replyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replyer')
	message = models.ForeignKey(Message, on_delete=models.CASCADE, )
	reply_body = models.TextField(blank=True, null=True,)
	uploads = models.FileField(blank=True, null=True, upload_to='email_uploads')
			
	def __str__(self):
		return f'{self.sender}, {self.message}'
