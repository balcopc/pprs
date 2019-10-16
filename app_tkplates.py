from tkinter import *
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import urllib.request, json

print("Loading...be patient!")

url = "https://api.ipify.org/?format=json"

req=urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
	buf = response.read()
	data = json.loads(buf.decode('utf-8'))

ip1=data['ip']
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('mydb-226117-35c1502dfc9a.json', scope)
gc = gspread.authorize(credentials)
wks=gc.open('Test').sheet1
records=wks.get_all_records()

def search1():
	text1.delete(0.0,END)
	get1=entry1.get()
	get1=get1.upper()
		
	for x,recs in enumerate(records):
		if get1==records[x]["Plate"]:
			state1=records[x]["State"]
			color1=records[x]["Color"]
			make1=records[x]["Make"]
			model1=records[x]["Model"]
			crime1=records[x]["Crime"]
			date1=records[x]["DateTime"]
			info=state1+" "+get1+" "+color1+" "+make1+" "+model1+" "+crime1+" "+date1+"\n"
			text1.insert(INSERT,info)
		
def clr():
	entry1.delete(0,END)

def reset():
	text1.delete(0.0,END)
	clr()	
	
def clear():
	entry2.delete(0,END)
	entry3.delete(0,END)
	entry4.delete(0,END)
	entry5.delete(0,END)	
	entry6.delete(0,END)
	entry7.delete(0,END)
	
def report():
	
	state1=entry2.get()
	state1=state1.upper()[:2]
	plate1=entry3.get()
	plate1=plate1.upper()[:7]
	report1=entry8.get()
	report1=report1.lower()[:20]
	
	if plate1=="":
		text1.insert(INSERT,"Plate required"+"\n")
		pass
	else:	
		color1=entry4.get()
		color1=color1.title()[:10]
		make1=entry5.get()
		make1=make1.title()[:10]
		model1=entry6.get()
		model1=model1.title()[:10]
		crime1=entry7.get()
		crime1=crime1.upper()[:15]
		if crime1=="":
			text1.insert(INSERT,"Infraction required"+"\n")
			pass
			
		else:
			date1=datetime.datetime.now()
			date1=str(date1)[:16]
			info=state1+" "+plate1+" "+color1+" "+make1+" "+model1+" "+crime1+" "+date1+"\n"
			text1.insert(INSERT,"Reported\n"+info)
			info1={"State":state1,"Plate":plate1,"Color":color1,"Make":make1,"Model":model1,"Crime":crime1,"DateTime":date1,"Reporter":report1,"User":ip1}
			records.append(info1.copy())
			wks.append_row([state1,plate1,color1,make1,model1,crime1,date1,report1,ip1])
						
root=Tk()
root.title("User ID: "+str(ip1)+" | PPrS 1.0 | by pcondemand")
root.geometry("560x360")

label1=Label(root,text="Vehicle Plate #").place(x=20,y=5)
entry1=Entry(root,width=7)
entry1.place(x=140,y=7)

button1=Button(root,text="Search",command=search1,activebackground="green")
button1.place(x=240,y=0)

button2=Button(root,text="Clr",command=clr,activebackground="yellow")
button2.place(x=320,y=0)

button3=Button(root,text="Reset",command=reset,activebackground="red")
button3.place(x=375,y=0)

text1=Text(root,width=65,height=10)
text1.place(x=20,y=50)

label2=Label(root,text="State   Plate*        Color	Make             Model             Infraction*")
label2.place(x=20,y=240)

entry2=Entry(root,width=2)
entry2.place(x=20,y=260) # State

entry3=Entry(root,width=7)
entry3.place(x=68,y=260) # Plate

entry4=Entry(root,width=8)
entry4.place(x=136,y=260) # Color

entry5=Entry(root,width=10)
entry5.place(x=212,y=260) # Make

entry6=Entry(root,width=10)
entry6.place(x=302,y=260) # Model

entry7=Entry(root,width=15)
entry7.place(x=392,y=260) # Infraction

label3=Label(root,text="Email")
label3.place(x=20,y=306)

entry8=Entry(root)
entry8.place(x=64,y=304) #Email Entry

button4=Button(root,text="Report",activebackground="green",command=report)
button4.place(x=240,y=300) # Report button

button5=Button(root,text="Clear",command=clear,activebackground="yellow")
button5.place(x=360,y=300) # Clear button

root.mainloop()
