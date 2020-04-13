from tasks.paired_assoc import PairedAssociatesSimulation

if __name__ == '__main__':

    # one simulation
    # env = Environment()
    # task = PairedAssociatesTask(env)
    # agent = PairedAssociatesAgent(env)
    # World(task, agent).run(1590)

    # multiple simulations
    n = 10
    print('Running {} simulations...'.format(n))
    PairedAssociatesSimulation().run(n=n, output=True)
