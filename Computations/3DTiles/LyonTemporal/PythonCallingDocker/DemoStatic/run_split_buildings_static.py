import os
import sys
import logging
import demo_workflow_static as workflow

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from run import run_demo_split_buildings


if __name__ == '__main__': 
    split = workflow.demo_split
    run_demo_split_buildings(split)
