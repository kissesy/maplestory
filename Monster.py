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

monster_img = {
    "0":{
        "name":"mush",
        "left_walk":[]
    }
}

#slime = pygame.image.load('images/monster/slime.png')
TrueFalse = [True, False]


GREEN = (0, 128, 0)
RED = (204, 0, 0)

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
        for _ in enumerate(range(self.Currnet_Mob, Max_Mob, 1)):
            mob = Monster(self.game, 0, (800, 100))
            self.Currnet_Mob+=1
            self.MonsterGroup.add(mob)
   
    def GetMonsterGroup(self):
        return self.MonsterGroup
    
    def InitGroup(self):
        self.MonsterGroup = pygame.sprite.Group()

#image를 이중 리스트로 
# 딕셔너리 안에 리스트
class Monster(pygame.sprite.Sprite):
    def __init__(self, game, monster_number, pos):
        pygame.sprite.Sprite.__init__(self)
        self.Attacked = False #공격받고 있다면 위헤 health bar 올리기 
        self.game = game
        self.damage_font = pygame.font.Font('font/Maplestory_Bold.ttf', 30)
        self.CanJump = False #True
        self.jump_count = 10
        self.Fallen = True
        self.move_count = 0
        self.direction = 1
        self.number = monster_number
        self.MakeImage(pos)
        self.GetData()
        self.name = monster_img[str(self.number)]['name']
        self.NoneDamage = False
        self.Start_Ticks = 0
        self.AttackIndex = -20
        

    def MakeImage(self, pos):
        self.index = 0
        self.images = []
        ######################################################## images/monster/{}{}.png.format()
        self.images.append(pygame.image.load('images/monster/mush1.png'))
        self.images.append(pygame.image.load('images/monster/mush1.png'))
        self.images.append(pygame.image.load('images/monster/mush1.png'))
        self.images.append(pygame.image.load('images/monster/mush2.png'))
        self.images.append(pygame.image.load('images/monster/mush3.png'))
        self.images.append(pygame.image.load('images/monster/mush4.png'))
        self.images.append(pygame.image.load('images/monster/mush4.png'))
        self.images.append(pygame.image.load('images/monster/mush4.png'))

        for image in self.images:
            monster_img[str(self.number)]['left_walk'].append(pygame.transform.scale(image, (60, 60)))
        self.image = monster_img[str(self.number)]['left_walk'][self.index]
        self.rect = self.image.get_rect()
        self.rect.center = pos

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
###
        original = {'x':self.rect.x, 'y':self.rect.y}
        self.index+=1
        if self.index >= len(monster_img[str(self.number)]['left_walk']):
            self.index = 0
        self.image = monster_img[str(self.number)]['left_walk'][self.index]
        self.rect = self.image.get_rect()
        self.rect.x = original['x']
        self.rect.y = original['y']
###
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
    

    #누적 확률값을 이용해서 아이템 드랍 
    def MakeDropItem(self):
        drop_item = {}
        temp = 0
        percent = random.randint(1, 101)
        item = self.mobinfo[self.name]['drop_item']
        for key in item:
            drop_item[key] = item[key] + temp
            temp += drop_item[key]

        for key in drop_item:
            if drop_item[key] >= percent and drop_item[key] <= percent:
                return key
        return "ERROR DONT HAVE ITEM" 

    def GiveMoney(self):
        return random.choice(self.mobinfo[self.name]["drop_money"])

    def GiveItem(self):
        return self.MakeDropItem()

    def GiveExp(self):
        return self.mobinfo[self.name]['drop_exp']

#플레이어의 데미지를 받음  damage를 넘길때 몇 번 때리는지 표시하고 이를 바탕으로 데미지 스킨 위로 제작
    def GetDamage(self, damage, NumberOf):
        self.New = True #만약 False라면 이전 데미지 위로 
        for _ in range(NumberOf):
            damage = self.Cal_Damage(damage)
            pos = [self.rect.x, self.rect.y+self.AttackIndex]
            self.game.DamageSkin.Handler("damage", damage, pos)
            self.AttackIndex-=20
            if self.AttackIndex <= -100:
                self.AttackIndex = -20
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



