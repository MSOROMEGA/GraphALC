import sys
sys.path.append('core')
import core.galc_methods as amt
import numpy as np

def run_GALC(node_list, node_sequnce, Algorithm, outerloop_num, inner_loop_num, inner_loop_threshold, outer_loop_threshold, outer_loop_consistency_threshold, beta, w0=1,v0=0,cpl0=0,c_old=[], obj_old=10000000000, inner_loop_count=0):    
    print('Initializing...')
    amt.alc_init(node_list,w0=w0,v0=v0,cpl0=cpl0)
    print('Initialization complete!')    
    obj_list = []
    c2_list = []
    for o in range(outerloop_num):
        for i in range(inner_loop_num):
            obj_now = amt.inner_loop_coordination(node_list, node_sequnce)
            inner_loop_count += 1
            # Convergence check
            print('  obj:', round(obj_now,1))
            if np.abs(obj_now - obj_old) / (np.abs(obj_now) + 1) <= inner_loop_threshold:
                print('🟢🌛Inner loop converged, number of iterations: {}'.format(i + 1), end='')
                break
            elif i == inner_loop_num - 1:
                print('🔴🌛Inner loop did not converge after {} iterations'.format(i + 1), end='')
                break
            obj_old = obj_now
        c_alllist, c_old_alllist, c_old = Algorithm.algorithm(node_list, o, beta, c_old)   
        # Convergence check
        fseable_convergence = np.linalg.norm(c_alllist)
        alm_convergence = np.linalg.norm(c_alllist - c_old_alllist)
        print(" Outer loop iteration:", o, " Inner loop iteration:", inner_loop_count, " obj:", round(obj_now), " Outer loop convergence 1:", round(alm_convergence,2), " Outer loop convergence 2:", round(fseable_convergence,2), '\n')
        obj_list.append(obj_now)
        c2_list.append(fseable_convergence)
        if alm_convergence <= outer_loop_threshold:
            if fseable_convergence <= outer_loop_consistency_threshold:
                print('🟢☀️Outer loop converged, number of iterations: {}'.format(o + 1))
                break
        if o == outerloop_num - 1:
            print('🔴☀️Outer loop did not converge after {} maximum iterations'.format(o + 1))
            break
            
