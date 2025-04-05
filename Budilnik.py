import time
import winsound
from datetime import datetime, timedelta
import threading


def exit_code(timeout=10):
    user_input = [None]
    def wait_for_input():
        user_input[0] = input("Для выхода введите 'exit' (или подождите {} секунд): ".format(timeout)).strip().lower()
    input_thread = threading.Thread(target=wait_for_input)
    input_thread.daemon = True
    input_thread.start()
    input_thread.join(timeout)
    if user_input[0] == 'exit':
        print("Выход из программы...")
        exit()
    else:
        print("Продолжаем выполнение программы...")

def get_alarm_time():
    while True:
        alarm_time = input("Введите время будильника в формате ЧЧ:ММ: ")
        try:
            time.strptime(alarm_time, "%H:%M")
            return alarm_time
        except ValueError:
            print("Неправильный формат времени. Пожалуйста, попробуйте снова.")

def get_notification_type():
    return input("Выберите тип уведомления (1 - звук, 2 - текст): ")

def get_sound_choice():
    sounds = ['sound1.wav', 'sound2.wav', 'sound3.wav']
    print("Доступные звуки:")
    for i, sound in enumerate(sounds):
        print(f"{i + 1} - {sound}")
    choice = int(input("Выберите номер звука: ")) - 1
    return sounds[choice] if 0 <= choice < len(sounds) else sounds[0]

def get_days_of_week():
    days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    print("Выберите дни недели (например, 1,2,3 для Пн, Вт, Ср):")
    print(", ".join(days))
    selected_days = input("Введите номера дней через запятую: ")
    return [days[int(day) - 1] for day in selected_days.split(",") if day.isdigit()]

def play_sound(sound):
    winsound.PlaySound(sound, winsound.SND_FILENAME)

def main():
    alarms = []

    while True:
        alarm_time = get_alarm_time()
        notification_type = get_notification_type()

        sound_choice = ""
        text_choice = ""

        if notification_type == '1':
            sound_choice = get_sound_choice()
        elif notification_type == '2':
            text_choice = input("Введите текст уведомления: ")

        days_of_week = get_days_of_week()
        repeat_interval = input("Введите интервал повтора в минутах (0 для отключения): ")
        repeat_interval = int(repeat_interval) if repeat_interval.isdigit() else 0

        alarms.append({
            "time": alarm_time,
            "type": notification_type,
            "sound": sound_choice,
            "text": text_choice,
            "days": days_of_week,
            "repeat": repeat_interval
        })

        print(f"Будильник установлен на {alarm_time}.")

        exit_code(timeout=10)

        while True:
            current_time = datetime.now().strftime("%H:%M")
            current_day_index = datetime.now().weekday()
            current_day_short = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"][current_day_index]

            print(f"Текущее время: {current_time}, Текущий день: {current_day_short}")

            for alarm in alarms:
                print(f"Проверка будильника: {alarm['time']} на дни {alarm['days']}")
                if current_time == alarm["time"] and current_day_short in alarm["days"]:
                    if alarm["type"] == '1':
                        play_sound(alarm["sound"])
                    elif alarm["type"] == '2':
                        print(alarm["text"])
                    print("Будильник сработал!")

                    if alarm["repeat"] > 0:
                        next_time = (datetime.now() + timedelta(minutes=alarm["repeat"])).strftime("%H:%M")
                        alarm["time"] = next_time
                    else:
                        alarms.remove(alarm)
                    break
            exit_code(timeout=10)
            time.sleep(30)

if __name__ == "__main__":
    main()