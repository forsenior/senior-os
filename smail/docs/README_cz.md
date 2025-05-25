
# SMAIL – E-mailový klient pro seniory

Tento e-mailový klient je přizpůsoben pro seniory ve věkové skupině 90 let a více.  
Vyvinutý klient je snadno ovladatelný a obsahuje pouze funkce, které může senior potřebovat.

## Prostředí pro čtení e-mailových zpráv
SMAIL má prostředí speciálně navržené pro čtení e-mailů přívětivou formou, s velkými a přehlednými tlačítky a textem.  
![menu1](https://github.com/forsenior/senior-os/blob/6eb5618b83e951d328ce9a7cb85962fc49fd6fa3/smail/screens/smail_screen1_cz.png)

## Prostředí pro psaní e-mailových zpráv
Prostředí pro psaní e-mailů je co nejjednodušší, s předdefinovanými kontakty pro snadné odesílání.  
![menu2](https://github.com/forsenior/senior-os/blob/6eb5618b83e951d328ce9a7cb85962fc49fd6fa3/smail/screens/smail_screen2_cz.png)

## Potvrzení úspěšného odeslání e-mailu
Po úspěšném odeslání e-mailu zobrazí aplikace potvrzovací zprávu, že e-mail byl odeslán.  
![alert](https://github.com/forsenior/senior-os/blob/6eb5618b83e951d328ce9a7cb85962fc49fd6fa3/smail/screens/smail_email_send_cz.png)

## Varování při odesílání citlivých údajů
Aplikace upozorní uživatele, když se chystá odeslat citlivé informace, čímž přidává další vrstvu zabezpečení.  
![alert1](https://github.com/forsenior/senior-os/blob/6eb5618b83e951d328ce9a7cb85962fc49fd6fa3/smail/screens/smail_sensitive_data_alert_cz.png)

## Varování při opuštění neuloženého e-mailu
Aplikace varuje uživatele při pokusu o opuštění rozepsané zprávy. Uživatel je vyzván k potvrzení, zda si přeje e-mail zrušit.  
![alert2](https://github.com/forsenior/senior-os/blob/6eb5618b83e951d328ce9a7cb85962fc49fd6fa3/smail/screens/smail_unconfirmed_email_cz.png)

## 1) Spuštění aplikace – použijte následující postup:
Stáhněte si nejnovější ISO z [repozitáře](https://github.com/forsenior/senior-os/releases).  
Vytvořte nový virtuální stroj ve vámi zvoleném virtualizačním prostředí (např. VirtualBox, VMware nebo QEMU) a přidejte stažené ISO.  
Toto ISO je distribuováno jako systém založený na Linuxu.  
Spusťte virtuální prostředí a pokud se aplikace nespustí automaticky, spusťte následující příkaz v terminálu:
```bash
srun
```

## 2) Pro snadnější úpravy a přehled o aplikaci postupujte následovně:

## Instalace
Pro spuštění SMAIL postupujte podle následujících kroků pro naklonování repozitáře a instalaci závislostí:

### Krok 1: Instalace Poetry
SMAIL používá Poetry pro správu závislostí a balení.  
Pokud nemáte Poetry nainstalované, nejprve jej nainstalujte.  
Můžete postupovat podle tohoto [podrobného návodu k instalaci Poetry](https://gist.github.com/Isfhan/b8b104c8095d8475eb377230300de9b0).

### Krok 2: Klonování repozitáře a instalace závislostí
Po instalaci Poetry pokračujte těmito kroky:

```bash
# Klonování repozitáře
git clone https://github.com/forsenior/senior-os

# Přejděte do složky projektu
cd smail

# Sestavení a instalace závislostí pomocí Poetry
poetry build

poetry install
```

Tyto kroky opakujte i pro složky *sconf* a *srun* (cd .. -> cd sconf -> poetry build -> poetry install):  
```bash
#Spusťte tento příkaz ve složce se stejným názvem:
poetry run srun
#Nebo můžete použít tento příkaz po nastavení konfiguračního souboru:
poetry run smail
```

Podporované verze Pythonu: Tento program je testován a optimalizován pro Python 3.12.

## Požadovaná konfigurace pro SMAIL

Pro správné fungování e-mailového klienta SMAIL se doporučuje nejprve upravit konfigurační soubory.  
Pro dočasnou konfiguraci můžete upravit hlavní konfigurační soubor config.json, který se nachází v domovském adresáři (např. C:\Users\user\.sconf\config.json).  
Pokud není přítomen, zkopírujte nebo vytvořte soubor config.json (soubor se automaticky vytvoří po spuštění *srun*).  
Pro trvalé nastavení, které bude fungovat kontinuálně, je třeba upravit soubor `smail_configuration.py`, který se nachází v `sconf/src/sconf/models/`.  
Během tohoto procesu zadejte svou vlastní e-mailovou adresu a heslo pro personalizaci aplikace.  
Výchozí nastavení jsou k dispozici, ale pro lepší zabezpečení a přizpůsobení se doporučuje použít vlastní údaje.

### Generování hesla pro SMAIL

Pro připojení ke svému Gmail účtu z newebového prostředí, jako je aplikace SMAIL, je potřeba vygenerovat heslo pro aplikaci.  
Postupujte následovně:

1. Přejděte do nastavení účtu Google na stránce *Google účet*.

2. Otevřete záložku „Zabezpečení“.

3. V části „Přihlášení do Googlu“ vyhledejte a vyberte „Dvoufázové ověření“.

4. Po ověření identity přejděte dolů do části „Hesla pro aplikace“.

5. Vyberte možnost pro vytvoření nového hesla pro aplikaci.

6. Zvolte aplikaci nebo zařízení, pro které heslo vytváříte.

7. Postupujte podle pokynů pro vygenerování hesla.

8. Zkopírujte vygenerované heslo a použijte ho v aplikaci SGIVE pro bezpečné připojení e-mailového klienta k vašemu Gmail účtu.

Pokud nemůžete najít správnou sekci, použijte tento odkaz: [Hesla pro aplikace](https://myaccount.google.com/apppasswords)

## Spuštění aplikace SMAIL

Pro spuštění aplikace postupujte následovně:

1. **Otevřete své preferované IDE**  
   Spusťte vámi zvolené vývojové prostředí, například PyCharm nebo jiné.

2. **Přejděte do adresáře smail**  
   Pomocí správce souborů v IDE otevřete složku `smail` v rámci naklonovaného repozitáře.

3. **Otevřete terminál v této složce**  
   Ujistěte se, že máte aktivní terminálovou relaci ve složce `smail`.

4. **Ujistěte se, že jsou nainstalovány všechny potřebné závislosti**  
   Ověřte, že jsou všechny závislosti správně nainstalovány. Můžete postupovat dle sekce [Instalace](#instalace).

5. **Nastavte konfiguraci a heslo pro aplikaci**  
   Před spuštěním aplikace nastavte konfiguraci a vygenerujte heslo dle sekce [Generování hesla](#generovani-hesla-pro-smail).

6. **Spusťte aplikaci**  
   Jakmile je vše připraveno, spusťte aplikaci tímto příkazem:
```bash
cd smail
poetry run smail
```
