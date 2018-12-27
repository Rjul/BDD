import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import sqlite3
import time

class BDD :

    def __init__ (self) :
        
        self.fichierDonnees ="/home/rjul/bdd.sq3" ## Localisation de la base de donné
        self.conn =sqlite3.connect(self.fichierDonnees) ## Creation de l'object connect heritier de la localisation
        self.cur =self.conn.cursor()  ## création d'un object cursor heritier de connect


        self.Client = str
        self.REF = str
        self.Machine = str
        self.Designation = str
        self.Temps = float


    def Envoie_info (Client, REF, Designation, Machine, Temps):
        Temps = str(Temps)
        REF = ''' ' ''' + REF + ''' ' '''
        Machine = ''' ' ''' + Machine + ''' ' '''
        Designation = ''' ' ''' + Designation + ''' ' '''
        Temps = ''' ' ''' + Temps + ''' ' '''
        ##ajouter une verification avec retour au menu
        tu = "INSERT INTO "+ Client +" (Refferense, Desig, Machin, Temps) VALUES("+ REF +" , " + Designation + " , "+ Machine + " , "+ Temps + ')' 
        print (tu)
        try:
            BDD1.cur.execute(tu)
            BDD1.conn.commit()
            print("envoie ok")
        except sqlite3.OperationalError:
            print('Erreur la table existe déjà ou des entrer sont incorecte')
        except Exception as e:
            print("Erreur")
            conn.rollback()
        
class MAIN ():

    def __init__ (self) :
        print("INIT")
        self.Refference_ok = False
        self.Selection_client_ok = False
        self.temps_stocage= 1
        self.En_cour = False
        
    def onDestroy(self, *args):
        Gtk.main_quit()

    def Ajoutclient_clicked_cb(self, button):
        print("actualisation liste client")
        Client = ""
        self.text = window.entrer_client.get_text() ### appelle fonction recup text
        window.entrer_client.delete_text(0,120)
        print(self.text)
        
        tu = "CREATE TABLE "+ self.text +" (Refferense TEXT , Desig TEXT, Machin TEXT, Temps TEXT )"
        try:
            BDD1.cur.execute(tu) ## Execution d'une commande sqlite dans la memoir tampon du curseur
            BDD1.conn.commit() ## déclenchement du transfert vers la basse de donnée grace de commit un fonction de l'object connect
        
        except sqlite3.OperationalError:
            print('Erreur le CLIENT existe déjà ou des entrer sont incorecte')
        except Exception as e:
            print("Erreur")
            conn.rollback()


    def actualisation_clicked_cb(self, button):
        print('ajout')
        BDD1.cur.execute("select name from sqlite_master  where type = 'table'")
        liste = tuple
        liste = BDD1.cur.fetchall()       
        print(liste)
        print('ici')
        long = len(liste)
        window.listeclient.remove_all() ## Suprimer les entrer combox client
        
        for l in liste:
            print("1")
            print(l)
            print("2")
            Long2 = len(l)
            print(Long2)
            for v in l :
                print("3")
                
                print(v)## OK pour liste client
                window.listeclient.insert (0,'0', v) ## Entrer client liste
                
    def SelectionCLIENT (self, widget):
        self.ClientSelectionner = window.listeclient.get_active_text()
        print(self.ClientSelectionner)
        self.Selection_client_ok = True
        self.Verif_Condition()

    def debut_clicked_cb (self, button):

        HeurDebut = time.strftime("%A %d %B %Y %H:%M:%S")
        self.debut = time.time()
        print(HeurDebut)
        window.DebutBouton.set_sensitive (False)
        window.PauseBouton.set_sensitive (True)
        window.FinBouton.set_sensitive (True)
        self.En_cour = True
        
    def pause_clicked_cb (self, button):
        self.pause = time.time()
        self.temps = self.pause - self.debut 
        print(self.temps, " Second reprise")
        self.temps_stocage = self.temps_stocage + self.temps
        self.temps_minute = self.temps_stocage/60
        print (self.temps_minute , " minutes total")
        window.DebutBouton.set_label ("Reprendre")
        window.DebutBouton.set_sensitive (True)
        window.PauseBouton.set_sensitive (False)
        window.FinBouton.set_sensitive (True)
        self.En_cour = False

    def fin_clicked_cb (self , button):

        
        self.REF = window.entrer_ref.get_text()
        self.Designation = window.designation.get_text()
        self.Machine = window.machine.get_text()
        

        
        if self.En_cour == False :
            print(self.temps_stocage)
            BDD.Envoie_info(self.ClientSelectionner, self.REF, self.Designation, self.Machine, self.temps_stocage)
            self.Reinisialiser()

        if self.En_cour == True :
            self.pause = time.time()
            self.temps = self.pause - self.debut 
            print(self.temps, " Second reprise")
            self.temps_stocage = self.temps_stocage + self.temps
            print(self.temps_stocage)
            BDD.Envoie_info(self.ClientSelectionner, self.REF, self.Designation, self.Machine, self.temps_stocage)
            self.Reinisialiser()


            
    def Reinisialiser (self):
        window.DebutBouton.set_sensitive (False)
        window.PauseBouton.set_sensitive (False)
        window.FinBouton.set_sensitive (False)
        window.DebutBouton.set_label ("DEBUT")        
        window.entrer_ref.delete_text(0,25444)
        window.designation.delete_text(0,25444)
        window.machine.delete_text(0,25444)
        self.temps_stocage= 1
        

    def Ref_entrer (self , Ref_ajout , long=0 ):
        Refference_ok = True
        print('ref on')
        print(long)
        print(Ref_ajout)
        self.text = window.entrer_ref.get_text()
        print(self.text)
        if len(self.text) == 5:
            self.Refference_ok = True
            self.Verif_Condition()
        else :
            self.Refference_ok = False
            self.Verif_Condition()
        
    def Verif_Condition(self):
        if (self.Refference_ok == True and self.Selection_client_ok == True): window.DebutBouton.set_sensitive (True)
        else : window.DebutBouton.set_sensitive (False)
        
        
builder = Gtk.Builder()
builder.add_from_file("TESTgraphique.glade")
builder.connect_signals(MAIN())

window = builder.get_object("Main1") ### INIT fenetre principal
window.entrer_client = builder.get_object("entrybuffer1")###ajout client INIT entry héritier de fenetre
window.entrer_ref = builder.get_object("entrybuffer3")## recup ref
window.designation = builder.get_object("entrybuffer4")## recup desi
window.machine = builder.get_object("entrybuffer5")## recup machine

window.listeclient = builder.get_object('LISTEclient')

window.DebutBouton = builder.get_object('debut')
window.PauseBouton = builder.get_object('pause')
window.FinBouton = builder.get_object('fin')

window.DebutBouton.set_sensitive (False)
window.PauseBouton.set_sensitive (False)
window.FinBouton.set_sensitive (False)

BDD1 = BDD ()
window.show_all()

Gtk.main()
