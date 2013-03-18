## xkcd-info - A simple and fast script to retrieve info about an specific xkcd comic
# Version 0.1
#
# This script can be used as a stand-alone program or as a module for a
# bigger script
#
# 
# Author: Gonzalo Ciruelos <comp.gonzalo@gmail.com>
# License: GPLv3

import urllib
import json
import sys
import re
from optparse import OptionParser

class Link():
	def __init__(self, line):
		#Example: <a href="/wiki/index.php?title=Megan" title="Megan">Megan</a>
		self.links = 0
		self.line = line

class Explanation():
	def __init__(self, comic):
			self.raw_explanation = urllib.urlopen('http://www.explainxkcd.com/wiki/index.php?title='+comic).read().split('\n')
			
			for line in self.raw_explanation:
				if 'id="Explanation"' in line:
					start = self.raw_explanation.index(line)
				elif 'id="Transcript"' in line:
					end = self.raw_explanation.index(line)
			try:
				self.less_raw_explanation = self.raw_explanation[start+1:end-1]
			except:
				self.less_raw_explanation = ''
	
	def clean(self):
		if self.less_raw_explanation == '':
			return 'This comic has no explanation available.'
	
		cleaned0 = []
		for line in self.less_raw_explanation:
			cleaned0.append(str(line))

		findings = []											#cleans paragraphs and italics tags
		for line in cleaned0:
			findings = findings + re.findall('</?[pi]>', line)
		findings = set(findings)
		for expression in findings:
			for line in cleaned0:
				i = cleaned0.index(line)
				cleaned0[i] = line.replace(expression, '')
				
		cleaned1 = cleaned0
		
		explanation = '\n'.join(cleaned1)
		
		return explanation		


class Comic():
	def __init__(self, opts):
		
		self.alls = opts['all']
		self.explanation = opts['explanation']
		self.mouseover = opts['mouseover']
		self.basic = opts['nobasic']
		self.transcript = opts['transcript']


		if opts['comic_number'] in ('last', 'current', '0'):
			comicn = ''
		else:
			if opts['comic_number'] == '420':
				print 'Blaze it faggot'
			comicn = opts['comic_number']+'/'
			
		try:
			self.comic = opts['comic_number']
			self.raw_information = urllib.urlopen('http://xkcd.com/'+comicn+'info.0.json').read()
			self.information = json.loads(self.raw_information)
		except:
			try:
				int(opts['comic_number'])
				print 'The comic you tried to get information about doesn\'t exist yet.'
			except:
				print 'The comic number you entered is not a number or is invalid.'
			exit()

	def print_raw_info(self):
		print self.information

	def getnumber(self):
		number = self.information['num']
		
		return str(number)
	
	def gettitle(self):
		title = self.information['safe_title']
		
		return title

	def getdate(self):
		months = ['null', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
		
		day = self.information['day']
		month = months[int(self.information['month'])]
		year = self.information['year']
		
		if day[-1] == '3':
			suffix = 'rd'
		elif day[-1] == '2':
			suffix = 'nd'
		elif day[-1] == '1':
			suffix = 'st'
		else:
			suffix = 'th'
		day = day+suffix
		
		return day+' '+month+' '+year

	def getlink(self):
		link = self.information['img']
		return link

	def gettranscript(self):
		raw_transcript = self.information['transcript']
		listoflines = raw_transcript.split('\n')
		
		transcript = '\n'.join(listoflines[:-2])		
		
		return transcript

	def getmouseovertext(self):
		text = self.information['alt']
		return text
	
	def getexplanation(self):
		explanation = Explanation(self.comic).clean()

		return explanation
			
	def __str__(self):		
		i = ['\n']
		
		if self.basic == True:
			i.append('Number: '+self.getnumber())
			i.append('Title: '+self.gettitle())
			i.append('Date: '+self.getdate())
			i.append('Link: '+self.getlink())
		if self.transcript == True:
			i.append('\n'+'Transcript:\n'+self.gettranscript())
		if self.mouseover == True:
			i.append('\n'+'Mouseover text:\n'+self.getmouseovertext())
		if self.explanation == True:
			i.append('\n'+'Explanation:\n'+self.getexplanation())
		if self.alls == True:
			i = ['\n']
			i.append('Number: '+self.getnumber())
			i.append('Title: '+self.gettitle())
			i.append('Date: '+self.getdate())
			i.append('Link: '+self.getlink())
			i.append('\n'+'Transcript:\n'+self.gettranscript())
			i.append('\n'+'Mouseover text:\n'+self.getmouseovertext())
			i.append('\n'+'Explanation:\n'+self.getexplanation())		

		try:
			info = '\n'.join(i)+'\n'
		except:
			print 'FATAL ERROR'
			exit()
		return info

		
def main():
	arguments = sys.argv
	
	parser = OptionParser(usage='Usage: %prog [options]',
						  version='%prog 0.1')
	parser.add_option('-c', '--comic', action='store', dest="comic_number",
					  help='The comic number of the comic you want to get info about.')
	parser.add_option('-a', '--all', action='store_true', default=False,
					  help='Show all the information.')	
	parser.add_option('-n', '--nobasic', action='store_false', default=True,
					  help='Do not show the basic information.')
	parser.add_option('-m', '--mouseover', action='store_true', default=False,
					  help='Show the mouseover text of the comic.')
	parser.add_option('-e', '--explanation', action='store_true', default=False,
					  help='Show the explanation of the comic.')
	parser.add_option('-t', '--transcript', action='store_true', default=False,
					  help='Show the transcript of the comic.')


	(options, args) = parser.parse_args(arguments)
	
	options = options.__dict__

	if options['comic_number'] == None:
		comic_number = raw_input('Which comic do you want to have information about? Enter a number: ')
		options['comic_number'] = comic_number
		
	comic = Comic(options)

	print comic

	
if __name__ == '__main__':
	main()
