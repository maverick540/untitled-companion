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

    return


#########################
# LOOP PRINCIPAL DEL JUEGO
#########################

label main_loop:

    # Este pause hace que el juego siga corriendo sin salir al menú.
    $ renpy.pause(0.1, hard=True)

    # En el futuro puedes poner aquí cosas como:
    # - Diálogos automáticos de motivación
    # - Eventos al completar ciclos
    # - Comentarios de Luna según el modo
    # - Integraciones externas

    jump main_loop
