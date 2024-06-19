import time
import threading
import queue

# this is the thread kill value
sentinel = object()


class Object:
    def __init__(self):
        self.x = 0
        self.y = 0


class Agent(Object):
    def __init__(self):
        super().__init__()
        self.speed_x = 0
        self.speed_y = 0

    def move(self):
        pass


class Player(Agent):
    def __init__(self):
        super().__init__()
        pass


def game_loop(message_queue):
    player = Player()
    last_frame_time = time.time()
    fps = 60
    message = []

    while True:
        # a way to receive messages without blocking
        while message_queue.qsize():
            message.append(message_queue.get())

        if message and message[0] is sentinel:
            break
        elif message and message[0] == "move":
            player.speed_y = 1
        elif message and message[0] == "pos":
            print("X: ", player.x, ", Y: ", player.y)
            print("> ", end="", flush=True)

        current_time = time.time()
        # dt is the time delta in seconds (float).
        dt = current_time - last_frame_time
        last_frame_time = current_time

        sleep_time = 1./fps - (current_time - last_frame_time)
        if sleep_time > 0:
            time.sleep(sleep_time)

        game_logic(player, dt)

        # remove commands from the queue so they don't all pile up
        message.clear()


def game_logic(player, dt):
    # Where speed might be a vector. E.g speed.x = 1 means
    # you will move by 1 unit per second on x's direction.
    player.x = player.x + player.speed_x * dt
    player.y = player.y + player.speed_y * dt


def main_loop():
    game_loop_messages = queue.Queue()
    game_thread = threading.Thread(target=game_loop, args=(game_loop_messages,))
    game_thread.start()

    while True:
        command = input("> ")
        if command == "q" or command == "quit" or command == "exit":
            game_loop_messages.put(sentinel)
            game_thread.join()
            return
        elif command == "move":
            game_loop_messages.put("move")
        elif command == "pos":
            game_loop_messages.put("pos")


if __name__ == '__main__':
    main_loop()
