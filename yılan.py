import pygame
import random

# Pygame modülünü başlat
pygame.init()

# Oyun ekranını ayarla
ekran_genişliği = 800
ekran_yüksekliği = 600
ekran = pygame.display.set_mode((ekran_genişliği, ekran_yüksekliği))
pygame.display.set_caption("Yılan Oyunu")

# Oyun ayarları
beyaz = (255, 255, 255)
siyah = (0, 0, 0)
yeşil = (0, 255, 0)
kırmızı = (255, 0, 0)
gri = (128, 128, 128)
blok_boyutu = 20
oyuncu_hızı = 20

# Fonksiyonlar
def yem_oluştur():
    x = random.randrange(0, (ekran_genişliği - blok_boyutu) // blok_boyutu) * blok_boyutu
    y = random.randrange(0, (ekran_yüksekliği - blok_boyutu) // blok_boyutu) * blok_boyutu
    return [x, y]

def oyunu_başlat():
    global oyuncu_pozisyonu, oyuncu_yönü, oyuncu_uzunluğu, yılan, yemek_pozisyonu, skor, oyun_devam_ediyor
    oyuncu_pozisyonu = [ekran_genişliği // 2, ekran_yüksekliği // 2]
    oyuncu_yönü = "SAĞ"
    oyuncu_uzunluğu = 1
    yılan = [oyuncu_pozisyonu[:]]
    yemek_pozisyonu = yem_oluştur()
    skor = 0
    oyun_devam_ediyor = True

def buton_çiz(metin, x, y, genişlik, yükseklik, aktif_renk, pasif_renk, aksiyon=None):
    fare_poz = pygame.mouse.get_pos()
    tıklama = pygame.mouse.get_pressed()
    
    if x < fare_poz[0] < x + genişlik and y < fare_poz[1] < y + yükseklik:
        pygame.draw.rect(ekran, aktif_renk, (x, y, genişlik, yükseklik))
        if tıklama[0] == 1 and aksiyon != None:
            aksiyon()
    else:
        pygame.draw.rect(ekran, pasif_renk, (x, y, genişlik, yükseklik))
    
    yazı_fontu = pygame.font.SysFont(None, 36)
    metin_yüzey = yazı_fontu.render(metin, True, siyah)
    metin_dikdörtgen = metin_yüzey.get_rect()
    metin_dikdörtgen.center = (x + genişlik // 2, y + yükseklik // 2)
    ekran.blit(metin_yüzey, metin_dikdörtgen)

# Oyunu başlat
oyunu_başlat()

# Ana oyun döngüsü
çalışıyor = True
while çalışıyor:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            çalışıyor = False
        elif olay.type == pygame.KEYDOWN and oyun_devam_ediyor:
            if olay.key == pygame.K_UP and oyuncu_yönü != "ALT":
                oyuncu_yönü = "ÜST"
            elif olay.key == pygame.K_DOWN and oyuncu_yönü != "ÜST":
                oyuncu_yönü = "ALT"
            elif olay.key == pygame.K_LEFT and oyuncu_yönü != "SAĞ":
                oyuncu_yönü = "SOL"
            elif olay.key == pygame.K_RIGHT and oyuncu_yönü != "SOL":
                oyuncu_yönü = "SAĞ"

    if oyun_devam_ediyor:
        # Oyuncu hareketini güncelle
        if oyuncu_yönü == "SAĞ":
            oyuncu_pozisyonu[0] += oyuncu_hızı
        elif oyuncu_yönü == "SOL":
            oyuncu_pozisyonu[0] -= oyuncu_hızı
        elif oyuncu_yönü == "ÜST":
            oyuncu_pozisyonu[1] -= oyuncu_hızı
        elif oyuncu_yönü == "ALT":
            oyuncu_pozisyonu[1] += oyuncu_hızı

        # Yılanın hareketini güncelle
        yılan.insert(0, oyuncu_pozisyonu[:])
        if oyuncu_pozisyonu == yemek_pozisyonu:
            skor += 1
            oyuncu_uzunluğu += 1
            yemek_pozisyonu = yem_oluştur()
        else:
            if len(yılan) > oyuncu_uzunluğu:
                yılan.pop()

        # Çarpışma kontrolü
        if (oyuncu_pozisyonu[0] < 0 or oyuncu_pozisyonu[0] >= ekran_genişliği or
            oyuncu_pozisyonu[1] < 0 or oyuncu_pozisyonu[1] >= ekran_yüksekliği):
            oyun_devam_ediyor = False
        for blok in yılan[1:]:
            if oyuncu_pozisyonu == blok:
                oyun_devam_ediyor = False

        # Ekranı temizle
        ekran.fill(siyah)

        # Oyun öğelerini çiz
        pygame.draw.rect(ekran, yeşil, pygame.Rect(yemek_pozisyonu[0], yemek_pozisyonu[1], blok_boyutu, blok_boyutu))
        for blok in yılan:
            pygame.draw.rect(ekran, beyaz, pygame.Rect(blok[0], blok[1], blok_boyutu, blok_boyutu))

        # Skor ve oyunu güncelle
        yazı_fontu = pygame.font.SysFont(None, 36)
        skor_yazısı = yazı_fontu.render("Skor: " + str(skor), True, beyaz)
        ekran.blit(skor_yazısı, (10, 10))
    else:
        ekran.fill(siyah)
        oyun_bitti_yazısı = pygame.font.SysFont(None, 72).render("Oyun Bitti! Skor: " + str(skor), True, beyaz)
        ekran.blit(oyun_bitti_yazısı, (ekran_genişliği//2 - oyun_bitti_yazısı.get_width()//2, ekran_yüksekliği//2 - 100))
        
        buton_çiz("Tekrar Başlat", ekran_genişliği//2 - 100, ekran_yüksekliği//2, 200, 50, kırmızı, gri, oyunu_başlat)
        buton_çiz("Çık", ekran_genişliği//2 - 100, ekran_yüksekliği//2 + 70, 200, 50, kırmızı, gri, pygame.quit)

    pygame.display.flip()

    # Oyun hızını ayarla
    pygame.time.Clock().tick(10)

# Oyun bittiğinde Pygame'i kapat
pygame.quit()