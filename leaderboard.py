# !/usr/bin/python
# -*- coding: utf-8 -*-

#   Leaderboard - from the sourest puss the loveliest goose

class Leaderboard(object):
    def __init__(self):
        self.leaderboard = {}

    def create_leaderboard(self):
        """ Calculates the total negativity for a block of time, and then assigns blame to anyone in the vicinity. This blame is then tallied up. """
        self.leaderboard = dict.fromkeys(self.unique_names, 0)
        # Create a dictionary where the key is the user, and the value is the total of the blocks they were present in when negativity occured
        for n in self.blocks:
            total_negativity_for_this_block = 0
            unique_authors_for_this_block = set()
            for item in n['items']: 
                total_negativity_for_this_block += item['compound']
                unique_authors_for_this_block.add(item['author'])
            for author in unique_authors_for_this_block:
                self.leaderboard[item['author']] += total_negativity_for_this_block / self.posts_per_user[item['author']]
        self.order_leaderboard()

    def order_leaderboard(self):
        self.leaderboard = [ (v,k) for k,v in self.leaderboard.items() ]
        self.leaderboard.sort(reverse=True) # natively sort tuples by first element