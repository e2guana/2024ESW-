def check_collision(entity1, entity2):
    #장애물과<->플레이어, 내가 발사한 레이저
    # entity1의 충돌 박스 계산
    if hasattr(entity1, "get_hitbox"):  # Spaceship인 경우 get_hitbox 사용
        x1_1, y1_1, x2_1, y2_1 = entity1.get_hitbox()
    elif hasattr(entity1, "size"):  # Obstacle인 경우
        x1_1 = entity1.x
        y1_1 = entity1.y
        x2_1 = entity1.x + entity1.size
        y2_1 = entity1.y + entity1.size
    elif hasattr(entity1, "image"):  # Laser인 경우
        x1_1 = entity1.x - entity1.image.width // 2
        y1_1 = entity1.y
        x2_1 = entity1.x + entity1.image.width // 2
        y2_1 = entity1.y + entity1.image.height

    # entity2의 충돌 박스 계산
    if hasattr(entity2, "get_hitbox"):  # Spaceship인 경우 get_hitbox 사용
        x1_2, y1_2, x2_2, y2_2 = entity2.get_hitbox()
    elif hasattr(entity2, "size"):  # Obstacle인 경우
        x1_2 = entity2.x
        y1_2 = entity2.y
        x2_2 = entity2.x + entity2.size
        y2_2 = entity2.y + entity2.size
    elif hasattr(entity2, "image"):  # Laser인 경우
        x1_2 = entity2.x - entity2.image.width // 2
        y1_2 = entity2.y
        x2_2 = entity2.x + entity2.image.width // 2
        y2_2 = entity2.y + entity2.image.height

    # 충돌 여부 확인 (박스 간의 겹침 여부 확인)
    return not (
        x2_1 < x1_2 or  # entity1이 entity2의 왼쪽에 있음
        x1_1 > x2_2 or  # entity1이 entity2의 오른쪽에 있음
        y2_1 < y1_2 or  # entity1이 entity2의 위쪽에 있음
        y1_1 > y2_2     # entity1이 entity2의 아래쪽에 있음
    )
# utils.py

def calculate_collision_position(entity1, entity2):
    #충돌표시가 발생을 위한 충돌 위치 계산 함수/ 적 레이저 <->내 우주선, 장애물 <-> 내 우주선
    # Entity1의 히트박스 계산
    if hasattr(entity1, "get_hitbox"):
        x1_1, y1_1, x2_1, y2_1 = entity1.get_hitbox()
    elif hasattr(entity1, "image"):  # Laser 또는 이미지 기반 객체
        x1_1 = entity1.x - entity1.image.width // 2
        y1_1 = entity1.y
        x2_1 = entity1.x + entity1.image.width // 2
        y2_1 = entity1.y + entity1.image.height
    else:
        raise ValueError("Entity1은 히트박스를 계산할 수 없습니다.")

    # Entity2의 히트박스 계산
    if hasattr(entity2, "get_hitbox"):
        x1_2, y1_2, x2_2, y2_2 = entity2.get_hitbox()
    elif hasattr(entity2, "image"):  # Laser 또는 이미지 기반 객체
        x1_2 = entity2.x - entity2.image.width // 2
        y1_2 = entity2.y
        x2_2 = entity2.x + entity2.image.width // 2
        y2_2 = entity2.y + entity2.image.height
    else:
        raise ValueError("계산 불가")

    # 겹치는 부분의 좌표 계산
    collision_x1 = max(x1_1, x1_2)  # 겹치는 왼쪽 x
    collision_y1 = max(y1_1, y1_2)  # 겹치는 위쪽 y
    collision_x2 = min(x2_1, x2_2)  # 겹치는 오른쪽 x
    collision_y2 = min(y2_1, y2_2)  # 겹치는 아래쪽 y


    # 중앙 좌표 계산
    collision_x = (collision_x1 + collision_x2) // 2
    collision_y = (collision_y1 + collision_y2) // 2

    return collision_x, collision_y
