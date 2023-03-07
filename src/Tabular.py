from tkinter import *
from CriterionColumn import CriterionColumn
from UnitRow import UnitRow
from customtkinter import (CTkLabel, CTkButton)

class Tabular:
    def __init__(self, master, x, y) -> None:
        self.master = master
        self.xc = x + 141
        self.yc = y
        self.xu = x
        self.yu = y+150
        self.criteria = []
        self.units = []
        self.criteriaLabel = CTkLabel(master=self.master, text="Criteria:", text_color="#000000")
        self.weightsLabel = CTkLabel(master=self.master, text="Weights:", text_color="#000000")
        self.typesLabel = CTkLabel(master=self.master, text="Preference Function:", text_color="#000000")
        self.pcLabel = CTkLabel(master=self.master, text="Pc:", text_color="#000000")
        self.qcLabel = CTkLabel(master=self.master, text="Qc:", text_color="#000000")
        self.button_add_criterion = CTkButton(master=self.master, text="Add a criterion", command=self.add_supp_criterion)
        self.button_add_unit = CTkButton(master=self.master, text="Add an alternative", command=self.add_supp_unit)
        self.button_delete_criterion = CTkButton(master=self.master, text="Delete a criterion", command=self.del_criterion)
        self.button_delete_unit = CTkButton(master=self.master, text="Delete an alternative", command=self.del_unit)


    def add_infos(self) -> None:
        self.criteriaLabel.place(x=self.xu, y=self.yc)
        self.weightsLabel.place(x=self.xu, y=self.yc+25)
        self.typesLabel.place(x=self.xu, y=self.yc+50)
        self.pcLabel.place(x=self.xu, y=self.yc+75)
        self.qcLabel.place(x=self.xu, y=self.yc+100)

        self.button_add_criterion.place(x=self.xc, y=self.yc)
        self.button_add_unit.place(x=self.xu, y=self.yu)
        self.button_delete_criterion.place(x=self.xc, y=self.yc+25)
        self.button_delete_unit.place(x=self.xu+141, y=self.yu)

    
    def add_criteria(self, nb:int=1, names:list=None, weights:list=None, types:list=None, pc:list=None, qc:list=None) -> None:
        x = self.xc
        for i in range(nb):
            x = self.xc + i*141
            self.criteria.append(CriterionColumn(master=self.master, x=x, y=self.yc))
            if(names != None and names != []):
                self.criteria[i].set_name(names[i])
            if(weights != None and weights != []):
                self.criteria[i].set_weight(weights[i])
            if(types != None and types != []):
                self.criteria[i].set_typePF(types[i])
            if(pc != None and pc != []):
                self.criteria[i].set_pc(pc[i])
            if(qc != None and qc != []):
                self.criteria[i].set_qc(qc[i])
        self.xc = x

        self.button_add_criterion.place(x=self.xc+150, y=self.yc)
        self.button_delete_criterion.place(x=self.xc+150, y=self.yc+25)


    def add_units(self, nb:int=1, names:list=None, values:list=None) -> None:
        y = self.yu
        for i in range(nb):
            y = self.yu + i*25
            self.units.append(UnitRow(master=self.master, nb_criteria=len(self.criteria), x=self.xu, y=y))
            if(names != None):
                self.units[i].set_name(names[i])
            if(values != None):
                self.units[i].set_values(values[i])
        self.yu = y
        
        self.button_add_unit.place(x=self.xu, y=self.yu+30)
        self.button_delete_unit.place(x=self.xu+141, y=self.yu+30)

    
    def add_supp_criterion(self):
        self.xc += 141
        self.criteria.append(CriterionColumn(self.master, x=self.xc, y=self.yc))
        for i in range(len(self.units)):
            self.units[i].add_column()
        
        self.button_add_criterion.place(x=self.xc+150, y=self.yc)
        self.button_delete_criterion.place(x=self.xc+150, y=self.yc+25)

    def add_supp_unit(self):
        self.yu += 25
        self.units.append(UnitRow(master=self.master, nb_criteria=len(self.criteria), x=self.xu, y=self.yu))
        self.button_add_unit.place(x=self.xu, y=self.yu+30)
        self.button_delete_unit.place(x=self.xu+141, y=self.yu+30)


    def del_criterion(self):
        self.criteria[-1].destroy()
        self.criteria.pop()
        self.xc -= 141
        for i in range(len(self.units)):
            self.units[i].del_column()
        self.button_add_criterion.place(x=self.xc+150, y=self.yc)
        self.button_delete_criterion.place(x=self.xc+150, y=self.yc+25)

    
    def del_unit(self):
        self.units[-1].destroy()
        self.units.pop()
        self.yu -= 25
        self.button_add_unit.place(x=self.xu, y=self.yu+30)
        self.button_delete_unit.place(x=self.xu+141, y=self.yu+30)


    def extracts_data(self) -> tuple:
        """
        Return the lists: (criteria, weights, type_pf, pc, qc, units)
        """
        criteria = []
        weights = []
        type_pf = []
        pc = []
        qc = []
        units = []
        for i in range(len(self.criteria)):
            criteria.append(self.criteria[i].get_name())
            weights.append(self.criteria[i].get_weight())
            type_pf.append(self.criteria[i].get_typePF())
            pc.append(self.criteria[i].get_pc())
            qc.append(self.criteria[i].get_qc())
        for j in range(len(self.units)):
            units.append(self.units[j].get_row())

        return (criteria, weights, type_pf, pc, qc, units)