import bpy
import os

filepath = bpy.data.filepath
directory = os.path.dirname(filepath)



bpy.ops.object.select_all(action='TOGGLE')
bpy.ops.object.select_all(action='TOGGLE')

bpy.ops.object.delete(use_global=False)

inch = 0.0254
main_dims = (13.4,6.9,2.4)

def trace_image():
    empty = bpy.data.objects.new("trace_image", None)
    empty.location = (-0.343254, -0.177876, 0.061025)
    empty.scale = (0.689661,0.689661,0.689661)
    empty.color[3] = 0.304085
    scene = bpy.context.scene
    scene.objects.link(empty)
    scene.update()
    empty.empty_draw_type = 'IMAGE'
    img = bpy.data.images.load(os.path.join( directory , "rytm1_2048x2048.png"))
    empty.data = img
    return empty

trace_image = trace_image()


class main_body():
    def __init__(self, main_dims):
        self.len = main_dims[0] * inch
        self.wid = main_dims[1] * inch
        self.hei = main_dims[2] * inch 
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
        bpy.context.object.scale = (self.len, self.wid, self.hei)
        bpy.context.object.name = "main_body"
        #bpy.ops.object.modifier_add(type='SUBSURF')
        #bpy.context.object.modifiers["Subsurf"].levels = 2
        bpy.context.object.data.materials.append(self.new_mat)
        bpy.context.object.active_material.use_object_color = True
        return bpy.context.object
        


main_body = main_body(main_dims)


class pads():
    def __init__(self, main_dims):
        self.main_dims = main_dims
        self.len = .7 * inch
        self.wid = .7 * inch
        self.hei = .2 * inch

        self.init_pos = [-0.2605,0.050351,0.06]
        # self.init_pos = [-11.15*inch,4.775*inch,2.6*inch]
        self.create_pad()
        self.create_pads()
        

    

    def create_pad(self):
        pad = bpy.ops.mesh.primitive_cube_add(view_align=False,enter_editmode=False, location = self.init_pos)
        bpy.context.object.scale = (self.len, self.wid, self.hei)
        bpy.context.object.name = "pad_init"
        return bpy.context.object
    
    def create_pads(self):
        counter = 1
        pad = bpy.data.objects.get("pad_init")
        rowcounter = 0
        colcounter = 0
        pad_y_pos = self.init_pos[1]
        while counter != 13:
            if colcounter == 4:
                colcounter = 0
                rowcounter += 1
                pad_y_pos = self.init_pos[1]+(-0.0545649*rowcounter)
            
            pad_x_pos = self.init_pos[0]+(0.0472651*colcounter)
            
            pad2 = pad.copy()
            pad2.name = ('pad')
            pad2.location = (pad_x_pos,pad_y_pos,self.init_pos[2])
            bpy.data.scenes[0].objects.link(pad2)
            counter += 1
            colcounter += 1
        objs = bpy.data.objects
        objs.remove(objs["pad_init"], True)
        
pads = pads(main_dims)




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
        bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, view_align=False, enter_editmode=False,location=self.init_pos)
        bpy.context.object.scale = (0.009466, 0.009466, 0.012)
        bpy.context.object.name = "knob_init"
        self.knob = bpy.data.objects.get("knob_init")
        main_knob = self.knob.copy()
        main_knob.location = (-0.289487,0.138046,0.07419)
        bpy.data.scenes[0].objects.link(main_knob)
        self.create_param_knobs()

    def create_param_knobs(self):
        counter = 1
        knob_x_location = 0.15765 
        knob_y_location = 0.114188
        while counter != 9:
            if counter == 5:
                knob_y_location += -0.05
                knob_x_location -= (0.0532818 * 4)
            param_knob  = self.knob.copy()
            param_knob.location = (knob_x_location,knob_y_location,0.074186)
            knob_x_location += 0.0532818
            bpy.data.scenes[0].objects.link(param_knob)
            counter += 1

knobs = knobs()

class small_buttons():
    def __init__(self):
        self.init_pos = (-0.068885,0.059996,0.063561)
        bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, view_align=False, enter_editmode=False,location=self.init_pos)
        bpy.context.object.scale = (0.006901, 0.006901, 0.002874)
        bpy.context.object.name = "small_button_init"
        self.small_button = bpy.data.objects.get("small_button_init")
        self.top_small_buttons()
        self.start_stop_buttons()
        self.arrows()
        self.pattern_select()
        self.page_buttons()
        
    def start_stop_buttons(self):
        top_small = self.small_button.copy()
        top_small.location = (-0.011,0.025067,0.063561)
        bpy.data.scenes[0].objects.link(top_small)  
         
        top_small = self.small_button.copy()
        top_small.location = (-0.011,-0.008485,0.063561)
        bpy.data.scenes[0].objects.link(top_small)     
        
    def top_small_buttons(self):
        counter = 1
        but_x_pos = -0.24407
        while counter != 6:
            top_small = self.small_button.copy()
            top_small.location = (but_x_pos,0.112461,0.063561)
            but_x_pos += 0.0278
            bpy.data.scenes[0].objects.link(top_small)
            counter += 1
        
    def arrows(self):
        top_small = self.small_button.copy()
        top_small.location = (0.033121,-0.008485,0.063561)
        bpy.data.scenes[0].objects.link(top_small)
        
        top_small = self.small_button.copy()
        top_small.location = (0.064264,-0.008485,0.063561)
        bpy.data.scenes[0].objects.link(top_small)

        top_small = self.small_button.copy()
        top_small.location = (0.096664,-0.008485,0.063561)
        bpy.data.scenes[0].objects.link(top_small)  

        top_small = self.small_button.copy()
        top_small.location = (0.064264,0.024667,0.063561)
        bpy.data.scenes[0].objects.link(top_small)              
            
    def pattern_select(self):
        counter = 1
        but_x_pos = -0.022792
        while counter != 5:
            top_small = self.small_button.copy()
            top_small.location = (but_x_pos,-0.079691,0.063561)
            but_x_pos += 0.0318
            bpy.data.scenes[0].objects.link(top_small)
            counter += 1

    def page_buttons(self):
        counter = 1
        but_x_pos = 0.162415
        while counter != 7:
            top_small = self.small_button.copy()
            top_small.location = (but_x_pos,0.008335,0.063561)
            but_x_pos += 0.028
            bpy.data.scenes[0].objects.link(top_small)
            counter += 1

small_buttons = small_buttons()

class wide_buttons():
    def __init__(self):
        self.init_pos = (-0.06153,-0.046612,0.062694)
        bpy.ops.mesh.primitive_cube_add(view_align=False, enter_editmode=False,location=self.init_pos)
        bpy.context.object.scale = (0.011847, 0.004849, 0.00229)
        bpy.context.object.name = "wide_button_init"
        self.wide_button = bpy.data.objects.get("wide_button_init")
        
        left_button_bottom = self.wide_button.copy()
        left_button_bottom.location = (-0.31229,-0.060675,0.062694)
        bpy.data.scenes[0].objects.link(left_button_bottom)
        
        left_button_middle = self.wide_button.copy()
        left_button_middle.location = (-0.31229,-0.004328,0.062694)
        bpy.data.scenes[0].objects.link(left_button_middle)        
        
        left_button_top = self.wide_button.copy()
        left_button_top.location = (-0.31229,0.052022,0.062694)
        bpy.data.scenes[0].objects.link(left_button_top)
        
        
        rec_button = self.wide_button.copy()
        rec_button.location = (0.135,-0.061347,0.062694)
        bpy.data.scenes[0].objects.link(rec_button)
        
        play_button = self.wide_button.copy()
        play_button.location = (0.173318,-0.061347,0.062694)
        bpy.data.scenes[0].objects.link(play_button)
  
        stop_button = self.wide_button.copy()
        stop_button.location = (0.211154,-0.061347,0.062694)
        bpy.data.scenes[0].objects.link(stop_button)  
        
        song_button = self.wide_button.copy()
        song_button.location = (0.268486,-0.061347,0.062694)
        bpy.data.scenes[0].objects.link(song_button)          
        
        chain_button = self.wide_button.copy()
        chain_button.location = (0.305438,-0.061347,0.062694)
        bpy.data.scenes[0].objects.link(chain_button)
        
        page_button = self.wide_button.copy()
        page_button.location = (0.301824,-0.132425,0.062694)
        bpy.data.scenes[0].objects.link(page_button) 
        
wide_buttons = wide_buttons()


#bpy.ops.object.select_all(action='TOGGLE')
#bpy.ops.object.select_all(action='TOGGLE')

# bpy.ops.objects.resize(value=(1,1,1))

class leds():
    def __init__(self):
        led_init_pos = (0.135498,-0.039772,0.06096)
        bpy.ops.mesh.primitive_uv_sphere_add(size=1, view_align=False, enter_editmode=False,location=led_init_pos)
        bpy.context.object.scale = (0.002875, 0.002875, 0.002875)
        bpy.context.object.name = "led_init"
        self.led = bpy.data.objects.get("led_init")

        led = self.led.copy()
        led.location = (0.083901,-0.04,0.06096)
        bpy.data.scenes[0].objects.link(led)   
        
        led = self.led.copy()
        led.location = (-0.068194,0.080124,0.06096)
        bpy.data.scenes[0].objects.link(led) 
        
        led = self.led.copy()
        led.location = (0.083901,-0.051409,0.06096)
        bpy.data.scenes[0].objects.link(led)  



        led = self.led.copy()
        led.location = (0.267032,-0.039772,0.06096)
        bpy.data.scenes[0].objects.link(led)  


        led = self.led.copy()
        led.location = (0.305601,-0.039772,0.06096)
        bpy.data.scenes[0].objects.link(led)  


        counter = 1
        led_x_location = -0.023513
        while counter != 5:
            led = self.led.copy()
            led.location = (led_x_location,-0.062289,0.06096)
            led_x_location += 0.0318639
            bpy.data.scenes[0].objects.link(led) 
            counter += 1       

        led = self.led.copy()
        led.location = (-0.06164,-0.079991,0.06096)
        bpy.data.scenes[0].objects.link(led) 


        counter = 1
        led_x_location = -0.306835
        while counter != 17:
            led = self.led.copy()
            led.location = (led_x_location,-0.107291,0.06096)
            led_x_location += 0.038
            bpy.data.scenes[0].objects.link(led) 
            counter += 1 



        counter = 1
        led_x_location = 0.284346
        while counter != 5:
            led = self.led.copy()
            led.location = (led_x_location,-0.111262,0.06096)
            led_x_location += 0.0111663
            bpy.data.scenes[0].objects.link(led) 
            counter += 1 



        counter = 1
        led_x_location = 0.160981
        while counter != 7:
            led = self.led.copy()
            led.location = (led_x_location,0.028403,0.06096)
            led_x_location += 0.028
            bpy.data.scenes[0].objects.link(led) 
            counter += 1 


        counter = 1
        led_x_location = -0.243758
        while counter != 6:
            led = self.led.copy()
            led.location = (led_x_location,0.132559,0.06096)
            led_x_location += 0.0284735
            bpy.data.scenes[0].objects.link(led) 
            counter += 1 


leds = leds()



