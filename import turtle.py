import turtle
import heapq
import random
import time

# Initialize the screen
window = turtle.Screen()
window.title("Exit Search Game")
window.bgcolor("white")
window.setup(width=800, height=600)
window.tracer(0)

# Timer Display
timer1 = turtle.Turtle()
timer1.hideturtle()
timer1.penup()
timer1.goto(-200, 260)
timer1.write("Turtle 1 Time: 0.0s", align="center", font=("Arial", 16, "normal"))

timer2 = turtle.Turtle()
timer2.hideturtle()
timer2.penup()
timer2.goto(200, 260)
timer2.write("Turtle 2 Time: 0.0s", align="center", font=("Arial", 16, "normal"))

# Turtle 1 (A* algorithm)
player = turtle.Turtle()
player.speed(5)
player.shape("turtle")
player.color("green")
player.penup()
player.goto(-380, 0)

# Exit
exit = turtle.Turtle()
exit.speed(0)
exit.shape("circle")
exit.color("red")
exit.penup()
exit.goto(380, 0)

# Obstacles
obstacles = []
obstacle_positions = set()  # To keep track of obstacle positions to avoid overlap

# Function to check if a position is valid
def is_valid_position(x, y):
    if abs(x - player.xcor()) < 20 and abs(y - player.ycor()) < 20:
        return False
    if abs(x - exit.xcor()) < 20 and abs(y - exit.ycor()) < 20:
        return False
    if (x, y) in obstacle_positions:
        return False
    return True

while len(obstacles) < 50:  # Increase the number of obstacles
    x = random.randint(-350, 350)
    y = random.randint(-250, 250)
    if is_valid_position(x, y):
        obstacle = turtle.Turtle()
        obstacle.speed(0)
        obstacle.shape("square")
        obstacle.color("gray")
        obstacle.penup()
        obstacle.goto(x, y)
        obstacles.append(obstacle)
        obstacle_positions.add((x, y))

# A* algorithm
def a_star(start, goal, obstacles):
    graph = {}
    for i in range(-400, 401, 20):
        for j in range(-300, 301, 20):
            if any(abs(i - obs[0]) < 20 and abs(j - obs[1]) < 20 for obs in obstacles):
                graph[(i, j)] = float('inf')
            else:
                graph[(i, j)] = 20

    queue = [(0, start)]
    distances = {start: 0}
    while queue:
        (dist, current) = heapq.heappop(queue)
        if current == goal:
            break
        for direction in [(20, 0), (-20, 0), (0, 20), (0, -20)]:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if -400 <= neighbor[0] <= 400 and -300 <= neighbor[1] <= 300:
                new_dist = distances[current] + graph[neighbor]
                if new_dist < distances.get(neighbor, float('inf')):
                    distances[neighbor] = new_dist
                    heapq.heappush(queue, (new_dist + abs(neighbor[0] - goal[0]) + abs(neighbor[1] - goal[1]), neighbor))
    return distances

# Move Turtle 1 using A* algorithm
def move_player():
    start = (player.xcor(), player.ycor())
    goal = (exit.xcor(), exit.ycor())
    obstacle_positions = [(obstacle.xcor(), obstacle.ycor()) for obstacle in obstacles]
    distances = a_star(start, goal, obstacle_positions)
    path = []
    current = goal
    while current != start:
        path.append(current)
        min_dist = float('inf')
        best_neighbor = None
        for direction in [(20, 0), (-20, 0), (0, 20), (0, -20)]:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if -400 <= neighbor[0] <= 400 and -300 <= neighbor[1] <= 300:
                if neighbor not in path and distances.get(neighbor, float('inf')) < min_dist:
                    min_dist = distances.get(neighbor, float('inf'))
                    best_neighbor = neighbor
        current = best_neighbor
    path.append(start)
    path.reverse()
    for position in path:
        player.goto(position)
        window.update()
        time.sleep(0.1)  # Pause for 0.1 seconds

# Turtle 2 (Dijkstra's algorithm)
player2 = turtle.Turtle()
player2.speed(5)
player2.shape("turtle")
player2.color("blue")
player2.penup()
player2.goto(-380, 0)

# Dijkstra's algorithm
def dijkstra(start, goal, obstacles):
    graph = {}
    for i in range(-400, 401, 20):
        for j in range(-300, 301, 20):
            if any(abs(i - obs[0]) < 20 and abs(j - obs[1]) < 20 for obs in obstacles):
                graph[(i, j)] = float('inf')
            else:
                graph[(i, j)] = 20

    queue = [(0, start)]
    distances = {start: 0}
    while queue:
        (dist, current) = heapq.heappop(queue)
        if current == goal:
            break
        for direction in [(20, 0), (-20, 0), (0, 20), (0, -20)]:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if -400 <= neighbor[0] <= 400 and -300 <= neighbor[1] <= 300:
                new_dist = distances[current] + graph[neighbor]
                if new_dist < distances.get(neighbor, float('inf')):
                    distances[neighbor] = new_dist
                    heapq.heappush(queue, (new_dist, neighbor))
    return distances

# Move Turtle 2 using Dijkstra's algorithm
def move_player2():
    start = (player2.xcor(), player2.ycor())
    goal = (exit.xcor(), exit.ycor())
    obstacle_positions = [(obstacle.xcor(), obstacle.ycor()) for obstacle in obstacles]
    distances = dijkstra(start, goal, obstacle_positions)
    path = []
    current = goal
    while current != start:
        path.append(current)
        min_dist = float('inf')
        best_neighbor = None
        for direction in [(20, 0), (-20, 0), (0, 20), (0, -20)]:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if -400 <= neighbor[0] <= 400 and -300 <= neighbor[1] <= 300:
                if neighbor not in path and distances.get(neighbor, float('inf')) < min_dist:
                    min_dist = distances.get(neighbor, float('inf'))
                    best_neighbor = neighbor
        current = best_neighbor
    path.append(start)
    path.reverse()
    for position in path:
        player2.goto(position)
        window.update()
        time.sleep(0.1)  # Pause for 0.1 seconds

# Main loop
start_time = time.time()
move_player()
end_time = time.time()
time1 = end_time - start_time
print("Turtle 1 took", time1, "seconds to reach the exit")
timer1.clear()
timer1.write(f"Turtle 1 Time: {time1:.2f}s", align="center", font=("Arial", 16, "normal"))

start_time = time.time()
move_player2()
end_time = time.time()
time2 = end_time - start_time
print("Turtle 2 took", time2, "seconds to reach the exit")
timer2.clear()
timer2.write(f"Turtle 2 Time: {time2:.2f}s", align="center", font=("Arial", 16, "normal"))

result_message = "Turtle 1 is faster!" if time1 < time2 else "Turtle 2 is faster!"

# Display result message
result_turtle = turtle.Turtle()
result_turtle.hideturtle()
result_turtle.penup()
result_turtle.goto(0, 0)
result_turtle.write(result_message, align="center", font=("Arial", 24, "normal"))

# Keep the window open
window.mainloop()
