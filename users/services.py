from .models import CustomUser


def find_neighbours(user: CustomUser):
    neighbours = CustomUser.objects.all()
    current_room = user.room_number  # номер комнаты, для которой нужно найти ближайшие соседи

    floor = current_room // 100  # вычисление номера этажа
    room_number = current_room % 100  # вычисление номера комнаты на этаже

    closest_upper = None  # ближайшая комната на верхнем этаже
    closest_lower = None  # ближайшая комната на нижнем этаже

    for room in neighbours:
        if room == current_room:
            continue  # пропустить текущую комнату

        # вычисление этажа и номера комнаты для соседней комнаты
        neighbor_floor = room // 100
        neighbor_room_number = room % 100

        # проверка наличия соседней комнаты на текущем этаже
        if neighbor_floor == floor:
            # вычисление расстояния между номерами комнат
            distance = abs(neighbor_room_number - room_number)

            # проверка, является ли соседняя комната на верхнем этаже и ближе, чем текущий ближайший сосед на верхнем этаже
            if neighbor_floor > floor and (closest_upper is None or distance < abs(closest_upper % 100 - room_number)):
                closest_upper = room

            # проверка, является ли соседняя комната на нижнем этаже и ближе, чем текущий ближайший сосед на нижнем этаже
            if neighbor_floor < floor and (closest_lower is None or distance < abs(closest_lower % 100 - room_number)):
                closest_lower = room

    # вывод ближайших соседей
    if closest_upper is not None:
        print("Ближайшая комната на верхнем этаже: ", closest_upper)
    if closest_lower is not None:
        print("Ближайшая комната на нижнем этаже: ", closest_lower)
