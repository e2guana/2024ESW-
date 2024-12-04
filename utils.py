def check_collision(spaceship, obstacle):
    return (
        spaceship.x < obstacle.x + obstacle.size and
        spaceship.x + spaceship.size > obstacle.x and
        spaceship.y < obstacle.y + obstacle.size and
        spaceship.y + spaceship.size > obstacle.y
    )
