
# SMAIL – E-mailovı klient pro seniory

Tento e-mailovı klient je pøizpùsoben pro seniory ve vìkové skupinì 90 let a více.  
Vyvinutı klient je snadno ovladatelnı a obsahuje pouze funkce, které mùe senior potøebovat.

## Prostøedí pro ètení e-mailovıch zpráv
SMAIL má prostøedí speciálnì navrené pro ètení e-mailù pøívìtivou formou, s velkımi a pøehlednımi tlaèítky a textem.  
![menu1](https://github.com/forsenior/senior-os/blob/9651ba7d8c7fbd04c794c4344ed667deeb5b5458/smail/screens/smail_screen1_cz.png)

## Prostøedí pro psaní e-mailovıch zpráv
Prostøedí pro psaní e-mailù je co nejjednodušší, s pøeddefinovanımi kontakty pro snadné odesílání.  
![menu2](https://github.com/forsenior/senior-os/blob/9651ba7d8c7fbd04c794c4344ed667deeb5b5458/smail/screens/smail_screen2_cz_.png)

## Potvrzení úspìšného odeslání e-mailu
Po úspìšném odeslání e-mailu zobrazí aplikace potvrzovací zprávu, e e-mail byl odeslán.  
![alert](https://github.com/forsenior/senior-os/blob/b772ef10bc80c3467e30be05966db91266d85aa3/smail/screens/smail_email_send_cz_.png)

## Varování pøi odesílání citlivıch údajù
Aplikace upozorní uivatele, kdy se chystá odeslat citlivé informace, èím pøidává další vrstvu zabezpeèení.  
![alert1](https://github.com/forsenior/senior-os/blob/b772ef10bc80c3467e30be05966db91266d85aa3/smail/screens/smail_sensitive_data_alert_cz.png)

## Varování pøi opuštìní neuloeného e-mailu
Aplikace varuje uivatele pøi pokusu o opuštìní rozepsané zprávy. Uivatel je vyzván k potvrzení, zda si pøeje e-mail zrušit.  
![alert2](https://github.com/forsenior/senior-os/blob/b772ef10bc80c3467e30be05966db91266d85aa3/smail/screens/smail_unconfirmed_email_cz.png)

## 1) Spuštìní aplikace – pouijte následující postup:
Stáhnìte si nejnovìjší ISO z [repozitáøe](https://github.com/forsenior/senior-os/releases).  
Vytvoøte novı virtuální stroj ve vámi zvoleném virtualizaèním prostøedí (napø. VirtualBox, VMware nebo QEMU) a pøidejte staené ISO.  
Toto ISO je distribuováno jako systém zaloenı na Linuxu.  
Spuste virtuální prostøedí a pokud se aplikace nespustí automaticky, spuste následující pøíkaz v terminálu:
```bash
srun
```

## 2) Pro snadnìjší úpravy a pøehled o aplikaci postupujte následovnì:

## Instalace
Pro spuštìní SMAIL postupujte podle následujících krokù pro naklonování repozitáøe a instalaci závislostí:

### Krok 1: Instalace Poetry
SMAIL pouívá Poetry pro správu závislostí a balení.  
Pokud nemáte Poetry nainstalované, nejprve jej nainstalujte.  
Mùete postupovat podle tohoto [podrobného návodu k instalaci Poetry](https://gist.github.com/Isfhan/b8b104c8095d8475eb377230300de9b0).

### Krok 2: Klonování repozitáøe a instalace závislostí
Po instalaci Poetry pokraèujte tìmito kroky:

```bash
# Klonování repozitáøe
git clone https://github.com/forsenior/senior-os

# Pøejdìte do sloky projektu
cd smail

# Sestavení a instalace závislostí pomocí Poetry
poetry build

poetry install
```

Tyto kroky opakujte i pro sloky *sconf* a *srun* (cd .. -> cd sconf -> poetry build -> poetry install):  
```bash
#Spuste tento pøíkaz ve sloce se stejnım názvem:
poetry run srun
#Nebo mùete pouít tento pøíkaz po nastavení konfiguraèního souboru:
poetry run smail
```

Podporované verze Pythonu: Tento program je testován a optimalizován pro Python 3.12.

## Poadovaná konfigurace pro SMAIL

Pro správné fungování e-mailového klienta SMAIL se doporuèuje nejprve upravit konfiguraèní soubory.  
Pro doèasnou konfiguraci mùete upravit hlavní konfiguraèní soubor config.json, kterı se nachází v domovském adresáøi (napø. C:\Users\user\.sconf\config.json).  
Pokud není pøítomen, zkopírujte nebo vytvoøte soubor config.json (soubor se automaticky vytvoøí po spuštìní *srun*).  
Pro trvalé nastavení, které bude fungovat kontinuálnì, je tøeba upravit soubor `smail_configuration.py`, kterı se nachází v `sconf/src/sconf/models/`.  
Bìhem tohoto procesu zadejte svou vlastní e-mailovou adresu a heslo pro personalizaci aplikace.  
Vıchozí nastavení jsou k dispozici, ale pro lepší zabezpeèení a pøizpùsobení se doporuèuje pouít vlastní údaje.

### Generování hesla pro SMAIL

Pro pøipojení ke svému Gmail úètu z newebového prostøedí, jako je aplikace SMAIL, je potøeba vygenerovat heslo pro aplikaci.  
Postupujte následovnì:

1. Pøejdìte do nastavení úètu Google na stránce *Google úèet*.

2. Otevøete záloku „Zabezpeèení“.

3. V èásti „Pøihlášení do Googlu“ vyhledejte a vyberte „Dvoufázové ovìøení“.

4. Po ovìøení identity pøejdìte dolù do èásti „Hesla pro aplikace“.

5. Vyberte monost pro vytvoøení nového hesla pro aplikaci.

6. Zvolte aplikaci nebo zaøízení, pro které heslo vytváøíte.

7. Postupujte podle pokynù pro vygenerování hesla.

8. Zkopírujte vygenerované heslo a pouijte ho v aplikaci SGIVE pro bezpeèné pøipojení e-mailového klienta k vašemu Gmail úètu.

Pokud nemùete najít správnou sekci, pouijte tento odkaz: [Hesla pro aplikace](https://myaccount.google.com/apppasswords)

## Spuštìní aplikace SMAIL

Pro spuštìní aplikace postupujte následovnì:

1. **Otevøete své preferované IDE**  
   Spuste vámi zvolené vıvojové prostøedí, napøíklad PyCharm nebo jiné.

2. **Pøejdìte do adresáøe smail**  
   Pomocí správce souborù v IDE otevøete sloku `smail` v rámci naklonovaného repozitáøe.

3. **Otevøete terminál v této sloce**  
   Ujistìte se, e máte aktivní terminálovou relaci ve sloce `smail`.

4. **Ujistìte se, e jsou nainstalovány všechny potøebné závislosti**  
   Ovìøte, e jsou všechny závislosti správnì nainstalovány. Mùete postupovat dle sekce [Instalace](#instalace).

5. **Nastavte konfiguraci a heslo pro aplikaci**  
   Pøed spuštìním aplikace nastavte konfiguraci a vygenerujte heslo dle sekce [Generování hesla](#generovani-hesla-pro-smail).

6. **Spuste aplikaci**  
   Jakmile je vše pøipraveno, spuste aplikaci tímto pøíkazem:
```bash
cd smail
poetry run smail
```
