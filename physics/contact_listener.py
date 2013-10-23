'''
Created on Sep 9, 2013

@author: efarhan
'''
import engine
from Box2D import *

class PlatformerContactListener(b2ContactListener):
    def BeginContact(self, contact):
        fixture_user_data = contact.fixtureA.userData
        fixture_user_data2 = contact.fixtureB.userData
        # feet is touching something
        if((fixture_user_data == 3 and fixture_user_data2 != 5)\
           or (fixture_user_data2 == 3 and fixture_user_data != 5)):
            
            engine.level_manager.level.player.anim.foot_num += 1
          
        #electricity touch the player  
        if((fixture_user_data == 4 and fixture_user_data2 == 5)\
           or (fixture_user_data == 5 and fixture_user_data2 == 4)):
            engine.level_manager.level.player.anim.touch_electricity(True)
        
        #fire touch the player  
        if((fixture_user_data == 4 and fixture_user_data2 == 6)\
           or (fixture_user_data == 6 and fixture_user_data2 == 4)):
            engine.level_manager.level.player.anim.touch_fire(True)
            
    def EndContact(self, contact):
        fixture_user_data = contact.fixtureA.userData
        fixture_user_data2 = contact.fixtureB.userData
        if((fixture_user_data == 3 and fixture_user_data2 != 5)\
           or fixture_user_data2 == 3 and fixture_user_data != 5):
            # feet is touching something
            engine.level_manager.level.player.anim.foot_num -= 1
        #electricity does no more touch the player  
        if((fixture_user_data == 4 and fixture_user_data2 == 5)\
           or (fixture_user_data == 5 and fixture_user_data2 == 4)):
            engine.level_manager.level.player.anim.touch_electricity(False)
        
        #fire does no more touch the player  
        if((fixture_user_data == 4 and fixture_user_data2 == 6)\
           or (fixture_user_data == 6 and fixture_user_data2 == 4)):
            engine.level_manager.level.player.anim.touch_fire(False)