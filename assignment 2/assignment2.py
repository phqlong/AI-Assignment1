"""
========  Constraint Vehicle Routing Problem - CVRP   ==========
    Algorithm using:
        Artificial bee colony algorithm 
        Steepest-Ascent Hill Climbing (Gradient Search) Algorithm
"""

import random
import time
from copy import deepcopy

##################      Utility     ###################
# Calculate distance using Euclid distance
def calculate_distance(track):
    def distance(x, y): return ((y[0] - x[0])**2 + (y[1] - x[1])**2) ** 0.5
    return sum([distance(track[i], track[i+1]) for i in range(len(track)-1)])

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
        with open(self.file_output, 'w') as output:
            for order_list in [staff['order'] for staff in self.STAFF]:
                for packet in order_list:
                    output.write('%d ' % packet)
                output.write('\n')

    def assign_order(self):
        if self.NUM_ORDER <= 50:
            print("Using ABC Algorithm")
            self.STAFF = self.solve_ABC(150, 100, 300)
        elif self.NUM_ORDER <= 200:
            print("Using ABC Algorithm")
            self.STAFF = self.solve_ABC(150, 100, 400)
        elif self.NUM_ORDER <= 300:
            print("Using Steepest-Ascent Hill Climbing Algorithm  => 20 times")
            best_sol = None
            best_delta = 100000
            for _ in range(20):
                sol = self.solve_hill_climbing()
                delta = self.min_function(sol)
                # print(delta)
                if delta < best_delta:
                    best_delta = delta
                    best_sol = deepcopy(sol)

            self.STAFF = best_sol
        elif self.NUM_ORDER <= 500:
            print("Using Steepest-Ascent Hill Climbing Algorithm  => 5 times")
            best_sol = None
            best_delta = 100000
            for _ in range(5):
                sol = self.solve_hill_climbing()
                delta = self.min_function(sol)
                # print(delta)
                if delta < best_delta:
                    best_delta = delta
                    best_sol = deepcopy(sol)

            self.STAFF = best_sol
        else:
            print("Using Steepest-Ascent Hill Climbing (Gradient Search) Algorithm")
            self.STAFF = self.solve_hill_climbing()

        min_diff = self.min_function(self.STAFF)

        # import pprint
        # pprint.pprint(self.STAFF)

        print("----------------------------------")
        print("Min delta = " + str(min_diff))
        profit = [i['profit'] for i in self.STAFF]
        min_sum = sum([abs(x - y) for x in profit for y in profit])/2
        print("Min sum = " + str(min_sum))

    def evaluate_staff(self, staff):
        # calculate staff income
        order_idx_list = staff['order']
        staff['income'] = sum([self.ORDER[i]['cost'] for i in order_idx_list])

        # calculate staff road
        track = [self.ORDER[i]['location'] for i in order_idx_list]
        staff['road'] = calculate_distance([self.STOCK_LOCATION] + track)

        # calculate staff cost
        staff['cost'] = staff['road']*20/40 + 10

        # calculate staff profit
        staff['profit'] = staff['income'] - staff['cost']
        return staff['profit']

    def min_function(self, staff_list):
        profit = []
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

            profit += [staff['profit']]

        return max(profit) - min(profit)
        # return sum([abs(x - y) for x in profit for y in profit])/2

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
        fitnesses = [self.min_function(sol) for sol in solutions]
        counters = [0]*len(solutions)

        best_fitness = min(fitnesses)
        best_sol = solutions[fitnesses.index(min(fitnesses))]

        S = [[] for _ in range(nOnlooker)]
        for _ in range(search_limit):
            # print(best_fitness)

            # Employed bees phase
            for i, sol in enumerate(solutions):
                current_fitness = self.min_function(sol)
                counters[i] += 1
                neighboring_sol = self.climb_neighbor_sol(sol)

                if neighboring_sol is None:
                    solutions[i] = self.random_generate()
                else:
                    solutions[i] = neighboring_sol
                    current_fitness = self.min_function(solutions[i])

                if current_fitness < best_fitness:
                    best_fitness = current_fitness
                    best_sol = solutions[i]
                if counters[i] == search_limit//2:
                    solutions[i] = self.random_generate()
                    counters[i] = 0

            # Onlooker bees phase
            fitnesses = [self.min_function(sol) for sol in solutions]
            for i in range(0, nOnlooker):
                p_id = fitnesses.index(min(fitnesses))

                S[i] = self.climb_neighbor_sol(solutions[p_id])

                if S[i] is not None and self.min_function(S[i]) < best_fitness:
                    best_sol = S[i]
                    best_fitness = self.min_function(S[i])
                    # print(str(best_fitness) + " == " + str(self.min_function(best_sol)))

        return best_sol

    def solve_hill_climbing(self):
        sol = self.random_generate()
        best_delta = self.min_function(sol)
        best_sol = deepcopy(sol)

        while True:
            # print(self.min_function(sol))
            sol = self.climb_neighbor_sol(sol)
            if sol is None:
                break

            curr_delta = self.min_function(sol)
            if curr_delta < best_delta:
                best_delta = curr_delta
                best_sol = deepcopy(sol)

        return best_sol

    def climb_neighbor_sol(self, solution):
        staff_list = deepcopy(solution)
        profit = [staff['profit'] for staff in staff_list]

        max_val = max(profit)
        min_val = min(profit)
        delta = max_val - min_val

        profit = list(enumerate(profit))
        maxlist = [i for i in profit if i[1] == max_val]
        minlist = [i for i in profit if i[1] == min_val]

        # min inner swap
        for min_idx, _ in minlist:
            staff = staff_list[min_idx]
            order = staff['order']
            nOrder = len(order)

            for i in range(nOrder - 1):
                for j in range(i + 1, nOrder):
                    order[i], order[j] = order[j], order[i]
                    new_min_val = self.evaluate_staff(staff)

                    if new_min_val > min_val and new_min_val < max_val:
                        return staff_list
                        # new_delta = self.min_function(staff_list)
                        # if new_delta < delta:
                        #     # print("min inner swap")
                        #     return staff_list

        # min max swap
        # staff_list = deepcopy(solution)
        for min_idx, _ in minlist:
            min_order = staff_list[min_idx]['order']
            for max_idx, _ in maxlist:
                max_order = staff_list[max_idx]['order']

                for i in range(len(min_order)):
                    for j in range(len(max_order)):
                        min_order[i], max_order[j] = max_order[j], min_order[i]
                        # new_delta = self.min_function(staff_list)
                        new_delta = abs(self.evaluate_staff(
                            staff_list[max_idx]) - self.evaluate_staff(staff_list[min_idx]))

                        if new_delta < delta:
                            # print("min max swap")
                            return staff_list

        # max give 1 packet to min
        # staff_list = deepcopy(solution)
        for max_idx, _ in maxlist:
            max_order = staff_list[max_idx]['order']
            for min_idx, _ in minlist:
                min_order = staff_list[min_idx]['order']

                for i in range(len(max_order)):
                    min_order.append(max_order.pop(i))
                    # new_delta = self.min_function(staff_list)
                    new_delta = abs(self.evaluate_staff(
                        staff_list[max_idx]) - self.evaluate_staff(staff_list[min_idx]))

                    if new_delta < delta:
                        # print("max give 1 packet to min")
                        return staff_list
                    else:
                        max_order.append(min_order.pop(-1))

        # max inner swap (not good for 1 big max) (not needed for value only)
        # if the biggest is not alone, then we shall shuffle that staff_list path
        # staff_list = deepcopy(solution)
        for max_idx, _ in maxlist:
            staff = staff_list[max_idx]
            order = staff['order']
            nOrder = len(order)

            for i in range(nOrder - 1):
                for j in range(i + 1, nOrder):
                    order[i], order[j] = order[j], order[i]
                    new_max_val = self.evaluate_staff(staff)

                    if new_max_val < max_val and new_max_val > min_val:
                        return staff_list
                        # new_delta = self.min_function(staff_list)
                        # if new_delta < delta:
                        #     # print("max inner swap")
                        #     return staff_list

        # print("None")
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
