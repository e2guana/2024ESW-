from PIL import Image, ImageDraw
from spaceship import Spaceship
from obstacle import Obstacle, Rock1, Rock2
from utils import check_collision, calculate_collision_position
from enemy import Enemy
from item import Lifeitem
from collision import Collision
from explosion import Explosion
import random

class AstroEvasion:
    def __init__(self, joystick):
        self.joystick = joystick
        self.width = joystick.width
        self.height = joystick.height
        self.image = Image.new("RGB", (self.width, self.height))
        self.spaceship = Spaceship(self.width, self.height)
        self.obstacles = []
        self.score = 0
        self.game_over = False
        self.background = Image.open("assets/Background.png").resize((self.width, self.height))
        self.enemies = []  # 적 우주선 리스트
        self.items = []  # 아이템 리스트 추가
        self.collisions = []  # 충돌 표시 리스트
        self.explosions = []  # 폭발 애니메이션 리스트

        self.last_enemy_score = 0
        
    def add_obstacle(self):
        # Rock1 생성 확률
        if random.random() < 0.04:  # 4% 확률로 Rock1 생성
            self.obstacles.append(Rock1(self.width))
        # Rock2 생성 확률
        if random.random() < 0.02:  # 2% 확률로 Rock2 생성
            self.obstacles.append(Rock2(self.width))

    def add_enemy(self):
        # 1000점마다 적 등장
        if self.score >= self.last_enemy_score + 1000:
            self.enemies.append(Enemy(self.width))
            self.last_enemy_score += 1000
            
    def add_item(self, x, y):
        #특정 좌표에서 Item 생성
        self.items.append(Lifeitem(x, y))

    def update(self, buttons):
        self.spaceship.move(buttons)
        self.spaceship.update_barrier()  # 방어막 상태 업데이트
        
        if buttons["fire"]:  # 버튼 눌리면 발사
            self.spaceship.shoot()
        
        self.spaceship.update_lasers()
        
        # 장애물 이동
        obstacles_to_remove = []
        for obstacle in self.obstacles:
            obstacle.move()
        
        # 레이저와 장애물 충돌 처리
        lasers_to_remove = []  # 충돌한 레이저
        obstacles_to_remove = []  # 제거할 장애물
        
        for laser in self.spaceship.lasers:
            for obstacle in self.obstacles:
                if check_collision(laser, obstacle):
                    obstacle.take_damage(laser.damage)
                    lasers_to_remove.append(laser)
                    if obstacle.is_destroyed:
                        self.explosions.append(
                            Explosion(obstacle.x, obstacle.y, obstacle.size)
                        )
                        self.score += obstacle.get_score()
                        obstacles_to_remove.append(obstacle)
                    break  # 한 레이저는 한 장애물만 처리
            
        
        # 충돌한 레이저 제거
        self.spaceship.lasers = [laser for laser in self.spaceship.lasers if laser not in lasers_to_remove]
         # 제거할 장애물 리스트를 사용해 장애물 제거
        self.obstacles = [obstacle for obstacle in self.obstacles if obstacle not in obstacles_to_remove]

        # 폭발 애니메이션 업데이트
        self.explosions = [exp for exp in self.explosions if not exp.finished]
        for explosion in self.explosions:
            explosion.update()
        
        # 화면 밖으로 벗어난 장애물 삭제
        self.obstacles = [o for o in self.obstacles if o.y < self.height]
        self.spaceship.lasers = [l for l in self.spaceship.lasers if not l.is_off_screen(self.height)]
        
        # 장애물과 우주선 충돌 처리
        obstacles_to_remove = []  # 충돌한 장애물
        for obstacle in self.obstacles:
            if check_collision(self.spaceship, obstacle):
                if not self.spaceship.barrier.is_active:
                    self.spaceship.take_damage()  # 우주선 체력 감소
                    # 충돌 표시 생성
                    collision_x, collision_y = calculate_collision_position(self.spaceship, obstacle)
                    self.collisions.append(Collision(collision_x, collision_y))
                obstacles_to_remove.append(obstacle)
                if self.spaceship.is_destroyed():
                    self.game_over = True

        # 충돌한 장애물 즉시 제거
        self.obstacles = [o for o in self.obstacles if o not in obstacles_to_remove]
        
        # 충돌 표시 제거 (해당 충돌 표시가 사라져야 할 때)
        self.collisions = [collision for collision in self.collisions if collision.is_active()]
        
        #점수 증가
        self.score += 1
        
        # 적 우주선 추가
        self.add_enemy()
        
        # 적 이동
        enemy_to_remove = []
        for enemy in self.enemies:
            enemy.move()
            enemy.shoot()
            for laser in enemy.lasers:
                laser.move()

            
        # 적과 플레이어 레이저 충돌 처리
        lasers_to_remove = []  # 충돌한 레이저
        for laser in self.spaceship.lasers:
            for enemy in self.enemies:
                if check_collision(laser, enemy):  # 적과 레이저 충돌 확인
                    enemy.take_damage(laser.damage)  # 적 체력 감소
                    lasers_to_remove.append(laser)
                    if enemy.is_destroyed:
                        self.explosions.append(Explosion(enemy.x, enemy.y, enemy.size))
                        self.add_item(enemy.x, enemy.y)  # 아이템 생성
                        enemy_to_remove.append(enemy)
                break
                
        # 충돌한 레이저 제거
        self.spaceship.lasers = [laser for laser in self.spaceship.lasers if laser not in lasers_to_remove]
        # 제거할 적 리스트를 사용해 적 제거
        self.enemies = [enemy for enemy in self.enemies if enemy not in enemy_to_remove]
        # 폭발 애니메이션 업데이트
        self.explosions = [exp for exp in self.explosions if not exp.finished]
        for explosion in self.explosions:
            explosion.update()
        
        
        # 적 레이저와 플레이어 충돌 처리
        for enemy in self.enemies:
            lasers_to_remove = []  # 충돌한 레이저 리스트
            for laser in enemy.lasers:
                if check_collision(self.spaceship, laser):
                    if not self.spaceship.barrier.is_active:  # 방어막이 없는 경우
                        # 충돌 표시 생성
                        collision_x, collision_y = calculate_collision_position(self.spaceship, laser)
                        self.collisions.append(Collision(collision_x, collision_y))
                        
                        self.spaceship.take_damage()  # 체력 감소
                        if self.spaceship.is_destroyed():
                            self.game_over = True
                    lasers_to_remove.append(laser)  # 충돌한 레이저 제거

            # 충돌한 레이저 제거
            enemy.lasers = [laser for laser in enemy.lasers if laser not in lasers_to_remove]


        # 아이템 이동 및 충돌 처리
        for item in self.items:
            item.move()
            if item.check_collision(self.spaceship):  # 우주선과 충돌 확인
                if self.spaceship.health < 5:  # 최대 체력 제한
                    self.spaceship.health += 1
                self.items.remove(item)

        # 화면 밖 객체 제거
        self.items = [i for i in self.items if not i.is_off_screen(self.height)]
        
    def draw(self):
        # 새 이미지로 구현 초기화
        self.image.paste(self.background, (0, 0))  # 배경 이미지 설정
        draw = ImageDraw.Draw(self.image)  # 이미지에 그리기 객체 생성

        # 우주선 구현
        self.spaceship.draw(self.image)
        # 장애물 구현
        for obstacle in self.obstacles:
            obstacle.draw(self.image)   
        # 적 우주선 구현
        for enemy in self.enemies:
            enemy.draw(self.image)
        
        # 아이템 구현
        for item in self.items:
            item.draw(self.image)
            
        # 충돌 표시 그리기
        for collision in self.collisions:
            collision.draw(self.image)
        
        # 폭발 애니메이션 그리기
        for explosion in self.explosions:
            explosion.draw(self.image)

        
        # 점수 표시
        draw.text((10, 10), f"Score: {self.score}", fill=(255, 255, 255))  # 흰색 텍스트
    
