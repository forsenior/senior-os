# <p align="center">Návod na použití aplikace SWEB</p>
## Ovládání aplikace:
Aplikace má hlavní ovládací panel, který obsahuje 5 tlačítek pro jedno menu (celkově 10 tlačítek):  
 ![MENU_1](https://github.com/forsenior/senior-os/blob/main/sweb/screens/sweb_menu1.png)
 ![MENU_2](https://github.com/forsenior/senior-os/blob/main/sweb/screens/sweb_menu2_cz.png)
1.	**Menu** – umožňuje přepínat mezi dvěma různými částmi aplikace (Menu 1 a Menu 2).
2.	**Červené tlačítko s bílým křížkem** – slouží k ukončení aplikace.
3.	**Tlačítka s ikonami webů** – rychlý přístup na konkrétní webovou stránku, jedno kliknutí a webová stránka se otevře na obrazovce. 
4.	**Tlačítko "Vyhledávání"** –  otevře prázdné pole, do kterého může uživatel zadat libovolnou webovou adresu.

## Otevření webové stránky
- **Úroveň ochrany 1: Základní ochrana**
1. **Otevření prostřednictvím nabídky:** Kliknutím na libovolné tlačítko nebo ikonu v MENU 1/2 otevřete webovou stránku přímo.
2. **Otevření prostřednictvím vyhledávání:** Otevřete webovou stránku pomocí vyhledávání. Klikněte na tlačítko vyhledávání, zadejte hledaný text a zadání bude zkontrolováno podle blacklistu a detekce phishingu pomocí neuronové sítě.

- **Úroveň ochrany 2: Zvýšená ochrana**
1. **Otevření prostřednictvím nabídky:** Kliknutím na libovolné tlačítko nebo ikonu v MENU 1/2 se webová stránka otevře přímo.
2. **Otevření prostřednictvím vyhledávání:** Otevřete webovou stránku, kterou chcete otevřít: Klikněte na tlačítko vyhledávání, zadejte hledaný text a vstup bude ověřen podle bílé listiny. Systém otevře pouze ty adresy URL, které odpovídají zadání na Whitelistu.
  
- **Úroveň ochrany 3: Maximální ochrana**
1. **Otevření prostřednictvím nabídky:** Kliknutím na libovolné tlačítko nebo ikonu v MENU 1/2 se webová stránka otevře přímo.
2. **Žádné vyhledávání:** Tlačítko pro vyhledávání bude zakázáno a funkce vyhledávání není na této úrovni ochrany k dispozici.

## Upozornění na detekci phishingu:

- **Detekce phishingu:**
   - Zadání adresy URL nebo návštěva webu: Při zadávání adresy URL nebo návštěvě webové stránky systém zkontroluje, zda je adresa URL uvedena na černé listině nebo zda je prostřednictvím neuronové sítě detekována jako phishingová.
- **Mechanismus upozornění:**
   - Pokud je detekována potenciální hrozba phishingu, tlačítko na panelu nabídky změní barvu na červenou, aby uživatele upozornilo na potenciální nebezpečí.
- **Ignorování výstrahy:**
   - Pokud uživatel ignoruje červené upozornění a pokračuje v zadávání jakýchkoli údajů na webové stránce, aplikace automaticky odešle e-mailové upozornění opatrovníkovi, aby ho informovala o podezřelé aktivitě.

