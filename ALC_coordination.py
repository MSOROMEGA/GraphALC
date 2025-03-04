# -*- coding: utf-8 -*-
# Making this is not easy, please indicate the source when reprinting
# Source: Hainan Huang, hhn0113@outlook.com
import sys
sys.path.append('core')
import node1.node_1, node2.node_2, node3.node_3, node4.node_4, node5.node_5,node6.node_6,node7.node_7
import core.galc_methods as amt
import run_GALC
import result_display

# Import model
node_1, node_2, node_3, node_4, node_5, node_6, node_7  \
= node1.node_1.node_1(), node2.node_2.node_2(), node3.node_3.node_3(), node4.node_4.node_4(), node5.node_5.node_5(), node6.node_6.node_6(), node7.node_7.node_7()
node_sequnce = [1, 2, 3, 4, 5, 6, 7]
node_list = [eval('node_{}'.format(i)) for i in node_sequnce]
scemode = 'MLV-S1' # Problem-Scenario: MLV-S1, MLV-S2, MLV-S3
experiment = 5 # Information sharing level: 5,4,3,2,1,0
ISmode = 'US' # Information sharing structure: US, UDS, CS, DS
DSmode = 'BSC' # Decision coordination network: BSC, BASC, BPSC, CC
for i in node_sequnce:
    eval('node_{}'.format(i)).DSmode = DSmode
    eval('node_{}'.format(i)).ISmode = ISmode
    eval('node_{}'.format(i)).experiment = experiment
    eval('node_{}'.format(i)).scemode = scemode
# RUN GALC
w0 = {'BSC':0.03, 'BASC':30, 'BPSC':0.05, 'CC':0.1,} # Initial penalty coefficient
run_GALC.run_GALC(
    node_list, 
    node_sequnce, 
    Algorithm = amt.ORIGIN(), 
    outerloop_num = 500, 
    inner_loop_num = 10, 
    inner_loop_threshold = 0.001, 
    outer_loop_threshold = 0.1, 
    outer_loop_consistency_threshold = 0.1, 
    beta = 1, 
    w0 = w0[DSmode],
    v0 = 0,
    cpl0 = 0,
    )
result_display.result_display(node_list)
