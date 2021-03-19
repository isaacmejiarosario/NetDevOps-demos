import os
from pyats.easypy import run


def main(runtime):
    runtime.job.name = 'MPLS_TEST'
    script_path = os.path.dirname(os.path.abspath(__file__))
    ospf_test = os.path.join(script_path, 'ospf_test.py')
    run(testscript = ospf_test, runtime = runtime)
    #run(testscript = 'script_two.py', runtime = runtime)





""" access runtime information, such as runtime directory eg, save a new file into runtime directory"""
    #with open(os.path.join(runtime.directory, 'my_file.txt')) as f:
        #f.write('some content')



