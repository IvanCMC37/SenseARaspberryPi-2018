from sense_hat import SenseHat

sense = SenseHat()
sense.clear()

temp = sense.get_temperature()
if temp >30:
    print('hi')
else:   
    print(temp)