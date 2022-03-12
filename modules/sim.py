
class Sim:

    pos = (0, 0)
    move = (0, 0)
    attack = (0, 0)

    master = None # начальник симулякра (тот, кому передает данные; тот, от кого получает приказ)
    slaves = None # массив подчиненных симулякра (тот, от кого получает данные; тот, кому отдает приказ)
    observed_outsiders = None # массив наблюдаемых посторонних (не подчиненных) симулякров

    team = None # команда симулякра

    def __init__(self, team, spawnpoint = team.default_spawnpoint):

        self.__pos = spawnpoint
        self.__move = (0, 0)
        self.__attack = (0, 0)

        self.__master = None # начальник симулякра (тот, кому передает данные; тот, от кого получает приказ)
        self.__slaves = [] # массив подчиненных симулякра (тот, от кого получает данные; тот, кому отдает приказ)
        self.__observed_outsiders = [] # массив наблюдаемых посторонних (не подчиненных) симулякров - противники, союзники и неподчиненные однокомандники

    def add_slave(self, slave):
        if slave in self.__slaves:
            raise("Этот подчиненный уже значится в списке")
        else:
            self.__slaves.append(slave)

    def remove_slave(self, slave):
        if slave in self.__slaves:
            self.__slaves.append(slave)
        else:
            raise("Этот подчиненный не значится в списке")

    def change_master(self, master):
        if self.__master:
            self.__master.remove_slave(self)
        master.add_slave(self)
        self.__master = master

    def get_situation_from_slaves(self):
        situation = []

        for slave in self.__slaves:
            slave.get_processed_situation()

    def get_processed_situation(self):
        pass
