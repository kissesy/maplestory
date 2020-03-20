import json 
import pygame 
import random

#몬스터 그룹을 만들때에 한 맵에 나오는 몬스터들끼리 그룹화 하기 
#monster_number로 어떤 몬스터를 가지고올것인지 결정한다. 
#Slime : 0
#Orange_Mushroom : 1
'''
    #display update하면 바로 사라질 텐데 음 #Attacked를 두고 3초뒤에 지우기?
    def Draw_Damage(self, damage):
        if self.New == True: #처음 맞은거임 데미지 스킨 위치 저장 
            self.damagetext = self.damage_font.render(str(damage), True, DAMAGE_COLOR)
            self.damageRect = self.damagetext.get_rect()
            self.damageRect.topleft = (self.rect.x, self.rect.y-20)
            self.previous = self.damageRect.topleft
            #game blit은 update에 따로 함수 두기 
            #self.game.gamepad.blit(self.damagetext, self.damageRect)

        elif self.New == False:
            pass
'''

monster_img = []
monster_name = {
    0:'Slime',
    1:'Orange_Mushroom',
}
slime = pygame.image.load('images/monster/slime.png')
monster_img.append(pygame.transform.scale(slime, (60, 60)))
TrueFalse = [True, False]

test_pos = [(800, 100), (700, 100), (600, 100)] #json으로 변환 

GREEN = (0, 128, 0)
RED = (204, 0, 0)
DAMAGE_COLOR = (180, 4, 174)

class MonsterClass(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.InitGroup()
        self.Currnet_Mob = 0

    def MakeMonster(self, Max_Mob):
        if self.Currnet_Mob != 0:
            #print("Max ",self.Currnet_Mob)
            return
        for index, _ in enumerate(range(self.Currnet_Mob, Max_Mob, 1)):
            #print(self.Currnet_Mob)
            mob = Monster(self.game, 0, test_pos[index])
            self.Currnet_Mob+=1
            self.MonsterGroup.add(mob)
   
    def GetMonsterGroup(self):
        return self.MonsterGroup
    
    def InitGroup(self):
        self.MonsterGroup = pygame.sprite.Group()


class Monster(pygame.sprite.Sprite):
    def __init__(self, game, monster_number, pos):
        pygame.sprite.Sprite.__init__(self)
        self.Attacked = False #공격받고 있다면 위헤 health bar 올리기 
        self.game = game
        self.image = monster_img[monster_number]
        self.damage_font = pygame.font.Font('font/Maplestory_Bold.ttf', 30)
        self.CanJump = False #True
        self.jump_count = 10
        self.Fallen = True
        self.move_count = 0
        self.direction = 1
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.GetData()
        self.name = monster_name[monster_number]
        self.NoneDamage = False
        self.Start_Ticks = 0
        self.New = True #True라면 처음 스킬에 맞은거임 

    def GetData(self):
        with open('json/monster.json', encoding='utf-8') as monsterinfo:
            self.mobinfo = json.load(monsterinfo)

    def Check_Collision(self):
        collisions = pygame.sprite.spritecollide(self, self.game.MapObj.GetMapGroup(), False)
        if collisions:
            for collision in collisions:
                if (collision.rect.top+10 >= self.rect.bottom):
                    self.rect.bottom = collision.rect.top-3 #+1해서 보정값 세워야하나
                    self.CanJump = False #점프 못하게 방지 
                    self.jump_count = 10
                    self.Fallen = False
                else: 
                    continue

    #랜덤으로 움직일지 아닐지 결정   jump_count를 바탕으로 점프가 끝나고 나서야 할지 말지 체크 
    def decision_jump(self):
        if self.CanJump == True or self.mobinfo[self.name]['CanJump'] == False: #여기에 몬스터가 점프 속성이 있는지 체크
            return False #현재 점프중이다.
        else:
            return True #점프중이 아님

    def MakeMoveCount(self):
        return random.choice([0, 20])
        #return random.choice([0,0, 0, 0,10,14,20])

    def decision_direction(self):
        return random.choice([1, -1])

    def update(self):
        self.Draw_BottomBar()
        if self.decision_jump(): #점프중이 아닐때 True를 반환함
            self.CanJump = random.choice(TrueFalse)
        if self.move_count == 0:
            self.move_count = self.MakeMoveCount()
            self.direction = self.decision_direction()
        else:
            self.move()
            self.move_count -= 1
        self.jump()

    def move(self):
        x = 2 * self.direction
        if self.rect.right+x >= 1024 or self.rect.left+x<=0:
            return
        else:
            self.rect.x+=x
        self.Fallen = True
        self.Check_Collision()

    def jump(self):
        if self.CanJump:
            if self.jump_count <= 0:
                self.rect.y += (1 ** 2)*10
                self.jump_count -= 1
                self.Check_Collision()
            elif self.jump_count > 0 and self.jump_count <= 10:
                self.rect.y -= (self.jump_count ** 2) * 0.015
                self.jump_count -= 1
            else:
                self.jump_count = 10
                self.CanJump = False
        elif self.Fallen:
            self.rect.y += (1**2)*10
            self.Check_Collision()
        
#대미지 x ( 100 / (100 + 방어력) ) 
#한번 플레이어를 공격하게 되면 3초간 데미지를 주지 않는다 .
    def Attack(self):
        if self.NoneDamage == True:
            self.SetDamageZero()
            return 0
        else:
            self.NoneDamage = True
            return self.mobinfo[self.name]['damage']

    def GetPercent(self, cur, max, len):
        return (len * (1 - ((max-cur)/max)))

    def Draw_BottomBar(self):
        cur = self.mobinfo[self.name]['hp'][0]
        max = self.mobinfo[self.name]['hp'][1]
        hp_percent = self.GetPercent(cur, max, 50)
        x = self.rect.x
        y = self.rect.y-10
        pygame.draw.rect(self.game.gamepad, RED , (x, y, 50, 5)) #150
        pygame.draw.rect(self.game.gamepad, GREEN , (x, y, hp_percent, 5))

    def SetDamageZero(self):
        if self.Start_Ticks == 0:
            self.Start_Ticks = pygame.time.get_ticks()
        else:
            seconds = (pygame.time.get_ticks() - self.Start_Ticks)/1000
            if seconds >= 2:
                self.NoneDamage = False
                self.Start_Ticks = 0 
    

    def GiveExp(self):
        return self.mobinfo[self.name]['drop_exp']

#플레이어의 데미지를 받음  damage를 넘길때 몇 번 때리는지 표시하고 이를 바탕으로 데미지 스킨 위로 제작
    def GetDamage(self, damage, NumberOf):
        self.New = True #만약 False라면 이전 데미지 위로 
        for _ in range(NumberOf):
            damage = self.Cal_Damage(damage)
            if self.mobinfo[self.name]['hp'][0] - damage <= 0:
                self.game.MonsterObj.GetMonsterGroup().remove(self)
                self.game.MonsterObj.Currnet_Mob -= 1
                return True  #몬스터 사망 그룹에서 제거
            else:
                self.mobinfo[self.name]['hp'][0] -= damage
        #self.New = True
        return False

#방어력 공식 계산
    def Cal_Damage(self, damage):
        return damage * (100 / (100 * self.mobinfo[self.name]['defensive']))

    def Health(self):
        pass

    def DropItem(self):
        pass



