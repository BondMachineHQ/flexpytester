out = "['real: x', 'imag: x', 'real: y', 'imag: y', 'real: z', 'imag: z']"
exec("first_line_array = " + out)
print(first_line_array)

pos_real = {}
pos_imag = {}

for i in range(len(first_line_array)):
	s = first_line_array[i]
	if s.startswith('real: '):
		s=s[6:]
		pos_real[s] = i
	elif s.startswith('imag: '):
		s=s[6:]
		pos_imag[s] = i


print(pos_real)
print(pos_imag)




values = []

for item in first_line_array:
	values.append(item.split(': ')[1])
	single_values = list(set(values))


print(single_values)