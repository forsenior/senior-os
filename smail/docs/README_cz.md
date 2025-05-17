
# SMAIL � E-mailov� klient pro seniory

Tento e-mailov� klient je p�izp�soben pro seniory ve v�kov� skupin� 90 let a v�ce.  
Vyvinut� klient je snadno ovladateln� a obsahuje pouze funkce, kter� m��e senior pot�ebovat.

## Prost�ed� pro �ten� e-mailov�ch zpr�v
SMAIL m� prost�ed� speci�ln� navr�en� pro �ten� e-mail� p��v�tivou formou, s velk�mi a p�ehledn�mi tla��tky a textem.  
![menu1](https://github.com/forsenior/senior-os/blob/9651ba7d8c7fbd04c794c4344ed667deeb5b5458/smail/screens/smail_screen1_cz.png)

## Prost�ed� pro psan� e-mailov�ch zpr�v
Prost�ed� pro psan� e-mail� je co nejjednodu���, s p�eddefinovan�mi kontakty pro snadn� odes�l�n�.  
![menu2](https://github.com/forsenior/senior-os/blob/9651ba7d8c7fbd04c794c4344ed667deeb5b5458/smail/screens/smail_screen2_cz_.png)

## Potvrzen� �sp�n�ho odesl�n� e-mailu
Po �sp�n�m odesl�n� e-mailu zobraz� aplikace potvrzovac� zpr�vu, �e e-mail byl odesl�n.  
![alert](https://github.com/forsenior/senior-os/blob/b772ef10bc80c3467e30be05966db91266d85aa3/smail/screens/smail_email_send_cz_.png)

## Varov�n� p�i odes�l�n� citliv�ch �daj�
Aplikace upozorn� u�ivatele, kdy� se chyst� odeslat citliv� informace, ��m� p�id�v� dal�� vrstvu zabezpe�en�.  
![alert1](https://github.com/forsenior/senior-os/blob/b772ef10bc80c3467e30be05966db91266d85aa3/smail/screens/smail_sensitive_data_alert_cz.png)

## Varov�n� p�i opu�t�n� neulo�en�ho e-mailu
Aplikace varuje u�ivatele p�i pokusu o opu�t�n� rozepsan� zpr�vy. U�ivatel je vyzv�n k potvrzen�, zda si p�eje e-mail zru�it.  
![alert2](https://github.com/forsenior/senior-os/blob/b772ef10bc80c3467e30be05966db91266d85aa3/smail/screens/smail_unconfirmed_email_cz.png)

## 1) Spu�t�n� aplikace � pou�ijte n�sleduj�c� postup:
St�hn�te si nejnov�j�� ISO z [repozit��e](https://github.com/forsenior/senior-os/releases).  
Vytvo�te nov� virtu�ln� stroj ve v�mi zvolen�m virtualiza�n�m prost�ed� (nap�. VirtualBox, VMware nebo QEMU) a p�idejte sta�en� ISO.  
Toto ISO je distribuov�no jako syst�m zalo�en� na Linuxu.  
Spus�te virtu�ln� prost�ed� a pokud se aplikace nespust� automaticky, spus�te n�sleduj�c� p��kaz v termin�lu:
```bash
srun
```

## 2) Pro snadn�j�� �pravy a p�ehled o aplikaci postupujte n�sledovn�:

## Instalace
Pro spu�t�n� SMAIL postupujte podle n�sleduj�c�ch krok� pro naklonov�n� repozit��e a instalaci z�vislost�:

### Krok 1: Instalace Poetry
SMAIL pou��v� Poetry pro spr�vu z�vislost� a balen�.  
Pokud nem�te Poetry nainstalovan�, nejprve jej nainstalujte.  
M��ete postupovat podle tohoto [podrobn�ho n�vodu k instalaci Poetry](https://gist.github.com/Isfhan/b8b104c8095d8475eb377230300de9b0).

### Krok 2: Klonov�n� repozit��e a instalace z�vislost�
Po instalaci Poetry pokra�ujte t�mito kroky:

```bash
# Klonov�n� repozit��e
git clone https://github.com/forsenior/senior-os

# P�ejd�te do slo�ky projektu
cd smail

# Sestaven� a instalace z�vislost� pomoc� Poetry
poetry build

poetry install
```

Tyto kroky opakujte i pro slo�ky *sconf* a *srun* (cd .. -> cd sconf -> poetry build -> poetry install):  
```bash
#Spus�te tento p��kaz ve slo�ce se stejn�m n�zvem:
poetry run srun
#Nebo m��ete pou��t tento p��kaz po nastaven� konfigura�n�ho souboru:
poetry run smail
```

Podporovan� verze Pythonu: Tento program je testov�n a optimalizov�n pro Python 3.12.

## Po�adovan� konfigurace pro SMAIL

Pro spr�vn� fungov�n� e-mailov�ho klienta SMAIL se doporu�uje nejprve upravit konfigura�n� soubory.  
Pro do�asnou konfiguraci m��ete upravit hlavn� konfigura�n� soubor config.json, kter� se nach�z� v domovsk�m adres��i (nap�. C:\Users\user\.sconf\config.json).  
Pokud nen� p��tomen, zkop�rujte nebo vytvo�te soubor config.json (soubor se automaticky vytvo�� po spu�t�n� *srun*).  
Pro trval� nastaven�, kter� bude fungovat kontinu�ln�, je t�eba upravit soubor `smail_configuration.py`, kter� se nach�z� v `sconf/src/sconf/models/`.  
B�hem tohoto procesu zadejte svou vlastn� e-mailovou adresu a heslo pro personalizaci aplikace.  
V�choz� nastaven� jsou k dispozici, ale pro lep�� zabezpe�en� a p�izp�soben� se doporu�uje pou��t vlastn� �daje.

### Generov�n� hesla pro SMAIL

Pro p�ipojen� ke sv�mu Gmail ��tu z newebov�ho prost�ed�, jako je aplikace SMAIL, je pot�eba vygenerovat heslo pro aplikaci.  
Postupujte n�sledovn�:

1. P�ejd�te do nastaven� ��tu Google na str�nce *Google ��et*.

2. Otev�ete z�lo�ku �Zabezpe�en�.

3. V ��sti �P�ihl�en� do Googlu� vyhledejte a vyberte �Dvouf�zov� ov��en�.

4. Po ov��en� identity p�ejd�te dol� do ��sti �Hesla pro aplikace�.

5. Vyberte mo�nost pro vytvo�en� nov�ho hesla pro aplikaci.

6. Zvolte aplikaci nebo za��zen�, pro kter� heslo vytv���te.

7. Postupujte podle pokyn� pro vygenerov�n� hesla.

8. Zkop�rujte vygenerovan� heslo a pou�ijte ho v aplikaci SGIVE pro bezpe�n� p�ipojen� e-mailov�ho klienta k va�emu Gmail ��tu.

Pokud nem��ete naj�t spr�vnou sekci, pou�ijte tento odkaz: [Hesla pro aplikace](https://myaccount.google.com/apppasswords)

## Spu�t�n� aplikace SMAIL

Pro spu�t�n� aplikace postupujte n�sledovn�:

1. **Otev�ete sv� preferovan� IDE**  
   Spus�te v�mi zvolen� v�vojov� prost�ed�, nap��klad PyCharm nebo jin�.

2. **P�ejd�te do adres��e smail**  
   Pomoc� spr�vce soubor� v IDE otev�ete slo�ku `smail` v r�mci naklonovan�ho repozit��e.

3. **Otev�ete termin�l v t�to slo�ce**  
   Ujist�te se, �e m�te aktivn� termin�lovou relaci ve slo�ce `smail`.

4. **Ujist�te se, �e jsou nainstalov�ny v�echny pot�ebn� z�vislosti**  
   Ov��te, �e jsou v�echny z�vislosti spr�vn� nainstalov�ny. M��ete postupovat dle sekce [Instalace](#instalace).

5. **Nastavte konfiguraci a heslo pro aplikaci**  
   P�ed spu�t�n�m aplikace nastavte konfiguraci a vygenerujte heslo dle sekce [Generov�n� hesla](#generovani-hesla-pro-smail).

6. **Spus�te aplikaci**  
   Jakmile je v�e p�ipraveno, spus�te aplikaci t�mto p��kazem:
```bash
cd smail
poetry run smail
```
