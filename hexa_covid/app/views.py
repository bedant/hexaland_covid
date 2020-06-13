from django.shortcuts import render
from django.http import HttpResponse
from .models import Hexlandcell
from django.template.defaulttags import register
from django.db.models import Sum

@register.filter
def get_range(value):
	return range(value)

rows=5
cols=5

def is_first_hotspot():
	queryset = Hexlandcell.objects.filter(is_affected=True)
	print("ifh" , queryset.count()==0)
	return queryset.count()==0
		# sum=0
		# for i in range(rows):
		# 	for j in range(self.cols):
		# 		sum += self.country[i][j][1]
		# if sum==0:
		# 	return True
		# return False


def isValid(x,y):
	if(x<0 or y<0 or x>=rows or y>=cols):
		return False
	return True

def neighbour(src_i,src_j,border):
	x=src_i
	y=src_j
	if(border==0):
		x-=1
	if(border==3):
		x+=1
	if(border==1):
		y+=1
		if(src_j%2==1):
			x-=1

	if(border==2):
		y+=1
		if(src_j%2==0):
			x+=1

	if(border==5):
		y-=1
		if(src_j%2==1):
			x-=1

	if(border==4):
		y-=1
		if(src_j%2==0):
			x+=1
	print(src_i,src_j,border,x,y)
	return x,y

# def query(name):
# 	x = self.name_to_idx[name][0]
# 	y = self.name_to_idx[name][1]
# 	neigh_list = []
# 	for border in range(6):
# 		neigh_x, neigh_y = self.neighbour(x,y,border)
# 		if self.isValid(neigh_x, neigh_y):
# 			if(self.country[neigh_x][neigh_y][1]==1):
# 				neigh_list.append((border,self.country[neigh_x][neigh_y][0],"red"))
# 			else:
# 				neigh_list.append((border,self.country[neigh_x][neigh_y][0],"blue"))
# 	return neigh_list

def search_cell(cell_name):
	print("search_cell ",cell_name)
	queryset = Hexlandcell.objects.filter(name=cell_name).values('name', 'is_affected','row','col')
	# cell_x = Hexlandcell.objects.raw('SELECT row FROM app_hexlandcell where name="'+cell_name+'"')
	print("cell_x ", queryset.get())
	src_x = queryset.get()['row']
	src_y = queryset.get()['col']
	neigh_list = []
	for border in range(6):
		neigh_x, neigh_y = neighbour(src_x,src_y,border)
		if isValid(neigh_x, neigh_y):
			queryset = Hexlandcell.objects.filter(row=neigh_x,col=neigh_y).values('name', 'is_affected','row','col')
			# if queryset.get().is_affected :
			print(queryset.get())
			print("QS2",queryset.get())
			
			neigh_list.append( "Cell " + str(cell_name+" shares its border " + str(border) + " with " + queryset.get()['name'])) #, queryset.get()['row'] , queryset.get()['col'] , queryset.get()['is_affected']])
			# neigh_list +="\n";
			# if country[neigh_x][neigh_y][1]==1 :
			# 	neigh_list.append((border,self.country[neigh_x][neigh_y][0],"red"))
			# else:
			# 	neigh_list.append((border,self.country[neigh_x][neigh_y][0],"blue"))
	return neigh_list
	

# def add_to_cluster(self,name,border):
# 	x = self.name_to_idx[name][0]
# 	y = self.name_to_idx[name][1]

# 	if(self.country[x][y][1]==1 or self.is_first_hotspot()):
# 	#can be added
# 		neigh_x,neigh_y = self.neighbour(x,y,border)

# 		if(self.isValid(neigh_x,neigh_y)):
# 			self.country[neigh_x][neigh_y][1]=1
# 			print(neigh_x,neigh_y, "is set as hotspot")
# 		else:
# 			print("invalid cell")

def insert_cell(cell_name,border):
	# print("insert_cell ",cell_name,border)
	query_set = Hexlandcell.objects.filter(name=cell_name).values('name', 'is_affected','row','col')
	message_list = []
	if is_first_hotspot()==True or query_set.get()['is_affected']==True:
	#can be added
		x = query_set.get()['row']
		y = query_set.get()['col']
		neigh_x,neigh_y = neighbour(x,y,border)
		print("neigh",neigh_x,neigh_y)
		
		if(isValid(neigh_x,neigh_y)):
			# self.country[neigh_x][neigh_y][1]=1
			t = Hexlandcell.objects.get(row=neigh_x,col=neigh_y)
			t.is_affected = True  # change field
			t.save() # this will update only
			message_list.append(str("Cell " +t.name+ " is set as hotspot!!"))
			return message_list
		else:
			message_list.append(str("Invalid cell, out of range!!"))
			return message_list
	else:
		message_list.append("Entered cell is not a hotspot!!")
		return message_list
	# cell_x = Hexlandcell.objects.raw('SELECT row FROM app_hexlandcell where name="'+cell_name+'"')
	# print("cell_x ", queryset.get())
	# src_x = queryset.get()['row']
	# src_y = queryset.get()['col']

	# print("insert_cell",cell_name,border)

def dfs(vis,src_i,src_j,country):
	vis[src_i][src_j] = True
	for border in range(6):
		neigh_x,neigh_y = neighbour(src_i,src_j,border)
		if isValid(neigh_x,neigh_y) and (not vis[neigh_x][neigh_y]) and (country[neigh_x][neigh_y][1]==True):
			dfs(vis,neigh_x,neigh_y,country)

# def remove_from_cluster(self,name):
# 	x = self.name_to_idx[name][0]
# 	y = self.name_to_idx[name][1]
# 	self.country[x][y][1]=0
# 	vis = [ [False for j in range(self.cols)] for i in range(self.rows)]
# 	connected_comps=0
# 	for i in range(self.rows):
# 		for j in range(self.cols):
# 			if not vis[i][j] and self.country[i][j][1]==1 :
# 				connected_comps+=1
# 				if connected_comps>1:
# 					break
# 				self.dfs(vis,i,j)
# 	if(connected_comps>1):
# 	#cant be removed
# 		self.country[x][y][1] = 1
# 		print("disconnects the cluster!!")

def remove_cell(cell_name):
	print("remove_cell ",cell_name)
	
	# self.country[x][y][1]=0
	country = [[[] for j in range(cols)] for i in range(rows)] 
	vis = [ [False for j in range(cols)] for i in range(rows)]
	query_set = list(Hexlandcell.objects.all())
	for entry in query_set:
		country[entry.row][entry.col] = [entry.name,entry.is_affected]
		# print(entry.name,entry.row,entry.col,entry.is_affected)
	# for i in range(rows):
	# 		for j in range(cols):
	# 			print(country[i][j],end="  ")
	# 		print("\n")

	query_set = Hexlandcell.objects.filter(name=cell_name).values('name', 'is_affected','row','col')
	x = query_set.get()['row']
	y = query_set.get()['col']
	if country[x][y][1] == False:
		message_list = [str("Cell "+cell_name+" was not a hotspot. No action required")]
		return message_list
	country[x][y][1] = False

	connected_comps=0
	for i in range(rows):
		for j in range(cols):
			print("vis",vis[i][j])
			print("country",country[i][j])
			if not vis[i][j] and country[i][j][1]==True :
				connected_comps+=1
				if connected_comps>1:
					break
				dfs(vis,i,j,country)
	message_list = []
	if(connected_comps>1):
	#cant be removed
		# self.country[x][y][1] = 1
		message_list.append(str("Removing cell "+ cell_name + " disconnects the cluster!!"))
		return message_list
	else:
		t = Hexlandcell.objects.get(row=x,col=y)
		t.is_affected = False  # change field
		t.save() # this will update only
		message_list.append(str("Cell " + cell_name + " removed!!"))
		return message_list

def home(request):
	# return HttpResponse('Hello, World!')
	message=""
	if request.method=="POST":
		query_type = request.POST['query_type']
		name = request.POST['name']
		query_set = Hexlandcell.objects.filter(name=name).values('name', 'is_affected','row','col')
		if not query_set:
			message = ["Incorrect Cell Name"]
		else:	
			print(type(request.POST))
			border = ""
			if request.POST.__contains__('border'):
				border = request.POST['border']
			else:
				print("no border provided")
			neighbours = []
			
			if query_type == "search":
				message = search_cell(name)
			
			if query_type == "insert":
				if(border=="" or int(border)>5 or int(border)<0):
					message = ["Border not in range!!"]
				else:
					message = insert_cell(name,int(border))
			
			if query_type == "remove":
				message = remove_cell(name)
			# print(query_type,name,str(border))
		# print(request.method)
	dict_to_pass = {}
	dict_to_pass['rows']=5
	dict_to_pass['cols']=cols
	dict_to_pass['message'] = message
	print(message)
	# name_to_idx = {}
	grid = [ [[] for j in range(cols)] for i in range(rows)]
	for entry in Hexlandcell.objects.all():
		# print(entry.name,entry.row)
		grid[entry.row][entry.col] = {"name":entry.name, "is_affected":entry.is_affected}
		# name_to_idx[entry.name] = (entry.row,entry.col)
	dict_to_pass['grid'] = grid
	
	return render(request, 'home.html', dict_to_pass)#, {'boards': boards})
# Create your views here.
def init(request):
	Hexlandcell.objects.all().delete()
	for i in range(rows):
		for j in range(cols):
			name = chr(ord('a') + i) + chr(ord('a') + j)
			foo_instance = Hexlandcell.objects.create(row=i,col=j,name=name,is_affected=False)
	dict_to_pass = {}
	dict_to_pass['rows']=5
	dict_to_pass['cols']=cols
	dict_to_pass['message'] = ""
	# print(message)
	# name_to_idx = {}
	grid = [ [[] for j in range(cols)] for i in range(rows)]
	for entry in Hexlandcell.objects.all():
		# print(entry.name,entry.row)
		grid[entry.row][entry.col] = {"name":entry.name, "is_affected":entry.is_affected}
		# name_to_idx[entry.name] = (entry.row,entry.col)
	dict_to_pass['grid'] = grid
	
	return render(request, 'home.html', dict_to_pass)#, {'boards': boards})
	# return render(request, 'home.html')


