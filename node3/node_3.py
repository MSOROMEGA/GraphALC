# -*- coding: utf-8 -*-
# Making this is not easy, please indicate the source when reprinting
# Source: Hainan Huang, hhn0113@outlook.com
import sys
import os
sys.path.append('core')
import numpy as np
import gurobipy as gp
from gurobipy import GRB
import node_methods as nmt

class node_3(): 
    def __init__(self):
        self.mutipler_list = []
        self.penalty_list = []
        self.receive_list = []
        self.node_id = 3
        self.DSmode = 'BSC'
        self.scemode = 'MLV-S3'
        self.ISmode = 'UDS'
        self.experiment = 5
        
    def infomation_sharing(self, ISmode, m):
        if ISmode == 'CS':# Centralized  sharing
            self.info_sending_list = [
                [],#1
                [],#2
                [],#3
                [],#4
                [],#5
                [],#6
                [self.experiment],#7
                ]
            self.info_receiving_list = [
                [],#1
                [],#2
                [],#3
                [],#4
                [],#5
                [],#6
                [],#7
                ]     
        
        elif ISmode == 'DS':# Downstream sharing
            self.info_sending_list = [
                [self.experiment],#1
                [self.experiment],#2
                [],#3
                [self.experiment],#4
                [],#5
                [],#6
                [],#7
                ]
            self.info_receiving_list = [
                [],#1
                [],#2
                [],#3
                [self.experiment],#4
                [self.experiment],#5
                [self.experiment],#6
                [],#7
                ]     
            
        elif ISmode == 'US':# Upstream sharing
            self.info_sending_list = [
                [],#1
                [],#2
                [],#3
                [self.experiment],#4
                [self.experiment],#5
                [self.experiment],#6
                [],#7
                ]
            self.info_receiving_list = [
                [self.experiment],#1
                [self.experiment],#2
                [],#3
                [self.experiment],#4
                [],#5
                [],#6
                [],#7
                ]     
        
        elif ISmode == 'UDS':# Upstream and downstream sharing
            self.info_sending_list = [
                [self.experiment],#1
                [self.experiment],#2
                [],#3
                [self.experiment],#4
                [self.experiment],#5
                [self.experiment],#6
                [],#7
                ]
            self.info_receiving_list = [
                [self.experiment],#1
                [self.experiment],#2
                [],#3
                [self.experiment],#4
                [self.experiment],#5
                [self.experiment],#6
                [],#7
                ]     
        
        m.update()
        new_obj_all = 0
        for nodeisend,nodeisendlist in enumerate(self.info_receiving_list):
            if nodeisendlist == []:
                continue
            temp_model = nmt.infomation_sharing_content(node_id=nodeisend+1,fname=self.scemode,i=nodeisendlist[0])
            
            variable_map = {}  
            for var in temp_model.getVars():
                if var.VarName in [v.VarName for v in m.getVars()]:
                    variable_map[var] = m.getVarByName(var.VarName)
                    continue
                new_var = m.addVar(
                    lb=var.lb,
                    ub=var.ub,
                    obj=var.obj,
                    vtype=var.VType,
                    name=var.VarName
                )
                variable_map[var] = new_var
            m.update()
            
            for c in temp_model.getConstrs():
                lhs = temp_model.getRow(c)  
                new_lhs = 0
                for i in range(lhs.size()):
                    coeff = lhs.getCoeff(i)
                    var = lhs.getVar(i)
                    new_lhs += coeff * variable_map[var]  
                rhs = c.RHS
                sense = c.Sense
                m.addLConstr(new_lhs, sense, rhs, name=c.ConstrName)
            gen_constrs = temp_model.getGenConstrs()
            for gc in gen_constrs:
                constr_type = gc.GenConstrType
                constr_name = gc.GenConstrName
                Outputvar, Inputvars, constant = temp_model.getGenConstrMin(gc)
                m.addGenConstrMin(variable_map[Outputvar], [variable_map[v] for v in Inputvars], constant=constant, name=constr_name)
            m.update()
            
            temp_new_obj = temp_model.getObjective()
            new_obj = 0
            if isinstance(temp_new_obj, gp.LinExpr):
                for i in range(temp_new_obj.size()):
                    coeff = temp_new_obj.getCoeff(i) 
                    var = temp_new_obj.getVar(i)     
                    new_obj += coeff * variable_map[var]  
                
            elif isinstance(temp_new_obj, gp.QuadExpr):
                lin_obj = temp_new_obj.getLinExpr()
                for i in range(lin_obj.size()):
                    coeff = lin_obj.getCoeff(i)  
                    var = lin_obj.getVar(i)      
                    new_obj += coeff * variable_map[var]  
                for i in range(temp_new_obj.size()):
                    coeff = temp_new_obj.getCoeff(i)  
                    var1 = temp_new_obj.getVar1(i)    
                    var2 = temp_new_obj.getVar2(i)    
                    new_obj += coeff * variable_map[var1] * variable_map[var2]
            new_obj_all += new_obj
            m.update()
        for nodeisend,nodeisendlist in enumerate(self.info_sending_list):
            if nodeisendlist == []:
                continue
            temp_model = nmt.infomation_sharing_content(node_id=self.node_id,fname=self.scemode,i=nodeisendlist[0])
            variable_map = {}  
            for var in temp_model.getVars():
                if var.VarName in [v.VarName for v in m.getVars()]:
                    variable_map[var] = m.getVarByName(var.VarName)
                    continue
                new_var = m.addVar(
                    lb=var.lb,
                    ub=var.ub,
                    obj=var.obj,
                    vtype=var.VType,
                    name=var.VarName
                )
                variable_map[var] = new_var
            m.update()            
            temp_new_obj = temp_model.getObjective()
            new_obj = 0
            if isinstance(temp_new_obj, gp.LinExpr):
                for i in range(temp_new_obj.size()):
                    coeff = temp_new_obj.getCoeff(i)  
                    var = temp_new_obj.getVar(i)      
                    new_obj += coeff * variable_map[var]  
                
            elif isinstance(temp_new_obj, gp.QuadExpr):
                lin_obj = temp_new_obj.getLinExpr()
                for i in range(lin_obj.size()):
                    coeff = lin_obj.getCoeff(i)  
                    var = lin_obj.getVar(i)      
                    new_obj += coeff * variable_map[var]  
                for i in range(temp_new_obj.size()):
                    coeff = temp_new_obj.getCoeff(i)  
                    var1 = temp_new_obj.getVar1(i)    
                    var2 = temp_new_obj.getVar2(i)    
                    new_obj += coeff * variable_map[var1] * variable_map[var2]
            new_obj_all -= new_obj
        return new_obj_all

    def decision_coordination(self, DSmode,var):
        x_sfj_list = var['x_sfj'].select('*', 'F1', '*')
        x_fdj_list = var['x_fdj'].select('F1', '*', '*')
        zm1_ffj_list = var['zm1_ffj'].select('*', '*', '*')
        zm2_ffj_list = var['zm2_ffj'].select('*', '*', '*')
        f3t1 = var['x_sfj'].select('S1', 'F1', '*')
        f3t2 = var['x_sfj'].select('S2', 'F1', '*')
        f3t4 = zm1_ffj_list + zm2_ffj_list
        f3t5 = var['x_fdj'].select('F1', 'D1', '*')
        f3t6 = var['x_fdj'].select('F1', 'D2', '*')
        
        if DSmode == 'CC': # Centralized coordination            
            # send_column
            cs1 = []
            cs2 = []
            cs3 = []
            cs4 = []
            cs5 = []
            cs6 = []
            cs7 = []
            # receive_column
            cr1 = []
            cr2 = []
            cr3 = []
            cr4 = []
            cr5 = []
            cr6 = []
            cr7 = x_sfj_list+x_fdj_list+zm1_ffj_list+zm2_ffj_list 
        elif DSmode == 'BSC': # Bidirectional symmetric coordination            
            # send_column
            cs1 = f3t1
            cs2 = f3t2
            cs3 = []
            cs4 = f3t4
            cs5 = f3t5
            cs6 = f3t6
            cs7 = []
            # receive_column
            cr1 = f3t1
            cr2 = f3t2
            cr3 = []
            cr4 = f3t4
            cr5 = f3t5
            cr6 = f3t6
            cr7 = []
        elif DSmode == 'BPSC': # Bidirectional partially symmetric coordination            
            # send_column
            cs1 = var['x_sfj'].select('S1', 'F1', '*')
            cs2 = var['x_sfj'].select('S2', 'F1', '*')
            cs3 = []
            cs4 = zm1_ffj_list + zm2_ffj_list
            cs5 = [var['x_fdj'].select('F1', 'D1', 'J1')]
            cs6 = [var['x_fdj'].select('F1', 'D2', 'J2')]
            cs7 = []
            # receive_column
            cr1 = [f3t1[0]]
            cr2 = [f3t2[0]]
            cr3 = []
            cr4 = zm1_ffj_list + zm2_ffj_list
            cr5 = f3t5
            cr6 = f3t6
            cr7 = []
        elif DSmode == 'BASC': # Bidirectional asymmetric coordination
            # send_column
            cs1 = [f3t1[1]]
            cs2 = [f3t2[1]]
            cs3 = []
            cs4 = zm1_ffj_list
            cs5 = [f3t5[0]]
            cs6 = [f3t6[0]]
            cs7 = []
            # receive_column
            cr1 = [f3t1[0]]
            cr2 = [f3t2[0]]
            cr3 = []
            cr4 = zm2_ffj_list
            cr5 = [f3t5[1]]
            cr6 = [f3t6[1]]
            cr7 = []
            
        coupling_send_list = np.array([
            np.array([cs1,cr1],dtype=object),#1
            np.array([cs2,cr2],dtype=object),#2
            np.array([cs3,cr3],dtype=object),#3
            np.array([cs4,cr4],dtype=object),#4
            np.array([cs5,cr5],dtype=object),#5
            np.array([cs6,cr6],dtype=object),#6
            np.array([cs7,cr7],dtype=object),#7
            np.array([],dtype=object),#
            ],dtype=object)
        coupling_receive_list = np.array([
            np.array([cr1,cs1],dtype=object),#1
            np.array([cr2,cs2],dtype=object),#2
            np.array([cr3,cs3],dtype=object),#3
            np.array([cr4,cs4],dtype=object),#4
            np.array([cr5,cs5],dtype=object),#5
            np.array([cr6,cs6],dtype=object),#6
            np.array([cr7,cs7],dtype=object),#7
            np.array([],dtype=object),#
            ],dtype=object)
               
        obj_augmented_penalty,self.receive_list,self.mutipler_list,self.penalty_list = nmt.penalty_function(coupling_receive_list,self.receive_list,self.mutipler_list,self.penalty_list,self.node_id,coupling_send_list)
        return obj_augmented_penalty, coupling_receive_list, coupling_send_list

    def scenario(self,id):
        modelname = id
        if id == 'MLV-S1':
            processing1_capacity = dict({
                })
            processing2_capacity = dict({
                })
            manufacturing1_capacity = dict({
                'F1': 60*5,
                })
            manufacturing2_capacity = dict({
                'F1': 380*5,
                })
        elif id == 'MLV-S2':
            processing1_capacity = dict({
                })
            processing2_capacity = dict({
                })
            manufacturing1_capacity = dict({
                'F1': 70*5,
                })
            manufacturing2_capacity = dict({
                'F1': 380*5,
                })            
        elif id == 'MLV-S3':
            processing1_capacity = dict({
                })
            processing2_capacity = dict({
                })
            manufacturing1_capacity = dict({
                'F1': 220*5,
                })
            manufacturing2_capacity = dict({
                'F1': 380*5,
                })
            
        suppliers_dict = dict({
            'S1': 000,
            'S2': 000,
            })

        factories_dict = dict({
            'F1': 000,
            })

        depots_dict = dict({
            'D1': 220*5,
            'D2': 220*5,
            })

        customers_dict = dict({
            })

        products_dict = dict({
            'J1': 000,
            'J2': 000})

        customers_product_dict = dict({
            })

        processing1_rate = dict({
            })
        processing2_rate = dict({
            })
        manufacturing1_rate = dict({
            'J1': 1.5,
            'J2': 0.5,
            })
        manufacturing2_rate = dict({
            'J1': 0.8,
            'J2': 1.2,
            })

        arcs_sfj,cost_sfj = gp.multidict({
            ('S1', 'F1', 'J1'): 1.0,
            ('S1', 'F1', 'J2'): 1.2,
            ('S2', 'F1', 'J1'): 1.5,
            ('S2', 'F1', 'J2'): 1.7,
            })

        arcs_fdj,cost_fdj = gp.multidict({
            ('F1', 'D1', 'J1'): 1.0,
            ('F1', 'D1', 'J2'): 1.5,
            ('F1', 'D2', 'J1'): 1.2,
            ('F1', 'D2', 'J2'): 1.7,
            })

        arcs_dcj,cost_dcj = gp.multidict({():00,
            })


        _,processing1_cost = gp.multidict({():00,
            })
        _,processing2_cost = gp.multidict({():00,
            })
        _,manufacturing1_cost = gp.multidict({
            ('F1','J1'): 1.5,
            ('F1','J2'): 1.3,
            })
        _, manufacturing2_cost = gp.multidict({
            ('F1','J1'): 1.5,
            ('F1','J2'): 1.9,
            })

        arcs_ssj= [
            ]
        
        arcs_ssj_out,LScost_ssj_out = gp.multidict({():00,
            })
        
        arcs_ffj = [
            ('F1', 'F2', 'J1'),
            ('F1', 'F2', 'J2'),
            ('F2', 'F1', 'J1'),
            ('F2', 'F1', 'J2'),
            ]
        
        arcs_ffj_out,LFcost_ffj_out = gp.multidict({
            ('F1', 'F2', 'J1'): 0.6,
            ('F1', 'F2', 'J2'): 0.55,
            })
        
        return \
            processing1_capacity,processing2_capacity,manufacturing1_capacity,manufacturing2_capacity,\
            processing1_cost,processing2_cost,manufacturing1_cost,manufacturing2_cost,\
            processing1_rate,processing2_rate,manufacturing1_rate,manufacturing2_rate,\
            arcs_ssj,arcs_ssj_out,LScost_ssj_out,arcs_ffj,arcs_ffj_out,LFcost_ffj_out,\
            arcs_sfj,cost_sfj,arcs_fdj,cost_fdj,arcs_dcj,cost_dcj,\
            suppliers_dict,factories_dict,depots_dict,customers_dict,products_dict,customers_product_dict,\
            modelname,\
        
    def decision_model(self):
        _,_,manufacturing1_capacity,manufacturing2_capacity,\
        _,_,manufacturing1_cost,manufacturing2_cost,\
        _,_,manufacturing1_rate,manufacturing2_rate,\
        _,_,_,arcs_ffj,arcs_ffj_out,LFcost_ffj_out,\
        arcs_sfj,_,arcs_fdj,cost_fdj,_,_,\
        _,factories_dict,depots_dict,_,products_dict,_,\
        modelname,\
        = self.scenario(self.scemode)
        
        m = gp.Model(modelname)
        
        factories = factories_dict.keys()
        depots = depots_dict.keys()
        products = products_dict.keys()
        x_sfj = m.addVars(arcs_sfj,lb=0, name="x_sfj", )
        x_fdj = m.addVars(arcs_fdj,lb=0, name="x_fdj", )
        zm1_ffj = m.addVars(arcs_ffj,lb=0, name="zm1_ffj")
        zm2_ffj = m.addVars(arcs_ffj,lb=0, name="zm2_ffj")
        
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        new_obj_all = self.infomation_sharing(self.ISmode, m)
        sys.stdout = original_stdout
        
        m.addConstrs((gp.quicksum(x_fdj.select(factory, depot, product)[0] * manufacturing1_rate[product] for product in products for depot in depots  ) <= \
            manufacturing1_capacity[factory] + gp.quicksum(zm1_ffj.select('*', factory, '*')) - gp.quicksum(zm1_ffj.select(factory, '*', '*')) \
            for factory in factories), name="factory2")
        m.addConstrs((gp.quicksum(x_fdj.select(factory, depot, product)[0] * manufacturing2_rate[product] for product in products for depot in depots  ) <= \
            manufacturing2_capacity[factory] + gp.quicksum(zm2_ffj.select('*', factory, '*')) - gp.quicksum(zm2_ffj.select(factory, '*', '*')) \
            for factory in factories), name="factory3")
        m.addConstrs((gp.quicksum(zm1_ffj[arc] * manufacturing1_rate[arc[2]] for arc in arcs_ffj if factory == arc[0]) <= \
            max(0, manufacturing1_capacity[factory] - manufacturing2_capacity[factory]) \
            for factory in factories), name="factory4")
        m.addConstrs((gp.quicksum(zm2_ffj[arc] * manufacturing2_rate[arc[2]] for arc in arcs_ffj if factory == arc[0]) <= \
            max(0, manufacturing2_capacity[factory] - manufacturing1_capacity[factory]) \
            for factory in factories), name="factory5")
        m.addConstrs((gp.quicksum(x_fdj.select(factory,'*',product)) >= \
            gp.quicksum(zm1_ffj.select('*',factory,product)) * manufacturing1_rate[product] \
            for product in products for factory in factories), name="factory6")
        m.addConstrs((gp.quicksum(x_fdj.select(factory,'*',product)) >= \
            gp.quicksum(zm2_ffj.select('*',factory,product)) * manufacturing2_rate[product] \
            for product in products for factory in factories), name="factory7")
        
        m.addConstrs((gp.quicksum(x_fdj.select(factory, '*', product)) \
            == gp.quicksum(x_sfj.select('*', factory, product)) \
            for product in products for factory in factories), name="factory1")

        var = {'x_sfj':x_sfj, 'x_fdj':x_fdj, 'zm1_ffj':zm1_ffj, 'zm2_ffj':zm2_ffj}
        obj_augmented_penalty,coupling_receive_list,coupling_send_list = self.decision_coordination(DSmode=self.DSmode,var=var)
        
        factory_transport_cost = (gp.quicksum(x_fdj[arc] * cost_fdj[arc] for arc in arcs_fdj) )
        factory_latent_transpot_cost = (gp.quicksum(zm1_ffj[arc] * manufacturing1_rate[arc[2]] * LFcost_ffj_out[arc] + zm2_ffj[arc] * manufacturing2_rate[arc[2]] * LFcost_ffj_out[arc] for arc in arcs_ffj_out) )
        factory_latent_process_cost = (gp.quicksum(zm1_ffj[arc] * manufacturing1_rate[arc[2]] * manufacturing1_cost[arc[0],arc[2]] + zm2_ffj[arc] * manufacturing2_rate[arc[2]] * manufacturing2_cost[arc[0],arc[2]] for arc in arcs_ffj_out) )
        factory_manufacturing_cost =gp.quicksum( (gp.quicksum(x_fdj.select(factory,'*',product)) - gp.quicksum(zm1_ffj.select('*',factory,product)) * manufacturing1_rate[product]) * manufacturing1_cost[factory,product] + \
            (gp.quicksum(x_fdj.select(factory,'*',product)) - gp.quicksum(zm2_ffj.select('*',factory,product)) * manufacturing2_rate[product] ) * manufacturing2_cost[factory,product] for product in products for factory in factories )
        factory_objective = factory_transport_cost + factory_latent_transpot_cost + factory_latent_process_cost + factory_manufacturing_cost
        m.setObjective(factory_objective + obj_augmented_penalty + new_obj_all, GRB.MINIMIZE)
        
        m.setParam('OutputFlag', False)
        m.optimize()  
        self.optxv = [{key:x_sfj[key].x for key in x_sfj}, {key:x_fdj[key].x for key in x_fdj}, {key:zm1_ffj[key].x for key in zm1_ffj}, {key:zm2_ffj[key].x for key in zm2_ffj}]
        
        self.objVal = m.objVal
        try:
            self.pure_objVal = m.objVal - obj_augmented_penalty.getValue()
        except:
            self.pure_objVal = m.objVal - obj_augmented_penalty
        self.sending_list,self.consistency_list,self.coupling_receive_list_value_2 = nmt.return_penalty_result(coupling_receive_list, self.receive_list, coupling_send_list,self.node_id)
        
if __name__ == '__main__':
    node_3().decision_model() 
