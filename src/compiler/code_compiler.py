#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os

###########################################################################
#									STATE								  #
###########################################################################
state = { "IN":{ "STA":0, "LSB":0, "HSB":0, "CHS":0 }, "OUT":0, "CMD":"" }
		
###########################################################################
#								FUNCTIONS								  #
###########################################################################
def hexfixed(value):
	HSB = value[0:4]
	LSB = value[4:8]
	
	NEW_HEX = hex(int(HSB,2))[2] + hex(int(LSB,2))[2]
	
	return NEW_HEX
	pass


def checsum(TIME,IN,OUT):
	NEW_CHECKSUM = (bin(int(TIME,16) + int(IN,16) + int(OUT,16) + 2))
	NEW_CHECKSUM = NEW_CHECKSUM[2:len(NEW_CHECKSUM)]
	text = ""
	dif = 0
	st = 0
	
	if len(NEW_CHECKSUM)>8:
		dif = 12-len(NEW_CHECKSUM)
	else:
		dif = 8-len(NEW_CHECKSUM)
		
	for i in range(dif):
		text += "0"
		
	NEW_CHECKSUM = list(text + NEW_CHECKSUM)
	print NEW_CHECKSUM
	
	for i in range(len(NEW_CHECKSUM)):
		j=len(NEW_CHECKSUM)-1-i
		if (st==0 and NEW_CHECKSUM[j] == "1"):
			st = 1
			
		elif (st==1 and NEW_CHECKSUM[j] == "0"):
			NEW_CHECKSUM[j] = "1"
			
		elif (st==1 and NEW_CHECKSUM[j] == "1"):
			NEW_CHECKSUM[j] = "0"
	
	print NEW_CHECKSUM		
	
	NEW_CHECKSUM = list(hex(int("".join(NEW_CHECKSUM),2)))
	NEW_CHECKSUM.remove("x")
	NEW_CHECKSUM = "".join(NEW_CHECKSUM[len(NEW_CHECKSUM)-2:len(NEW_CHECKSUM)])
	return NEW_CHECKSUM
	pass
	
###########################################################################
#									MAIN CODE							  #
###########################################################################
def main():

	hex_mem = open("hex/code.hex","w")
	
	with open("code/code") as f:
		for line in f:
			if(line[0]=="0" or line[0]=="1"):
				print (line)
				
				state["IN"]["STA"]   = hexfixed(line[0:8])
				state["IN"]["HSB"]   = hexfixed(line[9:17])		
				state["OUT"]  		 = hexfixed(line[20:28])	
				state["IN"]["CHS"]   = checsum(state["IN"]["STA"],state["IN"]["HSB"],state["OUT"])				
				state["CMD"]		 = ":02%s%s00%s00%s\n" % (state["IN"]["STA"],state["IN"]["HSB"],state["OUT"],state["IN"]["CHS"])
				hex_mem.write(state["CMD"])
	
	hex_mem.write(":00000001FF")
	hex_mem.close()

main()