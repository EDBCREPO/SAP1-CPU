#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os

###########################################################################
#									STATE								  #
###########################################################################
state = {"IN":{ "TIME":0, "HSB":0, "LSB":0, "CHS1":"", "CHS2":"", "CHS3":"", },
		 "CMD1":"","CMD2":"","CMD3":"",
		 "OUT1":0,"OUT2":0,"OUT3":0, }

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

	hex_mem1 = open("hex/mem1.hex","w")
	hex_mem2 = open("hex/mem2.hex","w")
	hex_mem3 = open("hex/mem3.hex","w")

	with open("code/inst") as f:
		for line in f:
			if(line[0]=="0" or line[0]=="1"):
				print (line)
				inst = list(line)
				correction = list("11111111 11111111 : 01101100 00000000 00000000")
								 #"11111111 11111111 : 01101101 XX000000 XX000000"
				
				for i in range(len(correction)):
					if(correction[i]=="0" and inst[i]=="0"): inst[i]="1"
					elif(correction[i]=="0" and inst[i]=="1"): inst[i]="0"
					pass
				inst = "".join(inst)
				
				print inst

				state["IN"]["TIME"]   = hexfixed(inst[0:8])
				state["IN"]["HSB"]    = hexfixed(inst[9:17])
				state["OUT3"]		  = hexfixed(inst[20:28])
				state["OUT2"]		  = hexfixed(inst[29:37])
				state["OUT1"]		  = hexfixed(inst[38:46])
				
				state["IN"]["CHS3"]   = checsum(state["IN"]["HSB"],state["IN"]["TIME"],state["OUT3"])
				state["IN"]["CHS2"]   = checsum(state["IN"]["HSB"],state["IN"]["TIME"],state["OUT2"])
				state["IN"]["CHS1"]   = checsum(state["IN"]["HSB"],state["IN"]["TIME"],state["OUT1"])
				
				state["CMD1"] 		  = ":02%s%s00%s00%s\n" % (state["IN"]["TIME"],state["IN"]["HSB"],state["OUT1"],state["IN"]["CHS1"])
				state["CMD2"] 		  = ":02%s%s00%s00%s\n" % (state["IN"]["TIME"],state["IN"]["HSB"],state["OUT2"],state["IN"]["CHS2"])
				state["CMD3"]		  = ":02%s%s00%s00%s\n" % (state["IN"]["TIME"],state["IN"]["HSB"],state["OUT3"],state["IN"]["CHS3"])
				
				print state["CMD1"]
				print state["CMD2"]
				print state["CMD3"]
				
				hex_mem1.write(state["CMD1"])
				hex_mem2.write(state["CMD2"])
				hex_mem3.write(state["CMD3"])
	
	hex_mem1.write(":00000001FF")
	hex_mem2.write(":00000001FF")
	hex_mem3.write(":00000001FF")
	
	hex_mem1.close()
	hex_mem2.close()
	hex_mem3.close()

main()