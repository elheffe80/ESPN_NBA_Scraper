#!/usr/bin/env python3
"""
A script used to scrape a very small subset of ESPN's pages and create a graph.  Intended for me to use to learn how
to scrape pages with BeautifulSoup, and graphs with MatPlotLib.
In order to use, change the stats_page variable to point to one of the pages on ESPN's stats for the NBA.  I was
specifically interested in the free throws, thus the current URL.
"""


# import libraries
import re
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# specify the url
stats_page = 'http://www.espn.com/nba/statistics/player/_/stat/free-throws/year/2018'

# yank that page down here for some post-processing!!
page = requests.get(stats_page)

# pull the page & parse with html, will be pushed to different functions
soup = BeautifulSoup(page.text, 'html.parser')


def get_players(data) -> list:
    """
    Function to get the player names from soup'd up data
    :param data: the soup pulled from the page
    :return: list of names for all the players on the page
    """
    players = data.find_all(attrs={'class': re.compile("^evenrow|^oddrow")})
    result = []
    for player in players:
        result += player.a
    return result


def print_players(players: list) -> None:
    """
    Function to print out the players names
    :param list players: list of the players
    :return: null
    """

    for player in players:
        print(player)
    return


def get_field_throw_average(data) -> list:
    """
    Function to get the field throw average
    :param data: the soup pulled from the page
    :return: list of the total average for the players
    """
    result = []
    tmp_averages = data.find_all(attrs={'class': "sortcell"})
    for average in tmp_averages:
        result.append(average.string)
    return result


def print_average(players: list, averages_to_be_printed: list) -> None:
    """
    Function to print the averages, useless as is
    :param list players: list of players to be printed
    :param list averages_to_be_printed: list of averages for the free throws
    :return: None
    """
    # TODO: get this printing nicely with the players names
    if len(players) == len(averages_to_be_printed):
        i = 0
        print("Player\tFree Throw Avg")
        while i < len(players):
            print(players[i], "\t", averages_to_be_printed[i])
            i += 1
    else:
        print("Data sets not compatible. Kick the author")
    return


def get_average_of_averages(all_the_averages) -> float:
    """
    Return the average of the averages for given players.
    :param list all_the_averages: List of strings for the averages
    :return: a float of the average of averages
    """
    length = len(all_the_averages)
    result = 0
    for average in all_the_averages:
        result += float(average)
    return result / length


def make_graph_free_throw_averages(graph_averages: list) -> None:
    """
    Generates a graph for the averages of all the players given.
    :param list graph_averages: List of Strings for the averages
    :return: None
    """
    plt.suptitle('Average of Averages')
    plt.xlabel('NBA Players')
    plt.ylabel('Free Throw Average')

    plt.plot(graph_averages)
    plt.show()
    return


def averages_to_float(float_averages: list) -> list:
    '''
    Function to change the type of the averages from string to float
    :param list float_averages: list of averages in string format
    :return: list result: list of averages in float format
    '''
    result = []
    for item in float_averages:
        result.append(float(item))
    return result


names = get_players(soup.table)
averages = get_field_throw_average(soup.table)
print_average(names, averages)
print('The average of the averages for listed players: ', get_average_of_averages(averages))
make_graph_free_throw_averages(averages_to_float(averages))
