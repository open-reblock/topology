import logging
import timeit 
import subprocess
from graph import my_graph as mg
from graph import my_graph_helpers as mgh

NUMBER_RUNS       = 10
DEFAULT_THRESHOLD = 1
DEFAULT_BLOCKING  = True

def get_git_hash():
    return subprocess.check_output(["git", "describe", "--always"]).strip()

def test_case(filename, name):
    logger = logging.getLogger()
    logger.disabled = True
    graph = mgh.import_and_setup(filename=filename, 
        threshold=DEFAULT_THRESHOLD, 
        byblock=DEFAULT_BLOCKING, 
        name=name,
        logger=logger)
    return len(graph.connected_components())

def main(names): 
    git_hash = get_git_hash()
    for name in names:
        print git_hash, name,
        blocks = test_case("data/" + name, name)
        time_taken = min(timeit.repeat(
            'test_case("data/" + name, name)', 
            setup='from __main__ import test_case; name = "%s"' % name, 
            repeat=NUMBER_RUNS,
            number=1))
        print blocks, time_taken, blocks/time_taken

if __name__ == '__main__':
    names = [
        'Phule_Nagar_v6',
        'Epworth_Before',
        'Epworth_demo',
        'Las_Vegas',
        'NYC',
        'Prague',
        'CapeTown'
    ]
    main(names)
