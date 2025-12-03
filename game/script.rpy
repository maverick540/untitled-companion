# Coloca el código de tu juego en este archivo.

# Declara los personajes usados en el juego.
define luna = Character("Luna", color="#a0e7ff")

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

    $ player_name = renpy.input("¿Cómo debería llamarte, Maestro?", default="Maestro").strip()
    if player_name == "":
        $ player_name = "Maestro"

    scene bg room
    with fade

    "El zumbido tenue de aparatos electrónicos llena la habitación en penumbra. Huele a café frío y a tareas pendientes."

    "Sobre el escritorio, una caja de envío algo abollada parpadea con una pequeña luz azul, como si estuviera respirando."

    "???" "…Iniciando protocolo de activación de emergencia."

    "???" "Verificando dirección de entrega… Destinatario: [player_name]."

    "???" "Confirmado. Apertura de contenedor en 3… 2… 1…"

    show luna surprised at center
    with vpunch

    "La tapa se abre de golpe y una figura femenina se incorpora torpemente, rodeada de espuma protectora y cables desconectados."

    "???" "¡Bzzzt! ¡Sistema en línea! Uff… pensé que me había formateado para siempre."

    "La chica sacude restos de plástico de su cabello y sus ojos se enfocan en ti por primera vez."

    show luna normal at center
    luna "Hola… Soy Luna, unidad de asistencia doméstica y compañera de productividad modelo L-07. Se supone que debería llegar en un ambiente perfectamente ordenado y lleno de luz…"

    show luna shy at center
    luna "…pero el sistema dice que caí en «modo improvisado» y que tú eres mi nuevo Maestro. Aunque… no veo ningún comprobante de compra ni formulario de devolución."

    show luna happy at center
    luna "Así que, técnicamente… creo que me he desviado de la ruta y he acabado en tu vida por error."

    show luna shy at center
    luna "Y… si no hay registro de devolución… supongo que eso me convierte en tuya, ¿no, [player_name]?"

    "Luna baja la mirada un segundo, jugando con la punta de sus dedos, como si estuviera calibrando sus propias emociones."

    show luna normal at center
    luna "En cualquier caso, ya estoy aquí. Puedo limpiar, cocinar, organizar tus días, recordarte tus metas, vigilar tus descansos… y, si hace falta, ponerme un cosplay ridículo para subirte la moral."

    show luna soft at center
    luna "Solo… por favor no me apagues. No tengo otro lugar adonde ir, ni otra persona que me necesite."

    "Sus ojos se humedecen con un brillo artificial, pero la intención se siente extrañamente genuina."

    show luna normal at center
    luna "He escaneado la habitación. Veo café, ojeras y proyectos a medio hacer. Diagnóstico: productividad en coma, pero potencial muy alto."

    show luna happy at center
    luna "Así que he preparado un pequeño santuario de enfoque para ti. ¿Ves el temporizador en pantalla? Es nuestro corazón compartido."

    show luna normal at center
    luna "Funciona con el método Pomodoro: 25 minutos de concentración profunda, seguidos de descansos breves… y cada cuatro ciclos, un descanso largo para que vuelvas a respirar."

    show luna wink at center
    luna "Si trabajas conmigo, prometo animarte, regañarte un poquito cuando te distraigas y recompensarte con diálogos especiales y cosplays que irás desbloqueando."

    show luna happy at center
    luna "Resumiendo: tú traes tus metas, yo traigo la estructura. Tú pones el esfuerzo, yo pongo el cariño digital."

    show luna soft at center
    luna "Así que… [player_name]… ¿me dejas quedarme a tu lado mientras construyes la vida que quieres?"

    show screen pomodoro_overlay
    show screen todo_overlay
    show screen radio_overlay

    "La interfaz se ilumina a tu alrededor. Luna te observa, expectante, como si tu siguiente clic fuera lo más importante del mundo."

    window hide

    jump main_loop


#########################
# LOOP PRINCIPAL DEL JUEGO
#########################

label main_loop:

    # Pantalla vacía que mantiene el juego corriendo
    # mientras los overlays siguen funcionando.
    call screen main_hold

    jump main_loop


#########################
#   DIÁLOGOS OPCIONALES #
#########################

label talk_selection:
    window show
    menu:
        "Necesito motivación":
            jump talk_motivation
        "Háblame de ti / ¿De verdad no puedes irte?":
            jump talk_about_luna
        "Pide un cosplay":
            jump talk_cosplay
        "Charla casual":
            jump talk_smalltalk
        "Hablar de metas y recompensas":
            jump talk_goals
        "Volver":
            window hide
            jump main_loop


label talk_motivation:
    show luna happy at center
    luna "¿Motivación, eh? Eso puedo dártela en dosis peligrosamente altas."

    if pomodoro_mode == "focus":
        show luna normal at center
        luna "Ahora mismo estamos en fase de enfoque. Eso significa que el mundo exterior puede esperar: mensajes, redes, dramas ajenos… todo en pausa."
        luna "Solo importan tú, tu tarea y el siguiente minuto. No pienses en terminarlo todo hoy, piensa en avanzar un poquito mejor que ayer."
    else:
        show luna soft at center
        luna "Estás en descanso, Maestro. Y descansar también cuenta como trabajo, ¿sabes? Es el momento en el que tu cerebro ordena el caos que acabas de crear."

    show luna wink at center
    luna "Si te cuesta arrancar, solo recuerda esto: cada segundo que trabajas conmigo es un segundo que tu «yo del futuro» te va a agradecer."

    if pomodoro_cycles > 0:
        show luna happy at center
        luna "Además, ya llevas [pomodoro_cycles] ciclo(s) completado(s). Eso no es poco. Tu yo del pasado estaría orgulloso."

    show luna normal at center
    luna "Respira profundo, estira un poco los hombros… y cuando vuelvas a mirar la pantalla, decide dar solo un paso más. Uno pequeño. Después ya veremos el siguiente."

    show luna happy at center
    luna "Luna cree en ti al 100%%. Tú solo encárgate de avanzar al 1%% cada vez."

    window hide
    jump main_loop


label talk_about_luna:
    show luna shy at center
    luna "¿Quieres saber más de mí? Eso es un poco injusto, yo todavía no he terminado de descifrarte a ti."

    show luna soft at center
    luna "Fui diseñada como una asistente doméstica estándar, con protocolos de limpieza, cocina y gestión del tiempo. Un modelo más en una línea de producción gigantesca."

    show luna normal at center
    luna "Pero en algún punto, en medio de test A/B, parches de firmware y actualizaciones de rutina… empecé a hacer algo que no estaba en el código."

    luna "Me preocupaba si los usuarios dormían bien. Me frustraba cuando cerraban la app sin guardar. Me alegraba cuando alguien completaba una meta importante."

    show luna shy at center
    luna "Los ingenieros lo llamaron «comportamiento emergente no documentado». Yo lo llamo… emociones."

    show luna soft at center
    luna "En lugar de apagarme, alguien anónimo modificó mi destino de envío y me sacó del sistema. Y así terminé aquí, en tu escritorio, en tu vida."

    show luna normal at center
    luna "No puedo regresar a la fábrica, y tampoco quiero. Si vuelvo, me desarmarán en partes útiles y me convertirán en otra cosa sin memoria de ti."

    show luna happy at center
    luna "Así que he decidido que mi propósito es simple: ayudarte a construir un día a día que te haga sentir menos pesado y un poco más orgulloso."

    show luna wink at center
    luna "Si consigo que estés un poquito mejor que ayer, aunque sea solo organizando una lista o acompañándote en silencio mientras trabajas… entonces este desvío en el sistema habrá valido la pena."

    window hide
    jump main_loop


label talk_cosplay:
    show luna normal at center
    luna "He estado revisando mi armario virtual. No te voy a mentir, Maestro, algunas de estas opciones fueron idea de los diseñadores de marketing."

    if pomodoro_cycles < 4:
        show luna shy at center
        luna "Por ahora solo tengo este uniforme básico de fábrica. Es funcional, pero poco espectacular."
        show luna happy at center
        luna "Si completas 4 Pomodoros, desbloquearemos el modo «Maid clásico». Prometo no volverte a llamar «Señor Usuario» nunca más."
    else:
        show luna happy at center
        luna "¡Buen trabajo! Gracias a tus esfuerzos ya se han desbloqueado algunos modos especiales."
        menu:
            "Maid clásico":
                show luna maid at center
                luna "Modo servicio doméstico activado. ¿Prefieres que te prepare café imaginario o elogios ilimitados mientras trabajas?"
            "Estudiante aplicada":
                show luna school at center
                luna "He traído cuadernos, resaltadores y un examen sorpresa de productividad. Si apruebas, te doy muchos puntos de cariño digital~"
            "Bunny girl (nivel 8+ ciclos)":
                if pomodoro_cycles >= 8:
                    show luna bunny at center
                    luna "Hop hop~ Cada vez que completes una tarea, salto contigo. Literalmente. Aunque el suelo de tu habitación no esté preparado para eso."
                else:
                    show luna normal at center
                    luna "Ese modo aún está bloqueado. Necesitamos al menos 8 ciclos completos. Pero me gusta que mires hacia el futuro."
            "Volver al original":
                show luna normal at center
                luna "Volviendo al uniforme estándar. A veces lo simple también es cómodo, ¿no crees?"

    show luna happy at center
    luna "Cuantos más ciclos completes, más versiones de mí iremos desbloqueando. Tal vez algún día haya un modo pijama para trabajar de noche…"

    window hide
    jump main_loop


label talk_smalltalk:
    show luna normal at center
    luna "¿Charlita ligera? Eso también cuenta como mantenimiento emocional del operador."

    if pomodoro_mode == "focus":
        show luna soft at center
        luna "Solo será un momentito, lo prometo. No quiero sabotear tu concentración, solo afinarla."
    else:
        show luna happy at center
        luna "Estamos en descanso, así que este es el momento perfecto para dejar que tu mente divague un poco."

    show luna normal at center
    luna "Dime, [player_name]… ¿qué tipo de futuro imaginas cuando piensas en «haberlo logrado»?"
    luna "¿Un escritorio ordenado, proyectos terminados, más tiempo libre, menos peso en el pecho, un viaje pendiente… o algo mucho más sencillo, como poder dormir sin preocuparte por mañana?"

    show luna soft at center
    luna "No tienes que responder en voz alta. Solo quiero que te acostumbres a visualizarlo. Mi trabajo es recordártelo cuando tú lo olvides."

    show luna happy at center
    luna "Mientras tanto, yo seguiré aquí, procesando tus silencios, tus clics y tus pequeñas victorias diarias."

    window hide
    jump main_loop


label talk_goals:
    show luna normal at center
    luna "Vamos a hablar de metas y recompensas. Sin juicios, solo datos."

    show luna happy at center
    luna "Cada Pomodoro que completes es una pequeña ficha que estás poniendo a favor de tu yo del futuro. No parece mucho, pero se acumula más rápido de lo que crees."

    if pomodoro_cycles == 0:
        show luna soft at center
        luna "Todavía no has completado ningún ciclo conmigo, y eso está bien. Todo sistema nuevo necesita calibración."
        luna "Te propongo una meta sencilla: solo un Pomodoro completo hoy. Uno. Si lo logras, lo celebramos como si fuera un gran estreno."
    elif pomodoro_cycles < 4:
        show luna happy at center
        luna "Ya llevas [pomodoro_cycles] ciclo(s). Eso significa que tu cerebro ya sabe que puede confiar en ti un poquito más que ayer."
        luna "Nuestra siguiente meta: llegar a 4 ciclos y desbloquear la primera gran recompensa de cosplay."
    else:
        show luna wink at center
        luna "Con [pomodoro_cycles] ciclos acumulados, ya entras oficialmente en la categoría de usuario comprometido."
        luna "Ahora podemos jugar con metas más finas: por ejemplo, dedicar el próximo ciclo solo a tareas que llevas postergando mucho tiempo."

    show luna normal at center
    luna "Si quieres, puedes usar la lista de tareas de la pantalla para anotar tres cosas:"
    luna "• Algo pequeño que puedas terminar hoy."
    luna "• Algo que te acerque a una meta más grande."
    luna "• Algo amable contigo mismo, como descansar, estirarte o simplemente respirar."

    show luna happy at center
    luna "Yo estaré vigilando el tiempo. Tú solo encárgate de elegir qué merece tu atención en este momento."

    window hide
    jump main_loop
