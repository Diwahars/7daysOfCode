#!/bin/python

from sys import argv
from colorama import init, Fore, Style
from bs4 import BeautifulSoup
from os import popen
from random import choice
import requests
import textwrap

def cli():
	argv.pop(0)
	init(autoreset=True)
	headers = (
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
		'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0',
		'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko)',
		'Chrome/19.0.1084.46 Safari/536.5',
		'Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko)',
		'Chrome/19.0.1084.46',
		'Safari/536.5',
		'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13',
		)
	header = {'User-agent': choice(headers)}

	if len(argv) == 0:
		print('Usage: askstackoverflow <your question>')
		exit()
	query = (' '.join(argv)).replace(' ', '+')

	page = requests.get('https://duckduckgo.com/html/?q=' +  query + ' site:stackoverflow.com', headers=header).text
	soup = BeautifulSoup(page, 'html.parser')
	possible_links = soup.find_all('a', {'class':'result__a'})
	#print possible_links

	width = int((popen('stty size', 'r').read().split())[1])
	links = []
	color = True
	numb = 1

	for x in possible_links[:10]:
		inner_link = 'https://duckduckgo.com' + x['href']
		page = requests.get(inner_link, headers=header).text
		soup = BeautifulSoup(page, 'html.parser')
		link = (soup.find('script').get_text()).replace('window.parent.location.replace("', '').replace('");', '')
		#if link.startswith('https://www.quora.com/') and not link.startswith('https://www.quora.com/topic/') and not link.startswith('https://www.quora.com/profile/'):
		if link.startswith('http://stackoverflow.com/questions'):
			if color:
				prefix = Fore.RED + Style.BRIGHT + '{0: <4}'.format(str(numb) + '.')
			else:
				prefix = Fore.MAGENTA + Style.BRIGHT + '{0: <4}'.format(str(numb) + '.')
			wrapper = textwrap.TextWrapper(initial_indent=prefix, width=width, subsequent_indent='    ')
			print wrapper.fill(link.split('/')[-1].replace('-', ' '))
			links.append(link)

			color = not color
			numb += 1

	print('')
	print('Choose a Question')

	while True:
		selection = int(raw_input('> '))
		if selection <= len(links) and selection >= 1:
			break
		else:
			print('Choose a valid number!')

	link = links[selection-1]
	ques_page = (requests.get(link, headers=header).text)
	ques_page = ques_page.replace('<b>', Fore.YELLOW).replace('</b>', Fore.RED)
	ques_page = ques_page.replace('<a', Fore.BLUE + '<a').replace('</a>', Fore.RED + '</a>')
	ques_page = ques_page.replace('<br />', '\n')
	ques_page = ques_page.replace('</p>', '\n\n')

	print('')
	soup = BeautifulSoup(ques_page, 'html.parser')

	try:
		answer = Fore.RED + Style.BRIGHT + soup.find('div',{'class': 'answer accepted-answer'}).find('td',{'class':'answercell'}).get_text()
		print answer.replace('\n\n\n','\n')
	except AttributeError:
		print 'Sorry, this question has not been answered yet..'
	exit()

if __name__=='__main__':
	cli()