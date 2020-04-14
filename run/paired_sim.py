from tasks.paired_assoc import PairedAssociatesSimulation

if __name__ == '__main__':
    n = 5
    print('Running {} simulations...'.format(n))
    PairedAssociatesSimulation().run(n=n, output=False)
