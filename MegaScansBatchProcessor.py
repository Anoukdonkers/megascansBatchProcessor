# comment info
# # = what to write here
# # // = ideas on what functions or code to use
# ! extra functionality
# $ information to copy
import maya.cmds as cmds
import os

# let user specify file path for foliage and 3d assets
# create UI class
class BatchProcessor(object):
    def __init__(self, window_width=420, window_height=500):
        self.window = cmds.window(title="Megascans batch Processor V1.14", h=window_height, w=window_width, s=False)
        self.c_layout = cmds.columnLayout(co=["left", 5], adjustableColumn=True)
        self.base_path = "Select the import path"
        self.export_path = "Select the export path"
        self.assetString_list = []
        self.plantString_list = []
        self.asset_export_dictionary = {}
        self.plant_export_dictionary = {}
        self.vertex_bool = False
        # self.maya_UIbg_color = [0.26,0.26,0.26]
        # self.maya_UIhl_color = [0.32, 0.51, 0.648]
        cmds.showWindow(self.window)

        # create UI elements
        # help button that navigates to github page
        cmds.text(l='<a href="https://github.com/Anoukdonkers/megascansBatchProcessor" style="color: #C8C8C8" style="text-decoration: none">help</a>',
                  h=20, p=self.c_layout, al="left", hl=True)
        cmds.separator(p=self.c_layout, st="none", h=5)
        cmds.text(label="Import assets from 'quixel bridge/Downloaded' location", h=20, p=self.c_layout, al="left")

        # create two checkboxes
        cmds.separator(p=self.c_layout, st="none", h=10)
        checkboxes = cmds.rowLayout(adjustableColumn=2, numberOfColumns=2, columnAttach2=["left","right"], co2=[140,140], p=self.c_layout)
        self.assetCheckbox = cmds.checkBox(label="3D assets", v=True, p =checkboxes)
        self.plantCheckbox = cmds.checkBox(label="Foliage", p=checkboxes)
        cmds.separator(p=self.c_layout, st="none", h=10)

        # create file path
        cmds.rowLayout(adjustableColumn=1, numberOfColumns=3, p=self.c_layout)
        cmds.text(label="Import file", h=20)
        self.txtfield = cmds.textField(w=300, text = self.base_path, en=False)
        cmds.button(label="Browser", c=self.open_file_dialog)

        # create import button
        cmds.rowLayout(adjustableColumn=1, numberOfColumns=1, p=self.c_layout)
        self.import_button = cmds.button(label="import", c=self.import_ms, en=False)
        cmds.separator(p=self.c_layout, h=20)

        # vertex gradient UI
        cmds.text(label="Create a vertex gradient for selected assets", h=20, p=self.c_layout, al="left")
        cmds.separator(p=self.c_layout, st="none", h=10)
        radiobuttons = cmds.rowLayout(adjustableColumn=1, numberOfColumns=2, columnAttach2=["left","right"], co2=[100,100], p=self.c_layout)
        cmds.radioButton(l="Top-Bottom", p=radiobuttons, onc=self.set_vertex_false,sl=True)
        cmds.radioButton(l="Bottom-Top", p=radiobuttons, onc=self.set_vertex_true)
        cmds.separator(p=self.c_layout, st="none", h=10)
        cmds.button(label="Create vertex gradient", c=self.create_vertex_gradient, p = self.c_layout, w=20)
        cmds.separator(p=self.c_layout, h=20)

        # export UI
        cmds.text(label="Export all assets to folder location", h=20, p=self.c_layout, al="left")
        # create file path
        cmds.rowLayout(adjustableColumn=1, numberOfColumns=3, p=self.c_layout)
        cmds.text(label="Export file", h=20)
        self.exporttxt = cmds.textField(w=300, text = self.export_path, en=False)
        cmds.button(label="Browser", c=self.export_file_dialog)
        cmds.rowLayout(adjustableColumn=1, numberOfColumns=1, p=self.c_layout)
        cmds.button(label="export", c=self.export_ms)
        cmds.separator(p=self.c_layout, h=20)

    def open_file_dialog(self, buttonbool):
        self.base_path = cmds.fileDialog2(fileMode=2, dialogStyle=1)[0]
        #if "Downloaded" not in self.base_path:
        last_letters= self.base_path[-10:]
        if last_letters != "Downloaded":
            cmds.confirmDialog(m="please select the 'quixel bridge\Downloaded' folder", t="Import path error", ma="left")
            self.base_path = "Please select the correct folder folder"
        cmds.textField(self.txtfield, e=True, text = self.base_path)
        if last_letters == "Downloaded":
            self.import_possible = True
            cmds.button(self.import_button, e=True, en=True)

    def export_file_dialog(self, buttonbool):
        self.export_path = cmds.fileDialog2(fileMode=2, dialogStyle=1)[0]
        cmds.textField(self.exporttxt, e=True, text=self.export_path)

    def set_vertex_false(self, ignore):
        self.vertex_bool=False

    def set_vertex_true(self, ignore):
        self.vertex_bool=True

    # check if file path has plant inside the string
    # ! maybe a button for 3d, 3dplants or both, and based on that it will load them
    # create boolean is plant
    def import_ms(self, ignore):
        # filter on 3d plants or 3D assets
        isAsset = cmds.checkBox(self.assetCheckbox, q=True, v=True)
        isPlant = cmds.checkBox(self.plantCheckbox, q=True, v=True)

        if "Downloaded" in self.base_path:
            print("Downloaded is in the name")
            if isAsset:
                print("is asset is true")
                self.import_assets(False)
            elif isPlant:
                print("is plant is true")
                self.import_plants(False)
            elif (isPlant and isAsset) == False:
                # ! create a popup box that says you have none selected
                cmds.confirmDialog(m="please select to import plants, assets or both", t="Import error")

            if isPlant and isAsset:
                print("You have selected both")
                self.import_plants(False)
                self.import_assets(False)
        else:
            cmds.confirmDialog(m="please select the 'quixel bridge\Downloaded' folder", t="Import path error")

    def import_assets(self, ignore):
        cmds.select(ado=True)

        # self.assetString_list = []
        # get only the assets folder
        self.asset_string = self.base_path + r"/3d"
        # get list of subfolders
        item_list = os.listdir(self.asset_string)
        for item in item_list:
            item_path = os.path.join(self.asset_string, item)
            if not os.path.isfile(item_path):
                self.assetString_list.append(item_path)
        for folder in self.assetString_list:
            item_list = os.listdir(folder)
            for item in item_list:
                section = item.split(".")
                if section[-1] == "fbx":
                    listOldAssets = cmds.ls(selection=True)
                    selectOldAssets = set(listOldAssets)

                    # import new asset
                    full_asset_path = os.path.join(folder, item)
                    cmds.file(full_asset_path, i=True)

                    cmds.select(ado=True)
                    listNewAssets = cmds.ls(selection=True)
                    selectNewAssets = set(listNewAssets)
                    tempSet = selectNewAssets-selectOldAssets
                    selectImportedAsset = list(tempSet)
                    imported_asset_name = cmds.ls(selectImportedAsset)
                    print(imported_asset_name)
                    if len(imported_asset_name) > 0:
                        self.asset_export_dictionary[imported_asset_name[0]]=full_asset_path

    def import_plants(self, ignore):
        # self.plantString_list = []
        print("You have selected 3D plant")
        # get only the assets folder
        self.plant_string = self.base_path + r"/3dplant"
        # get list of first subfolders
        first_subfolder_list = os.listdir(self.plant_string)
        for subfolder in first_subfolder_list:
            # make path with those first subfolders
            first_path = os.path.join(self.plant_string, subfolder)
            # get all the subfolders in those paths
            second_subfolder_list = os.listdir(first_path)
            for subfolder2 in second_subfolder_list:
                # create paths of the subfolders in subfolders
                final_path = os.path.join(first_path, subfolder2)
                # add these paths to the empty array
                if not os.path.isfile(final_path):
                    self.plantString_list.append(final_path)
            for folder in self.plantString_list:
                first_subfolder_list = os.listdir(folder)
                for item in first_subfolder_list:
                    section = item.split(".")
                    if section[-1] == "fbx":
                            # select all original assets
                            plistOldAssets = cmds.ls(selection=True)
                            pselectOldAssets = set(plistOldAssets)

                            full_plant_path = os.path.join(folder, item)
                            cmds.file(full_plant_path, i=True)

                            # get name of new asset in outliner
                            cmds.select(ado=True)
                            plistNewAssets = cmds.ls(selection=True)
                            pselectNewAssets = set(plistNewAssets)
                            ptempSet = pselectNewAssets - pselectOldAssets
                            pselectImportedAsset = list(ptempSet)
                            pimported_asset_name = cmds.ls(pselectImportedAsset)
                            print(pimported_asset_name)
                            if len(pimported_asset_name) > 0:
                                self.plant_export_dictionary[pimported_asset_name[0]] = full_plant_path

# apply vertex gradient to every fbx that is imported
# we need to select one object, get the vertex amount
# // to get only the geo and not a list you use the geo_name[0]
# // calculate top and bottom vertex // maybe there are other ideas tho on how to tackle this
# // function name_mesh.setVertexColor()
    def create_vertex_gradient(self, ignore):
        # create a string of all selections of the user
        allselections = cmds.ls(selection=True)
        print(allselections)
        # only do everything if the user has selected something
        if not allselections:
            cmds.confirmDialog(m="You have nothing selected", t="Selection error",
                               ma="left")
        else:
            cmds.makeIdentity(a=True)
            highest_vert = -10000.0

            for selection in allselections:
                # display vertex colors of selection
                cmds.setAttr(selection+".displayColors", 1)

                # select all vertices
                all_vertex = cmds.ls("{}.vtx[:]".format(selection),fl=True)

                for passHeight in all_vertex:
                    # get single vertex position
                    vertex_h = cmds.xform(passHeight,q=True,t=True)

                    #get highest vertex
                    if vertex_h[1] > highest_vert:
                        highest_vert = vertex_h[1]

                for vertex in all_vertex:
                    # get single vertex position
                    vertex_y = cmds.xform(vertex, q=True, t=True)
                    # color vertex
                    cmds.select(vertex)
                    if not self.vertex_bool:
                        cmds.polyColorPerVertex( rgb=(1.0/highest_vert*vertex_y[1], 1.0/highest_vert*vertex_y[1], 1.0/highest_vert*vertex_y[1]) )
                        cmds.select(allselections)
                    if self.vertex_bool:
                        old_rgb = 1.0 / highest_vert * vertex_y[1]
                        cmds.polyColorPerVertex(rgb=(1-old_rgb, 1-old_rgb, 1-old_rgb))
                        cmds.select(allselections)

# ! put the fbxes pivot at the bottom, and place that at 0

# Let the user pick a path, on where to save all these new fbxes
# these files need to be written with the same folder structure so that they will overwrite the
# existing fbxes
# // we will also use cmds.file for this has a exportAll=True function
    def export_ms(self, ignore):
        # make folder structure
        self.make_folder_structure(False)

    def make_folder_structure(self,ignore):
        cmds.select(ado=True)
        selectAll = cmds.ls( selection = True )
        # returns names of objects in scene
        object_name_list = (cmds.ls(sl=True))

        # add downloaded text to folder
        download_folder = os.path.join(self.export_path, "Downloaded")
        # print(download_folder)
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        # assets
        for afolder in self.assetString_list:
            asection = afolder.split(r"Downloaded")
            for apart in asection:
                asubpart = apart[1:]
                sub_asset_folders = os.path.join(download_folder, asubpart)
                if "3d" in sub_asset_folders:
                    if not os.path.exists(sub_asset_folders):
                        os.makedirs(sub_asset_folders)
        # export here
        for item in self.asset_export_dictionary:
            #print(item) # object name in outliner
            key_location = (self.asset_export_dictionary[item]) # export name
            temp_name = key_location.split(r"Downloaded")
            temp_name_subpart = temp_name[1]
            temp_name_final = temp_name_subpart[1:]
            new_location = os.path.join(download_folder, temp_name_final)
            cmds.select(item)
            cmds.file(new_location, es=True, type="FBX Export")

        # plants folders
        for pfolder in self.plantString_list:
            psection = pfolder.split(r"Downloaded")
            for ppart in psection:
                psubpart = ppart[1:]
                sub_plant_folders = os.path.join(download_folder, psubpart)
                if "3dplant" in sub_plant_folders:
                    if not os.path.exists(sub_plant_folders):
                        os.makedirs(sub_plant_folders)
        # export plants
        for item in self.plant_export_dictionary:
            #print(item) # object name in outliner
            pkey_location = (self.plant_export_dictionary[item]) # export name
            ptemp_name = pkey_location.split(r"Downloaded")
            ptemp_name_subpart = ptemp_name[1]
            ptemp_name_final = ptemp_name_subpart[1:]
            pnew_location = os.path.join(download_folder, ptemp_name_final)
            cmds.select(item)
            print(pnew_location)
            cmds.file(pnew_location, es=True, type="FBX Export")

BatchProcessor()
