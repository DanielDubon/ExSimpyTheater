import random
import simpy
import statistics

wait_time = []

class Theater(object):

    def __init__(self, env ,num_cashiers, num_servers, num_ushers, num_baths):
        self.env = env
        self.cashier = simpy.Resource(env, num_cashiers)
        self.servers = simpy.Resource(env, num_servers)
        self.ushers = simpy.Resource(env, num_ushers)
        self.baths = simpy.Resource(env, num_baths)


    def purchase_ticket(self, client):
        print("Client "+str(client)+" purachased a Ticket at t="+str(env.now))
        yield self.env.timeout(random.randint(1,3))

    def check_ticket(self,client):
        print("Client "+str(client)+" checked a Ticket at t="+str(env.now))
        yield self.env.timeout(3/60)

    def sell_food(self,client):
        print("Client " + str(client) + " purachased food at t=" + str(env.now))
        yield self.env.timeout(random.randint(1,6))

    def bath_time(self,client):
        # No todos los clientes van al baño entonces probabilidad del 20%
        if random.randint(1,6) == 2:
            print("Client "+str(client)+" went to the BATHH at t= "+str(env.now))
            yield  self.env.timeout(random.randint(2,6))

    def go_to_movies(self, client):

        arrival_time = self.env.now

        with self.cashier.request() as request:
            yield request
            yield self.env.process(self.purchase_ticket(client))

        # El cliente se une a la fila para verificar el boleto
        wait_time.append(self.env.now - arrival_time)
        with self.ushers.request() as request:
            yield request
            yield self.env.process(self.check_ticket(client))

        # El cliente se une a la fila para comprar comida
        with self.servers.request() as request:
            yield request
            yield self.env.process(self.sell_food(client))

        with self.baths.request() as request:
            yield request
            yield self.env.process(self.bath_time(client))




def run_theater(env, num_cashiers, num_servers, num_ushers, moviegoers,num_baths):
    theater = Theater(env, num_cashiers, num_servers, num_ushers,num_baths)

    for i in range(moviegoers):
        env.process(theater.go_to_movies(i))

    while True:
        yield env.timeout(0.1)  # verificar la cola cada 0.1 minutos
        if not theater.cashier.queue and not theater.servers.queue and not theater.ushers.queue:
            break

env = simpy.Environment()
client = 100
num_cashiers = 4
num_servers = 3
num_ushers = 1
num_baths = 1

env.process(run_theater(env, num_cashiers, num_servers, num_ushers, client,num_baths))
env.run()

# Calcular el tiempo de espera promedio
average_wait_time = statistics.mean(wait_time)
print("El tiempo de espera promedio fue de %.2f minutos." % average_wait_time)
