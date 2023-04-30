def fullDbReportTable(MyModel):
	ModelObj = MyModel.objects.all()
	fields_names = fieldsNameFullDb(MyModel)
	return tableStruc(ModelObj,fields_names)

def customFieldsReportTable(MyModel, customModelFields=[]):
	ModelObj = MyModel.objects.all()
	fields_names = customModelFields
	return tableStruc(ModelObj,fields_names)

def customQuerysetReportTable(ModelObj, customModelFields=[]):
	fields_names = customModelFields
	return tableStruc(ModelObj,fields_names)

def customQuerysetFullDbReportTable(ModelObj, MyModel):
	fields_names = fieldsNameFullDb(MyModel)
	return tableStruc(ModelObj,fields_names)

def tableStruc(ModelObj, fields_names):
	table = []
	for value in ModelObj.values():
		t=[]
		for i in range(len(fields_names)):
			t.append(value['{}'.format(fields_names[i])])
		table.append(t)
	return table

def fieldsNameFullDb(MyModel):
	fields_names = [f.name for f in MyModel._meta.get_fields()]
	return fields_names

class formInputReport:
	def __init__(self, form):
		table, fields_names = self.formtoTable(form)
		self.table = table
		self.fields_names = fields_names

	def formtoTable(self,form):
		table = []
		fields_names = []
		data = []
		for items in form.data.items():
			data.append(items)
		t=[]
		x=len(data)
		for key, value in data[0:1]:
			fields_names.append(key)
			t.append(value)
		table.append(t)

		print(fields_names, table)

		return table, fields_names


# def bordered(text):
#     lines = text.splitlines()
#     width = max(len(s) for s in lines)
#     res = ['┌' + '─' * width + '┐']
#     for s in lines:
#         res.append('│' + (s + ' ' * width)[:width] + '│')
#     res.append('└' + '─' * width + '┘')
#     return '\n'.join(res)