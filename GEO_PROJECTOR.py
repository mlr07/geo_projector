########################
### GEO PROJECTOR v3 ###
########################

# Matt Rhoads, 11/1/18

# Simple GUI calculator that projects casing points and landings. Outputs may be saved to .csv for future reference.  

import PySimpleGUI as sg
import csv

# Functions to calculate and compare projections.
def proj_land(set_depth, obj_mark, off_mark, off_tot):
    thick = off_tot-off_mark
    t_thick = str(thick)
    p_tot = abs(thick+obj_mark)
    t_tot = str(p_tot)
    p_bot = abs(p_tot+set_depth)
    t_bot = str(p_bot)
    proj_land = [p_tot, p_bot, t_tot, t_bot, t_thick]
    return proj_land

def comp_land(p_tot, p_bot, p_icp):
    if  p_icp <= p_bot and p_icp >= p_tot: 
        f_tot = abs(p_tot-p_icp)
        f_bot = abs(p_bot-p_icp)
        l_tot = str(f_tot)+" FT below TOT"
        l_bot = str(f_bot)+" FT above BOT"
    elif p_icp >= p_bot and p_icp >= p_tot: 
        f_tot = abs(p_tot-p_icp)
        f_bot = abs(p_bot-p_icp)
        l_tot = str(f_tot)+" FT below TOT"
        l_bot = str(f_bot)+" FT below BOT"
    elif p_icp <= p_bot and p_icp <= p_tot: 
        f_tot = abs(p_tot-p_icp)
        f_bot = abs(p_bot-p_icp)
        l_tot = str(f_tot)+" FT above TOT"
        l_bot = str(f_bot)+" FT above BOT"
    comp_land = [f_tot, f_bot, l_tot, l_bot]
    return comp_land

def proj_icp(set_depth,obj_mark,off_mark,off_fm):
	thick = off_fm-off_mark
	p_fm = thick+obj_mark
	p_icp = p_fm+set_depth
	t_thick = str(thick)
	t_fm = str(p_fm)
	t_icp = str(p_icp)
	proj_icp = [thick, p_fm, p_icp, t_thick, t_fm, t_icp]
	return proj_icp

def comp_icp(plan_icp, proj_icp):
	diff=plan_icp-proj_icp
	if diff < 0:
		t_diff = str(abs(diff))
		comp = t_diff+" FT below plan" 
	elif diff > 0:
		t_diff = str(abs(diff))
		comp = t_diff+" FT above plan"
	else:
		comp = 'On plan'
	comp_icp = [diff, t_diff, comp]
	return comp_icp

def check_output_log(file_name, mode):
	try:
		open_file = open(file_name).close()
	except IOError:
		if mode_return == "Project ICP":
			head = ["THICKNESS", "PROJ_FM_TOP", "PROJ_ICP", "PLAN_vs_PROJ"]
		elif mode_return == "Project Landing":
			head = ["THICKNESS", "PROJ_TOT", "PROJ_BOT", "LP_POS_TOT", "LP_POS_BOT" ]
		with open(file_name, "w", newline = "") as csv_file:
			csv.writer(csv_file).writerow(head) 
			csv_file.close() 

def append_output(file_name, output_data):
	with open(file_name, "a", newline = "" ) as csv_file:
		csv.writer(csv_file).writerow(output_data)			
		csv_file.close() 						

# Select projection mode: ICP or Landing.
mode = sg.FlexForm("Select Mode", font=("arial", "14"))

mode_rows = [
			 [sg.SimpleButton("Project ICP", button_color=("white","dark red"), size = (14,1))],
			 [sg.SimpleButton("Project Landing", button_color=("white","dark green"), size = (14,1))]
			]

button = mode.LayoutAndRead(mode_rows)

mode_return = button[0]

# ICP Projection Mode
if mode_return == "Project ICP":
	icp = sg.FlexForm('Project ICP', font=("arial", "14"))
	
	icp_rows = [
				[sg.Text("ICP Plan:", size = (16,1)), sg.InputText(size = (6,1), key = "p_icp"), sg.Text("TVD")],
				[sg.Text("Set depth (+/-):", size = (16,1)), sg.InputText(size = (6,1), key = "set_depth"), sg.Text("FT")],
				[sg.Text("Objective Marker:", size = (16,1)), sg.InputText(size = (6,1), key = "obj_mark"), sg.Text("TVD")],
				[sg.Text("Offset Marker:", size = (16,1)), sg.InputText(size = (6,1),key = "off_mark"), sg.Text("TVD")],
				[sg.Text("Offset Top:", size = (16,1)), sg.InputText(size = (6,1), key = "off_fm"), sg.Text("TVD")],
				[sg.Text("-"*70, size = (30,1), text_color = "black")],
				[sg.Text("", size = (30,1),key = "state")],
				[sg.Text("-"*70, size = (30,1), text_color = "black")],
				[sg.Text("Thickness: ", size = (16,1)), sg.Text("", size =(6,1), key = "thick"), sg.Text("TVD")],
				[sg.Text("Projected Top: ", size = (16,1)), sg.Text("", size =(6,1), key = "p_fm_top"), sg.Text("TVD")],
				[sg.Text("Projected ICP: ", size = (16,1)), sg.Text("", size =(6,1), key = "proj_icp"), sg.Text("TVD")],
				[sg.Text("Plan vs Projected: ", size = (16,1)), sg.Text("", size =(16,1), key = "comp_icp")],
				[sg.Text("-"*70, size = (30,1), text_color = "black")],
				[sg.SaveAs(button_text = "Save As", size = (9,1), button_color = ("white", "dark blue"), key = "input"), sg.ReadFormButton("Project", size = (9,1), button_color=("white", "dark green"), bind_return_key=True)]
			   ]

	icp.Layout(icp_rows)

	while True:
		button, values = icp.Read()  

		if button is not None:
			icp.FindElement("p_icp").Update(values["p_icp"])
			icp.FindElement("set_depth").Update(values["set_depth"])
			icp.FindElement("obj_mark").Update(values["obj_mark"])
			icp.FindElement("off_mark").Update(values["off_mark"])
			icp.FindElement("off_fm").Update(values["off_fm"])
			icp.FindElement("input").Update(values["input"])
			save = values.pop("input", None)

			try:
				values = {k:int(v) for (k,v) in values.items()}
				icp_proj = proj_icp(values["set_depth"], values["obj_mark"], values["off_mark"],values["off_fm"])
				icp_comp = comp_icp(values["p_icp"], icp_proj[2])
				display = [icp_proj[3],icp_proj[4],icp_proj[5], icp_comp[2]]
				state = "COMPLETE" 

			except:
				display = ["NULL", "NULL", "NULL", "NULL", "NULL"]
				state = "ERROR"
			
			if save != "" and state == "COMPLETE": 
				check_output_log(save, mode)
				append_output(save, display)
				u_state = "PROJECTION COMPLETE"
				t_color = "blue"
				b_text = "Saved"

			elif save == "" and state == "COMPLETE":
				u_state = "PROJECTION COMPLETE"
				t_color = "blue"
				b_text = "Save As"

			elif state == "ERROR":
				u_state = "ERROR: ENTER WHOLE INTEGERS"
				t_color = "red"
				b_text = "Not Saved"
 
			icp.FindElement('thick').Update(display[0])
			icp.FindElement('p_fm_top').Update(display[1])
			icp.FindElement('proj_icp').Update(display[2])
			icp.FindElement('comp_icp').Update(display[3])
			icp.FindElement('state').Update(u_state, text_color = t_color)
			icp.FindElement('input').Update(text = b_text)

		else:
			break

# Laninding Projection Mode
elif mode_return == "Project Landing":
	lp = sg.FlexForm('Project Landing', font=("arial", "14"))

	lp_rows = [
				[sg.Text("Landing Point:", size = (16 ,1)), sg.InputText(size = (6,1), key = "p_icp"), sg.Text("TVD")],
				[sg.Text("Window Size:", size = (16,1)), sg.InputText(size = (6,1), key = "set_depth"), sg.Text("FT")],
				[sg.Text("Objective Marker:", size = (16,1)), sg.InputText(size = (6,1), key = "obj_mark"), sg.Text("TVD")],
				[sg.Text("Offset Marker:", size = (16,1)), sg.InputText(size = (6,1),key = "off_mark"), sg.Text("TVD")],
				[sg.Text("Offset TOT:", size = (16,1)), sg.InputText(size = (6,1), key = "off_tot"), sg.Text("TVD")],
				[sg.Text("-"*70, size = (30,1), text_color = "black")],
				[sg.Text("", size = (30,1),key = "state")],
				[sg.Text("-"*70, size = (30,1), text_color = "black")],
				[sg.Text("Thickness: ", size = (16,1)), sg.Text("", size =(6,1), key = "thick"), sg.Text("TVD")],
				[sg.Text("TOT Projection: ", size = (16,1)), sg.Text("", size =(6,1), key = "proj_tot"), sg.Text("TVD")],
				[sg.Text("BOT Projection: ", size = (16,1)), sg.Text("", size =(6,1), key = "proj_bot"), sg.Text("TVD")],
				[sg.Text("LP Positon: ", size = (16,1)), sg.Text("", size =(16,1), key = "pos_tot")],
				[sg.Text("", size = (16,1)), sg.Text("", size =(16,1), key = "pos_bot")],
				[sg.Text("-"*70, size = (30,1), text_color = "black")],
				[sg.SaveAs(button_text = "Save As", size = (9,1), button_color = ("white", "dark blue"), key = "input"), sg.ReadFormButton("Project", size = (9,1), button_color=("white", "dark green"), bind_return_key=True)]
			   ]

	lp.Layout(lp_rows) 
	
	while True:
		button, values = lp.Read()  
		
		if button is not None:
			lp.FindElement("p_icp").Update(values["p_icp"])
			lp.FindElement("set_depth").Update(values["set_depth"])
			lp.FindElement("obj_mark").Update(values["obj_mark"])
			lp.FindElement("off_mark").Update(values["off_mark"])
			lp.FindElement("off_tot").Update(values["off_tot"])
			save = values.pop("input")

			try:
				values = {k:int(v) for (k,v) in values.items()}
				obj_proj = proj_land(values["set_depth"], values["obj_mark"], values["off_mark"], values["off_tot"])
				obj_comp = comp_land(obj_proj[0], obj_proj[1], values["p_icp"])
				display = [obj_proj[4], obj_proj[2], obj_proj[3], obj_comp[2], obj_comp[3]]
				state = "COMPLETE"

			except:
				display = ["NULL", "NULL", "NULL", "NULL", "NULL"]
				state = "ERROR"
			
			if save != "" and state == "COMPLETE": 
				check_output_log(save, mode)
				append_output(save, display)
				u_state = "PROJECTION COMPLETE"
				t_color = "blue"
				b_text = "Saved"

			elif save == "" and state == "COMPLETE":
				u_state = "PROJECTION COMPLETE"
				t_color = "blue"
				b_text = "Save As"

			elif state == "ERROR":
				u_state = "ERROR: ENTER WHOLE INTEGERS"
				t_color = "red"
				b_text = "Not Saved"

			lp.FindElement('thick').Update(display[0])
			lp.FindElement('proj_tot').Update(display[1])
			lp.FindElement('proj_bot').Update(display[2])
			lp.FindElement('pos_tot').Update(display[3])
			lp.FindElement('pos_bot').Update(display[4])
			lp.FindElement('state').Update(u_state, text_color = t_color)
			lp.FindElement('input').Update(text = b_text)

		else:
			break

