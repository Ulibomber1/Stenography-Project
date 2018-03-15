from PIL import Image
import binascii
import numpy as np
import Tkinter


#view
root = Tkinter.Tk()

b = Tkinter.Label(root, text='type text, and file name in \nhide box to hide\nand do the same in \nthe retive box to \nto retrive.')
b.grid(row=0, column=1)

textbox = Tkinter.text(root, text='l' )
textbox.grid(row=2, column=0)


root.mainloop()

def rgb2hex(r, g, b):
	return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def hex2rgb(hexcode):
	return tuple(map(ord, hexcode[1:].decode('hex')))

def str2bin(message):
	binary = bin(int(binascii.hexlify(message), 16)) 
	return binary[2:]

def bin2str(binary):
	message = binascii.unhexlify('%x' % (int('0b'+binary,2)))
	return message

def encode(hexcode, digit):
	if hexcode[-1] in ('0','1', '2', '3', '4', '5'):
		hexcode = hexcode[:-1] + digit
		return hexcode
	else:
		return None

def decode(hexcode):
	if hexcode[-1] in ('0', '1'):
		return hexcode[-1]
	else:
		return None

def hide(filename, message):
#        rgb = ('r', 'g', 'b')
            
            
	img = Image.open(filename)
	binary = str2bin(message) + '1111111111111110'
	if img.mode in ('RGBA'):
		img = img.convert('RGBA')
		datas = img.getdata()
		print 'Before'
		print list (datas[1]),list (datas[2]),list (datas[3]),list (datas[4]),list (datas[5]),list (datas[6]),list (datas[7]),list (datas[8]),list (datas[9]),list (datas[10])
		newData = []
		digit = 0
		temp = ''
		for item in datas:
			if (digit < len(binary)):
				newpix = encode(rgb2hex(item[0],item[1],item[2]),binary[digit])
				if newpix == None:
					newData.append(item)
				else:
					r, g, b = hex2rgb(newpix)
					newData.append((r,g,b,255))
					digit += 1
			else:
				newData.append(item)	
		img.putdata(newData)
		img.save(filename, "PNG")
		print 'After'
		print list (datas[1]),list (datas[2]),list (datas[3]),list (datas[4]),list (datas[5]),list (datas[6]),list (datas[7]),list (datas[8]),list (datas[9]),list (datas[10])
		print 'Some times none the of the first ten RGB values are not changed also can been seen better on black images'
		return "Completed!"
			
	return "Incorrect Image Mode, Couldn't Hide"

						
				

def retr(filename):
	img = Image.open(filename)
	binary = ''
	
	if img.mode in ('RGBA'): 
		img = img.convert('RGBA')
		datas = img.getdata()
		
		for item in datas:
			digit = decode(rgb2hex(item[0],item[1],item[2]))
			if digit == None:
				pass
			else:
				binary = binary + digit
				if (binary[-16:] == '1111111111111110'):
					print "Success"
					return bin2str(binary[:-16])

		return bin2str(binary)
	return "Incorrect Image Mode, Couldn't Retrieve"
	
