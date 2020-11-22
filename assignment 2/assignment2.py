# Them cac thu vien neu can
import random
import time

##################  Utility ###################

# Calculate distance using Euclid distance
def calculate_distance(track):
    def distance(x, y): return ((y[0] - x[0])**2 + (y[1] - x[1])**2) ** 0.5
    return sum([distance(track[i], track[i+1]) for i in range(len(track)-1)])


##################  Class Delivery ###################

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
        self.STAFF = self.random_generate()
        # self.STAFF = self.genetic_algorithm()
        
        self.evaluate_staff(self.STAFF)

        import pprint
        pprint.pprint(self.STAFF)

        min_diff = self.profit_diff_function(self.STAFF)
        print("Sum of profit different = " + str(min_diff))

    def evaluate_staff(self, staff_list):
        for staff in staff_list:
            # calculate each staff income
            order_idx_list = staff['order']
            staff['income'] = sum([self.ORDER[i]['cost'] for i in order_idx_list])

            # calculate each staff road
            track = [self.ORDER[i]['location'] for i in order_idx_list]
            staff['road'] = calculate_distance([self.STOCK_LOCATION] + track)

            # calculate each staff cost
            staff['cost'] = staff['road']*20/40 + 10

            # calculate each staff profit
            staff['profit'] = staff['income'] - staff['cost']

    def profit_diff_function(self, staff_list):
        return sum([abs(x['profit'] - y['profit']) for x in staff_list for y in staff_list])/2

    def random_generate(self):
        order = list(range(self.NUM_ORDER))
        random.shuffle(order)
        staff_list = []

        for i in range(1, self.NUM_STAFF + 1):
            if i == self.NUM_STAFF:
                staff_list.append({'order': order})
                break

            num = random.randrange(1, len(order) - (self.NUM_STAFF - i) + 1)
            staff_list.append({'order': order[:num]})
            order = order[num:]

        return staff_list

    def genetic_algorithm(self):
        pass


def assign(file_input, file_output):
    # read input
    delivery = Delivery(file_input, file_output)

    # run algorithm
    delivery.assign_order()

    # write output
    delivery.write_output()


if __name__ == "__main__":
    assign('input.txt', 'output.txt')
