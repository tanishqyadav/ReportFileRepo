import ctypes
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from tabulate import tabulate
from .models import *
from .helperReport import *
from .forms import *

# Create your views here.



def report(request):
	response = HttpResponse(content_type='text/plain')
	response['Content-Disposition'] = 'attachment;filename = report.txt'

	programsobj = Program.objects.all()
	examsobj = Exams.objects.all()
	semester = [1,2,3,4,5,6]
	report_type = ['1','2','report']
	# print(examsobj)

	if request.method == 'POST':
		sem = request.POST.get('semester_no')
		pcode = request.POST.get('program_code')
		aterm = request.POST.get('academic_term')
		rtype = request.POST.get('report_type')
		# print(sem,type(sem), pcode, aterm)
		examdetails = examsobj.filter(pk=aterm).first()
		programdetails = programsobj.filter(pk=pcode).first()
		icode = programdetails.code + str(examdetails.pk)

		institutedetails = Institute.objects.filter(code=icode).first()
		studobj = Student.objects.filter(institute=1,program=2).all()
		
		# print(icode,type(icode))
		if rtype == '1':
			# response.writelines('Examination Form Verification Report')
			initial_print = '''
			Examination Form Verification Report
			sem:\t{}
			exam:\t{}
			name of institute:\t{}
			institute code:\t{}
			name of branch:\t{}
			branch code:\t{}
			exam held:\t{}
			report time:\t{}
			'''.format(
				sem,
				examdetails.academic_term,
				institutedetails.name,
				icode,
				programdetails.name,
				programdetails.code,
				examdetails.exam_held,
				datetime.now())
			response.write(initial_print)
			response.writelines('\n')
			fields_names=['reg_no','first_name','middle_name','last_name','gender','modified_date','category','paymentstatus']
			
			print('\n studval', studobj.values().first())
			response.write((tabulate(customQuerysetReportTable(studobj,fields_names), headers=fields_names, tablefmt='psql',)))

			return response
		if rtype == '2':
			initial_print='''
			Attendence sheet of students
			Name of Institute:{}
			Name of Branch:{}
			Name of Exam:{},held in {}
			'''.format(
				institutedetails.name,
				programdetails.name,
				examdetails.academic_term,examdetails.exam_held
			)

			fields_names = ['sr.','Roll Number, Name & Signature','Subject\nCode','Date of\nExam','Signature of Student/\nAbsent','Copy No.','Signature of Invigilator']
			table = []
			for value in studobj.values():
				sign = 'E:\WNC8\project\static\images\inner-image\sign.jpg'
				subject_code = '''123\n234\n345'''
				empty= '_'
			
				table.append(['{}\n{}\n{}\n{}'.format(value['reg_no'], value['first_name'],'-'*len(fields_names[1]) ,sign),'{}\n '.format( subject_code),'{}\n '.format(subject_code),(empty*len(fields_names[4]) + '\n')*3,(empty*len(fields_names[5]) + '\n')*3,(empty*len(fields_names[6]) + '\n')*3])
			
			# print(table)
			response.write((tabulate(table, headers=fields_names, tablefmt='grid',showindex=True,)))

			return response
		if rtype == '3':
			initial_print='''
			Semester:{}
			Name of Institute:{}
			Name of Branch:{}
			Name of Exam:{},held in {}
			'''.format(
				sem,
				institutedetails.name,
				programdetails.name,
				examdetails.academic_term,examdetails.exam_held
			)
			
			courseobj = CourseLe.objects.all()
			print(courseobj)
			header = []
			head = []
			for course in courseobj:
				head.append([course.code,course.name])
		
			print(head)

			# response.write(tabulate(table,headers=header,tablefmt='grid',stralign='right'))
			# return response


	context = {
		'programsobj':programsobj,
		'examsobj':examsobj,
		'semester':semester
	}
	return render(request, 'report.html', context)

def namepls(f='',m='',l=''):
	name = ''
	# if f != None and m!=None and l!=None:
	# 	name = f + m + l
	if f !=None and m!=None and l==None:
		name = f+m
	if f!=None and m==None and l!=None:
		name = f+l
	else:
		name = f 

	return name



def dashboard(request):
	# from .make_csvfile_locally import qs_to_local_csv
	# qsf = Student.objects.filter(id=487)
	# qs=Student.objects.all()

	# # qs_to_local_csv(qs)
	# qs_to_local_csv(qsf,filename='qsa_student.csv')
	import pandas as pd
	import numpy as np

	marksheet = pd.read_csv('E:\WNC8\csvstorage\marksheetverification.csv') 
	obtained_mrks = marksheet['obtained_marks']
	xaxis = ['obtained marks']
	context = {
		'omarks':obtained_mrks,
		'xaxis':xaxis
	}
	return render(request,'dashboard.html',context)



def enterreport(request):
	response = HttpResponse(content_type='text/plain')
	response['Content-Disposition'] = 'attachment;filename = report.txt'
	form = MyForm()
	if request.method == 'POST':
		form = MyForm(request.POST)
		
		if form.is_valid():
			f = form.cleaned_data['first']
			s = form.cleaned_data['second']
		
			
			response.write((tabulate(formInputReport(form).table, headers=formInputReport(form).fields_names, tablefmt='psql',)))

			for i in range(3):
				print(i)
				enterreport(request)
			return response
				

	return render(request, 'entreport.html', {'form':form})

