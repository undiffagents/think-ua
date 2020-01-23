# %% Main Task
# CK 2020-01-23
# Updated logging:
# 'do_outlog = True' (first line in main code), logging is sent to a textfile (named 'log#.txt', # = number of existing logs + 1) in the logs folder (logs/).
# 'do_outlog = False' defaults back to original script design (logs to console)

from tasks.pvt import OWL_INSTRUCTIONS, PVTTask
from think import World
from ua import OWLUndifferentiatedAgent
import logging
from think.core.logger import get_think_logger
import os, importlib, glob #directory pathing, reload modules, filename globbing



if __name__ == "__main__":
    
    do_outlog = True    #indicator: log to a textfile (or not)
    psep = os.path.sep  #path separator of current OS
    
    if do_outlog:
        #should be robust across computers and OSes
        logdir = os.path.realpath("logs" + psep) + psep
        curlog = logdir + "log" + str( 1+len(glob.glob(logdir + "log*.txt")) ) + ".txt"
        thinklog = get_think_logger(logfilename=curlog, uselogfile=True)
        
        agent = OWLUndifferentiatedAgent(output=thinklog)
        task = PVTTask(agent, instructions=OWL_INSTRUCTIONS)
        World(task, agent).run(100)
        
        #shutdown and reset logging - faster to implement than updating/fixing handlers between executions. Also ensures no cross-contamination of logging configuration across multiple executions (if the logging gets more complex in the future)
        logging.shutdown();  importlib.reload(logging)
    
    else:
        #original pvt_owl.py code
        agent = OWLUndifferentiatedAgent()
        task = PVTTask(agent, instructions=OWL_INSTRUCTIONS)
        World(task, agent).run(100)
    
    
    


# %%
#comparison of instructions for ease of ref
    
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





