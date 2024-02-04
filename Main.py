import pygame
import random
pygame.init()

genislik = 1000
yukseklik = 600
goruntu_yuzeyi = pygame.display.set_mode((genislik, yukseklik))


class Oyun:
    def __init__(self, oyuncu_g, kitap_g, sihirlik_g, teknoloji_g):
        self.score = 0
        self.round_numarasi = 0
        self.round_suresi = 0
        self.soguma = 0
        self.cerceve_sayisi = 0
        self.oyuncu = oyuncu_g
        self.kitaplar = kitap_g
        self.sihirliler = sihirlik_g
        self.teknoloji = teknoloji_g

        self.ileri_seviye_muzigi = pygame.mixer.Sound("yeniseviye.wav")
        pygame.mixer.music.load("arka_ses.flac")
        self.font = pygame.font.Font("AttackGraffiti.ttf", 24)

        kitap_resim = pygame.image.load("kitap.png")
        s_kitap_resim = pygame.image.load("şanslı_kitap.png")
        telefon_resim = pygame.image.load("telefon.png")
        tablet_resim = pygame.image.load("tablet.png")
        bilgisayar_resim = pygame.image.load("bilgisayar.png")

        self.kitap_resimleri = [kitap_resim, s_kitap_resim]
        self.teknoloji_resimleri = [telefon_resim, tablet_resim, bilgisayar_resim]

    def update(self):
        self.cerceve_sayisi += 1
        if self.cerceve_sayisi == FPS:
            self.round_suresi += 1
            self.soguma += 1
            self.cerceve_sayisi = 0
        if self.soguma == 10:
            self.soguma = 0
            self.sihirliler.add(SKitap(random.randint(0, genislik - 64), random.randint(100, yukseklik - 164)))
        self.carpisma_tespiti()

    def cizmek(self):
        beyaz = (255, 255, 255)

        skor_metni = self.font.render(f"SKOR: {self.score}", True, beyaz)
        skor_kordinati = skor_metni.get_rect()
        skor_kordinati.topleft = (5, 5)

        can_metni = self.font.render(f"CAN: {self.oyuncu.can}", True, beyaz)
        can_kordinati = can_metni.get_rect()
        can_kordinati.topright = (genislik - 5, 5)

        round_metni = self.font.render(f"ROUND {self.round_numarasi}", True, beyaz)
        round_kordinati = round_metni.get_rect()
        round_kordinati.topleft = (5, 35)

        zaman_metin = self.font.render(str(self.round_suresi), True, beyaz)
        zaman_kordinati = zaman_metin.get_rect()
        zaman_kordinati.center = (genislik // 2, 10)

        s_kitap_metin = self.font.render(f"SIHIRLI KITAP SAYISI: {self.oyuncu.s_kitap_sayi}", True, beyaz)
        s_kitap_metin_kordinati = s_kitap_metin.get_rect()
        s_kitap_metin_kordinati.topright = (genislik - 5, 35)

        goruntu_yuzeyi.blit(skor_metni, skor_kordinati)
        goruntu_yuzeyi.blit(round_metni, round_kordinati)
        goruntu_yuzeyi.blit(can_metni, can_kordinati)
        goruntu_yuzeyi.blit(s_kitap_metin, s_kitap_metin_kordinati)
        goruntu_yuzeyi.blit(zaman_metin, zaman_kordinati)
        pygame.draw.rect(goruntu_yuzeyi, beyaz, (0, 100, genislik, yukseklik - 200), 2)

    def carpisma_tespiti(self):
        carpisma = pygame.sprite.spritecollideany(self.oyuncu, self.teknoloji)
        carpisma1 = pygame.sprite.spritecollideany(self.oyuncu, self.kitaplar)
        carpisma2 = pygame.sprite.spritecollideany(self.oyuncu, self.sihirliler)
        if carpisma:
            self.oyuncu.yanma_sesi.play()
            self.oyuncu.can -= 1
            if self.oyuncu.can <= 0:
                self.oyun_durdu(f"SKOR: {self.score}", "YENIDEN BASLAMAK ICIN ENTER TUSUNA BASINIZ")
                self.oyun_yenile()
            self.oyuncu.yenilenme()
        if carpisma1:
            self.score += self.round_numarasi * 100
            carpisma1.remove(self.kitaplar)
            if self.kitaplar:
                self.oyuncu.yakalama_sesi.play()
            else:
                self.oyuncu.yenilenme()
                self.yeni_round_baslatma()
        if carpisma2:
            self.score += 200 * self.round_numarasi
            self.oyuncu.s_kitap_sayi += 1
            self.sihirliler.remove(carpisma2)
            self.oyuncu.s_kitap_sesi.play()

    def yeni_round_baslatma(self):
        self.score += 10000 * self.round_numarasi // (1 + self.round_suresi)
        self.round_suresi = 0
        self.soguma = 0
        self.cerceve_sayisi = 0
        self.round_numarasi += 1

        for a in self.kitaplar:
            self.kitaplar.remove(a)
        for b in self.sihirliler:
            self.sihirliler.remove(b)
        for c in self.teknoloji:
            self.teknoloji.remove(c)

        for i in range(self.round_numarasi):
            for d in range(3):
                self.teknoloji.add(Teknoloji(random.randint(0, genislik - 64), random.randint(100, yukseklik - 164),
                                             self.teknoloji_resimleri[d], d))
        for i in range(3):
            self.kitaplar.add(Kitap(random.randint(0, genislik - 64), random.randint(100, yukseklik - 164)))
        self.ileri_seviye_muzigi.play()

    def oyun_durdu(self, ana_metin, baslangic_m):
        global durum
        beyaz = (255, 255, 255)
        siyah = (0, 0, 0)

        ana_metin = self.font.render(ana_metin, True, beyaz)
        ana_metin_kordinati = ana_metin.get_rect()
        ana_metin_kordinati.center = (genislik//2, yukseklik//2)

        baslik_metni = self.font.render(baslangic_m, True, beyaz)
        baslik_metni_kordinati = baslik_metni.get_rect()
        baslik_metni_kordinati.center = (genislik//2, yukseklik//2 + 64)

        goruntu_yuzeyi.fill(siyah)
        goruntu_yuzeyi.blit(ana_metin, ana_metin_kordinati)
        goruntu_yuzeyi.blit(baslik_metni, baslik_metni_kordinati)
        pygame.display.update()

        pygame.mixer.music.stop()

        durdu = True
        while durdu:
            for element in pygame.event.get():
                if element.type == pygame.KEYDOWN:
                    if element.key == pygame.K_RETURN:
                        durdu = False
                        pygame.mixer.music.play()
                elif element.type == pygame.QUIT:
                    durdu = False
                    durum = False

    def oyun_yenile(self):
        self.score = 0
        self.round_numarasi = 0
        self.oyuncu.can = 5
        self.oyuncu.s_kitap_sayi = 0
        self.oyuncu.yenilenme()
        self.yeni_round_baslatma()


class Oyuncu(pygame.sprite.Sprite):
    def __init__(self, teknolojiler):
        super().__init__()
        self.image = pygame.image.load("çocuk.png")
        self.tek = teknolojiler
        self.rect = self.image.get_rect()
        self.rect.centerx = genislik//2
        self.rect.bottom = yukseklik

        self.can = 5
        self.s_kitap_sayi = 0
        self.hiz = 8

        self.yakalama_sesi = pygame.mixer.Sound("yakalama.wav")
        self.yanma_sesi = pygame.mixer.Sound("yakalanma.wav")
        self.joker_sesi = pygame.mixer.Sound("joker.wav")
        self.s_kitap_sesi = pygame.mixer.Sound("joker.wav")

    def update(self):
        tus = pygame.key.get_pressed()
        if tus[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.hiz
        elif tus[pygame.K_RIGHT] and self.rect.right < genislik:
            self.rect.x += self.hiz
        elif tus[pygame.K_UP] and self.rect.top > 100:
            self.rect.y -= self.hiz
        elif tus[pygame.K_DOWN] and self.rect.bottom < yukseklik - 100:
            self.rect.y += self.hiz

    def canavar_sil(self):
        if self.s_kitap_sayi > 1:
            self.s_kitap_sayi -= 2
            self.joker_sesi.play()
            for k in self.tek:
                self.tek.remove(k)
                break

    def kurtul(self):
        if self.s_kitap_sayi > 0:
            self.s_kitap_sayi -= 1
            self.joker_sesi.play()
            self.rect.bottom = yukseklik

    def can_arttir(self):
        if self.s_kitap_sayi > 2:
            self.can += 1
            self.s_kitap_sayi -= 3
            self.s_kitap_sesi.play()
            self.yenilenme()

    def yenilenme(self):
        self.rect.centerx = genislik // 2
        self.rect.bottom = yukseklik


class Kitap(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("kitap.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])
        self.hiz = random.randint(1, 5)

    def update(self):
        self.rect.x += self.dx * self.hiz
        self.rect.y += self.dy * self.hiz

        if self.rect.left < 0 or self.rect.right > genislik:
            self.dx *= -1
        if self.rect.top < 100 or self.rect.bottom > yukseklik - 100:
            self.dy *= -1


class SKitap(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("şanslı_kitap.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])
        self.hiz = random.randint(1, 5)

    def update(self):
        self.rect.x += self.dx * self.hiz
        self.rect.y += self.dy * self.hiz

        if self.rect.left < 0 or self.rect.right > genislik:
            self.dx *= -1
        if self.rect.top < 100 or self.rect.bottom > yukseklik - 100:
            self.dy *= -1


class Teknoloji(pygame.sprite.Sprite):
    def __init__(self, x, y, image, tip):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.type = tip
        self.rect.topleft = (x, y)
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])
        self.hiz = random.randint(1, 5)

    def update(self):
        self.rect.x += self.dx * self.hiz
        self.rect.y += self.dy * self.hiz

        if self.rect.left < 0 or self.rect.right > genislik:
            self.dx *= -1
        if self.rect.top < 100 or self.rect.bottom > yukseklik - 100:
            self.dy *= -1


teknoloji_grubum = pygame.sprite.Group()
kitap_grubum = pygame.sprite.Group()
skitap_grubum = pygame.sprite.Group()

oyuncu_grubum = pygame.sprite.Group()
oyuncum = Oyuncu(teknoloji_grubum)
oyuncu_grubum.add(oyuncum)

oyunum = Oyun(oyuncum, kitap_grubum, skitap_grubum, teknoloji_grubum)
oyunum.oyun_durdu("KITAPLAR DOSTTUR", "BASLAMAK ICIN ENTER TUSUNA BASIN")
oyunum.oyun_yenile()

FPS = 30
saat = pygame.time.Clock()

durum = True
while durum:
    for etkinlik in pygame.event.get():
        if etkinlik.type == pygame.QUIT:
            durum = False
        if etkinlik.type == pygame.KEYDOWN:
            if etkinlik.key == pygame.K_r:
                oyuncum.canavar_sil()
            if etkinlik.key == pygame.K_e:
                oyuncum.kurtul()
            if etkinlik.key == pygame.K_h:
                oyuncum.can_arttir()
    goruntu_yuzeyi.fill((0, 0, 50))
    oyuncu_grubum.update()
    oyuncu_grubum.draw(goruntu_yuzeyi)
    teknoloji_grubum.update()
    teknoloji_grubum.draw(goruntu_yuzeyi)
    kitap_grubum.update()
    kitap_grubum.draw(goruntu_yuzeyi)
    skitap_grubum.update()
    skitap_grubum.draw(goruntu_yuzeyi)
    oyunum.update()
    oyunum.cizmek()
    pygame.display.update()
    saat.tick(FPS)
pygame.quit()
