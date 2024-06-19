import glfw
import moderngl
import numpy as np


import moderngl_window as glw
import numpy as np

def check_if_released(buff) -> bool:
    return type(buffer.mglo) == moderngl._moderngl.InvalidObject


# Versão mais recente do OpenGL
GLSL_VERSION = 460 
GL_VERSION   = (4,6)

# Retorna a classe Window
# Usa 'pyglet' como classe de contexto padrão
WindowClass = glw.get_local_window_cls() 


window = WindowClass\
(
    size=(512, 512), fullscreen=False, title='ACH2117',
    resizable=False, vsync=True, gl_version=GL_VERSION
)

# Instancia objeto de contexto
ctx = window.ctx
glw.activate_context(window, ctx=ctx)

# Configura o modo de Garbage Collection do contexto
ctx.gc_mode = "context_gc"

window.clear()
window.swap_buffers()


# Inicializa Shaders
prog = ctx.program(

    vertex_shader=\
    f"""

        #version {GLSL_VERSION}

        in vec2 in_vert;
        in vec3 in_color;
        out vec3 v_color;

        void main()
        {{
            v_color = in_color;
            gl_Position = vec4(in_vert, 0.0, 1.0);
        }}

    """,

    fragment_shader=\
    f"""

        #version {GLSL_VERSION}

        in vec3 v_color;
        out vec3 f_color;
        
        void main() 
        {{
            f_color = v_color;
        }}

    """,

)


x = np.linspace(-1.0, 1.0, 50) # Gera 50 valores espaçados por 1 pixel variando de 1 a -1
y = np.random.rand(50) - 0.5   # Gera 50 valores aleatórios 
r = np.zeros(50)               # Gera 50 zeros
g = np.ones(50)                # Gera 50 uns (1)
b = np.zeros(50)

vertices = np.dstack([x, y, r, g, b]) # Ref: https://numpy.org/doc/stable/reference/generated/numpy.dstack.html
vbo = ctx.buffer \
(
    # np.ndarray.astype("f4") -> retorna array de float de 4 bytes
    # retorna um espaço de memória
    vertices.astype("f4").tobytes()
)
vao = ctx.vertex_array(prog, vbo, "in_vert", "in_color")

# Ref: https://moderngl.readthedocs.io/en/latest/reference/context.html#Context.framebuffer
fbo = ctx.framebuffer \
(
    # Ref: https://moderngl.readthedocs.io/en/latest/reference/context.html#Context.texture
    color_attachments=[ctx.texture((512, 512), 3)]
)

while not window.is_closing:
    
    try:
        fbo.use()
        fbo.clear(0.0, 0.0, 0.0, 1.0)
        vao.render(moderngl.LINE_STRIP)
        ctx.copy_framebuffer(window.fbo, fbo)
        window.swap_buffers()
    
    except KeyboardInterrupt as k:
        window.is_closing = True
