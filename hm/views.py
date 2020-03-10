from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.db.models import  Q, Count, IntegerField, OuterRef, Subquery, Max
from django.db import transaction
from django.views.generic import (
	ListView,
	DetailView,
	UpdateView,
	CreateView
	)
from django.forms.models import modelformset_factory
import datetime
from datetime import timedelta
from django.utils import timezone
from .models import*
from users.models import*
from .forms import*
from django.db import IntegrityError
from django.db.models import Sum
from django.utils.safestring import mark_safe
import calendar
from calendar import monthrange
from . import calendar
from .calendar import*
import xml.etree.ElementTree as etree
from .utils import Calendar
from django.urls import reverse

class StudentCreateView(LoginRequiredMixin, CreateView):
	form_class = StudentCreateForm
	model = Student

	def get_context_data(self, **kwargs):
		context = super(StudentCreateView, self).get_context_data(**kwargs)
		children = Student.objects.filter(user=self.request.user).order_by('-id')
		context["children"] = children
		context["title"] = "Children"
		context["submenu"] = "Add Child"
		return context

	def form_valid(self, form):
		form = StudentCreateForm(self.request.POST, self.request.FILES)
		if form.is_valid():
			form.instance.user = self.request.user
			try:
				form.save()
				name = form.cleaned_data.get('name')
				messages.success(self.request, f'Thank you! You have added {name}')
			except IntegrityError:
				messages.warning(self.request, f'Error! May be cantact the admin ')
			return redirect('new-student')

class StudentUpdateView(LoginRequiredMixin, UpdateView):
	form_class = StudentCreateForm
	model = Student

	def get_context_data(self, **kwargs):
		context = super(StudentUpdateView, self).get_context_data(**kwargs)
		children = Student.objects.filter(user=self.request.user).order_by('-id')
		context["children"] = children
		context["title"] = "Children"
		context["submenu"] = "Add Child"
		return context

	def form_valid(self, form):
		student = Student.objects.get(pk=self.object.id)
		form = StudentCreateForm(self.request.POST, self.request.FILES, instance=student)
		if form.is_valid():
			form.instance.user = self.request.user
			try:
				form.save()
				name = form.cleaned_data.get('name')
				messages.success(self.request, f'Thank you! You have Updated {name}')
			except IntegrityError:
				messages.warning(self.request, f'Error! May be cantact the admin ')
			return redirect('new-student')

class StudentListView(LoginRequiredMixin, ListView):
	model = Student

	def get_context_data(self, **kwargs):
		context = super(StudentListView, self).get_context_data(**kwargs)
		children = Student.objects.all().order_by('-id')
		classes = ClassInformation.objects.values('child').annotate(current=Max('id'))
		context["children"] = children
		context["title"] = "Children"
		context["classes"] = classes
		context["submenu"] = "View Children"
		return context

def students(request):
	students = Student.objects.all()
	classes = ClassInformation.objects.values('child').annotate(current=Max('id'))
	class_list = Classe.objects.all()

	context = {
	'title':'Children',
	'submenu':'View Children',
	'head':'All',
	'children':students,
	'classes':classes,
	'class_list':class_list,
	}
	return render(request, 'hm/student_list.html', context)

def selected_students(request):
	year = request.GET.get('year', None)
	the_class = request.GET.get('the_class', None)
	clas = Classe.objects.get(pk=the_class)
	if year and clas:
		students = Student.objects.filter(classinformation__current_class=the_class, classinformation__year_of_registration=year,)
	elif clas:
		students = Student.objects.filter(classinformation__current_class=the_class,)
	elif year:
		students = Student.objects.filter(classinformation__year_of_registration=year,)
	else:
		students = Student.objects.all()
	classes = ClassInformation.objects.values('child').annotate(current=Max('id'))
	class_list = Classe.objects.all()
	context = {
	'title':'Children',
	'submenu':'View Children',
	'children':students,
	'classes':classes,
	'class_list':class_list,
	'the_class':clas,
	'year':year
	}
	return render(request, 'hm/student_list.html', context)




class StaffCreateView(LoginRequiredMixin, CreateView):
	form_class = StaffCreateForm
	model = Staff

	def get_context_data(self, **kwargs):
		context = super(StaffCreateView, self).get_context_data(**kwargs)
		staffs = Staff.objects.filter(user=self.request.user).order_by('-id')
		context["staffs"] = staffs
		context["title"] = "Staff"
		context["submenu"] = "Add Staff"
		return context

	def form_valid(self, form):
		form = StaffCreateForm(self.request.POST, self.request.FILES)
		if form.is_valid():
			form.instance.user = self.request.user
			try:
				form.save()
				name = form.cleaned_data.get('name')
				messages.success(self.request, f'Thank you! You have added {name}')
			except IntegrityError:
				messages.warning(self.request, f'Error! May be cantact the admin ')
			return redirect('new-staff')

class StaffUpdateView(LoginRequiredMixin, UpdateView):
	form_class = StaffCreateForm
	model = Staff

	def get_context_data(self, **kwargs):
		context = super(StaffUpdateView, self).get_context_data(**kwargs)
		staffs = Staff.objects.filter(user=self.request.user).order_by('-id')
		context["staffs"] = staffs
		context["title"] = "Staff"
		context["submenu"] = "Add Staff"
		return context

	def form_valid(self, form):
		staff = Staff.objects.get(pk=self.object.id)
		form = StaffCreateForm(self.request.POST, self.request.FILES, instance=staff)
		if form.is_valid():
			form.instance.user = self.request.user
			try:
				form.save()
				name = form.cleaned_data.get('name')
				messages.success(self.request, f'Thank you! You have Updated {name}')
			except IntegrityError:
				messages.warning(self.request, f'Error! May be cantact the admin ')
			return redirect('new-staff')

class StaffListView(LoginRequiredMixin, ListView):
	model = Staff

	def get_context_data(self, **kwargs):
		context = super(StaffListView, self).get_context_data(**kwargs)
		staffs = Staff.objects.all().order_by('-id')
		context["staffs"] = staffs
		context["title"] = "Staff"
		context["submenu"] = "View Staff"
		return context

class TeachingStaff(LoginRequiredMixin, ListView):
	model = Staff

	def get_context_data(self, **kwargs):
		context = super(TeachingStaff, self).get_context_data(**kwargs)
		staffs = Staff.objects.filter(position__category=1)
		context["staffs"] = staffs
		context["title"] = "Staff"
		context["submenu"] = "Teaching Staff"
		context["head"] = "Teaching Staff"
		return context

class NonTeachingStaff(LoginRequiredMixin, ListView):
	model = Staff

	def get_context_data(self, **kwargs):
		context = super(NonTeachingStaff, self).get_context_data(**kwargs)
		staffs = Staff.objects.filter(position__category=2).order_by('-id')
		context["staffs"] = staffs
		context["title"] = "Staff"
		context["submenu"] = "Non Teaching Staff"
		context["head"] = "Non Teaching Staff"
		return context
@login_required
def staff(request, pk):
	staff=Staff.objects.get(pk=pk)
	# Add next of kin
	if request.method == 'POST':
		nextofkin_form = NextofkinCreateForm(request.POST, request.FILES)
		if nextofkin_form.is_valid():
			nextofkin_form.instance.user = request.user
			nextofkin_form.instance.staff = staff
			nextofkin_form.save(commit=False)
			try:
				nextofkin_form.save()
				messages.success(request, f'You have added Next of kin {staff}!')
				return HttpResponseRedirect(reverse('staff-details', kwargs={'pk':staff.id}))
			except Exception:
				messages.warning(request, f'Error! May be Contact admin')
				
	else:
		nextofkin_form = NextofkinCreateForm()

	# Add Teacher Subject
	if request.method == 'POST':
		teachersubject_form = TeacherSubjectCreateForm(request.POST, request.FILES)
		if teachersubject_form.is_valid():
			teachersubject_form.instance.user = request.user
			teachersubject_form.instance.staff = staff
			teachersubject_form.save(commit=False)
			try:
				teachersubject_form.save()
				messages.success(request, f'You have added a subject for {staff}!')
				return HttpResponseRedirect(reverse('staff-details', kwargs={'pk':staff.id}))
			except Exception:
				messages.warning(request, f'Error! Check Your form Again!')
				
	else:
		teachersubject_form = TeacherSubjectCreateForm()

	# Add Track Record
	if request.method == 'POST':
		trackrecord_form = TrackRecordCreateForm(request.POST, request.FILES)
		if trackrecord_form.is_valid():
			trackrecord_form.instance.user = request.user
			trackrecord_form.instance.staff = staff
			trackrecord_form.save(commit=False)
			try:
				trackrecord_form.save()
				messages.success(request, f'You have added Track Record for {staff}.')
				return HttpResponseRedirect(reverse('staff-details', kwargs={'pk':staff.id}))
			except Exception:
				messages.warning(request, f'Error! May be Contact admin')
				
	else:
		trackrecord_form = TrackRecordCreateForm()

	# Add Track Record
	if request.method == 'POST':
		academic_form = AcademicInformationCreateForm(request.POST, request.FILES)
		if academic_form.is_valid():
			academic_form.instance.user = request.user
			academic_form.instance.staff = staff
			academic_form.save(commit=False)
			try:
				academic_form.save()
				messages.success(request, f'You have added Academic Information for {staff}.')
				return HttpResponseRedirect(reverse('staff-details', kwargs={'pk':staff.id}))
			except Exception:
				messages.warning(request, f'Error! May be Contact admin')
				
	else:
		academic_form = AcademicInformationCreateForm()

	# Add Desgnat....
	if request.method == 'POST':
		designation_form = DesignationCreateForm(request.POST, request.FILES)
		if designation_form.is_valid():
			designation_form.instance.user = request.user
			designation_form.instance.staff = staff
			designation_form.save(commit=False)
			try:
				designation_form.save()
				messages.success(request, f'You have added Designation for {staff}.')
				return HttpResponseRedirect(reverse('staff-details', kwargs={'pk':staff.id}))
			except Exception:
				messages.warning(request, f'Error! May be Contact admin')
				
	else:
		designation_form = DesignationCreateForm()

	# Add Classes....
	if request.method == 'POST':
		class_form = ClassTeacherCreateForm(request.POST, request.FILES)
		if class_form.is_valid():
			class_form.instance.user = request.user
			class_form.instance.staff = staff
			class_form.save(commit=False)
			try:
				class_form.save()
				messages.success(request, f'You have added a class for {staff}.')
				return HttpResponseRedirect(reverse('staff-details', kwargs={'pk':staff.id}))
			except Exception:
				messages.warning(request, f'Error! May be Contact admin')
				
	else:
		class_form = ClassTeacherCreateForm()

	# Add Leave....
	if request.method == 'POST':
		leave_form = LeaveCreateForm(request.POST, request.FILES)
		if leave_form.is_valid():
			leave_form.instance.user = request.user
			leave_form.instance.staff = staff
			leave_form.save(commit=False)
			try:
				leave_form.save()
				messages.success(request, f'You have added Leave for {staff}.')
				return HttpResponseRedirect(reverse('staff-details', kwargs={'pk':staff.id}))
			except Exception:
				messages.warning(request, f'Error! May be Contact admin')
				
	else:
		leave_form = LeaveCreateForm()

	nextofkins = NextOfKin.objects.filter(staff=staff).order_by('-id')
	academics = AcademicInformation.objects.filter(staff=staff).order_by('-id')
	subjects = TeacherSubject.objects.filter(staff=staff).order_by('-id')
	trackrecords = TrackRecord.objects.filter(staff=staff).order_by('-id')
	designations = Designation.objects.filter(staff=staff).order_by('-id')
	classes = ClassTeacher.objects.filter(staff=staff).order_by('-id')
	leaves = Leave.objects.filter(staff=staff).order_by('-id')
	context = {
	'title': 'Staff', 
	'submenu': 'View Staff',
	'staff': staff,
	'nextofkin_form': nextofkin_form,
	'teachersubject_form': teachersubject_form,
	'trackrecord_form': trackrecord_form,
	'academic_form': academic_form,
	'class_form': class_form,
	'leave_form': leave_form,
	'designation_form': designation_form,
	'nextofkins': nextofkins,
	'subjects': subjects,
	'trackrecords': trackrecords,
	'academics': academics,
	'designations': designations,
	'classes': classes,
	'leaves': leaves,
	}

	return render(request, 'hm/staff_detail.html', context)

def delete_tnext(request, pk, id):
	staff = get_object_or_404(Staff, pk=id)
	try:
		report = get_object_or_404(NextOfKin, pk=pk).delete()
		messages.success(request, f'The Next Of Kin was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('staff-details', kwargs={'pk':staff.id}))

def delete_tsubject(request, pk, id):
	staff = get_object_or_404(Staff, pk=id)
	try:
		report = get_object_or_404(TeacherSubject, pk=pk).delete()
		messages.success(request, f'The Subject was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('staff-details', kwargs={'pk':staff.id}))

def delete_tclass(request, pk, id):
	staff = get_object_or_404(Staff, pk=id)
	try:
		report = get_object_or_404(ClassTeacher, pk=pk).delete()
		messages.success(request, f'The Class was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('staff-details', kwargs={'pk':staff.id}))

def delete_trecord(request, pk, id):
	staff = get_object_or_404(Staff, pk=id)
	try:
		report = get_object_or_404(TrackRecord, pk=pk).delete()
		messages.success(request, f'The Track Record was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('staff-details', kwargs={'pk':staff.id}))

def delete_designation(request, pk, id):
	staff = get_object_or_404(Staff, pk=id)
	try:
		report = get_object_or_404(Designation, pk=pk).delete()
		messages.success(request, f'The Designation was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('staff-details', kwargs={'pk':staff.id}))

def delete_qualification(request, pk, id):
	staff = get_object_or_404(Staff, pk=id)
	try:
		report = get_object_or_404(AcademicInformation, pk=pk).delete()
		messages.success(request, f'The Academic Information was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('staff-details', kwargs={'pk':staff.id}))

def delete_leave(request, pk, id):
	staff = get_object_or_404(Staff, pk=id)
	try:
		report = get_object_or_404(Leave, pk=pk).delete()
		messages.success(request, f'The Leave Record was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('staff-details', kwargs={'pk':staff.id}))

@login_required
def child(request, pk):
	child=Student.objects.get(pk=pk)
	current_class=ClassInformation.objects.filter(child=pk).last()
	# Add PARENT
	if request.method == 'POST':
		parent_form = ParentCreateForm(request.POST, request.FILES)
		if parent_form.is_valid():
			parent_form.instance.user = request.user
			parent_form.instance.child = child
			parent_form.save(commit=False)
			try:
				parent_form.save()
				messages.success(request, f'You have added Parent Information of {child}!')
				return HttpResponseRedirect(reverse('child-details', kwargs={'pk':child.id}))
			except Exception:
				messages.warning(request, f'Error! May be Contact admin')
				
	else:
		parent_form = ParentCreateForm()

	# Add Health Information
	if request.method == 'POST':
		health_form = HealthInformationCreateForm(request.POST, request.FILES)
		if health_form.is_valid():
			health_form.instance.user = request.user
			health_form.instance.child = child
			health_form.save(commit=False)
			try:
				health_form.save()
				messages.success(request, f'You have added Health Information of {child}!')
				return HttpResponseRedirect(reverse('child-details', kwargs={'pk':child.id}))
			except Exception:
				messages.warning(request, f'Error! May be Contact admin')
				
	else:
		health_form = HealthInformationCreateForm()

	# Add Appointment
	if request.method == 'POST':
		report_form = ClassroomReportCreateForm(request.POST, request.FILES)
		if report_form.is_valid():
			report_form.instance.user = request.user
			report_form.instance.child = child
			report_form.save(commit=False)
			try:
				report_form.save()
				messages.success(request, f'You have added class room report for  {child}.')
				return HttpResponseRedirect(reverse('child-details', kwargs={'pk':child.id}))
			except Exception:
				messages.warning(request, f'Error! May be Contact admin')
				
	else:
		report_form = ClassroomReportCreateForm()

	# Add Classes
	if request.method == 'POST':
		class_form = ClassInformationCreateForm(request.POST, request.FILES)
		if class_form.is_valid():
			class_form.instance.user = request.user
			class_form.instance.child = child
			class_form.save(commit=False)
			try:
				class_form.save()
				messages.success(request, f'You have added Class Information for {child}.')
				return HttpResponseRedirect(reverse('child-details', kwargs={'pk':child.id}))
			except Exception:
				messages.warning(request, f'Error! May be Contact admin')
				
	else:
		class_form = ClassInformationCreateForm()

	# Add Requirement
	if request.method == 'POST':
		requirement_form = SchoolRequirementCreateForm(request.POST, request.FILES)
		if requirement_form.is_valid():
			requirement_form.instance.user = request.user
			requirement_form.instance.child = child
			requirement_form.save(commit=False)
			try:
				requirement_form.save()
				messages.success(request, f'You have added a Requirement for {child}.')
				return HttpResponseRedirect(reverse('child-details', kwargs={'pk':child.id}))
			except Exception:
				messages.warning(request, f'Error! May be Contact admin')
				
	else:
		requirement_form = SchoolRequirementCreateForm()

	# Add Requirement
	if request.method == 'POST':
		gatepass_form = GatePassCreateForm(request.POST, request.FILES)
		if gatepass_form.is_valid():
			gatepass_form.instance.user = request.user
			gatepass_form.instance.child = child
			gatepass_form.save(commit=False)
			try:
				gatepass_form.save()
				messages.success(request, f'You recorded a gate pass for {child}.')
				return HttpResponseRedirect(reverse('child-details', kwargs={'pk':child.id}))
			except Exception:
				messages.warning(request, f'Error! May be Contact admin')
	else:
		gatepass_form = GatePassCreateForm()

	# Add Disciplinary
	if request.method == 'POST':
		disciplinary_form = DisciplinaryRecordCreateForm(request.POST, request.FILES)
		if disciplinary_form.is_valid():
			disciplinary_form.instance.user = request.user
			disciplinary_form.instance.child = child
			disciplinary_form.save(commit=False)
			try:
				disciplinary_form.save()
				messages.success(request, f'You recorded a Disciplinary action for {child}.')
				return HttpResponseRedirect(reverse('child-details', kwargs={'pk':child.id}))
			except Exception:
				messages.warning(request, f'Error! May be Contact admin')
	else:
		disciplinary_form = DisciplinaryRecordCreateForm()

	parents = Parent.objects.filter(child=child).order_by('-id')
	classes = ClassInformation.objects.filter(child=child).order_by('-id')
	health_infos = HealthInformation.objects.filter(child=child).order_by('-id')
	reports = ClassRoomReport.objects.filter(child=child).order_by('-id')
	requirements = SchoolRequirement.objects.filter(child=child).order_by('-id')
	gate_passes = GatePass.objects.filter(child=child).order_by('-id')
	disciplines = DisciplinaryRecord.objects.filter(child=child).order_by('-id')
	fees = Fees.objects.filter(child=child).values('fees_class','term','year').annotate(samount=Sum('amount'))
	all_fees = Fees.objects.filter(child=child)
	fees_structure = SetFees.objects.all()
	context = {
	'title': 'Children', 
	'submenu': 'View Children',
	'child': child,
	'parent_form': parent_form,
	'disciplinary_form': disciplinary_form,
	'health_form': health_form,
	'report_form': report_form,
	'class_form': class_form,
	'gatepass_form': gatepass_form,
	'requirement_form': requirement_form,
	'gate_passes': gate_passes,
	'classes': classes,
	'disciplines': disciplines,
	'requirements': requirements,
	'reports': reports,
	'parents': parents,
	'health_infos': health_infos,
	'current_class': current_class,
	'fees': fees,
	'all_fees': all_fees,
	'fees_structure': fees_structure,
	}

	return render(request, 'hm/student_detail.html', context)

def delete_parent(request, pk, id):
	child = get_object_or_404(Student, pk=id)
	try:
		parent = get_object_or_404(Parent, pk=pk).delete()
		messages.success(request, f'The parent was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('child-details', kwargs={'pk':child.id}))

def delete_health(request, pk, id):
	child = get_object_or_404(Student, pk=id)
	try:
		health = get_object_or_404(HealthInformation, pk=pk).delete()
		messages.success(request, f'The Health Information was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('child-details', kwargs={'pk':child.id}))

def delete_report(request, pk, id):
	child = get_object_or_404(Student, pk=id)
	try:
		report = get_object_or_404(ClassRoomReport, pk=pk).delete()
		messages.success(request, f'The General report was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('child-details', kwargs={'pk':child.id}))

def delete_class(request, pk, id):
	child = get_object_or_404(Student, pk=id)
	try:
		report = get_object_or_404(ClassInformation, pk=pk).delete()
		messages.success(request, f'The Class Information was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('child-details', kwargs={'pk':child.id}))

def delete_requirement(request, pk, id):
	child = get_object_or_404(Student, pk=id)
	try:
		report = get_object_or_404(SchoolRequirement, pk=pk).delete()
		messages.success(request, f'The School Requirement was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('child-details', kwargs={'pk':child.id}))

def delete_gatepass(request, pk, id):
	child = get_object_or_404(Student, pk=id)
	try:
		report = get_object_or_404(GatePass, pk=pk).delete()
		messages.success(request, f'The Gate Pass was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('child-details', kwargs={'pk':child.id}))

def delete_discipline(request, pk, id):
	child = get_object_or_404(Student, pk=id)
	try:
		report = get_object_or_404(DisciplinaryRecord, pk=pk).delete()
		messages.success(request, f'The Disciplinary Record was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('child-details', kwargs={'pk':child.id}))

class MeetingCreateView(LoginRequiredMixin, CreateView):
	form_class = MeetingCreateForm
	model = Meeting

	def get_context_data(self, **kwargs):
		context = super(MeetingCreateView, self).get_context_data(**kwargs)
		meetings = Meeting.objects.filter(Q(date__gt=datetime.datetime.now())).order_by('date')
		context["meetings"] = meetings
		prv_meetings = Meeting.objects.filter(Q(date__lt=datetime.datetime.now())).order_by('date')
		context["prv_meetings"] = prv_meetings
		context["title"] = "Home"
		context["submenu"] = "Meetings"
		return context

	def form_valid(self, form):
		form = MeetingCreateForm(self.request.POST, self.request.FILES)
		if form.is_valid():
			form.instance.user = self.request.user
			try:
				form.save()
				name = form.cleaned_data.get('topic')
				messages.success(self.request, f'Thank you! You have scheduled a meeting for {name}')
			except IntegrityError:
				messages.warning(self.request, f'Error! May be cantact the admin ')
			return redirect('meeting')

class MeetingUpdateView(LoginRequiredMixin, UpdateView):
	form_class = MeetingUpdateForm
	model = Meeting

	def get_context_data(self, **kwargs):
		context = super(MeetingUpdateView, self).get_context_data(**kwargs)
		meetings = Meeting.objects.filter(Q(date__gt=datetime.datetime.now())).order_by('date')
		context["meetings"] = meetings
		prv_meetings = Meeting.objects.filter(Q(date__lt=datetime.datetime.now())).order_by('date')
		context["prv_meetings"] = prv_meetings
		context["title"] = "Home"
		context["submenu"] = "Meetings"
		return context

	def form_valid(self, form):
		meeting = Meeting.objects.get(pk=self.object.id)
		form = MeetingUpdateForm(self.request.POST, self.request.FILES, instance=meeting)
		if form.is_valid():
			try:
				form.save()
				name = form.cleaned_data.get('topic')
				messages.success(self.request, f'Thank you! You have Updated meeting for {name}')
			except IntegrityError:
				messages.warning(self.request, f'Error! May be cantact the admin ')
			return redirect('meeting')

class MeetingListView(LoginRequiredMixin, ListView):
	model = Meeting

	def get_context_data(self, **kwargs):
		context = super(MeetingListView, self).get_context_data(**kwargs)
		meetings = Meeting.objects.filter(Q(date__gt=datetime.datetime.now())).order_by('date')
		context["meetings"] = meetings
		prv_meetings = Meeting.objects.filter(Q(date__lt=datetime.datetime.now())).order_by('date')
		context["prv_meetings"] = prv_meetings
		context["title"] = "Home"
		context["submenu"] = "Meetings"
		return context

class ClassTeacherListView(LoginRequiredMixin, ListView):
	model = ClassTeacher

	def get_context_data(self, **kwargs):
		context = super(ClassTeacherListView, self).get_context_data(**kwargs)
		class_teachers = ClassTeacher.objects.all().order_by('-id')
		context["title"] = "Staff"
		context["submenu"] = "Class Teachers"
		context["class_teachers"] = class_teachers
		return context

class SubjectTeacherListView(LoginRequiredMixin, ListView):
	model = TeacherSubject

	def get_context_data(self, **kwargs):
		context = super(SubjectTeacherListView, self).get_context_data(**kwargs)
		subject_teachers = TeacherSubject.objects.all().order_by('-id')
		context["title"] = "Staff"
		context["submenu"] = "Subject Teachers"
		context["subject_teachers"] = subject_teachers
		return context

class ContractListView(LoginRequiredMixin, ListView):
	model = Designation

	def get_context_data(self, **kwargs):
		context = super(ContractListView, self).get_context_data(**kwargs)
		contracts = Designation.objects.all().order_by('-id')
		context["title"] = "Staff"
		context["submenu"] = "Contracts"
		context["contracts"] = contracts
		return context

class LeaveListView(LoginRequiredMixin, ListView):
	model = Leave

	def get_context_data(self, **kwargs):
		context = super(LeaveListView, self).get_context_data(**kwargs)
		leaves = Leave.objects.all().order_by('-id')
		context["title"] = "Staff"
		context["submenu"] = "Leaves"
		context["leaves"] = leaves
		return context

# class AppraisalListView(LoginRequiredMixin, ListView):
# 	model = Appraisal

# 	def get_context_data(self, **kwargs):
# 		context = super(AppraisalListView, self).get_context_data(**kwargs)
# 		appraisals = Appraisal.objects.all().order_by('-id')
# 		context["title"] = "Staff"
# 		context["submenu"] = "Appraisals"
# 		context["subject_teachers"] = "contracts"
# 		return context

class TrackRecordListView(LoginRequiredMixin, ListView):
	model = TrackRecord

	def get_context_data(self, **kwargs):
		context = super(TrackRecordListView, self).get_context_data(**kwargs)
		records = TrackRecord.objects.all().order_by('-id')
		context["title"] = "Staff"
		context["submenu"] = "Track Records"
		context["records"] = records
		return context

@login_required
def meeting(request, pk):
	meeting =Meeting.objects.get(pk=pk)
	context = {
	'title': 'Home',
	'submenu': 'Meetings',
	'meeting': 'meeting',
	}

	return render(request, 'hm/meeting_detail.html', context)

class IncomeCreateView(LoginRequiredMixin, CreateView):
	form_class = IncomeCreateForm
	model = Income

	def get_context_data(self, **kwargs):
		context = super(IncomeCreateView, self).get_context_data(**kwargs)
		incomes = Income.objects.all().order_by('-id')
		context["incomes"] = incomes
		context["title"] = "Finance"
		context["submenu"] = "Incomes"
		return context

	def form_valid(self, form):
		form = IncomeCreateForm(self.request.POST, self.request.FILES)
		if form.is_valid():
			form.instance.user = self.request.user
			try:
				form.save()
				name = form.cleaned_data.get('received_from')
				source = form.cleaned_data.get('source')
				messages.success(self.request, f'Thank you! You have recorded {source} from {name}')
			except IntegrityError:
				messages.warning(self.request, f'Error! May be cantact the admin ')
			return redirect('income')

class IncomeUpdateView(LoginRequiredMixin, UpdateView):
	form_class = IncomeCreateForm
	model = Income

	def get_context_data(self, **kwargs):
		context = super(IncomeUpdateView, self).get_context_data(**kwargs)
		incomes = Income.objects.all().order_by('-id')
		context["incomes"] = incomes
		context["title"] = "Finance"
		context["submenu"] = "Incomes"
		return context

	def form_valid(self, form):
		income = Income.objects.get(pk=self.object.id)
		form = IncomeCreateForm(self.request.POST, self.request.FILES, instance=income)
		if form.is_valid():
			try:
				form.save()
				name = form.cleaned_data.get('received_from')
				source = form.cleaned_data.get('source')
				messages.success(self.request, f'Thank you! You have updated {source} from {name}')
			except IntegrityError:
				messages.warning(self.request, f'Error! May be cantact the admin ')
			return redirect('income')

class IncomeListView(LoginRequiredMixin, ListView):
	model = Income

	def get_context_data(self, **kwargs):
		context = super(IncomeListView, self).get_context_data(**kwargs)
		incomes = Income.objects.all().order_by('-id')
		context["incomes"] = incomes
		context["title"] = "Finance"
		context["submenu"] = "Incomes"
		return context

class ExpenseCreateView(LoginRequiredMixin, CreateView):
	form_class = ExpenseCreateForm
	model = Expense

	def get_context_data(self, **kwargs):
		context = super(ExpenseCreateView, self).get_context_data(**kwargs)
		expenses = Expense.objects.all().order_by('-id')
		context["expenses"] = expenses
		context["title"] = "Store"
		context["submenu"] = "Add New Item"
		return context

	def form_valid(self, form):
		form = ExpenseCreateForm(self.request.POST, self.request.FILES)
		if form.is_valid():
			form.instance.user = self.request.user
			form.save(commit=False)
			quantity = form.cleaned_data.get('quantity')
			unit = form.cleaned_data.get('unit_cost')
			form.instance.total_cost = quantity*unit
			try:
				form.save()
				unit_measure = form.cleaned_data.get('unit_measure')
				item = form.cleaned_data.get('item')
				quantity = form.cleaned_data.get('quantity')
				messages.success(self.request, f'Thank you! You have recorded {quantity} {unit_measure} of {item}')
			except IntegrityError:
				messages.warning(self.request, f'Error! May be cantact the admin ')
			return redirect('expense')

class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
	form_class = ExpenseCreateForm
	model = Expense

	def get_context_data(self, **kwargs):
		context = super(ExpenseUpdateView, self).get_context_data(**kwargs)
		expenses = Expense.objects.all().order_by('-id')
		context["expenses"] = expenses
		context["title"] = "Store"
		context["submenu"] = "Add New Item"
		return context

	def form_valid(self, form):
		expense = Expense.objects.get(pk=self.object.id)
		form = ExpenseCreateForm(self.request.POST, self.request.FILES, instance=expense)
		if form.is_valid():
			form.save(commit=False)
			quantity = form.cleaned_data.get('quantity')
			unit = form.cleaned_data.get('unit_cost')
			form.instance.total_cost = quantity*unit
			try:
				form.save()
				unit_measure = form.cleaned_data.get('unit_measure')
				item = form.cleaned_data.get('item')
				quantity = form.cleaned_data.get('quantity')
				unit = form.cleaned_data.get('unit_cost')
				messages.success(self.request, f'Thank you! You have updated the {quantity} {unit_measure} of {item}')
			except IntegrityError:
				messages.warning(self.request, f'Error! May be cantact the admin ')
			return redirect('expense')

class ExpenseListView(LoginRequiredMixin, ListView):
	model = Expense

	def get_context_data(self, **kwargs):
		context = super(ExpenseListView, self).get_context_data(**kwargs)
		expenses = Expense.objects.all().order_by('-id')
		context["expenses"] = expenses
		context["title"] = "Finance"
		context["submenu"] = "Expenses"
		return context

class BillCreateView(LoginRequiredMixin, CreateView):
	form_class = BillCreateForm
	model = Bill

	def get_context_data(self, **kwargs):
		context = super(BillCreateView, self).get_context_data(**kwargs)
		bills = Bill.objects.all().order_by('-id')
		context["bills"] = bills
		context["title"] = "Expense"
		context["submenu"] = "Add Expense"
		return context

	def form_valid(self, form):
		form = BillCreateForm(self.request.POST, self.request.FILES)
		if form.is_valid():
			form.instance.user = self.request.user
			form.save(commit=False)
			quantity = form.cleaned_data.get('quantity')
			unit = form.cleaned_data.get('unit_cost')
			form.instance.total_cost = quantity*unit
			try:
				form.save()
				unit_measure = form.cleaned_data.get('unit_measure')
				item = form.cleaned_data.get('item')
				quantity = form.cleaned_data.get('quantity')
				messages.success(self.request, f'Thank you! You have recorded {quantity} {unit_measure} of {item}')
			except IntegrityError:
				messages.warning(self.request, f'Error! May be cantact the admin ')
			return redirect('bill')

class BillUpdateView(LoginRequiredMixin, UpdateView):
	form_class = BillCreateForm
	model = Bill

	def get_context_data(self, **kwargs):
		context = super(BillUpdateView, self).get_context_data(**kwargs)
		bills = Bill.objects.all().order_by('-id')
		context["bills"] = bills
		context["title"] = "Expense"
		context["submenu"] = "Add Expense"
		return context

	def form_valid(self, form):
		bill = Bill.objects.get(pk=self.object.id)
		form = BillCreateForm(self.request.POST, self.request.FILES, instance=bill)
		if form.is_valid():
			form.save(commit=False)
			quantity = form.cleaned_data.get('quantity')
			unit = form.cleaned_data.get('unit_cost')
			form.instance.total_cost = quantity*unit
			try:
				form.save()
				unit_measure = form.cleaned_data.get('unit_measure')
				item = form.cleaned_data.get('item')
				quantity = form.cleaned_data.get('quantity')
				unit = form.cleaned_data.get('unit_cost')
				messages.success(self.request, f'Thank you! You have updated the {quantity} {unit_measure} of {item}')
			except IntegrityError:
				messages.warning(self.request, f'Error! May be cantact the admin ')
			return redirect('bill')

class BillListView(LoginRequiredMixin, ListView):
	model = Bill

	def get_context_data(self, **kwargs):
		context = super(BillListView, self).get_context_data(**kwargs)
		bills = Bill.objects.all().order_by('-id')
		context["bills"] = bills
		context["title"] = "Expense"
		context["submenu"] = "Expenses"
		return context

class BookCreateView(LoginRequiredMixin, CreateView):
	form_class = BookCreateForm
	model = Book

	def get_context_data(self, **kwargs):
		context = super(BookCreateView, self).get_context_data(**kwargs)
		books = Book.objects.all().order_by('-id')
		context["books"] = books
		context["title"] = "Library"
		context["submenu"] = "Books"
		return context

	def form_valid(self, form):
		form = BookCreateForm(self.request.POST, self.request.FILES)
		if form.is_valid():
			form.instance.user = self.request.user
			try:
				form.save()
				name = form.cleaned_data.get('title')
				messages.success(self.request, f'Thank you! You have added {name}')
			except IntegrityError:
				messages.warning(self.request, f'Error! May be cantact the admin ')
			return redirect('book')

class BookUpdateView(LoginRequiredMixin, UpdateView):
	form_class = BookCreateForm
	model = Book

	def get_context_data(self, **kwargs):
		context = super(BookUpdateView, self).get_context_data(**kwargs)
		books = Book.objects.all().order_by('-id')
		context["books"] = books
		context["title"] = "Library"
		context["submenu"] = "Books"
		return context

	def form_valid(self, form):
		book = Book.objects.get(pk=self.object.id)
		form = BookCreateForm(self.request.POST, self.request.FILES, instance=book, )
		if form.is_valid():
			form.instance.user = self.request.user
			try:
				form.save()
				name = form.cleaned_data.get('title')
				messages.success(self.request, f'Thank you! You have updated {name}')
			except IntegrityError:
				messages.warning(self.request, f'Error! May be cantact the admin ')
			return redirect('book')

class BookListView(LoginRequiredMixin, ListView):
	model = Book

	def get_context_data(self, **kwargs):
		context = super(BookListView, self).get_context_data(**kwargs)
		books = Book.objects.all().order_by('-id')
		context["books"] = books
		context["title"] = "Library"
		context["submenu"] = "Books"
		return context

@login_required
def book(request, pk):
	book = Book.objects.get(pk=pk)
	child_borrowings = LendBookChild.objects.filter(book=book).order_by('-id')
	staff_borrowings = LendBookStaff.objects.filter(book=book).order_by('-id')
	context = {
	'title': 'Library',
	'submenu': 'Books',
	'book': book,
	'staff_borrowings': staff_borrowings,
	'child_borrowings': child_borrowings,
	}

	return render(request, 'hm/book_detail.html', context)

@login_required
def lend_book(request):
	children = Student.objects.all()
	staffs = Staff.objects.all()
	context = {
	'title': 'Library',
	'submenu': 'Lend Books',
	'staffs': staffs,
	'children': children,
	}

	return render(request, 'hm/lend_book.html', context)

@login_required
def return_book(request):
	children = LendBookChild.objects.filter(status=1).order_by('return_date')
	staffs = LendBookStaff.objects.filter(status=1).order_by('return_date')
	context = {
	'title': 'Library',
	'submenu': 'Return Books',
	'staffs': staffs,
	'children': children,
	}

	return render(request, 'hm/return_book.html', context)

@login_required
def return_book_child(request, pk):
	book = LendBookChild.objects.get(pk=pk)
	if request.method == 'POST':
		form = ReturnBookChildCreateForm(request.POST, request.FILES, instance=book)
		if form.is_valid():
			try:
				form.save()
				messages.success(request, f'The book has been returned successfully.')
				return HttpResponseRedirect(reverse('return-book'))
			except Exception:
				messages.warning(request, f'Error! May be Contact admin')
				
	else:
		form = ReturnBookChildCreateForm()
	context = {
	'title': 'Library',
	'submenu': 'Return Books',
	'book': book,
	'form': form,
	'borrower': 'Child',
	}

	return render(request, 'hm/return_book_child.html', context)

@login_required
def return_book_staff(request, pk):
	book = LendBookStaff.objects.get(pk=pk)
	if request.method == 'POST':
		form = ReturnBookStaffCreateForm(request.POST, request.FILES, instance=book)
		if form.is_valid():
			try:
				form.save()
				messages.success(request, f'The book has been returned successfully.')
				return HttpResponseRedirect(reverse('return-book'))
			except Exception:
				messages.warning(request, f'Error! May be Contact admin')
				
	else:
		form = ReturnBookStaffCreateForm()
	context = {
	'title': 'Library',
	'submenu': 'Return Books',
	'book': book,
	'form': form,
	'borrower': 'Staff',
	}

	return render(request, 'hm/return_book_child.html', context)

@login_required
def lend_book_child(request, pk):
	child = Student.objects.get(pk=pk)
	not_returned = BookStatus.objects.get(pk=1)
	book = None
	child_borrowings = LendBookChild.objects.all().order_by('-id')
	if request.method == 'POST':
		form = LendBookChildCreateForm(request.POST, request.FILES)
		if form.is_valid():
			form.instance.user = request.user
			form.instance.child = child
			form.save(commit=False)
			book = form.cleaned_data.get('book')
			borrowed_book = LendBookChild.objects.filter(book=book, status=not_returned).last()
			borrowed_book_staff = LendBookStaff.objects.filter(book=book, status=not_returned).last()
			if borrowed_book:
				messages.warning(request, f'Sorry the book you are trying to give out is already borrowed by some child.')
			elif borrowed_book_staff:
				messages.warning(request, f'Sorry the book you are trying to give out is already borrowed by some staff.')
			else:
				try:
					form.save()
					messages.success(request, f'You have given out {book} to {child}.')
					return HttpResponseRedirect(reverse('lend-book'))
				except Exception:
					messages.warning(request, f'Error! May be Contact admin')
				
	else:
		form = LendBookChildCreateForm()

	context = {
	'title': 'Library',
	'submenu': 'Lend Books',
	'book': book,
	'form': form,
	'child': child,
	'borrowings': child_borrowings,
	'borrower': 'Children'
	}

	return render(request, 'hm/lendbookchild_form.html', context)

@login_required
def lend_book_staff(request, pk):
	staff = Staff.objects.get(pk=pk)
	not_returned = BookStatus.objects.get(pk=1)
	book = None
	staff_borrowings = LendBookStaff.objects.all().order_by('-id')
	if request.method == 'POST':
		form = LendBookStaffCreateForm(request.POST, request.FILES)
		if form.is_valid():
			form.instance.user = request.user
			form.instance.staff = staff
			form.save(commit=False)
			book = form.cleaned_data.get('book')
			borrowed_book = LendBookChild.objects.filter(book=book, status=not_returned).last()
			borrowed_book_staff = LendBookStaff.objects.filter(book=book, status=not_returned).last()
			if borrowed_book:
				messages.warning(request, f'Sorry the book you are trying to give out is already borrowed by some child.')
			elif borrowed_book_staff:
				messages.warning(request, f'Sorry the book you are trying to give out is already borrowed by some staff.')
			else:
				try:
					form.save()
					messages.success(request, f'You have given out {book} to {staff}.')
					return HttpResponseRedirect(reverse('lend-book'))
				except Exception:
					messages.warning(request, f'Error! May be Contact admin')
				
	else:
		form = LendBookStaffCreateForm()

	context = {
	'title': 'Library',
	'submenu': 'Lend Books',
	'book': book,
	'form': form,
	'staff': staff,
	'borrowings': staff_borrowings,
	'borrower':'Staff'
	}

	return render(request, 'hm/lendbookchild_form.html', context)

@login_required
def available_items(request):
	# items = Expense.objects.all()
	items = Expense.objects.annotate(qty_used=Sum('useitem__quantity_used'))
	context = {
	'title': 'Store',
	'submenu': 'Available Items',
	'items': items,
	}
	return render(request, 'hm/available_items.html', context)

@login_required
def used_items(request):
	items_used = Expense.objects.annotate(qty_used=Sum('useitem__quantity_used'))
	items = UseItem.objects.all()
	context = {
	'title': 'Store',
	'submenu': 'Used Items',
	'items': items,
	}
	return render(request, 'hm/used_items.html', context)

@login_required
def items_summary(request):
	qty_used = ExpenseItem.objects.annotate(qty_used=Sum('expense__useitem__quantity_used')).filter(pk=OuterRef('pk'))
	qty_bought = ExpenseItem.objects.annotate(qty_bought=Sum('expense__quantity')).filter(pk=OuterRef('pk'))
	total_cost = ExpenseItem.objects.annotate(total_cost=Sum('expense__total_cost')).filter(pk=OuterRef('pk'))
	items = ExpenseItem.objects.annotate(qty_bought=Subquery(qty_bought.values('qty_bought'), output_field=IntegerField()), total_cost=Subquery(total_cost.values('total_cost'), output_field=IntegerField()), qty_used=Subquery(qty_used.values('qty_used'), output_field=IntegerField()))
	context = {
	'title': 'Store',
	'submenu': 'Items Summary',
	'items': items,
	}
	return render(request, 'hm/items_summary.html', context)

@login_required
def expense(request, pk):
	expense =Expense.objects.get(pk=pk)
	context = {
	'title': 'Finance',
	'submenu': 'Expenses',
	'expense': expense,
	}

	return render(request, 'hm/expense_detail.html', context)

@login_required
def use_item(request, pk):
	expense =Expense.objects.get(pk=pk)
	expenses_used = UseItem.objects.all()
	if request.method == 'POST':
		use_form = UseItemCreateForm(request.POST, request.FILES)
		if use_form.is_valid():
			use_form.instance.user = request.user
			use_form.instance.item = expense
			use_form.save(commit=False)
			try:
				use_form.save()
				messages.success(request, f'You have recorded use of {expense}.')
				return HttpResponseRedirect(reverse('available-items'))
			except Exception:
				messages.warning(request, f'Error! May be Contact admin')
				
	else:
		use_form = UseItemCreateForm()

	context = {
	'title': 'Finance',
	'submenu': 'Expenses',
	'expense': expense,
	'use_form': use_form,
	'expenses_used': expenses_used,
	}

	return render(request, 'hm/use_item.html', context)
@login_required
def gate_pass(request):
	gate_passes = GatePass.objects.all().order_by('-id')
	context = {
	'title': 'Children',
	'submenu': 'Gate Pass',
	'gate_passes': gate_passes,
	}

	return render(request, 'hm/gate_pass.html', context)
@login_required
def disciplinary_records(request):
	disciplinary_records = DisciplinaryRecord.objects.all().order_by('-id')
	context = {
	'title': 'Children',
	'submenu': 'Disciplinary Records',
	'disciplinary_records': disciplinary_records,
	}

	return render(request, 'hm/disciplinary_records.html', context)
@login_required
def health_records(request):
	health_records = HealthInformation.objects.all().order_by('-id')
	context = {
	'title': 'Children',
	'submenu': 'Health Records',
	'health_records': health_records,
	}

	return render(request, 'hm/health_records.html', context)
@login_required
def parents(request):
	parents = Parent.objects.all().order_by('-id')
	context = {
	'title': 'Children',
	'submenu': 'Parents',
	'parents': parents,
	}

	return render(request, 'hm/parents.html', context)
@login_required
def choose_subject(request):
	user = request.user
	if request.method == 'POST':
		form = ChooseForm(request.POST, user = request.user)
		if form.is_valid():
			form.save(commit=False)
			return redirect('enter-marks')
	else:
		form = ChooseForm(user = request.user)

	subjects = TeacherSubject.objects.filter(staff=request.user.userprofile.staff).order_by('-id')
	context = {
	'title': 'Marks',
	'submenu': 'Enter Marks',
	'subjects': subjects,
	'form': form,
	}

	return render(request, 'hm/choose_subject.html', context)
@login_required
def choose_marks(request):
	user = request.user
	if request.method == 'POST':
		form = ChooseForm(request.POST, user = request.user)
		if form.is_valid():
			form.save(commit=False)
			return redirect('view-marks')
	else:
		form = ChooseForm(user = request.user)

	subjects = TeacherSubject.objects.filter(staff=request.user.userprofile.staff).order_by('-id')
	context = {
	'title': 'Marks',
	'submenu': 'View Marks',
	'subjects': subjects,
	'form': form,
	}

	return render(request, 'hm/choose_marks.html', context)

@login_required
def enter_marks(request):
	if request.method == 'POST':
		select_form = ChooseForm(request.POST, user = request.user)
		if select_form.is_valid():
			select_form.save(commit=False)
			return redirect('enter-marks')
	else:
		select_form = ChooseForm(user = request.user)

	the_subject = None
	the_term = None
	the_exam_set = None

	teacher_subject = request.GET.get('subject', None)
	year = request.GET.get('year', None)
	term = request.GET.get('term', None)
	exam_set = request.GET.get('exam_set', None)
	try:
		the_subject = TeacherSubject.objects.get(id=request.GET.get('subject', None))
		the_term = Term.objects.get(id=request.GET.get('term', None))
		the_exam_set = ExamSet.objects.get(id=request.GET.get('exam_set', None))
	except Exception:
		messages.warning(request, f'Try to make selections Again')

	subject = the_subject.subject
	marks_class = the_subject.subject_class
	stream = the_subject.stream
	term = the_term
	exam_set = the_exam_set
	subjects = TeacherSubject.objects.filter(staff=request.user.userprofile.staff).order_by('-id')
	students = ClassInformation.objects.filter(year_of_registration=year, current_class=marks_class, stream=stream).order_by('child')
	if request.method == 'POST':
		for student in students:
			form = MarkCreateForm(request.POST, )
			if form.is_valid():
				child = form.cleaned_data.get('child')
				marks = form.cleaned_data.get('marks')

				form.instance.subject = subject
				form.instance.marks_class = marks_class
				form.instance.stream = stream
				form.instance.year = year
				form.instance.term = term
				form.instance.exam_set = exam_set
				
				form.instance.user = request.user

				if child == student.child:
					form.instance.child = student.child
					form.instance.marks = marks
					try:
						form.save()
						messages.success(request, f'Marks Submitted Successfully')
						return redirect('choose-subject')
					except:
						messages.warning(request, f'Marks already entered for some students')

				else:
					messages.warning(request, f'Marks not Submitted for {child} {student.child.name} {marks}')


	else:
		form = MarkCreateForm()
	context = {
	'title': 'Marks',
	'submenu': 'Enter Marks',
	'select_form': select_form,
	'subjects': subjects,
	'students': students,
	'subject': subject,
	'subject_class': marks_class,
	'stream': stream,
	'year': year,
	'exam_set': exam_set,
	'term': the_term,
	'form': form,
	}

	return render(request, 'hm/enter_marks.html', context)


@login_required
def view_marks(request):
	if request.method == 'POST':
		select_form = ChooseForm(request.POST, user = request.user)
		if select_form.is_valid():
			select_form.save(commit=False)
			return redirect('view-marks')
	else:
		select_form = ChooseForm(user = request.user)

	the_subject = None
	the_term = None
	the_exam_set = None

	teacher_subject = request.GET.get('subject', None)
	year = request.GET.get('year', None)
	term = request.GET.get('term', None)
	exam_set = request.GET.get('exam_set', None)
	try:
		the_subject = TeacherSubject.objects.get(id=request.GET.get('subject', None))
		the_term = Term.objects.get(id=request.GET.get('term', None))
		the_exam_set = ExamSet.objects.get(id=request.GET.get('exam_set', None))
	except Exception:
		messages.warning(request, f'Try to make selections Again')

	subject = the_subject.subject
	marks_class = the_subject.subject_class
	stream = the_subject.stream
	term = the_term
	exam_set = the_exam_set

	subjects = TeacherSubject.objects.filter(staff=request.user.userprofile.staff).order_by('-id')
	students = ClassInformation.objects.filter(year_of_registration=year, current_class=marks_class, stream=stream).order_by('child')
	marks = Mark.objects.filter(marks_class=marks_class, year=year, exam_set=exam_set, stream=stream, term=term).order_by('-id')
	context = {
	'title': 'Marks',
	'submenu': 'View Marks',
	'select_form': select_form,
	'subjects': subjects,
	'students': students,
	'subject': subject,
	'subject_class': marks_class,
	'stream': stream,
	'year': year,
	'exam_set': exam_set,
	'term': the_term,
	'marks': marks,
	}

	return render(request, 'hm/view_marks.html', context)
@login_required
def choose_report_cards(request):
	user = request.user
	if request.method == 'POST':
		form = ChooseReportCardForm(request.POST)
		if form.is_valid():
			form.save(commit=False)
			return redirect('report-cards')
	else:
		form = ChooseReportCardForm()

	subjects = Subject.objects.all().order_by('-id')
	context = {
	'title': 'Academia',
	'submenu': 'Report Cards',
	'subjects': subjects,
	'form': form,
	}

	return render(request, 'hm/choose_report_cards.html', context)

@login_required
def report_cards(request):

	the_class = None
	the_term = None
	the_stream = None

	card_classs = request.GET.get('marks_class', None)
	year = request.GET.get('year', None)
	term = request.GET.get('term', None)
	stream = request.GET.get('stream', None)
	try:
		the_class = Classe.objects.get(id=request.GET.get('marks_class', None))
		the_term = Term.objects.get(id=request.GET.get('term', None))
		the_stream = Stream.objects.get(id=request.GET.get('stream', None))
	except Exception:
		messages.warning(request, f'Try to make selections Again')

	card_class = the_class
	stream = the_stream
	term = the_term

	subjects = Subject.objects.filter(subject_class__in = card_classs).order_by('id')
	exam_sets = ExamSet.objects.filter(set_class__in = card_classs).order_by('id')
	students = ClassInformation.objects.filter(year_of_registration=year, current_class=card_class, stream=stream).order_by('child')
	marks = Mark.objects.filter(marks_class=card_class, year=year, stream=stream, term=term).order_by('-id')
	remarks = Remark.objects.filter(marks_class=card_class, year=year, stream=stream, term=term).order_by('-id')
	class_remarks = ClassTeacherRemark.objects.filter(marks_class=card_class, year=year, stream=stream, term=term).order_by('-id')
	subject_remarks = SubjectTeacherRemark.objects.filter(marks_class=card_class, year=year, stream=stream, term=term).order_by('-id')
	context = {
	'title': 'Report Cards',
	'subjects': subjects,
	'students': students,
	'card_class': card_class,
	'stream': stream,
	'year': year,
	'term': term,
	'marks': marks,
	'exam_sets': exam_sets,
	'remarks': remarks,
	'class_remarks': class_remarks,
	'subject_remarks': subject_remarks,
	}

	return render(request, 'hm/report_cards.html', context)

@login_required
def choose_review(request):
	user = request.user
	if request.method == 'POST':
		form = ChooseReportCardForm(request.POST)
		if form.is_valid():
			form.save(commit=False)
			return redirect('review-marks')
	else:
		form = ChooseReportCardForm()

	subjects = Subject.objects.all().order_by('-id')
	context = {
	'title': 'Academia',
	'submenu': 'Review Performance',
	'subjects': subjects,
	'form': form,
	}

	return render(request, 'hm/choose_review.html', context)

@login_required
def choose_attendance(request):
	user = request.user
	if request.method == 'POST':
		form = ChooseReportCardForm(request.POST)
		if form.is_valid():
			form.save(commit=False)
			return redirect('track-attendance')
	else:
		form = ChooseReportCardForm()

	subjects = Subject.objects.all().order_by('-id')
	context = {
	'title': 'Academia',
	'submenu': 'Track Daily Attendance',
	'subjects': subjects,
	'form': form,
	}

	return render(request, 'hm/choose_attendance.html', context)

@login_required
def select_attendance(request):
	attendances = TrackAttendance.objects.filter(date=timezone.now().date()).values('marks_class', 'stream').annotate(totalcount=Count('attendance'), presentcount=Count('attendance', filter=Q(attendance=1)), absentcount=Count('attendance', filter=Q(attendance=2)))
	context = {
	'title': 'Academia',
	'submenu': 'View Attendance',
	'attendances': attendances,
	'attendance_date': timezone.now().date(),
	}

	return render(request, 'hm/attendance.html', context)

@login_required
def attendance(request):
	attendance_date = request.GET.get('date', None)
	attendances = TrackAttendance.objects.filter(date=attendance_date).values('marks_class','stream').annotate(totalcount=Count('attendance'), presentcount=Count('attendance', filter=Q(attendance=1)), absentcount=Count('attendance', filter=Q(attendance=2)))
	context = {
	'title': 'Academia',
	'submenu': 'View Attendance',
	'attendances': attendances,
	'attendance_date': attendance_date,
	}

	return render(request, 'hm/attendance.html', context)

@login_required
def select_analysis(request):
	terms = Term.objects.all()
	subjects = Subject.objects.all()
	examsets = ExamSet.objects.all()
	the_term = Term.objects.get(pk=1)
	the_subject = Subject.objects.get(pk=1)
	the_examset = ExamSet.objects.get(pk=1)
	analysis = Mark.objects.filter(year=timezone.now().year, term=1, subject=1, exam_set=1).values('marks_class','stream').annotate(totalcount=Count('marks'), 
		d1count=Count('marks', filter=Q(marks__gte=95, marks__lte=100)), 
		d2count=Count('marks', filter=Q(marks__gte=80, marks__lte=94)), 
		c3count=Count('marks', filter=Q(marks__gte=70, marks__lte=79)), 
		c4count=Count('marks', filter=Q(marks__gte=60, marks__lte=69)),
		c5count=Count('marks', filter=Q(marks__gte=55, marks__lte=59)),
		c6count=Count('marks', filter=Q(marks__gte=50, marks__lte=54)),
		p7count=Count('marks', filter=Q(marks__gte=45, marks__lte=49)),
		p8count=Count('marks', filter=Q(marks__gte=40, marks__lte=44)),
		f9count=Count('marks', filter=Q(marks__gte=0, marks__lte=39)),)
	context = {
	'title': 'Academia',
	'submenu': 'Marks Analysis',
	'analysis': analysis,
	'year': timezone.now().year,
	'term':the_term,
	'subject':the_subject,
	'subjects':subjects,
	'terms':terms,
	'examsets':examsets,
	'examset':the_examset,
	}

	return render(request, 'hm/marks_analysis.html', context)

@login_required
def marks_analysis(request):
	year = request.GET.get('year', None)
	term = request.GET.get('term', None)
	subject = request.GET.get('subject', None)
	examset = request.GET.get('examset', None)
	the_term = Term.objects.get(pk=term)
	the_subject = Subject.objects.get(pk=subject)
	the_examset = ExamSet.objects.get(pk=examset)
	terms = Term.objects.all()
	subjects = Subject.objects.all()
	examsets = ExamSet.objects.all()
	analysis = Mark.objects.filter(year=year, term=term, subject=subject, exam_set=examset).values('marks_class','stream').annotate(totalcount=Count('marks'), 
		d1count=Count('marks', filter=Q(marks__gte=95, marks__lte=100)), 
		d2count=Count('marks', filter=Q(marks__gte=80, marks__lte=94)), 
		c3count=Count('marks', filter=Q(marks__gte=70, marks__lte=79)), 
		c4count=Count('marks', filter=Q(marks__gte=60, marks__lte=69)),
		c5count=Count('marks', filter=Q(marks__gte=55, marks__lte=59)),
		c6count=Count('marks', filter=Q(marks__gte=50, marks__lte=54)),
		p7count=Count('marks', filter=Q(marks__gte=45, marks__lte=49)),
		p8count=Count('marks', filter=Q(marks__gte=40, marks__lte=44)),
		f9count=Count('marks', filter=Q(marks__gte=0, marks__lte=39)),)

	context = {
	'title': 'Academia',
	'submenu': 'Marks Analysis',
	'analysis': analysis,
	'year': year,
	'term':the_term,
	'subject':the_subject,
	'subjects':subjects,
	'terms':terms,
	'examset':the_examset,
	'examsets':examsets,
	}

	return render(request, 'hm/marks_analysis.html', context)

@login_required
def track_attendance(request):

	the_class = None
	the_term = None
	the_stream = None

	card_classs = request.GET.get('marks_class', None)
	year = request.GET.get('year', None)
	term = request.GET.get('term', None)
	stream = request.GET.get('stream', None)
	try:
		the_class = Classe.objects.get(id=request.GET.get('marks_class', None))
		the_term = Term.objects.get(id=request.GET.get('term', None))
		the_stream = Stream.objects.get(id=request.GET.get('stream', None))
	except Exception:
		messages.warning(request, f'Try to make selections Again')

	card_class = the_class
	stream = the_stream
	term = the_term

	if request.method == 'POST':
		form = AttendanceCreateForm(request.POST,)

		if form.is_valid():
			form.instance.marks_class = card_class
			form.instance.stream = stream
			form.instance.year = year
			form.instance.term = term
			form.instance.user = request.user
			try:
				form.save()
				messages.success(request, f'Attendances Submitted Successfully')
				return redirect('choose-card')
			except:
				messages.warning(request, f'Attendances already entered for some students')

	else:
		form = AttendanceCreateForm()
	students = ClassInformation.objects.filter(year_of_registration=year, current_class=card_class, stream=stream).order_by('child')
	attendances = TrackAttendance.objects.filter(marks_class=card_class, year=year, stream=stream, term=term).order_by('-id')
	context = {
	'title': 'Academia',
	'submenu': 'Track Daily Attendance',
	'students': students,
	'card_class': card_class,
	'stream': stream,
	'year': year,
	'term': term,
	'attendances': attendances,
	'form':form,
	}

	return render(request, 'hm/track_attendance.html', context)

@login_required
def hm_review(request):

	the_class = None
	the_term = None
	the_stream = None

	card_classs = request.GET.get('marks_class', None)
	year = request.GET.get('year', None)
	term = request.GET.get('term', None)
	stream = request.GET.get('stream', None)
	try:
		the_class = Classe.objects.get(id=request.GET.get('marks_class', None))
		the_term = Term.objects.get(id=request.GET.get('term', None))
		the_stream = Stream.objects.get(id=request.GET.get('stream', None))
	except Exception:
		messages.warning(request, f'Try to make selections Again')

	card_class = the_class
	stream = the_stream
	term = the_term

	if request.method == 'POST':
		form = RemarkCreateForm(request.POST,)

		if form.is_valid():
			form.instance.marks_class = card_class
			form.instance.stream = stream
			form.instance.year = year
			form.instance.term = term
			form.instance.user = request.user
			try:
				form.save()
				messages.success(request, f'Remarks Submitted Successfully')
				return redirect('choose-card')
			except:
				messages.warning(request, f'Remarks already entered for some students')

	else:
		form = RemarkCreateForm()

	subjects = Subject.objects.filter(subject_class__in = card_classs).order_by('id')
	exam_sets = ExamSet.objects.filter(set_class__in = card_classs).order_by('id')
	sets = ExamSet.objects.filter(set_class__in = card_classs).count()
	students = ClassInformation.objects.filter(year_of_registration=year, current_class=card_class, stream=stream).order_by('child')
	marks = Mark.objects.filter(marks_class=card_class, year=year, stream=stream, term=term).order_by('-id')
	remarks = Remark.objects.filter(marks_class=card_class, year=year, stream=stream, term=term).order_by('-id')
	context = {
	'title': 'Academia',
	'submenu': 'Review Performance',
	'subjects': subjects,
	'students': students,
	'card_class': card_class,
	'stream': stream,
	'year': year,
	'term': term,
	'marks': marks,
	'remarks': remarks,
	'exam_sets': exam_sets,
	'sets':sets,
	'form':form,
	}

	return render(request, 'hm/hm_review.html', context)

@login_required
def class_choose_review(request):
	user = request.user
	if request.method == 'POST':
		form = ChooseClassReviewForm(request.POST, user=user)
		if form.is_valid():
			form.save(commit=False)
			return redirect('class-review')
	else:
		form = ChooseClassReviewForm()

	subjects = Subject.objects.all().order_by('-id')
	context = {
	'title': 'Marks',
	'submenu': 'Review Class Performance',
	'subjects': subjects,
	'form': form,
	}

	return render(request, 'hm/class_choose_review.html', context)
@login_required
def subject_review(request):

	the_subject = None
	the_term = None

	teacher_subject = request.GET.get('subject', None)
	year = request.GET.get('year', None)
	term = request.GET.get('term', None)
	try:
		the_subject = TeacherSubject.objects.get(id=request.GET.get('subject', None))
		the_term = Term.objects.get(id=request.GET.get('term', None))
	except Exception:
		messages.warning(request, f'Try to make selections Again')

	subject = the_subject.subject
	marks_class = the_subject.subject_class
	stream = the_subject.stream
	term = the_term

	if request.method == 'POST':
		form = SubjectTeacherRemarkCreateForm(request.POST,)

		if form.is_valid():
			form.instance.marks_class = marks_class
			form.instance.stream = stream
			form.instance.subject = subject
			form.instance.year = year
			form.instance.term = term
			form.instance.user = request.user
			try:
				form.save()
				messages.success(request, f'Remarks Submitted Successfully')
				return redirect('class-choose-review')
			except:
				messages.warning(request, f'Remarks already entered for some students')

	else:
		form = SubjectTeacherRemarkCreateForm()

	subjects = Subject.objects.all().order_by('id')
	exam_sets = ExamSet.objects.all().order_by('id')
	sets = ExamSet.objects.all().count()
	students = ClassInformation.objects.filter(year_of_registration=year, current_class=marks_class, stream=stream).order_by('child')
	marks = Mark.objects.filter(marks_class=marks_class, year=year, stream=stream, term=term).order_by('-id')
	remarks = SubjectTeacherRemark.objects.filter(marks_class=marks_class, year=year, stream=stream, term=term).order_by('-id')
	context = {
	'title': 'Marks',
	'submenu': 'Review Subject Performance',
	'subjects': subjects,
	'subject': subject,
	'students': students,
	'marks_class': marks_class,
	'stream': stream,
	'year': year,
	'term': term,
	'marks': marks,
	'remarks': remarks,
	'exam_sets': exam_sets,
	'sets':sets,
	'form':form,
	}

	return render(request, 'hm/subject_review.html', context)

def subject_choose_review(request):
	user = request.user
	if request.method == 'POST':
		form = ChooseRevForm(request.POST, user=user)
		if form.is_valid():
			form.save(commit=False)
			return redirect('subject-review')
	else:
		form = ChooseRevForm()

	subjects = Subject.objects.all().order_by('-id')
	context = {
	'title': 'Marks',
	'submenu': 'Review Subject Performance',
	'subjects': subjects,
	'form': form,
	}

	return render(request, 'hm/subject_choose_review.html', context)
@login_required
def class_review(request):

	the_class = None
	the_term = None
	the_stream = None

	card_classs = request.GET.get('marks_class', None)
	year = request.GET.get('year', None)
	term = request.GET.get('term', None)
	stream = request.GET.get('stream', None)
	try:
		the_class = Classe.objects.get(id=request.GET.get('marks_class', None))
		the_term = Term.objects.get(id=request.GET.get('term', None))
		the_stream = Stream.objects.get(id=request.GET.get('stream', None))
	except Exception:
		messages.warning(request, f'Try to make selections Again')

	card_class = the_class
	stream = the_stream
	term = the_term

	if request.method == 'POST':
		form = ClassTeacherRemarkCreateForm(request.POST,)

		if form.is_valid():
			form.instance.marks_class = card_class
			form.instance.stream = stream
			form.instance.year = year
			form.instance.term = term
			form.instance.user = request.user
			try:
				form.save()
				messages.success(request, f'Remarks Submitted Successfully')
				return redirect('class-choose-review')
			except:
				messages.warning(request, f'Remarks already entered for some students')

	else:
		form = ClassTeacherRemarkCreateForm()

	subjects = Subject.objects.filter(subject_class__in = card_classs).order_by('id')
	exam_sets = ExamSet.objects.filter(set_class__in = card_classs).order_by('id')
	sets = ExamSet.objects.filter(set_class__in = card_classs).count()
	students = ClassInformation.objects.filter(year_of_registration=year, current_class=card_class, stream=stream).order_by('child')
	marks = Mark.objects.filter(marks_class=card_class, year=year, stream=stream, term=term).order_by('-id')
	remarks = ClassTeacherRemark.objects.filter(marks_class=card_class, year=year, stream=stream, term=term).order_by('-id')
	context = {
	'title': 'Marks',
	'submenu': 'Review Class Performance',
	'subjects': subjects,
	'students': students,
	'card_class': card_class,
	'stream': stream,
	'year': year,
	'term': term,
	'marks': marks,
	'remarks': remarks,
	'exam_sets': exam_sets,
	'sets':sets,
	'form':form,
	}

	return render(request, 'hm/hm_review.html', context)

@login_required
def fees(request):
	fees = Fees.objects.values('child', 'fees_class','term','year').annotate(samount=Sum('amount'))
	students = Student.objects.all()
	fees_structure = SetFees.objects.all()
	context = {
	'title': 'Finance',
	'submenu': 'Fees',
	'fees': fees,
	'students': students,
	'fees_structure':fees_structure,
	}
	return render(request, 'hm/fees.html', context)

@login_required
def fees_record(request, child, fees_class, term, year):
	fees = Fees.objects.values('child', 'fees_class','term','year').annotate(samount=Sum('amount'))
	students = Student.objects.all()
	fees_structure = SetFees.objects.all()
	fees_records = Fees.objects.filter(child=child, fees_class=fees_class, term=term, year=year)
	child = Student.objects.get(pk=child)
	fees_class = Classe.objects.get(pk=fees_class)
	term = Term.objects.get(pk=term)
	context = {
	'title': 'Finance',
	'submenu': 'Fees',
	'fees': fees,
	'students': students,
	'fees_structure':fees_structure,
	'fees_records':fees_records,
	'child': child,
	'fees_class': fees_class,
	'term': term,
	'year': year,
	}
	return render(request, 'hm/fees.html', context)

@login_required
def print_gatepass(request, pk, id):
	student = Student.objects.get(pk=pk)
	gatepass = GatePass.objects.get(pk=id)
	context = {
	'title': 'Gate Pass',
	'student': student,
	'gatepass': gatepass,
	}
	return render(request, 'print/print_gatepass.html', context)

@login_required
def record_fees(request, pk):
	student =Student.objects.get(pk=pk)
	students = Student.objects.all()
	fees = Fees.objects.all()
	fees_structure = SetFees.objects.all()
	if request.method == 'POST':
		form = FeesCreateForm(request.POST, request.FILES)
		if form.is_valid():
			form.instance.user = request.user
			form.instance.child = student
			form.save(commit=False)
			try:
				form.save()
				messages.success(request, f'You have recorded fees for {student}.')
				return HttpResponseRedirect(reverse('fees'))
			except Exception:
				messages.warning(request, f'Error! May be Contact admin')
				
	else:
		form = FeesCreateForm()

	context = {
	'title': 'Finance',
	'submenu': 'Fees',
	'child': student,
	'fees': fees,
	'form': form,
	'fees_structure':fees_structure,
	}

	return render(request, 'hm/record_fees.html', context)

@login_required
def set_fees(request):
	if request.method == 'POST':
		form = SetFeesCreateForm(request.POST, request.FILES)
		if form.is_valid():
			form.instance.user = request.user
			form.save(commit=False)
			try:
				form.save()
				messages.success(request, f'Fees was set successful.')
				return HttpResponseRedirect(reverse('set-fees'))
			except Exception:
				messages.warning(request, f'Error! May be Contact admin')
				
	else:
		form = SetFeesCreateForm()
	fees = SetFees.objects.all()
	context = {
	'title': 'Finance',
	'submenu': 'Set Fees',
	'form': form,
	'fees': fees,
	}

	return render(request, 'hm/set_fees.html', context)

@login_required
def update_set_fees(request, pk):
	fee = SetFees.objects.get(pk=pk)
	if request.method == 'POST':
		form = SetFeesCreateForm(request.POST, request.FILES, instance=fee)
		if form.is_valid():
			try:
				form.save()
				messages.success(request, f'Fees was updated successfully.')
				return HttpResponseRedirect(reverse('set-fees'))
			except Exception:
				messages.warning(request, f'Error! May be Contact admin')
				
	else:
		form = SetFeesCreateForm(instance=fee)
	fees = SetFees.objects.all()
	context = {
	'title': 'Finance',
	'submenu': 'Set Fees',
	'form': form,
	'fees': fees,
	'tags': 'update',
	}

	return render(request, 'hm/set_fees.html', context)

def delete_set_fees(request, pk):
	try:
		fee = get_object_or_404(SetFees, pk=pk).delete()
		messages.warning(request, f'Fees structure was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('set-fees'))

@login_required
def update_fees(request, pk):
	fee =Fees.objects.get(pk=pk)
	students = Student.objects.all()
	fees = Fees.objects.all()
	fees_structure = SetFees.objects.all()
	if request.method == 'POST':
		form = FeesCreateForm(request.POST, request.FILES, instance=fee)
		if form.is_valid():
			form.save(commit=False)
			try:
				form.save()
				messages.success(request, f'You have Updated fees for {fee.child}.')
				return HttpResponseRedirect(reverse('fees'))
			except Exception:
				messages.warning(request, f'Error! May be Contact admin')
				
	else:
		form = FeesCreateForm(instance=fee)

	context = {
	'title': 'Finance',
	'submenu': 'Fees',
	'fee': fee,
	'fees': fees,
	'form': form,
	'tags': 'update',
	'fees_structure':fees_structure,
	}

	return render(request, 'hm/record_fees.html', context)
@login_required
def choose_fees_report(request):
	fees = Fees.objects.all().order_by('-id')
	total_fees = Fees.objects.all().aggregate(Sum('amount'))
	fees_structure = SetFees.objects.all()
	context = {
	'title': 'Finance',
	'submenu': 'Fees Report',
	'fees': fees,
	'total_fees': total_fees,
	'fees_structure': fees_structure,
	}

	return render(request, 'hm/choose_fees_report.html', context)
@login_required
def fees_report(request):
	start = request.GET.get('start', None)
	end = request.GET.get('end', None)
	fees_structure = SetFees.objects.all()
	fees = Fees.objects.filter(date__gte=start, date__lte=end).order_by('-id')
	total_fees = Fees.objects.filter(date__gte=start, date__lte=end).aggregate(Sum('amount'))
	context = {
	'title': 'Finance',
	'submenu': 'Fees Report',
	'fees': fees,
	'total_fees': total_fees,
	'start': start,
	'end': end,
	'fees_structure':fees_structure
	}

	return render(request, 'hm/choose_fees_report.html', context)
@login_required
def choose_income_report(request):
	incomes = Income.objects.all().order_by('-id')
	total_fees = Income.objects.all().aggregate(Sum('amount'))
	context = {
	'title': 'Finance',
	'submenu': 'Income Report',
	'incomes': incomes,
	'total_fees': total_fees,
	}

	return render(request, 'hm/choose_income_report.html', context)
@login_required
def income_report(request):
	start = request.GET.get('start', None)
	end = request.GET.get('end', None)
	incomes = Income.objects.filter(date__gte=start, date__lte=end).order_by('-id')
	total_fees = Income.objects.filter(date__gte=start, date__lte=end).aggregate(Sum('amount'))
	context = {
	'title': 'Finance',
	'submenu': 'Income Report',
	'incomes': incomes,
	'total_fees': total_fees,
	'start': start,
	'end': end,
	}

	return render(request, 'hm/choose_income_report.html', context)
@login_required
def choose_bill_report(request):
	bills = Bill.objects.all().order_by('-id')
	total_fees = Bill.objects.all().aggregate(Sum('total_cost'))
	context = {
	'title': 'Expense',
	'submenu': 'Expense Report',
	'bills': bills,
	'total_fees': total_fees,
	}

	return render(request, 'hm/choose_bill_report.html', context)
@login_required
def bill_report(request):
	start = request.GET.get('start', None)
	end = request.GET.get('end', None)
	bills = Bill.objects.filter(date__gte=start, date__lte=end).order_by('-id')
	total_fees = Bill.objects.filter(date__gte=start, date__lte=end).aggregate(Sum('total_cost'))
	context = {
	'title': 'Expense',
	'submenu': 'Expense Report',
	'bills': bills,
	'total_fees': total_fees,
	'start': start,
	'end': end,
	}

	return render(request, 'hm/choose_bill_report.html', context)
@login_required
def choose_expense_report(request):
	expenses = Expense.objects.all().order_by('-id')
	total_fees = Expense.objects.all().aggregate(Sum('total_cost'))

	qty_used = ExpenseItem.objects.annotate(qty_used=Sum('expense__useitem__quantity_used')).filter(pk=OuterRef('pk'))
	qty_bought = ExpenseItem.objects.annotate(qty_bought=Sum('expense__quantity')).filter(pk=OuterRef('pk'))
	total_cost = ExpenseItem.objects.annotate(total_cost=Sum('expense__total_cost')).filter(pk=OuterRef('pk'))
	items = ExpenseItem.objects.annotate(qty_bought=Subquery(qty_bought.values('qty_bought'), output_field=IntegerField()), total_cost=Subquery(total_cost.values('total_cost'), output_field=IntegerField()), qty_used=Subquery(qty_used.values('qty_used'), output_field=IntegerField()))

	context = {
	'title': 'Store',
	'submenu': 'Items Report',
	'expenses': expenses,
	'total_fees': total_fees,
	'items': items,
	}

	return render(request, 'hm/choose_expense_report.html', context)
@login_required
def expense_report(request):
	start = request.GET.get('start', None)
	end = request.GET.get('end', None)
	expenses = Expense.objects.filter(date__gte=start, date__lte=end).order_by('-id')
	total_fees = Expense.objects.filter(date__gte=start, date__lte=end).aggregate(Sum('total_cost'))

	qty_used = ExpenseItem.objects.filter(expense__useitem__date__gte=start, expense__useitem__date__lte=end).annotate(qty_used=Sum('expense__useitem__quantity_used')).filter(pk=OuterRef('pk'))
	qty_bought = ExpenseItem.objects.filter(expense__date__gte=start, expense__date__lte=end).annotate(qty_bought=Sum('expense__quantity')).filter(pk=OuterRef('pk'))
	total_cost = ExpenseItem.objects.filter(expense__date__gte=start, expense__date__lte=end).annotate(total_cost=Sum('expense__total_cost')).filter(pk=OuterRef('pk'))
	items = ExpenseItem.objects.annotate(qty_bought=Subquery(qty_bought.values('qty_bought'), output_field=IntegerField()), total_cost=Subquery(total_cost.values('total_cost'), output_field=IntegerField()), qty_used=Subquery(qty_used.values('qty_used'), output_field=IntegerField()))
	context = {
	'title': 'Store',
	'submenu': 'Items Report',
	'expenses': expenses,
	'total_fees': total_fees,
	'start': start,
	'end': end,
	'items': items,
	}

	return render(request, 'hm/choose_expense_report.html', context)

@login_required
def messanger(request):
	current_user = request.user
	if request.method == 'POST':
		form = MessageCreateForm(request.POST, request.FILES,)
		if form.is_valid():
			form.instance.sender = current_user
			# form.save()
			try:
				form.save()
				messages.success(request, f'Your message has been send.')
				return HttpResponseRedirect(reverse('messanger'))
			except Exception:
				messages.warning(request, f'Error! message not send')
				
	else:
		form = MessageCreateForm()

	users = User.objects.all()
	send = Message.objects.filter(sender = current_user).order_by('-id')
	inbox = Message.objects.filter(receiver__username__contains = current_user.username, status__lte=2).order_by('-id')
	total = Message.objects.filter(status=1, receiver__username__contains = current_user.username).count()
	context = {
	'title': 'Home',
	'submenu': 'Communication',
	'users': users,
	'form': form,
	'send': send,
	'inbox': inbox,
	'total': total,
	}
	return render(request, 'hm/messanger.html', context)

@login_required
def message_details(request, pk):
	current_user = request.user
	message = Message.objects.get(pk=pk)
	if request.method == 'POST':
		form = ReplyCreateForm(request.POST, request.FILES,)
		if form.is_valid():
			form.instance.message = message
			form.instance.replyer = current_user
			# form.save()
			try:
				form.save()
				messages.success(request, f'Your reply has been send.')
				return HttpResponseRedirect(reverse('message', kwargs={'pk':message.id}))
			except Exception:
				messages.warning(request, f'Error! reply not send')
				
	else:
		form = ReplyCreateForm()

	users = User.objects.all()
	send = Message.objects.filter(sender = current_user).order_by('-id')
	replys = Reply.objects.filter(message = message).order_by('-id')
	inbox = Message.objects.filter(receiver__username__contains = current_user.username, status__lte=2).order_by('-id')
	total = Message.objects.filter(status=1, receiver__username__contains = current_user.username).count()
	context = {
	'title': 'Home',
	'submenu': 'Communication',
	'users': users,
	'form': form,
	'send': send,
	'inbox': inbox,
	'total': total,
	'message': message,
	'replys': replys,
	}
	return render(request, 'hm/message_detail.html', context)

@login_required
def my_children(request):
	children = Student.objects.filter(parent=request.user.parentprofile.parent)
	context = {
	'title': 'Children',
	'submenu': 'My Children',
	'children': children,
	}

	return render(request, 'hm/my_children_list.html', context)

@login_required
def set_children(request):

	if  request.method == 'POST':
		social_form = SocialSkillCreateForm(request.POST, request.FILES,)
		if social_form.is_valid():
			if 'save_social' in request.POST:
				try:
					social_form.save()
					messages.success(request, f'New Social Skill has been added.')
					return HttpResponseRedirect(reverse('set-children'))
				except Exception:
					messages.warning(request, f'Error! Social Skill not added')
	else:
		social_form = SocialSkillCreateForm()

	if  request.method == 'POST':
		sport_form = SportCreateForm(request.POST, request.FILES,)
		if sport_form.is_valid():
			if 'save_sport' in request.POST:
				try:
					sport_form.save()
					messages.success(request, f'New Sport has been added.')
					return HttpResponseRedirect(reverse('set-children'))
				except Exception:
					messages.warning(request, f'Error! Sport not added')
	else:
		sport_form = SportCreateForm()

	if  request.method == 'POST':
		hygiene_form = HygieneCreateForm(request.POST, request.FILES,)
		if hygiene_form.is_valid():
			if 'save_hygiene' in request.POST:
				try:
					hygiene_form.save()
					messages.success(request, f'New Hygiene Level has been added.')
					return HttpResponseRedirect(reverse('set-children'))
				except Exception:
					messages.warning(request, f'Error! Hygiene level not added')
	else:
		hygiene_form = HygieneCreateForm()

	if  request.method == 'POST':
		reading_form = ReadingCreateForm(request.POST, request.FILES,)
		if reading_form.is_valid():
			if 'save_reading' in request.POST:
				try:
					reading_form.save()
					messages.success(request, f'New Reading level has been added.')
					return HttpResponseRedirect(reverse('set-children'))
				except Exception:
					messages.warning(request, f'Error! Reading level not added')
	else:
		reading_form = ReadingCreateForm()

	if  request.method == 'POST':
		participation_form = ParticipationCreateForm(request.POST, request.FILES,)
		if participation_form.is_valid():
			if 'save_participation' in request.POST:
				try:
					participation_form.save()
					messages.success(request, f'New participation level has been added.')
					return HttpResponseRedirect(reverse('set-children'))
				except Exception:
					messages.warning(request, f'Error! participation level not added')
	else:
		participation_form = ReadingCreateForm()

	if  request.method == 'POST':
		leadership_form = LeadershipCreateForm(request.POST, request.FILES,)
		if leadership_form.is_valid():
			if 'save_leadership' in request.POST:
				try:
					leadership_form.save()
					messages.success(request, f'New Leadership level has been added.')
					return HttpResponseRedirect(reverse('set-children'))
				except Exception:
					messages.warning(request, f'Error! Leadership level not added')
	else:
		leadership_form = LeadershipCreateForm()

	if  request.method == 'POST':
		smartness_form = SmartnessCreateForm(request.POST, request.FILES,)
		if smartness_form.is_valid():
			if 'save_smartness' in request.POST:
				try:
					smartness_form.save()
					messages.success(request, f'New Smartness level has been added.')
					return HttpResponseRedirect(reverse('set-children'))
				except Exception:
					messages.warning(request, f'Error! Smartness level not added')
	else:
		smartness_form = SmartnessCreateForm()

	socialskills = SocialSkill.objects.all()
	sports = Sport.objects.all()
	hygiene_levels = Hygiene.objects.all()
	reading_levels = Reading.objects.all()
	participation_levels = Participation.objects.all()
	leadership_levels = Leadership.objects.all()
	smartness_levels = Smartness.objects.all()
	context = {
	'title': 'Settings',
	'submenu': 'Children',
	'social_form':social_form,
	'sport_form':sport_form,
	'hygiene_form':hygiene_form,
	'reading_form':reading_form,
	'participation_form':participation_form,
	'leadership_form':leadership_form,
	'smartness_form':smartness_form,
	'sports':sports,
	'socialskills':socialskills,
	'hygiene_levels':hygiene_levels,
	'reading_levels':reading_levels,
	'participation_levels':participation_levels,
	'leadership_levels':leadership_levels,
	'smartness_levels':smartness_levels,
	}

	return render(request, 'hm/set_children.html', context)

def delete_smartness(request, pk,):
	try:
		report = get_object_or_404(Smartness, pk=pk).delete()
		messages.success(request, f'The Smartness Level was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('set-children'))

def delete_leadership(request, pk,):
	try:
		report = get_object_or_404(Leadership, pk=pk).delete()
		messages.success(request, f'The Leadership Level was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('set-children'))

def delete_participation(request, pk,):
	try:
		report = get_object_or_404(Participation, pk=pk).delete()
		messages.success(request, f'The Participation Level was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('set-children'))

def delete_reading(request, pk,):
	try:
		report = get_object_or_404(Reading, pk=pk).delete()
		messages.success(request, f'The Reading Level was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('set-children'))

def delete_hygiene(request, pk,):
	try:
		report = get_object_or_404(Hygiene, pk=pk).delete()
		messages.success(request, f'The Hygiene Level was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('set-children'))

def delete_stream(request, pk,):
	try:
		report = get_object_or_404(Stream, pk=pk).delete()
		messages.success(request, f'The Stream was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('set-children'))

def delete_social(request, pk,):
	try:
		report = get_object_or_404(SocialSkill, pk=pk).delete()
		messages.success(request, f'The Social Skill was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('set-children'))

def delete_sport(request, pk,):
	try:
		report = get_object_or_404(Sport, pk=pk).delete()
		messages.success(request, f'The Sport was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('set-children'))

@login_required
def set_staff(request):
	if  request.method == 'POST':
		position_form = PositionCreateForm(request.POST, request.FILES,)
		if position_form.is_valid():
			if 'save_position' in request.POST:
				try:
					position_form.save()
					messages.success(request, f'New Position has been added.')
					return HttpResponseRedirect(reverse('set-staff'))
				except Exception:
					messages.warning(request, f'Error! Position not added')
	else:
		position_form = PositionCreateForm()

	if  request.method == 'POST':
		category_form = StaffCategoryCreateForm(request.POST, request.FILES,)
		if category_form.is_valid():
			if 'save_category' in request.POST:
				try:
					category_form.save()
					messages.success(request, f'New Category has been added.')
					return HttpResponseRedirect(reverse('set-staff'))
				except Exception:
					messages.warning(request, f'Error! Category not added')
	else:
		category_form = StaffCategoryCreateForm()

	if  request.method == 'POST':
		status_form = StaffStatusCreateForm(request.POST, request.FILES,)
		if status_form.is_valid():
			if 'save_status' in request.POST:
				try:
					status_form.save()
					messages.success(request, f'New Staff Status has been added.')
					return HttpResponseRedirect(reverse('set-staff'))
				except Exception:
					messages.warning(request, f'Error! Staff Status was not added')
	else:
		status_form = StaffStatusCreateForm()

	if  request.method == 'POST':
		scale_form = ScaleCreateForm(request.POST, request.FILES,)
		if scale_form.is_valid():
			if 'save_scale' in request.POST:
				try:
					scale_form.save()
					messages.success(request, f'New Scale has been added.')
					return HttpResponseRedirect(reverse('set-staff'))
				except Exception:
					messages.warning(request, f'Error! Scale was not added')
	else:
		scale_form = ScaleCreateForm()

	positions = Position.objects.all()
	categories = StaffCategory.objects.all()
	statuses = StaffStatus.objects.all()
	scales = Scale.objects.all()
	context = {
	'title': 'Settings',
	'submenu': 'Staff',
	'positions': positions,
	'position_form': position_form,
	'categories': categories,
	'category_form': category_form,
	'statuses': statuses,
	'status_form': status_form,
	'scales': scales,
	'scale_form': scale_form,
	}
	return render(request, 'hm/set_staff.html', context)

def delete_position(request, pk,):
	try:
		report = get_object_or_404(Position, pk=pk).delete()
		messages.success(request, f'The Position was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('set-staff'))

def delete_scale(request, pk,):
	try:
		report = get_object_or_404(Scale, pk=pk).delete()
		messages.success(request, f'The Scale was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('set-staff'))

def delete_staff_category(request, pk,):
	try:
		report = get_object_or_404(StaffCategory, pk=pk).delete()
		messages.success(request, f'The Category was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('set-staff'))

def delete_staff_status(request, pk,):
	try:
		report = get_object_or_404(StaffStatus, pk=pk).delete()
		messages.success(request, f'The Status was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('set-staff'))


@login_required
def set_academia(request):
	if request.method == 'POST':
		stream_form = StreamCreateForm(request.POST, request.FILES,)
		if stream_form.is_valid():
			if 'save_stream' in request.POST:
				try:
					stream_form.save()
					messages.success(request, f'New stream has been added.')
					return HttpResponseRedirect(reverse('set-academia'))
				except Exception:
					messages.warning(request, f'Error! stream not added')
				
	else:
		stream_form = StreamCreateForm()

	if request.method == 'POST':
		subject_form = SubjectCreateForm(request.POST, request.FILES,)
		if subject_form.is_valid():
			if 'save_subject' in request.POST:
				try:
					subject_form.save()
					messages.success(request, f'New subject has been added.')
					return HttpResponseRedirect(reverse('set-academia'))
				except Exception:
					messages.warning(request, f'Error! subject not added')
				
	else:
		subject_form = SubjectCreateForm()

	if request.method == 'POST':
		class_form = ClassCreateForm(request.POST, request.FILES,)
		if class_form.is_valid():
			if 'save_class' in request.POST:
				try:
					class_form.save()
					messages.success(request, f'New class has been added.')
					return HttpResponseRedirect(reverse('set-academia'))
				except Exception:
					messages.warning(request, f'Error! class not added')
				
	else:
		class_form = ClassCreateForm()

	if request.method == 'POST':
		examset_form = ExamSetCreateForm(request.POST, request.FILES,)
		if examset_form.is_valid():
			if 'save_examset' in request.POST:
				try:
					examset_form.save()
					messages.success(request, f'New Exam Set has been added.')
					return HttpResponseRedirect(reverse('set-academia'))
				except Exception:
					messages.warning(request, f'Error! Exam Set not added')
				
	else:
		examset_form = ExamSetCreateForm()

	if request.method == 'POST':
		term_form = TermCreateForm(request.POST, request.FILES,)
		if term_form.is_valid():
			if 'save_term' in request.POST:
				try:
					term_form.save()
					messages.success(request, f'New Term has been added.')
					return HttpResponseRedirect(reverse('set-academia'))
				except Exception:
					messages.warning(request, f'Error! Term not added')
				
	else:
		term_form = TermCreateForm()

	streams = Stream.objects.all()
	classes = Classe.objects.all()
	subjects = Subject.objects.all()
	examsets = ExamSet.objects.all()
	terms = Term.objects.all()
	context = {
	'title': 'Settings',
	'submenu': 'Academia',
	'streams':streams,
	'stream_form':stream_form,
	'classes':classes,
	'class_form':class_form,
	'subjects':subjects,
	'subject_form':subject_form,
	'examset_form':examset_form,
	'examsets':examsets,
	'terms':terms,
	'term_form':term_form,

	}
	return render(request, 'hm/set_academia.html', context)

def delete_term(request, pk,):
	try:
		report = get_object_or_404(Term, pk=pk).delete()
		messages.success(request, f'The Term was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('set-academia'))

def delete_examset(request, pk,):
	try:
		report = get_object_or_404(ExamSet, pk=pk).delete()
		messages.success(request, f'The Exam Set was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('set-academia'))

def delete_subject(request, pk,):
	try:
		report = get_object_or_404(Subject, pk=pk).delete()
		messages.success(request, f'The Subject was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('set-academia'))

def delete_clas(request, pk,):
	try:
		report = get_object_or_404(Classe, pk=pk).delete()
		messages.success(request, f'The Class was deleted')
	except Exception:
		messages.warning(request, f'Error! Record Not Found')
	return HttpResponseRedirect(reverse('set-academia'))

@login_required
def set_finance(request):
	context = {
	'title': 'Settings',
	'submenu': 'Finance',
	}

	return render(request, 'hm/set_finance.html', context)

@login_required
def set_inventory(request):
	context = {
	'title': 'Settings',
	'submenu': 'Inventory',
	}

	return render(request, 'hm/set_inventory.html', context)

@login_required
def set_library(request):
	context = {
	'title': 'Settings',
	'submenu': 'Library',
	}

	return render(request, 'hm/set_library.html', context)

@login_required
def set_general(request):
	context = {
	'title': 'Settings',
	'submenu': 'General',
	}

	return render(request, 'hm/set_general.html', context)

@login_required
def home(request):
	current_user = request.user
	yr = timezone.now().year
	total_fees = Fees.objects.filter(year=yr).aggregate(fees_amount = Sum('amount'))
	total_expenses = Bill.objects.filter(date__year=yr).aggregate(expense_amount = Sum('total_cost'))
	total_students = ClassInformation.objects.filter(year_of_registration=yr).count()
	total_staff = Staff.objects.filter(status=1).count()
	gatepass = GatePass.objects.filter(date_created__year=yr).count()
	attendance = TrackAttendance.objects.filter(date=timezone.now()).count()
	message = Message.objects.filter(receiver__username__contains = current_user.username, status__lte=2).count()
	context = {
	'title': 'Home',
	'submenu': 'Home',
	'total_fees':total_fees,
	'total_students':total_students,
	'total_staff':total_staff,
	'total_expenses':total_expenses,
	'attendance':attendance,
	'gatepass':gatepass,
	'message':message,
	}

	return render(request, 'hm/home.html', context)

class CalendarView(ListView):
    model = Meeting
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))
        d = get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['title'] = 'Home'
        context['submenu'] = 'Calendar'
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime.date(year, month, day=1)
    return datetime.datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month
