import bpy
import os
filepath = bpy.data.filepath
directory = os.path.dirname(filepath)

# delete everything between running scripts, for dev use
bpy.ops.object.select_all(action='TOGGLE')
bpy.ops.object.select_all(action='TOGGLE')
bpy.ops.object.delete(use_global=False)


bpy.ops.wm.addon_enable(module='io_import_images_as_planes')
#bpy.ops.import_image.to_plane(files=[{'name':(os.path.join( directory , "rytm1_2048x2048.png"))}])


img = bpy.ops.import_image.to_plane(files=[{'name':(os.path.join( directory , "rytm1_2048x2048.png"))}])
bpy.context.object.location = (-0.002387,0.001423,0.06183)
bpy.context.object.scale = (0.353905,0.356265,0.356265)



scene = bpy.context.scene
# now add some light
lamp_data = bpy.data.lamps.new(name="lampa", type='POINT')  
lamp_object = bpy.data.objects.new(name="Lampicka", object_data=lamp_data)  
scene.objects.link(lamp_object)  
lamp_object.location = (0.088046, 0.071371, 2.27678)

# and now set the camera
cam_data = bpy.data.cameras.new(name="cam")  
cam_ob = bpy.data.objects.new(name="Kamerka", object_data=cam_data)  
scene.objects.link(cam_ob)  
cam_ob.location = (0, 0, 0.9)  
cam_ob.rotation_euler = (68.9842,-0.000008,-26.0696)  
cam = bpy.data.cameras[cam_data.name]  
cam.lens = 10



import bpy

verts = [(-1,  1,   0),
         ( 1,  1,   0),
         ( 2, -3,   0),
         (-2, -1,   0),
         (-1,  1.5, 1),
         ( 1,  1.5, 1),
        ]

# faces are a list of indices to each vertex from the above list
faces = [[0, 1, 2, 3], [0, 1, 5, 4]]

mesh = bpy.data.meshes.new(name="New Mesh")
mesh.from_pydata(verts, [], faces)
obj = bpy.data.objects.new('New object', mesh)
bpy.context.scene.objects.link(obj)




class trace_image:
    def __init__(self):
        empty = bpy.data.objects.new("trace_image", None)
        empty.location = (-0.340345, -0.177876, 0.061025)
        empty.scale = (0.681091,0.685632,0.685632)
        empty.color[3] = 0.304085
        scene = bpy.context.scene
        scene.objects.link(empty)
        scene.update()
        empty.empty_draw_type = 'IMAGE'
        img = bpy.data.images.load(os.path.join( directory , "rytm1_2048x2048.png"))
        empty.data = img

trace_image = trace_image()

class main_body():
    def __init__(self):
        inch = 0.0254
        self.dims = (13.4*inch,6.9*inch,2.4*inch)
        self.create_mat()
        self.create_main_body()

    def create_mat(self):
        mat = bpy.data.materials.new('Color1')
        mat.diffuse_color = (0, 0, 0.01)
        mat.diffuse_shader = 'LAMBERT'
        mat.diffuse_intensity = 1.0
        self.new_mat = bpy.data.materials['Color1']

    def create_main_body(self):
        main_body = bpy.ops.mesh.primitive_cube_add(view_align=False, enter_editmode=False, location=(0,0,0))
        bpy.context.object.scale = (self.dims)
        bpy.context.object.name = "main_body"
        #bpy.ops.object.modifier_add(type='SUBSURF')
        #bpy.context.object.modifiers["Subsurf"].levels = 2
        bpy.context.object.data.materials.append(self.new_mat)
        bpy.context.object.active_material.use_object_color = True
        
main_body = main_body()


class pads():
    def __init__(self):
        self.init_pos = [-0.2605,0.050351,0.06]
        self.create_mat()
        self.create_pad()
        self.pad = bpy.data.objects.get("pad_init")
        self.create_pads()
        objs = bpy.data.objects
        objs.remove(objs["pad_init"], True)

    def create_mat(self):
        mat_name = 'Pad_1'
        mat = bpy.data.materials.new(mat_name)
        bpy.data.materials[mat_name].use_nodes = True
        bpy.data.materials[mat_name].node_tree.nodes.new(type='ShaderNodeEmission')
        bpy.data.materials[mat_name].node_tree.nodes["Emission"].inputs[0].default_value = (0, 0.814053, 0.00291153, 1)
        inp = bpy.data.materials[mat_name].node_tree.nodes['Material Output'].inputs["Surface"]
        outp = bpy.data.materials[mat_name].node_tree.nodes["Emission"].outputs["Emission"]
        bpy.data.materials[mat_name].node_tree.links.new(inp,outp)
        self.new_mat = bpy.data.materials[mat_name]

    def create_pad(self):
        pad = bpy.ops.mesh.primitive_cube_add(view_align=False,enter_editmode=False, location = self.init_pos)
        bpy.context.object.scale = (0.01778,0.01778,0.00508)
        bpy.context.object.name = "pad_init"
        bpy.context.object.data.materials.append(self.new_mat)
        return bpy.context.object
    
    def create_pads(self):
        counter = 1
        rowcounter = 0
        colcounter = 0
        pad_y_pos = self.init_pos[1]
        while counter != 13:
            if colcounter == 4:
                colcounter = 0
                rowcounter += 1
                pad_y_pos = self.init_pos[1]+(-0.0545649*rowcounter)
            pad_x_pos = self.init_pos[0]+(0.0472651*colcounter)
            new_pad = self.pad.copy()
            new_pad.name = ('pad')
            new_pad.location = (pad_x_pos,pad_y_pos,self.init_pos[2])
            bpy.data.scenes[0].objects.link(new_pad)
            counter += 1
            colcounter += 1
        
        
pads = pads()

class bottom_buttons():
    def __init__(self):
        self.init_pos = (-0.308,-0.132,0.063)
        bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, view_align=False, enter_editmode=False,location=self.init_pos)
        bpy.context.object.scale = (0.014, 0.014, 0.0015)
        bpy.context.object.name = "button_init"
        self.create_bottom_buttons()
        
    def create_bottom_buttons(self):
        counter = 0
        while counter != 16:
            button = bpy.data.objects.get("button_init")
            new_button = button.copy()
            button_x_pos = self.init_pos[0]+(0.0382*counter)
            new_button.location = (button_x_pos,self.init_pos[1],self.init_pos[2])
            new_button.name = "button"
            bpy.data.scenes[0].objects.link(new_button)
            counter += 1

bottom_buttons = bottom_buttons()


class knobs():
    def __init__(self):
        self.init_pos = (-0.070415,0.117944,0.074186)
        self.scale = (0.009466, 0.009466, 0.015)
        self.create_knob()
        self.knob = bpy.data.objects.get("knob_init")
        self.knob.scale = self.scale

        main_knob = self.knob.copy()
        main_knob.location = (-0.289487,0.138046,self.init_pos[2])
        bpy.data.scenes[0].objects.link(main_knob)
        self.create_param_knobs()

    def create_knob(self):
        bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, view_align=False, enter_editmode=False,location=self.init_pos)
        bpy.context.object.scale = self.scale
        bpy.context.object.name = "knob_init"

    def create_param_knobs(self):
        counter = 1
        knob_x_location = 0.15765 
        knob_y_location = 0.114188
        while counter != 9:
            if counter == 5:
                knob_y_location += -0.05
                knob_x_location -= (0.0532818 * 4)
            param_knob  = self.knob.copy()
            param_knob.location = (knob_x_location,knob_y_location,self.init_pos[2])
            knob_x_location += 0.0532818
            bpy.data.scenes[0].objects.link(param_knob)
            counter += 1

knobs = knobs()

class small_buttons():
    def __init__(self):
        self.z_pos = 0.063561
        self.x_y_diff_count = (\
            (-0.068885,0.059996,0,2),\
            (-0.011,0.025067,0,2),\
            (-0.011,-0.008485,0,2),\
            (0.033121,-0.008485,0,2),\
            (0.064264,-0.008485,0,2),\
            (0.096664,-0.008485,0,2),\
            (0.064264,0.024667,0,2),\
            (-0.24407,0.112461,0.0278,6),\
            (-0.022792,-0.079691,0.0318,5),\
            (0.162415,0.008335,0.028,7)\
        )
        self.create_small_button()
        self.small_button = bpy.data.objects.get("small_button_init")
        self.clone_small_button_loops()

    def create_small_button(self):
         bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, view_align=False, enter_editmode=False,location=(0,0,0))
         bpy.context.object.scale = (0.006901, 0.006901, 0.002874)
         bpy.context.object.name = "small_button_init"  
        
    def clone_small_button_loops(self):
        for pos in self.x_y_diff_count:
            counter = 1
            but_x_location = pos[0]
            while counter != pos[3]:
                but = self.small_button.copy()
                but.location = (but_x_location,pos[1],self.z_pos)
                but_x_location += pos[2]
                bpy.data.scenes[0].objects.link(but) 
                counter += 1  
          
small_buttons = small_buttons()

class wide_buttons():
    def __init__(self):
        self.z_pos = 0.062694
        self.x_y_pos = (\
            (-0.06153,-0.046612,''),\
            (-0.31229,-0.060675,'left_button_bottom'),\
            (-0.31229,-0.004328,'left_button_middle'),\
            (-0.31229,0.052022,'left_button_top'),\
            (0.135,-0.061347,'rec_button'),\
            (0.173318,-0.061347,'play_button'),\
            (0.211154,-0.061347,'stop_button'),\
            (0.268486,-0.061347,'song_button'),\
            (0.305438,-0.061347,'chain_button'),\
            (0.301824,-0.132425,'page_button'),\
        )
        self.create_wide_button_mesh()
        self.wide_button = bpy.data.objects.get("wide_button_init")
        self.clone_wide_button()
        bpy.data.objects.remove(bpy.data.objects["wide_button_init"], True)
        

    def create_wide_button_mesh(self):
        bpy.ops.mesh.primitive_cube_add(view_align=False, enter_editmode=False,location=(0,0,0))
        bpy.context.object.scale = (0.011847, 0.004849, 0.00229)
        bpy.context.object.name = "wide_button_init"

        
    def clone_wide_button(self):
        for pos in self.x_y_pos:
            button = self.wide_button.copy()
            button.location = (pos[0],pos[1],self.z_pos)
            bpy.data.scenes[0].objects.link(button) 
        
wide_buttons = wide_buttons()

class leds():
    def __init__(self):
        self.z_pos = 0.06096
        self.x_y_diff_count = (\
            (0.135498,-0.039772,0,2),\
            (0.083901,-0.04,0,2),\
            (-0.068194,0.080124,0,2),\
            (0.083901,-0.051409,0,2),\
            (0.267032,-0.039772,0,2),\
            (0.305601,-0.039772,0,2),\
            (-0.023513,-0.062289,0.0318639,5),\
            (-0.306835, -0.107291, 0.038, 17),\
            (0.284346,-0.111262,0.0111663,5),\
            (0.160981,0.028403,0.028,7),\
            (-0.243758,0.132559,0.0284735,6)\
        )
        self.create_mat()
        self.create_led_mesh()
        self.led = bpy.data.objects.get("led_init")
        self.clone_led_loops()
        bpy.data.objects.remove(bpy.data.objects["led_init"], True)

    def create_mat(self):
        mat_name = 'Led_1'
        mat = bpy.data.materials.new(mat_name)
        bpy.data.materials[mat_name].use_nodes = True
        bpy.data.materials[mat_name].node_tree.nodes.new(type='ShaderNodeEmission')
        bpy.data.materials[mat_name].node_tree.nodes["Emission"].inputs[0].default_value = (0.748414, 0, 0, 1)
        inp = bpy.data.materials[mat_name].node_tree.nodes['Material Output'].inputs["Surface"]
        outp = bpy.data.materials[mat_name].node_tree.nodes["Emission"].outputs["Emission"]
        bpy.data.materials[mat_name].node_tree.links.new(inp,outp)
        self.new_mat = bpy.data.materials[mat_name]

    def create_led_mesh(self):
        bpy.ops.mesh.primitive_uv_sphere_add(size=1, view_align=False, enter_editmode=False,location=(0,0,0))
        bpy.context.object.scale = (0.002875, 0.002875, 0.002875)
        bpy.context.object.name = "led_init"
        bpy.context.object.data.materials.append(self.new_mat)

    def clone_led_loops(self):
        for pos in self.x_y_diff_count:
            counter = 1
            led_x_location = pos[0]
            while counter != pos[3]:
                led = self.led.copy()
                led.location = (led_x_location,pos[1],self.z_pos)
                led_x_location += pos[2]
                bpy.data.scenes[0].objects.link(led) 
                counter += 1       

leds = leds()