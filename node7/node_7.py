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

class node_7(): 
    def __init__(self):
        self.mutipler_list = []
        self.penalty_list = []
        self.receive_list = []
        self.node_id = 7
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
                [],#7
                ]
            self.info_receiving_list = [
                [self.experiment],#1
                [self.experiment],#2
                [self.experiment],#3
                [self.experiment],#4
                [self.experiment],#5
                [self.experiment],#6
                [],#7
                ]     
        
        elif ISmode == 'DS':# Downstream sharing
            self.info_sending_list = [
                [],#1
                [],#2
                [],#3
                [],#4
                [self.experiment],#5
                [self.experiment],#6
                [],#7
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
            
        elif ISmode == 'US':# Upstream sharing
            self.info_sending_list = [
                [],#1
                [],#2
                [],#3
                [],#4
                [],#5
                [],#6
                [],#7
                ]
            self.info_receiving_list = [
                [],#1
                [],#2
                [],#3
                [],#4
                [self.experiment],#5
                [self.experiment],#6
                [],#7
                ]     
        
        elif ISmode == 'UDS':# Upstream and downstream sharing
            self.info_sending_list = [
                [],#1
                [],#2
                [],#3
                [],#4
                [self.experiment],#5
                [self.experiment],#6
                [],#7
                ]
            self.info_receiving_list = [
                [],#1
                [],#2
                [],#3
                [],#4
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
        if DSmode == 'CC': # Centralized coordination            
            # send_column
            cs1 = var['x_sfj'].select('S1', '*', '*') + var['zp1_ssj'].select('*', '*', '*') + var['zp2_ssj'].select('*', '*', '*')
            cs2 = var['x_sfj'].select('S2', '*', '*') + var['zp1_ssj'].select('*', '*', '*') + var['zp2_ssj'].select('*', '*', '*')
            cs3 = var['x_sfj'].select('*', 'F1', '*') + var['x_fdj'].select('F1', '*', '*') + var['zm1_ffj'].select('*', '*', '*') + var['zm2_ffj'].select('*', '*', '*')
            cs4 = var['x_sfj'].select('*', 'F2', '*') + var['x_fdj'].select('F2', '*', '*') + var['zm1_ffj'].select('*', '*', '*') + var['zm2_ffj'].select('*', '*', '*')
            cs5 = var['x_fdj'].select('*', 'D1', '*') + var['x_dcj'].select('D1', '*', '*')
            cs6 = var['x_fdj'].select('*', 'D2', '*') + var['x_dcj'].select('D2', '*', '*')
            cs7 = []
            # receive_column
            cr1 = []
            cr2 = []
            cr3 = []
            cr4 = []
            cr5 = []
            cr6 = []
            cr7 = []       
        elif DSmode == 'BSC': # Bidirectional symmetric coordination            
            # send_column
            cs1 = []
            cs2 = []
            cs3 = []
            cs4 = []
            cs5 = var['x_dcj'].select('D1', '*', '*')
            cs6 = var['x_dcj'].select('D2', '*', '*')
            cs7 = []
            # receive_column
            cr1 = []
            cr2 = []
            cr3 = []
            cr4 = []
            cr5 = var['x_dcj'].select('D1', '*', '*')
            cr6 = var['x_dcj'].select('D2', '*', '*')
            cr7 = []
        elif DSmode == 'BPSC': # Bidirectional partially symmetric coordination            
            # send_column
            cs1 = []
            cs2 = []
            cs3 = []
            cs4 = []
            cs5 = var['x_dcj'].select('D1', '*', '*')
            cs6 = var['x_dcj'].select('D2', '*', '*')
            cs7 = []
            # receive_column
            cr1 = []
            cr2 = []
            cr3 = []
            cr4 = []
            cr5 = var['x_dcj'].select('D1', '*', '*')
            cr6 = var['x_dcj'].select('D2', '*', '*')
            cr7 = []
        elif DSmode == 'BASC': # Bidirectional asymmetric coordination
            # send_column
            cs1 = []
            cs2 = []
            cs3 = []
            cs4 = []
            cs5 = var['x_dcj'].select('D1', '*', 'J2')
            cs6 = var['x_dcj'].select('D2', '*', 'J2')
            cs7 = []
            # receive_column
            cr1 = []
            cr2 = []
            cr3 = []
            cr4 = []
            cr5 = var['x_dcj'].select('D1', '*', 'J1')
            cr6 = var['x_dcj'].select('D2', '*', 'J1')
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
                })
            processing2_capacity = dict({
                })
            manufacturing1_capacity = dict({
                })
            manufacturing2_capacity = dict({
                })
        elif id == 'MLV-S2':
            processing1_capacity = dict({
                })
            processing2_capacity = dict({
                })
            manufacturing1_capacity = dict({
                })
            manufacturing2_capacity = dict({
                })            
        elif id == 'MLV-S3':
            processing1_capacity = dict({
                })
            processing2_capacity = dict({
                })
            manufacturing1_capacity = dict({
                })
            manufacturing2_capacity = dict({
                })
            
        suppliers_dict = dict({
            'S1': None,
            'S2': None,
            })

        factories_dict = dict({
            'F1': None,
            'F2': None,
            })

        depots_dict = dict({
            'D1': 220*5,
            'D2': 220*5,
            })

        customers_dict = dict({
            'C1': None,
            'C2': None,
            'C3': None,
            'C4': None,
            })

        products_dict = dict({
            'J1': None,
            'J2': None,
            })

        customers_product_dict = dict({
            ('C1','J1'): 10*5,
            ('C1','J2'): 75*5,
            ('C2','J1'): 10*5,
            ('C2','J2'): 80*5,
            ('C3','J1'): 10*5,
            ('C3','J2'): 10*5,
            ('C4','J1'): 10*5,
            ('C4','J2'): 10*5,
            })

        processing1_rate = dict({
            })
        processing2_rate = dict({
            })
        manufacturing1_rate = dict({
            })
        manufacturing2_rate = dict({
            })

        arcs_sfj,cost_sfj = gp.multidict({
            ('S1', 'F1', 'J1'): None,
            ('S1', 'F1', 'J2'): None,
            ('S1', 'F2', 'J1'): None,
            ('S1', 'F2', 'J2'): None,
            ('S2', 'F1', 'J1'): None,
            ('S2', 'F1', 'J2'): None,
            ('S2', 'F2', 'J1'): None,
            ('S2', 'F2', 'J2'): None,
            })

        arcs_fdj,cost_fdj = gp.multidict({
            ('F1', 'D1', 'J1'): None,
            ('F1', 'D1', 'J2'): None,
            ('F1', 'D2', 'J1'): None,
            ('F1', 'D2', 'J2'): None,
            ('F2', 'D1', 'J1'): None,
            ('F2', 'D1', 'J2'): None,
            ('F2', 'D2', 'J1'): None,
            ('F2', 'D2', 'J2'): None,
            })

        arcs_dcj,cost_dcj = gp.multidict({
            ('D1', 'C1', 'J1'): 2.0,
            ('D1', 'C1', 'J2'): 3.0,
            ('D1', 'C2', 'J1'): 3.0,
            ('D1', 'C2', 'J2'): 2.5,
            ('D1', 'C3', 'J1'): 1.0,
            ('D1', 'C3', 'J2'): 2.2,
            ('D1', 'C4', 'J1'): 2.0,
            ('D1', 'C4', 'J2'): 1.5,
            ('D2', 'C1', 'J1'): 1.0,
            ('D2', 'C1', 'J2'): 1.0,
            ('D2', 'C2', 'J1'): 3.0,
            ('D2', 'C2', 'J2'): 2.8,
            ('D2', 'C3', 'J1'): 4.0,
            ('D2', 'C3', 'J2'): 4.4,
            ('D2', 'C4', 'J1'): 3.0,
            ('D2', 'C4', 'J2'): 3.5,
            })


        _,processing1_cost = gp.multidict({():00,
            })
        _,processing2_cost = gp.multidict({():00,
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
            ('S1', 'S2', 'J1'): None,
            ('S1', 'S2', 'J2'): None,
            ('S2', 'S1', 'J1'): None,
            ('S2', 'S1', 'J2'): None,
            })
        
        arcs_ffj = [
            ('F1', 'F2', 'J1'),
            ('F1', 'F2', 'J2'),
            ('F2', 'F1', 'J1'),
            ('F2', 'F1', 'J2'),
            ]
        
        arcs_ffj_out,LFcost_ffj_out = gp.multidict({
            ('F1', 'F2', 'J1'): None,
            ('F1', 'F2', 'J2'): None,
            ('F2', 'F1', 'J1'): None,
            ('F2', 'F1', 'J2'): None,
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
        _,_,_,_,\
        _,_,_,_,\
        _,_,_,_,\
        arcs_ssj,_,_,arcs_ffj,_,_,\
        arcs_sfj,_,arcs_fdj,_,arcs_dcj,_,\
        _,_,depots_dict,customers_dict,products_dict,customers_product_dict,\
        modelname,\
        = self.scenario(self.scemode)
        
        m = gp.Model(modelname)
        
        depots = depots_dict.keys()
        customers = customers_dict.keys()
        products = products_dict.keys()
        x_dcj = m.addVars(arcs_dcj,lb=0, name="x_dcj", )
        x_sfj = m.addVars(arcs_sfj,lb=0, name="x_sfj", )
        x_fdj = m.addVars(arcs_fdj,lb=0, name="x_fdj", )
        zp1_ssj = m.addVars(arcs_ssj,lb=0, name="zp1_ssj")
        zp2_ssj = m.addVars(arcs_ssj,lb=0, name="zp2_ssj")
        zm1_ffj = m.addVars(arcs_ffj,lb=0, name="zm1_ffj")
        zm2_ffj = m.addVars(arcs_ffj,lb=0, name="zm2_ffj")
        
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        new_obj_all = self.infomation_sharing(self.ISmode, m)
        sys.stdout = original_stdout


        var = {'x_sfj':x_sfj,'x_fdj':x_fdj,'x_dcj':x_dcj,'zp1_ssj':zp1_ssj,'zp2_ssj':zp2_ssj,'zm1_ffj':zm1_ffj,'zm2_ffj':zm2_ffj}
        obj_augmented_penalty,coupling_receive_list,coupling_send_list = self.decision_coordination(DSmode=self.DSmode,var=var)
        
        retail_objective = (gp.quicksum( (gp.quicksum(x_dcj[(depot,customer, product)] for depot in depots) - customers_product_dict[customer, product])**2 for product in products for customer in customers if (customer, product) in  customers_product_dict ) )
        m.setObjective(150*retail_objective + obj_augmented_penalty + new_obj_all, GRB.MINIMIZE)
        
        m.setParam('OutputFlag', False)
        m.optimize()  
        self.optxv = [{key:x_dcj[key].x for key in x_dcj},]
        self.unstdemand = (gp.quicksum(gp.quicksum(x_dcj[(depot, customer, product)] for depot in depots) - customers_product_dict[customer, product] for product in products for customer in customers if (customer, product) in  customers_product_dict )).getValue()

        self.objVal = m.objVal
        try:
            self.pure_objVal = m.objVal - obj_augmented_penalty.getValue()
        except:
            self.pure_objVal = m.objVal - obj_augmented_penalty
        self.sending_list,self.consistency_list,self.coupling_receive_list_value_2 = nmt.return_penalty_result(coupling_receive_list, self.receive_list, coupling_send_list,self.node_id)
        
if __name__ == '__main__':
    node_7().decision_model() 
  
        
        
