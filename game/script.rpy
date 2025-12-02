# Coloca el código de tu juego en este archivo.

# Declara los personajes usados en el juego.
define luna = Character("Luna", color="#f4a9c5")

# Variables del sistema Pomodoro.
default pomodoro_focus_duration = 25 * 60
default pomodoro_short_break_duration = 5 * 60
default pomodoro_long_break_duration = 15 * 60
default pomodoro_mode = "focus"
default pomodoro_time_remaining = pomodoro_focus_duration
default pomodoro_running = False
default pomodoro_cycles = 0

# Variables del sistema TODO
default todo_list = []
default new_task_text = ""

default player_name = ""

init python:
    def pomodoro_duration_for_mode(mode):
        if mode == "focus":
            return store.pomodoro_focus_duration
        if mode == "break":
            return store.pomodoro_short_break_duration
        if mode == "long_break":
            return store.pomodoro_long_break_duration
        return store.pomodoro_focus_duration

    def pomodoro_reset(next_mode=None):
        mode = next_mode or store.pomodoro_mode
        store.pomodoro_mode = mode
        store.pomodoro_time_remaining = pomodoro_duration_for_mode(mode)
        store.pomodoro_running = False

    def pomodoro_toggle():
        if store.pomodoro_time_remaining <= 0:
            pomodoro_reset(store.pomodoro_mode)
        store.pomodoro_running = not store.pomodoro_running

    def pomodoro_skip_phase():
        if store.pomodoro_mode == "focus":
            store.pomodoro_cycles += 1
            next_mode = "long_break" if store.pomodoro_cycles % 4 == 0 else "break"
        else:
            next_mode = "focus"
        pomodoro_reset(next_mode)

    def pomodoro_tick():
        if not store.pomodoro_running:
            return
        store.pomodoro_time_remaining = max(0, store.pomodoro_time_remaining - 1)
        if store.pomodoro_time_remaining == 0:
            store.pomodoro_running = False
            pomodoro_skip_phase()

    def pomodoro_time_display():
        minutes = int(store.pomodoro_time_remaining // 60)
        seconds = int(store.pomodoro_time_remaining % 60)
        return f"{minutes:02d}:{seconds:02d}"

    # Funciones para la lista de tareas
    def add_task(title):
        if title.strip():
            store.todo_list.append({"title": title, "done": False})

    def toggle_task(index):
        if 0 <= index < len(store.todo_list):
            store.todo_list[index]["done"] = not store.todo_list[index]["done"]

    def delete_task(index):
        if 0 <= index < len(store.todo_list):
            store.todo_list.pop(index)

    def add_task_from_input():
        add_task(store.new_task_text)
        store.new_task_text = ""


#######################
#  FLUJO DEL JUEGO    #
#######################

label start:

    $ player_name = renpy.input("¿Cómo debería llamarte?", default="senpai").strip()
    if player_name == "":
        $ player_name = "senpai"

    scene bg room
    show eileen happy

    show screen pomodoro_overlay
    show screen todo_overlay

    call intro_dialog

    jump main_loop


# Introducción hablada por Luna

label intro_dialog:

    luna "¡Hola, [player_name]! Soy Luna, tu waifu compañera de productividad."

    luna "Convertí este espacio en nuestro cuartel creativo. Yo aporto la motivación, tú aportas los sueños."

    luna "¿Ves el temporizador en la esquina? Es nuestro Pomodoro encantado: 25 minutos de enfoque, descansos cortos y abrazos virtuales cuando completes cuatro ciclos."

    luna "Pulsa Iniciar cuando estés listo, toma notas en tus propias aplicaciones y yo iré animándote para que mantengas el ritmo."

    luna "Si necesitas un respiro antes de tiempo, toca Omitir para saltar a un descanso, o Reiniciar para refrescar una sesión."

    luna "Ahora respira profundo, alinea tu espalda, y dime qué misión dominarás hoy. ¡Estoy a tu lado, [player_name]!"

    # >>> OCULTAR EL PANEL DE DIÁLOGO <<<
    window hide

    return


#########################
# LOOP PRINCIPAL DEL JUEGO
#########################

label main_loop:
    
    # Llamamos a una pantalla vacía que no hace nada más que esperar.
    # Esto evita el error de loop infinito y mantiene el juego corriendo
    # mientras los overlays (pomodoro, todo) siguen funcionando.
    call screen main_hold

    jump main_loop


label talk_selection:
    window show
    menu:
        "Necesito motivación":
            jump talk_motivation
        "Cuéntame sobre ti":
            jump talk_about_luna
        "Volver":
            window hide
            jump main_loop

label talk_motivation:
    luna "¡Tú puedes con todo, [player_name]! Recuerda por qué empezaste."
    luna "Cada pequeño paso cuenta. ¡Sigue así!"
    window hide
    jump main_loop

label talk_about_luna:
    luna "Soy una entidad digital creada para ayudarte a ser tu mejor versión."
    luna "Me alimento de tu productividad y de tus descansos bien merecidos."
    window hide
    jump main_loop
