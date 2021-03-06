import statistics

a_2c = [{"setup":1.19137}]
a_2c = [{"setup":1.19137, "0a":0.01050, "0b":0.03013, "1a":0.02438, "1b":0.051128, "2":0.01254, "3":0.041182, "4":0.019442, "total":217.27728},\
		{"setup": 1.30050, "0a": 0.01886, "0b": 0.05642, "1a": 0.04384, "1b": 0.058397, "2": 0.02129, "3": 0.042750, "4": 0.023481, "total": 274.84863},\
		{"setup": 1.29002, "0a": 0.01288, "0b": 0.02648, "1a": 0.02351, "1b": 0.047680, "2": 0.01426, "3": 0.024627, "4": 0.025813, "total": 284.50457},\
		{"setup": 2.84258, "0a": 0.00990, "0b": 0.02665, "1a": 0.06171, "1b": 0.061151, "2": 0.02687, "3": 0.022214, "4": 0.056905, "total": 215.63345}]

a_1c = []

def compute_mean(data):
	avg_dict = {}
	for key in data[0]:
		vals = []
		for i in range(len(data)):
			vals += [data[i][key]]
		avg_dict[key] = statistics.mean(vals)
	return avg_dict

print(compute_mean(a_2c))


