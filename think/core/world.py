from .process import Process


class Task(Process):

    def __init__(self, agent, name="task"):
        super().__init__("task", clock=agent.clock)
        self.agent = agent


class World:

    def __init__(self, *processes):
        self.processes = processes
        if len(self.processes) > 0:
            p0 = self.processes[0]
            for p in self.processes[1:]:
                p.clock = p0.clock        

    def run(self, time=300):
        if len(self.processes) > 0:
            p0 = self.processes[0]
            for p in self.processes[1:]:
                p0.run_thread(lambda: p.run(time=time))
            p0.run(time=time)
            p0.wait_for_all()
