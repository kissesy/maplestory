import pygame
from Player import Player
import sys
from Map import *
from Monster import *

'''
쉽게 상황으로 설명을 하면
1. 발사키를 눌르면 event가 발생
2. event 가 발생하면 총알 발사(객체 생성)
3. 생성된 개체는 게임 안의 sprite group 에 add
4. bullet group 안에도 들어감
5. 이후 총알이 적과 충돌하면
6. 충돌한 총알 객체를 group에서 제거
'''
'''
그럼 
'''

WHITE = (255, 255, 255)
pad_width = 1024
pad_height = 512

forest_background = pygame.image.load('images/map/forest.jpg')
forest_background = pygame.transform.scale(forest_background, (1024, 512))

class Game:
    def __init__(self):
        pygame.init()
        self.Max_Mob = 0
        self.Current_Mob = 0
        self.LookAt = True #True is right False is left LookAt
        self.make_map = True
        self.pos_map = 'level1'
        self.clock = pygame.time.Clock()
        self.pad_width = 1024
        self.pad_height = 512
        self.gamepad = pygame.display.set_mode((pad_width, pad_height))
        pygame.display.set_caption('MapleStory')
        self.player_dict = {'x':300, 'y':200}

    #여러 복수객체들의 경우 pygame.sprite.Group()화 시켜야하는것인가 
    def new(self):
        self.MapObj =  MapClass()
        self.player = Player(self) #플레이어 객체 
        self.playerGroup = pygame.sprite.Group()
        self.MonsterObj = MonsterClass(self)
        self.playerGroup.add(self.player)

    #특정 개체수 미만으로 떨어지면 생성
    def LoadMonster(self):
        if self.Max_Mob == 0: #만약 몬스터가 없는 지역이라면
            return
        self.MonsterObj.MakeMonster(self.Max_Mob)
        self.MonsterGroup = self.MonsterObj.GetMonsterGroup()
        self.MonsterGroup.update()
        self.MonsterGroup.draw(self.gamepad)
            

    def LoadMap(self):
        self.gamepad.blit(forest_background, (0,0))
        self.MapGroup = self.MapObj.GetMapGroup()
        self.MapGroup.draw(self.gamepad)

    def MakeMap(self):
        self.MapObj.Handler('Start') #Current_Pos
        self.MonsterObj.InitGroup() #몬스터 그룹 초기화
        self.Max_Mob = self.MapObj.GetMaxMonster('Start')

    def run(self):
        self.playing = True
        self.new()
        while self.playing:
            self.clock.tick(60)    
            if self.make_map == True: #True라면 맵을 만든다. 
                self.MakeMap()
                #맵 로드하고 플레이어 위치 설정 
                self.player.SetPos(self.MapObj.GetSetPlayerPos())
                self.make_map = False

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                self.LookAt = False
                self.player.move(-2, 0)
            if key[pygame.K_RIGHT]:
                self.LookAt = True
                self.player.move(2, 0)
            if key[pygame.K_SPACE]:
                self.player.CanJump = True 

            self.gamepad.fill(WHITE)
            self.LoadMap()
            self.LoadMonster()
            self.player.update(self.LookAt)
            self.player.jump()
            self.gamepad.blit(self.player.image, self.player.rect)
            
            pygame.display.flip() #화면 전체를 업데이트함. pygame.display.update()와 같지만 이 update는 인수가 있다면 그 인수만 update


game = Game()
game.run()