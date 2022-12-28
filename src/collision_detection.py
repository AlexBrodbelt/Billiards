def sweep_and_prune(balls):
    """sweep along one axis:  y axis ; returns list of possible intersections    """
    enumerated_balls = enumerate(balls)
    sorted_balls_y = sorted(enumerated_balls, key=(lambda item: item[1].position.y)) # sort balls by the y_axis
    sorted_balls_x = sorted(enumerated_balls, key=(lambda item: item[1].position.x))
    return get_active_intervals(sorted_balls_x).intersection(get_active_intervals(sorted_balls_y))

def is_active_interval(ball_1, ball_2):
    return (ball_1.position.y + ball_1.radius) >= (ball_2.position.y - ball_2.radius)

def get_active_intervals(sorted_balls):
    active_intervals = set()
    for k in range(len(sorted_balls) - 1):
        i, ball_1 = sorted_balls[k]; j, ball_2 = sorted_balls[k+1]
        if is_active_interval(ball_1, ball_2):
            active_intervals.add((i, j))
    return active_intervals
     

