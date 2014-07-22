from engine.const import CONST
from engine.init import engine
from game_object.image import Image
from network import client
from network.client import get_self_id

__author__ = 'efarhan'


class NetworkGamestate():
    def init(self, loading=False):
        if CONST.network:
            client.init()
            self.players_img = {}

    def loop(self, screen):
        if CONST.network and self.player:
            #client.set_request(self.player.pos + engine.get_screen_size() * self.player.screen_relative_pos,
            #                   self.player.anim.state,
            #                   self.player.anim.index)
            #client.get_players_request()
            client.set_player(self.player)
            players_list = client.get_players()
            """Check if player already present else set an image"""
            for p in players_list.keys():
                if p != str(get_self_id()):
                    try:
                        self.players_img[p]

                    except KeyError:
                        self.players_img[p] = Image(pos=players_list[p][1], path="", size=self.player.size)

                    self.players_img[p].pos = players_list[p][1]
                    try:
                        anim_index = self.player.anim.img_indexes[
                                     self.player.anim.state_range[players_list[p][2]][0]:
                                     self.player.anim.state_range[players_list[p][2]][1]]
                        try:
                            self.players_img[p].img = anim_index[players_list[p][3]]
                        except IndexError:
                            self.players_img[p].img = anim_index[0]
                    except KeyError:
                        pass
                    self.players_img[p].loop(screen)