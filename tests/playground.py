#ORIGINAL:
#OWL_INSTRUCTIONS = [
#    'task(Psychomotor-Vigilance)',
#    'button(Acknowledge)',
#    'box(Box)',
#    'target(Target)',
#    'letter(Letter)',
#    'subject(Subject)',
#    'isPartOf(Box,Psychomotor-Vigilance)',
#    'isPartOf(Target,Psychomotor-Vigilance)',
#    'isPartOf(Letter,Target)',
#    # 'hasProperty(Psychomotor-Vigilance,active)=>appearsIn(Target,Box)',
#    'appearsIn(Target,Box)=>click(Subject,Acknowledge),remember(Subject,Letter)',
#    'done(Psychomotor-Vigilance)'
#]

#PROCESSED:
#task(Psychomotor-vigilance)
#button(Acknowledge)
#box(Box)
#target(Target)
#isPartOf(Acknowledge,Psychomotor-vigilance)
#isPartOf(Box,Psychomotor-vigilance)
#isPartOf(Target,Psychomotor-vigilance)
#target(X) => letter(X)
#appearsIn(Target,Box) => click(Subject,Acknowledge),remember(Subject,Target)
#hasProperty(Psychomotor-vigilance,Active) => appearsIn(Target,Box)
#done(Psychomotor-vigilance)


# %% Tester

# %% Main Task
from tasks.pvt import OWL_INSTRUCTIONS, PVTTask
#from tasks.pvt import PVTTask
from think import World
from ua import OWLUndifferentiatedAgent
from core.logger import get_think_logger
import logging



if __name__ == "__main__":
#    thinklog = get_think_logger(logfilename="outfile.txt", uselogfile=True)
#    agent = OWLUndifferentiatedAgent(output=thinklog)
    agent = OWLUndifferentiatedAgent()
    task = PVTTask(agent, instructions=OWL_INSTRUCTIONS)
    World(task, agent).run(100)
    logging.shutdown()

#sys.stdout = ogout
    
#    for line in owlin:
#        if not ' ' in line:
#            if 'object'in line:
#                objs.append(parseObjectLine(line))
#                unnamedFacts.append(objs[-1][1])
#            elif 'named' in line or 'string' in line:
#                preds.append(parsePredicateLine(line))