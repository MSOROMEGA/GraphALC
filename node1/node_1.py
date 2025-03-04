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

class node_1(): 
    def __init__(self):
        self.mutipler_list = []
        self.penalty_list = []
        self.receive_list = []
        self.node_id = 1
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
                [],#1
                [self.experiment],#2
                [],#3
                [],#4
                [],#5
                [],#6
                [],#7
                ]
            self.info_receiving_list = [
                [],#1
                [self.experiment],#2
                [self.experiment],#3
                [self.experiment],#4
                [],#5
                [],#6
                [],#7
                ]     
            
        elif ISmode == 'US':# Upstream sharing
            self.info_sending_list = [
                [],#1
                [self.experiment],#2
                [self.experiment],#3
                [self.experiment],#4
                [],#5
                [],#6
                [],#7
                ]
            self.info_receiving_list = [
                [],#1
                [self.experiment],#2
                [],#3
                [],#4
                [],#5
                [],#6
                [],#7
                ]     
        
        elif ISmode == 'UDS':# Upstream and downstream sharing
            self.info_sending_list = [
                [],#1
                [self.experiment],#2
                [self.experiment],#3
                [self.experiment],#4
                [],#5
                [],#6
                [],#7
                ]
            self.info_receiving_list = [
                [],#1
                [self.experiment],#2
                [self.experiment],#3
                [self.experiment],#4
                [],#5
                [],#6
                [],#7
                ]     
        
        m.update()
        new_obj_all = 0
        for nodeisend,nodeisendlist in enumerate(self.info_receiving_list):
            if nodeisendlist == []:
                continue
            variable_map = {}  
            temp_model = nmt.infomation_sharing_content(node_id=nodeisend+1,fname=self.scemode,i=nodeisendlist[0])
            
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
        x_sfj_list = var['x_sfj'].select('S1', '*', '*')
        zp1_ssj_list = var['zp1_ssj'].select('*', '*', '*')
        zp2_ssj_list = var['zp2_ssj'].select('*', '*', '*')
        x_13j_list = var['x_sfj'].select('S1', 'F1', '*')
        x_14j_list = var['x_sfj'].select('S1', 'F2', '*')
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
            cr7 = x_sfj_list+zp1_ssj_list+zp2_ssj_list
        elif DSmode == 'BSC': # Bidirectional symmetric coordination            
            # send_column
            cs1 = []
            cs2 = zp1_ssj_list+zp2_ssj_list
            cs3 = var['x_sfj'].select('S1', 'F1', '*')
            cs4 = var['x_sfj'].select('S1', 'F2', '*')
            cs5 = []
            cs6 = []
            cs7 = []
            # receive_column
            cr1 = []
            cr2 = [i for i in zp1_ssj_list+zp2_ssj_list]
            cr3 = [i for i in x_13j_list]
            cr4 = [i for i in x_14j_list]
            cr5 = []
            cr6 = []
            cr7 = []
        elif DSmode == 'BPSC': # Bidirectional partially symmetric coordination            
            # send_column
            cs1 = []
            cs2 = zp1_ssj_list+zp2_ssj_list
            cs3 = [x_13j_list[0]]
            cs4 = [x_14j_list[0]]
            cs5 = []
            cs6 = []
            cs7 = []
            # receive_column
            cr1 = []
            cr2 = zp1_ssj_list + zp2_ssj_list
            cr3 = x_13j_list
            cr4 = x_14j_list
            cr5 = []
            cr6 = []
            cr7 = []
        elif DSmode == 'BASC': # Bidirectional asymmetric coordination
            # send_column
            cs1 = []
            cs2 = [i for i in zp1_ssj_list]
            cs3 = [x_13j_list[0]]
            cs4 = [x_14j_list[0]]
            cs5 = []
            cs6 = []
            cs7 = []
            # receive_column
            cr1 = []
            cr2 = [i for i in zp2_ssj_list]
            cr3 = [x_13j_list[1]]
            cr4 = [x_14j_list[1]]
            cr5 = []
            cr6 = []
            cr7 = []
            
        coupling_send_list = np.array([
            np.array([cs1,cr1],dtype=object),#1
            np.array([cs2,cr2],dtype=object),#2
            np.array([cs3,cr3],dtype=object),#3
            np.array([cs4,cr4],dtype=object),#4
            np.array([cs5,cr5],dtype=object),#5
            np.array([cs6,cr6],dtype=object),#6
            np.array([cs7,cr7],dtype=object),#7
            np.array([],dtype=object),
            ],dtype=object)
        coupling_receive_list = np.array([
            np.array([cr1,cs1],dtype=object),#1
            np.array([cr2,cs2],dtype=object),#2
            np.array([cr3,cs3],dtype=object),#3
            np.array([cr4,cs4],dtype=object),#4
            np.array([cr5,cs5],dtype=object),#5
            np.array([cr6,cs6],dtype=object),#6
            np.array([cr7,cs7],dtype=object),#7
            np.array([],dtype=object),
            ],dtype=object)
               
        obj_augmented_penalty,self.receive_list,self.mutipler_list,self.penalty_list = nmt.penalty_function(coupling_receive_list,self.receive_list,self.mutipler_list,self.penalty_list,self.node_id,coupling_send_list)
        return obj_augmented_penalty, coupling_receive_list, coupling_send_list

    def scenario(self,id):
        modelname = id
        if id == 'MLV-S1':
            processing1_capacity = dict({
                'S1': 60*5,
                })
            processing2_capacity = dict({
                'S1': 380*5,
                })
            manufacturing1_capacity = dict({
                })
            manufacturing2_capacity = dict({
                })
        elif id == 'MLV-S2':
            processing1_capacity = dict({
                'S1': 50*5,
                })
            processing2_capacity = dict({
                'S1': 380*5,
                })
            manufacturing1_capacity = dict({
                })
            manufacturing2_capacity = dict({
                })            
        elif id == 'MLV-S3':
            processing1_capacity = dict({
                'S1': 220*5,
                })
            processing2_capacity = dict({
                'S1': 380*5,
                })
            manufacturing1_capacity = dict({
                })
            manufacturing2_capacity = dict({
                })
        suppliers_dict = dict({
            'S1': 000,
            })
        factories_dict = dict({
            'F1': 000,
            'F2': 000,
            })
        depots_dict = dict({
            })
        customers_dict = dict({
            })
        products_dict = dict({
            'J1': 000,
            'J2': 000})
        customers_product_dict = dict({
            })
        processing1_rate = dict({
            'J1': 1.0,
            'J2': 1.0})
        processing2_rate = dict({
            'J1': 1.5,
            'J2': 0.5})
        manufacturing1_rate = dict({
            })
        manufacturing2_rate = dict({
            })
        arcs_sfj,cost_sfj = gp.multidict({
            ('S1', 'F1', 'J1'): 1.0,
            ('S1', 'F1', 'J2'): 1.2,
            ('S1', 'F2', 'J1'): 2.0,
            ('S1', 'F2', 'J2'): 1.5,
            })
        arcs_fdj,cost_fdj = gp.multidict({():00,
            })
        arcs_dcj,cost_dcj = gp.multidict({():00,
            })
        _,processing1_cost = gp.multidict({
            ('S1','J1'): 1.0,
            ('S1','J2'): 2.0,
            })
        _,processing2_cost = gp.multidict({
            ('S1','J1'): 1.5,
            ('S1','J2'): 1.0,
            })
        _,manufacturing1_cost = gp.multidict({():00,
            })
        _, manufacturing2_cost = gp.multidict({():00,
            })
        arcs_ssj= [
            ('S1', 'S2', 'J1'),
            ('S1', 'S2', 'J2'),
            ('S2', 'S1', 'J1'),
            ('S2', 'S1', 'J2'),
            ]
        arcs_ssj_out,LScost_ssj_out = gp.multidict({
            ('S1', 'S2', 'J1'): 0.25,
            ('S1', 'S2', 'J2'): 0.4,
            })
        arcs_ffj = [
            ]
        arcs_ffj_out,LFcost_ffj_out = gp.multidict({():00,
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
        processing1_capacity,processing2_capacity,_,_,\
        processing1_cost,processing2_cost,_,_,\
        processing1_rate,processing2_rate,_,_,\
        arcs_ssj,arcs_ssj_out,LScost_ssj_out,_,_,_,\
        arcs_sfj,cost_sfj,_,_,_,_,\
        suppliers_dict,factories_dict,_,_,products_dict,_,\
        modelname,\
        = self.scenario(self.scemode)
        
        m = gp.Model(modelname)
        suppliers = suppliers_dict.keys()
        factories = factories_dict.keys()
        products = products_dict.keys()
        x_sfj = m.addVars(arcs_sfj,lb=0, name="x_sfj", )
        zp1_ssj = m.addVars(arcs_ssj,lb=0, name="zp1_ssj")
        zp2_ssj = m.addVars(arcs_ssj,lb=0, name="zp2_ssj")
        
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        new_obj_all = self.infomation_sharing(self.ISmode, m)
        sys.stdout = original_stdout
        
        m.addConstrs((gp.quicksum(x_sfj.select(supplier, factory, product)[0] * processing1_rate[product] for product in products for factory in factories) \
            <= processing1_capacity[supplier] + gp.quicksum(zp1_ssj.select('*', supplier, '*')) - gp.quicksum(zp1_ssj.select(supplier, '*', '*')) \
            for supplier in suppliers), name="suppier1")
        m.addConstrs((gp.quicksum(x_sfj.select(supplier, factory, product)[0] * processing1_rate[product] for product in products for factory in factories) \
            <= processing2_capacity[supplier] + gp.quicksum(zp2_ssj.select('*', supplier, '*')) - gp.quicksum(zp2_ssj.select(supplier, '*', '*')) \
            for supplier in suppliers), name="suppier2")
        m.addConstrs((gp.quicksum(zp1_ssj[arc] * processing1_rate[arc[2]] for arc in arcs_ssj if supplier == arc[0]) \
            <= max(0, processing1_capacity[supplier] - processing2_capacity[supplier]) \
            for supplier in suppliers), name="suppier3")
        m.addConstrs((gp.quicksum(zp2_ssj[arc] * processing2_rate[arc[2]] for arc in arcs_ssj if supplier == arc[0]) \
            <= max(0, processing2_capacity[supplier] - processing1_capacity[supplier]) \
            for supplier in suppliers), name="suppier4")
        m.addConstrs((gp.quicksum(x_sfj.select(supplier,'*',product)) \
            >= gp.quicksum(zp1_ssj.select('*',supplier,product)) * processing1_rate[product] \
            for product in products for supplier in suppliers), name="suppier5")
        m.addConstrs((gp.quicksum(x_sfj.select(supplier,'*',product)) \
            >= gp.quicksum(zp2_ssj.select('*',supplier,product)) * processing2_rate[product] \
            for product in products for supplier in suppliers), name="suppier6")
                
        var = {'x_sfj':x_sfj,'zp1_ssj':zp1_ssj,'zp2_ssj':zp2_ssj}
        obj_augmented_penalty,coupling_receive_list,coupling_send_list = self.decision_coordination(DSmode=self.DSmode,var=var)
            
        suppier_transport_cost = (gp.quicksum(x_sfj[arc] * cost_sfj[arc]  for arc in arcs_sfj) )
        suppier_latent_transpot_cost = (gp.quicksum(zp1_ssj[arc] * processing1_rate[arc[2]] * LScost_ssj_out[arc] + zp2_ssj[arc] * processing2_rate[arc[2]] * LScost_ssj_out[arc] for arc in arcs_ssj_out) )
        suppier_latent_process_cost = (gp.quicksum(zp1_ssj[arc] * processing1_rate[arc[2]] * processing1_cost[arc[0],arc[2]] + zp2_ssj[arc] * processing2_rate[arc[2]] * processing2_cost[arc[0],arc[2]] for arc in arcs_ssj_out) )
        suppier_process_cost = gp.quicksum( (gp.quicksum(x_sfj.select(supplier,'*',product)) - gp.quicksum(zp1_ssj.select('*',supplier,product)) * processing1_rate[product]) * processing1_cost[supplier,product]\
            + (gp.quicksum(x_sfj.select(supplier,'*',product)) - gp.quicksum(zp2_ssj.select('*',supplier,product)) * processing2_rate[product]) * processing2_cost[supplier,product] for product in products for supplier in suppliers )
        suppier_objective = suppier_transport_cost + suppier_latent_transpot_cost + suppier_latent_process_cost + suppier_process_cost
        m.setObjective(suppier_objective + obj_augmented_penalty + new_obj_all, GRB.MINIMIZE)
        
        m.setParam('OutputFlag', False)
        m.optimize()  
        self.optxv = [{key:x_sfj[key].x for key in x_sfj}, {key:zp1_ssj[key].x for key in zp1_ssj}, {key:zp2_ssj[key].x for key in zp2_ssj}]
        
        self.objVal = m.objVal
        try:
            self.pure_objVal = m.objVal - obj_augmented_penalty.getValue()
        except:
            self.pure_objVal = m.objVal - obj_augmented_penalty
        self.sending_list,self.consistency_list,self.coupling_receive_list_value_2 = nmt.return_penalty_result(coupling_receive_list, self.receive_list, coupling_send_list,self.node_id)
        
if __name__ == '__main__':
    node_1().decision_model() 