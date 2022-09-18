import sys
import mujoco as mj
import glfw
from glfw_fp import GlfwFixedPipelineRenderer
import imgui
import OpenGL.GL as gl


def main():
    cam = mj.MjvCamera()
    opt = mj.MjvOption()
    print(dir(opt))

    glfw.init()

    window = glfw.create_window(600, 450, "Demo", None, None)
   
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    mj.mjv_defaultCamera(cam)
    mj.mjv_defaultOption(opt)

    xml_path = "hello.xml"
    model = mj.MjModel.from_xml_path(xml_path)
    data = mj.MjData(model)

    scene = mj.MjvScene(model, maxgeom=10000)
    context = mj.MjrContext(model, mj.mjtFontScale.mjFONTSCALE_150.value)
    #gl.glActiveTexture(gl.GL_TEXTURE0)

    imgui.create_context()
    impl = GlfwFixedPipelineRenderer(window)
    print(' ,',dir(impl.render))

    while not glfw.window_should_close(window):
        glfw.poll_events()

        simstart = data.time

        while (data.time - simstart < 1.0/60.0):
            mj.mj_step(model, data)

        #viewport = mj.MjrRect(0, 0, 0, 0)
        #glfw.get_framebuffer_size(window)
        viewport = mj.MjrRect(0, 0, 1200, 900)

        #mj.mjv_updateScene(model, data, opt, None, cam, 0, scene)
        mj.mjv_updateScene(model, data, opt, None, cam, mj.mjtCatBit.mjCAT_ALL.value, scene)
        
        #record_values = glhelper.record()
        mj.mjr_render(viewport, scene, context)
        #glhelper.restore(record_values)
        gl.glDisable(gl.GL_LIGHTING)

        gl.glActiveTexture(gl.GL_TEXTURE0)
        imgui.new_frame()

        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):

                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", 'Cmd+Q', False, True
                )

                if clicked_quit:
                    exit()

                imgui.end_menu()
            imgui.end_main_menu_bar()

        impl.process_inputs()
        imgui.begin("Custom window", False)
        imgui.text("Bar")
        imgui.text_ansi("B\033[31marA\033[mnsi ")
        imgui.text_ansi_colored("Eg\033[31mgAn\033[msi ", 0.2, 1., 0.)
        imgui.extra.text_ansi_colored("Eggs", 0.2, 1., 0.)
        if(imgui.button("aaaa")):
            print('click button')
        
        imgui.end()

        imgui.render()
        impl.render(imgui.get_draw_data())

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()