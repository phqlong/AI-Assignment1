# Artificial bee colony algorithm for constraint vehicle routing problem
# Them cac thu vien neu can
import random
import time
from itertools import combinations


##################      Utility     ###################

# Calculate distance using Euclid distance
def calculate_distance(track):
    def distance(x, y): return ((y[0] - x[0])**2 + (y[1] - x[1])**2) ** 0.5
    return sum([distance(track[i], track[i+1]) for i in range(len(track)-1)])


def profit_diff_func(params):
    print(params)
    return sum([abs(x['profit'] - y['profit']) for x in params for y in params])/2


##################  Class Delivery  ###################

class Delivery():
    STOCK_LOCATION = ()

    NUM_STAFF = 0
    STAFF = []

    NUM_ORDER = 0
    ORDER = []

    def __init__(self, file_input, file_output):
        self.read_input(file_input)
        self.file_output = file_output

    def read_input(self, file_input):
        with open("./" + file_input, 'r') as input:
            data = input.read().split('\n')

            self.STOCK_LOCATION = tuple(float(i) for i in data[0].split(' '))
            self.NUM_STAFF, self.NUM_ORDER = (
                int(i) for i in data[1].split(' '))

            for row in data[2:]:
                row = [float(i) for i in row.split(' ')]
                self.ORDER.append({
                    'location': (row[0], row[1]),
                    'volume':   row[2],
                    'weight':   row[3],
                    'cost':     5 + row[2] + 2*row[3]})

    def write_output(self):
        pass

    def assign_order(self):
        # self.STAFF = self.random_generate()

        # for i in range(self.NUM_STAFF):
        #     self.STAFF.append({'order': order[i]})

        # solutions = [self.random_generate() for _ in range(1000)]
        # fitnesses = [self.evaluate_staff(sol) for sol in solutions]
        # self.STAFF = solutions[fitnesses.index(min(fitnesses))]

        self.STAFF = self.solve_ABC(50, 150, 50)

        min_diff = self.evaluate_staff(self.STAFF)

        import pprint
        pprint.pprint(self.STAFF)

        print("Sum of profit different = " + str(min_diff))

    def evaluate_staff(self, staff_list):
        for staff in staff_list:
            # calculate each staff income
            order_idx_list = staff['order']
            staff['income'] = sum([self.ORDER[i]['cost']
                                   for i in order_idx_list])

            # calculate each staff road
            track = [self.ORDER[i]['location'] for i in order_idx_list]
            staff['road'] = calculate_distance([self.STOCK_LOCATION] + track)

            # calculate each staff cost
            staff['cost'] = staff['road']*20/40 + 10

            # calculate each staff profit
            staff['profit'] = staff['income'] - staff['cost']

        return self.profit_diff_function(staff_list)

    def profit_diff_function(self, staff_list):
        profit_list = [x['profit'] for x in staff_list]
        return max(profit_list) - min(profit_list)
        # return sum([abs(x['profit'] - y['profit']) for x in staff_list for y in staff_list])/2

    def random_generate(self):
        order = list(range(self.NUM_ORDER))
        random.shuffle(order)
        staff_list = []

        avg_packet = self.NUM_ORDER//self.NUM_STAFF
        for _ in range(self.NUM_STAFF):
            staff_list.append({'order': order[:avg_packet]})
            order = order[avg_packet:]

        for i in range(self.NUM_STAFF):
            if order:
                staff_list[i]['order'] += [order.pop()]
            else:
                break

        return staff_list

    def solve_ABC(self, nEmployed, nOnlooker, search_limit):
        solutions = [self.random_generate() for _ in range(nEmployed)]
        fitnesses = [self.evaluate_staff(sol) for sol in solutions]
        counters = [0]*len(solutions)

        best_fitness = min(fitnesses)
        best_sol = solutions[fitnesses.index(min(fitnesses))]

        for _ in range(search_limit):
            fitnesses = [self.evaluate_staff(sol) for sol in solutions]

            # Employed bees phase
            for i, sol in enumerate(solutions):
                current_fitness = self.evaluate_staff(sol)
                counters[i] += 1
                neighboring_sol = self.generate_neighboring_sol(sol)

                if neighboring_sol is None:
                    solutions[i] = self.random_generate()
                elif self.evaluate_staff(neighboring_sol) < current_fitness:
                    solutions[i] = neighboring_sol
                    current_fitness = self.evaluate_staff(sol)
                elif counters[i] == search_limit:
                    solutions[i] = self.random_generate()
                    counters[i] = 0

                if current_fitness < best_fitness:
                    best_fitness = current_fitness
                    best_sol = solutions[i]

            S = [[] for _ in range(nOnlooker)]
            # Onlooker bees phase
            for i in range(0, nOnlooker//2):
                max_id = fitnesses.index(max(fitnesses))

                S[i] = self.generate_neighboring_sol(solutions[max_id])

                if S[i] is not None and self.evaluate_staff(S[i]) < best_fitness:
                    best_sol = S[i]
                    best_fitness = self.evaluate_staff(S[i])

            for i in range(nOnlooker//2, nOnlooker):
                min_id = fitnesses.index(min(fitnesses))

                S[i] = self.generate_neighboring_sol(solutions[min_id])

                if S[i] is not None and self.evaluate_staff(S[i]) < best_fitness:
                    best_sol = S[i]
                    best_fitness = self.evaluate_staff(S[i])

            # for i in range(nOnlooker):
            #     if S[i] is not None and self.evaluate_staff(S[i]) < self.evaluate_staff(solutions[i]):
            #         solutions[i] = S[i]
        return best_sol

    def generate_neighboring_sol(self, solution):
        curr_min_diff = self.evaluate_staff(solution)
        sol = solution.copy()

        for staff in sol:
            nOrders = len(staff['order'])
            for i, j in combinations(range(nOrders), 2):
                # swap 2 order in staff's order list
                staff['order'][i], staff['order'][j] = staff['order'][j], staff['order'][i]

                min_diff = self.evaluate_staff(sol)
                if min_diff < curr_min_diff:
                    return sol

                # swap back
                staff['order'][i], staff['order'][j] = staff['order'][j], staff['order'][i]

        return None


def assign(file_input, file_output):
    # read input
    delivery = Delivery(file_input, file_output)

    # run algorithm
    start = time.time()
    delivery.assign_order()
    print("time elapsed: ", time.time() - start)

    # write output
    delivery.write_output()


if __name__ == "__main__":
    assign('input.txt', 'output.txt')
