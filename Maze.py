MAZE = """
    #. #######
    #  #     #
    #  #  #  #
    #     #  #
    #  ##### #
    #  #     *
    ##########
"""

START = '.'
GOAL = '*'
WALL = '#'

REWARD_BORDER = -2
REWARD_EMPTY = -1
REWARD_GOAL = 10
REWARD_OUT = -10

UP = 'U'
DOWN = 'D'
RIGHT = 'R'
LEFT = 'L'
ACTIONS = [UP, DOWN, RIGHT, LEFT]

class Environment:
    def __init__(self, text):
        self.__states = {}

        lines = list(map(lambda x: x.strip(), text.strip().split('\n')))

        for row in range(len(lines)):
            for col in range(len(lines[row])):
                self.__states[(row, col)] = lines[row][col]
                if lines[row][col] == GOAL:
                    self.__goal = (row, col)
                if lines[row][col] == START:
                    self.__start = (row, col)

        #print(self.__states[(0, 1)])

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
                reward = REWARD_BORDER
            elif self.__states[new_state] == GOAL:
                reward = REWARD_GOAL
            else:
                reward = REWARD_EMPTY
            state = new_state
        else:
            reward = REWARD_OUT
        agent.update(state, reward)

class Agent:
    def __init__(self, environment):
        self.__state = environment.start
        self.__score = 0
        self.__last_action = None
        self.__qtable = {}

        for s in environment.states:
            self.__qtable[s] = {}
            for a in ACTIONS:
                self.__qtable[s][a] = 0.0

    def update(self, new_state, reward):
        self.__state = new_state
        self.__score += reward

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

if __name__ == '__main__':
    env = Environment(MAZE)
    print(env.states)

    agent = Agent(env)
    print(agent.state, agent.score)
    env.apply(agent, DOWN)
    print(agent.state, agent.score)

    env.apply(agent, UP)
    print(agent.state, agent.score)
    env.apply(agent, UP)
    print(agent.state, agent.score)
