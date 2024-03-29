MAZE = """
    #. #######
    #  #     #
    #  #  #  #
    #     #  #
    #  ##### #
    #  #     *
    ##########
"""

# Environment elements
START = '.'
GOAL = '*'
WALL = '#'

# Rewards
REWARD_OUT = -5
REWARD_WALL = -2
REWARD_EMPTY = -1
REWARD_GOAL = 10

# Possible actions
UP = 'U'
DOWN = 'D'
RIGHT = 'R'
LEFT = 'L'
ACTIONS = [UP, DOWN, RIGHT, LEFT]

LEARNING_RATE = 1
DISCOUNT_FACTOR = 0.5

class Environment:
    def __init__(self, text):
        self.__states = {}

        # Environment parsing
        lines = list(map(lambda x: x.strip(), text.strip().split('\n')))
        for row in range(len(lines)):
            for col in range(len(lines[row])):
                self.__states[(row, col)] = lines[row][col]
                if lines[row][col] == GOAL:
                    self.__goal = (row, col)
                if lines[row][col] == START:
                    self.__start = (row, col)

    @property
    def start(self):
        return self.__start

    @property
    def goal(self):
        return self.__goal

    @property
    def states(self):
        return self.__states.keys()

    # Appliquer une action sur l'environnement
    # On met à jour l'état de l'agent, on lui donne sa récompense
    def apply(self, agent, action):
        state = agent.state
        new_state = (-1, -1)
        if action == UP:
            new_state = (state[0] - 1, state[1])
        if action == DOWN:
            new_state = (state[0] + 1, state[1])
        if action == LEFT:
            new_state = (state[0], state[1] - 1)
        if action == RIGHT:
            new_state = (state[0], state[1] + 1)

        # Calcul recompense agent et lui transmettre
        if new_state in self.__states:
            if self.__states[new_state] in [WALL, START]:
                reward = REWARD_WALL
            elif self.__states[new_state] == GOAL:
                reward = REWARD_GOAL
            else:
                reward = REWARD_EMPTY
            state = new_state
        else:
            reward = REWARD_OUT
        agent.update(action, state, reward)
        return reward

class Agent:
    def __init__(self, environment):
        self.__env = environment
        self.__state = environment.start
        self.__score = 0
        self.__last_action = None
        self.__qtable = {}

        # QTable initialization
        for s in environment.states:
            self.__qtable[s] = {}
            for a in ACTIONS:
                self.__qtable[s][a] = 0.0

    def update(self, action, new_state, reward):
        # QTable update
        # Q(s, a) <- Q(s, a) + learning_rate * [reward + discount_factor * max(qtable[a]) - Q(s, a)]
        maxQ = max(self.__qtable[new_state].values())
        # Moved in constants
        # LEARNING_RATE = 1
        # DISCOUNT_FACTOR = 0.5

        self.__qtable[self.__state][action] += LEARNING_RATE * \
                        (reward + DISCOUNT_FACTOR * maxQ - self.__qtable[self.__state][action])

        self.__state = new_state
        self.__score += reward
        self.__last_action = action

    # Best action who maximise reward
    def best_action(self):
        possible_rewards = self.__qtable[self.__state]
        best = None
        for a in possible_rewards:
            if best is None or possible_rewards[a] > possible_rewards[best]:
                best = a
        return best

    @property
    def state(self):
        return self.__state

    @property
    def score(self):
        return self.__score

    @property
    def qtable(self):
        return self.__qtable

    def reset(self):
        self.__state = self.__env.start
        self.__score = 0
        self.__last_action = None

def play(agent, environement):
    iteration = 0
    while agent.state != environement.goal:
        iteration += 1
        action = agent.best_action()
        # print(action)
        reward = environement.apply(agent, action)
        # print(iteration, agent.state, agent.score, reward)
        # print(agent.qtable)
    print(iteration, agent.score)
    # print()

if __name__ == '__main__':
    env = Environment(MAZE)
    print(env.states)

    agent = Agent(env)

    for i in range(40):
        play(agent, env)
        agent.reset()
