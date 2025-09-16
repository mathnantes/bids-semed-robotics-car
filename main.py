"""
Remote Control Car (micro:bit + Robot:Bit)
Ações:
  1 -> Frente
  2 -> Parar
  3 -> Ré (acende luzes de ré)
  4 -> Virar esquerda (pisca seta esquerda)
  5 -> Virar direita (pisca seta direita)
"""

# ==========================
# Pins (substitua os das setas conforme seu hardware)
# ==========================
INDICATOR_LEFT_PIN = DigitalPin.P0   # seta esquerda (trocar pelo pino correto)
INDICATOR_RIGHT_PIN = DigitalPin.P1  # seta direita  (trocar pelo pino correto)

# LEDs de ré seguem os mesmos pinos usados no código original:
# DigitalPin.P15 (esquerdo) e DigitalPin.P14 (direito)

# ==========================
# Simple state (guarda a última ação recebida)
# ==========================
CURRENT_ACTION = 0  # 1, 2, 3, 4 ou 5

# ==========================
# Reverse lights (ré)
# ==========================
def set_reverse_lights(state):
    """Liga(1)/Desliga(0) os dois LEDs de ré (P15 e P14)."""
    pins.digital_write_pin(DigitalPin.P15, state)
    pins.digital_write_pin(DigitalPin.P14, state)

def update_reverse_lights():
    """Acende as luzes de ré SOMENTE quando a ação atual é 3 (ré)."""
    if CURRENT_ACTION == 3:
        set_reverse_lights(1)
    else:
        set_reverse_lights(0)

# ==========================
# Turn indicators (setas)
# ==========================
def blink_indicator(pin):
    """Pisca um LED (acende, espera, apaga, espera). Chamado em loop para manter o efeito."""
    pins.digital_write_pin(pin, 1)
    basic.pause(200)
    pins.digital_write_pin(pin, 0)
    basic.pause(200)

def update_indicators():
    """
    Pisca setas conforme a ação atual:
      4 -> pisca esquerda
      5 -> pisca direita
      outras -> ambas apagadas
    """
    if CURRENT_ACTION == 4:
        blink_indicator(INDICATOR_LEFT_PIN)
        pins.digital_write_pin(INDICATOR_RIGHT_PIN, 0)
    elif CURRENT_ACTION == 5:
        blink_indicator(INDICATOR_RIGHT_PIN)
        pins.digital_write_pin(INDICATOR_LEFT_PIN, 0)
    else:
        pins.digital_write_pin(INDICATOR_LEFT_PIN, 0)
        pins.digital_write_pin(INDICATOR_RIGHT_PIN, 0)

# ==========================
# Radio callback (mantém o nome original)
# ==========================
def on_received_number(received_number):
    global CURRENT_ACTION
    CURRENT_ACTION = received_number  # atualiza o estado primeiro

    if received_number == 1:
        # Frente
        robotbit.motor_run_dual(robotbit.Motors.M1A, -255, robotbit.Motors.M1B, 255)
        robotbit.motor_run_dual(robotbit.Motors.M2A, -255, robotbit.Motors.M2B, 255)

    elif received_number == 2:
        # Parar
        robotbit.motor_stop(robotbit.Motors.M1A)
        robotbit.motor_stop(robotbit.Motors.M1B)
        robotbit.motor_stop(robotbit.Motors.M2A)
        robotbit.motor_stop(robotbit.Motors.M2B)

    elif received_number == 3:
        # Trás (ré)
        robotbit.motor_run_dual(robotbit.Motors.M1A, 255, robotbit.Motors.M1B, -255)
        robotbit.motor_run_dual(robotbit.Motors.M2A, 255, robotbit.Motors.M2B, -255)

    elif received_number == 4:
        # Virar esquerda (para lado direito)
        robotbit.motor_stop(robotbit.Motors.M1B)
        robotbit.motor_stop(robotbit.Motors.M2A)

    elif received_number == 5:
        # Virar direita (para lado esquerdo)
        robotbit.motor_stop(robotbit.Motors.M1A)
        robotbit.motor_stop(robotbit.Motors.M2B)

radio.on_received_number(on_received_number)

# ==========================
# Local controls (mantidos com os nomes originais)
# ==========================
# Virar esquerda
def on_gesture_tilt_left():
    radio.send_number(4)
input.on_gesture(Gesture.TILT_LEFT, on_gesture_tilt_left)

# Frente
def on_button_pressed_a():
    radio.send_number(1)
input.on_button_pressed(Button.A, on_button_pressed_a)

# Trás
def on_button_pressed_ab():
    radio.send_number(3)
input.on_button_pressed(Button.AB, on_button_pressed_ab)

# Parar
def on_button_pressed_b():
    radio.send_number(2)
input.on_button_pressed(Button.B, on_button_pressed_b)

# Virar direita
def on_gesture_tilt_right():
    radio.send_number(5)
input.on_gesture(Gesture.TILT_RIGHT, on_gesture_tilt_right)

# ==========================
# Main loop (mantém regras ativas o tempo todo)
# ==========================
def on_forever():
    update_reverse_lights()
    update_indicators()
basic.forever(on_forever)

# ==========================
# Radio group (mantido)
# ==========================
radio.set_group(1)
