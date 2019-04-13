import wingdbstub
wingdbstub.Ensure()

from functools import partial
import maya.cmds as cmds
import os.path

# global variables for folders and files
short_file_name = cmds.file (sceneName=True, shortName=True, q=True)
long_file_name = cmds.file (sceneName=True, expandName=True, q=True)
folder_path = long_file_name.replace(short_file_name, "") 
subfolder_path = folder_path + "_processed/"
locators_namespace = "new_pose"

pose_file_name = subfolder_path + "_temp_delta.ma" # TODO: to be deleted
pose_file_name_1 = subfolder_path + "_pose_1_delta.ma"
pose_file_name_2 = subfolder_path + "_pose_2_delta.ma"
pose_file_name_3 = subfolder_path + "_pose_3_delta.ma"
pose_file_name_4 = subfolder_path + "_pose_4_delta.ma"
naming_file = subfolder_path + "naming.txt"

# global lists
ctrl_names_glob =[] 
init_pose_locators_glob =[]  
new_pose_locators_glob =[] 
old_layer_name_string_glob = []
new_layer_name_string_glob = []
prefix1_glob =[]
prefix2_glob =[]
prefix3_glob =[]
prefix4_glob =[]
prefix_list = []
blendframes1 = []
blendframes2 = []
blendframes3 = []
blendframes4 = []
blendframes_list = []
ctrl_objs = 'obj_root', 'obj_spine', 'obj_head', 'obj_l_shoulder', 'obj_r_shoulder', 'obj_l_elbow', 'obj_r_elbow', 'obj_l_hand', 'obj_r_hand'


def object_selection_ui():
	
	cmds.window(title='Animset Pose Update - for MAYA 2018',sizeable=False)
	cmds.columnLayout("main_column")
	cmds.rowLayout(nc=2)
	button_save_naming = cmds.button(label="save", width=30, height=15, c= 'doint_nothing()' )
	button_load_naming = cmds.button(label="load", width=30, height = 15, c= 'doint_nothing()' ) 
	cmds.columnLayout (p='main_column')
	cmds.textFieldGrp('obj_root', width=500, adj=2, label='COM Ctrl Name', text ="", textChangedCommand = partial(paste_selected_name, 'obj_root') )		
	cmds.textFieldGrp('obj_spine', width=500, adj=2, label='Spine Ctrl Name', text = "", textChangedCommand = partial(paste_selected_name, 'obj_spine') )
	cmds.textFieldGrp('obj_head', width=500, adj=2, label='Head Ctrl Name', text = "", textChangedCommand = partial(paste_selected_name, 'obj_head') )
	cmds.textFieldGrp('obj_l_shoulder', width=500, adj=2, label='l_shoulder Ctrl Name', text = "", textChangedCommand = partial(paste_selected_name, 'obj_l_shoulder'))
	cmds.textFieldGrp('obj_r_shoulder', width=500, adj=2, label='r_shoulder Ctrl Name', text = "", textChangedCommand = partial(paste_selected_name, 'obj_r_shoulder'))
	cmds.textFieldGrp('obj_l_elbow', width=500, adj=2, label='l_elbow Ctrl Name', text = "", textChangedCommand = partial(paste_selected_name, 'obj_l_elbow'))
	cmds.textFieldGrp('obj_r_elbow', width=500, adj=2, label='r_elbow Ctrl Name', text = "", textChangedCommand = partial(paste_selected_name, 'obj_r_elbow'))
	cmds.textFieldGrp('obj_l_hand',width=500, adj=2, label='l_hand Ctrl Name', text = "", textChangedCommand = partial(paste_selected_name, 'obj_l_hand'))
	cmds.textFieldGrp('obj_r_hand',width=500, adj=2, label='r_hand Ctrl Name', text = "", textChangedCommand = partial(paste_selected_name, 'obj_r_hand'))
	cmds.rowLayout(nc=5)
	button_1 = cmds.button(label="Pick Initial Pose", width=100, c= 'doint_nothing()' ) 	
	button_2 = cmds.button(label="Pick New Pose", width=100, c= 'doint_nothing()')
	button_3 = cmds.button(label="Update Folder", width=100, c= 'doint_nothing()')
	button_4 = cmds.button(label="Update Current", width=100, c= 'doint_nothing()')	
	checkBox_chk = cmds.checkBox (label="attach hands", value = True)
	# layer override
	cmds.columnLayout (p='main_column')
	cmds.rowLayout(nc=3)
	checkBox_layer_rmv = cmds.checkBox (label="delete layer", value = False, en=True, width=80)
	cmds.textFieldGrp('old_layer_name', adj=2, label=' ', text ="", en=False, width=135, columnAttach2 = ('left','left'), columnOffset2 = (0,-150) )
	cmds.textFieldGrp('new_layer_name', adj=2, width=270, label='new layer ', text ="pose_update", en=True, columnAttach2 = ('left','left'), columnOffset2 = (0,-75) )
	# poses override
	cmds.columnLayout (p='main_column')
	cmds.rowLayout(nc=3)
	pose1_chk = cmds.checkBox (label="pose 1", value = False, en=True, width=60)
	cmds.textFieldGrp('file_prefix_1', label='file prefix detect: ', text ="idle", en=True,  adj=2, width=288, columnAttach2 = ('left','left'), columnOffset2 = (0,-50) )
	cmds.textFieldGrp('frames_pose_1', label='frames to blend Inital pose', text ="0", en=True, width=140, columnAttach2 = ('left','left'), columnOffset2 = (-50,-50))
	cmds.columnLayout (p='main_column')
	cmds.rowLayout(nc=3)
	pose2_chk = cmds.checkBox (label="pose 2", value = False, en=False, width=60)
	cmds.textFieldGrp('file_prefix_2', label='file prefix detect: ', text ="walk", en=True,  adj=2, width=288, columnAttach2 = ('left','left'), columnOffset2 = (0,-50) )
	cmds.textFieldGrp('frames_pose_2', label='frames to blend Inital pose', text ="0", en=True, width=140, columnAttach2 = ('left','left'), columnOffset2 = (-50,-50))
	cmds.columnLayout (p='main_column')
	cmds.rowLayout(nc=3)
	pose3_chk = cmds.checkBox (label="pose 3", value = False, en=False, width=60)
	cmds.textFieldGrp('file_prefix_3', label='file prefix detect: ', text ="jog", en=True,  adj=2, width=288, columnAttach2 = ('left','left'), columnOffset2 = (0,-50) )
	cmds.textFieldGrp('frames_pose_3', label='frames to blend Inital pose', text ="0", en=True, width=140, columnAttach2 = ('left','left'), columnOffset2 = (-50,-50))
	cmds.columnLayout (p='main_column')
	cmds.rowLayout(nc=3)
	pose4_chk = cmds.checkBox (label="pose 4", value = False, en=False, width=60)
	cmds.textFieldGrp('file_prefix_4', label='file prefix detect: ', text ="sprint", en=True,  adj=2, width=288, columnAttach2 = ('left','left'), columnOffset2 = (0,-50) )
	cmds.textFieldGrp('frames_pose_4', label='frames to blend Inital pose', text ="0", en=True, width=140, columnAttach2 = ('left','left'), columnOffset2 = (-50,-50))	

	cmds.button(button_1,  edit=True, c= partial (init_pose, button_1, button_2, pose1_chk, pose2_chk, pose3_chk, pose4_chk, checkBox_layer_rmv, checkBox_chk) )  # updating button call function to send buttons ID as argument to enable it
	cmds.button(button_2,  edit=True, en=False, c= partial (new_pose, button_1, button_2, pose1_chk, pose2_chk, pose3_chk, pose4_chk, checkBox_layer_rmv, checkBox_chk) ) # updating button call function to send buttons IDs
	cmds.button(button_3,  edit=True, c= partial (proc_folder, checkBox_chk, pose1_chk, pose2_chk, pose3_chk, pose4_chk, checkBox_layer_rmv) ) 	# updating button call function to send checkbox ID to read its value
	cmds.button(button_4,  edit=True, c= partial (proc_file,   checkBox_chk, pose1_chk, pose2_chk, pose3_chk, pose4_chk, checkBox_layer_rmv) ) 	# updating button call function to send checkbox ID to read its value
	
	cmds.button(button_save_naming,  edit=True, c= partial (save_naming_into_file) ) 	
	cmds.button(button_load_naming,  edit=True, c= partial (load_naming_from_file) ) 	
	
	cmds.checkBox (checkBox_layer_rmv, edit=True, changeCommand=partial (button_enabling_logic, button_1, button_2, pose1_chk, pose2_chk, pose3_chk, pose4_chk, checkBox_layer_rmv, checkBox_chk) )
	cmds.checkBox (pose1_chk, edit=True, changeCommand=partial (button_enabling_logic, button_1, button_2, pose1_chk, pose2_chk, pose3_chk, pose4_chk, checkBox_layer_rmv, checkBox_chk) )
	cmds.checkBox (pose2_chk, edit=True, changeCommand=partial (button_enabling_logic, button_1, button_2, pose1_chk, pose2_chk, pose3_chk, pose4_chk, checkBox_layer_rmv, checkBox_chk) )
	cmds.checkBox (pose3_chk, edit=True, changeCommand=partial (button_enabling_logic, button_1, button_2, pose1_chk, pose2_chk, pose3_chk, pose4_chk, checkBox_layer_rmv, checkBox_chk) )
	cmds.checkBox (pose4_chk, edit=True, changeCommand=partial (button_enabling_logic, button_1, button_2, pose1_chk, pose2_chk, pose3_chk, pose4_chk, checkBox_layer_rmv, checkBox_chk) )
	cmds.showWindow()
	
def update_ctrl_loc_names ():
	# declaring global vars and reseting them
	global ctrl_names_glob
	global init_pose_locators_glob
	global new_pose_locators_glob
	global old_layer_name_string_glob
	global new_layer_name_string_glob
	global short_file_name
	global long_file_name
	global folder_path
	global prefix1_glob
	global prefix2_glob
	global prefix3_glob
	global prefix4_glob
	global blendframes1
	global blendframes2
	global blendframes3
	global blendframes4
	global ctrl_objs
	ctrl_names_glob =[] 
	init_pose_locators_glob =[]  
	new_pose_locators_glob =[] 
	# update file name
	short_file_name = cmds.file (sceneName=True, shortName=True, q=True)
	long_file_name = cmds.file (sceneName=True, expandName=True, q=True)
	folder_path = long_file_name.replace(short_file_name, "") 		
	# initializing with strings	
	old_layer_name_string_glob = cmds.textFieldGrp ("old_layer_name", text=True, q=True)
	new_layer_name_string_glob = cmds.textFieldGrp ("new_layer_name", text=True, q=True)
	prefix1_glob = cmds.textFieldGrp ("file_prefix_1", text=True, q=True)
	prefix2_glob = cmds.textFieldGrp ("file_prefix_2", text=True, q=True)
	prefix3_glob = cmds.textFieldGrp ("file_prefix_3", text=True, q=True)
	prefix4_glob = cmds.textFieldGrp ("file_prefix_4", text=True, q=True)
	blendframes1 = cmds.textFieldGrp ("frames_pose_1", text=True, q=True)
	blendframes2 = cmds.textFieldGrp ("frames_pose_2", text=True, q=True)
	blendframes3 = cmds.textFieldGrp ("frames_pose_3", text=True, q=True)
	blendframes4 = cmds.textFieldGrp ("frames_pose_4", text=True, q=True)
	# initializing with ctrl names
	for ctrl_obj in ctrl_objs:
		ctrl_names_glob.append ( cmds.textFieldGrp (ctrl_obj, text=True, q=True) )
	# none empty check
	if '' in ctrl_names_glob:
		cmds.confirmDialog( title='Empty Ctrl Names', message='Please, add all ctrl names', button=['Ok'], defaultButton='Ok' )
		return False
	else:
		# list of locators for initial and new poses 
		init_pose_prefix = '_loc_init'  
		new_pose_prefix  = '_loc_new' 
		init_pose_locators_glob = [ init_pose_locator + init_pose_prefix for init_pose_locator in ctrl_names_glob ]
		new_pose_locators_glob =  [ new_pose_locator + new_pose_prefix  for new_pose_locator  in ctrl_names_glob ]		
		return True

# passting buttons ID as arguments    
def init_pose(button_1, button_2, pose1_chk, pose2_chk, pose3_chk, pose4_chk, checkBox_layer_rmv, checkBox_chk, *args):
	# initialize names
	if update_ctrl_loc_names ():
		# goto first frame and create 
		cmds.currentTime ( cmds.playbackOptions( minTime=True, q=True ) )
		create_delta_locators ()
		# aligning init pose locators to specified ctrl objects
		for ctrl_name, init_pose_locator in zip(ctrl_names_glob, init_pose_locators_glob): 
			cmds.delete (cmds.parentConstraint (ctrl_name, init_pose_locator))
		# set keyframe			
		cmds.setKeyframe ( init_pose_locators_glob, al = 'BaseAnimation')
		button_enabling_logic (button_1, button_2, pose1_chk, pose2_chk, pose3_chk, pose4_chk, checkBox_layer_rmv, checkBox_chk)

# passting buttons ID as arguments
def new_pose(button_1, button_2,pose1_chk, pose2_chk, pose3_chk, pose4_chk, checkBox_layer_rmv, checkBox_chk, *args):
	# reinitialize names to prevent user from changing it
	if update_ctrl_loc_names ():
		#cmds.button(button_2, edit=True, en=False)
		#cmds.button(button_1, edit=True, en=True)
		# alinging locators to the new pose
		for new_pose_locator, ctrl_name in zip (new_pose_locators_glob, ctrl_names_glob):
			cmds.delete (cmds.parentConstraint (ctrl_name, new_pose_locator))
		cmds.setKeyframe ( new_pose_locators_glob, al = 'BaseAnimation')
		# saving
		save_pose_file (pose1_chk, pose2_chk, pose3_chk, pose4_chk)
		button_enabling_logic (button_1, button_2, pose1_chk, pose2_chk, pose3_chk, pose4_chk, checkBox_layer_rmv, checkBox_chk)
		
def proc_folder(checkBox_chk, pose1_chk, pose2_chk, pose3_chk, pose4_chk, checkBox_layer_rmv,  *args):
	# checking file exists
	#if not os.path.isfile (pose_file_name):  #replace it with load_file fuction
	if not check_pose_files_by_settings (pose1_chk, pose2_chk, pose3_chk, pose4_chk):
		cmds.confirmDialog( title='No Pose File Created', message='Please, use Pick Poses buttons first', button=['Ok'], defaultButton='Ok' )
	else:
		if update_ctrl_loc_names ():
			target_files = cmds.getFileList( filespec="*.ma", folder= folder_path)
			# all files in same folder
			for target_file in target_files:
				# skipping existing files
				if os.path.isfile (subfolder_path + target_file):
					print ("Skipping " +(subfolder_path + target_file))
					continue
				# open file and merging data (skipping unresolved ref)
				cmds.file (folder_path+target_file, open=True, force=True, prompt=False)
				# collecting prefixes based on settings and recognizing them in the file
				update_prefix_list (pose1_chk, pose2_chk, pose3_chk, pose4_chk) 
				poses_indexes = recognize_file_prefixes (target_file, prefix_list) 
				# pose pasting params 
				frame_offset_1 =0
				frame_offset_2 =0
				if (poses_indexes[0]):
					frame_offset_1=blendframes_list[(poses_indexes[0]-1)]
				if (poses_indexes[1]):
					frame_offset_2=blendframes_list[(poses_indexes[1]-1)]
				else:
					frame_offset_2 = frame_offset_1					
				if not poses_indexes[0]:
					paste_poses_by_settings(1, 1, frame_offset_1, frame_offset_2, checkBox_layer_rmv, checkBox_chk)                        
				if (poses_indexes[0] and (not poses_indexes[1])):
					paste_poses_by_settings(poses_indexes[0], poses_indexes[0], frame_offset_1, frame_offset_2, checkBox_layer_rmv, checkBox_chk)                        						
				if (poses_indexes[0] and poses_indexes[1]):
					paste_poses_by_settings(poses_indexes[0], poses_indexes[1], frame_offset_1, frame_offset_2, checkBox_layer_rmv, checkBox_chk)                        
				# saving to new folder
				cmds.file (rename = (subfolder_path + target_file) ) # saving copy to new subfolder_path
				cmds.file (force =True, type ="mayaAscii", save =True)

def proc_file(checkBox_chk, pose1_chk, pose2_chk, pose3_chk, pose4_chk, checkBox_layer_rmv,  *args):
	# checking file exists
	#if not os.path.isfile (pose_file_name):  #replace it with load_file fuction
	if not check_pose_files_by_settings (pose1_chk, pose2_chk, pose3_chk, pose4_chk):
		cmds.confirmDialog( title='No Pose File Created', message='Please, use Pick Poses buttons first', button=['Ok'], defaultButton='Ok' )
	else:
		if update_ctrl_loc_names ():
			# collecting prefixes based on settings and recognizing them in the file
			update_prefix_list (pose1_chk, pose2_chk, pose3_chk, pose4_chk) 
			poses_indexes = recognize_file_prefixes (short_file_name, prefix_list) 
			# pose pasting params 				
			frame_offset_1 =0
			frame_offset_2 =0
			if (poses_indexes[0]):
				frame_offset_1=blendframes_list[(poses_indexes[0]-1)]
			if (poses_indexes[1]):
				frame_offset_2=blendframes_list[(poses_indexes[1]-1)]
			else:
				frame_offset_2 = frame_offset_1								
			if not poses_indexes[0]:
				paste_poses_by_settings(1, 1, frame_offset_1, frame_offset_2, checkBox_layer_rmv, checkBox_chk)                        
			if (poses_indexes[0] and (not poses_indexes[1])):
				paste_poses_by_settings(poses_indexes[0], poses_indexes[0], frame_offset_1, frame_offset_2, checkBox_layer_rmv, checkBox_chk)                        						
			if (poses_indexes[0] and poses_indexes[1]):
				paste_poses_by_settings(poses_indexes[0], poses_indexes[1], frame_offset_1, frame_offset_2, checkBox_layer_rmv, checkBox_chk)   


                     			
				
def create_delta_locators ():
	# creating init pose locators
	for init_pose_locator in init_pose_locators_glob:
		cmds.spaceLocator( p=(0, 0, 0), n=init_pose_locator)
		local_scale_list = ".localScaleX",".localScaleY" , ".localScaleZ" 
		for local_scale in local_scale_list: cmds.setAttr( (init_pose_locator+local_scale),0.01)
	# making itterator to skip the first element in parenting for init pose locators:
	iter_init_pose_locators = iter (init_pose_locators_glob)
	next (iter_init_pose_locators)
	for init_pose_locator in iter_init_pose_locators:
		cmds.parent (init_pose_locator, init_pose_locators_glob[0])
	# creating new pose locators
	for new_pose_locator in new_pose_locators_glob:
		cmds.spaceLocator( p=(0, 0, 0), n=new_pose_locator)
		local_scale_list = ".localScaleX",".localScaleY" , ".localScaleZ" 
		for local_scale in local_scale_list: cmds.setAttr( (new_pose_locator+local_scale),0.01)
	# making itterator to skip the first element in parenting for new pose locators:
	iter_new_pose_locators = iter (new_pose_locators_glob)
	next (iter_new_pose_locators)
	for new_pose_locator in iter_new_pose_locators:
		cmds.parent (new_pose_locator, new_pose_locators_glob[0])

def button_enabling_logic (init_pose_button, new_pose_button, pose1_chk, pose2_chk, pose3_chk, pose4_chk, checkBox_layer_rmv, checkBox_chk,  *args):
	#checking if pose files are exist	
	cmds.textFieldGrp('old_layer_name', edit=True, enable= (cmds.checkBox (checkBox_layer_rmv, value=True, q=True)))
	if update_ctrl_loc_names ():
		b1= cmds.checkBox (pose1_chk, value=True, q=True)
		b2= cmds.checkBox (pose2_chk, value=True, q=True)
		b3= cmds.checkBox (pose3_chk, value=True, q=True)
		b4= cmds.checkBox (pose4_chk, value=True, q=True)
		f1= os.path.isfile (pose_file_name_1)
		f2= os.path.isfile (pose_file_name_2)
		f3= os.path.isfile (pose_file_name_3)
		f4= os.path.isfile (pose_file_name_4)
		def init_button_switch ():
			cmds.button(init_pose_button, edit=True, en=True)
			cmds.button(new_pose_button,  edit=True, en=False)
		def new_button_switch ():
			cmds.button(init_pose_button, edit=True, en=False)
			cmds.button(new_pose_button,  edit=True, en=True)
	#default not prefixes case	
		if not b1:
			new_button_switch ()
		if (not b1) and (not (cmds.objExists(init_pose_locators_glob[0])) ):
			init_button_switch ()	
		# 1st checkbx
		if b1:
			cmds.checkBox (checkBox_chk, edit=True, value=False, en=False)
			if f1:
				init_button_switch ()
				cmds.checkBox (pose2_chk, en=True, edit=True)
			else:
				if cmds.objExists(init_pose_locators_glob[0]):
					new_button_switch ()
				cmds.checkBox (pose2_chk, en=False, value=False, edit=True)
				cmds.checkBox (pose3_chk, en=False, value=False, edit=True)
				cmds.checkBox (pose4_chk, en=False, value=False, edit=True)
		else:
			cmds.checkBox (checkBox_chk, edit=True, en=True)
		# 2nd checkbx
		if b1 and b2:
			if f1:
				if f2:
					init_button_switch ()
					cmds.checkBox (pose3_chk, en=True, edit=True)
				else:
					if cmds.objExists(init_pose_locators_glob[0]):
						new_button_switch ()
					cmds.checkBox (pose3_chk, en=False, value=False, edit=True)
					cmds.checkBox (pose4_chk, en=False, value=False, edit=True)
			else:
				cmds.checkBox (pose2_chk, en=False, value=False, edit=True)
				cmds.checkBox (pose3_chk, en=False, value=False, edit=True)
				cmds.checkBox (pose4_chk, en=False, value=False, edit=True)
		# 3d checkbx
		if b1 and b2 and b3:
			if f2:
				if f3:
					init_button_switch ()
					cmds.checkBox (pose4_chk, en=True, edit=True)
				else:
					if cmds.objExists(init_pose_locators_glob[0]):
						new_button_switch ()
					cmds.checkBox (pose4_chk, en=False, value=False, edit=True)
			else:
				cmds.checkBox (pose3_chk, en=False, value=False, edit=True)
				cmds.checkBox (pose4_chk, en=False, value=False, edit=True)
		# 4thd checkbx
		if b1 and b2 and b3 and b4:
			if f3:
				if f4:
					#init_button_switch ()
					pass
				else:
					if cmds.objExists(init_pose_locators_glob[0]):
						new_button_switch ()
			else:
				cmds.checkBox (pose4_chk, en=False, value=False, edit=True)	
	if not b3:
		cmds.checkBox (pose4_chk, en=False, value=False, edit=True)
	if not b2:
		cmds.checkBox (pose3_chk, en=False, value=False, edit=True)
		cmds.checkBox (pose4_chk, en=False, value=False, edit=True)
	if not b1:
		cmds.checkBox (pose2_chk, en=False, value=False, edit=True)
		cmds.checkBox (pose3_chk, en=False, value=False, edit=True)
		cmds.checkBox (pose4_chk, en=False, value=False, edit=True)
		
def save_pose_file (pose1_chk, pose2_chk, pose3_chk, pose4_chk, *args):
	cmds.sysFile( subfolder_path, makeDir=True )
	cmds.select (init_pose_locators_glob)
	cmds.select (new_pose_locators_glob, tgl=True)
	b1= cmds.checkBox (pose1_chk, value=True, q=True)
	b2= cmds.checkBox (pose2_chk, value=True, q=True)
	b3= cmds.checkBox (pose3_chk, value=True, q=True)
	b4= cmds.checkBox (pose4_chk, value=True, q=True)
	f1= os.path.isfile (pose_file_name_1)
	f2= os.path.isfile (pose_file_name_2)
	f3= os.path.isfile (pose_file_name_3)
	f4= os.path.isfile (pose_file_name_4)	
	pose_0_condition = (not b1) and (not b2) and (not b3) and (not b4) 
	pose_1_condition = (	b1) and (not b2) and (not b3) and (not b4)  #and (not f1)
	pose_2_condition = (	b1) and (	 b2) and (not b3) and (not b4)  and (f1) and (not f2)
	pose_3_condition = (	b1) and (    b2) and (    b3) and (not b4)  and (f1) and (    f2) and (not f3)
	pose_4_condition = (	b1) and (    b2) and (    b3) and (    b4)  and (f1) and (    f2) and (    f3) and (not f4)
	def save_procedure (name):
		cmds.file (rename = name)
		cmds.file (force =True, options ="v=0;", type ="mayaAscii", exportSelected =True)
		cmds.delete (init_pose_locators_glob)
		cmds.delete (new_pose_locators_glob)
		cmds.file (rename = long_file_name)
	if pose_0_condition or pose_1_condition:
		save_procedure(pose_file_name_1)
		return True
	if pose_2_condition:
		save_procedure(pose_file_name_2)
		return True
	if pose_3_condition:
		save_procedure(pose_file_name_3)
		return True
	if pose_4_condition:
		save_procedure(pose_file_name_4)
		return True
	return False
	
def load_pose_file (pose_file_index):
	def switched_pose_file (index):
		switcher = {
			0: False,
			1: pose_file_name_1,
			2: pose_file_name_2,
			3: pose_file_name_3,
			4: pose_file_name_4,
		}
		return switcher.get(index, False)
	if switched_pose_file (pose_file_index):	
	#managing fucking namespaces			
		cmds.file (switched_pose_file (pose_file_index), i =True, namespace = locators_namespace ) 
		global ctrl_names_glob
		global init_pose_locators_glob
		global new_pose_locators_glob
		update_ctrl_loc_names()
		init_pose_locators_glob = [locators_namespace + ':' + init_pose_locator for init_pose_locator in init_pose_locators_glob ]
		new_pose_locators_glob = [locators_namespace  + ':' + new_pose_locator  for new_pose_locator  in new_pose_locators_glob ]
		return True
	else:
		return False
	
def check_pose_files_by_settings (pose1_chk, pose2_chk, pose3_chk, pose4_chk, *args):
	b1= cmds.checkBox (pose1_chk, value=True, q=True)
	b2= cmds.checkBox (pose2_chk, value=True, q=True)	
	b3= cmds.checkBox (pose3_chk, value=True, q=True)	
	b4= cmds.checkBox (pose4_chk, value=True, q=True)	
	f1= os.path.isfile (pose_file_name_1)	
	f2= os.path.isfile (pose_file_name_2)	
	f3= os.path.isfile (pose_file_name_3)	
	f4= os.path.isfile (pose_file_name_4)
	def xnor (a,b):
		return not ((a and not b) or (not a and b))
	
	return (f1 and xnor(b2,f2) and xnor(b3,f3) and xnor(b4,f4)) #TODO: to rework in case when off but the pose exists
	
def paste_poses_by_settings (pose_enum_start, pose_enum_end, frame_offset_start, frame_offset_end, checkBox_layer_rmv, checkBox_chk, *args):	
	def layer_managment (checkBox_layer_rmv, *args):
		# deleting old layer
		if cmds.checkBox (checkBox_layer_rmv, value=True, q=True):
			if not old_layer_name_string_glob:
				cmds.confirmDialog( title='No Anim Layer Set', message='Please, Specify Animation Layer To Delete', button=['Ok'], defaultButton='Ok' )
			else:
				if cmds.animLayer (old_layer_name_string_glob, exists=True, q=True):
					cmds.delete (old_layer_name_string_glob)
		#creating new layer with Ctrls
		cmds.select (ctrl_names_glob) 
		if not cmds.animLayer (new_layer_name_string_glob, exists=True, q=True):
			cmds.animLayer (new_layer_name_string_glob, addSelectedObjects=True, selected=True, preferred=True)
		else:
			cmds.animLayer (new_layer_name_string_glob, edit=True, lock=False, mute=False, selected=True, preferred=True, addSelectedObjects=True)
		cmds.select (cl=True)	
	def pasting_procedure (frame):			
		# align COMs
		cmds.currentTime (frame)  	
		cmds.delete (cmds.pointConstraint (ctrl_names_glob[0], init_pose_locators_glob[0]))
		cmds.delete (cmds.orientConstraint (ctrl_names_glob[0], init_pose_locators_glob[0], skip=['x','z']))
		cmds.delete (cmds.pointConstraint (ctrl_names_glob[0], new_pose_locators_glob[0]))
		cmds.delete (cmds.orientConstraint (ctrl_names_glob[0], new_pose_locators_glob[0], skip=['x','z']))
		# parenting ctrls to init pose locators
		iter_ctrl_names = iter (ctrl_names_glob) # iterator to skip parenting roots
		iter_init_pose_locators = iter (init_pose_locators_glob)
		next (iter_ctrl_names)
		next (iter_init_pose_locators)
		for ctrl_name, init_pose_locator in zip(iter_ctrl_names,iter_init_pose_locators):
			#cmds.parentConstraint (init_pose_locator, ctrl_name, maintainOffset=True, name = "init_pose_contraint_") # adding labeled constraints to delete them later
			# deleting non-referenced constraints
			constr_list = cmds.listConnections (ctrl_name,  type="constraint")
			delete_constr_list = []
			if constr_list:
				for single_constr in constr_list:
					if not cmds.referenceQuery (single_constr,isNodeReferenced=True):
						delete_constr_list.append (single_constr)
			cmds.delete (delete_constr_list, cn=True)
			# checking unlocked attr before constrainting
			locked_attr = cmds.listAttr (ctrl_name, locked = True)
			if not any ("translate" in attr_test for attr_test in locked_attr):
				cmds.pointConstraint (init_pose_locator, ctrl_name, maintainOffset=True, name = "init_pos_contraint_")
			if not any ("rotate" in attr_test for attr_test in locked_attr):
				cmds.orientConstraint (init_pose_locator, ctrl_name, maintainOffset=True, name = "init_rot_contraint_")
		# aling init locators to new ones
		cmds.cutKey (init_pose_locators_glob) # deleting keys from 
		for init_pose_locator, new_pose_locator in zip(init_pose_locators_glob, new_pose_locators_glob):
			cmds.delete (cmds.parentConstraint (new_pose_locator, init_pose_locator))
		# keying ctrls and deleting constraints
		cmds.setKeyframe ( ctrl_names_glob, al = new_layer_name_string_glob)
		#cmds.delete (cmds.ls ("init_pose_contraint_") )  #deleting  constrants
		cmds.delete (cmds.ls ("init_pos_contraint_") )
		cmds.delete (cmds.ls ("init_rot_contraint_") )
	def l_hand_to_r_hand_const (checkBox_chk, *args):
		# constraint L_Hand to R_Hand if checked
		if cmds.checkBox (checkBox_chk, value=True, q=True):  # reading checkbox value
			constr_list = cmds.listConnections (ctrl_names_glob [7], type='parentConstraint')  # listing existing parent constraints on hand
			if constr_list:
				for single_constr in constr_list:
					test_obj = cmds.parentConstraint (single_constr, targetList=True, q=True)
					if ctrl_names_glob[8] not in test_obj:  # check of existing constraints
						cmds.parentConstraint (ctrl_names_glob [8], ctrl_names_glob [7], maintainOffset=True, name = "l_hand_to_r_hand_ParentCnst")
			else:
				cmds.parentConstraint (ctrl_names_glob [8], ctrl_names_glob [7], maintainOffset=True, name = "l_hand_to_r_hand_ParentCnst")
	# Start
	layer_managment (checkBox_layer_rmv)
	# setting zero keys at start and end
	cmds.currentTime ( cmds.playbackOptions( minTime=True, q=True ))
	cmds.setKeyframe ( ctrl_names_glob, al = new_layer_name_string_glob)
	cmds.currentTime ( cmds.playbackOptions( maxTime=True, q=True ))
	cmds.setKeyframe ( ctrl_names_glob, al = new_layer_name_string_glob)	
	# setting zero keys in the middle if specified
	if (int(frame_offset_start) != 0):
		cmds.currentTime ( (cmds.playbackOptions( minTime=True, q=True )) + int (frame_offset_start ))
		cmds.setKeyframe ( ctrl_names_glob, al = new_layer_name_string_glob)
	if (int(frame_offset_end) != 0):
		cmds.currentTime ( (cmds.playbackOptions( maxTime=True, q=True )) - int (frame_offset_end ))
		cmds.setKeyframe ( ctrl_names_glob, al = new_layer_name_string_glob)
	if pose_enum_start:
		load_pose_file (pose_enum_start)
		pasting_procedure ( cmds.playbackOptions( minTime=True, q=True ) )			
		cmds.delete (init_pose_locators_glob)
		cmds.delete (new_pose_locators_glob)
		# deleting namespace
		cmds.namespace( set=':' )
		cmds.namespace( rm=locators_namespace, deleteNamespaceContent = True )		
		cmds.currentTime ( cmds.playbackOptions( minTime=True, q=True ) ) #updating viewport		
	if pose_enum_end: # always runs to ensure offset on character turn
		load_pose_file (pose_enum_end)
		pasting_procedure ( cmds.playbackOptions( maxTime=True, q=True ) )
		cmds.delete (init_pose_locators_glob)
		cmds.delete (new_pose_locators_glob)	
		# deleting namespace
		cmds.namespace( set=':' )
		cmds.namespace( rm=locators_namespace, deleteNamespaceContent = True )		
		cmds.currentTime ( cmds.playbackOptions( minTime=True, q=True ) ) #updating viewport		
	if cmds.checkBox (checkBox_chk, value=True, q=True):
		cmds.currentTime (cmds.playbackOptions( minTime=True, q=True ))
		l_hand_to_r_hand_const (checkBox_chk)
		
# returns prefix indexes in list in  the file name	
def recognize_file_prefixes (file_name, prefix_list):
	result_first_prefix = False
	result_last_prefix = False
	for index, first_prefix in enumerate(prefix_list):
		if first_prefix in file_name:
			result_first_prefix = index+1
			pre_cut = file_name [:file_name.find(first_prefix)]  # spliting file name in substring before the prefix
			post_cut = (file_name [file_name.find(first_prefix):]).replace(first_prefix,"")  # spliting file name in substring and excluding prefix
			for second_index, next_prefix in enumerate(prefix_list):
				if next_prefix in pre_cut:
					result_first_prefix = second_index+1
					result_last_prefix = index+1
					break
				if next_prefix in post_cut:
					result_first_prefix = index+1
					result_last_prefix = second_index+1                                   
					break                       
	return result_first_prefix, result_last_prefix
	
def update_prefix_list (pose1_chk, pose2_chk, pose3_chk, pose4_chk, *args):
	global prefix_list
	global blendframes_list
	prefix_list = []
	blendframes_list = []
	if cmds.checkBox (pose1_chk, value=True, q=True):
		prefix_list.append (prefix1_glob)
	if cmds.checkBox (pose2_chk, value=True, q=True):
		prefix_list.append (prefix2_glob)
	if cmds.checkBox (pose3_chk, value=True, q=True):
		prefix_list.append (prefix3_glob)
	if cmds.checkBox (pose4_chk, value=True, q=True):
		prefix_list.append (prefix4_glob)
	blendframes_list.append (blendframes1)
	blendframes_list.append (blendframes2)
	blendframes_list.append (blendframes3)
	blendframes_list.append (blendframes4)

def doint_nothing():
	print ("Doing Nothing")
	
def paste_selected_name(text_field, *args):
	selected_obj = cmds.ls (sl=True)
	if selected_obj :
		cmds.textFieldGrp (text_field, edit=True, text= selected_obj[0].encode('ascii','ignore'))  # weird convertion of unicode to string
	
def save_naming_into_file (*args):
	if update_ctrl_loc_names ():
		cmds.sysFile( subfolder_path, makeDir=True )
		file = open (naming_file, "w+")
		for i, line in enumerate (ctrl_names_glob):
			file.write (line+ "\r\n")
		file.close()
	else:
		print ("Doing Nothing")
	
def load_naming_from_file (*args):
	cmds.select(clear=True)
	if os.path.isfile (naming_file):
		file = open (naming_file, "r")
		file_lines = file.readlines()
		file.close()			
		for file_line, ctrl_obj in zip (file_lines, ctrl_objs):
			cmds.textFieldGrp (ctrl_obj,  edit = True, text=(file_line.replace("\r\n",''))) 
		update_ctrl_loc_names ()
	else: 	
		print ("no naming file found")

    
object_selection_ui() 
