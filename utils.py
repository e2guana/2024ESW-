def check_collision(entity1, entity2):
    """
    두 객체(entity1, entity2) 간의 충돌을 감지하는 함수.
    Spaceship, Laser, Obstacle 객체를 지원합니다.
    """
    # entity1의 충돌 박스 계산
    if hasattr(entity1, "size"):  # Spaceship 또는 Obstacle인 경우
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
    if hasattr(entity2, "size"):  # Spaceship 또는 Obstacle인 경우
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
