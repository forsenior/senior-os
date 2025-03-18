# Webový prohlížeč pro seniory a osoby s mentálním postižením

## Přehled aplikací

Tento projekt je webový prohlížeč přizpůsobený pro seniory, vytvořený pomocí PyQt5, s velkým důrazem na přístupnost, jednoduchost a bezpečnost. 
Jeho cílem je vytvořit uživatelsky přívětivější prostředí pro seniory tím, že nabízí funkce, jako je lepší čitelnost textu, intuitivní navigace, 
podpora zvuku, vícejazyčné možnosti a robustní bezpečnostní opatření na ochranu před podvodnými webovými stránkami. 
Níže je uveden koncept designu webového prohlížeče:

## MENU1 Přehled
MENU1 poskytuje uživatelsky přívětivé rozhraní se čtyřmi velkými tlačítky pevné velikosti, navrženými pro snadnou navigaci zejména pro seniory.

<img src=„screens/sweb_screen_1.png“ width=„900“ />

Akce tlačítek:

1. Tlačítko MENU1: Přepne panel nabídek na MENU2.
2. Tlačítko Exit: Zavře aplikaci.
3. Tlačítka webových stránek (3): Tlačítka pro spuštění aplikace: Otevírají odkazy na předdefinované webové stránky.
   
## MENU2 Přehled
MENU2 obsahuje pět tlačítek s následujícími funkcemi:

<img src=„screens/sweb_screen_2.png“ width=„900“ />

Akce tlačítek:

1. Tlačítko MENU2: Přepne panel nabídek zpět na MENU1.
2. Tlačítka webových stránek (3): Tlačítko MENU 3: Otevírají odkazy na předdefinované webové stránky.
3. Tlačítko pro vyhledávání: Otevře vyhledávací panel pro dotazy uživatele.

## Detekce phishingových webových stránek
Tato funkce je jádrem naší aplikace a upozorňuje uživatele, pokud je webová stránka potenciálně phishingová.

<img src=„screens/sweb_screen_3.png“ width=„900“ />

- Upozornění na phishing: Pokud uživatel zadá známou phishingovou adresu URL, pozadí panelu nástrojů se změní na červené, aby bylo snadno viditelné, zejména pro seniory.

Podrobnější informace o fungování detektoru phishingu budou uvedeny v dokumentaci.

## Instalace

!!!Ujistěte se, že máte v systému nainstalovaný Python3 nebo pip.
Podle následujících kroků nastavte webový prohlížeč v operačním systému FEDORA:

```bash
# Nainstalujte požadované balíčky Pythonu pomocí dnf, pokud používáte Fedoru.
sudo dnf install python3

# Naklonujte repozitář projektu
git clone https://github.com/forsenior/senior-os

# Nainstalujte požadavky z souboru requirements.txt v adresáři sweb
py -m pip install -r requirements.txt

```
      

## Demonstrační video

https://github.com/user-attachments/assets/88fbb138-6467-47d3-ad12-a0fb98515719




# Jak přispět
Pokud narazíte na nějaký problém nebo máte návrhy na zlepšení, neváhejte odesílat žádosti o stažení nebo vznášet problémy.

## Licence
Tento projekt je licencován pod licencí MIT.