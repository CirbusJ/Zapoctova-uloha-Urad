class Udalost:
    def __init__(self, kdo, co, kdy):
        self.kdo = kdo
        self.co = co
        self.kdy = kdy

class Kalendar:
    def __init__(self):
        self.kal = []
    def prvni(self):
        if self.kal == []: return None
        self.min = 0
        self.cas = self.kal[0].kdy
        for i in range(1, len(self.kal)):
            if self.kal[i].kdy < self.cas:
                self.min, self.cas = i, self.kal[i].kdy
        return(self.kal.pop(self.min))
    def zarad(self, u):
        self.kal.append(u)
    def vyrad(self, a):
        for u in self.kal:
            if u.kdo == a:
                self.kal.remove(u)
                break

class Oddeleni:
    def __init__(self,patro):
        self.patro=patro
        self.jednani=False
        self.fronta_jednani=[]
        self.fronta_vytah=[]

class Vytah:
    def __init__(self,max_kapacita,cas_nastupu,cas_jizdy_o_jedno_patro):
        self.kapacita=max_kapacita
        self.uzivatele=[]
        self.kamjet=[]
        self.kamjet_kabina=[]
        self.patro=0
        self.smer=0
        self.nastup=cas_nastupu
        self.rychlost=cas_jizdy_o_jedno_patro
        self.cas_provozu=0

    def naplanuj(self, co, kdy):
        k.zarad(Udalost(self, co, kdy))

    def zpracujudalost(self,co):
        if co==8: # jede o jedno patro
            if len(self.kamjet_kabina)!=0:
                if self.patro<self.kamjet_kabina[0]:
                    self.smer=1
                elif self.kamjet_kabina[0]<self.patro:
                    self.smer=-1
                self.naplanuj(9,cas+self.rychlost)
                self.cas_provozu+=self.rychlost
                print(str(cas)+" výtah vyjel z patra "+str(self.patro),file=vystup)

            elif len(self.kamjet)!=0:
                if self.patro<self.kamjet[0]:
                    self.smer=1
                elif self.kamjet[0]<self.patro:
                    self.smer=-1
                self.naplanuj(9,cas+self.rychlost)
                self.cas_provozu+=self.rychlost
                print(str(cas)+" výtah vyjel z patra "+str(self.patro),file=vystup)

        elif co==9:# kontroluje jestli někdo vystupuje/nastupuje
            delo_se_neco=False
            seznam_vystupujicich=[]

            if self.smer==1:
                self.patro+=1
            elif self.smer==-1:
                self.patro-=1

            for i in self.uzivatele: # vystup
                if i.kamchce==self.patro:
                    seznam_vystupujicich.append(i)
                    i.strav_vytah+=cas-i.zacatek_cekani
                    i.naplanuj(3,cas)

            for i in seznam_vystupujicich:
                self.uzivatele.remove(i)

            if len(seznam_vystupujicich)!=0 and len(self.uzivatele)!=0:
                delo_se_neco=True

            if self.patro in self.kamjet:
                self.kamjet.remove(self.patro)

            if self.patro in self.kamjet_kabina:
                self.kamjet_kabina.remove(self.patro)

            for j in budova_uradu[self.patro].fronta_vytah:  # nastup
                if len(self.uzivatele) < self.kapacita:
                    if (self.smer==j.smer or len(self.uzivatele)==0):
                        if len(self.uzivatele)==0:
                            self.smer=j.smer
                        self.uzivatele.append(j)
                        j.cekani_vytah+=cas-j.zacatek_cekani
                        j.zacatek_cekani=cas
                        if j.kamchce not in self.kamjet_kabina:
                            self.kamjet_kabina.append(j.kamchce)
                        print(str(cas) + " " + j.jmeno + " nastoupil do výtahu v patře "+str(self.patro),file=vystup)
                        delo_se_neco = True

            for i in self.uzivatele: # odstrani zakazniky z fronty u vytahu
                if i in budova_uradu[self.patro].fronta_vytah:
                    budova_uradu[self.patro].fronta_vytah.remove(i)

            if len(budova_uradu[self.patro].fronta_vytah)!=0:
                self.kamjet.append(self.patro)
            if delo_se_neco:
                self.naplanuj(8,cas+self.nastup)
                self.cas_provozu+=self.nastup
            elif len(self.kamjet_kabina)!=0:
                self.naplanuj(8,cas)
            elif len(self.kamjet)!=0:
                self.naplanuj(8,cas)
            self.smer=0

class Zakaznik:
    def __init__(self,cas_prichodu,jmeno,seznam_jednani):
        self.jmeno=jmeno
        self.jednani=seznam_jednani
        self.prichod=cas_prichodu
        self.patro=0
        self.smer=1
        self.kamchce=seznam_jednani[0][0]
        self.zacatek_cekani=0
        self.cas_na_jednani=0
        self.cekani_jednani=0
        self.cekani_vytah=0
        self.strav_vytah=0
        self.prichazi=False

    def naplanuj(self, co, kdy):
        k.zarad(Udalost(self, co, kdy))

    def zpracujudalost(self,co):
        global vstup,cas,vytah,pocet_lidi,celkovy_cas_cekani_vytah,celkovy_cas_v_budove,celkovy_cas_cekani_jednani,celkovy_cas_ve_vytahu,celkovy_cas_na_jednani
        if co==0: # příchod
            line=vstup.readline().split(" ")
            if line!=[""]:
                jednani = line[2:]
                jednanif = []
                for i in jednani:
                    i = i.split(":")
                    i_ = []
                    for j in i:
                        j = int(j)
                        i_.append(j)
                    jednanif.append(i_)
                z = Zakaznik(int(line[1]), line[0], jednanif)
                z.naplanuj(0,z.prichod)
            self.naplanuj(1,cas+cas_cesty_na_jednani)
            print(str(cas)+" "+self.jmeno+" přichází",file=vystup)

        elif co==1: # zavolat výtah
            self.zacatek_cekani=cas
            if self.patro not in vytah.kamjet:
                vytah.kamjet.append(self.patro)
            budova_uradu[self.patro].fronta_vytah.append(self)
            if not vytah_jede:
                vytah.naplanuj(9,cas)
            print(str(cas)+" "+self.jmeno + " zavolal výtah",file=vystup)

        elif co == 3:  # vystoupit z výtahu
            self.patro=self.kamchce
            self.prichazi=True
            if self.kamchce!=0:
                self.naplanuj(4,cas+cas_cesty_na_jednani)
            else:
                self.naplanuj(6,cas+cas_cesty_na_jednani)
            print(str(cas)+" "+self.jmeno + " vystoupil z výtahu v patře "+str(self.patro),file=vystup)

        elif co == 4:  # začít jednání nebo se přidat do fronty
            if (budova_uradu[self.patro].jednani or (self.prichazi and len(budova_uradu[self.patro].fronta_jednani)!=0)):
                budova_uradu[self.patro].fronta_jednani.append(self)
                self.zacatek_cekani=cas
                self.prichazi=False
                print(str(cas) + " " + self.jmeno + " čeká na jednání",file=vystup)
            else:
                if len(budova_uradu[self.patro].fronta_jednani)!=0:
                    budova_uradu[self.patro].fronta_jednani.pop(0)
                    self.cekani_jednani+=cas-self.zacatek_cekani
                self.naplanuj(5,self.jednani[0][1]+cas)
                self.cas_na_jednani+=self.jednani[0][1]
                budova_uradu[self.patro].jednani=True
                print(str(cas)+" "+self.jmeno + " začal jednání",file=vystup)

        elif co == 5:  # skončit jednání
            self.jednani.pop(0)
            if len(self.jednani)!=0:
                self.kamchce=self.jednani[0][0]
                if self.kamchce<self.patro:
                    self.smer=-1
                else:
                    self.smer=1
            else:
                self.kamchce=0
                self.smer=-1
            self.naplanuj(1, cas+cas_cesty_na_jednani)
            if len(budova_uradu[self.patro].fronta_jednani)!=0:
                dalsi=budova_uradu[self.patro].fronta_jednani[0]
                dalsi.naplanuj(4,cas)
            budova_uradu[self.patro].jednani = False
            print(str(cas)+" "+self.jmeno + " skončil jednání",file=vystup)

        elif co == 6:  # odchod
            print(str(cas)+" "+self.jmeno+" odchazí",file=vystup)
            pocet_lidi+=1
            celkovy_cas_cekani_vytah+=self.cekani_vytah
            celkovy_cas_v_budove+=cas-self.prichod
            celkovy_cas_cekani_jednani+=self.cekani_jednani
            celkovy_cas_ve_vytahu+=self.strav_vytah
            celkovy_cas_na_jednani+=self.cas_na_jednani

budova_uradu = []
pocet_odd=int(input("Zadejte pocet oddeleni:"))
for i in range(pocet_odd+1):
    budova_uradu.append(Oddeleni(i))

kapacita_vytah=int(input("Zadejte maximalni kapacitu vytahu:"))
cas_nastupu_vytah=int(input("Zadejte jak dlouho se nastupuje do vytahu:"))
cas_jizdy_vytah=int(input("Zadejte jak dlouho jede vytah o jedno patro:"))
cas_cesty_na_jednani=int(input("Zadejte jak dlouho trva zakaznikovi dojit od vytahu na jednani:"))

vytah=Vytah(kapacita_vytah,cas_nastupu_vytah,cas_jizdy_vytah)

k=Kalendar()
cas=0
pocet_lidi=0
celkovy_cas_cekani_vytah=0
celkovy_cas_v_budove=0
celkovy_cas_cekani_jednani=0
celkovy_cas_ve_vytahu=0
celkovy_cas_na_jednani=0

vstup=open("zakaznici.txt","r")
line=vstup.readline().split(" ")
jednani=line[2:]
jednanif=[]
for i in jednani:
    i=i.split(":")
    i_=[]
    for j in i:
        j=int(j)
        i_.append(j)
    jednanif.append(i_)

z=Zakaznik(int(line[1]),line[0],jednanif)
z.naplanuj(0,z.prichod)

vystup=open("log.txt","w")

while len(k.kal)!=0:
    vytah_jede=False
    if (len(vytah.kamjet)!=0 or len(vytah.kamjet_kabina)!=0):
        vytah_jede=True
    u = k.prvni()
    cas = u.kdy
    a = u.kdo
    a.zpracujudalost(u.co)
vstup.close()
vystup.close()
print("Prumerny cas straveny v budove uradu "+str(celkovy_cas_v_budove/pocet_lidi))
print("Prumerny cas straveny jednanim "+str(celkovy_cas_na_jednani/pocet_lidi))
print("Prumerny cas straveny cekanim na jednani "+str(celkovy_cas_cekani_jednani/pocet_lidi))
print("Prumerny cas straveny cekanim na vytah "+str(celkovy_cas_cekani_vytah/pocet_lidi))
print("Prumerny cas straveny ve vytahu "+str(celkovy_cas_ve_vytahu/pocet_lidi))
print("Vytah byl v provozu "+str((vytah.cas_provozu/cas)*100)+"% casu")