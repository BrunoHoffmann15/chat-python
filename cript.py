#-*- coding: UTF-8 -*-
letters = ['a','A','b','B','c','C','D','d','E','e','F','f','G','g','h','H','i', 'I','j', 'J','k', 'K','l','L','m','M','n', 'N','o', 'O','P','p','Q','q','R','r','S','s','T','t','U','u','v','V','w','W','X','x','Y','y','Z','z',' ','.',',','_','?','1','2','3','4','5','6','7','8','9','0', '[', ']', '{', '}']

key = "4IMELHOR"
print len(letters)

def find_list_postion(letter):
	return letters.index(letter)

class Cript ():

	def encrypt (self, text) :
		cont = 0
		encrypt = ""
		for l in text:
			indexText = find_list_postion(l)
			indexKey = find_list_postion(key[cont])
			indexCript = ((indexText + indexKey) % 71)
			encrypt += letters[indexCript]
			cont += 1
			if cont <= len(key)-1:
				cont = 0
		return encrypt
	
	def decrypt (self, crypt) :
		cont = 0
		decrypt = ""
		for l in crypt:
			indexCrypt = find_list_postion(l)
			indexKey = find_list_postion(key[cont])
			indexText = (((indexCrypt - indexKey) + 71) % 71)
			decrypt += letters[indexText]
			cont += 1
			if cont <= len(key)-1:
				cont = 0
		return decrypt
