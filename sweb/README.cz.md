# 📖 Choose your language / Wählen Sie Ihre Sprache / Zvolte si jazyk

- [English](README.md)
- [Deutsch](README.de.md)
- [Čeština](README.cz.md)
  
# Webový prohlížeč pro seniory a osoby s mentálním postižením

## Přehled aplikace

Tento projekt je webový prohlížeč určený pro seniory, vytvořený pomocí PyQt5, s důrazem na přístupnost, jednoduchost a bezpečnost.
Cílem je vytvořit uživatelsky přívětivější prostředí pro starší dospělé osoby pomocí funkcí, jako je lepší čitelnost textu, intuitivní navigace,
podpora zvuku, možnosti více jazyků a robustní bezpečnostní opatření k ochraně před phishingovými weby.
Níže je uveden návrh designu webového prohlížeče:

## Přehled MENU1
MENU1 poskytuje uživatelsky přívětivé rozhraní se pěti velkými tlačítky s pevnou velikostí, navrženými pro snadnou navigaci, zvláště pro seniory.

<img src="screens/sweb_screen_1.png" width="900" />

Funkce tlačítek:

1. Tlačítko MENU1: Přepne panel nabídeky na MENU2.
2. Tlačítko Ukončit: Zavře aplikaci.
3. Tlačítka webových stránek (3): Otevírají předdefinované webové stránky.
   
## Přehled MENU2
MENU2 obsahuje pět tlačítek s následujícími funkcemi:

<img src="screens/sweb_screen_2.png" width="900" />

Funkce tlačítek:

1. Tlačítko MENU2: Přepne panel nabídeky zpět na MENU1.
2. Tlačítka webových stránek (3): Otevírají předdefinované webové stránky.
3. Tlačítko Hledat: Otevírá vyhledávací pole pro uživatelské dotazy.

## Detekce phishingových webů
Tato funkce je klíčovou součástí naší aplikace a upozorňuje uživatele, pokud je webová stránka potenciálně phishingová.

<img src="screens/sweb_screen_3.png" width="900" />

- Varování před phishingem: Pokud uživatel zadá známou phishingovou URL adresu, změní se pozadí panelu nástrojů na červenou, aby byla snadno viditelná, zejména pro seniory.
- Níže je znázorněn diagram znázorňující proces detekce phishingových URL adres.
<p align="center">
  <img src="screens/sweb_phishing.gif" width="70%" />
</p>
Podrobnější informace o fungování detekce phishingu budou uvedeny v dokumentaci.

## Instalace

### Spuštění aplikace  

Pro spuštění aplikace postupujte podle těchto kroků:  

1. Stáhněte si nejnovější ISO z repozitáře [zde](https://github.com/forsenior/senior-os/releases).  
2. Vytvořte nový virtuální stroj v preferované virtualizačním softwaru (např. VirtualBox, VMware nebo QEMU).  
3. Připojte stažený ISO soubor k virtuálnímu stroji nebo vytvořte zaváděcí USB disk. ISO je založeno na linuxové distribuci (Archie).  
4. Spusťte virtuální stroj. Pokud se aplikace nespustí automaticky, otevřete terminál a spusťte:  

   ```sh
   srun
   ```  

---

### Instalace a nastavení vývoje  

Pro snadnější úpravy a lepší přehled aplikace postupujte podle těchto kroků:  

#### Krok 1: Instalace Poetry  

SWEB používá [Poetry](https://python-poetry.org/) pro správu závislostí a balíčkování. Pokud nemáte Poetry nainstalováno, postupujte podle oficiálního [průvodce instalací](https://python-poetry.org/docs/#installation).  

#### Krok 2: Klonování repozitáře a instalace závislostí  

Po instalaci Poetry pokračujte takto:  

```sh
# Klonování repozitáře projektu
git clone https://github.com/forsenior/senior-os  

# Přechod do adresáře projektu
cd sweb  

# Instalace závislostí
poetry build  
poetry install  
```  

Tyto kroky opakujte i pro adresáře `sconf` a `srun`:  

```sh
cd ..  
cd sconf  
poetry build  
poetry install  

cd ..  
cd srun  
poetry build  
poetry install  
```  

#### Spuštění aplikace  

Pro spuštění SWEB použijte:  

```sh
poetry run sweb  
```  

**Podporované verze Pythonu:**  
Tento program je testován a optimalizován pro **Python 3.12**.  
> [!NOTE]
> Pokud se pokusíte spustit aplikaci SWEB samostatně, můžete narazit na chybu kvůli umístění konfiguračního souboru. Ve výchozím nastavení by se config.json měl nacházet zde:  
> "$HOME/$USER/.sconf/config.json"

## Demonstracní video

https://github.com/user-attachments/assets/88fbb138-6467-47d3-ad12-a0fb98515719

# Jak přispět
Můžete zasílat pull requesty nebo hlásit chyby a návrhy na vylepšení.

## Licence
Tento projekt je licencován pod licencí MIT.


